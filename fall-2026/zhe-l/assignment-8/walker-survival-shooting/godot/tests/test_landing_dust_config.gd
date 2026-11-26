extends SceneTree

const EFFECT_SCENE := "res://effects/landing_dust.tscn"
const EPS := 0.0001
const FLOOR_LIMIT := 0.30
const RING_FINAL_DIAMETER := 0.90

const DUST_AMOUNT := 24
const DUST_LIFETIME := 1.6
const DUST_LIFETIME_RANDOMNESS := 0.2
const DUST_RING_RADIUS := 0.2
const DUST_RING_INNER_RADIUS := 0.05
const DUST_SPREAD := 180.0
const DUST_FLATNESS := 1.0
const DUST_VELOCITY := Vector2(0.6, 0.9)
const DUST_DAMPING := Vector2(1.4, 1.8)
const DUST_ANGLE := Vector2(0.0, 360.0)
const DUST_SCALE := Vector2(0.8, 1.2)
const DUST_SCALE_CURVE := Vector2(0.6, 1.0)
const DUST_COLOR := Color(0.48, 0.45, 0.40)
const DUST_OPACITY_KEYS := [[0.0, 0.0], [0.15, 0.6], [0.8, 0.15], [1.6, 0.0]]
const DUST_QUAD := Vector2(0.32, 0.32)
const DUST_HEIGHT := 0.04
const DUST_AABB := AABB(Vector3(-0.6, -0.1, -0.6), Vector3(1.2, 0.3, 1.2))

const RING_AMOUNT := 1
const RING_LIFETIME := 0.45
const RING_GROWN_SECONDS := 0.30
const RING_SCALE_START := 0.2
const RING_COLOR := Color(0.62, 0.59, 0.53)
const RING_OPACITY_START := 0.35
const RING_QUAD := Vector2(0.9, 0.9)
const RING_HEIGHT := 0.01
const RING_AABB := AABB(Vector3(-0.5, -0.05, -0.5), Vector3(1.0, 0.1, 1.0))

