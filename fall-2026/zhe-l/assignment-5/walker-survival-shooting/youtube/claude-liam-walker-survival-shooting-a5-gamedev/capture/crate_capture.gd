extends SceneTree
## Film capture for the A5 crate wear shader. Runs ONLY in an isolated copy.
## Instantiates the unmodified res://base.tscn inside a 3840x2160 SubViewport
## (native 4K, real window run, not headless) and saves PNGs. It never edits,
## moves or deletes a node of base.tscn and never saves a scene or resource.
## Parameter values are changed only at runtime with set_shader_parameter() on
## the loaded material; nothing is written back to disk.
## REQUIRES: base.tscn contains nodes "crate_long" and "crate_cube" whose
## Crate_OliveDrab surface uses crate_long_wear.tres / crate_cube_wear.tres.
##
## Usage (user args after "--"):
##   shot=pair  out=<dir>                         both crates, one shader, two materials
##   shot=sweep out=<dir> target=crate_cube param=<uniform> values=<v1;v2;v3>
##       float values: 0.0;0.85;1.0   colour values: 0,0,0,1;0.26,0.283,0.19,1;1,1,1,1
## Camera positions are film choices (labelled as such), set below; tune before final takes.

const SETTLE_FRAMES := 10
const SHADER_PATH := "res://shaders/crate_wear.gdshader"

var shot := "pair"
var out_dir := "user://capture"
var target := "crate_cube"
var param := ""
var values: Array = []
var vp: SubViewport
var base: Node3D
var cam: Camera3D
var mat: ShaderMaterial
var frame := 0
var step := -1
var done := false

func _initialize() -> void:
	for a in OS.get_cmdline_user_args():
		var kv := a.split("=", true, 1)
		match kv[0]:
			"shot": shot = kv[1]
			"out": out_dir = kv[1]
			"target": target = kv[1]
			"param": param = kv[1]
			"values": values = Array(kv[1].split(";"))
	DirAccess.make_dir_recursive_absolute(out_dir)
	vp = SubViewport.new()
	vp.size = Vector2i(3840, 2160)
	vp.own_world_3d = true
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	base = load("res://base.tscn").instantiate()
	vp.add_child(base)
	for n in ["crate_long", "crate_cube"]:
		if base.get_node_or_null(n) == null:
			push_error("base.tscn has no node '%s' in this copy; stop" % n)
			quit(1)
			return
		_report_material(n)
	cam = Camera3D.new()
	cam.name = "film_camera_added_by_capture_script"
	vp.add_child(cam)
	var crate := base.get_node(target) as Node3D
	match shot:
		"pair":
			var a := (base.get_node("crate_long") as Node3D).position
			var b := (base.get_node("crate_cube") as Node3D).position
			var mid := (a + b) * 0.5
			cam.fov = 40.0
			_aim(mid + Vector3(0.0, 1.1, 2.1), mid + Vector3(0.0, 0.2, 0.0))
		"sweep_glint":
			# eye placed so ceiling_light_2 (5.38, 1.71, -3.63) mirrors off the top face of
			# crate_cube at about (6.89, 0.75, -4.09): the highlight shows roughness changes
			mat = _wear_material(target)
			cam.fov = 50.0
			_aim(Vector3(7.6, 1.2, -4.3), crate.position + Vector3(0.0, 0.5, 0.0))
		"sweep":
			mat = _wear_material(target)
			cam.fov = 35.0
			var c := crate.position  # base.tscn root sits at the origin; crates are its direct children
			_aim(c + Vector3(0.35, 0.85, 1.25), c + Vector3(0.0, 0.2, 0.0))
	cam.current = true
	print("CAPTURE shot=%s target=%s param=%s values=%s cam=%s size=%s renderer=%s" % [
		shot, target, param, values, cam.position, vp.size,
		RenderingServer.get_current_rendering_method()])
	RenderingServer.frame_post_draw.connect(_on_post_draw)

func _aim(eye: Vector3, look: Vector3) -> void:
	cam.transform = Transform3D(Basis(), eye).looking_at(look, Vector3.UP)  # cam is a direct child of the SubViewport

func _wear_material(node_name: String) -> ShaderMaterial:
	for mi in base.get_node(node_name).find_children("*", "MeshInstance3D", true, false):
		var m := mi as MeshInstance3D
		for s in m.mesh.get_surface_count():
			var sm := m.get_active_material(s)
			if sm is ShaderMaterial and (sm as ShaderMaterial).shader.resource_path == SHADER_PATH:
				return sm
	push_error("no crate_wear material under %s" % node_name)
	return null

func _report_material(node_name: String) -> void:
	var m := _wear_material(node_name)
	if m == null:
		return
	print("MATERIAL %s -> %s wear_amount=%s paint_roughness=%s texture_scale=%s" % [
		node_name, m.resource_path, m.get_shader_parameter("wear_amount"),
		m.get_shader_parameter("paint_roughness"), m.get_shader_parameter("texture_scale")])

func _parse(v: String) -> Variant:
	if v.contains(","):
		var p := v.split(",")
		return Color(p[0].to_float(), p[1].to_float(), p[2].to_float(), p[3].to_float())
	return v.to_float()

func _on_post_draw() -> void:
	if done:
		return
	frame += 1
	# the player scene in base.tscn brings its own Camera3D, which becomes current when it
	# enters the tree; take the view back once the tree is live, before any frame is saved
	if not cam.current:
		cam.current = true
	if frame < SETTLE_FRAMES:
		return
	if shot == "pair":
		vp.get_texture().get_image().save_png("%s/pair.png" % out_dir)
		print("SAVED pair.png")
		done = true
		quit(0)
		return
	# sweep: set a value, let it draw a few frames, save, next value
	if step >= 0 and (frame - SETTLE_FRAMES) % 4 == 0:
		var name := "%s_%s_%s.png" % [target, param, values[step].replace(",", "-")]
		vp.get_texture().get_image().save_png("%s/%s" % [out_dir, name])
		print("SAVED ", name, " value=", mat.get_shader_parameter(param))
		if step == values.size() - 1:
			done = true
			quit(0)
			return
	if (frame - SETTLE_FRAMES) % 4 == 0:
		step += 1
		mat.set_shader_parameter(param, _parse(values[step]))
