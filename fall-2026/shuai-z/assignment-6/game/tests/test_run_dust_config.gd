extends SceneTree
## Configuration checks for Effect B, the running dust trail (CHANGE-BRIEF.md,
## section 3, "The settings"). Run from the assignment folder:
##   scripts/run-test.sh test_run_dust_config.gd 60
## Prints one line per check and exits with code 1 if any check fails.
##
## It loads game/effects/run_dust.tscn and reads every setting the brief's
## table names back from the loaded node and resources, with the brief's
## values as the expected values. The process feature Effect B adds over
## Effect A is damping (damping_min / damping_max, 120 / 180 px/s²), with a box
## emission shape where Effect A has a point; both are read here. It reads the
## Godot 4 _min/_max values, never whether a name exists: a Godot 3 line such
## as `damping = 120.0` loads without a message and leaves damping_min at 0,
## which fails here (CHANGE-BRIEF.md, Revision 2). Godot 4.7.2 maps the Godot 3
## class names and flag_disable_z silently, so no loaded value can show them;
## the scene's text is scanned for them instead.
## Headless, nothing is drawn: these are the settings, not the look.

const SCENE_PATH := "res://effects/run_dust.tscn"
const EPS := 1e-4
const COLOR_EPS := 1e-3
const VISIBILITY := Rect2(-320, -80, 640, 110)
const TEXTURE_SIZE := Vector2i(32, 32)
const TEXTURE_OFFSETS := [0.0, 0.6, 1.0]
const TEXTURE_COLORS := [Color(1, 1, 1, 1), Color(1, 1, 1, 0.6), Color(1, 1, 1, 0)]
const RAMP_OFFSETS := [0.0, 0.15, 0.6, 1.0]
const RAMP_COLORS := [Color("#5C4A35", 0.0), Color("#5C4A35", 1.0), Color("#6E5A43", 0.8), Color("#9C8463", 0.0)]
## The brief's points, then the midpoints of its two straight segments.
const SCALE_POINTS := [Vector2(0, 0.5), Vector2(0.4, 1.0), Vector2(1, 1.15)]
const SCALE_MIDPOINTS := [Vector2(0.2, 0.75), Vector2(0.7, 1.075)]

var _failures := 0


func _initialize() -> void:
	var scene := load(SCENE_PATH) as PackedScene
	_check("the scene loads as a PackedScene", scene != null, SCENE_PATH)
	if scene == null:
		_finish()
		return
	_check_source_names()
	var root := scene.instantiate()
	var e := root as GPUParticles2D
	_check("root is a GPUParticles2D named RunDust", e != null and root.name == &"RunDust",
		"%s %s" % [root.get_class(), root.name])
	_check("root has no children: one emitter, no layers", root.get_child_count() == 0, "%d" % root.get_child_count())
	if e:
		_check_emitter(e)
	root.free()
	_finish()


func _finish() -> void:
	print("%s  test_run_dust_config: %d failure(s)" % ["PASS" if _failures == 0 else "FAIL", _failures])
	quit(1 if _failures > 0 else 0)


## Godot 3 names the engine maps or drops without a message (CLAUDE.md,
## "Godot 4 names"): no loaded value can show them, so the file is read.
func _check_source_names() -> void:
	var text := FileAccess.get_file_as_string(SCENE_PATH)
	var g3_class := RegEx.create_from_string("type=\"(Particles2D|ParticlesMaterial)\"")
	var found := g3_class.search_all(text).map(func(m: RegExMatch) -> String: return m.get_string(1))
	_check("the scene file names no Godot 3 class", found.is_empty(), "found %s" % [found] if found else "")
	var g3_prop := RegEx.create_from_string("^(flag_disable_z|flag_align_y|flag_rotate_y|initial_velocity|scale|damping|hue_variation|angular_velocity|linear_accel|radial_accel|tangential_accel|angle) =")
	var in_material := false
	var bad: Array[String] = []
	for line in text.split("\n"):
		if line.begins_with("["):
			in_material = line.contains("type=\"ParticleProcessMaterial\"") or line.contains("type=\"ParticlesMaterial\"")
		elif in_material and g3_prop.search(line):
			bad.append(line.strip_edges())
	_check("no process material in the file has a Godot 3 property line", bad.is_empty(), "found %s" % [bad] if bad else "")


