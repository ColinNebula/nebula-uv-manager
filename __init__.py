"""Nebula UV Manager extension entry point."""

import bpy

from .operators import (
    NEBULAUVMANAGER_OT_reset_selected_scale,
    NEBULAUVMANAGER_OT_uv_auto_pack,
    NEBULAUVMANAGER_OT_uv_checker,
    NEBULAUVMANAGER_OT_uv_symmetry_mirror,
    NEBULAUVMANAGER_OT_uv_unwrap_preset,
)
from .panels import NEBULAUVMANAGER_PT_tools
from .preferences import NEBULAUVMANAGER_Preferences

classes = (
    NEBULAUVMANAGER_Preferences,
    NEBULAUVMANAGER_OT_reset_selected_scale,
    NEBULAUVMANAGER_OT_uv_auto_pack,
    NEBULAUVMANAGER_OT_uv_checker,
    NEBULAUVMANAGER_OT_uv_symmetry_mirror,
    NEBULAUVMANAGER_OT_uv_unwrap_preset,
    NEBULAUVMANAGER_PT_tools,
)


def register() -> None:
    bpy.types.Scene.nebula_uv_manager_unwrap_preset = bpy.props.EnumProperty(
        name="Unwrap Preset",
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

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister() -> None:
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.nebula_uv_manager_unwrap_preset


if __name__ == "__main__":
    register()
