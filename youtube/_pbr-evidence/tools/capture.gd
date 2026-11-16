extends SceneTree
## Offline, fixed-step capture of the PBR demonstrations. Every material is a stock StandardMaterial3D
## except the decode demo, which needs two otherwise identical ShaderMaterials that differ by one texture hint.
## Usage: godot --path <project> --script res://tools/capture.gd -- --id <capture id> --seconds <s> --out <abs dir> [--fps 24]
## Frames land as <out>/<id>/NNNN.jpg; a log line per capture goes to stdout.

const TEX := "res://textures/"
var args := {}
var label: Label
var sub: Label

func _init() -> void:
	var a := OS.get_cmdline_user_args()
	for i in range(0, a.size() - 1, 2):
		args[a[i].trim_prefix("--")] = a[i + 1]
	call_deferred("_main")

func tex(name: String) -> Texture2D:
	var img := Image.load_from_file(ProjectSettings.globalize_path(TEX + name))
	img.generate_mipmaps()
	return ImageTexture.create_from_image(img)

func mat(albedo: Color, metallic: float, rough: float) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_color = albedo
	m.metallic = metallic
	m.roughness = rough
	return m

func sphere(scene: Node3D, pos: Vector3, m: Material, r := 1.0) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	var s := SphereMesh.new(); s.radius = r; s.height = 2.0 * r; s.radial_segments = 128; s.rings = 64
	mi.mesh = s; mi.material_override = m; mi.position = pos
	scene.add_child(mi)
	return mi

func floor_plane(scene: Node3D, y := -1.0) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	var p := PlaneMesh.new(); p.size = Vector2(40, 40)
	mi.mesh = p; mi.position = Vector3(0, y, 0)
	mi.material_override = mat(Color("#B8B2A6"), 0.0, 0.85)
	scene.add_child(mi)
	return mi

class Rig:
	var env: Environment
	var sky: ProceduralSkyMaterial
	var sun: DirectionalLight3D
	var cam: Camera3D

func rig(scene: Node3D, cam_pos: Vector3, look: Vector3, fov := 40.0) -> Rig:
	var r := Rig.new()
	var we := WorldEnvironment.new()
	r.env = Environment.new()
	r.sky = ProceduralSkyMaterial.new()
	var sk := Sky.new(); sk.sky_material = r.sky
	r.env.background_mode = Environment.BG_SKY
	r.env.sky = sk
	r.env.ambient_light_source = Environment.AMBIENT_SOURCE_SKY
	r.env.reflected_light_source = Environment.REFLECTION_SOURCE_SKY
	r.env.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	we.environment = r.env
	scene.add_child(we)
	r.sun = DirectionalLight3D.new()
	r.sun.shadow_enabled = true
	r.sun.rotation_degrees = Vector3(-45, -35, 0)
	scene.add_child(r.sun)
	r.cam = Camera3D.new(); r.cam.fov = fov
	scene.add_child(r.cam)
	r.cam.position = cam_pos; r.cam.look_at(look)
	return r

# lighting presets: noon, sunset, night room
func preset(r: Rig, k: float) -> String:
	var noon := {"pitch": -60.0, "col": Color(1.0, 0.98, 0.94), "e": 1.3, "top": Color(0.38, 0.55, 0.85), "hor": Color(0.72, 0.80, 0.90), "amb": 1.0}
	var sunset := {"pitch": -8.0, "col": Color(1.0, 0.55, 0.28), "e": 1.2, "top": Color(0.30, 0.25, 0.45), "hor": Color(0.95, 0.55, 0.35), "amb": 0.8}
	var night := {"pitch": -35.0, "col": Color(0.55, 0.65, 1.0), "e": 0.18, "top": Color(0.02, 0.03, 0.08), "hor": Color(0.06, 0.07, 0.14), "amb": 0.35}
	var a: Dictionary; var b: Dictionary; var f: float; var name: String
	if k < 0.5:
		a = noon; b = sunset; f = smoothstep(0.3, 0.45, k)
		name = "noon sun" if k < 0.38 else "sunset"
	else:
		a = sunset; b = night; f = smoothstep(0.62, 0.77, k)
		name = "sunset" if k < 0.7 else "dim blue room"
	r.sun.rotation_degrees = Vector3(lerpf(a.pitch, b.pitch, f), -35, 0)
	r.sun.light_color = a.col.lerp(b.col, f)
	r.sun.light_energy = lerpf(a.e, b.e, f)
	r.sky.sky_top_color = a.top.lerp(b.top, f)
	r.sky.sky_horizon_color = a.hor.lerp(b.hor, f)
	r.sky.ground_horizon_color = r.sky.sky_horizon_color
	r.sky.ground_bottom_color = r.sky.sky_top_color.darkened(0.5)
	r.env.ambient_light_energy = lerpf(a.amb, b.amb, f)
	r.env.background_energy_multiplier = lerpf(a.amb, b.amb, f)
	return name

