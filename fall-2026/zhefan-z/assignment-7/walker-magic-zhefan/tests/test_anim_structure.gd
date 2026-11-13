extends SceneTree
## Assignment 7 state-machine structure test (CHANGE-BRIEF Objectives "one authority" and "two clocks", Tests):
## every Player.State and Wolf.State maps to an existing clip and play() uses it; autoplay empty; both AnimationPlayers
## on the physics callback; no game script writes a property a clip keys (a scan of the source); exactly one
## AnimationPlayer drives each sprite node; the read-only image tables equal the clips' texture keys.
## From fall-2026/zhefan-z/assignment-7/:
##   ./scripts/run-test.sh test_anim_structure.gd 60
## Prints one JSON line per check and "WALKER TESTS: N checks / F failures"; exit code 1 on any failure.
## The "play() uses it" checks call _set_state / _enter / fail / take_damage on scenes outside the game loop: this is a
## structure test, not a behaviour test (the pin is).

const AnimChecks := preload("res://tests/anim_checks.gd")
const OWNERS := {   # scene -> its script, the one game script that may start its clips
	"res://features/player/player.tscn": "res://features/player/player.gd",
	"res://features/wolf/wolf.tscn": "res://features/wolf/wolf.gd",
}
const GAME_DIRS := ["res://features", "res://game", "res://ui", "res://audio", "res://effects"]

var results: Array[Dictionary] = []
var failures := 0


func _initialize() -> void:
	call_deferred("run")


func check(id: String, passed: bool, observed: Dictionary) -> void:
	results.append({"id": id, "status": "PASS" if passed else "FAIL", "observed": observed})
	if not passed:
		failures += 1
	print(JSON.stringify(results.back()))


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


## Keyed [node path, property] pairs of every clip of `ap`.
func keyed(ap: AnimationPlayer) -> Array:
	var out := []
	for n in ap.get_animation_list():
		var anim := ap.get_animation(n)
		for i in anim.get_track_count():
			var p := anim.track_get_path(i)
			var pair := [str(p.get_concatenated_names()), str(p.get_subname(0))]
			if not pair in out:
				out.append(pair)
	return out


## Lines of `source` that write `prop` on the node at `node_path`: through `$path`, get_node("path"), or an @onready
## variable bound to either, by assignment, set(), set_deferred() or set_indexed().
func writes(source: String, node_path: String, prop: String) -> Array:
	var refs := ["\\$" + _esc(node_path), "\\$\"" + _esc(node_path) + "\"", "get_node\\(\\^?\"" + _esc(node_path) + "\"\\)"]
	var bind := RegEx.create_from_string("var\\s+(\\w+)\\s*(?::\\s*\\w+)?\\s*:?=\\s*(?:" + "|".join(refs) + ")\\s*$")
	for line in source.split("\n"):
		var m := bind.search(line.strip_edges())
		if m:
			refs.append(m.get_string(1))
	var target := "(?<![\\w.])(?:" + "|".join(refs) + ")"
	var patterns := [
		target + "\\." + prop + "(?:\\.\\w+)?\\s*(?:=|\\+=|-=|\\*=|/=)(?!=)",
		target + "\\.(?:set|set_deferred)\\(\\s*&?\"" + prop + "\"",
		target + "\\.set_indexed\\(\\s*\\^?\"" + prop,
	]
	var hits := []
	var lines := source.split("\n")
	for i in lines.size():
		var code := lines[i].split("#")[0]
		for pat: String in patterns:
			if RegEx.create_from_string(pat).search(code):
				hits.append("%d: %s" % [i + 1, lines[i].strip_edges()])
				break
	return hits


func _esc(s: String) -> String:
	return s.replace("/", "\\/").replace(".", "\\.")


