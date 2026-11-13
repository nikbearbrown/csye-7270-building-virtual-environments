extends SceneTree
## Assignment 7 read-back of clip 1, the mage run cycle, and the player's other clips (CHANGE-BRIEF Clip 1 and Tests).
## Loads features/player/player.tscn (not added to the tree, so nothing plays) and reads every clip back key by key:
## every track resolves (the assignment's track_problems() in anim_checks.gd; key types in key_problems()); every clip name present; each clip
## keys Sprite2D texture, hframes and frame, discrete; every frame key below hframes * vframes. Run r2 (approved
## 2026-11-12): the Gemini 4-frame sheet mage_run_cycle_sheet.png (248x69, hframes 4) at 10 fps, frame keys 0-3 at 0,
## 0.1, 0.2, 0.3 s, length 0.4, LOOP_LINEAR, the seam rule; the sheet's size, palette (the A2 mage sprites' colours
## only), ground rows per cell, imported pixels and import settings.
## From fall-2026/zhefan-z/assignment-7/:
##   ./scripts/run-test.sh test_clip_run.gd 60
## Prints one JSON line per check and "WALKER TESTS: N checks / F failures"; exit code 1 on any failure.
## Image.load_from_file prints an engine WARNING ("will not work on export") per source PNG; it is expected here.

const AnimChecks := preload("res://tests/anim_checks.gd")
const SCENE := "res://features/player/player.tscn"
const MAGE := "res://assets/sprites/mage/"
const SHEET := MAGE + "mage_run_cycle_sheet.png"
const CELLS := [MAGE + "mage_run_contact.png", MAGE + "mage_run_passing.png"]   # import settings to match
const A2_SPRITES := ["mage_idle", "mage_run_contact", "mage_run_passing", "mage_rise", "mage_fall", "mage_cast",
	"mage_hurt", "mage_fail", "mage_win"]
const RUN_KEYS := [[0.0, 0], [0.1, 1], [0.2, 2], [0.3, 3]]
## Lowest opaque row of each cell, from tools/clean_run_cycle.py: frames 1-3 on the ground row 66 (anchor 31, 67);
## frame 4 ("up") airborne, 2 px above it.
const CELL_LOWEST_ROW := [66, 66, 66, 64]
const CLIP_TEXTURE := {"idle": "mage_idle.png", "run": "mage_run_cycle_sheet.png", "rise": "mage_rise.png",
	"fall": "mage_fall.png", "cast": "mage_cast.png", "hurt": "mage_hurt.png", "fail": "mage_fail.png",
	"fail_pit": "mage_fall.png", "win": "mage_win.png"}
const TRACKS := ["Sprite2D:texture", "Sprite2D:hframes", "Sprite2D:frame"]
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


func keys_of(anim: Animation, i: int) -> Array:
	var out := []
	for k in anim.track_get_key_count(i):
		out.append([snappedf(anim.track_get_key_time(i, k), 1e-6), anim.track_get_key_value(i, k)])
	return out


func params_of(import_path: String) -> String:
	var text := FileAccess.get_file_as_string(ProjectSettings.globalize_path(import_path))
	var at := text.find("[params]")
	return text.substr(at) if at >= 0 else ""


