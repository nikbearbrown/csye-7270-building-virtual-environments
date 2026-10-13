extends SceneTree
# SubViewports film, helper for check 10 and 11: a big window kept on top at (0, 0) for 40 seconds, so that it COVERS the window of the check that runs next to it.
# Started and stopped by run-cover-checks.sh (it stops this one by PID; never use pkill -f on a script name, other films run scripts with the same names).
func _initialize() -> void: call_deferred("run")

func run() -> void:
	root.size = Vector2i(1700, 1000)
	var r := ColorRect.new()
	r.color = Color(0.2, 0.2, 0.2)
	r.size = Vector2(1700, 1000)
	root.add_child(r)
	await create_timer(40.0).timeout
	quit(0)