func run() -> void:
	# --- Clips for every state, and play() starts them (Player) ---
	var player: Player = load("res://features/player/player.tscn").instantiate()
	root.add_child(player)
	player.set_physics_process(false)
	var pap: AnimationPlayer = player.get_node("AnimationPlayer")
	var p_missing := []
	var p_played := {}
	for s: int in Player.State.values():
		var clip: StringName = Player.CLIPS.get(s, &"")
		if not pap.has_animation(clip):
			p_missing.append(Player.State.keys()[s])
	for extra: StringName in [&"fail_pit"]:
		if not pap.has_animation(extra):
			p_missing.append(str(extra))
	check("every-player-state-has-a-clip", p_missing.is_empty() and Player.CLIPS.size() == Player.State.size(),
		{"clips": Player.CLIPS.values(), "missing": p_missing})
	for s: int in [Player.State.IDLE, Player.State.RUN, Player.State.RISE, Player.State.FALL, Player.State.CAST,
			Player.State.HURT, Player.State.WIN]:
		player._set_state(s)
		p_played[Player.State.keys()[s]] = [str(pap.assigned_animation), player.sprite.texture == Player.TEXTURES[s]]
	player.fail("structure", true)
	p_played["FAIL (pit)"] = [str(pap.assigned_animation), player.sprite.texture == Player.TEXTURES[Player.State.FALL]]
	var player2: Player = load("res://features/player/player.tscn").instantiate()
	root.add_child(player2)
	player2.set_physics_process(false)
	player2.fail("structure")
	p_played["FAIL"] = [str(player2.anim.assigned_animation), player2.sprite.texture == Player.TEXTURES[Player.State.FAIL]]
	var p_ok := p_played.keys().all(func(k: String) -> bool:
		var want: String = "fail_pit" if k == "FAIL (pit)" else str(Player.CLIPS[Player.State[k]])
		return p_played[k][0] == want and p_played[k][1])
	check("player-set-state-and-fail-play-the-state-clip", p_ok, {"state_to_clip_and_image_ok": p_played})

	# RUN re-entry restarts the cycle at frame 0.
	player2.queue_free()
	var player3: Player = load("res://features/player/player.tscn").instantiate()
	root.add_child(player3)
	player3.set_physics_process(false)
	player3._set_state(Player.State.RUN)
	player3.anim.seek(0.2, true)
	var mid_frame := player3.sprite.frame
	player3._set_state(Player.State.RUN)
	var kept := player3.anim.current_animation_position
	player3._set_state(Player.State.RISE)
	player3._set_state(Player.State.RUN)
	# The frame the run clip itself keys at 0.2 s (not a hardcoded value), so this holds for any run cycle.
	var run_anim := player3.anim.get_animation("run")
	var keyed_mid: int = run_anim.value_track_interpolate(AnimChecks.track(run_anim, "Sprite2D:frame"), 0.2)
	check("run-reentry-restarts-at-frame-0", mid_frame == keyed_mid and mid_frame != 0 and kept > 0.19
		and player3.anim.current_animation_position == 0.0 and player3.sprite.frame == 0,
		{"frame_at_0.2s": mid_frame, "keyed_frame_at_0.2s": keyed_mid, "position_while_still_running": kept,
		"position_after_reentry": player3.anim.current_animation_position, "frame_after_reentry": player3.sprite.frame})

	# --- Wolf ---
	var wolf: Wolf = load("res://features/wolf/wolf.tscn").instantiate()
	root.add_child(wolf)
	wolf.set_physics_process(false)
	var wap: AnimationPlayer = wolf.get_node("AnimationPlayer")
	var w_missing := []
	for s: int in Wolf.State.values():
		if not wap.has_animation(Wolf.CLIPS.get(s, &"")):
			w_missing.append(Wolf.State.keys()[s])
	check("every-wolf-state-has-a-clip", w_missing.is_empty() and Wolf.CLIPS.size() == Wolf.State.size(),
		{"clips": Wolf.CLIPS, "missing": w_missing})
	var w_played := {"ready": str(wap.assigned_animation)}
	wolf._enter(Wolf.State.GROWL)
	wap.seek(0.3, true)
	w_played["GROWL"] = str(wap.assigned_animation)
	wolf._enter(Wolf.State.LUNGE)
	var after_lunge := wap.current_animation_position
	wolf._enter(Wolf.State.RECOVER)
	var after_recover := wap.current_animation_position
	w_played["LUNGE"] = str(wap.assigned_animation)
	wolf._enter(Wolf.State.PATROL)
	w_played["PATROL"] = str(wap.assigned_animation)
	var patrol_tex := wolf.sprite.texture == Wolf.TEX_RUN
	wolf.hp = 1
	wolf.take_damage(1)
	w_played["DEAD"] = str(wap.assigned_animation)
	check("wolf-enter-and-death-play-the-state-clip", w_played == {"ready": "patrol", "GROWL": "lunge", "LUNGE": "lunge",
		"PATROL": "patrol", "DEAD": "dead"} and absf(after_lunge - 0.3) < 1e-6 and absf(after_recover - 0.3) < 1e-6
		and patrol_tex and wolf.sprite.texture == Wolf.TEX_DOWN, {"clips": w_played,
		"lunge_position_left_running_on_LUNGE_and_RECOVER": [after_lunge, after_recover]})
	var facing_node: Node2D = wolf.get_node("Facing")
	var fresh_wolf: Node = load("res://features/wolf/wolf.tscn").instantiate()
	var scene_material: Material = fresh_wolf.get_node("Sprite2D").material
	fresh_wolf.free()
	check("wolf-flash-material-shared-with-rig", facing_node.material == wolf.sprite.material
		and facing_node.material != scene_material,
		{"facing_uses_the_duplicated_material": facing_node.material == wolf.sprite.material,
		"duplicated_from_the_scene_material": facing_node.material != scene_material})
	var f_seen := []
	for dir: int in [1, -1]:
		wolf.facing = dir
		wolf._apply_facing()
		f_seen.append([facing_node.scale.x, wolf.sprite.flip_h])
	check("wolf-facing-sets-facing-scale-and-flip-h", f_seen == [[1.0, false], [-1.0, true]], {"scale_x_and_flip_h": f_seen})

	# --- Both AnimationPlayers: physics callback, no autoplay; read-only image tables equal the clips' texture keys ---
	var cfg := {}
	for ap: AnimationPlayer in [pap, wap]:
		cfg[str(ap.get_parent().name)] = {"callback": ap.callback_mode_process, "autoplay": ap.autoplay}
	check("both-players-physics-callback-no-autoplay", cfg.values().all(func(c: Dictionary) -> bool:
		return c.callback == AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS and c.autoplay == ""), cfg)
	var mirror := {}
	for s: int in Player.State.values():
		var anim := pap.get_animation(Player.CLIPS[s])
		var key: Texture2D = anim.track_get_key_value(AnimChecks.track(anim, "Sprite2D:texture"), 0)
		if key != Player.TEXTURES[s] and s != Player.State.FAIL:
			mirror[Player.State.keys()[s]] = key.resource_path
	var fail_key: Texture2D = pap.get_animation("fail").track_get_key_value(0, 0)
	var pit_key: Texture2D = pap.get_animation("fail_pit").track_get_key_value(0, 0)
	for pair: Array in [["patrol", Wolf.TEX_RUN], ["lunge", Wolf.TEX_LUNGE], ["dead", Wolf.TEX_DOWN]]:
		var anim := wap.get_animation(pair[0])
		var i := AnimChecks.track(anim, "Sprite2D:texture")
		if i < 0 or anim.track_get_key_value(i, 0) != pair[1]:
			mirror[pair[0]] = "texture key differs from Wolf.TEX_*"
	check("image-tables-equal-clip-texture-keys", mirror.is_empty() and fail_key == Player.TEXTURES[Player.State.FAIL]
		and pit_key == Player.TEXTURES[Player.State.FALL], {"mismatches": mirror})

	# --- No game script writes a property a clip keys ---
	var scanned := []
	for dir: String in GAME_DIRS:
		scanned.append_array(gd_files(dir))
	var offenders := {}
	for scene: String in OWNERS:
		var inst: Node = load(scene).instantiate()
		var pairs := keyed(inst.get_node("AnimationPlayer"))
		inst.free()
		for path: String in scanned:
			var src := FileAccess.get_file_as_string(path)
			for pair: Array in pairs:
				# Inside the owning script, refs are relative to its root. Elsewhere, a write reaches this scene's sprite
				# through its `sprite` member (e.g. `wolf.sprite.texture = ...`).
				var hits := writes(src, pair[0], pair[1]) if path == OWNERS[scene] else []
				if path != OWNERS[scene] and pair[0] == "Sprite2D":
					var ext := RegEx.create_from_string("\\w\\.sprite\\." + pair[1] + "\\s*(?:=|\\+=|-=)(?!=)")
					var lines := src.split("\n")
					for i in lines.size():
						if ext.search(lines[i].split("#")[0]):
							hits.append("%d: %s" % [i + 1, lines[i].strip_edges()])
				for h in hits:
					offenders["%s %s:%s" % [path, pair[0], pair[1]]] = h
	# The scanner must find a planted write, or a broken scanner would pass.
	var planted := writes("@onready var spr: Sprite2D = $Sprite2D\nfunc f():\n\tspr.texture = null\n\t$Facing/Rig.set_deferred(\"scale\", 1)",
		"Sprite2D", "texture").size() == 1 and writes("\t$Facing/Rig.set_deferred(\"scale\", 1)", "Facing/Rig", "scale").size() == 1
	check("no-game-script-writes-a-keyed-property", offenders.is_empty() and planted and scanned.size() > 5,
		{"scripts_scanned": scanned.size(), "offenders": offenders, "scanner_finds_planted_writes": planted})

	# --- Exactly one AnimationPlayer drives each sprite node, across the main scene ---
	var main: Node = load("res://game/main.tscn").instantiate()
	var drivers := {}
	for ap: AnimationPlayer in AnimChecks.players(main):
		var ap_root := ap.get_node(ap.root_node)
		for pair: Array in keyed(ap):
			var target := ap_root.get_node_or_null(NodePath(pair[0]))
			if target:
				for sp in _sprites_under(target):
					drivers[str(main.get_path_to(sp))] = drivers.get(str(main.get_path_to(sp)), {})
					drivers[str(main.get_path_to(sp))][str(main.get_path_to(ap))] = true
	var sprites := _sprites_under(main).filter(func(s: Node) -> bool:
		return s.get_parent().name in ["Player", "Wolf", "RearPivot", "FrontPivot"])
	var counts := {}
	for sp in sprites:
		counts[str(main.get_path_to(sp))] = drivers.get(str(main.get_path_to(sp)), {}).size()
	var animated := _sprites_under(main).filter(func(s: Node) -> bool: return s is AnimatedSprite2D)
	check("one-animation-player-per-sprite", counts.size() == 4 and counts.values().all(func(c: int) -> bool: return c == 1)
		and animated.is_empty(), {"drivers_per_sprite": counts, "animated_sprite2d": animated.size()})
	main.free()

	player.queue_free()
	player3.queue_free()
	wolf.queue_free()
	await process_frame
	print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
	quit(1 if failures else 0)


func _sprites_under(n: Node) -> Array:
	var out := []
	if n is Sprite2D or n is AnimatedSprite2D:
		out.append(n)
	for c in n.get_children():
		out.append_array(_sprites_under(c))
	return out