const PROPERTY_NAMES := {
	"GPUParticles3D": ["emitting", "amount", "lifetime", "one_shot", "explosiveness", "preprocess", "local_coords",
		"visibility_aabb", "process_material", "draw_pass_1", "cast_shadow"],
	"ParticleProcessMaterial": ["lifetime_randomness", "emission_shape", "emission_ring_axis", "emission_ring_radius",
		"emission_ring_inner_radius", "emission_ring_height", "direction", "spread", "flatness", "initial_velocity_min",
		"initial_velocity_max", "damping_min", "damping_max", "gravity", "angle_min", "angle_max", "scale_min", "scale_max",
		"scale_curve", "color", "color_ramp"],
	"QuadMesh": ["size", "orientation", "material"],
	"StandardMaterial3D": ["shading_mode", "transparency", "vertex_color_use_as_albedo", "billboard_mode",
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
	_check_root(root)
	var dust := root.get_node_or_null("Dust") as GPUParticles3D
	var ring := root.get_node_or_null("GroundRing") as GPUParticles3D
	if dust != null:
		_check_dust(dust)
	if ring != null:
		_check_ring(ring)
	if dust != null and ring != null:
		_check_derived(dust, ring)
	_report_initial_velocity()
	root.free()
	_finish()


func _check_property_names() -> void:
	for cls_name in PROPERTY_NAMES:
		var known := {}
		for prop in ClassDB.class_get_property_list(cls_name):
			known[prop.name] = true
		for prop_name in PROPERTY_NAMES[cls_name]:
			_check("ClassDB: %s.%s exists" % [cls_name, prop_name], known.has(prop_name))


func _check_root(root: Node) -> void:
	_check("root is a Node3D (got %s)" % root.get_class(), root.get_class() == "Node3D")
	var names: Array[String] = []
	for child in root.get_children():
		names.append(child.name)
	_check("root children are [Dust, GroundRing] (got %s)" % [names], names == ["Dust", "GroundRing"])
	for child in root.get_children():
		_check("%s is a GPUParticles3D (got %s)" % [child.name, child.get_class()], child.get_class() == "GPUParticles3D")


func _check_dust(dust: GPUParticles3D) -> void:
	_check_emitter_node(dust, DUST_AMOUNT, DUST_LIFETIME, DUST_HEIGHT, DUST_AABB)
	var pm := dust.process_material as ParticleProcessMaterial
	if not _check("Dust process_material is a ParticleProcessMaterial", pm != null):
		return
	_near("Dust lifetime_randomness", pm.lifetime_randomness, DUST_LIFETIME_RANDOMNESS)
	_check("Dust emission_shape is RING (got %d)" % pm.emission_shape, pm.emission_shape == ParticleProcessMaterial.EMISSION_SHAPE_RING)
	_vec("Dust emission_ring_axis", pm.emission_ring_axis, Vector3(0, 1, 0))
	_near("Dust emission_ring_radius", pm.emission_ring_radius, DUST_RING_RADIUS)
	_near("Dust emission_ring_inner_radius", pm.emission_ring_inner_radius, DUST_RING_INNER_RADIUS)
	_near("Dust emission_ring_height", pm.emission_ring_height, 0.0)
	_vec("Dust direction", pm.direction, Vector3(1, 0, 0))
	_near("Dust spread", pm.spread, DUST_SPREAD)
	_near("Dust flatness", pm.flatness, DUST_FLATNESS)
	_near("Dust initial_velocity_min", pm.initial_velocity_min, DUST_VELOCITY.x)
	_near("Dust initial_velocity_max", pm.initial_velocity_max, DUST_VELOCITY.y)
	_near("Dust damping_min", pm.damping_min, DUST_DAMPING.x)
	_near("Dust damping_max", pm.damping_max, DUST_DAMPING.y)
	_vec("Dust gravity", pm.gravity, Vector3.ZERO)
	_near("Dust angle_min", pm.angle_min, DUST_ANGLE.x)
	_near("Dust angle_max", pm.angle_max, DUST_ANGLE.y)
	_near("Dust scale_min", pm.scale_min, DUST_SCALE.x)
	_near("Dust scale_max", pm.scale_max, DUST_SCALE.y)
	var curve := _curve_of(pm.scale_curve, "Dust scale_curve")
	if curve != null:
		_near("Dust scale_curve at life 0", curve.sample(0.0), DUST_SCALE_CURVE.x)
		_near("Dust scale_curve at life 0.5", curve.sample(0.5), lerpf(DUST_SCALE_CURVE.x, DUST_SCALE_CURVE.y, 0.5))
		_near("Dust scale_curve at life 1", curve.sample(1.0), DUST_SCALE_CURVE.y)
	_color("Dust color", pm.color, DUST_COLOR)
	var ramp := _ramp_of(pm.color_ramp, "Dust color_ramp")
	if ramp != null:
		for key in DUST_OPACITY_KEYS:
			var life: float = key[0] / DUST_LIFETIME
			var c := ramp.sample(life)
			_near("Dust opacity at %.2f s (life %.4f)" % [key[0], life], c.a, key[1])
			_color("Dust ramp rgb at %.2f s stays white" % key[0], Color(c.r, c.g, c.b), Color.WHITE)
	var mesh := _quad_of(dust, "Dust")
	if mesh != null:
		_vec2("Dust QuadMesh size", mesh.size, DUST_QUAD)
		var mat := _material_of(mesh, "Dust")
		if mat != null:
			_check_draw_switches(mat, "Dust", BaseMaterial3D.BILLBOARD_PARTICLES)
			_check("Dust billboard_keep_scale is on (added, not in the brief)", mat.billboard_keep_scale)
			_check_round_texture(mat.albedo_texture, "Dust")


func _check_ring(ring: GPUParticles3D) -> void:
	_check_emitter_node(ring, RING_AMOUNT, RING_LIFETIME, RING_HEIGHT, RING_AABB)
	var pm := ring.process_material as ParticleProcessMaterial
	if not _check("GroundRing process_material is a ParticleProcessMaterial", pm != null):
		return
	_near("GroundRing lifetime_randomness", pm.lifetime_randomness, 0.0)
	_near("GroundRing initial_velocity_min", pm.initial_velocity_min, 0.0)
	_near("GroundRing initial_velocity_max", pm.initial_velocity_max, 0.0)
	_vec("GroundRing gravity", pm.gravity, Vector3.ZERO)
	_check("GroundRing scale_min/max stay 1 (fixed size)", is_equal_approx(pm.scale_min, 1.0) and is_equal_approx(pm.scale_max, 1.0))
	var grown := RING_GROWN_SECONDS / RING_LIFETIME
	var curve := _curve_of(pm.scale_curve, "GroundRing scale_curve")
	if curve != null:
		_near("GroundRing scale_curve at 0 s", curve.sample(0.0), RING_SCALE_START)
		_near("GroundRing scale_curve at 0.15 s", curve.sample(0.15 / RING_LIFETIME), lerpf(RING_SCALE_START, 1.0, 0.15 / RING_GROWN_SECONDS))
		_near("GroundRing scale_curve at 0.30 s", curve.sample(grown), 1.0)
		_near("GroundRing scale_curve at 0.40 s", curve.sample(0.40 / RING_LIFETIME), 1.0)
		_near("GroundRing scale_curve at 0.45 s", curve.sample(1.0), 1.0)
	_color("GroundRing color", pm.color, RING_COLOR)
	var ramp := _ramp_of(pm.color_ramp, "GroundRing color_ramp")
	if ramp != null:
		_near("GroundRing opacity at 0 s", ramp.sample(0.0).a, RING_OPACITY_START)
		_near("GroundRing opacity at mid-life", ramp.sample(0.5).a, RING_OPACITY_START * 0.5)
		_near("GroundRing opacity at 0.45 s", ramp.sample(1.0).a, 0.0)
		_color("GroundRing ramp rgb stays white", Color(ramp.sample(0.5).r, ramp.sample(0.5).g, ramp.sample(0.5).b), Color.WHITE)
	var mesh := _quad_of(ring, "GroundRing")
	if mesh != null:
		_vec2("GroundRing QuadMesh size", mesh.size, RING_QUAD)
		_check("GroundRing QuadMesh orientation is FACE_Y (got %d)" % mesh.orientation, mesh.orientation == PlaneMesh.FACE_Y)
		var mat := _material_of(mesh, "GroundRing")
		if mat != null:
			_check_draw_switches(mat, "GroundRing", BaseMaterial3D.BILLBOARD_DISABLED)
			_check_ring_texture(mat.albedo_texture)


func _check_emitter_node(p: GPUParticles3D, amount: int, lifetime: float, height: float, aabb: AABB) -> void:
	_check("%s amount = %d (got %d)" % [p.name, amount, p.amount], p.amount == amount)
	_near("%s lifetime" % p.name, p.lifetime, lifetime)
	_check("%s one_shot is on" % p.name, p.one_shot)
	_near("%s explosiveness" % p.name, p.explosiveness, 1.0)
	_check("%s emitting is off in the scene file" % p.name, not p.emitting)
	_near("%s preprocess" % p.name, p.preprocess, 0.0)
	_check("%s local_coords is off" % p.name, not p.local_coords)
	_check("%s visibility_aabb = %s (got %s)" % [p.name, aabb, p.visibility_aabb], p.visibility_aabb.is_equal_approx(aabb))
	_check("%s cast_shadow is OFF" % p.name, p.cast_shadow == GeometryInstance3D.SHADOW_CASTING_SETTING_OFF)
	_vec("%s position" % p.name, p.position, Vector3(0, height, 0))


func _check_draw_switches(mat: StandardMaterial3D, label: String, billboard: int) -> void:
	_check("%s shading_mode is UNSHADED" % label, mat.shading_mode == BaseMaterial3D.SHADING_MODE_UNSHADED)
	_check("%s transparency is ALPHA" % label, mat.transparency == BaseMaterial3D.TRANSPARENCY_ALPHA)
	_check("%s vertex_color_use_as_albedo is on" % label, mat.vertex_color_use_as_albedo)
	_check("%s blend_mode is MIX" % label, mat.blend_mode == BaseMaterial3D.BLEND_MODE_MIX)
	_check("%s billboard_mode = %d (got %d)" % [label, billboard, mat.billboard_mode], mat.billboard_mode == billboard)


func _check_round_texture(tex: Texture2D, label: String) -> void:
	var g := tex as GradientTexture2D
	if not _check("%s albedo_texture is a GradientTexture2D" % label, g != null and g.gradient != null):
		return
	_check("%s texture fill is RADIAL" % label, g.fill == GradientTexture2D.FILL_RADIAL)
	_vec2("%s texture fill_from (centre)" % label, g.fill_from, Vector2(0.5, 0.5))
	_near("%s texture radius reaches the edge" % label, g.fill_from.distance_to(g.fill_to), 0.5)
	_near("%s texture alpha at centre" % label, g.gradient.sample(0.0).a, 1.0)
	_near("%s texture alpha at edge" % label, g.gradient.sample(1.0).a, 0.0)
	_check("%s texture edge is soft (alpha at half radius is between)" % label, g.gradient.sample(0.5).a > 0.1 and g.gradient.sample(0.5).a < 0.9)


func _check_ring_texture(tex: Texture2D) -> void:
	var g := tex as GradientTexture2D
	if not _check("GroundRing albedo_texture is a GradientTexture2D", g != null and g.gradient != null):
		return
	_check("GroundRing texture fill is RADIAL", g.fill == GradientTexture2D.FILL_RADIAL)
	_vec2("GroundRing texture fill_from (centre)", g.fill_from, Vector2(0.5, 0.5))
	_near("GroundRing texture radius reaches the edge", g.fill_from.distance_to(g.fill_to), 0.5)
	var peak := 0.0
	var peak_at := 0.0
	var wide := 0
	for i in 101:
		var a := g.gradient.sample(i / 100.0).a
		if a > peak:
			peak = a
			peak_at = i / 100.0
		if a > 0.5:
			wide += 1
	_near("GroundRing texture alpha at centre", g.gradient.sample(0.0).a, 0.0)
	_check("GroundRing texture band is bright (peak %.2f)" % peak, peak > 0.9)
	_check("GroundRing texture band is near the outer edge (at %.2f of the radius)" % peak_at, peak_at >= 0.8 and peak_at < 1.0)
	_check("GroundRing texture band is thin (%d%% of the radius above half alpha)" % wide, wide > 0 and wide <= 20)
	_near("GroundRing texture alpha at edge", g.gradient.sample(1.0).a, 0.0)


func _check_derived(dust: GPUParticles3D, ring: GPUParticles3D) -> void:
	var pm := dust.process_material as ParticleProcessMaterial
	var mesh := dust.draw_pass_1 as QuadMesh
	if pm == null or mesh == null or not (pm.scale_curve is CurveTexture):
		return
	var curve := (pm.scale_curve as CurveTexture).curve
	if curve == null:
		return
	var curve_max := 0.0
	for i in 101:
		curve_max = maxf(curve_max, curve.sample(i / 100.0))
	var top := dust.position.y + mesh.size.y * pm.scale_max * curve_max * 0.5
	_check("Dust top including quads = %.3f m <= %.2f m (mid-calf)" % [top, FLOOR_LIMIT], top <= FLOOR_LIMIT + EPS)
	var ring_pm := ring.process_material as ParticleProcessMaterial
	var ring_mesh := ring.draw_pass_1 as QuadMesh
	if ring_pm == null or ring_mesh == null or not (ring_pm.scale_curve is CurveTexture):
		return
	var final_diameter := ring_mesh.size.x * (ring_pm.scale_curve as CurveTexture).curve.sample(1.0)
	_near("GroundRing final outer diameter (m)", final_diameter, RING_FINAL_DIAMETER)


func _report_initial_velocity() -> void:
	var names := {}
	for prop in ClassDB.class_get_property_list("ParticleProcessMaterial"):
		names[prop.name] = prop
	if names.has("initial_velocity"):
		var p: Dictionary = names["initial_velocity"]
		print("  INFO  ParticleProcessMaterial lists initial_velocity: type %d, usage %d (the scene sets initial_velocity_min / max only)" % [p.type, p.usage])
	else:
		print("  INFO  ParticleProcessMaterial does not list initial_velocity in this engine")


func _curve_of(tex: Texture2D, label: String) -> Curve:
	var ct := tex as CurveTexture
	_check("%s is a CurveTexture with a Curve" % label, ct != null and ct.curve != null)
	return ct.curve if ct != null else null


func _ramp_of(tex: Texture2D, label: String) -> Gradient:
	var gt := tex as GradientTexture1D
	_check("%s is a GradientTexture1D with a Gradient" % label, gt != null and gt.gradient != null)
	return gt.gradient if gt != null else null


func _quad_of(p: GPUParticles3D, label: String) -> QuadMesh:
	var q := p.draw_pass_1 as QuadMesh
	_check("%s draw_pass_1 is a QuadMesh (got %s)" % [label, p.draw_pass_1.get_class() if p.draw_pass_1 else "null"], q != null)
	return q


func _material_of(mesh: QuadMesh, label: String) -> StandardMaterial3D:
	var m := mesh.material as StandardMaterial3D
	_check("%s draw material is a StandardMaterial3D" % label, m != null)
	return m


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
