extends SceneTree
## Assignment 7 visual upgrade: read-back of the cave-light flicker clip (effects/cave_lights.tscn) and the darkening.
## Checks: the assignment's track_problems() (and key_problems()); only energy and texture_scale of the two
## PointLight2Ds are keyed, continuous; LOOP_LINEAR and autoplay; the continuous-track seam rule per track (first key at
## 0, last key at the length, value at 0 equal to the value at the length); each light's scene value equals its clip
## value at 0; the flicker is clearly visible but bounded (r1, 2026-11-12: energy swings at least 20 % and at most
## 32 % around the scene value, texture_scale at least 6 % and at most 9 %) and irregular; nothing else keys the lights (every AnimationPlayer in the main scene) and no
## game script writes their energy or texture_scale; both CanvasModulates in place.
## From fall-2026/zhefan-z/assignment-7/:
##   ./scripts/run-test.sh test_clip_flicker.gd 60
## Prints one JSON line per check and "WALKER TESTS: N checks / F failures"; exit code 1 on any failure.

const AnimChecks := preload("res://tests/anim_checks.gd")
const SCENE := "res://effects/cave_lights.tscn"
const LIGHTS := ["TorchLeft", "TorchRight"]
const PROPS := ["energy", "texture_scale"]
const GAME_DIRS := ["res://features", "res://game", "res://ui", "res://audio", "res://effects"]
const EPS := 1e-6

var results: Array[Dictionary] = []
var failures := 0


func _initialize() -> void:
	call_deferred("run")


func check(id: String, passed: bool, observed: Dictionary) -> void:
	results.append({"id": id, "status": "PASS" if passed else "FAIL", "observed": observed})
	if not passed:
		failures += 1
	print(JSON.stringify(results.back()))


func observe(id: String, observed: Dictionary) -> void:
	print(JSON.stringify({"id": id, "observation": observed}))


func gd_files(dir: String) -> Array[String]:
	var out: Array[String] = []
	var d := DirAccess.open(dir)
	if d == null:
		return out
	for f in d.get_files():
		if f.ends_with(".gd"):
			out.append(dir.path_join(f))
	for sub in d.get_directories():
		out.append_array(gd_files(dir.path_join(sub)))
	return out


