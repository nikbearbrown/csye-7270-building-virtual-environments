extends SceneTree
# Run headlessly:
#   godot --headless --path godot --script res://tests/test_hit_audio.gd

var _all_passed := true


func _check(name: String, result: bool) -> void:
	if result:
		print("PASS ", name)
	else:
		print("FAIL ", name)
		_all_passed = false
		quit(1)


# Drain every available frame from an AudioEffectCapture and return the peak
# amplitude in dBFS. Returns -200.0 if no frames were captured.
func _peak_db(cap: AudioEffectCapture) -> float:
	var n := cap.get_frames_available()
	if n == 0:
		return -200.0
	var buf := cap.get_buffer(n)   # PackedVector2Array; removes frames from ring
	var peak := 0.0
	for v in buf:
		var ax := absf(v.x)
		var ay := absf(v.y)
		if ax > peak:
			peak = ax
		if ay > peak:
			peak = ay
	if peak <= 0.0:
		return -200.0
	return 20.0 * log(peak) / log(10.0)


func _initialize() -> void:
	_run.call_deferred()


func _run() -> void:
	# Scene is untyped like test_live_restart.gd — using the NoteManager class
	# annotation forces early script compilation before autoloads are ready.
	var scene = load("res://scenes/main/main.tscn").instantiate()
	root.add_child(scene)
	current_scene = scene
	await process_frame
	await process_frame

	var player:    AudioStreamPlayer = scene.get_node("Player")
	var metronome: AudioStreamPlayer = scene.get_node("Metronome")
	var hit_sound: AudioStreamPlayer = scene.get_node("HitSound")
	var notes = scene.get_node("Notes")   # NoteManager — untyped to avoid early compile

	# ── 1. Bus topology ──────────────────────────────────────────────────────
	var master_idx := AudioServer.get_bus_index("Master")
	var music_idx  := AudioServer.get_bus_index("Music")
	var sfx_idx    := AudioServer.get_bus_index("SFX")

	_check("bus_master_exists",    master_idx >= 0)
	_check("bus_music_exists",     music_idx  >= 0)
	_check("bus_sfx_exists",       sfx_idx    >= 0)
	_check("music_sends_to_master",
			music_idx >= 0 and AudioServer.get_bus_send(music_idx) == &"Master")
	_check("sfx_sends_to_master",
			sfx_idx   >= 0 and AudioServer.get_bus_send(sfx_idx)   == &"Master")

	# ── 2. Node bus routing ──────────────────────────────────────────────────
	_check("player_on_music_bus",   player.bus    == &"Music")
	_check("metronome_on_sfx_bus",  metronome.bus == &"SFX")
	_check("hitsound_on_sfx_bus",   hit_sound.bus == &"SFX")

	# ── 3. note_hit signal → HitSound for hits, silent for misses ───────────
	# The signal is connected synchronously in the scene. Calling emit() fires
	# _on_note_hit immediately, which calls HitSound.play(). Snapshot playing
	# before any await: Dummy mixes eight 512-frame steps in one 4096-frame
	# burst, so a 60 ms click can finish between two rendered frames.

	notes.note_hit.emit(0.0, Enums.HitType.PERFECT, 0.0)
	var perfect_playing := hit_sound.playing
	_check("hitsound_plays_on_perfect", perfect_playing)
	await process_frame
	hit_sound.stop()
	await process_frame

	notes.note_hit.emit(0.0, Enums.HitType.GOOD_EARLY, -0.05)
	var good_early_playing := hit_sound.playing
	_check("hitsound_plays_on_good_early", good_early_playing)
	await process_frame
	hit_sound.stop()
	await process_frame

	notes.note_hit.emit(0.0, Enums.HitType.GOOD_LATE, 0.05)
	var good_late_playing := hit_sound.playing
	_check("hitsound_plays_on_good_late", good_late_playing)
	await process_frame
	hit_sound.stop()
	await process_frame

	notes.note_hit.emit(0.0, Enums.HitType.MISS_EARLY, -0.2)
	var miss_early_playing := hit_sound.playing
	_check("hitsound_silent_on_miss_early", not miss_early_playing)
	await process_frame

	notes.note_hit.emit(0.0, Enums.HitType.MISS_LATE, 0.2)
	var miss_late_playing := hit_sound.playing
	_check("hitsound_silent_on_miss_late", not miss_late_playing)
	await process_frame

	# ── 4. AudioEffectCapture peak checks ────────────────────────────────────
	# The Dummy driver mixes audio in real time on a background thread; the
	# bus peak meter (get_bus_peak_volume_left_db) exposes only the most-recent
	# ~11.6 ms mix block and consistently misses a 60 ms clip unless you poll
	# at the exact right moment. AudioEffectCapture accumulates samples into a
	# ring buffer across every mix block, so it reliably records short clips.
	#
	# A capture effect on a bus reads audio BEFORE that bus's mute/volume fader.
	# A capture on Master reads what each child bus actually sends through.
	#
	# Setup (in test only — not written to default_bus_layout.tres):
	#   • AudioEffectCapture on SFX   → sees HitSound before SFX mute/volume
	#   • AudioEffectCapture on Master → sees what SFX bus sends after its mute
	#   • Music bus is muted so Master carries only SFX during measurement.
	#   • Metronome is disabled so SFX carries only HitSound.

	hit_sound.stop()
	await process_frame

	var sfx_cap    := AudioEffectCapture.new()
	var master_cap := AudioEffectCapture.new()
	sfx_cap.buffer_length    = 0.5   # 500 ms ring — plenty for a 60 ms clip
	master_cap.buffer_length = 0.5

	AudioServer.add_bus_effect(sfx_idx,    sfx_cap)
	var sfx_eff_idx    := AudioServer.get_bus_effect_count(sfx_idx)    - 1
	AudioServer.add_bus_effect(master_idx, master_cap)
	var master_eff_idx := AudioServer.get_bus_effect_count(master_idx) - 1

	AudioServer.set_bus_mute(music_idx, true)
	# GlobalSettings is an autoload — access via path to avoid compile-time
	# identifier failure when the script runs in --script mode.
	var _gs = root.get_node("GlobalSettings")
	var _orig_metronome: bool = _gs.enable_metronome
	_gs.enable_metronome = false

	# ── 4a. SFX unmuted: both captures should peak above -12 dBFS ───────────
	sfx_cap.clear_buffer()
	master_cap.clear_buffer()
	notes.note_hit.emit(0.0, Enums.HitType.PERFECT, 0.0)
	# Wait ≥ 200 ms wall time, spanning more than two 4096-frame Dummy
	# driver bursts, so the capture has time to receive the entire 60 ms clip.
	var t0 := Time.get_ticks_msec()
	while Time.get_ticks_msec() - t0 < 200:
		await process_frame
	hit_sound.stop()

	var sfx_db_hi    := _peak_db(sfx_cap)
	var master_db_hi := _peak_db(master_cap)
	_check("peak_sfx_capture_after_perfect",    sfx_db_hi    > -12.0)
	_check("peak_master_capture_after_perfect", master_db_hi > -12.0)

	# ── 4b. SFX muted: SFX capture still hears; Master goes silent ───────────
	# SFX capture is before the SFX mute fader → still sees the clip.
	# Master capture is after the SFX bus output → SFX is silent, so Master
	# carries only Music (also muted) → stays below -60 dBFS.
	sfx_cap.clear_buffer()
	master_cap.clear_buffer()
	AudioServer.set_bus_mute(sfx_idx, true)
	notes.note_hit.emit(0.0, Enums.HitType.PERFECT, 0.0)
	t0 = Time.get_ticks_msec()
	while Time.get_ticks_msec() - t0 < 200:
		await process_frame
	hit_sound.stop()

	var sfx_db_muted    := _peak_db(sfx_cap)
	var master_db_muted := _peak_db(master_cap)
	_check("peak_sfx_capture_still_hears_when_bus_muted", sfx_db_muted    > -12.0)
	_check("peak_master_capture_silent_when_bus_muted",   master_db_muted < -60.0)

	# Restore bus state, metronome setting, and remove capture effects.
	AudioServer.set_bus_mute(sfx_idx,   false)
	AudioServer.set_bus_mute(music_idx, false)
	_gs.enable_metronome = _orig_metronome
	# Remove in reverse-add order so indices stay stable.
	AudioServer.remove_bus_effect(master_idx, master_eff_idx)
	AudioServer.remove_bus_effect(sfx_idx,    sfx_eff_idx)

	# ── 5. Real Space key → Perfect hit → HitSound starts ───────────────────
	# Mirror test_live_restart.gd: wait TWO frames after key press before
	# releasing and checking state. NoteManager processes input at most one
	# frame after parse_input_event, so two frames give ample margin.
	var deadline := Time.get_ticks_msec() + 30000
	var hit_sent := false
	while Time.get_ticks_msec() < deadline:
		await process_frame
		if not notes._notes.is_empty() and \
				abs(notes._get_note_delta(notes._notes[0])) < 0.015:
			var ev := InputEventKey.new()
			ev.physical_keycode = KEY_SPACE
			ev.pressed = true
			Input.parse_input_event(ev)
			hit_sent = true
			await process_frame
			await process_frame
			ev = InputEventKey.new()
			ev.physical_keycode = KEY_SPACE
			ev.pressed = false
			Input.parse_input_event(ev)
			break

	# HitSound plays for 60 ms; at max 1000 FPS two frames ≤ 2 ms, so the
	# clip is still in flight when we check here.
	var hs_after_space := hit_sound.playing
	_check("space_hit_scores_perfect",
			hit_sent and notes._play_stats.perfect_count >= 1)
	_check("space_hit_starts_hitsound",
			hit_sent and hs_after_space)

	# ── 6. R reloads scene; HitSound silent; song position < 1 s ────────────
	var ev_r := InputEventKey.new()
	ev_r.physical_keycode = KEY_R
	ev_r.pressed = true
	Input.parse_input_event(ev_r)
	await process_frame
	await process_frame
	await process_frame
	ev_r = InputEventKey.new()
	ev_r.physical_keycode = KEY_R
	ev_r.pressed = false
	Input.parse_input_event(ev_r)

	scene     = current_scene
	hit_sound = scene.get_node("HitSound")
	player    = scene.get_node("Player")

	_check("restart_hitsound_silent",       not hit_sound.playing)
	_check("restart_song_position_under_1s", player.get_playback_position() < 1.0)

	# ── 7. P pauses tree; song freezes while paused and resumes afterward ─
	var ev_p := InputEventKey.new()
	ev_p.physical_keycode = KEY_P
	ev_p.pressed = true
	Input.parse_input_event(ev_p)
	await process_frame   # PauseHandler._process fires; tree is now paused
	await process_frame   # Player received NOTIFICATION_PAUSED; stream frozen
	ev_p = InputEventKey.new()
	ev_p.physical_keycode = KEY_P
	ev_p.pressed = false
	Input.parse_input_event(ev_p)

	# SceneTree.paused is the property on self (we extend SceneTree).
	_check("pause_tree_paused", self.paused)
	var song_pos_paused_start := player.get_playback_position()
	await create_timer(0.3).timeout
	var song_pos_paused_end := player.get_playback_position()
	_check("song_position_frozen_while_paused",
			song_pos_paused_end - song_pos_paused_start <= 0.02)

	# Unpause, then verify the long song advances again over wall-clock time.
	var ev_p2 := InputEventKey.new()
	ev_p2.physical_keycode = KEY_P
	ev_p2.pressed = true
	Input.parse_input_event(ev_p2)
	await process_frame
	await process_frame
	_check("pause_tree_resumed", not self.paused)
	var song_pos_resumed_start := player.get_playback_position()
	await create_timer(0.3).timeout
	var song_pos_resumed_end := player.get_playback_position()
	_check("song_position_advances_after_resume",
			song_pos_resumed_end - song_pos_resumed_start > 0.02)
	ev_p2 = InputEventKey.new()
	ev_p2.physical_keycode = KEY_P
	ev_p2.pressed = false
	Input.parse_input_event(ev_p2)
	await process_frame

	# ── teardown (FRICTIONAL.md: stop audio then drain 0.2 s before free) ───
	scene.get_node("Conductor").stop()
	hit_sound = scene.get_node("HitSound")
	hit_sound.stop()
	await create_timer(0.2).timeout
	await process_frame
	scene.queue_free()
	await process_frame
	await process_frame

	quit(0 if _all_passed else 1)