func _check_emitter(e: GPUParticles2D) -> void:
	_check("RunDust z_index is 0", e.z_index == 0, "%d" % e.z_index)
	# Emission
	_check("RunDust amount is 40", e.amount == 40, "%d" % e.amount)
	_check("RunDust one_shot is false", e.one_shot == false, "%s" % e.one_shot)
	_check_float("RunDust explosiveness", e.explosiveness, 0.0)
	_check_float("RunDust randomness", e.randomness, 0.2)
	_check_float("RunDust lifetime", e.lifetime, 0.5)
	_check("RunDust emitting is false as saved", e.emitting == false, "%s" % e.emitting)
	_check_float("RunDust preprocess", e.preprocess, 0.0)
	_check("RunDust fixed_fps is 30", e.fixed_fps == 30, "%d" % e.fixed_fps)
	_check("RunDust trail_enabled is false (Compatibility draws no trails)", e.trail_enabled == false, "%s" % e.trail_enabled)
	_check("RunDust use_fixed_seed is off, so the trail varies in play", e.use_fixed_seed == false, "%s" % e.use_fixed_seed)
	# Space and culling
	_check("RunDust local_coords is false (the trail)", e.local_coords == false, "%s" % e.local_coords)
	_check("RunDust visibility_rect is %s" % VISIBILITY, e.visibility_rect.is_equal_approx(VISIBILITY), "%s" % e.visibility_rect)
	# Draw
	_check("RunDust has no draw material (default mix blending)", e.material == null, "%s" % e.material)
	_check_texture(e)
	# Process
	var m := e.process_material as ParticleProcessMaterial
	_check("RunDust process_material is a ParticleProcessMaterial", m != null, "%s" % e.process_material)
	if m == null:
		return
	_check("RunDust emission_shape is box (3)", m.emission_shape == ParticleProcessMaterial.EMISSION_SHAPE_BOX, "%d" % m.emission_shape)
	_check("RunDust emission_box_extents is (14, 3, 0)", m.emission_box_extents.is_equal_approx(Vector3(14, 3, 0)), "%s" % m.emission_box_extents)
	_check("RunDust particle_flag_disable_z is true", m.particle_flag_disable_z == true, "%s" % m.particle_flag_disable_z)
	_check("RunDust particle_flag_align_y is false", m.particle_flag_align_y == false, "%s" % m.particle_flag_align_y)
	_check("RunDust direction is (0, -1, 0)", m.direction.distance_to(Vector3(0, -1, 0)) < 1e-3, "%s" % m.direction)
	_check_float("RunDust spread", m.spread, 50.0)
	_check_float("RunDust initial_velocity_min", m.initial_velocity_min, 80.0)
	_check_float("RunDust initial_velocity_max", m.initial_velocity_max, 160.0)
	_check("RunDust gravity is (0, 0, 0)", m.gravity.is_equal_approx(Vector3.ZERO), "%s" % m.gravity)
	# Damping: Effect B's process feature, which Effect A does not use.
	_check_float("RunDust damping_min", m.damping_min, 120.0)
	_check_float("RunDust damping_max", m.damping_max, 180.0)
	_check("RunDust damping has no curve, so it acts at full strength all life", m.damping_curve == null, "%s" % m.damping_curve)
	_check_float("RunDust lifetime_randomness", m.lifetime_randomness, 0.3)
	_check_float("RunDust scale_min", m.scale_min, 0.7)
	_check_float("RunDust scale_max", m.scale_max, 1.0)
	_check_float("RunDust hue_variation_min", m.hue_variation_min, -0.02)
	_check_float("RunDust hue_variation_max", m.hue_variation_max, 0.02)
	_check_scale_curve(m)
	var ramp := m.color_ramp as GradientTexture1D
	_check("RunDust color_ramp is a GradientTexture1D", ramp != null, "%s" % m.color_ramp)
	if ramp:
		_check_gradient("RunDust color_ramp", ramp.gradient, RAMP_OFFSETS, RAMP_COLORS)


