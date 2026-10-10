extends SceneTree
## Film capture harness for walker-survival-shooting (source f848d84).
## Runs ONLY in an isolated capture copy. It instantiates the unmodified
## res://base.tscn inside a 3840x2160 SubViewport (so the engine renders at
## native 4K instead of the 1152x648 default window) and writes each rendered
## frame as a PNG. For some shots it adds one extra Camera3D (the "film
## camera"). It never edits, moves or deletes any node of base.tscn. There is
## no player and no input in this project, so nothing is "played" here.
## Collision-debug takes use --debug-collisions plus an override.cfg in the
## capture copy that only changes the debug shape colour (see CAPTURE.md).
##
## Usage (user args after "--"):  shot=<name> frames=<n> out=<dir>
##   preview      the scene's own preview_camera, untouched
##   stairs_side  orthographic film camera, side view of the stairs (+X looking -X)
##   stairs_3q    perspective film camera, three-quarter view of the stairs
##   room_pan     perspective film camera, slow pan across the room

var shot := "preview"
var frames := 3
var out_dir := "user://capture"
var vp: SubViewport
var cam: Camera3D
var frame := 0

func _initialize() -> void:
	for a in OS.get_cmdline_user_args():
		if a.begins_with("shot="):
			shot = a.substr(5)
		elif a.begins_with("frames="):
			frames = a.substr(7).to_int()
		elif a.begins_with("out="):
			out_dir = a.substr(4)
	DirAccess.make_dir_recursive_absolute(out_dir)
	RenderingServer.frame_post_draw.connect(_on_post_draw)
	vp = SubViewport.new()
	vp.size = Vector2i(3840, 2160)
	vp.own_world_3d = true
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	var base: Node = load("res://base.tscn").instantiate()
	vp.add_child(base)
	if shot == "preview":
		print("CAPTURE shot=preview camera=preview_camera (scene's own) size=", vp.size)
		return
	cam = Camera3D.new()
	cam.name = "film_camera_added_by_capture_script"
	vp.add_child(cam)
	match shot:
		"stairs_side":
			cam.projection = Camera3D.PROJECTION_ORTHOGONAL
			cam.size = 1.6
			_aim(Vector3(-1.0, 0.9, 2.25), Vector3(-5.0, 0.9, 2.25))
		"stairs_3q":
			cam.fov = 55.0
			_aim(Vector3(-2.2, 1.9, -0.6), Vector3(-5.0, 0.8, 2.6))
		"room_pan":
			cam.fov = 70.0
			_pan(0.0)
	cam.current = true
	print("CAPTURE shot=%s camera=%s pos=%s size=%s" % [shot, cam.name, cam.position, vp.size])

func _pan(t: float) -> void:
	# 0..1 over the take: yaw from the back-wall chair toward the stairs.
	var yaw := lerpf(deg_to_rad(-35.0), deg_to_rad(82.0), t)
	var eye := Vector3(2.0, 1.7, 3.2)
	_aim(eye, eye + Vector3(-sin(yaw), -0.22, -cos(yaw)))

func _aim(eye: Vector3, target: Vector3) -> void:
	# Transform math only, so it also works before the camera is in the tree.
	cam.transform = Transform3D(Basis(), eye).looking_at(target, Vector3.UP)

func _process(_delta: float) -> bool:
	return false

func _on_post_draw() -> void:
	# Runs after the frame has been drawn, so the texture holds this frame's
	# finished render. Frames 0-1 let the scene settle; then n frames are
	# written in order, and the camera is moved for the next frame.
	if frame >= 2:
		var img := vp.get_texture().get_image()
		img.save_png("%s/f%05d.png" % [out_dir, frame - 2])
		if shot == "room_pan" and frames > 1:
			_pan(clampf(float(frame - 1) / float(frames - 1), 0.0, 1.0))
	frame += 1
	if frame >= frames + 2:
		quit(0)
