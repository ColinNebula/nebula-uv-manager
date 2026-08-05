"""Preferences for Nebula UV Manager."""

from __future__ import annotations

import bpy


class NEBULAUVMANAGER_Preferences(bpy.types.AddonPreferences):
    """Add-on preferences for extension-safe configuration."""

    # Use package namespace for extension compatibility.
    bl_idname = __package__

    write_operation_log: bpy.props.BoolProperty(
        name="Write Operation Log",
        description="Write basic operation events into the extension user folder",
        default=False,
    )

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        layout.prop(self, "write_operation_log")