func _check_texture(e: GPUParticles2D) -> void:
	var t := e.texture as GradientTexture2D
	_check("RunDust texture is a GradientTexture2D", t != null, "%s" % e.texture)
	if t == null:
		return
	var size := Vector2i(t.width, t.height)
	_check("RunDust texture is 32 x 32", size == TEXTURE_SIZE, "%s" % size)
	_check("RunDust texture fill is radial", t.fill == GradientTexture2D.FILL_RADIAL, "%d" % t.fill)
	_check("RunDust texture fill_from is (0.5, 0.5)", t.fill_from.is_equal_approx(Vector2(0.5, 0.5)), "%s" % t.fill_from)
	_check("RunDust texture fill_to is (1.0, 0.5)", t.fill_to.is_equal_approx(Vector2(1.0, 0.5)), "%s" % t.fill_to)
	_check_gradient("RunDust texture gradient", t.gradient, TEXTURE_OFFSETS, TEXTURE_COLORS)


func _check_scale_curve(m: ParticleProcessMaterial) -> void:
	var t := m.scale_curve as CurveTexture
	_check("RunDust scale_curve is a CurveTexture", t != null, "%s" % m.scale_curve)
	if t == null or t.curve == null:
		_check("RunDust scale_curve has a curve", false)
		return
	var c := t.curve
	_check("RunDust scale_curve has %d points" % SCALE_POINTS.size(), c.point_count == SCALE_POINTS.size(), "%d" % c.point_count)
	for p: Vector2 in SCALE_POINTS:
		var got := c.sample(p.x)
		_check("RunDust scale_curve is %.2f at %.1f" % [p.y, p.x], absf(got - p.y) < EPS, "%.4f" % got)
	# The brief gives only the points; between them it runs straight, not eased.
	for p: Vector2 in SCALE_MIDPOINTS:
		var got := c.sample(p.x)
		_check("RunDust scale_curve is linear (%.3f at %.1f)" % [p.y, p.x], absf(got - p.y) < 1e-3, "%.4f" % got)


func _check_gradient(what: String, g: Gradient, offsets: Array, colors: Array) -> void:
	_check("%s exists" % what, g != null)
	if g == null:
		return
	_check("%s has %d stops" % [what, offsets.size()], g.get_point_count() == offsets.size(), "%d" % g.get_point_count())
	if g.get_point_count() != offsets.size():
		return
	for i in offsets.size():
		var off := g.get_offset(i)
		var col := g.get_color(i)
		var want: Color = colors[i]
		var col_ok := absf(col.r - want.r) < COLOR_EPS and absf(col.g - want.g) < COLOR_EPS \
			and absf(col.b - want.b) < COLOR_EPS and absf(col.a - want.a) < COLOR_EPS
		_check("%s stop %d is %s at %.2f" % [what, i, _rgba(want), offsets[i]],
			absf(off - offsets[i]) < EPS and col_ok, "%s at %.4f" % [_rgba(col), off])


func _rgba(c: Color) -> String:
	return "(%.3f, %.3f, %.3f, %.2f)" % [c.r, c.g, c.b, c.a]


func _check_float(what: String, got: float, want: float) -> void:
	_check("%s is %s" % [what, want], absf(got - want) < EPS, "%s" % got)


func _check(what: String, ok: bool, detail: String = "") -> void:
	print("%s  %s%s" % ["PASS" if ok else "FAIL", what, "" if detail.is_empty() else "  (%s)" % detail])
	if not ok:
		_failures += 1
