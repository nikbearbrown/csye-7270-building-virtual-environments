extends SceneTree
## Assignment 6 headless configuration check for Effect A, the fireball impact (CHANGE-BRIEF "Effect A" settings and
## revision 2026-11-05): loads effects/fireball_impact.tscn and reads every Sparks and Smoke setting the brief names
## back from the loaded nodes and resources. Expected values are copied by hand from the brief; the script does not
## read the Markdown. Also the root's structure, the two textures and their import settings, and Godot 3 names (F1).
## From fall-2026/zhefan-z/assignment-6/:
##   ./scripts/run-test.sh test_fireball_impact_config.gd 60
## Prints one JSON line per check and "WALKER TESTS: N checks / F failures"; exit code 1 on any failure.
## Lines with "observation" instead of "status" are printed, not asserted: what a headless run shows of the effect
## once it is in the tree (renderer, node state over time, particle bounds, draw calls, CPU time).

const SCENE := "res://effects/fireball_impact.tscn"
const SPARK_TEX := "res://assets/textures/fx/spark.png"
const SMOKE_TEX := "res://assets/textures/fx/smoke.png"
const EPS := 1e-4

## Per emitter: node properties, ParticleProcessMaterial properties, scale curve samples (life, scale), colour ramp
## stops before the last (the last is the same colour at alpha 0), texture and size, draw blend mode.
const EXPECTED := {
	"Sparks": {
		"node": {"amount": 24, "one_shot": true, "explosiveness": 1.0, "lifetime": 0.45, "local_coords": false,
			"visibility_rect": Rect2(-96, -96, 192, 192), "preprocess": 0.0},
		"process": {"emission_shape": ParticleProcessMaterial.EMISSION_SHAPE_POINT, "direction": Vector3(1, 0, 0),
			"spread": 180.0, "initial_velocity_min": 90.0, "initial_velocity_max": 160.0, "gravity": Vector3(0, 300, 0),
			"damping_min": 40.0, "damping_max": 60.0, "scale_min": 1.0, "scale_max": 2.0,
			"hue_variation_min": -0.03, "hue_variation_max": 0.03},
		"scale_curve": [[0.0, 1.0], [1.0, 0.0]],
		"ramp": [Color(1, 0.95, 0.7, 1), Color(1, 0.55, 0.15, 1), Color(0.6, 0.1, 0.05, 1)],
		"texture": SPARK_TEX, "size": Vector2i(4, 4), "blend": CanvasItemMaterial.BLEND_MODE_ADD,
	},
	"Smoke": {
		"node": {"amount": 8, "one_shot": true, "explosiveness": 0.9, "lifetime": 0.8, "local_coords": false,
			"visibility_rect": Rect2(-96, -96, 192, 192), "preprocess": 0.0},
		"process": {"direction": Vector3(0, -1, 0), "spread": 180.0, "initial_velocity_min": 15.0,
			"initial_velocity_max": 35.0, "gravity": Vector3(0, -20, 0), "damping_min": 10.0, "damping_max": 20.0,
			"scale_min": 1.0, "scale_max": 1.5},
		"scale_curve": [[0.0, 1.0], [1.0, 2.0]],
		"ramp": [Color(0.45, 0.42, 0.40, 0.55)],
		"texture": SMOKE_TEX, "size": Vector2i(12, 12), "blend": CanvasItemMaterial.BLEND_MODE_MIX,
	},
}

var results: Array[Dictionary] = []
var failures := 0
var _game_time := 0.0   # read by the finished-signal lambdas (lambdas copy captured locals)


func _initialize() -> void:
	call_deferred("run")


func check(id: String, passed: bool, observed: Dictionary) -> void:
	results.append({"id": id, "status": "PASS" if passed else "FAIL", "observed": observed})
	if not passed:
		failures += 1
	print(JSON.stringify(results.back()))


