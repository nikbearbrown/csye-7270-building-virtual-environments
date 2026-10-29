extends Node
## Headless checks for the hearts' safe tint (CHANGE-BRIEF.md, sections 2 and 6).
## Run from the assignment folder:
##   scripts/run-test.sh game invulnerable_tint_checks.tscn <fps>
## Prints one line per check and exits with code 1 if any check fails.
##
## The shader: its uniforms as the engine reports them, and their defaults as
## the source declares them, since a headless engine reports none. The
## material: on Hud/Hearts only, local to the scene, and no script but hud.gd
## names tint_amount. Then real play, through real input: Enter on the title,
## move_right into the first spikes. A sampler with a high process_priority
## records tint_amount after every other _process() in each frame, and the
## checks read those samples:
## - hit 1: the first frame, the fade, the end and the duration; Rudy walks back
##   into the spikes while the window is open, and the hit is ignored;
## - hit 2, at Engine.time_scale 0.5: the duration in real time;
## - hit 3 takes his last heart, and the respawn opens a new window;
## - hit 4: Esc in mid-window holds the tint, and resumes it; then the level is
##   freed and started again, as Enter on the end card does, and the new hearts
##   start at 0.0.
## Headless, nothing is drawn: the checks read the value the material holds,
## not a pixel.

const MAIN := preload("res://app/main.tscn")
const SHADER_PATH := "res://shaders/invulnerable_tint.gdshader"
const MATERIAL_PATH := "res://ui/hearts_tint.tres"
const EPS := 1e-6

var _failures := 0
var _main: Main
var _rudy: Rudy
var _sampler: Sampler
var _fps := 0


## Records, once per frame and after every other _process(), what the hearts'
## material holds and the state of Rudy's window. It runs while the game is
## paused, and counts the physics ticks the game ran since the last frame.
class Sampler extends Node:
	var main: Main
	var samples: Array[Dictionary] = []
	var _ticks := 0
	var _game_time := 0.0

	func _physics_process(_delta: float) -> void:
		if get_tree().paused:
			return
		_ticks += 1
		_game_time += Engine.time_scale / Engine.physics_ticks_per_second

	func _process(delta: float) -> void:
		if is_instance_valid(main):
			var rudy: Rudy = main.get_node("Rudy")
			var hud: Hud = main.get_node("Hud")
			var material := (main.get_node("Hud/Hearts") as Control).material as ShaderMaterial
			var spikes: Spikes = main.get_node("Level1/Hazards/SpikesA")
			var value: Variant = material.get_shader_parameter(&"tint_amount")
			samples.append({
				"material": material,
				"tint": 0.0 if value == null else float(value),
				"tint_set": value != null,
				"invulnerable": rudy.is_invulnerable(),
				"left": rudy._invulnerable_left,
				"window": rudy.invulnerable_time,
				"hearts": rudy.hearts,
				"mode": rudy.mode,
				"on_spikes": spikes.overlaps_body(rudy),
				"paused": get_tree().paused,
				"showing_paused": hud.is_showing_paused(),
				"time_scale": Engine.time_scale,
				"delta": delta,
				"ticks": _ticks,
				"game_time": _game_time,
			})
		_ticks = 0
		_game_time = 0.0


func _ready() -> void:
	_sampler = Sampler.new()
	_sampler.process_priority = 1000
	_sampler.process_mode = Node.PROCESS_MODE_ALWAYS
	add_child(_sampler)
	_check_shader()
	_start_level()
	await _frames(5)
	_fps = roundi(1.0 / _sampler.samples[-1].delta)
	print("frames per second, from the frame delta: %d" % _fps)
	_check_material()
	await _run_play()
	Engine.time_scale = 1.0
	print("all checks passed" if _failures == 0 else "%d check(s) FAILED" % _failures)
	get_tree().quit(1 if _failures > 0 else 0)


## A fresh level that opens on the title, as the game does.
func _start_level() -> void:
	Main.title_shown = false
	_main = MAIN.instantiate()
	add_child(_main)
	_rudy = _main.get_node("Rudy")
	_sampler.main = _main


