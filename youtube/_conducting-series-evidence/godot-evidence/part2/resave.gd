extends SceneTree
func _initialize() -> void:
	var p := load("res://pong.tscn") as PackedScene
	var root := p.instantiate()
	var again := PackedScene.new()
	again.pack(root)
	var err := ResourceSaver.save(again, "/private/tmp/claude-501/godot-evidence-work/resave/pong.resaved.tscn")
	print("ResourceSaver.save -> ", error_string(err))
	root.free()
	quit(0)
