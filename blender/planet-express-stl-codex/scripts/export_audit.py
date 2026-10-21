import bpy,json,math,hashlib,struct
from pathlib import Path
from mathutils import Vector
R=Path('/Users/bear/Downloads/planet-express-stl-build');s=bpy.context.scene
root=bpy.data.objects.get('Planet Express • master')
if not root:root=bpy.data.objects.new('Planet Express • master',None);s.collection.objects.link(root)
meshes=[o for o in s.objects if o.type=='MESH' and not o.hide_render and not any(c.hide_render for c in o.users_collection)]
for o in meshes:
 mw=o.matrix_world.copy();o.parent=root;o.matrix_world=mw;o['export_part']=True
for o in s.objects:
 if o.type=='MESH' and o not in meshes:o['export_part']=False
tri=0;coords=[]
for o in meshes:
 o.data.calc_loop_triangles();tri+=len(o.data.loop_triangles);coords += [o.matrix_world@v.co for v in o.data.vertices]
a={'blender':bpy.app.version_string,'mesh_objects':len(meshes),'triangles':tri,'materials':len({m.name for o in meshes for m in o.data.materials if m}),'dimensions_mm':[round(max(v[k] for v in coords)-min(v[k] for v in coords),4) for k in range(3)],'bounds_mm':[[min(v[k] for v in coords) for k in range(3)],[max(v[k] for v in coords) for k in range(3)]],'accessory_meshes':len([o for o in s.objects if o.type=='MESH' and o not in meshes]),'source_triangles':737487,'source_files':26,'reference_rounds_documented':3,'finite_vertices':all(math.isfinite(x) for o in meshes for v in o.data.vertices for x in v.co),'geometry_creator':'GOODesign / GOODesignLabs','builder':'Codex (assembly, materials, added antenna and lettering)','human_review':'Professor Bear: pending'}
(R/'audit.json').write_text(json.dumps(a,indent=2))
transforms={o.name:{'source_file':o.get('source_file'),'export_part':o.get('export_part'),'matrix_world':[list(row) for row in o.matrix_world]} for o in s.objects if o.type=='MESH'}
(R/'assembly-transforms.json').write_text(json.dumps(transforms,indent=2))
for o in s.objects:o.select_set(False)
for o in meshes:o.select_set(True)
root.select_set(True);bpy.context.view_layer.objects.active=root
# Native numeric coordinates are millimeters; export them as meters explicitly.
root.scale=(.001,.001,.001);s.unit_settings.scale_length=1
bpy.ops.export_scene.gltf(filepath=str(R/'planet-express-ship.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=False,export_extras=True)
root.scale=(1,1,1);s.unit_settings.scale_length=.001
# Save an uncluttered opening viewport.
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   sp=area.spaces.active;sp.overlay.show_overlays=False;sp.clip_end=2000;sp.shading.type='MATERIAL';sp.region_3d.view_perspective='CAMERA'
s.camera=bpy.data.objects['View • hero']
for o in s.objects:o.select_set(False)
root.select_set(True);bpy.context.view_layer.objects.active=root
bpy.ops.wm.save_as_mainfile(filepath=str(R/'planet-express-ship.blend'),compress=True)
b=(R/'planet-express-ship.glb').read_bytes();length,kind=struct.unpack_from('<II',b,12);g=json.loads(b[20:20+length]);(R/'glb-structure.json').write_text(json.dumps({'bytes':len(b),'meshes':len(g.get('meshes',[])),'materials':len(g.get('materials',[])),'images':len(g.get('images',[])),'animations':len(g.get('animations',[])),'extensions_used':g.get('extensionsUsed',[])},indent=2))
print(json.dumps(a))