## A1, A2, A14: the uniforms the engine reports, the defaults in the source,
## and the renderer the project names.
func _check_shader() -> void:
	var shader: Shader = (load(MATERIAL_PATH) as ShaderMaterial).shader
	var reported := {}
	for uniform: Dictionary in shader.get_shader_uniform_list():
		reported[uniform.name] = uniform
	var types_ok: bool = reported.keys().size() == 3 and reported.has("tint_amount") and reported.has("tint_color") \
		and reported.has("tint_strength") and reported.tint_amount.type == TYPE_FLOAT \
		and reported.tint_color.type == TYPE_COLOR and reported.tint_strength.type == TYPE_FLOAT
	var ranges_ok: bool = types_ok
	for name: String in ["tint_amount", "tint_strength"]:
		if not types_ok:
			break
		var bounds: PackedStringArray = reported[name].hint_string.split(",")
		ranges_ok = ranges_ok and reported[name].hint == PROPERTY_HINT_RANGE and bounds.size() >= 2 \
			and float(bounds[0]) == 0.0 and float(bounds[1]) == 1.0
	_check("A1 the shader reports exactly tint_amount (float), tint_color (Color) and tint_strength (float); both floats are hint_range(0.0, 1.0)",
		types_ok and ranges_ok, ", ".join(PackedStringArray(reported.keys().map(func(n: String) -> String:
			return "%s %s '%s'" % [n, type_string(reported[n].type), reported[n].hint_string]))))

	var source := FileAccess.get_file_as_string(SHADER_PATH)
	var declared := {}
	var declaration := RegEx.create_from_string(r"uniform\s+(\w+)\s+(\w+)\s*(?::[^=;]*)?(?:=\s*([^;]+))?;")
	for found in declaration.search_all(source):
		declared[found.get_string(2)] = found.get_string(3).strip_edges()
	var color := RegEx.create_from_string(r"^vec4\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*\)$").search(declared.get("tint_color", ""))
	var defaults_ok: bool = declared.size() == 3 and declared.get("tint_amount", "") != "" and float(declared.tint_amount) == 0.0 \
		and declared.get("tint_strength", "") != "" and float(declared.tint_strength) == 0.4 and color != null \
		and float(color.get_string(1)) == 0.6 and float(color.get_string(2)) == 0.88 \
		and float(color.get_string(3)) == 1.0 and float(color.get_string(4)) == 1.0
	var mode_ok := RegEx.create_from_string(r"(?m)^\s*shader_type\s+canvas_item\s*;").search(source) != null \
		and not source.contains("render_mode")
	_check("A2 the source declares the defaults 0.0, vec4(0.6, 0.88, 1.0, 1.0) and 0.4, shader_type canvas_item and no render_mode",
		defaults_ok and mode_ok, "declared %s" % declared)

	var method: String = ProjectSettings.get_setting("rendering/renderer/rendering_method")
	_check("A14 the project names the GL Compatibility renderer (a setting read, not a render)",
		method == "gl_compatibility", method)


## A3, A4 (scripts): where the material is, and who sets its uniforms.
func _check_material() -> void:
	var file_material := load(MATERIAL_PATH) as ShaderMaterial
	var using: PackedStringArray = []
	var pending: Array[Node] = [_main]
	while not pending.is_empty():
		var node: Node = pending.pop_back()
		pending.append_array(node.get_children())
		if node is CanvasItem and (node as CanvasItem).material is ShaderMaterial:
			var shader := ((node as CanvasItem).material as ShaderMaterial).shader
			if shader and shader.resource_path == SHADER_PATH:
				using.append(String(_main.get_path_to(node)))
	var naming: PackedStringArray = []
	for path in _files_under("res://", ["tscn", "tres"]):
		if FileAccess.get_file_as_string(path).contains(MATERIAL_PATH):
			naming.append(path)
	var hearts_material := (_main.get_node("Hud/Hearts") as Control).material
	_check("A3 only Hud/Hearts uses the shader, only hud.tscn names the material, and the material is local to the scene",
		using == PackedStringArray(["Hud/Hearts"]) and naming == PackedStringArray(["res://ui/hud.tscn"])
		and file_material.resource_local_to_scene and hearts_material != file_material,
		"used by %s; named in %s; local to scene %s; the hearts have their own copy %s" % [
			using, naming, file_material.resource_local_to_scene, hearts_material != file_material])

	var names := {"tint_amount": [], "tint_color": [], "tint_strength": []}
	for dir: String in ["res://app", "res://content", "res://ui", "res://systems"]:
		for path in _files_under(dir, ["gd"]):
			var text := FileAccess.get_file_as_string(path)
			for name: String in names:
				if text.contains(name):
					names[name].append(path)
	_check("A4 no game script names tint_color or tint_strength, and only hud.gd names tint_amount",
		names.tint_color.is_empty() and names.tint_strength.is_empty()
		and names.tint_amount == ["res://ui/hud.gd"], str(names))


