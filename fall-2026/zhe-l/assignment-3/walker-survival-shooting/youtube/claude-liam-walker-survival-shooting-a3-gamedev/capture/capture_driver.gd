extends SceneTree
## Film capture harness for walker-survival-shooting Assignment 3 (source b370626).
## Runs ONLY in an isolated capture copy. It instantiates the unmodified
## res://base.tscn inside a 3840x2160 SubViewport (so the engine renders at
## native 4K) and writes each finished frame as a PNG. It never edits, moves or
## deletes a node of base.tscn and never saves the scene. There is no player
## and no input in this project, so nothing is "played" here.
##
## Usage (user args after "--"):  shot=<name> frames=<n> out=<dir> [open_at=<f>] [close_at=<f>]
##   asset_cam    the scene's own a3_asset_camera, made current at runtime only
##   latch_close  film camera: front of the small crate (latches, handles)
##   tablet_close film camera: the tablet where it floats beside the large crate
##   crates_open  film camera on both crates; at frame open_at the script plays each
##                crate's own imported "open" animation, at close_at its "close"
##   row          film camera: the whole asset row against the back wall, from the room
## Run with --fixed-fps 30 so every frame advances the animation by exactly 1/30 s.

var shot := "asset_cam"
var frames := 3
var out_dir := "user://capture"
var open_at := -1
var close_at := -1
var vp: SubViewport
var cam: Camera3D
var base: Node3D
var frame := 0

func _initialize() -> void:
	for a in OS.get_cmdline_user_args():
		var kv := a.split("=", true, 1)
		match kv[0]:
			"shot": shot = kv[1]
			"frames": frames = kv[1].to_int()
			"out": out_dir = kv[1]
			"open_at": open_at = kv[1].to_int()
			"close_at": close_at = kv[1].to_int()
	DirAccess.make_dir_recursive_absolute(out_dir)
	RenderingServer.frame_post_draw.connect(_on_post_draw)
	vp = SubViewport.new()
	vp.size = Vector2i(3840, 2160)
	vp.own_world_3d = true
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	base = load("res://base.tscn").instantiate()
	vp.add_child(base)
	if shot == "asset_cam":
		(base.get_node("a3_asset_camera") as Camera3D).current = true
		print("CAPTURE shot=asset_cam camera=a3_asset_camera (scene's own) size=", vp.size)
		return
	cam = Camera3D.new()
	cam.name = "film_camera_added_by_capture_script"
	vp.add_child(cam)
	match shot:
		"latch_close":
			cam.fov = 40.0
			_aim(Vector3(7.05, 0.80, -2.85), Vector3(7.05, 0.47, -4.15))
		"tablet_close":
			cam.fov = 35.0
			_aim(Vector3(5.05, 0.95, -3.3), Vector3(5.2, 0.62, -4.15))
		"crates_open":
			cam.fov = 45.0
			_aim(Vector3(6.55, 1.55, -2.05), Vector3(6.55, 0.45, -4.2))
		"row":
			cam.fov = 62.0
			_aim(Vector3(2.65, 1.75, 0.1), Vector3(2.65, 0.55, -4.3))
	cam.current = true
	print("CAPTURE shot=%s camera=%s pos=%s size=%s open_at=%d close_at=%d" % [shot, cam.name, cam.position, vp.size, open_at, close_at])

func _aim(eye: Vector3, target: Vector3) -> void:
	cam.transform = Transform3D(Basis(), eye).looking_at(target, Vector3.UP)

func _play(anim: String) -> void:
	for n in ["crate_long", "crate_cube"]:
		var ap := base.get_node(n).find_child("AnimationPlayer", true, false) as AnimationPlayer
		ap.play(anim)
	print("frame %d: play '%s' on crate_long and crate_cube" % [frame - 2, anim])

func _on_post_draw() -> void:
	# Frames 0-1 let the scene settle; then frames are written in order.
	if frame >= 2:
		var i := frame - 2
		vp.get_texture().get_image().save_png("%s/f%05d.png" % [out_dir, i])
		if i + 1 == open_at:
			_play("open")
		elif i + 1 == close_at:
			_play("close")
	frame += 1
	if frame >= frames + 2:
		quit(0)
