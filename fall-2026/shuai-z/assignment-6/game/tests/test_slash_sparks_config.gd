extends SceneTree
## Configuration checks for Effect A, the sword-swing sparks (CHANGE-BRIEF.md,
## section 2, "The settings"). Run from the assignment folder:
##   scripts/run-test.sh test_slash_sparks_config.gd 60
## Prints one line per check and exits with code 1 if any check fails.
##
## It loads game/effects/slash_sparks.tscn and reads every setting the brief's
## table names back from the loaded nodes and resources, with the brief's
## values as the expected values. It reads the Godot 4 _min/_max values, never
## whether a name exists: a Godot 3 line such as `initial_velocity = 260.0`
## loads without a message and leaves initial_velocity_min at 0, which fails
## here (CHANGE-BRIEF.md, Revision 2). Godot 4.7.2 maps the Godot 3 class names
## and flag_disable_z silently, so no loaded value can show them; the scene's
## text is scanned for them instead.
## Headless, nothing is drawn: these are the settings, not the look.

const SCENE_PATH := "res://effects/slash_sparks.tscn"
const EPS := 1e-4
const COLOR_EPS := 1e-3
const VISIBILITY := Rect2(-50, -100, 270, 230)
const TEXTURE_OFFSETS := [0.0, 0.55, 0.70, 0.85]
const TEXTURE_COLORS := [Color("#FFFFF0", 1.0), Color("#FFE58A", 1.0), Color("#290F0D", 1.0), Color("#290F0D", 0.0)]

## Each emitter's expected settings, from the brief's table.
const EXPECTED := {
	"Flash": {
		"amount": 1, "one_shot": true, "explosiveness": 1.0, "lifetime": 0.12,
		"texture_size": Vector2i(64, 64),
		"emission_shape": ParticleProcessMaterial.EMISSION_SHAPE_POINT,
		"direction": Vector3(1, 0, 0), "spread": 0.0,
		"initial_velocity": [0.0, 0.0], "gravity": Vector3(0, 0, 0), "damping": [0.0, 0.0],
		"align_y": false, "lifetime_randomness": 0.0, "scale": [0.9, 1.1],
		"scale_curve": [Vector2(0, 1.0), Vector2(1, 1.3)],
		"ramp_offsets": [0.0, 1.0], "ramp_colors": [Color(1, 1, 1, 1), Color(1, 1, 1, 0)],
		"hue_variation": [0.0, 0.0],
	},
	"Sparks": {
		"amount": 28, "one_shot": true, "explosiveness": 1.0, "lifetime": 0.45,
		"texture_size": Vector2i(12, 40),
		"emission_shape": ParticleProcessMaterial.EMISSION_SHAPE_POINT,
		"direction": Vector3(0.944, -0.330, 0), "spread": 30.0,
		"initial_velocity": [260.0, 420.0], "gravity": Vector3(0, 700, 0), "damping": [0.0, 0.0],
		"align_y": true, "lifetime_randomness": 0.4, "scale": [0.7, 1.1],
		"scale_curve": [Vector2(0, 1.0), Vector2(1, 0.3)],
		"ramp_offsets": [0.0, 0.25, 0.7, 1.0],
		"ramp_colors": [Color(1, 1, 1, 1), Color(1, 0.9, 0.45, 1), Color(1, 0.55, 0.2, 1), Color(0.9, 0.35, 0.15, 0)],
		"hue_variation": [-0.03, 0.03],
	},
}

var _failures := 0


func _initialize() -> void:
	var scene := load(SCENE_PATH) as PackedScene
	_check("the scene loads as a PackedScene", scene != null, SCENE_PATH)
	if scene == null:
		_finish()
		return
	_check_source_names()
	var root := scene.instantiate()
	_check_root(root)
	for emitter_name: String in EXPECTED:
		var emitter := root.get_node_or_null(emitter_name) as GPUParticles2D
		_check("%s is a GPUParticles2D child of the root" % emitter_name, emitter != null,
			"" if emitter else "found %s" % root.get_node_or_null(emitter_name))
		if emitter:
			_check_emitter(emitter, EXPECTED[emitter_name])
	root.free()
	_finish()


func _finish() -> void:
	print("%s  test_slash_sparks_config: %d failure(s)" % ["PASS" if _failures == 0 else "FAIL", _failures])
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


func _check_root(root: Node) -> void:
	_check("root is a Node2D named SlashSparks", root is Node2D and root.name == &"SlashSparks",
		"%s %s" % [root.get_class(), root.name])
	if root is Node2D:
		_check("root z_index is 1", (root as Node2D).z_index == 1, "%d" % (root as Node2D).z_index)
	var names := root.get_children().map(func(n: Node) -> String: return n.name)
	_check("root's children are Flash then Sparks, and nothing else", names == ["Flash", "Sparks"], "%s" % [names])


