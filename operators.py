"""Operators for Nebula UV Manager."""

from __future__ import annotations

import bmesh
import bpy

from .storage import append_extension_log


def _ensure_edit_mesh(context: bpy.types.Context):
    obj = context.active_object
    if obj is None or obj.type != 'MESH':
        return None

    if context.mode != 'EDIT_MESH':
        bpy.ops.object.mode_set(mode='EDIT')

    return obj


def _get_active_bmesh_uv_layer(bm, mesh) -> object | None:
    if not mesh.uv_layers.active:
        return None

    uv_layer_name = mesh.uv_layers.active.name
    uv_layer = bm.loops.layers.uv.get(uv_layer_name)
    if uv_layer is None:
        uv_layer = bm.loops.layers.uv.verify()
    return uv_layer


class NEBULAUVMANAGER_OT_reset_selected_scale(bpy.types.Operator):
    """Reset scale to 1.0 for selected editable objects"""

    bl_idname = "nebula_uv_manager.reset_selected_scale"
    bl_label = "Reset Selected Scale"
    bl_options = {'REGISTER', 'UNDO'}

    only_unapplied: bpy.props.BoolProperty(
        name="Only Unapplied",
        description="Only reset objects that are not already 1,1,1 scale",
        default=True,
    )

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        return (
            context.mode == 'OBJECT'
            and context.selected_objects is not None
            and any(obj.library is None for obj in context.selected_objects)
        )

    def execute(self, context: bpy.types.Context) -> set[str]:
        editable = [
            obj
            for obj in context.selected_objects
            if obj.library is None and hasattr(obj, "scale")
        ]

        if not editable:
            self.report({'WARNING'}, "No editable selected objects")
            return {'CANCELLED'}

        changed_count = 0
        eps = 1e-6

        for obj in editable:
            if self.only_unapplied:
                if all(abs(axis - 1.0) <= eps for axis in obj.scale):
                    continue
            obj.scale = (1.0, 1.0, 1.0)
            changed_count += 1

        self.report({'INFO'}, f"Reset scale on {changed_count} object(s)")

        addon_entry = context.preferences.addons.get(__package__)
        prefs = addon_entry.preferences if addon_entry else None
        if prefs and prefs.write_operation_log:
            append_extension_log(f"reset_selected_scale changed={changed_count}")

        return {'FINISHED'}


class NEBULAUVMANAGER_OT_uv_auto_pack(bpy.types.Operator):
    """Pack UV islands for the active mesh in edit mode."""

    bl_idname = "nebula_uv_manager.uv_auto_pack"
    bl_label = "UV Auto Pack"
    bl_options = {'REGISTER', 'UNDO'}

    margin: bpy.props.FloatProperty(
        name="Margin",
        description="UV island spacing",
        default=0.01,
        min=0.0,
        max=0.5,
        subtype='DISTANCE',
    )
    rotate: bpy.props.BoolProperty(
        name="Rotate Islands",
        description="Allow Blender to rotate islands while packing",
        default=False,
    )

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        obj = context.active_object
        return obj is not None and obj.type == 'MESH'

    def execute(self, context: bpy.types.Context) -> set[str]:
        obj = _ensure_edit_mesh(context)
        if obj is None:
            self.report({'WARNING'}, "Select a mesh object first")
            return {'CANCELLED'}

        if not obj.data.uv_layers.active:
            self.report({'WARNING'}, "This mesh has no active UV map")
            return {'CANCELLED'}

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.pack_islands(rotate=self.rotate, margin=self.margin)
        self.report({'INFO'}, "Packed UV islands")
        return {'FINISHED'}


class NEBULAUVMANAGER_OT_uv_checker(bpy.types.Operator):
    """Run a basic UV validation pass and select problematic faces."""

    bl_idname = "nebula_uv_manager.uv_checker"
    bl_label = "UV Checker"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        obj = context.active_object
        return obj is not None and obj.type == 'MESH'

    def execute(self, context: bpy.types.Context) -> set[str]:
        obj = _ensure_edit_mesh(context)
        if obj is None:
            self.report({'WARNING'}, "Select a mesh object first")
            return {'CANCELLED'}

        if not obj.data.uv_layers.active:
            self.report({'WARNING'}, "This mesh has no active UV map")
            return {'CANCELLED'}

        bm = bmesh.from_edit_mesh(obj.data)
        bm.faces.ensure_lookup_table()
        uv_layer = _get_active_bmesh_uv_layer(bm, obj.data)
        if uv_layer is None:
            self.report({'WARNING'}, "This mesh has no active UV map")
            return {'CANCELLED'}

        selected_faces = [face for face in bm.faces if face.select]
        if not selected_faces:
            selected_faces = list(bm.faces)

        problem_faces = set()
        issue_count = 0

        for face in selected_faces:
            uv_coords = [loop[uv_layer].uv for loop in face.loops]
            face_issues = []

            for uv in uv_coords:
                if not (uv.x == uv.x and uv.y == uv.y):
                    face_issues.append("non-finite")
                    break
                if uv.x < -1e-4 or uv.x > 1.0001 or uv.y < -1e-4 or uv.y > 1.0001:
                    face_issues.append("out-of-range")
                    break

            if not face_issues:
                area_sum = 0.0
                for index, uv in enumerate(uv_coords):
                    next_uv = uv_coords[(index + 1) % len(uv_coords)]
                    area_sum += uv.x * next_uv.y - next_uv.x * uv.y
                if abs(area_sum) < 1e-6:
                    face_issues.append("degenerate")

            if face_issues:
                problem_faces.add(face.index)
                issue_count += 1

        for face in selected_faces:
            if face.index in problem_faces:
                face.select_set(True)
            else:
                face.select_set(False)

        bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)

        if issue_count:
            self.report({'WARNING'}, f"Found {issue_count} face(s) with UV issues")
        else:
            self.report({'INFO'}, "No UV issues found")
        return {'FINISHED'}