func run() -> void:
	# Godot 4 names on this binary (CLAUDE.md "Godot 4 names").
	var godot3_present := []
	for n: String in ["loop", "playback_speed", "playback_process_mode"]:
		if AnimChecks.missing_properties("AnimationPlayer", [n]).is_empty() \
				or AnimChecks.missing_properties("Animation", [n]).is_empty():
			godot3_present.append(n)
	var missing := {
		"AnimationPlayer": AnimChecks.missing_properties("AnimationPlayer", ["callback_mode_process", "autoplay", "speed_scale"]),
		"Animation": AnimChecks.missing_properties("Animation", ["loop_mode", "length"]),
		"Sprite2D": AnimChecks.missing_properties("Sprite2D", ["texture", "hframes", "vframes", "frame"]),
		"godot3_present": godot3_present}
	check("godot4-property-names-exist", missing.values().all(func(a: Array) -> bool: return a.is_empty()), missing)

	var player: Node = load(SCENE).instantiate()
	var aps := AnimChecks.players(player)
	var ap: AnimationPlayer = aps[0] if aps.size() == 1 else null
	var sprite: Sprite2D = player.get_node("Sprite2D")
	check("one-animation-player-physics-no-autoplay", ap != null and ap.get_parent() == player
		and ap.callback_mode_process == AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS and ap.autoplay == "",
		{"animation_players": aps.size(), "callback_mode_process": ap.callback_mode_process if ap else -1,
		"autoplay": ap.autoplay if ap else null})
	if ap == null:
		print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
		quit(1)
		return

	var names := Array(ap.get_animation_list())
	var absent := CLIP_TEXTURE.keys().filter(func(n: String) -> bool: return not n in names)
	check("every-clip-present", absent.is_empty() and names.size() == CLIP_TEXTURE.size(),
		{"clips": names, "missing": absent})

	var problems := []
	var wrong_tracks := {}
	var wrong_texture := {}
	var not_discrete := []
	var out_of_range := []
	for n: String in names:
		var anim := ap.get_animation(n)
		var paths := []
		for i in anim.get_track_count():
			paths.append(str(anim.track_get_path(i)))
			if anim.value_track_get_update_mode(i) != Animation.UPDATE_DISCRETE:
				not_discrete.append("%s %s" % [n, anim.track_get_path(i)])
		if paths != TRACKS:
			wrong_tracks[n] = paths
		var ti := AnimChecks.track(anim, "Sprite2D:texture")
		var tex: Texture2D = anim.track_get_key_value(ti, 0) if ti >= 0 else null
		if tex == null or tex.resource_path.get_file() != CLIP_TEXTURE.get(n, "?"):
			wrong_texture[n] = tex.resource_path if tex else null
		var hi := AnimChecks.track(anim, "Sprite2D:hframes")
		var fi := AnimChecks.track(anim, "Sprite2D:frame")
		if hi >= 0 and fi >= 0:
			var cells: int = anim.track_get_key_value(hi, 0) * sprite.vframes
			for k in anim.track_get_key_count(fi):
				var f: Variant = anim.track_get_key_value(fi, k)
				if typeof(f) != TYPE_INT or f < 0 or f >= cells:
					out_of_range.append({"clip": n, "frame": f, "cells": cells})
	problems = AnimChecks.track_problems(ap)
	check("every-track-resolves", problems.is_empty(), {"problems": problems})
	var key_problems := AnimChecks.key_problems(ap)
	check("every-key-in-range-increasing-and-typed", key_problems.is_empty(), {"problems": key_problems})
	check("each-clip-keys-texture-hframes-frame", wrong_tracks.is_empty(), {"expected": TRACKS, "wrong": wrong_tracks})
	check("each-clip-texture", wrong_texture.is_empty(), {"expected": CLIP_TEXTURE, "wrong": wrong_texture})
	check("every-track-discrete", not_discrete.is_empty(), {"not_discrete": not_discrete})
	check("every-frame-key-below-hframes-times-vframes", out_of_range.is_empty(),
		{"out_of_range": out_of_range, "vframes": sprite.vframes})

	var run_anim := ap.get_animation("run")
	var run_fi := AnimChecks.track(run_anim, "Sprite2D:frame")
	var frames := keys_of(run_anim, run_fi)
	var keys_ok := frames.size() == RUN_KEYS.size()
	for k in mini(frames.size(), RUN_KEYS.size()):
		keys_ok = keys_ok and absf(frames[k][0] - RUN_KEYS[k][0]) < EPS and frames[k][1] == RUN_KEYS[k][1]
	check("run-frame-keys-0-1-2-3-at-0-0.1-0.2-0.3", keys_ok, {"frame_keys": frames, "expected": RUN_KEYS})
	check("run-length-0.4-loop-linear", absf(run_anim.length - 0.4) < EPS and run_anim.loop_mode == Animation.LOOP_LINEAR,
		{"length": run_anim.length, "loop_mode": run_anim.loop_mode})
	var run_hi := AnimChecks.track(run_anim, "Sprite2D:hframes")
	check("run-sheet-hframes-4", keys_of(run_anim, run_hi) == [[0.0, 4]] and sprite.vframes == 1,
		{"hframes_keys": keys_of(run_anim, run_hi), "vframes": sprite.vframes})
	var gap: float = run_anim.length - frames.back()[0] if frames.size() > 0 else -1.0
	var interval: float = frames[1][0] - frames[0][0] if frames.size() > 1 else -1.0
	check("run-seam-no-duplicate-gap-equals-interval", frames.size() > 1 and frames.back()[1] != frames[0][1]
		and absf(gap - interval) < EPS, {"last_to_length_s": gap, "key_interval_s": interval})
	var loops := {}
	for n: String in names:
		loops[n] = ap.get_animation(n).loop_mode
	check("only-run-loops", loops.keys().all(func(n: String) -> bool:
		return loops[n] == (Animation.LOOP_LINEAR if n == "run" else Animation.LOOP_NONE)), {"loop_mode": loops})

	# The sheet: size; only the A2 mage sprites' colours; each cell's lowest row (feet on the ground, frame 4 airborne);
	# the imported texture equal to the PNG on every visible pixel (the import's fix_alpha_border only recolours
	# transparent pixels).
	var palette := {}
	for s_name: String in A2_SPRITES:
		var img := Image.load_from_file(ProjectSettings.globalize_path(MAGE + s_name + ".png"))
		img.convert(Image.FORMAT_RGBA8)
		for y in img.get_height():
			for x in img.get_width():
				var c := img.get_pixel(x, y)
				if c.a8 > 0:
					palette[c.to_html(false)] = true
	var sheet_raw := Image.load_from_file(ProjectSettings.globalize_path(SHEET))
	var sheet_img: Image = (load(SHEET) as Texture2D).get_image()
	for img: Image in [sheet_raw, sheet_img]:
		img.convert(Image.FORMAT_RGBA8)
	var off_palette := 0
	var visible_mism := 0
	var lowest := [-1, -1, -1, -1]
	for y in sheet_raw.get_height():
		for x in sheet_raw.get_width():
			var a := sheet_raw.get_pixel(x, y)
			var b := sheet_img.get_pixel(x, y)
			if a.a8 != b.a8 or (a.a8 > 0 and a != b):
				visible_mism += 1
			if a.a8 > 0:
				if not palette.has(a.to_html(false)):
					off_palette += 1
				lowest[x / 62] = maxi(lowest[x / 62], y)
	check("sheet-248x69-a2-palette-feet-rows-imported-equal", sheet_raw.get_size() == Vector2i(248, 69)
		and sheet_img.get_size() == Vector2i(248, 69) and off_palette == 0 and visible_mism == 0
		and lowest == CELL_LOWEST_ROW, {"size": sheet_img.get_size(), "cell": Vector2i(248 / 4, 69),
		"a2_palette_colours": palette.size(), "off_palette_px": off_palette, "imported_visible_mismatches": visible_mism,
		"lowest_row_per_cell": lowest, "expected": CELL_LOWEST_ROW})
	var sheet_params := params_of(SHEET + ".import")
	check("sheet-import-settings-match-run-frames", not sheet_params.is_empty()
		and sheet_params == params_of(CELLS[0] + ".import") and sheet_params == params_of(CELLS[1] + ".import"),
		{"has_params": not sheet_params.is_empty(), "compress_mode_0": "compress/mode=0" in sheet_params,
		"mipmaps_off": "mipmaps/generate=false" in sheet_params})

	player.free()
	print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
	quit(1 if failures else 0)
