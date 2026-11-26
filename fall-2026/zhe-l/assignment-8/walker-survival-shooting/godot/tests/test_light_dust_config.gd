extends SceneTree

const EFFECT_SCENE := "res://effects/light_dust.tscn"
const EPS := 0.0001

const AMOUNT := 1300
const LIFETIME := 6.0
const LIFETIME_RANDOMNESS := 0.5
const BOX_EXTENTS := Vector3(7.0, 1.3, 4.5)
const BOX_FULL_SIZE := Vector3(14.0, 2.6, 9.0)
const BOX_OFFSET := Vector3(0.0, 0.15, 3.2)
const SPREAD := 180.0
const VELOCITY := Vector2(0.01, 0.04)
const TURBULENCE_STRENGTH := 1.0
const TURBULENCE_SCALE := 4.0
const TURBULENCE_INFLUENCE := Vector2(0.02, 0.06)
const SCALE := Vector2(0.1, 1.0)
const COLOR := Color(0.39, 0.43, 0.5)
const OPACITY_KEYS := [[0.0, 0.0], [0.10, 0.6], [0.25, 0.15], [0.40, 0.9], [0.55, 0.2], [0.70, 0.7], [0.85, 0.1], [1.0, 0.0]]
const QUAD := Vector2(0.03, 0.03)
const SPECK_SIZE := Vector2(0.003, 0.03)
const AABB_BOX := AABB(Vector3(-7.3, -1.45, -1.6), Vector3(14.6, 3.2, 9.6))
const PREPROCESS := 6.0

const PROPERTY_NAMES := {
	"GPUParticles3D": ["emitting", "amount", "lifetime", "one_shot", "explosiveness", "preprocess", "local_coords",
		"visibility_aabb", "process_material", "draw_pass_1", "cast_shadow"],
	"ParticleProcessMaterial": ["lifetime_randomness", "emission_shape", "emission_box_extents", "direction", "spread", "flatness",
		"initial_velocity_min", "initial_velocity_max", "gravity", "turbulence_enabled", "turbulence_noise_strength",
		"turbulence_noise_scale", "turbulence_influence_min", "turbulence_influence_max", "scale_min", "scale_max",
		"color", "color_ramp", "emission_shape_offset"],
	"QuadMesh": ["size", "material"],
	"StandardMaterial3D": ["shading_mode", "transparency", "blend_mode", "vertex_color_use_as_albedo", "billboard_mode",
		"billboard_keep_scale", "albedo_texture"],
	"GradientTexture2D": ["gradient", "fill", "fill_from", "fill_to"],
}

var _failures := 0
var _passes := 0


func _init() -> void:
	_check_property_names()
	var packed := load(EFFECT_SCENE) as PackedScene
	if not _check("%s loads as a PackedScene" % EFFECT_SCENE, packed != null):
		_finish()
		return
	var root := packed.instantiate()
	var dust := _check_root(root)
	if dust != null:
		_check_node(dust)
		_check_process(dust)
		_check_draw(dust)
	root.free()
	_finish()


func _check_property_names() -> void:
	for cls_name in PROPERTY_NAMES:
		var known := {}
		for prop in ClassDB.class_get_property_list(cls_name):
			known[prop.name] = true
		for prop_name in PROPERTY_NAMES[cls_name]:
			_check("ClassDB: %s.%s exists" % [cls_name, prop_name], known.has(prop_name))


func _check_root(root: Node) -> GPUParticles3D:
	_check("root is a GPUParticles3D (got %s)" % root.get_class(), root.get_class() == "GPUParticles3D")
	_check("root has no children (got %d)" % root.get_child_count(), root.get_child_count() == 0)
	return root as GPUParticles3D


func _check_node(p: GPUParticles3D) -> void:
	_check("amount = %d (got %d)" % [AMOUNT, p.amount], p.amount == AMOUNT)
	_near("lifetime", p.lifetime, LIFETIME)
	_check("one_shot is off", not p.one_shot)
	_near("explosiveness", p.explosiveness, 0.0)
	_near("preprocess", p.preprocess, PREPROCESS)
	_check("local_coords is off", not p.local_coords)
	_check("visibility_aabb = %s (got %s)" % [AABB_BOX, p.visibility_aabb], p.visibility_aabb.is_equal_approx(AABB_BOX))
	_check("cast_shadow is OFF", p.cast_shadow == GeometryInstance3D.SHADOW_CASTING_SETTING_OFF)
	_check("emitting is off in the scene file (added, not in the brief)", not p.emitting)
	var emission_box := AABB(BOX_OFFSET - BOX_EXTENTS, BOX_EXTENTS * 2.0)
	_check("visibility_aabb encloses the emission box", p.visibility_aabb.encloses(emission_box))


