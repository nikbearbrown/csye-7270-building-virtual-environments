extends SceneTree
## Windowed captures for TEST-REPORT.md's interface sweep and its "one shader,
## two materials" check (the assignment's Use It), under props_room.tscn's own
## lighting. Every change is made to the loaded resources in memory and never
## saved, so the shader file, the material files and the scene stay as they are.
## - sweep: each uniform of weathered_stone.gdshader, on the waystone's
##   material, at its minimum, default and maximum, seen from the scene's
##   Camera, then again with that camera moved close to the waystone;
## - shader: one line of the shader's code changed in memory (ALBEDO halved),
##   on the Shader both materials share;
## - material: one value of the circle's material changed, normal_strength to
##   2.0, then albedo_tint to the waystone's white.
## For each capture it prints how much each prop's part of the frame changed
## from the default. Not headless. Run from assignment-5/:
##   godot --path godot --resolution 1920x1080 --always-on-top --script res://tests/capture_sweep.gd
## The crops go to evidence/use-it/sweep/.

const SCENE := "res://scenes/props_room.tscn"
const LINE := "ALBEDO = texture(albedo_tex, scaled_uv).rgb * albedo_tint.rgb;" ## weathered_stone.gdshader:18
const HALVED := "ALBEDO = texture(albedo_tex, scaled_uv).rgb * albedo_tint.rgb * 0.5;"
## uniform, then [label, value] at its minimum, default and maximum
const SWEEP := [
	["albedo_tint", [["min", Color(0, 0, 0, 1)], ["default", Color(1, 1, 1, 1)]]], # white is the default and the maximum
	["uv_scale", [["min", 0.25], ["default", 1.0], ["max", 4.0]]],
	["normal_strength", [["min", 0.0], ["default", 1.0], ["max", 2.0]]],
	["roughness_offset", [["min", -0.5], ["default", 0.0], ["max", 0.5]]],
]
const STEPS := 2 ## a pixel counts as changed when a channel moves by more than this
const CLOSE := Vector3(0.7, 0.55, 1.8) ## m from the waystone's centre: about 2 m away, in front, to the right and above

var _camera: Camera3D
var _regions := {}
var _default: Image
var _out := ""


func _initialize() -> void:
	if DisplayServer.get_name() == "headless":
		printerr("STOP this needs a window: a headless run draws no frame to read")
		quit(1)
		return
	_out = ProjectSettings.globalize_path("res://").path_join("../evidence/use-it/sweep").simplify_path()
	DirAccess.make_dir_recursive_absolute(_out)
	var scene := (load(SCENE) as PackedScene).instantiate() as Node3D
	root.add_child(scene)
	_camera = scene.get_node("Camera") as Camera3D
	var waystone_mesh := scene.get_node("Waystone/Waystone") as MeshInstance3D
	var circle_mesh := scene.get_node("TeleportCircle/TeleportCircle") as MeshInstance3D
	var waystone := waystone_mesh.get_surface_override_material(0) as ShaderMaterial
	var circle := circle_mesh.get_surface_override_material(1) as ShaderMaterial
	print("SHARED the two materials use one Shader object: %s (%s)" % [waystone.shader == circle.shader, waystone.shader.resource_path])

	_default = await _frame()
	if _default == null:
		return
	var size := _default.get_size()
	_regions["waystone"] = _region(waystone_mesh, size)
	_regions["circle"] = _region(circle_mesh, size)
	print("FRAME %d x %d; waystone at %s, circle at %s" % [size.x, size.y, _regions["waystone"], _regions["circle"]])
	_save(_default, _regions["waystone"], "waystone-default.png")
	_save(_default, _both(), "two-materials-default.png")
	await _report("default again", _default) # how much two identical frames differ

	# The sweep, on the waystone's material only.
	await _sweep(waystone, "waystone", ["waystone", "circle"])

	# One line of the shader, changed in memory on the Shader both materials share.
	var shader := waystone.shader
	var code := shader.code
	if not code.contains(LINE):
		printerr("STOP the shader no longer holds the line to change: %s" % LINE)
		quit(1)
		return
	shader.code = code.replace(LINE, HALVED)
	var halved := await _report("shader line 18 with ALBEDO halved", null)
	_save(halved, _both(), "two-materials-shader-line.png")
	shader.code = code

	# One value in one material: a relief value, then the colour, each restored.
	# normal_strength alone changed too little to see, so albedo_tint follows.
	for change: Array in [[&"normal_strength", 2.0], [&"albedo_tint", Color(1, 1, 1, 1)]]:
		var original: Variant = circle.get_shader_parameter(change[0])
		circle.set_shader_parameter(change[0], change[1])
		var one := await _report("circle_darkstone %s %s" % change, null)
		_save(one, _both(), "two-materials-circle-%s.png" % change[0])
		circle.set_shader_parameter(change[0], original)

	# The sweep again from close up: from the scene's Camera the waystone is
	# about 220 px tall, too small to judge the relief and the highlight.
	var centre := (waystone_mesh.global_transform * waystone_mesh.get_aabb()).get_center()
	_camera.global_position = centre + CLOSE
	_camera.look_at(centre)
	_default = await _frame()
	_regions["close"] = _region(waystone_mesh, size)
	print("CLOSE camera at %s, looking at %s; waystone at %s" % [_camera.global_position, centre, _regions["close"]])
	_save(_default, _regions["close"], "close-default.png")
	await _report("close default again", _default, ["close"])
	await _sweep(waystone, "close", ["close"])
	print("DONE nothing was saved but the crops")
	quit(0)


