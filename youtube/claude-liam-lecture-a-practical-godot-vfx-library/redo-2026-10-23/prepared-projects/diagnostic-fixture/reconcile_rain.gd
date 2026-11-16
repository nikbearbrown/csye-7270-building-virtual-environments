extends SceneTree
func _initialize():call_deferred("run")
func own(node,base):
 for c in node.get_children():c.owner=base;own(c,base)
func run():
 var stage=load("res://arena.tscn").instantiate();root.add_child(stage)
 var old=stage.get_node("Rain");var where=old.transform;var show=old.visible;old.free()
 var fixed=load("res://effects/rain.tscn").instantiate();fixed.name="Rain";stage.add_child(fixed);fixed.transform=where;fixed.visible=show;fixed.owner=stage;own(fixed,stage)
 var packed=PackedScene.new();assert(packed.pack(stage)==OK);assert(ResourceSaver.save(packed,"res://arena.tscn")==OK)
 assert(fixed.get_node("Ground").size==Vector3(10,2,10));assert(fixed.get_node("Splash").process_material.collision_mode==1)
 print("Embedded Rain reconciled with checked saved scene; visual capture pending")
 stage.queue_free();await process_frame;quit()