func _check_process(p: GPUParticles3D) -> void:
	var pm := p.process_material as ParticleProcessMaterial
	if not _check("process_material is a ParticleProcessMaterial", pm != null):
		return
	_near("lifetime_randomness", pm.lifetime_randomness, LIFETIME_RANDOMNESS)
	_check("emission_shape is BOX (got %d)" % pm.emission_shape, pm.emission_shape == ParticleProcessMaterial.EMISSION_SHAPE_BOX)
	_vec("emission_box_extents", pm.emission_box_extents, BOX_EXTENTS)
	_vec("emission box full size", pm.emission_box_extents * 2.0, BOX_FULL_SIZE)
	_vec("emission_shape_offset", pm.emission_shape_offset, BOX_OFFSET)
	_near("spread", pm.spread, SPREAD)
	_near("flatness (added, not in the brief)", pm.flatness, 0.0)
	_near("initial_velocity_min", pm.initial_velocity_min, VELOCITY.x)
	_near("initial_velocity_max", pm.initial_velocity_max, VELOCITY.y)
	_vec("gravity", pm.gravity, Vector3.ZERO)
	_check("turbulence_enabled is on", pm.turbulence_enabled)
	_near("turbulence_noise_strength", pm.turbulence_noise_strength, TURBULENCE_STRENGTH)
	_near("turbulence_noise_scale", pm.turbulence_noise_scale, TURBULENCE_SCALE)
	_near("turbulence_influence_min", pm.turbulence_influence_min, TURBULENCE_INFLUENCE.x)
	_near("turbulence_influence_max", pm.turbulence_influence_max, TURBULENCE_INFLUENCE.y)
	_near("scale_min", pm.scale_min, SCALE.x)
	_near("scale_max", pm.scale_max, SCALE.y)
	_color("color", pm.color, COLOR)
	var gt := pm.color_ramp as GradientTexture1D
	if not _check("color_ramp is a GradientTexture1D with a Gradient", gt != null and gt.gradient != null):
		return
	for key in OPACITY_KEYS:
		var c := gt.gradient.sample(key[0])
		_near("opacity at life %.2f" % key[0], c.a, key[1])
		_color("ramp rgb at life %.2f stays white" % key[0], Color(c.r, c.g, c.b), Color.WHITE)


func _check_draw(p: GPUParticles3D) -> void:
	var mesh := p.draw_pass_1 as QuadMesh
	if not _check("draw_pass_1 is a QuadMesh (got %s)" % [p.draw_pass_1.get_class() if p.draw_pass_1 else "null"], mesh != null):
		return
	_vec2("QuadMesh size", mesh.size, QUAD)
	var pm := p.process_material as ParticleProcessMaterial
	if pm != null:
		_near("smallest speck (quad x scale_min, m)", mesh.size.x * pm.scale_min, SPECK_SIZE.x)
		_near("largest speck (quad x scale_max, m)", mesh.size.x * pm.scale_max, SPECK_SIZE.y)
	var mat := mesh.material as StandardMaterial3D
	if not _check("draw material is a StandardMaterial3D", mat != null):
		return
	_check("shading_mode is PER_PIXEL (lit)", mat.shading_mode == BaseMaterial3D.SHADING_MODE_PER_PIXEL)
	_check("blend_mode is ADD", mat.blend_mode == BaseMaterial3D.BLEND_MODE_ADD)
	_check("transparency is ALPHA", mat.transparency == BaseMaterial3D.TRANSPARENCY_ALPHA)
	_check("vertex_color_use_as_albedo is on", mat.vertex_color_use_as_albedo)
	_check("billboard_mode is PARTICLES (got %d)" % mat.billboard_mode, mat.billboard_mode == BaseMaterial3D.BILLBOARD_PARTICLES)
	_check("billboard_keep_scale is on (added, not in the brief)", mat.billboard_keep_scale)
	var g := mat.albedo_texture as GradientTexture2D
	if not _check("albedo_texture is a GradientTexture2D", g != null and g.gradient != null):
		return
	_check("texture fill is RADIAL", g.fill == GradientTexture2D.FILL_RADIAL)
	_vec2("texture fill_from (centre)", g.fill_from, Vector2(0.5, 0.5))
	_near("texture radius reaches the edge", g.fill_from.distance_to(g.fill_to), 0.5)
	_near("texture alpha at centre", g.gradient.sample(0.0).a, 1.0)
	_near("texture alpha at edge", g.gradient.sample(1.0).a, 0.0)
	_check("texture edge is soft (alpha at half radius is between)", g.gradient.sample(0.5).a > 0.1 and g.gradient.sample(0.5).a < 0.9)


func _check(label: String, ok: bool) -> bool:
	print(("  PASS  " if ok else "  FAIL  ") + label)
	if ok:
		_passes += 1
	else:
		_failures += 1
	return ok


func _near(label: String, got: float, want: float) -> void:
	_check("%s = %s (got %s)" % [label, want, got], absf(got - want) <= EPS)


func _vec(label: String, got: Vector3, want: Vector3) -> void:
	_check("%s = %s (got %s)" % [label, want, got], absf(got.x - want.x) <= EPS and absf(got.y - want.y) <= EPS and absf(got.z - want.z) <= EPS)


func _vec2(label: String, got: Vector2, want: Vector2) -> void:
	_check("%s = %s (got %s)" % [label, want, got], absf(got.x - want.x) <= EPS and absf(got.y - want.y) <= EPS)


func _color(label: String, got: Color, want: Color) -> void:
	var ok := absf(got.r - want.r) <= EPS and absf(got.g - want.g) <= EPS and absf(got.b - want.b) <= EPS
	_check("%s = (%.2f, %.2f, %.2f) (got (%.4f, %.4f, %.4f))" % [label, want.r, want.g, want.b, got.r, got.g, got.b], ok)


func _finish() -> void:
	print("== %d passed, %d failed ==" % [_passes, _failures])
	quit(1 if _failures > 0 else 0)
