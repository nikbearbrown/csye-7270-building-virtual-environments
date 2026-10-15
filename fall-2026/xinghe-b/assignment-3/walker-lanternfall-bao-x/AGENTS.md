# Project checks

## Checks

Rebuild the Lantern Gate and Supply Stack with:

```bash
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_lantern_gate.py
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_supply_stack.py
```

Do not run `tools/blender/build_oil_shrine.py` unless asked: the Lamp-oil
Shrine was hand-edited in Blender after its MCP build, so
`blender/a3/oil_shrine.blend` is its source and the script would overwrite the
edit. Re-export the shrine from that `.blend` (glTF Binary, +Y Up, Apply
Modifiers, materials exported) to `godot/a3/oil_shrine.glb`.

`tools/blender/build_<asset>.py` holds the Blender MCP `execute_blender_code`
bodies, verbatim and in order; it also runs headless. The pre-MCP headless
scripts are kept in `tools/blender/script_route/`. In a live Blender reached
through the MCP, never call `bpy.ops.wm.read_factory_settings`: it resets
preferences and drops the add-on connection. Clear scenes through `bpy.data`.

Import and test with:

```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --path godot --import
gtimeout 120 /Applications/Godot.app/Contents/MacOS/Godot --headless --path godot --script res://tests/test_a3_assets.gd --fixed-fps 60
gtimeout 120 /Applications/Godot.app/Contents/MacOS/Godot --headless --path godot --script res://tests/test_lantern_gate.gd --fixed-fps 60
gtimeout 120 /Applications/Godot.app/Contents/MacOS/Godot --headless --path godot --script res://tests/test_a3_camera.gd --fixed-fps 60
```

Rendered captures need a window, not `--headless` (a headless run never
reaches `frame_post_draw`):
`/Applications/Godot.app/Contents/MacOS/Godot --path godot --resolution 1280x720 --script res://tests/capture_a3_orbit.gd`

Do not hand-write `.import` files or invent Godot UIDs. Do not change existing
2D movement tuning, audio rules, or earlier tests to make an A3 check pass.