func make_labels(scene: Node) -> void:
	var layer := CanvasLayer.new(); scene.add_child(layer)
	var bg := ColorRect.new(); bg.color = Color(0.95, 0.94, 0.91, 0.88); bg.position = Vector2(0, 822); bg.size = Vector2(1600, 78)
	layer.add_child(bg)
	label = Label.new(); label.position = Vector2(36, 834)
	label.add_theme_color_override("font_color", Color("#3D3929")); label.add_theme_font_size_override("font_size", 38)
	layer.add_child(label)
	sub = Label.new(); sub.position = Vector2(36, 24)
	sub.add_theme_color_override("font_color", Color("#3D3929")); sub.add_theme_font_size_override("font_size", 34)
	sub.add_theme_color_override("font_outline_color", Color(0.95, 0.94, 0.91)); sub.add_theme_constant_override("outline_size", 10)
	layer.add_child(sub)

func label3d(scene: Node3D, text: String, pos: Vector3, size := 64, px := 0.004) -> void:
	var l := Label3D.new(); l.text = text; l.position = pos; l.font_size = size; l.pixel_size = px
	l.modulate = Color("#3D3929"); l.outline_modulate = Color(0.95, 0.94, 0.91); l.outline_size = 14
	l.billboard = BaseMaterial3D.BILLBOARD_ENABLED; l.shaded = false
	scene.add_child(l)

func seg(t: float, a: float, b: float) -> float:
	return clampf((t - a) / (b - a), 0.0, 1.0)