# ── Headless / Dummy driver note ──────────────────────────────────────────────
# Godot --headless selects the Dummy audio driver. The Dummy driver DOES mix
# audio in real time on a background thread. It mixes 4096-frame buffers at
# 44100 Hz (about one burst every 93 ms), with eight 512-frame AudioServer mix
# steps run back to back in each burst. This means:
#
#   CAN establish (verified headlessly in this test):
#     • Bus topology (AudioServer.get_bus_index, get_bus_send) — structural.
#     • Node bus assignments (AudioStreamPlayer.bus property).
#     • AudioStreamPlayer.playing state — the engine's active flag is set by
#       play(), but must be read synchronously because a 60 ms clip can start
#       and finish within one burst between two rendered frames.
#     • Actual audio content via AudioEffectCapture: the Dummy driver runs the
#       full mixing pipeline, and AudioEffectCapture accumulates samples across
#       every mix block. A 60 ms clip reliably appears in the ring buffer within
#       200 ms of wall time. This confirms the click is mixed at the right
#       amplitude on the SFX bus and that muting SFX silences Master.
#     • Score and UI state from real key-event input (same as test_live_restart).
#     • Scene-reload and pause-tree behaviour.
#     • Long-song playback position freezes while paused and advances after
#       resuming.
#
#   CANNOT establish:
#     • That the click is audible on a real audio output device.
#     • AudioServer.get_bus_peak_volume_left_db headlessly: the meter exposes
#       only the last 512-frame step of the latest burst. A 60 ms clip can be
#       fully mixed without ever appearing in a frame-based meter check. The
#       capture-based checks in section 4 replace this meter.
#     • Loudness or distortion as perceived by a listener.
#     • Correct behaviour across real audio drivers (CoreAudio, ALSA, WASAPI).
