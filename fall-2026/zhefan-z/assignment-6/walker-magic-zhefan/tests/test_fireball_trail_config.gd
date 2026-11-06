extends SceneTree
## Assignment 6 headless configuration check for Effect B, the fireball trail (CHANGE-BRIEF "Effect B" settings and the
## revisions of 2026-11-05): loads effects/fireball_trail.tscn and reads every setting the brief names back from the
## loaded node and resources, including the two features Effect A does not use, turbulence and the sphere emission
## shape. Expected values are copied by hand from the brief; the script does not read the Markdown.
## From fall-2026/zhefan-z/assignment-6/:
##   ./scripts/run-test.sh test_fireball_trail_config.gd 60
## Prints one JSON line per check and "WALKER TESTS: N checks / F failures"; exit code 1 on any failure.
## Several brief values equal the engine defaults (turbulence_noise_strength 1.0, turbulence_influence_min 0.1,
## explosiveness 0, ...), so reading them back cannot tell "set" from "missing"; those are also required in the file text.

const SCENE := "res://effects/fireball_trail.tscn"
const IMPACT_SCENE := "res://effects/fireball_impact.tscn"
const SPARK_TEX := "res://assets/textures/fx/spark.png"
const EPS := 1e-4

const NODE := {"amount": 32, "one_shot": false, "explosiveness": 0.0, "lifetime": 0.3, "local_coords": false,
	"visibility_rect": Rect2(-128, -48, 256, 96), "preprocess": 0.0}
const PROCESS := {"emission_shape": ParticleProcessMaterial.EMISSION_SHAPE_SPHERE, "emission_sphere_radius": 3.0,
	"direction": Vector3(-1, 0, 0), "spread": 30.0, "initial_velocity_min": 10.0, "initial_velocity_max": 20.0,
	"gravity": Vector3(0, -30, 0), "turbulence_enabled": true, "turbulence_noise_strength": 1.0,
	"turbulence_noise_scale": 2.0, "turbulence_influence_min": 0.1, "turbulence_influence_max": 0.2,
	"scale_min": 1.0, "scale_max": 1.5}
const SCALE_CURVE := [[0.0, 1.0], [1.0, 0.0]]
## Same as Sparks (brief): stops before the last; the last is the same colour at alpha 0.
const RAMP := [Color(1, 0.95, 0.7, 1), Color(1, 0.55, 0.15, 1), Color(0.6, 0.1, 0.05, 1)]

var results: Array[Dictionary] = []
var failures := 0


func _initialize() -> void:
	call_deferred("run")


func check(id: String, passed: bool, observed: Dictionary) -> void:
	results.append({"id": id, "status": "PASS" if passed else "FAIL", "observed": observed})
	if not passed:
		failures += 1
	print(JSON.stringify(results.back()))


func same(a: Variant, b: Variant) -> bool:
	if typeof(a) != typeof(b):
		return false
	match typeof(a):
		TYPE_FLOAT:
			return absf(a - b) < EPS
		TYPE_VECTOR3, TYPE_RECT2, TYPE_COLOR:
			return a.is_equal_approx(b)
	return a == b