func observe(id: String, observed: Dictionary) -> void:
	print(JSON.stringify({"id": id, "observation": observed}))


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
	var packed: PackedScene = load(SCENE)
	var fx: Node = packed.instantiate()

	# Structure (revision 2026-11-05: the A2 burst stays outside; the root holds only Sparks and Smoke).
	var kids := fx.get_children().map(func(n: Node) -> String: return "%s:%s" % [n.name, n.get_class()])
	check("root-node2d-fireballimpact-with-sparks-and-smoke", fx.get_class() == "Node2D" and fx.name == "FireballImpact"
		and kids == ["Sparks:GPUParticles2D", "Smoke:GPUParticles2D"], {"root": "%s:%s" % [fx.name, fx.get_class()], "children": kids})
	check("root-script-frees-after-0.9s", same(fx.get_script().get_script_constant_map().get("LIFETIME"), 0.9),
		{"LIFETIME": fx.get_script().get_script_constant_map().get("LIFETIME")})

	for emitter: String in EXPECTED:
		var want: Dictionary = EXPECTED[emitter]
		var p: GPUParticles2D = fx.get_node(emitter)
		for prop: String in want.node:
			check("%s-%s" % [emitter, prop], same(p.get(prop), want.node[prop]), {"value": p.get(prop), "expected": want.node[prop]})
		check("%s-emitting-on-spawn-no-fixed-seed" % emitter, p.emitting and not p.use_fixed_seed,
			{"emitting": p.emitting, "use_fixed_seed": p.use_fixed_seed})

		var pm := p.process_material as ParticleProcessMaterial
		check("%s-process-material-class" % emitter, pm != null,
			{"class": p.process_material.get_class() if p.process_material else "null"})
		if pm == null:
			continue
		for prop: String in want.process:
			check("%s-process-%s" % [emitter, prop], same(pm.get(prop), want.process[prop]),
				{"value": pm.get(prop), "expected": want.process[prop]})
		# Not a brief value: the brief's 2D spread needs it, and a loaded material with gravity already set keeps false.
		check("%s-process-particle_flag_disable_z" % emitter, pm.particle_flag_disable_z, {"value": pm.particle_flag_disable_z})

		var ct := pm.scale_curve as CurveTexture
		var samples := []
		var curve_ok := ct != null and ct.curve != null
		if curve_ok:
			for s: Array in want.scale_curve:
				var v := ct.curve.sample(s[0])
				samples.append([s[0], snappedf(v, 0.0001)])
				curve_ok = curve_ok and absf(v - s[1]) < EPS
		check("%s-scale-curve" % emitter, curve_ok,
			{"class": pm.scale_curve.get_class() if pm.scale_curve else "null", "samples": samples, "expected": want.scale_curve,
			"curve_max_value": ct.curve.max_value if ct and ct.curve else null})

		var ramp := pm.color_ramp as GradientTexture1D
		var colors: PackedColorArray = ramp.gradient.colors if ramp and ramp.gradient else PackedColorArray()
		var stops_ok: bool = colors.size() == want.ramp.size() + 1
		for i in want.ramp.size():
			stops_ok = stops_ok and colors[i].is_equal_approx(want.ramp[i])
		if stops_ok:
			var last := colors[colors.size() - 1]
			var before: Color = want.ramp.back()
			stops_ok = is_zero_approx(last.a) and Color(last, 1).is_equal_approx(Color(before, 1))
		check("%s-colour-ramp" % emitter, ramp != null and stops_ok,
			{"class": pm.color_ramp.get_class() if pm.color_ramp else "null", "colors": colors,
			"offsets": ramp.gradient.offsets if ramp and ramp.gradient else [], "expected_then_alpha_0": want.ramp})

		var tex := p.texture
		check("%s-texture" % emitter, tex != null and tex.resource_path == want.texture
			and Vector2i(tex.get_width(), tex.get_height()) == want.size,
			{"path": tex.resource_path if tex else "", "size": Vector2i(tex.get_width(), tex.get_height()) if tex else Vector2i.ZERO})
		var mat := p.material as CanvasItemMaterial
		check("%s-draw-material-blend" % emitter, mat != null and mat.blend_mode == want.blend,
			{"class": p.material.get_class() if p.material else "null", "blend_mode": mat.blend_mode if mat else -1,
			"expected": want.blend})

	# Import settings set explicitly: lossless, no mipmaps, no 3D detection.
	for path: String in [SPARK_TEX, SMOKE_TEX]:
		var cfg := ConfigFile.new()
		var err := cfg.load(path + ".import")
		var got := {"compress/mode": cfg.get_value("params", "compress/mode", null),
			"mipmaps/generate": cfg.get_value("params", "mipmaps/generate", null),
			"detect_3d/compress_to": cfg.get_value("params", "detect_3d/compress_to", null)}
		check("import-%s" % path.get_file(), err == OK and got["compress/mode"] == 0 and got["mipmaps/generate"] == false
			and got["detect_3d/compress_to"] == 0, got)

	# F1: no Godot 3 class names, and none of 4.7's Vector2 range aliases that a Godot 3 float would land on.
	var src := FileAccess.get_file_as_string(SCENE)
	var g3 := RegEx.create_from_string("(?m)^(initial_velocity|scale|damping|hue_variation|flag_disable_z) =|\"(ParticlesMaterial|Particles2D|GradientTexture)\"")
	var hits := g3.search_all(src).map(func(m: RegExMatch) -> String: return m.get_string())
	check("no-godot3-names-in-scene", hits.is_empty(), {"hits": hits})
	fx.free()

	await observe_headless()

	print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
	quit(1 if failures else 0)