func _run_play() -> void:
	var level: Node2D = _main.get_node("Level1")
	var spikes: Spikes = level.get_node("Hazards/SpikesA")
	var material := (_main.get_node("Hud/Hearts") as Control).material as ShaderMaterial

	# The title, then play before any hit.
	await _frames(10)
	var title_from := 0
	var title_to := _sampler.samples.size()
	if not _setup("the game opens on the title", _main.state == Main.State.TITLE):
		return
	await _tap(&"restart")
	await _frames(roundi(Main.FADE_TIME * Engine.physics_ticks_per_second) + 5)
	if not _setup("Enter starts play", _main.state == Main.State.PLAYING and _rudy.mode == Rudy.Mode.PLAY):
		return

	# Hit 1: walk into the spikes; then back into them while the window is open.
	var hit_1 := _sampler.samples.size()
	await _hold_until(&"move_right", func() -> bool: return _rudy.hearts < 3, 600)
	if not _setup("hit 1: move_right walks Rudy into the first spikes", _rudy.hearts == 2):
		return
	await _wait_until(func() -> bool: return _rudy.mode == Rudy.Mode.PLAY and _rudy.is_on_floor(), 120)
	await _hold_until(&"move_right", func() -> bool: return spikes.overlaps_body(_rudy), 120)
	if not _setup("hit 1: he walks back onto the spikes while invulnerable",
		spikes.overlaps_body(_rudy) and _rudy.is_invulnerable()):
		return
	await _hold_until(&"move_left", func() -> bool: return not spikes.overlaps_body(_rudy), 120)
	await _hold(&"move_left", 6)
	if not _setup("hit 1: he steps off the spikes before the window ends",
		not spikes.overlaps_body(_rudy) and _rudy.is_invulnerable() and _rudy.hearts == 2):
		return
	await _wait_until(func() -> bool: return not _rudy.is_invulnerable(), 120)
	await _frames(5)

	# Hit 2, at half speed.
	var hit_2 := _sampler.samples.size()
	Engine.time_scale = 0.5
	await _hold_until(&"move_right", func() -> bool: return _rudy.hearts < 2, 600)
	if not _setup("hit 2: at time scale 0.5, move_right walks him into the spikes", _rudy.hearts == 1):
		return
	await _wait_until(func() -> bool: return not _rudy.is_invulnerable(), 300)
	await _frames(5)
	Engine.time_scale = 1.0
	if not _setup("hit 2: he is off the spikes when the window ends", not spikes.overlaps_body(_rudy)):
		return

	# Hit 3 takes the last heart; the level starts over and he gets back up.
	var hit_3 := _sampler.samples.size()
	await _hold_until(&"move_right", func() -> bool: return _rudy.hearts < 1, 600)
	if not _setup("hit 3: the spikes take his last heart", _rudy.mode == Rudy.Mode.DEFEATED):
		return
	await _wait_until(func() -> bool: return _rudy.mode == Rudy.Mode.RESPAWNING, 300)
	await _wait_until(func() -> bool: return _rudy.mode == Rudy.Mode.PLAY and not _rudy.is_invulnerable(), 300)
	await _frames(5)
	if not _setup("hit 3: he gets back up with full hearts, and the respawn's window runs out",
		_rudy.hearts == 3 and _main.state == Main.State.PLAYING and not _rudy.is_invulnerable()):
		return

	# Hit 4: Esc in mid-window, then the level is freed and started again.
	var hit_4 := _sampler.samples.size()
	await _hold_until(&"move_right", func() -> bool: return _rudy.hearts < 3, 600)
	if not _setup("hit 4: move_right walks him into the spikes again", _rudy.hearts == 2):
		return
	await _frames(20)
	await _tap(&"pause")
	if not _setup("hit 4: Esc pauses in mid-window", _main.is_paused() and _rudy.is_invulnerable()):
		return
	for i in 30:
		await get_tree().process_frame
	await _tap(&"pause")
	await _frames(10)
	if not _setup("hit 4: Esc resumes, and the window is still open", not _main.is_paused() and _rudy.is_invulnerable()):
		return
	var reload := _sampler.samples.size()
	var old_value: Variant = material.get_shader_parameter(&"tint_amount")
	_sampler.main = null
	_main.queue_free()
	await _frames(1)
	_start_level()
	var new_material := (_main.get_node("Hud/Hearts") as Control).material as ShaderMaterial
	var new_before: Variant = new_material.get_shader_parameter(&"tint_amount")
	await _frames(5)
	var samples := _sampler.samples

	# What the samples show.
	# Each window is named by the stretch of the run it starts in; the respawn's
	# must start on the first frame he is getting back up. A window that is
	# missing fails every check that needs it.
	var windows := _windows(0, reload)
	var respawn := hit_4
	for k in range(hit_3, hit_4):
		if samples[k].mode == Rudy.Mode.RESPAWNING:
			respawn = k
			break
	var w1 := _window_in(windows, hit_1, hit_2)
	var w2 := _window_in(windows, hit_2, hit_3)
	var w_respawn := _window_in(windows, respawn, respawn + 1)
	var w4 := _window_in(windows, hit_4, reload)
	var labelled := {"hit 1": w1, "hit 2 (time scale 0.5)": w2, "hit 3": _window_in(windows, hit_3, respawn),
		"respawn": w_respawn, "hit 4": w4}
	print("windows found: %d; missing: %s" % [windows.size(),
		labelled.keys().filter(func(label: String) -> bool: return labelled[label].is_empty())])

	var before_hit := samples.slice(title_to, w1.get("first", hit_1))
	_check("A5 tint_amount is 0.0 on the title and in play before the first hit",
		title_to > 0 and _all(samples.slice(title_from, title_to), func(s: Dictionary) -> bool: return s.tint_set and s.tint == 0.0)
		and _all(before_hit, func(s: Dictionary) -> bool: return s.tint_set and s.tint == 0.0),
		"%d title frames, %d frames in play" % [title_to - title_from, before_hit.size()])

	var firsts: PackedStringArray = []
	var first_ok := true
	for label: String in labelled:
		var w: Dictionary = labelled[label]
		if w.is_empty():
			first_ok = false
			firsts.append("%s: no window" % label)
			continue
		var first: float = samples[w.first].tint
		firsts.append("%s %.6f (= %.3f/72)" % [label, first, first * 72.0])
		first_ok = first_ok and first >= 70.0 / 72.0 - EPS and first <= 1.0
		var exact := label in ["hit 1", "hit 3", "hit 4"] and _fps in [60, 144]
		if exact:
			first_ok = first_ok and absf(first - 71.0 / 72.0) <= EPS
	_check("A6 the first frame of every window is at least 70/72; after a hit at time scale 1.0 at 60 and 144 fps it is 71/72",
		first_ok, ", ".join(firsts))

	var fade_errors: PackedStringArray = []
	for label: String in labelled:
		var w: Dictionary = labelled[label]
		if w.is_empty():
			fade_errors.append("%s: no window" % label)
			continue
		var first: float = samples[w.first].tint
		var game_time := 0.0
		for k in range(w.first, w.last + 1):
			var s: Dictionary = samples[k]
			if k > w.first:
				game_time += s.game_time
			var from_state: float = s.left / s.window
			var from_time: float = first - game_time / s.window
			if absf(s.tint - from_state) > EPS or absf(s.tint - from_time) > EPS:
				fade_errors.append("%s frame %d: %.6f, state %.6f, game time %.6f" % [label, k - w.first, s.tint, from_state, from_time])
	_check("A7 on every frame of a window tint_amount is _invulnerable_left / invulnerable_time, and falls with game time from its first value",
		fade_errors.is_empty(), "; ".join(fade_errors.slice(0, 5)))

	var disagree: PackedStringArray = []
	for k in samples.size():
		var s: Dictionary = samples[k]
		if (s.tint > 0.0) != s.invulnerable:
			disagree.append("frame %d: tint %.6f, invulnerable %s" % [k, s.tint, s.invulnerable])
	var ends: PackedStringArray = []
	var ends_ok := true
	for label: String in ["hit 1", "hit 2 (time scale 0.5)", "respawn"]:
		var w: Dictionary = labelled[label]
		if w.is_empty():
			ends_ok = false
			ends.append("%s: no window" % label)
			continue
		ends_ok = ends_ok and w.end >= 0 and samples[w.end].tint_set and samples[w.end].tint == 0.0 \
			and not samples[w.end].invulnerable and samples[w.end - 1].invulnerable
		ends.append("%s ends %s" % [label, "%.6f" % samples[w.end].tint if w.end >= 0 else "never"])
	_check("A8 on every frame tint_amount is above 0 exactly when Rudy is invulnerable, and it is exactly 0.0 on the first frame he is not",
		disagree.is_empty() and ends_ok, "%d frames; %s; %s" % [samples.size(), ", ".join(ends), "; ".join(disagree.slice(0, 5))])

	var spans: PackedStringArray = []
	var spans_ok := true
	for label: String in ["hit 1", "hit 2 (time scale 0.5)"]:
		var w: Dictionary = labelled[label]
		var expected := 71.0 / 60.0 if label == "hit 1" else 144.0 / 60.0
		var span := float(w.end - w.first) / _fps if not w.is_empty() and w.end >= 0 else INF
		spans_ok = spans_ok and absf(span - expected) <= 1.0 / _fps + EPS
		spans.append("%s %.4f s of real time, expected %.4f s ± %.4f" % [label, span, expected, 1.0 / _fps])
	_check("A9 the tint shows for 1.183 s ± one frame at time scale 1.0, and for 2.4 s of real time ± one frame at 0.5",
		spans_ok, ", ".join(spans))

	# Hit 1's frames until it ends, or until hit 2 if it never does.
	var w1_end: int = (w1.end if w1.end >= 0 else hit_2) if not w1.is_empty() else hit_1
	var w1_frames := samples.slice(w1.get("first", hit_1), w1_end)
	var touched := w1_frames.filter(func(s: Dictionary) -> bool: return s.on_spikes and s.invulnerable).size()
	var rises := 0
	for k in range(w1.get("first", hit_1) + 1, w1_end):
		if samples[k].tint > samples[k - 1].tint:
			rises += 1
	_check("A10 walking back onto the spikes in the window is ignored: the hearts stay at 2 and tint_amount never rises",
		not w1.is_empty() and touched > 0 and rises == 0 and _all(w1_frames, func(s: Dictionary) -> bool: return s.hearts == 2),
		"%d invulnerable frames on the spikes, %d rises%s" % [touched, rises, "" if not w1.is_empty() else "; no window"])

	var r := respawn
	var before_jump: float = samples[r - 1].tint
	_check("A11 the respawn restarts the tint: on its first frame tint_amount jumps up to between 70/72 and 1.0",
		not w_respawn.is_empty() and samples[r].mode == Rudy.Mode.RESPAWNING and samples[r - 1].mode != Rudy.Mode.RESPAWNING
		and samples[r].tint > before_jump and samples[r].tint >= 70.0 / 72.0 - EPS and samples[r].tint <= 1.0
		and samples[r].hearts == 3,
		"%.6f before the jump, %.6f after" % [before_jump, samples[r].tint])

	var w4_frames := samples.slice(w4.get("first", hit_4), reload)
	var first_paused := -1
	var resumed := -1
	for k in w4_frames.size():
		if first_paused < 0 and w4_frames[k].paused:
			first_paused = k
		elif first_paused >= 0 and not w4_frames[k].paused:
			resumed = k
			break
	var paused: Array = w4_frames.slice(first_paused, resumed) if first_paused >= 0 and resumed > first_paused else []
	var held: float = paused[0].tint if not paused.is_empty() else -1.0
	var one_frame := ceilf(Engine.physics_ticks_per_second / float(_fps)) / Engine.physics_ticks_per_second / _rudy.invulnerable_time
	var game_time := 0.0
	for s: Dictionary in w4_frames.slice(1):
		game_time += s.game_time
	var fell: float = (w4_frames[0].tint - w4_frames[-1].tint) * _rudy.invulnerable_time
	var unpaused_time := float(w4_frames.size() - 1 - paused.size()) / _fps
	_check("A12 while paused tint_amount holds, with \"Paused\" showing; it resumes from the held value; it falls with unpaused game time only",
		not w4.is_empty() and paused.size() >= 30 and _all(paused, func(s: Dictionary) -> bool: return s.tint == held and s.showing_paused)
		and w4_frames[resumed].tint <= held and w4_frames[resumed].tint >= held - one_frame - EPS
		and absf(fell - game_time) <= EPS
		and absf(game_time - unpaused_time) <= 1.0 / Engine.physics_ticks_per_second + 1.0 / _fps + EPS,
		"%d paused frames at %.6f; resumed at %.6f; it fell %.4f s, over %.4f s of game time and %.4f s of unpaused real time (%.4f s in all)" % [
			paused.size(), held, w4_frames[resumed].tint if resumed >= 0 else -1.0, fell, game_time, unpaused_time,
			float(w4_frames.size() - 1) / _fps])

	var new_frames := samples.slice(reload).filter(func(s: Dictionary) -> bool: return s.material == new_material)
	_check("A13 a reload in mid-window: the old hearts were tinted, the new hearts have their own material, at 0.0 before their first frame and on it",
		old_value != null and float(old_value) > 0.0 and new_material != material
		and (new_before == null or float(new_before) == 0.0) and not new_frames.is_empty()
		and new_frames[0].tint_set and new_frames[0].tint == 0.0,
		"old %s; new before its first frame %s (unset means the shader's default, 0.0); on its first frame %s" % [
			old_value, "unset" if new_before == null else str(new_before),
			str(new_frames[0].tint) if not new_frames.is_empty() else "no frame"])

	var kept := [material, new_material].all(func(m: ShaderMaterial) -> bool:
		var c: Variant = m.get_shader_parameter(&"tint_color")
		var t: Variant = m.get_shader_parameter(&"tint_strength")
		return (c == null or c == Color(0.6, 0.88, 1.0, 1.0)) and (t == null or is_equal_approx(t, 0.4)))
	_check("A4 after play, tint_color and tint_strength are still unset on both materials, or at the shader's defaults",
		kept, "old %s, %s; new %s, %s" % [material.get_shader_parameter(&"tint_color"), material.get_shader_parameter(&"tint_strength"),
			new_material.get_shader_parameter(&"tint_color"), new_material.get_shader_parameter(&"tint_strength")])


