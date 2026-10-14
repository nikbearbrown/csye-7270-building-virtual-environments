# assignment-3

Assignment 3 — Your First 3D Game Assets with Claude, the Blender MCP, and Blender. Put this assignment's work and its own `FRICTIONAL.md` here.

- **Project:** [`walker-ninja-firefighter-joe-3d/`](walker-ninja-firefighter-joe-3d/): three simple 3D props for my Assignment 2 game (Extinguisho, the ninja firefighter), built in Blender through the Blender MCP, exported as `.glb`, and shown together in a small Godot 3D scene.
- **Assets:** fire hydrant · rescue bag · rooftop ledge.
- **Design docs**, committed before any building: [BLENDER-NOTES](walker-ninja-firefighter-joe-3d/BLENDER-NOTES.md) · [CHANGE-BRIEF](walker-ninja-firefighter-joe-3d/CHANGE-BRIEF.md)
- **Log:** [FRICTIONAL.md](FRICTIONAL.md)

## Folder layout

| Folder | What goes in it |
|---|---|
| `tools/blender/` | `build_<asset>.py`: every piece of code Claude ran in Blender, one file per asset |
| `blender/` | the saved `.blend` files (no `.blend1` backups) |
| `exports/` | the `.glb` exports (+Y Up) |
| `godot/` | the Godot 4 project with the 3D scene and the headless check script |
| `evidence/` | screenshots and check output |
