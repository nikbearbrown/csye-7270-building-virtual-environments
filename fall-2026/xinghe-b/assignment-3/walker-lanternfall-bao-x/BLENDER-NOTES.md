# Blender window notes — Assignment 3

## Hand edit — OilGem, 2026-10-14

**What I saw.** I selected `OilGem` in the Outliner. After I rotated it, the
Item panel on the right showed Z rotation 20°. After I applied the rotation,
Z rotation read 0° again, but the gem kept its new orientation; it did not
turn back.

**What I changed.** I rotated `OilGem` 20° around the Z axis, applied it with
**Ctrl+A → Rotation**, saved `blender/a3/oil_shrine.blend`, and re-exported
`godot/a3/oil_shrine.glb` with **File > Export**.

**What I learned.**

- The Outliner selects an object exactly, by name.
- A shortcut can rotate around a chosen axis by a typed angle (`R`, `Z`, `20`).
- Applying a rotation does not undo the visible turn. It writes the turn into
  the mesh data, which is why the object's rotation value returns to zero.
- That keeps the model at a unit transform when Godot imports it, so
  orientation and scale problems do not appear later.
- After the re-export, every test still passed.

**Consequence for the repository.** `blender/a3/oil_shrine.blend` is now the
shrine's source. `tools/blender/build_oil_shrine.py` rebuilds only the
pre-edit MCP version and would overwrite this edit if run.

## Six parts of the interface

1. **3D Viewport**: the main area for viewing and editing models. I used it to
   look at `OilGem` and confirm how it looked after the rotation.
2. **Outliner**: the list of objects in the scene. I used it to select
   `OilGem` exactly, by name.
3. **Toolbar**: the select, move, rotate and scale tools on the left. I used
   its rotate function to change the object's direction.
4. **Sidebar (N panel)**: shows the object's location, rotation, scale and
   dimensions. I used it to confirm that Z first became 20° and went back to
   0° after I applied the rotation.
5. **Properties Editor**: the area that manages object, material and scene
   settings. I used it to check the object's settings and the glowing
   material.
6. **Mode Selector**: switches between Object Mode and Edit Mode. I stayed in
   Object Mode to rotate and apply the whole `OilGem` object.

## What the window exercise established

- Blender uses +Z as up. With `+Y Up` enabled, the glTF exporter converts this
  to Godot's +Y-up convention.
- A default cube has scale `(1, 1, 1)` and dimensions `2 x 2 x 2 m`. The brief
  is measured in dimensions.
- **Ctrl+A → Scale** keeps the visible dimensions and bakes the scale back to
  one, so Godot receives no unexpected transforms.
- Scene Statistics reports vertices, faces and triangles. The assignment
  limits triangles and the number of visible primitives; the Outliner's object
  count alone does not show either.

## Evidence

- `evidence/a3/blender-interface-session.png` is my screenshot of the
  Blender 5.2.2 learning session. It shows the cube selected, the `N`
  sidebar open with unit scale and 2 m dimensions, and Scene Statistics on
  (12 triangles).
- Measured check of the hand edit: rotating the MCP export's gem vertices by
  20.0° about Blender Z reproduces the re-exported gem to within 1.84e-8 m.
  The gem has 72° symmetry, so the angle is unique only up to that symmetry.
  Its node in the GLB has no rotation or scale.