func _check_emitter(e: GPUParticles2D, x: Dictionary) -> void:
	var n := String(e.name)
	# Emission
	_check("%s amount is %d" % [n, x.amount], e.amount == x.amount, "%d" % e.amount)
	_check("%s one_shot is %s" % [n, x.one_shot], e.one_shot == x.one_shot, "%s" % e.one_shot)
	_check_float("%s explosiveness" % n, e.explosiveness, x.explosiveness)
	_check_float("%s lifetime" % n, e.lifetime, x.lifetime)
	_check("%s emitting is false as saved" % n, e.emitting == false, "%s" % e.emitting)
	_check_float("%s preprocess" % n, e.preprocess, 0.0)
	_check("%s fixed_fps is 30" % n, e.fixed_fps == 30, "%d" % e.fixed_fps)
	_check("%s trail_enabled is false (Compatibility draws no trails)" % n, e.trail_enabled == false, "%s" % e.trail_enabled)
	_check("%s use_fixed_seed is off, so repeats vary in play" % n, e.use_fixed_seed == false, "%s" % e.use_fixed_seed)
	# Space and culling
	_check("%s local_coords is false" % n, e.local_coords == false, "%s" % e.local_coords)
	_check("%s visibility_rect is %s" % [n, VISIBILITY], e.visibility_rect.is_equal_approx(VISIBILITY), "%s" % e.visibility_rect)
	# Draw
	_check("%s has no draw material (default mix blending)" % n, e.material == null, "%s" % e.material)
	_check_texture(e, x)
	# Process
	var m := e.process_material as ParticleProcessMaterial
	_check("%s process_material is a ParticleProcessMaterial" % n, m != null, "%s" % e.process_material)
	if m == null:
		return
	_check("%s emission_shape is point (0)" % n, m.emission_shape == x.emission_shape, "%d" % m.emission_shape)
	_check("%s particle_flag_disable_z is true" % n, m.particle_flag_disable_z == true, "%s" % m.particle_flag_disable_z)
	_check("%s particle_flag_align_y is %s" % [n, x.align_y], m.particle_flag_align_y == x.align_y, "%s" % m.particle_flag_align_y)
	_check("%s direction is %s" % [n, x.direction], m.direction.distance_to(x.direction) < 1e-3, "%s" % m.direction)
	_check_float("%s spread" % n, m.spread, x.spread)
	_check_float("%s initial_velocity_min" % n, m.initial_velocity_min, x.initial_velocity[0])
	_check_float("%s initial_velocity_max" % n, m.initial_velocity_max, x.initial_velocity[1])
	_check("%s gravity is %s" % [n, x.gravity], m.gravity.is_equal_approx(x.gravity), "%s" % m.gravity)
	_check_float("%s damping_min" % n, m.damping_min, x.damping[0])
	_check_float("%s damping_max" % n, m.damping_max, x.damping[1])
	_check_float("%s lifetime_randomness" % n, m.lifetime_randomness, x.lifetime_randomness)
	_check_float("%s scale_min" % n, m.scale_min, x.scale[0])
	_check_float("%s scale_max" % n, m.scale_max, x.scale[1])
	_check_float("%s hue_variation_min" % n, m.hue_variation_min, x.hue_variation[0])
	_check_float("%s hue_variation_max" % n, m.hue_variation_max, x.hue_variation[1])
	_check_scale_curve(n, m, x.scale_curve)
	_check_color_ramp(n, m, x.ramp_offsets, x.ramp_colors)


func _check_texture(e: GPUParticles2D, x: Dictionary) -> void:
	var n := String(e.name)
	var t := e.texture as GradientTexture2D
	_check("%s texture is a GradientTexture2D" % n, t != null, "%s" % e.texture)
	if t == null:
		return
	var size := Vector2i(t.width, t.height)
	_check("%s texture is %d x %d" % [n, x.texture_size.x, x.texture_size.y], size == x.texture_size, "%s" % size)
	_check("%s texture fill is radial" % n, t.fill == GradientTexture2D.FILL_RADIAL, "%d" % t.fill)
	_check("%s texture fill_from is (0.5, 0.5)" % n, t.fill_from.is_equal_approx(Vector2(0.5, 0.5)), "%s" % t.fill_from)
	_check("%s texture fill_to is (1.0, 0.5)" % n, t.fill_to.is_equal_approx(Vector2(1.0, 0.5)), "%s" % t.fill_to)
	_check_gradient("%s texture gradient" % n, t.gradient, TEXTURE_OFFSETS, TEXTURE_COLORS)


func _check_scale_curve(n: String, m: ParticleProcessMaterial, points: Array) -> void:
	var t := m.scale_curve as CurveTexture
	_check("%s scale_curve is a CurveTexture" % n, t != null, "%s" % m.scale_curve)
	if t == null or t.curve == null:
		_check("%s scale_curve has a curve" % n, false)
		return
	var c := t.curve
	_check("%s scale_curve has %d points" % [n, points.size()], c.point_count == points.size(), "%d" % c.point_count)
	for p: Vector2 in points:
		var got := c.sample(p.x)
		_check("%s scale_curve is %.2f at %.1f" % [n, p.y, p.x], absf(got - p.y) < EPS, "%.4f" % got)
	# The brief gives only the two ends; between them it runs straight, not eased.
	var mid: float = (points[0].y + points[1].y) / 2.0
	_check("%s scale_curve is linear (%.2f at 0.5)" % [n, mid], absf(c.sample(0.5) - mid) < 1e-3, "%.4f" % c.sample(0.5))


func _check_color_ramp(n: String, m: ParticleProcessMaterial, offsets: Array, colors: Array) -> void:
	var t := m.color_ramp as GradientTexture1D
	_check("%s color_ramp is a GradientTexture1D" % n, t != null, "%s" % m.color_ramp)
	if t:
		_check_gradient("%s color_ramp" % n, t.gradient, offsets, colors)


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
