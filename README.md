# Nebula UV Manager

Nebula UV Manager is a Blender add-on designed to make UV work faster, cleaner, and more repeatable for modeling, texturing, and asset preparation. It focuses on practical tools for packing islands, checking UV quality, mirroring coordinates, and applying common unwrap presets directly inside Blender.

## Purpose

This add-on helps artists and technical modelers:

- speed up UV layout workflows
- reduce texture stretching and invalid UV states
- quickly apply common unwrap methods
- keep UV work organized for baking, game assets, and texture painting

It is built for Blender 4.2+ and 5.x using the extension workflow.

## Complete Feature Breakdown

### 1. UV Auto Pack
- Packs selected UV islands automatically.
- Useful for quickly laying out islands for texture space.
- Includes a margin setting for spacing between islands.

### 2. UV Checker
- Scans the active UV map for common issues.
- Highlights faces that may have:
  - non-finite UV coordinates
  - UV values outside the expected 0 to 1 range
  - degenerate UV faces
- Selected faces are marked so you can inspect and fix them quickly.

### 3. UV Symmetry Mirror
- Mirrors selected UV coordinates across the chosen axis.
- Helpful for symmetrical assets, especially hard-surface models and organic forms.
- Supports mirroring along U or V.

### 4. Unwrap Presets
- Includes a preset selector for:
  - Smart UV Project
  - Cube Projection
  - Planar Projection
  - Cylinder Projection
  - Sphere Projection
  - Standard Unwrap
- Great for fast setup before manually refining UVs.

### 5. Sidebar Panel
- Adds a dedicated panel in the 3D View sidebar.
- Keeps the main UV tools visible and easy to access.
- Includes a preset chooser so you can pick the unwrap method without deep menu navigation.

### 6. Extension Preferences
- Supports extension-safe preferences for future configuration growth.
- Keeps user data flowing through Blender’s extension storage path.

## Installation

1. Build the extension zip file:
   - Open PowerShell in the project folder.
   - Run:
     ```powershell
     .\build-extension.ps1
     ```
2. In Blender:
   - Open Preferences > Extensions.
   - Click Install from Disk.
   - Select the generated zip file.
3. Enable the add-on from the Extensions panel.

## Setup

After installation:

1. Open the 3D View.
2. Go to the sidebar panel.
3. Select the object you want to work on.
4. Enter Edit Mode and make sure the mesh has a UV map.

For best results:
- work on a mesh with an active UV map
- select the faces or islands you want to process
- make sure the object is in Edit Mode before running UV tools

## Step-by-Step Usage

### Using UV Auto Pack
1. Select the mesh object.
2. Enter Edit Mode.
3. Select the faces or islands to pack.
4. Click UV Auto Pack in the panel.
5. Adjust the margin if needed and run again.

### Using UV Checker
1. Select the mesh object.
2. Enter Edit Mode.
3. Choose the faces you want to validate.
4. Click UV Checker.
5. Any problematic faces will be selected so you can inspect them.

### Using UV Symmetry Mirror
1. Select the UVs you want to mirror.
2. Choose U or V as the mirror axis.
3. Click Mirror UVs.
4. Review the mirrored result and refine manually if needed.

### Using Unwrap Presets
1. Select the mesh object.
2. Enter Edit Mode.
3. Select the faces to unwrap.
4. Choose a preset from the panel.
5. Click the unwrap button to apply it.

## Pro Workflow Tips

- Start with a simple unwrap preset, then refine manually.
- Use UV Checker before baking to catch obvious problems early.
- Use Auto Pack after your islands are roughly placed.
- Keep symmetry in mind for hard-surface assets and character work.
- Save a backup of your mesh before heavy UV edits if you are working on a production asset.
- For game assets, keep UV islands organized and avoid unnecessary stretching.
- For texture painting, aim for clear island spacing and consistent texel density.

## Troubleshooting

### The add-on does not appear
- Make sure the extension zip was installed correctly.
- Confirm the add-on is enabled in Blender Preferences > Extensions.
- Restart Blender if the panel does not appear after installation.

### UV Checker fails
- Ensure you are in Edit Mode.
- Make sure the mesh has an active UV map.
- Select at least one face or island.

### Unwrap preset does nothing
- Confirm the object is a mesh.
- Make sure the mesh is editable and has faces selected.
- Check that the view and selection are correct before running the operator.

### The panel looks incomplete
- Reload the add-on or restart Blender.
- Verify that the extension was built and installed from the latest zip file.

## Support

If you want to support Colin Nebula and the continued development of tools like this, you can donate here:

- GitHub: https://github.com/sponsors/ColinNebula
- PayPal: https://paypal.me/ColinNebula
- Ko-fi: https://ko-fi.com/colinnebula

Support / Contact:
- Email: support@nebula3ddev.com
- Website: https://www.nebula3ddev.com

## Development Notes

This add-on is intentionally lightweight and focused on UV utility workflows. It is a solid starting point for future expansion into:

- better UV packing controls
- island alignment helpers
- texel density tools
- baking helpers
- batch UV processing

## Privacy and Security

- The add-on does not make any network calls.
- The add-on does not collect analytics or telemetry.
- Optional operation logging is disabled by default.
- If enabled, logs are stored only in Blender's extension user-data path.

If you discover a security issue, do not open a public issue first. Please report it privately to:
- support@nebula3ddev.com

## GitHub Release Checklist

Use this flow before publishing a release:

1. Ensure version is updated in `blender_manifest.toml`.
2. Run Blender extension validation and build:
  ```powershell
  .\build-extension.ps1
  ```
3. Install the generated zip in Blender and smoke-test core operators.
4. Create a Git tag that matches the release version (example: `v0.1.1`).
5. Push commits and tags to GitHub.
6. Create a GitHub Release and attach the built extension zip.

## Recommended Repository Protection

For a public repository, enable these GitHub settings:

- Branch protection on `main` (require pull request before merge).
- Require status checks before merge.
- Block force pushes and branch deletion.
- Enable Dependabot alerts and secret scanning.
- Enable two-factor authentication on maintainer accounts.