class NEBULAUVMANAGER_OT_uv_symmetry_mirror(bpy.types.Operator):
    """Mirror selected UV coordinates across the chosen axis."""

    bl_idname = "nebula_uv_manager.uv_symmetry_mirror"
    bl_label = "Mirror UVs"
    bl_options = {'REGISTER', 'UNDO'}

    axis: bpy.props.EnumProperty(
        name="Axis",
        items=[('U', 'U', 'Mirror along the U axis'), ('V', 'V', 'Mirror along the V axis')],
        default='U',
    )
    center: bpy.props.FloatProperty(
        name="Center",
        description="Mirror center line",
        default=0.5,
        min=0.0,
        max=1.0,
    )

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        obj = context.active_object
        return obj is not None and obj.type == 'MESH'

    def execute(self, context: bpy.types.Context) -> set[str]:
        obj = _ensure_edit_mesh(context)
        if obj is None:
            self.report({'WARNING'}, "Select a mesh object first")
            return {'CANCELLED'}

        if not obj.data.uv_layers.active:
            self.report({'WARNING'}, "This mesh has no active UV map")
            return {'CANCELLED'}

        bm = bmesh.from_edit_mesh(obj.data)
        bm.faces.ensure_lookup_table()
        uv_layer = _get_active_bmesh_uv_layer(bm, obj.data)
        if uv_layer is None:
            self.report({'WARNING'}, "This mesh has no active UV map")
            return {'CANCELLED'}

        changed_count = 0

        for face in bm.faces:
            for loop in face.loops:
                luv = loop[uv_layer]
                if not luv.select:
                    continue
                if self.axis == 'U':
                    luv.uv.x = self.center * 2.0 - luv.uv.x
                else:
                    luv.uv.y = self.center * 2.0 - luv.uv.y
                changed_count += 1

        bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
        self.report({'INFO'}, f"Mirrored {changed_count} UV coordinate(s)")
        return {'FINISHED'}


class NEBULAUVMANAGER_OT_uv_unwrap_preset(bpy.types.Operator):
    """Apply a simple UV unwrap preset to selected faces."""

    bl_idname = "nebula_uv_manager.uv_unwrap_preset"
    bl_label = "UV Unwrap Preset"
    bl_options = {'REGISTER', 'UNDO'}

    preset: bpy.props.EnumProperty(
        name="Preset",
        items=[
            ('SMART', 'Smart UV Project', 'Use Smart UV Project'),
            ('CUBE', 'Cube Projection', 'Use Cube Projection'),
            ('PLANAR', 'Planar Projection', 'Use Planar Projection'),
            ('CYLINDER', 'Cylinder Projection', 'Use Cylinder Projection'),
            ('SPHERE', 'Sphere Projection', 'Use Sphere Projection'),
            ('UNWRAP', 'Unwrap', 'Use standard UV unwrap'),
        ],
        default='SMART',
    )

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        obj = context.active_object
        return obj is not None and obj.type == 'MESH'

    def execute(self, context: bpy.types.Context) -> set[str]:
        obj = _ensure_edit_mesh(context)
        if obj is None:
            self.report({'WARNING'}, "Select a mesh object first")
            return {'CANCELLED'}

        if not obj.data.uv_layers.active:
            self.report({'WARNING'}, "This mesh has no active UV map")
            return {'CANCELLED'}

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.select_all(action='SELECT')

        preset = self.preset
        if not preset:
            preset = context.scene.nebula_uv_manager_unwrap_preset

        if preset == 'CUBE':
            bpy.ops.uv.cube_project()
        elif preset == 'PLANAR':
            bpy.ops.uv.project_from_view(mode='VIEW_ON_EACH', correct_aspect=True)
        elif preset == 'CYLINDER':
            bpy.ops.uv.cylinder_project()
        elif preset == 'SPHERE':
            bpy.ops.uv.sphere_project()
        elif preset == 'UNWRAP':
            bpy.ops.uv.unwrap()
        else:
            bpy.ops.uv.smart_project()

        self.report({'INFO'}, f"Applied {preset.lower()} UV preset")
        return {'FINISHED'}
