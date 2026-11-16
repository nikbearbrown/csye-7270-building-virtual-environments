extends SceneTree
func _initialize():call_deferred("build")
func build():
 var stage=load("res://arena.tscn").instantiate();root.add_child(stage);current_scene=stage
 var converter=load("res://addons/lecture_capture/actions.gd").new()
 for req in JSON.parse_string(FileAccess.get_file_as_string("res://recipe.json")):
  var target=stage.get_node_or_null(NodePath(req.get("node",".")))
  var op=req.op
  if op=="add":
   var child=ClassDB.instantiate(req.class_name);child.name=req.name;target.add_child(child);child.owner=stage
   for key in req.get("properties",{}):child.set(key,converter.value(req.properties[key]))
  elif op=="set":
   var obj=target
   if req.has("resource_property"):obj=obj.get(req.resource_property)
   for key in req.get("resource_chain",[]):obj=obj.get(key)
   obj.set(req.property,converter.value(req.value))
  elif op=="duplicate":
   var copy=target.duplicate();copy.name=req.name;target.get_parent().add_child(copy);copy.owner=stage
   for key in req.get("properties",{}):copy.set(key,converter.value(req.properties[key]))
  elif op=="unique":target.set(req.property,target.get(req.property).duplicate(true))
  elif op=="save_branch":
   var branch=PackedScene.new();branch.pack(target);assert(ResourceSaver.save(branch,req.path)==OK)
 var packed=PackedScene.new();packed.pack(stage);assert(ResourceSaver.save(packed,"res://arena.tscn")==OK)
 print("DIAGNOSTIC FIXTURE built from planned property actions; not editor footage");quit()