## Not asserted. What a headless run shows once the effect is in the tree.
func observe_headless() -> void:
	observe("renderer", {"display": DisplayServer.get_name(), "driver": RenderingServer.get_current_rendering_driver_name(),
		"method": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name()})
	var packed: PackedScene = load(SCENE)

	# One instance; a second one hidden. Node state sampled over 1.0 s of game time.
	var fx: Node2D = packed.instantiate()
	var hidden: Node2D = packed.instantiate()
	hidden.visible = false
	fx.position = Vector2(320, 180)
	var finished_at := {}
	var t := 0.0
	_game_time = 0.0
	for emitter: String in ["Sparks", "Smoke"]:
		fx.get_node(emitter).finished.connect(func() -> void: finished_at[emitter] = snappedf(_game_time, 0.001))
	root.add_child(fx)
	root.add_child(hidden)
	var rows := []
	var marks := [0.0, 0.1, 0.3, 0.5, 0.85, 0.95]
	while t < 1.0:
		if not marks.is_empty() and t >= marks[0] - 1e-6:
			marks.pop_front()
			var row := {"t": snappedf(t, 0.001), "instances_alive": [is_instance_valid(fx), is_instance_valid(hidden)].count(true)}
			if is_instance_valid(fx):
				var sp: GPUParticles2D = fx.get_node("Sparks")
				var sm: GPUParticles2D = fx.get_node("Smoke")
				row.merge({"sparks_emitting": sp.emitting, "smoke_emitting": sm.emitting, "amount_ratio": sp.amount_ratio,
					"sparks_capture_rect": str(sp.capture_rect()), "visible_in_tree": sp.is_visible_in_tree()})
			if is_instance_valid(hidden):
				var hs: GPUParticles2D = hidden.get_node("Sparks")
				row.merge({"hidden_sparks_emitting": hs.emitting, "hidden_visible_in_tree": hs.is_visible_in_tree()})
			row["draw_calls_in_frame"] = RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_DRAW_CALLS_IN_FRAME)
			row["primitives_in_frame"] = RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_PRIMITIVES_IN_FRAME)
			rows.append(row)
		await process_frame
		t += root.get_process_delta_time()
		_game_time = t
	for row: Dictionary in rows:
		observe("state-over-time", row)
	observe("finished-signal", {"game_time_s": finished_at, "lifetimes_s": {"Sparks": 0.45, "Smoke": 0.8}})
	if is_instance_valid(fx):
		fx.free()
	if is_instance_valid(hidden):
		hidden.free()
	await process_frame

	# CPU price: wall time per frame for 50 frames with no effect, then 50 frames with 6 instances alive (the bound, A4).
	var idle := await wall_us_per_frame(50)
	var six: Array[Node] = []
	for i in 6:
		var inst: Node2D = packed.instantiate()
		inst.position = Vector2(100 + 80 * i, 180)
		root.add_child(inst)
		six.append(inst)
	var busy := await wall_us_per_frame(50)
	var alive := six.filter(func(n: Node) -> bool: return is_instance_valid(n)).size()
	observe("cpu-price", {"us_per_frame_no_effect": idle, "us_per_frame_6_instances": busy,
		"difference_us": busy.mean - idle.mean, "instances_alive_after": alive})
	for n: Node in six:
		if is_instance_valid(n):
			n.free()


func wall_us_per_frame(frames: int) -> Dictionary:
	var samples := []
	for i in frames:
		var t0 := Time.get_ticks_usec()
		await process_frame
		samples.append(Time.get_ticks_usec() - t0)
	samples.sort()
	var total := 0
	for s: int in samples:
		total += s
	return {"mean": snappedf(float(total) / frames, 0.1), "median": samples[frames / 2], "max": samples.back()}
