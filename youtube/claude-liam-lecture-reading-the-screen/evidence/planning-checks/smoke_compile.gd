extends SceneTree
# Compiles every shader in res://lab-shaders/ by drawing it on a ColorRect over the meadow; engine errors land between the NOTE lines in the log.
const L = preload("res://rts_lib.gd")

func _initialize() -> void: call_deferred("run")

func run() -> void:
	root.size = Vector2i(640, 360)
	var holder := Node2D.new()
	root.add_child(holder)
	L.build_world(holder, Vector2(640, 360))
	var dir := DirAccess.open("res://lab-shaders")
	var names: Array = []
	for f in dir.get_files():
		if f.ends_with(".gdshader"):
			names.append(f)
	names.sort()
	for n in names:
		print("NOTE compiling " + n)
		var r := L.rect(Vector2(40, 40), Vector2(300, 200), Color.WHITE, "T")
		r.material = L.mat_file(n)
		holder.add_child(r)
		for i in 3:
			await process_frame
		var img := L.grab(root)
		L.out("compiled", {"file": n, "centre_px": L.px(img, 0.30, 0.40), "uniforms": (r.material.shader as Shader).get_shader_uniform_list().map(func(u): return u["name"])})
		r.queue_free()
		await process_frame
	quit(0)