func run() -> void:
	var missing := AnimChecks.missing_properties("PointLight2D", ["energy", "texture_scale", "color", "texture"]) \
		+ AnimChecks.missing_properties("CanvasModulate", ["color"]) \
		+ AnimChecks.missing_properties("AnimationPlayer", ["autoplay", "callback_mode_process"])
	check("godot4-property-names-exist", missing.is_empty(), {"missing": missing})

	var lights: Node = load(SCENE).instantiate()
	var ap: AnimationPlayer = lights.get_node_or_null("Flicker")
	check("flicker-player-autoplays-flicker", ap != null and ap.autoplay == "flicker" and ap.has_animation("flicker")
		and ap.get_animation_list().size() == 1, {"autoplay": ap.autoplay if ap else null,
		"clips": Array(ap.get_animation_list()) if ap else []})
	if ap == null:
		print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
		quit(1)
		return
	var problems := AnimChecks.track_problems(ap)
	check("every-track-resolves", problems.is_empty(), {"problems": problems})
	var key_problems := AnimChecks.key_problems(ap)
	check("every-key-in-range-increasing-and-typed", key_problems.is_empty(), {"problems": key_problems})

	var anim := ap.get_animation("flicker")
	check("flicker-loops-linear", anim.loop_mode == Animation.LOOP_LINEAR, {"loop_mode": anim.loop_mode, "length": anim.length})
	var expected_paths := []
	for l: String in LIGHTS:
		for p: String in PROPS:
			expected_paths.append("%s:%s" % [l, p])
	var paths := []
	var seam := {}
	var continuous := true
	var ranges := {}
	for i in anim.get_track_count():
		var path := str(anim.track_get_path(i))
		paths.append(path)
		continuous = continuous and anim.track_get_type(i) == Animation.TYPE_VALUE \
			and anim.value_track_get_update_mode(i) == Animation.UPDATE_CONTINUOUS
		var n := anim.track_get_key_count(i)
		var first_t := anim.track_get_key_time(i, 0)
		var last_t := anim.track_get_key_time(i, n - 1)
		var v0: float = anim.value_track_interpolate(i, 0.0)
		var vl: float = anim.value_track_interpolate(i, anim.length)
		seam[path] = {"first_key_s": first_t, "last_key_s": snappedf(last_t, 1e-6), "value_at_0": v0,
			"value_at_length": vl, "ok": absf(first_t) < EPS and absf(last_t - anim.length) < 1e-5 and absf(v0 - vl) < EPS}
		var vals := []
		var gaps := []
		for k in n:
			vals.append(anim.track_get_key_value(i, k))
			if k > 0:
				gaps.append(snappedf(anim.track_get_key_time(i, k) - anim.track_get_key_time(i, k - 1), 0.001))
		ranges[path] = {"min": vals.min(), "max": vals.max(), "keys": n, "key_gaps_s": gaps}
	paths.sort()
	expected_paths.sort()
	check("only-energy-and-texture-scale-of-the-two-lights-continuous", paths == expected_paths and continuous,
		{"tracks": paths, "expected": expected_paths, "continuous": continuous})
	check("seam-rule-value-at-0-equals-value-at-length", seam.values().all(func(s: Dictionary) -> bool: return s.ok), seam)

	var rest := {}
	var visible_bounded := true
	for l: String in LIGHTS:
		var light: PointLight2D = lights.get_node(l)
		for p: String in PROPS:
			var path := "%s:%s" % [l, p]
			var at0: float = anim.value_track_interpolate(anim.find_track(NodePath(path), Animation.TYPE_VALUE), 0.0)
			rest[path] = [light.get(p), at0]
			var r: Dictionary = ranges[path]
			var base: float = light.get(p)
			var limit := 0.32 if p == "energy" else 0.09   # at most this far from the scene value
			var reach := 0.2 if p == "energy" else 0.06    # and at least this far both ways: clearly visible
			visible_bounded = visible_bounded and r.min >= base * (1.0 - limit) - EPS and r.max <= base * (1.0 + limit) + EPS 				and r.min <= base * (1.0 - reach) + EPS and r.max >= base * (1.0 + reach) - EPS
	check("scene-values-equal-clip-at-0", rest.values().all(func(v: Array) -> bool: return absf(v[0] - v[1]) < EPS), rest)
	var irregular := ranges.values().all(func(r: Dictionary) -> bool: return r.key_gaps_s.max() - r.key_gaps_s.min() > 0.05)
	check("flicker-visible-bounded-and-irregular", visible_bounded and irregular, {"ranges": ranges})
	lights.free()

	# Nothing else keys the lights; no game script writes their energy or texture_scale.
	var main: Node = load("res://game/main.tscn").instantiate()
	var light_paths := []
	for l: String in LIGHTS:
		light_paths.append(main.get_node("Background/CaveLights/" + l))
	var others := []
	for player: AnimationPlayer in AnimChecks.players(main):
		var root := player.get_node(player.root_node)
		for n in player.get_animation_list():
			var a := player.get_animation(n)
			for i in a.get_track_count():
				var target := root.get_node_or_null(NodePath(a.track_get_path(i).get_concatenated_names()))
				if target is Light2D and str(main.get_path_to(player)) != "Background/CaveLights/Flicker":
					others.append("%s %s %s" % [main.get_path_to(player), n, a.track_get_path(i)])
	var writes := []
	var pat := RegEx.create_from_string("\\.(energy|texture_scale)\\s*(=|\\+=|-=|\\*=)(?!=)|set(_deferred)?\\(\\s*&?\"(energy|texture_scale)\"")
	for dir: String in GAME_DIRS:
		for path in gd_files(dir):
			var lines := FileAccess.get_file_as_string(path).split("\n")
			for i in lines.size():
				if pat.search(lines[i].split("#")[0]):
					writes.append("%s:%d" % [path, i + 1])
	check("nothing-else-keys-or-writes-the-lights", others.is_empty() and writes.is_empty() and light_paths.size() == 2,
		{"other_players_keying_lights": others, "script_writes": writes})
	var world_dark: CanvasModulate = main.get_node_or_null("Darken")
	var bg_dark: CanvasModulate = main.get_node_or_null("Background/Darken")
	check("darkening-on-world-and-background", world_dark != null and bg_dark != null
		and world_dark.color.v < 1.0 and bg_dark.color.v < 1.0,
		{"world": world_dark.color if world_dark else null, "background": bg_dark.color if bg_dark else null})
	main.free()

	await process_frame
	print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
	quit(1 if failures else 0)