## The windows in samples[from, to): each starts on a frame where tint_amount
## rose on the same material, and ends on the first frame at 0.0 (`end`), or is
## cut by the next rise or a new material (`end` -1). `last` is its last frame
## above 0.
func _windows(from: int, to: int) -> Array[Dictionary]:
	var samples := _sampler.samples
	var found: Array[Dictionary] = []
	var open := {}
	for k in range(maxi(from, 1), to):
		var s: Dictionary = samples[k]
		var p: Dictionary = samples[k - 1]
		if not open.is_empty() and s.material != p.material:
			open.last = k - 1
			found.append(open)
			open = {}
		if s.material == p.material and s.tint > p.tint:
			if not open.is_empty():
				open.last = k - 1
				found.append(open)
			open = {"first": k, "end": -1, "last": k}
		elif not open.is_empty() and s.tint <= 0.0:
			open.end = k
			open.last = k - 1
			found.append(open)
			open = {}
	if not open.is_empty():
		open.last = to - 1
		found.append(open)
	return found


## The first window that starts in samples[from, to), or {}.
func _window_in(windows: Array[Dictionary], from: int, to: int) -> Dictionary:
	for w in windows:
		if w.first >= from and w.first < to:
			return w
	return {}


func _all(samples: Array, test: Callable) -> bool:
	return samples.all(test)


