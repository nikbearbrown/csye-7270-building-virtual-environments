extends SceneTree
## Automated check: one sound per event, including rapid repeats and held input.
##
## Run from the godot/ folder:
##   godot --headless --path . --script tests/test_sound_triggers.gd
##
## Exits 0 if every assertion passes, 1 otherwise. Asserts are never weakened
## to obtain a green result; a failure here is a real failure.

var _failures := 0
var _checks := 0


func _init() -> void:
	await process_frame
	var scene = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(scene)
	for i in 5: await process_frame

	var audio = scene.get_node("Audio")
	var meters = scene.get_node("Meters")
	var contact = scene.get_node("MusicBox")

	print("\n--- HOUSEGHOST sound trigger check ---")

	# 1. One flip, one flip sound.
	scene.flip()
	await _settle()
	_expect(audio.counts["flip"] == 1, "one flip produces exactly one flip sound", audio.counts["flip"])

	# 2. Mashing the flip key during the turn must not stack sounds. The guard
	#    lives in world.gd (_flipping), so the extra calls are ignored outright.
	var before: int = audio.counts["flip"]
	for i in 12:
		scene.flip()
	await _settle()
	_expect(audio.counts["flip"] == before + 1,
		"12 flip calls during a turn still produce one sound", audio.counts["flip"] - before)

	# 3. A resolved contact fires exactly one contact sound, and the cooldown
	#    stops a second resolve landing immediately after.
	if not scene.is_inverted:
		scene.flip()
		await _settle()
	var contacts_before: int = audio.counts["contact"]
	contact._player_inside = true
	contact._resolve(false)
	contact._resolve(false)          # blocked: cooldown is running
	await _settle(0.1)
	_expect(audio.counts["contact"] == contacts_before + 1,
		"two resolves inside the cooldown produce one contact sound",
		audio.counts["contact"] - contacts_before)

	# 4. Each torn day fires exactly one frost sound.
	var frost_before: int = audio.counts["frost"]
	var days_before: int = meters.days_left
	meters.spend(2, 0)
	await _settle(0.1)
	var days_lost: int = days_before - meters.days_left
	_expect(audio.counts["frost"] - frost_before == days_lost,
		"one frost sound per day torn", "%d sounds for %d days" % [audio.counts["frost"] - frost_before, days_lost])

	# 5. Muting must not change the counts: the game still did the thing, it is
	#    only inaudible. This is the "sound never decides state" rule.
	audio.set_sfx_muted(true)
	var muted_before: int = audio.counts["flip"]
	scene.flip()
	await _settle()
	_expect(audio.counts["flip"] == muted_before + 1,
		"muted SFX still counts the event (state is unchanged by audio)",
		audio.counts["flip"] - muted_before)

	# 6. One jump press, one jump sound and one landing sound. The key is held
	#    for the whole arc, so a retrigger mid-air would show up here.
	audio.set_sfx_muted(false)
	if scene.is_inverted:
		scene.flip()
		await _settle()
	var j0: int = audio.counts["jump"]
	var l0: int = audio.counts["land"]
	Input.action_press("jump")
	await _settle(1.4)
	Input.action_release("jump")
	await _settle(0.4)
	_expect(audio.counts["jump"] == j0 + 1,
		"a held jump fires one jump sound", audio.counts["jump"] - j0)
	_expect(audio.counts["land"] == l0 + 1,
		"landing from that jump fires one land sound", audio.counts["land"] - l0)


	print("--- %d checks, %d failed ---\n" % [_checks, _failures])
	quit(1 if _failures > 0 else 0)


## Headless frames are not real time, so waits must be wall-clock: a flip tween
## lasts 0.6 s regardless of how fast the frames tick.
func _settle(seconds: float = 0.9) -> void:
	await create_timer(seconds).timeout


func _expect(condition: bool, what: String, got = null) -> void:
	_checks += 1
	if condition:
		print("  PASS  ", what)
	else:
		_failures += 1
		printerr("  FAIL  %s (got: %s)" % [what, str(got)])
