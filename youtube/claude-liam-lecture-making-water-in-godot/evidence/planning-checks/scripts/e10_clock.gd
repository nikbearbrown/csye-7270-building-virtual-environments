extends SceneTree
# E10: do the shader's TIME and the script's clocks agree? A REAL-TIME run (window kept on top), not the offline harness.
# For each of 90 frames: read Time.get_ticks_msec() (script side), then read back the colour of a full-window quad that shows fract(TIME / 4).
const DIR := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-making-water-in-godot/evidence/planning-checks/check-shaders/"
var quad: MeshInstance3D
var log_rows: Array = []
var t_engine0 := 0.0
func _initialize() -> void:
	call_deferred("run")
func lin(c: float) -> float:
	return c / 12.92 if c <= 0.04045 else pow((c + 0.055) / 1.055, 2.4)
func run() -> void:
	DisplayServer.window_set_flag(DisplayServer.WINDOW_FLAG_ALWAYS_ON_TOP, true)
	root.size = Vector2i(640, 360)
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = 2.0
	cam.position = Vector3(0, 0, 3)
	root.add_child(cam)
	cam.current = true
	var q := QuadMesh.new()
	q.size = Vector2(4, 2)
	quad = MeshInstance3D.new()
	quad.mesh = q
	var sh := Shader.new()
	sh.code = FileAccess.get_file_as_string(DIR + "e10-clock.gdshader")
	var m := ShaderMaterial.new()
	m.shader = sh
	quad.material_override = m
	root.add_child(quad)
	for i in range(8):
		await process_frame
	var rows := []
	for i in range(90):
		await process_frame
		var ticks := Time.get_ticks_msec() / 1000.0
		await RenderingServer.frame_post_draw
		var img := root.get_texture().get_image()
		var c := img.get_pixel(320, 180)
		rows.append([ticks, lin(c.r) * 4.0])
	# TIME mod 4 = rows[i][1]; script clock = rows[i][0]; offset = ticks - TIME (mod 4)
	var offs: Array = []
	for r in rows:
		var d := fposmod(r[0] - r[1], 4.0)
		if d > 2.0: d -= 4.0
		offs.append(d)
	var mean := 0.0
	for o in offs: mean += o
	mean /= offs.size()
	var mn := 1e9; var mx := -1e9
	for o in offs:
		mn = minf(mn, o); mx = maxf(mx, o)
	print("RESULT E10: ticks_seconds - TIME (mod 4 s, +-2): mean %.3f s, min %.3f, max %.3f, over %d frames; first ticks %.3f s; renderer %s" % [mean, mn, mx, offs.size(), rows[0][0], RenderingServer.get_current_rendering_method()])
	quit()
