extends SceneTree

var checks := 0
var failures := 0


func _initialize() -> void:
	call_deferred("run")


func check(ok: bool, label: String) -> void:
	checks += 1
	if not ok:
		failures += 1
	print("PASS " if ok else "FAIL ", label)


func run() -> void:
	# Load the imported ship scene.
	var scene: PackedScene = load("res://polyhaven/dutch_ship_medium_1k.gltf")
	check(scene != null, "ship gltf PackedScene loads")
	if scene == null:
		print("RESULT 1 checks, 1 failures")
		quit(1)
		return

	var ship: Node = scene.instantiate()
	root.add_child(ship)
	await process_frame

	# ── Node structure ────────────────────────────────────────────────────────
	var rigging: MeshInstance3D = ship.find_child("dutch_ship_medium_rigging", true, false)
	var hull:    MeshInstance3D = ship.find_child("dutch_ship_medium_hull",    true, false)
	var sails:   MeshInstance3D = ship.find_child("dutch_ship_medium_sails",   true, false)
	check(rigging != null, "node 'dutch_ship_medium_rigging' found")
	check(hull    != null, "node 'dutch_ship_medium_hull' found")
	check(sails   != null, "node 'dutch_ship_medium_sails' found")

	# ── Material types ────────────────────────────────────────────────────────
	var rigging_mat: StandardMaterial3D = rigging.mesh.surface_get_material(0) if rigging else null
	var hull_mat:    StandardMaterial3D = hull.mesh.surface_get_material(0)    if hull    else null
	var sails_mat:   StandardMaterial3D = sails.mesh.surface_get_material(0)   if sails   else null
	check(rigging_mat is StandardMaterial3D, "rigging material is StandardMaterial3D")
	check(hull_mat    is StandardMaterial3D, "hull material is StandardMaterial3D")
	check(sails_mat   is StandardMaterial3D, "sails material is StandardMaterial3D")

	# ── Texture paths (one row per slot per material, matching MATERIALS.md table) ──
	var tex_expectations: Array = [
		# [mat, property, expected filename suffix]
		[rigging_mat, "albedo_texture",   "dutch_ship_medium_rigging_diff_1k.jpg"],
		[rigging_mat, "normal_texture",   "dutch_ship_medium_rigging_nor_gl_1k.jpg"],
		[rigging_mat, "metallic_texture", "dutch_ship_medium_rigging_arm_1k.jpg"],
		[rigging_mat, "roughness_texture","dutch_ship_medium_rigging_arm_1k.jpg"],
		[hull_mat,    "albedo_texture",   "dutch_ship_medium_hull_diff_1k.jpg"],
		[hull_mat,    "normal_texture",   "dutch_ship_medium_hull_nor_gl_1k.jpg"],
		[hull_mat,    "metallic_texture", "dutch_ship_medium_hull_arm_1k.jpg"],
		[hull_mat,    "roughness_texture","dutch_ship_medium_hull_arm_1k.jpg"],
		[sails_mat,   "albedo_texture",   "dutch_ship_medium_sails_diff_1k.jpg"],
		[sails_mat,   "normal_texture",   "dutch_ship_medium_sails_nor_gl_1k.jpg"],
		[sails_mat,   "metallic_texture", "dutch_ship_medium_sails_arm_1k.jpg"],
		[sails_mat,   "roughness_texture","dutch_ship_medium_sails_arm_1k.jpg"],
	]
	for entry in tex_expectations:
		var mat: StandardMaterial3D = entry[0]
		var prop: String = entry[1]
		var suffix: String = entry[2]
		if mat == null:
			check(false, prop + " (material is null)")
			continue
		var tex: Texture2D = mat.get(prop)
		check(tex != null, prop + " is bound (" + suffix + ")")
		if tex != null:
			check(tex.resource_path.ends_with(suffix),
				prop + " path ends_with '" + suffix + "' (got: " + tex.resource_path + ")")

	# ── Texture channels (glTF metallicRoughness: B=metallic, G=roughness) ───
	var channel_mats := {"rigging": rigging_mat, "hull": hull_mat, "sails": sails_mat}
	for mat_name in channel_mats:
		var mat: StandardMaterial3D = channel_mats[mat_name]
		if mat == null:
			continue
		check(mat.metallic_texture_channel == BaseMaterial3D.TEXTURE_CHANNEL_BLUE,
			mat_name + " metallic_texture_channel = BLUE (glTF B channel)")
		check(mat.roughness_texture_channel == BaseMaterial3D.TEXTURE_CHANNEL_GREEN,
			mat_name + " roughness_texture_channel = GREEN (glTF G channel)")

	# ── No AO texture: no occlusionTexture in GLTF → Findings F-1 ────────────
	for pair in [["rigging", rigging_mat], ["hull", hull_mat], ["sails", sails_mat]]:
		var mat: StandardMaterial3D = pair[1]
		if mat == null:
			continue
		check(mat.ao_texture == null,
			pair[0] + " ao_texture = null (no occlusionTexture declared in GLTF)")

	# ── Material flags and scalars ─────────────────────────────────────────────
	# rigging: opaque, double-sided, metallic=1.0, roughness=1.0 (glTF defaults)
	if rigging_mat:
		check(rigging_mat.transparency == BaseMaterial3D.TRANSPARENCY_DISABLED,
			"rigging transparency = DISABLED (alphaMode omitted → OPAQUE)")
		check(rigging_mat.cull_mode == BaseMaterial3D.CULL_DISABLED,
			"rigging cull_mode = DISABLED (doubleSided: true)")
		check(is_equal_approx(rigging_mat.metallic, 1.0),
			"rigging metallic = 1.0 (metallicFactor absent → glTF default)")
		check(is_equal_approx(rigging_mat.roughness, 1.0),
			"rigging roughness = 1.0 (roughnessFactor absent → glTF default)")

	# hull: opaque, double-sided, metallic=1.0, roughness=1.0
	if hull_mat:
		check(hull_mat.transparency == BaseMaterial3D.TRANSPARENCY_DISABLED,
			"hull transparency = DISABLED (alphaMode omitted → OPAQUE)")
		check(hull_mat.cull_mode == BaseMaterial3D.CULL_DISABLED,
			"hull cull_mode = DISABLED (doubleSided: true)")
		check(is_equal_approx(hull_mat.metallic, 1.0),
			"hull metallic = 1.0 (metallicFactor absent → glTF default)")
		check(is_equal_approx(hull_mat.roughness, 1.0),
			"hull roughness = 1.0 (roughnessFactor absent → glTF default)")

	# sails: alpha scissor at 0.5, double-sided, metallic=0.0 (explicit), roughness=1.0
	if sails_mat:
		check(sails_mat.transparency == BaseMaterial3D.TRANSPARENCY_ALPHA_SCISSOR,
			"sails transparency = ALPHA_SCISSOR (alphaMode: MASK)")
		check(is_equal_approx(sails_mat.alpha_scissor_threshold, 0.5),
			"sails alpha_scissor_threshold = 0.5 (alphaCutoff: 0.5)")
		check(sails_mat.cull_mode == BaseMaterial3D.CULL_DISABLED,
			"sails cull_mode = DISABLED (doubleSided: true)")
		check(is_equal_approx(sails_mat.metallic, 0.0),
			"sails metallic = 0.0 (metallicFactor: 0)")
		check(is_equal_approx(sails_mat.roughness, 1.0),
			"sails roughness = 1.0 (roughnessFactor absent → glTF default)")

	# ── Import settings via ConfigFile ────────────────────────────────────────
	# One representative check per texture across all three compress/mode and
	# normal_map values. Covers all nine textures via the matrix below.
	var import_checks: Array = [
		# diff textures: mode=0, normal_map=0, mipmaps=true, detect_3d=0
		["res://polyhaven/textures/dutch_ship_medium_hull_diff_1k.jpg.import",
			"params", "compress/mode",        0,    "hull_diff compress/mode=0"],
		["res://polyhaven/textures/dutch_ship_medium_hull_diff_1k.jpg.import",
			"params", "compress/normal_map",   0,    "hull_diff compress/normal_map=0"],
		["res://polyhaven/textures/dutch_ship_medium_hull_diff_1k.jpg.import",
			"params", "mipmaps/generate",      true, "hull_diff mipmaps/generate=true"],
		["res://polyhaven/textures/dutch_ship_medium_hull_diff_1k.jpg.import",
			"params", "detect_3d/compress_to", 0,    "hull_diff detect_3d/compress_to=0"],
		["res://polyhaven/textures/dutch_ship_medium_rigging_diff_1k.jpg.import",
			"params", "compress/mode",         0,    "rigging_diff compress/mode=0"],
		["res://polyhaven/textures/dutch_ship_medium_sails_diff_1k.jpg.import",
			"params", "compress/mode",         0,    "sails_diff compress/mode=0"],
		# nor_gl textures: mode=0, normal_map=1, mipmaps=true, detect_3d=0
		["res://polyhaven/textures/dutch_ship_medium_hull_nor_gl_1k.jpg.import",
			"params", "compress/mode",        0,    "hull_nor compress/mode=0"],
		["res://polyhaven/textures/dutch_ship_medium_hull_nor_gl_1k.jpg.import",
			"params", "compress/normal_map",   1,    "hull_nor compress/normal_map=1"],
		["res://polyhaven/textures/dutch_ship_medium_hull_nor_gl_1k.jpg.import",
			"params", "mipmaps/generate",      true, "hull_nor mipmaps/generate=true"],
		["res://polyhaven/textures/dutch_ship_medium_hull_nor_gl_1k.jpg.import",
			"params", "detect_3d/compress_to", 0,    "hull_nor detect_3d/compress_to=0"],
		["res://polyhaven/textures/dutch_ship_medium_rigging_nor_gl_1k.jpg.import",
			"params", "compress/normal_map",   1,    "rigging_nor compress/normal_map=1"],
		["res://polyhaven/textures/dutch_ship_medium_sails_nor_gl_1k.jpg.import",
			"params", "compress/normal_map",   1,    "sails_nor compress/normal_map=1"],
		# arm textures: mode=0, normal_map=0, mipmaps=true, detect_3d=0
		["res://polyhaven/textures/dutch_ship_medium_hull_arm_1k.jpg.import",
			"params", "compress/mode",         0,    "hull_arm compress/mode=0"],
		["res://polyhaven/textures/dutch_ship_medium_hull_arm_1k.jpg.import",
			"params", "compress/normal_map",   0,    "hull_arm compress/normal_map=0"],
		["res://polyhaven/textures/dutch_ship_medium_hull_arm_1k.jpg.import",
			"params", "mipmaps/generate",      true, "hull_arm mipmaps/generate=true"],
		["res://polyhaven/textures/dutch_ship_medium_hull_arm_1k.jpg.import",
			"params", "detect_3d/compress_to", 0,    "hull_arm detect_3d/compress_to=0"],
		["res://polyhaven/textures/dutch_ship_medium_rigging_arm_1k.jpg.import",
			"params", "compress/mode",         0,    "rigging_arm compress/mode=0"],
		["res://polyhaven/textures/dutch_ship_medium_sails_arm_1k.jpg.import",
			"params", "compress/mode",         0,    "sails_arm compress/mode=0"],
	]
	for ic in import_checks:
		var cf := ConfigFile.new()
		var err := cf.load(ic[0])
		check(err == OK, ic[0].get_file() + " opens")
		if err == OK:
			var val = cf.get_value(ic[1], ic[2], null)
			check(val == ic[3], ic[4])

	# ── Pixel checks: blue-channel heuristic to distinguish normal maps ───────
	# Tangent-space normal maps store Z (outward direction) in blue as (Z+1)/2.
	# All valid tangent-space normals have Z > 0, so blue > 0.5 on ≥ 95 % of
	# texels is a plausible sanity check. Diffuse/color images should NOT satisfy
	# this condition (expected ratio < 0.95).
	var pixel_cases: Array = [
		# [res_path, expect_normal_like (≥95% blue > 0.5)]
		["res://polyhaven/textures/dutch_ship_medium_hull_nor_gl_1k.jpg",     true],
		["res://polyhaven/textures/dutch_ship_medium_rigging_nor_gl_1k.jpg",  true],
		["res://polyhaven/textures/dutch_ship_medium_sails_nor_gl_1k.jpg",    true],
		["res://polyhaven/textures/dutch_ship_medium_hull_diff_1k.jpg",       false],
		["res://polyhaven/textures/dutch_ship_medium_rigging_diff_1k.jpg",    false],
		["res://polyhaven/textures/dutch_ship_medium_sails_diff_1k.jpg",      false],
	]
	for pc in pixel_cases:
		check_blue_ratio(pc[0], pc[1])

	print("RESULT ", checks, " checks, ", failures, " failures; headless state only — see below for limitations")
	print("")
	print("Cannot establish headlessly:")
	print("  - Visual rendering correctness (dummy renderer draws nothing)")
	print("  - Alpha scissor actually clips sails: JPEG diff has no alpha channel")
	print("    (Findings F-2), so every pixel passes the 0.5 threshold at runtime")
	print("  - AO channel effectiveness: ao_texture is null (Findings F-1)")
	print("  - GPU VRAM usage: all textures use lossless mode (Findings F-3)")
	print("  - That SDFGI/glow/fog/SSAO environment effects visually affect the ship")
	print("  - Performance (FPS, draw call count, shadow map quality)")

	ship.queue_free()
	await process_frame
	quit(1 if failures else 0)


func check_blue_ratio(res_path: String, expect_normal_like: bool) -> void:
	var abs_path: String = ProjectSettings.globalize_path(res_path)
	var img: Image = Image.load_from_file(abs_path)
	var label: String = res_path.get_file()
	if img == null:
		check(false, label + " image load failed")
		return
	var w := img.get_width()
	var h := img.get_height()
	# Sample every 16th pixel in both axes (~4096 samples on a 1024×1024 image).
	var step := 16
	var blue_above := 0
	var total := 0
	for x in range(0, w, step):
		for y in range(0, h, step):
			total += 1
			if img.get_pixel(x, y).b > 0.5:
				blue_above += 1
	var ratio := float(blue_above) / float(total)
	var is_normal_like := ratio >= 0.95
	var tag := " (expect ≥0.95 = normal map)" if expect_normal_like else " (expect <0.95 = not a normal map)"
	check(is_normal_like == expect_normal_like,
		label + " blue>0.5 ratio=%.3f" % ratio + tag)
