"""UI panels for Nebula UV Manager."""

from __future__ import annotations

import bpy

from .storage import get_extension_user_dir


class NEBULAUVMANAGER_PT_tools(bpy.types.Panel):
    """Tool panel in the 3D View sidebar"""

    bl_label = "Nebula UV Manager"
    bl_idname = "NEBULAUVMANAGER_PT_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Nebula UV Manager'

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        col = layout.column(align=True)

        col.label(text="Scale Utilities")
        col.operator("nebula_uv_manager.reset_selected_scale")

        col.separator()
        col.label(text="UV Tools")
        col.operator("nebula_uv_manager.uv_auto_pack")
        col.operator("nebula_uv_manager.uv_checker")
        col.operator("nebula_uv_manager.uv_symmetry_mirror")

        box = col.box()
        box.label(text="Unwrap Presets")
        row = box.row()
        row.prop(context.scene, "nebula_uv_manager_unwrap_preset", text="")
        box.operator("nebula_uv_manager.uv_unwrap_preset")

        user_dir = get_extension_user_dir(create=False)
        col.separator()
        col.label(text="User data folder:")
        col.label(text=user_dir)