func _main() -> void:
	var id: String = args.get("id", "")
	var seconds := float(args.get("seconds", "10"))
	var fps := int(args.get("fps", "24"))
	var outdir: String = args.get("out", ProjectSettings.globalize_path("res://evidence/frames")) + "/" + id
	DirAccess.make_dir_recursive_absolute(outdir)
	var scene := Node3D.new(); root.add_child(scene)
	make_labels(scene)
	var n := int(round(seconds * fps))
	var r: Rig
	var obj := {}
	var terra := Color("#D97757"); var brass := Color(0.89, 0.72, 0.38)
	match id:
		"albedo", "metallic", "roughness":
			r = rig(scene, Vector3(0, 0.4, 4.2), Vector3(0, 0, 0))
			floor_plane(scene)
			obj.m = mat(terra if id != "metallic" else brass, 0.0, 0.5 if id == "albedo" else 0.25)
			if id == "roughness": obj.m.albedo_color = Color("#8A3B22")
			sphere(scene, Vector3.ZERO, obj.m)
		"grid":
			r = rig(scene, Vector3(-0.9, -0.2, 24.0), Vector3(-0.9, -0.2, 0), 36.0)
			r.sun.rotation_degrees = Vector3(-35, -30, 0)
			for row in 5:
				for col in 5:
					sphere(scene, Vector3((col - 2) * 2.3, (2 - row) * 2.3 - 0.2, 0), mat(terra, row / 4.0, col / 4.0), 0.95)
			label3d(scene, "roughness  0  →  1", Vector3(0, 6.0, 0), 80, 0.01)
			label3d(scene, "metallic\n0\n↓\n1", Vector3(-7.4, -0.2, 0), 80, 0.01)
		"normal":
			r = rig(scene, Vector3(0, 0.3, 4.2), Vector3(0, 0, 0))
			floor_plane(scene)
			obj.m = mat(Color("#EDE3CC"), 0.0, 0.45)
			obj.m.normal_enabled = true
			obj.m.normal_texture = tex("flat_normal.png")
			obj.nt = tex("tiles_normal.png")
			obj.m.uv1_scale = Vector3(3, 2, 1)
			sphere(scene, Vector3.ZERO, obj.m)
		"ao":
			r = rig(scene, Vector3(0, 0.3, 4.0), Vector3(0, 0, 0))
			floor_plane(scene)
			obj.m = mat(Color("#EDE3CC"), 0.0, 0.6)
			obj.m.ao_texture = tex("tiles_ao.png")
			obj.m.normal_enabled = true; obj.m.normal_texture = tex("tiles_normal.png")
			obj.m.uv1_scale = Vector3(3, 2, 1)
			sphere(scene, Vector3.ZERO, obj.m)
		"lights", "three":
			r = rig(scene, Vector3(0, 0.6, 7.2), Vector3(0, -0.1, 0))
			floor_plane(scene)
			sphere(scene, Vector3(-2.4, 0, 0), mat(terra, 0.0, 0.35))
			sphere(scene, Vector3(0, 0, 0), mat(Color(1.0, 0.78, 0.34), 1.0, 0.2))
			sphere(scene, Vector3(2.4, 0, 0), mat(Color("#2E2C2A"), 0.0, 0.9))
			label3d(scene, "plastic", Vector3(-2.4, -1.35, 1.2), 56)
			label3d(scene, "gold", Vector3(0, -1.35, 1.2), 56)
			label3d(scene, "rubber", Vector3(2.4, -1.35, 1.2), 56)
		"painted_orbit", "painted_daynight", "painted_static":
			r = rig(scene, Vector3(0, 0.4, 6.4), Vector3(0, 0, 0))
			floor_plane(scene)
			var pm := StandardMaterial3D.new()
			pm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
			pm.albedo_texture = tex("painted_sphere.png")
			var ps := sphere(scene, Vector3(-1.5, 0, 0), pm)
			ps.rotation_degrees = Vector3(0, float(args.get("rot", "180")), 0)
			sphere(scene, Vector3(1.5, 0, 0), mat(terra, 0.0, 0.3))
			label3d(scene, "light painted in", Vector3(-1.5, -1.35, 1.2), 56)
			label3d(scene, "PBR material", Vector3(1.5, -1.35, 1.2), 56)
		"metal_sky":
			r = rig(scene, Vector3(0, 0.4, 4.2), Vector3(0, 0, 0))
			floor_plane(scene)
			sphere(scene, Vector3.ZERO, mat(Color(0.92, 0.92, 0.93), 1.0, 0.12))
		"roughmap":
			r = rig(scene, Vector3(0, 2.6, 4.6), Vector3(0, 0, -0.4))
			var mi := MeshInstance3D.new(); var pl := PlaneMesh.new(); pl.size = Vector2(6, 6); mi.mesh = pl
			var m := StandardMaterial3D.new()
			m.albedo_color = Color("#5A4A42")
			m.roughness_texture = tex("tiles_roughness.png"); m.roughness = 1.0
			m.metallic = 0.0
			mi.material_override = m
			scene.add_child(mi)
			r.env.ambient_light_energy = 0.4
		"stack":
			r = rig(scene, Vector3(0, 0.3, 4.2), Vector3(0, 0, 0))
			floor_plane(scene)
			obj.m = StandardMaterial3D.new()
			obj.m.uv1_scale = Vector3(3, 2, 1)
			sphere(scene, Vector3.ZERO, obj.m)
		"decode":
			r = rig(scene, Vector3(0, 0.3, 6.0), Vector3(0, 0, 0))
			r.sun.rotation_degrees = Vector3(0, 0, 0)          # light shines straight along -Z: head-on to the camera-facing side
			r.sun.light_energy = 1.2
			r.env.ambient_light_energy = 0.15
			floor_plane(scene)
			var code := "shader_type spatial;\nuniform sampler2D nmap : %s;\nvoid fragment() {\n\tALBEDO = vec3(0.80, 0.74, 0.62);\n\tROUGHNESS = 0.6;\n\tNORMAL_MAP = texture(nmap, UV).rgb;\n}\n"
			for i in 2:
				var sh := Shader.new(); sh.code = code % ["hint_normal" if i == 0 else "source_color"]
				var smat := ShaderMaterial.new(); smat.shader = sh
				smat.set_shader_parameter("nmap", tex("flat_normal.png"))
				sphere(scene, Vector3(-1.5 + 3.0 * i, 0, 0), smat)
			label3d(scene, "read as data", Vector3(-1.5, -1.35, 1.2), 56)
			label3d(scene, "read as colour", Vector3(1.5, -1.35, 1.2), 56)
		"profiles":
			r = rig(scene, Vector3(0, 0, 4.0), Vector3(0, 0, 0))
			r.env.background_mode = Environment.BG_COLOR; r.env.background_color = Color.BLACK
			r.env.ambient_light_source = Environment.AMBIENT_SOURCE_DISABLED
			r.env.reflected_light_source = Environment.REFLECTION_SOURCE_DISABLED
			r.env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
			r.sun.rotation_degrees = Vector3(0, 0, 0)
			r.sun.shadow_enabled = false
			r.sun.light_energy = 0.12
			obj.m = mat(Color(0.03, 0.03, 0.03), 0.0, 0.2)
			sphere(scene, Vector3.ZERO, obj.m)
		_:
			push_error("unknown capture id " + id); quit(2); return
	# warm up
	for i in 4: await process_frame
	var t0 := Time.get_ticks_msec()
	var extra := {}
	for f in n:
		var t: float = float(f) / float(maxi(1, n - 1))
		match id:
			"albedo":
				var c1 := Color("#9A958C"); var c2 := Color("#D97757"); var c3 := Color("#4F8C83")
				obj.m.albedo_color = c1.lerp(c2, seg(t, 0.15, 0.45)) if t < 0.55 else c2.lerp(c3, seg(t, 0.6, 0.9))
				label.text = "albedo = #%s     metallic 0.00 · roughness 0.50" % obj.m.albedo_color.to_html(false).to_upper()
			"metallic":
				obj.m.metallic = seg(t, 0.15, 0.85)
				label.text = "metallic = %.2f     roughness 0.25" % obj.m.metallic
			"roughness":
				obj.m.roughness = lerpf(0.05, 1.0, seg(t, 0.12, 0.88))
				label.text = "roughness = %.2f     metallic 0.00" % obj.m.roughness
			"grid":
				r.sun.rotation_degrees = Vector3(-35, -30 + 40.0 * sin(TAU * t), 0)
				label.text = "25 spheres · one albedo · only metallic and roughness change"
			"normal":
				r.sun.rotation_degrees = Vector3(-30, -100 + 160.0 * t, 0)
				if t >= 0.4 and not extra.has("swapped"):
					obj.m.normal_texture = obj.nt; extra.swapped = true
				label.text = "normal map: " + ("flat (128, 128, 255)" if t < 0.4 else "tiles · the outline stays round")
			"ao":
				var phase: int = 0 if t < 0.36 else (1 if t < 0.68 else 2)
				obj.m.ao_enabled = phase >= 1
				r.sun.light_energy = 0.0 if phase < 2 else 1.6
				r.sun.visible = phase == 2
				label.text = ["ambient occlusion OFF · lit by the sky only", "ambient occlusion ON · lit by the sky only", "ambient occlusion ON · sun added: direct light ignores it"][phase]
			"lights", "painted_daynight":
				label.text = preset(r, t) + "  ·  the materials never change"
			"three":
				label.text = preset(r, t) + "  ·  same three materials"
			"painted_static":
				label.text = "both lit from the upper left: they look alike"
			"painted_orbit":
				r.sun.rotation_degrees = Vector3(-35, -35 + 300.0 * seg(t, 0.08, 0.95), 0)
				label.text = "the light moves; only the PBR highlight follows it"
			"metal_sky":
				var on: bool = t >= 0.45
				r.env.background_mode = Environment.BG_SKY if on else Environment.BG_COLOR
				r.env.background_color = Color.BLACK
				r.env.ambient_light_source = Environment.AMBIENT_SOURCE_SKY if on else Environment.AMBIENT_SOURCE_DISABLED
				r.env.reflected_light_source = Environment.REFLECTION_SOURCE_SKY if on else Environment.REFLECTION_SOURCE_DISABLED
				label.text = ("sky to reflect" if on else "nothing to reflect") + "  ·  metallic 1.00 · roughness 0.12"
			"roughmap":
				r.sun.rotation_degrees = Vector3(-24, 180.0 - 35.0 + 70.0 * t, 0)
				label.text = "one roughness map · tiles 0.30 · grout 0.90"
			"stack":
				var step: int = mini(int(t * 5.0), 4)
				if not extra.has(step):
					extra[step] = true
					if step >= 0: obj.m.albedo_texture = tex("tiles_albedo.png")
					if step >= 1: obj.m.normal_enabled = true; obj.m.normal_texture = tex("tiles_normal.png")
					if step >= 2: obj.m.roughness_texture = tex("tiles_roughness.png"); obj.m.roughness = 1.0
					if step >= 3: obj.m.metallic_texture = tex("tiles_metallic.png"); obj.m.metallic = 1.0
					if step >= 4: obj.m.ao_enabled = true; obj.m.ao_texture = tex("tiles_ao.png")
				r.sun.rotation_degrees = Vector3(-35, -60 + 70.0 * t, 0)
				label.text = ["+ base colour map", "+ normal map", "+ roughness map", "+ metallic map", "+ ambient occlusion map"][step]
			"decode":
				label.text = "the same flat normal map (128, 128, 255) · light straight on"
			"profiles":
				var rv: float = [0.2, 0.4, 0.7][mini(int(t * 3.0), 2)]
				obj.m.roughness = rv
				label.text = "roughness = %.2f · sun only · linear tonemap" % rv
		await RenderingServer.frame_post_draw
		var img := root.get_viewport().get_texture().get_image()
		img.save_jpg("%s/%04d.jpg" % [outdir, f], 0.92)
	print("CAPTURE %s %d frames at %d fps (%.2f s) in %d ms; renderer %s" % [id, n, fps, seconds, Time.get_ticks_msec() - t0, RenderingServer.get_current_rendering_method()])
	quit(0)