func _files_under(root: String, extensions: Array[String]) -> PackedStringArray:
	var files: PackedStringArray = []
	var pending: Array[String] = [root]
	while not pending.is_empty():
		var dir: String = pending.pop_back()
		for sub in DirAccess.get_directories_at(dir):
			if not sub.begins_with("."):
				pending.append(dir.path_join(sub))
		for file in DirAccess.get_files_at(dir):
			if file.get_extension() in extensions:
				files.append(dir.path_join(file))
	return files


## A step the checks need, not a check: if it misses, the run stops here.
func _setup(what: String, ok: bool) -> bool:
	if not ok:
		print("FAIL  setup: %s" % what)
		_failures += 1
	return ok


func _check(what: String, ok: bool, detail: String = "") -> void:
	print("%s  %s%s" % ["PASS" if ok else "FAIL", what, "" if detail.is_empty() else "  (%s)" % detail])
	if not ok:
		_failures += 1


func _frames(n: int) -> void:
	for i in n:
		await get_tree().physics_frame


## Waits until `condition` is true, for at most `max_ticks`; returns the ticks waited.
func _wait_until(condition: Callable, max_ticks: int) -> int:
	for t in max_ticks:
		if condition.call():
			return t
		await get_tree().physics_frame
	return max_ticks


func _hold(action: StringName, ticks: int) -> void:
	Input.action_press(action)
	await _frames(ticks)
	Input.action_release(action)


func _hold_until(action: StringName, condition: Callable, max_ticks: int) -> void:
	Input.action_press(action)
	await _wait_until(condition, max_ticks)
	Input.action_release(action)


func _tap(action: StringName) -> void:
	Input.action_press(action)
	await _frames(2)
	Input.action_release(action)
