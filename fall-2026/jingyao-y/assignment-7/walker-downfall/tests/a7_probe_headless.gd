extends SceneTree

## A7 Step 1 review probe (agent, 2026-11-22). Confirms on Godot 4.7.2,
## headless, the facts CLAUDE.md states before they are added:
##  1. every Godot 4 animation name CLAUDE.md lists exists (and the Godot 3
##     names it forbids do not);
##  2. a headless run advances an AnimationPlayer clip and reads its
##     structure, and the renderer is a dummy (draws nothing);
##  3. key times are 32-bit floats after a .tres round trip (== fails,
##     a half-frame tolerance passes);
##  4. value_track_get_update_mode on a non-value track errors and answers
##     UPDATE_CONTINUOUS;
##  5. ANIMATION_CALLBACK_MODE_PROCESS_MANUAL clips move only on advance().
## Run: ./scripts/run-test.sh a7_probe_headless.gd 60
## Fact 4 prints an engine ERROR line on purpose; the wrapper only fails on
## SHADER/SCRIPT ERROR or Failed loading resource, so it is not a failure.

var failures := 0

func check(label: String, ok: bool, detail: String = "") -> void:
	print("%s  %s%s" % ["PASS" if ok else "FAIL", label, ("  (" + detail + ")") if detail != "" else ""])
	if not ok: failures += 1

func has_prop(cls: String, prop: String) -> bool:
	for p in ClassDB.class_get_property_list(cls):
		if p.name == prop: return true
	return false

func _initialize() -> void:
	print("engine ", Engine.get_version_info().string)
	print("adapter '%s' video '%s'" % [RenderingServer.get_video_adapter_name(), RenderingServer.get_current_rendering_method()])
	check("renderer is a dummy headless (adapter name empty)", RenderingServer.get_video_adapter_name() == "")

	# 1. Names.
	for p in ["loop_mode", "step", "length"]: check("Animation.%s exists" % p, has_prop("Animation", p))
	check("Animation.loop (Godot 3 boolean) absent", not has_prop("Animation", "loop"))
	for p in ["speed_scale", "autoplay", "current_animation", "current_animation_position"]: check("AnimationPlayer.%s exists" % p, has_prop("AnimationPlayer", p))
	for p in ["root_node", "callback_mode_process"]: check("AnimationMixer.%s exists" % p, has_prop("AnimationMixer", p))
	check("AnimationPlayer.playback_speed (Godot 3) absent", not has_prop("AnimationPlayer", "playback_speed"))
	check("AnimationPlayer.playback_process_mode (Godot 3) absent", not has_prop("AnimationPlayer", "playback_process_mode"))
	check("class AnimatedSprite (Godot 3) absent", not ClassDB.class_exists("AnimatedSprite"))
	check("class Spatial (Godot 3) absent", not ClassDB.class_exists("Spatial"))
	for c in ["AnimationLibrary", "AnimatedSprite3D", "ViewportTexture", "SubViewport", "Sprite3D", "Node2D"]: check("class %s exists" % c, ClassDB.class_exists(c))
	for p in ["hframes", "vframes", "frame", "frame_coords"]: check("Sprite3D.%s exists" % p, has_prop("Sprite3D", p))
	for p in ["transparent_bg", "render_target_update_mode"]: check("%s.%s exists" % ["Viewport" if p == "transparent_bg" else "SubViewport", p], has_prop("Viewport" if p == "transparent_bg" else "SubViewport", p))
	check("ANIMATION_CALLBACK_MODE_PROCESS_IDLE = %d" % AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_IDLE, true)
	check("ANIMATION_CALLBACK_MODE_PROCESS_MANUAL = %d" % AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL, true)
	for m in ["advance", "seek", "play", "stop", "get_animation_list"]: check("AnimationPlayer.%s() exists" % m, ClassDB.class_has_method("AnimationPlayer", m) or ClassDB.class_has_method("AnimationMixer", m))
	for m in ["value_track_set_update_mode", "value_track_get_update_mode", "track_set_interpolation_type", "track_get_key_time"]: check("Animation.%s() exists" % m, ClassDB.class_has_method("Animation", m))
	check("Animation.step default is 1/30", is_equal_approx(Animation.new().step, 1.0 / 30.0), str(Animation.new().step))

	# 3. 32-bit key times after a .tres round trip.
	var clip := Animation.new()
	clip.length = 16.0 / 12.0
	var t := clip.add_track(Animation.TYPE_VALUE)
	clip.track_set_path(t, NodePath(".:frame"))
	var want := [0.0, 4.0 / 12.0, 8.0 / 12.0, 12.0 / 12.0]
	for i in range(want.size()): clip.track_insert_key(t, want[i], i)
	var path := "user://a7_probe_clip.tres"
	check("save .tres", ResourceSaver.save(clip, path) == OK)
	var back := ResourceLoader.load(path, "", ResourceLoader.CACHE_MODE_IGNORE) as Animation
	var exact := 0
	var near := 0
	for i in range(want.size()):
		var got: float = back.track_get_key_time(t, i)
		print("  key %d: wanted %.17f got %.17f" % [i, want[i], got])
		if got == want[i]: exact += 1
		if absf(got - want[i]) < 0.5 / 12.0: near += 1
	check("after round trip, at least one key time != its float64 value (32-bit storage)", exact < want.size(), "%d of %d equal with ==" % [exact, want.size()])
	check("every key time within half a frame period", near == want.size())

	# 4. Update mode on a non-value track.
	var pos := clip.add_track(Animation.TYPE_POSITION_3D)
	clip.track_set_path(pos, NodePath("Skeleton3D:Hips"))
	print("  (an engine ERROR line may follow: expected, from asking a position track its update mode)")
	var mode := clip.value_track_get_update_mode(pos)
	check("value_track_get_update_mode on a POSITION_3D track answers UPDATE_CONTINUOUS", mode == Animation.UPDATE_CONTINUOUS, str(mode))

	# 2 and 5 need the tree.
	_run_players.call_deferred()

