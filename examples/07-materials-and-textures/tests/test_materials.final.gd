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
	# hull uses ORMMaterial3D from the external .tres; rigging/sails still use
	# the importer-generated StandardMaterial3D.
	var rigging_mat: StandardMaterial3D = rigging.mesh.surface_get_material(0) if rigging else null
	var hull_mat:    BaseMaterial3D     = hull.mesh.surface_get_material(0)    if hull    else null
	var sails_mat:   StandardMaterial3D = sails.mesh.surface_get_material(0)   if sails   else null
	check(rigging_mat is StandardMaterial3D, "rigging material is StandardMaterial3D")
	check(hull_mat    is ORMMaterial3D,      "hull material is ORMMaterial3D (external tres)")
	check(sails_mat   is StandardMaterial3D, "sails material is StandardMaterial3D")

	# ── Hull external material path ───────────────────────────────────────────
	# Verifies the Use External wire-up in dutch_ship_medium_1k.gltf.import
	# caused the importer to substitute the .tres instead of generating one.
	if hull_mat != null:
		check(hull_mat.resource_path.ends_with("dutch_ship_medium_hull.tres"),
			"hull resource_path ends with dutch_ship_medium_hull.tres (Use External wired)")

	# ── Texture paths (one row per slot per material, matching MATERIALS.md table) ──
	# Hull uses orm_texture instead of separate metallic/roughness textures.
	# Rigging and sails are unchanged (StandardMaterial3D from GLTF importer).
	var tex_expectations: Array = [
		# [mat, property, expected filename suffix]
		[rigging_mat, "albedo_texture",   "dutch_ship_medium_rigging_diff_1k.jpg"],
		[rigging_mat, "normal_texture",   "dutch_ship_medium_rigging_nor_gl_1k.jpg"],
		[rigging_mat, "metallic_texture", "dutch_ship_medium_rigging_arm_1k.jpg"],
		[rigging_mat, "roughness_texture","dutch_ship_medium_rigging_arm_1k.jpg"],
		# hull: albedo and normal unchanged; metallic/roughness folded into orm_texture
		[hull_mat,    "albedo_texture",   "dutch_ship_medium_hull_diff_1k.jpg"],
		[hull_mat,    "normal_texture",   "dutch_ship_medium_hull_nor_gl_1k.jpg"],
		[hull_mat,    "orm_texture",      "dutch_ship_medium_hull_arm_1k.jpg"],
		[sails_mat,   "albedo_texture",   "dutch_ship_medium_sails_diff_1k.jpg"],
		[sails_mat,   "normal_texture",   "dutch_ship_medium_sails_nor_gl_1k.jpg"],
		[sails_mat,   "metallic_texture", "dutch_ship_medium_sails_arm_1k.jpg"],
		[sails_mat,   "roughness_texture","dutch_ship_medium_sails_arm_1k.jpg"],
	]
	for entry in tex_expectations:
		var mat: BaseMaterial3D = entry[0]
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

	# ── Hull AO from the red channel of the ARM texture (Findings F-1 fix) ───
	# ORMMaterial3D always maps its orm_texture as R=AO, G=Roughness, B=Metallic.
	# ORMMaterial3D's packed texture is the proof: its fixed layout is R=AO,
	# G=roughness, B=metallic. The separate ao_texture slot remains unused.
	if hull_mat != null:
		var hull_orm_tex: Texture2D = hull_mat.get("orm_texture")
		check(hull_orm_tex != null,
			"hull orm_texture != null (ORM fixed layout uses red for AO)")
		if hull_orm_tex != null:
			check(hull_orm_tex.resource_path.ends_with("dutch_ship_medium_hull_arm_1k.jpg"),
				"hull orm_texture is ARM map (R channel drives AO)")
		check(hull_mat.ao_texture_channel == BaseMaterial3D.TEXTURE_CHANNEL_RED,
			"hull ao_texture_channel remains RED")
		# Human review: an ORM material emits AO = orm_tex.r only when the AO
		# feature is on (scene/resources/material.cpp, 4.7.2). Without this check
		# the change can pass every other assertion and still add no AO.
		check(hull_mat.ao_enabled,
			"hull ao_enabled = true (ORM red channel is read only when AO is on)")

	# ── Texture channels (glTF metallicRoughness: B=metallic, G=roughness) ───
	# Rigging and sails are StandardMaterial3D with explicit channel settings from
	# the GLTF importer.  Hull is ORMMaterial3D: the ORM shader always samples
	# B=metallic, G=roughness internally, and metallic_texture_channel=BLUE is set
	# explicitly in the .tres so the property value matches the rendering.
	if rigging_mat:
		check(rigging_mat.metallic_texture_channel == BaseMaterial3D.TEXTURE_CHANNEL_BLUE,
			"rigging metallic_texture_channel = BLUE (glTF B channel)")
		check(rigging_mat.roughness_texture_channel == BaseMaterial3D.TEXTURE_CHANNEL_GREEN,
			"rigging roughness_texture_channel = GREEN (glTF G channel)")
	if hull_mat:
		check(hull_mat.metallic_texture_channel == BaseMaterial3D.TEXTURE_CHANNEL_BLUE,
			"hull metallic_texture_channel = BLUE (ORM B channel, set in .tres)")
		check(hull_mat.roughness_texture_channel == BaseMaterial3D.TEXTURE_CHANNEL_GREEN,
			"hull roughness_texture_channel = GREEN (ORM G channel)")
	if sails_mat:
		check(sails_mat.metallic_texture_channel == BaseMaterial3D.TEXTURE_CHANNEL_BLUE,
			"sails metallic_texture_channel = BLUE (glTF B channel)")
		check(sails_mat.roughness_texture_channel == BaseMaterial3D.TEXTURE_CHANNEL_GREEN,
			"sails roughness_texture_channel = GREEN (glTF G channel)")

	# ── No AO texture for rigging and sails (F-1 unchanged) ──────────────────
	# Only the hull has been upgraded to ORMMaterial3D; rigging and sails still
	# have no occlusionTexture declared in the GLTF so ao_texture stays null.
	for pair in [["rigging", rigging_mat], ["sails", sails_mat]]:
		var mat: BaseMaterial3D = pair[1]
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

	# hull: ORMMaterial3D external .tres; all audited values preserved except
	# that AO is now active from the arm R channel (the intended change).
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

	# Prove the persistent Advanced Import Settings > Material > Use External
	# mapping itself, not only the current imported cache.
	var scene_import := ConfigFile.new()
	var scene_import_err := scene_import.load(
		"res://polyhaven/dutch_ship_medium_1k.gltf.import")
	check(scene_import_err == OK, "ship glTF import settings open")
	if scene_import_err == OK:
		var subresources: Dictionary = scene_import.get_value("params", "_subresources", {})
		var material_settings: Dictionary = subresources.get("materials", {})
		var hull_settings: Dictionary = material_settings.get("dutch_ship_medium_hull", {})
		check(hull_settings.get("use_external/enabled", false) == true,
			"hull Use External is enabled in glTF import settings")
		check(hull_settings.get("use_external/fallback_path", "") ==
				"res://materials/dutch_ship_medium_hull.tres",
			"hull Use External fallback path targets the ORM material")
		var external_uid: String = hull_settings.get("use_external/path", "")
		check(external_uid.begins_with("uid://") and
				ResourceUID.get_id_path(ResourceUID.text_to_id(external_uid)) ==
				"res://materials/dutch_ship_medium_hull.tres",
			"hull Use External UID resolves to the ORM material")

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
	print("  - GPU VRAM usage: all textures use lossless mode (Findings F-3)")
	print("  - That SDFGI/glow/fog/SSAO environment effects visually affect the ship")
	print("  - Performance (FPS, draw call count, shadow map quality)")
	print("  - Hull AO visual strength: orm_texture is wired with R=AO, but")
	print("    ao_light_affect (default 0.0) and the actual darkening need")
	print("    visual inspection in the running scene (see human checks below)")

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
