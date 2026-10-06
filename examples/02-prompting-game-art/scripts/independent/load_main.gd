extends SceneTree
func _initialize() -> void:
	var ps = load("res://game/main.tscn")
	print("main.tscn loaded: ", ps != null)
	quit(0 if ps != null else 1)
