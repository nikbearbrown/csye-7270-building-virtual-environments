extends SceneTree
var view: SubViewport
var lab: Node2D
var frame := 0
var output := ""
func _initialize() -> void:
	output=OS.get_cmdline_user_args()[0]
	DirAccess.make_dir_recursive_absolute(output)
	view=SubViewport.new();view.size=Vector2i(3840,2160)
	view.render_target_update_mode=SubViewport.UPDATE_ALWAYS
	root.add_child(view)
	var scale_root=Node2D.new();scale_root.scale=Vector2(3,3);view.add_child(scale_root)
	lab=load("res://render_game.tscn").instantiate();scale_root.add_child(lab)
func _process(_delta: float) -> bool:
	frame+=1
	if frame<60:return false
	RenderingServer.force_draw(false)
	var im=view.get_texture().get_image()
	im.save_png(output.path_join("frame-%04d.png"%(frame-60)))
	if frame>=149:
		print("NATIVE_4K_FRAMES=90 RESOLUTION=",im.get_size())
		quit()
	return false