func _run_players() -> void:
	var sprite := Sprite3D.new()
	sprite.hframes = 4
	root.add_child(sprite)
	var clip := Animation.new()
	clip.length = 16.0 / 12.0
	clip.step = 1.0 / 12.0
	clip.loop_mode = Animation.LOOP_LINEAR
	var t := clip.add_track(Animation.TYPE_VALUE)
	clip.track_set_path(t, NodePath(".:frame"))
	clip.value_track_set_update_mode(t, Animation.UPDATE_DISCRETE)
	for i in range(4): clip.track_insert_key(t, i * 4.0 / 12.0, i)
	var lib := AnimationLibrary.new()
	lib.add_animation(&"idle", clip)
	var idle_player := AnimationPlayer.new()
	sprite.add_child(idle_player)
	idle_player.root_node = NodePath("..")
	idle_player.add_animation_library(&"", lib)
	idle_player.play(&"idle")

	var manual := AnimationPlayer.new()
	var sprite2 := Sprite3D.new()
	sprite2.hframes = 4
	root.add_child(sprite2)
	sprite2.add_child(manual)
	manual.root_node = NodePath("..")
	manual.add_animation_library(&"", lib)
	manual.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	manual.play(&"idle")

	for i in range(30): await process_frame
	check("headless: an IDLE-mode clip advances (position > 0 after 30 frames)", idle_player.current_animation_position > 0.3, "%.4f" % idle_player.current_animation_position)
	check("headless: the discrete frame track wrote a cell (frame %d)" % sprite.frame, sprite.frame >= 1 and sprite.frame <= 3)
	check("MANUAL mode: no movement without advance()", is_zero_approx(manual.current_animation_position), "%.4f" % manual.current_animation_position)
	manual.advance(0.5)
	check("MANUAL mode: advance(0.5) moves to 0.5 and keys frame 1", is_equal_approx(manual.current_animation_position, 0.5) and sprite2.frame == 1, "%.4f, frame %d" % [manual.current_animation_position, sprite2.frame])

	print("a7_probe_headless: %s" % ("PASS" if failures == 0 else "%d FAILED" % failures))
	quit(1 if failures > 0 else 0)
