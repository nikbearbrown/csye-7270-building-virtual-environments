"""Blender -b seis-bot-v005-codex.blend --python scripts/export_glb.py -- out.glb
Exports visible objects only (hidden SOURCE_GEOMETRY excluded). Procedural Cycles materials do not export: flat base colours only."""
import sys, bpy
out = sys.argv[sys.argv.index("--") + 1]
bpy.ops.export_scene.gltf(filepath=out, export_format="GLB", use_visible=True, export_apply=True, export_cameras=False, export_lights=False)