## Each uniform at its minimum, default and maximum on one material, restored
## after. region names the part of the frame cropped, and the crops' prefix.
func _sweep(material: ShaderMaterial, region: String, props: Array) -> void:
	for entry: Array in SWEEP:
		var uniform: StringName = entry[0]
		var original: Variant = material.get_shader_parameter(uniform)
		for step: Array in entry[1]:
			material.set_shader_parameter(uniform, step[1])
			var image := await _report("%s %s %s %s" % [region, uniform, step[0], step[1]], null, props)
			_save(image, _regions[region], "%s-%s-%s.png" % [region, uniform, step[0]])
		material.set_shader_parameter(uniform, original)


## Draws a frame, then prints how far each prop's region moved from the default.
func _report(label: String, image: Image, props: Array = ["waystone", "circle"]) -> Image:
	if image == null or image == _default:
		image = await _frame()
	var parts: PackedStringArray = []
	for prop: String in props:
		var d := _difference(_default, image, _regions[prop])
		parts.append("%s mean %.2f, %.1f%% of pixels by more than %d" % [prop, d[0], d[1] * 100.0, STEPS])
	print("CHANGE %s: %s" % [label, "; ".join(parts)])
	return image


func _frame() -> Image:
	for i in 6:
		await process_frame
	await RenderingServer.frame_post_draw
	return root.get_texture().get_image()


func _region(mesh: MeshInstance3D, size: Vector2i) -> Rect2i:
	var box := mesh.global_transform * mesh.get_aabb()
	var lo := Vector2(INF, INF)
	var hi := Vector2(-INF, -INF)
	for i in 8:
		var p := _camera.unproject_position(box.get_endpoint(i))
		lo = lo.min(p)
		hi = hi.max(p)
	return Rect2i(Vector2i(lo.floor()), Vector2i((hi - lo).ceil())).grow(8).intersection(Rect2i(Vector2i.ZERO, size))


func _both() -> Rect2i:
	return (_regions["waystone"] as Rect2i).merge(_regions["circle"]).grow(24).intersection(Rect2i(Vector2i.ZERO, _default.get_size()))


## [mean of the largest channel difference, share of pixels changed by more than STEPS]
func _difference(a: Image, b: Image, r: Rect2i) -> Array:
	var total := 0
	var changed := 0
	for y in range(r.position.y, r.end.y):
		for x in range(r.position.x, r.end.x):
			var ca := a.get_pixel(x, y)
			var cb := b.get_pixel(x, y)
			var d := maxi(maxi(absi(ca.r8 - cb.r8), absi(ca.g8 - cb.g8)), absi(ca.b8 - cb.b8))
			total += d
			if d > STEPS:
				changed += 1
	var n := maxi(r.get_area(), 1)
	return [float(total) / n, float(changed) / n]


func _save(image: Image, r: Rect2i, file: String) -> void:
	image.get_region(r).save_png(_out.path_join(file))
	print("SAVED %s (%d x %d crop)" % [file, r.size.x, r.size.y])