func run() -> void:
	var trail: Node = (load(SCENE) as PackedScene).instantiate()
	check("root-gpuparticles2d-fireballtrail-one-emitter", trail is GPUParticles2D and trail.name == "FireballTrail"
		and trail.get_child_count() == 0 and trail.get_script() == null,
		{"root": "%s:%s" % [trail.name, trail.get_class()], "children": trail.get_child_count(), "script": trail.get_script() != null})
	var p := trail as GPUParticles2D
	for prop: String in NODE:
		check("trail-%s" % prop, same(p.get(prop), NODE[prop]), {"value": p.get(prop), "expected": NODE[prop]})
	check("trail-emitting-on-spawn-no-fixed-seed", p.emitting and not p.use_fixed_seed,
		{"emitting": p.emitting, "use_fixed_seed": p.use_fixed_seed})

	var pm := p.process_material as ParticleProcessMaterial
	check("trail-process-material-class", pm != null, {"class": p.process_material.get_class() if p.process_material else "null"})
	if pm:
		for prop: String in PROCESS:
			check("trail-process-%s" % prop, same(pm.get(prop), PROCESS[prop]), {"value": pm.get(prop), "expected": PROCESS[prop]})
		check("trail-process-particle_flag_disable_z", pm.particle_flag_disable_z, {"value": pm.particle_flag_disable_z})

		var ct := pm.scale_curve as CurveTexture
		var samples := []
		var curve_ok := ct != null and ct.curve != null
		if curve_ok:
			for s: Array in SCALE_CURVE:
				var v := ct.curve.sample(s[0])
				samples.append([s[0], snappedf(v, 0.0001)])
				curve_ok = curve_ok and absf(v - s[1]) < EPS
		check("trail-scale-curve", curve_ok, {"class": pm.scale_curve.get_class() if pm.scale_curve else "null",
			"samples": samples, "expected": SCALE_CURVE})

		var ramp := pm.color_ramp as GradientTexture1D
		var colors: PackedColorArray = ramp.gradient.colors if ramp and ramp.gradient else PackedColorArray()
		var stops_ok: bool = colors.size() == RAMP.size() + 1
		for i in RAMP.size() if stops_ok else 0:
			stops_ok = stops_ok and colors[i].is_equal_approx(RAMP[i])
		if stops_ok:
			stops_ok = is_zero_approx(colors[colors.size() - 1].a) and Color(colors[colors.size() - 1], 1).is_equal_approx(Color(RAMP.back(), 1))
		check("trail-colour-ramp", ramp != null and stops_ok, {"colors": colors,
			"offsets": ramp.gradient.offsets if ramp and ramp.gradient else [], "expected_then_alpha_0": RAMP})

		# "Same as Sparks": colours and offsets equal to the Sparks ramp loaded from the impact scene.
		var impact: Node = (load(IMPACT_SCENE) as PackedScene).instantiate()
		var sg: Gradient = (impact.get_node("Sparks").process_material as ParticleProcessMaterial).color_ramp.gradient
		var as_sparks: bool = ramp != null and ramp.gradient.colors.size() == sg.colors.size()
		for i in sg.colors.size() if as_sparks else 0:
			as_sparks = as_sparks and ramp.gradient.colors[i].is_equal_approx(sg.colors[i]) \
				and absf(ramp.gradient.offsets[i] - sg.offsets[i]) < EPS
		check("trail-colour-ramp-same-as-sparks", as_sparks, {"trail_offsets": ramp.gradient.offsets if ramp else [],
			"sparks_offsets": sg.offsets})
		impact.free()

	var tex := p.texture
	check("trail-texture", tex != null and tex.resource_path == SPARK_TEX and Vector2i(tex.get_width(), tex.get_height()) == Vector2i(4, 4),
		{"path": tex.resource_path if tex else "", "size": Vector2i(tex.get_width(), tex.get_height()) if tex else Vector2i.ZERO})
	var mat := p.material as CanvasItemMaterial
	check("trail-draw-material-blend-add", mat != null and mat.blend_mode == CanvasItemMaterial.BLEND_MODE_ADD,
		{"class": p.material.get_class() if p.material else "null", "blend_mode": mat.blend_mode if mat else -1})

	# Brief values that equal the engine default must still be written in the scene file.
	var src := FileAccess.get_file_as_string(SCENE)
	var defaults_node := GPUParticles2D.new()
	var defaults_pm := ParticleProcessMaterial.new()
	var at_default := []
	for prop: String in NODE:
		if same(defaults_node.get(prop), NODE[prop]):
			at_default.append(prop)
	for prop: String in PROCESS:
		if same(defaults_pm.get(prop), PROCESS[prop]):
			at_default.append(prop)
	defaults_node.free()
	var unwritten := at_default.filter(func(prop: String) -> bool:
		return not RegEx.create_from_string("(?m)^%s = " % prop).search(src))
	check("brief-values-at-engine-default-written-in-scene", unwritten.is_empty(),
		{"at_engine_default": at_default, "not_in_file": unwritten})

	# F1: no Godot 3 class names, and none of 4.7's Vector2 range aliases that a Godot 3 float would land on.
	var g3 := RegEx.create_from_string("(?m)^(initial_velocity|scale|damping|hue_variation|flag_disable_z) =|\"(ParticlesMaterial|Particles2D|GradientTexture)\"")
	var hits := g3.search_all(src).map(func(m: RegExMatch) -> String: return m.get_string())
	check("no-godot3-names-in-scene", hits.is_empty(), {"hits": hits})
	trail.free()

	print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
	quit(1 if failures else 0)
