class_name Lessons
extends RefCounted
# The lesson table: which .gdshader belongs to which original .cgfx, which generated textures it needs, and the demo values the stage uses.
# The numbers in the file names are the ORIGINAL CgFX numbers (traceability), nothing else.

const NAMES: Array[String] = [
	"00_super_simple", "01_base", "02_lambert", "03_lambert_ambient", "04_fresnel", "05_phong",
	"06_diffuse_mapped", "07_spec_mapped", "08_normal_mapped", "09_cube_mapped", "10_vertex_anim", "11_uv_manip",
	"12_techniques", "13_blended", "14_car_shader", "15_uber"]

static var use_mips := true      # the stage keeps mip chains; tools/verify.gd switches them off so level 0 is the only level the reference has to model

const CUBE_ORDER: Array[String] = ["px", "nx", "py", "ny", "pz", "nz"]   # +X, -X, +Y, -Y, +Z, -Z

# demo values the STAGE applies on top of the shaders' own defaults (the defaults mirror the Cg defaults)
static func demo(i: int) -> Dictionary:
	match i:
		0: return {"shader_color": Color("#5FA391")}
		10: return {"vert_offset": Vector3(0.0, 0.25, 0.0), "animation_frequency": 3.0, "animation_speed": 3.0}
		11: return {"uv_scale_translate": Vector4(2.0, 2.0, 0.0, 0.0), "speed_xy": Vector2(0.1, 0.0)}
		14: return {"shader_color": Color(0.55, 0.08, 0.08), "reflection_contrast": 2.0, "specular_power2": 8.0}
	return {}

static func shader_path(i: int) -> String:
	return "res://shaders/%s.gdshader" % NAMES[i]

static func load_image(file: String) -> Image:
	var img := Image.load_from_file(ProjectSettings.globalize_path("res://textures/" + file))
	img.convert(Image.FORMAT_RGBA8)
	return img

static func load_texture(file: String) -> ImageTexture:
	var img := load_image(file)
	if use_mips:
		img.generate_mipmaps()
	return ImageTexture.create_from_image(img)

static func load_cubemap() -> Cubemap:
	var faces: Array[Image] = []
	for f in CUBE_ORDER:
		faces.append(load_image("cube_%s.png" % f))
	var cube := Cubemap.new()
	cube.create_from_images(faces)
	return cube

# the texture a sampler uniform gets, by uniform name and lesson (lesson 15 uses its own channel packing and a DirectX-style normal map)
static func texture_for(uniform_name: String, lesson: int) -> Variant:
	match uniform_name:
		"diffuse_map": return load_texture("diffuse_checker.png")
		"spec_map": return load_texture("spec_uber.png" if lesson == 15 else "spec_rg.png")
		"normal_map": return load_texture("normal_dx.png" if lesson == 15 else "normal_gl.png")
		"blend_map": return load_texture("blend_map.png")
		"reflection_map": return load_cubemap()
	return null

# Builds the ShaderMaterial for lesson i. `code` replaces the file's source (used to test variants); `overrides` are applied last.
static func material(i: int, overrides := {}, code := "", with_demo := true) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = code if code != "" else FileAccess.get_file_as_string(shader_path(i))
	var mat := ShaderMaterial.new()
	mat.shader = sh
	for u in sh.get_shader_uniform_list():
		var t: Variant = texture_for(String(u["name"]), i)
		if t != null:
			mat.set_shader_parameter(String(u["name"]), t)
	if with_demo:
		for k in demo(i):
			mat.set_shader_parameter(k, demo(i)[k])
	for k in overrides:
		mat.set_shader_parameter(k, overrides[k])
	return mat
