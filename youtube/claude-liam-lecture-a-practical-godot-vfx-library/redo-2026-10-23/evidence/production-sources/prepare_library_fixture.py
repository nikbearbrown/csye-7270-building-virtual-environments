from pathlib import Path
import json
from make_film4 import b
w=Path('work-4');(w/'recipe.json').write_text(json.dumps([x for row in b for x in row['actions']],indent=2))
(w/'build_fixture.gd').write_text('''extends SceneTree
var stage:Node
var current_path:="res://arena.tscn"
var converter=load("res://addons/lecture_capture/actions.gd").new()
func _initialize():call_deferred("build")
func save_current():
 var packed=PackedScene.new();packed.pack(stage);assert(ResourceSaver.save(packed,current_path)==OK)
func put(obj,key,v):
 var found=key.begins_with("metadata/")
 for property in obj.get_property_list():
  if property.name==key:found=true
 assert(found,"Unknown property "+obj.get_class()+"."+key)
 obj.set(key,converter.value(v))
func build():
 stage=load(current_path).instantiate();root.add_child(stage);current_scene=stage
 for req in JSON.parse_string(FileAccess.get_file_as_string("res://recipe.json")):
  var op=req.op
  if op=="open":
   save_current();stage.free();current_path=req.path;stage=ResourceLoader.load(current_path,"",ResourceLoader.CACHE_MODE_IGNORE).instantiate();root.add_child(stage);current_scene=stage;continue
  var target=stage.get_node_or_null(NodePath(req.get("node",".")))
  if op in ["view3d","script","play_custom","game_input","stop","select","resource","zoom","save"]:continue
  assert(target!=null,"Missing node "+req.get("node","."))
  if op=="add":
   var child=ClassDB.instantiate(req.class_name);child.name=req.name;target.add_child(child);child.owner=stage
   for key in req.get("properties",{}):put(child,key,req.properties[key])
  elif op=="set":
   var obj=target
   if req.has("resource_property"):obj=obj.get(req.resource_property)
   for key in req.get("resource_chain",[]):obj=obj.get(key)
   put(obj,req.property,req.value)
  elif op=="duplicate":
   var copy=target.duplicate();copy.name=req.name;target.get_parent().add_child(copy);copy.owner=stage
   for key in req.get("properties",{}):put(copy,key,req.properties[key])
  elif op=="unique":target.set(req.property,target.get(req.property).duplicate(true))
  elif op=="unique_surface":
   var old=target.draw_pass_1;var mesh=old.duplicate(false);mesh.material=old.material.duplicate(false);target.draw_pass_1=mesh
   assert(mesh.material.albedo_texture==old.material.albedo_texture)
  elif op=="save_branch":
   var copy=target.duplicate();converter.own_children(copy,copy);var branch=PackedScene.new();branch.pack(copy);assert(ResourceSaver.save(branch,req.path)==OK);copy.free()
  elif op=="call":target.callv(req.method,req.get("args",[]))
 save_current();stage.queue_free();await process_frame
 print("DIAGNOSTIC LIBRARY FIXTURE saved; native editor capture still required");quit()
''')
