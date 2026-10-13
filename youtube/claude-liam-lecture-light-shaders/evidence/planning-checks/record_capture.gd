extends SceneTree
# record_capture.gd: the capture loop in its simplest form. Renders one capture of captures.json into a 1920x1080 SubViewport (scale 1) and writes one PNG per frame.
# The scene clock is driven by hand: one step(1/30) per rendered frame, so t is exactly frame/30. --fixed-fps 30 keeps the shader's TIME on the same 1/30 step, offline.
# Run: godot --path <project dir> --fixed-fps 30 --script res://record_capture.gd -- <id> <frames> <out dir> <lab-shaders dir> <captures.json>
# (The film's build session extends this to the whole clip, then ffmpeg turns the PNG sequence into an MP4.)
const LS := preload("res://light_scene.gd")

func _initialize() -> void: call_deferred("run")

func run() -> void:
	var a := OS.get_cmdline_user_args()
	var id := a[0]
	var n := int(a[1])
	var outdir := a[2]
	DirAccess.make_dir_recursive_absolute(outdir)
	var sv := SubViewport.new()
	sv.size = Vector2i(1920, 1080)
	sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(sv)
	var s: Node2D = LS.new()
	s.manual = true
	s.setup(id, a[3], a[4])
	sv.add_child(s)
	await process_frame
	for i in range(n):
		s.step(1.0 / 30.0)
		await process_frame
		RenderingServer.force_draw(false)
		sv.get_texture().get_image().save_png("%s/%s-%05d.png" % [outdir, id, i])
	print("RESULT " + JSON.stringify({"id": id, "frames": n, "clip_t": snappedf(s.t, 0.0001), "expected_t": snappedf(n / 30.0, 0.0001), "state": s.state()}))
	quit(0)
