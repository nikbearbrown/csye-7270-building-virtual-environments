# The exporter's own UI labels and defaults (Blender 5.1.2 bundled io_scene_gltf2): what the Export dialog calls these options.
import bpy
props = bpy.ops.export_scene.gltf.get_rna_type().properties
for k in ("export_yup", "export_apply", "export_lights", "export_format", "export_materials"):
    p = props[k]
    print(f"{k}: label={p.name!r} default={getattr(p,'default',None)!r}")
print("LABELS_DONE")
