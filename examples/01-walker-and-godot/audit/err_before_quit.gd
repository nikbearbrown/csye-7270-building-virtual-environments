extends SceneTree
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	var d: Dictionary = {}
	var x = d["missing"]  # runtime error: key not found
	quit(0)
