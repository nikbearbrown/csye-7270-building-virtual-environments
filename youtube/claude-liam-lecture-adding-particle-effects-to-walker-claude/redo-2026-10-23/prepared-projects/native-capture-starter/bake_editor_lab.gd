extends SceneTree
func _initialize():call_deferred("run")
func own(node,root_node):
 for c in node.get_children():
  c.owner=root_node
  own(c,root_node)
func strip_scripts(node):
 for c in node.get_children():strip_scripts(c)
 if node.get_script()!=null:node.set_script(null)
func run():
 var game=load("res://signal-garden/main.tscn").instantiate();game.audio_enabled=false;root.add_child(game);await process_frame
 for child in game.get_children():
  if child is CanvasLayer or child is CPUParticles3D or child.name in ["DecorativeMarkers"]:child.free()
 strip_scripts(game);game.name="SignalGardenEditorLab";game.set_script(load("res://editor_stage.gd"));own(game,game)
 var title=Label3D.new();title.name="LectureTitle";title.text="Signal Garden · derived editor lab";title.position=Vector3(0,4.3,0);title.font_size=48;title.pixel_size=.006;title.billboard=BaseMaterial3D.BILLBOARD_ENABLED;game.add_child(title);title.owner=game
 var scene=PackedScene.new();scene.pack(game);ResourceSaver.save(scene,"res://arena.tscn")
 game.queue_free();await process_frame;print("Derived editor lab baked from current Signal Garden geometry; not historical source");quit()
