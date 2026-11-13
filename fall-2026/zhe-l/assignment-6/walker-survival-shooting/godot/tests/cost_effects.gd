# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
extends SceneTree  # Extends SceneTree: run directly with --script, no scene needed; it builds each case itself
## A6 cost script: the CPU time per frame of the two effects in CHANGE-BRIEF ("Price predictions and budget"), measured headless.
## Adapted from the chapter's Example 09 script (examples/09-particle-effects/tests/particle_cost.gd): warm up 60 frames, time 300 frames,
## repeat each case 3 times. Changes: the cases are this game's, every frame is timed on its own so we can give a spread, and the
## repeats go round-robin (case 1, 2, 3, 4, 5, then again), so slow drift on the machine lands on every case alike.
## Cases:
##   1 empty: an empty Node3D, nothing else (the floor: the main loop plus this script's own timing);
##   2 base, both effects off: the real base.tscn; LandingDust never triggered, LightDust hidden (its listener stops births);
##   3 Effect A at its most: as 2, plus one Dust + GroundRing burst alive on every timed frame (the brief: at most 1 burst, 25 particles);
##   4 Effect B at its heaviest: the real base.tscn as it loads, lights on, LightDust shown and emitting (amount read from the scene);
##   5 control (added, not an effect): an empty Node3D plus one CPUParticles3D of 10,000, to show the instrument can see a CPU cost.
## Run: ./scripts/run-test.sh cost_effects.gd 60 300. --fixed-fps is needed: without it a headless frame sleeps toward
## application/run/low_processor_mode_sleep_usec (6,900 us), and every case would read about 6.9 ms (the chapter's lesson).
## Read-only: it changes no effect or gameplay file. To keep one burst alive in case 3 it emits Player.landed itself, which is what
## the body would announce on a landing; only the landing-dust trigger listens to it. It hides LightDust as "other code" would.
## What it cannot measure: the GPU. Headless Godot uses a dummy renderer, so GPU particle simulation, preprocess and all drawing
## do not run, and both effects are GPUParticles3D; their budget is GPU time, read on a real GPU render.

# ============================================================
# Constants: the scene, the frame counts, and the control's size
# ============================================================
const BASE_SCENE := "res://base.tscn"  # The real main scene, the same one the game runs
const WARM_UP_FRAMES := 60  # Frames we let each case settle before timing (as in Example 09)
const TIMED_FRAMES := 300  # Frames we time per repeat (as in Example 09); 5 s at 60 fps
const REPEATS := 3  # Repeats per case (as in Example 09)
const SETTLE_FRAMES := 2  # Frames we wait after freeing a case, before the next one
const RETRIGGER_FRAMES := 48  # Case 3 lands every 0.8 s: half the Dust lifetime (1.6 s), so a burst is always alive
const DUST_LIFETIME_FRAMES := 96  # Dust lifetime 1.6 s at 60 fps; a burst older than this is gone
const CONTROL_AMOUNT := 10000  # Particles in the control's CPUParticles3D
const CASES := ["empty", "base_off", "effect_a", "effect_b", "control"]  # The order inside each round
const LABELS := {  # What each case is, for the output
	"empty": "1 empty scene",
	"base_off": "2 base.tscn, both effects off",
	"effect_a": "3 base.tscn, Effect A: 1 burst alive",
	"effect_b": "4 base.tscn, Effect B: lights on, emitting",
	"control": "5 control: CPUParticles3D x 10000 (added)",
}

var _frames := {}  # Case name -> every timed frame of every repeat, microseconds
var _means := {}  # Case name -> the mean of each repeat, milliseconds
var _notes := {}  # Case name -> the state we read back at the end of the last repeat, so we know the case was what it says


# ============================================================
# Engine callbacks: functions Godot calls automatically at set times
# ============================================================
## Called by Godot once when the script starts. We defer the run, so the tree is up before we add anything.
func _initialize() -> void:
	call_deferred("_run")


# ============================================================
# Feature functions: the run, the cases, the timing
# ============================================================
## Called by _initialize(). Prints the instrument, runs every case REPEATS times round-robin, then prints the results.
func _run() -> void:
	print("Rendering method: ", RenderingServer.get_current_rendering_method())  # First we say what renderer this run has
	print("Video adapter: '", RenderingServer.get_video_adapter_name(), "'")  # Empty headless: there is no real GPU behind it
	print("Headless Godot uses a dummy renderer, so GPU particle simulation, preprocess and all drawing are not measured; these are CPU times only.")
	print("Frames: %d warm-up, %d timed, %d repeats per case, round-robin; Engine.max_fps %d, physics %d ticks/s" % [WARM_UP_FRAMES, TIMED_FRAMES, REPEATS, Engine.max_fps, Engine.physics_ticks_per_second])
	for name in CASES:  # Then we make an empty record for every case
		_frames[name] = []
		_means[name] = []
	for repeat in REPEATS:  # Each round runs every case once
		for name in CASES:
			await _run_case(name, repeat)
	_report()  # Then we print the numbers and the comparisons
	quit(0)


## Called by _run(). Builds one case, warms it up, times it, reads back its state, and frees it.
func _run_case(name: String, repeat: int) -> void:
	var holder := Node3D.new()  # Every case lives under its own holder, so freeing it frees the whole case
	root.add_child(holder)
	var base: Node = null
	if name in ["base_off", "effect_a", "effect_b"]:  # If the case needs the game scene, we load the real base.tscn
		base = (load(BASE_SCENE) as PackedScene).instantiate()
		holder.add_child(base)
		await process_frame  # One frame, so every _ready() has run and the listener has asked CeilingLights once
		if name != "effect_b":  # If Effect B is meant to be off, we hide it; its listener stops births (it is on at load)
			(base.get_node("LightDust") as GPUParticles3D).visible = false
	elif name == "control":  # If it is the control, we add one emitting CPUParticles3D to the empty holder
		var cpu := CPUParticles3D.new()
		cpu.amount = CONTROL_AMOUNT
		cpu.lifetime = 1.0
		cpu.initial_velocity_min = 0.5
		cpu.initial_velocity_max = 1.0
		cpu.emitting = true
		holder.add_child(cpu)
	var landings := {"count": 0, "since": 0}  # Case 3 only: how many landings we announced, and frames since the last one
	var finished := {"count": 0}  # Case 3 only: how many Dust bursts finished while we timed; 0 means one was alive on every frame
	if name == "effect_a":
		(base.get_node("LandingDust/Dust") as GPUParticles3D).finished.connect(func() -> void: finished.count += 1)
	for i in WARM_UP_FRAMES:  # Then we let the case settle; case 3 starts its bursts here, so the first timed frame already has one
		_tick_landing(name, base, landings)
		await process_frame
	finished.count = 0  # Only bursts that end while we time count
	var times: Array = _frames[name]
	var start := Time.get_ticks_usec()  # Then we time each frame on its own: the gap between two process_frame signals
	var total := 0
	for i in TIMED_FRAMES:
		_tick_landing(name, base, landings)
		await process_frame
		var now := Time.get_ticks_usec()
		times.append(now - start)  # One frame's wall time in microseconds; the spread below comes from these
		total += now - start
		start = now
	(_means[name] as Array).append(total / 1000.0 / TIMED_FRAMES)  # This repeat's mean, ms per frame
	if repeat == REPEATS - 1:  # On the last repeat we read the state back, so the output shows what each case really was
		_notes[name] = _read_state(name, base, holder, landings, finished)
	holder.queue_free()  # Then we free the case and let the tree settle before the next one
	for i in SETTLE_FRAMES:
		await process_frame


## Called by _run_case() every frame. In case 3 we announce a landing every RETRIGGER_FRAMES, as the body would on landing,
## so the trigger replays one burst at the feet; nothing else in the case moves.
func _tick_landing(name: String, base: Node, landings: Dictionary) -> void:
	if name != "effect_a":
		return
	if landings.count == 0 or landings.since >= RETRIGGER_FRAMES:  # The first frame, then every 0.8 s
		(base.get_node("Player") as Humanoid).landed.emit()
		landings.count += 1
		landings.since = 0
	landings.since += 1


## Called by _run_case() on the last repeat. Returns one line saying the state of the effects in this case.
func _read_state(name: String, base: Node, holder: Node, landings: Dictionary, finished: Dictionary) -> String:
	if base == null:
		return "children of the case: %d" % holder.get_child_count()
	var light := base.get_node("LightDust") as GPUParticles3D
	var line := "LightDust visible %s, emitting %s, amount %d" % [light.visible, light.emitting, light.amount]
	if name == "effect_a":
		line += "; %d landings announced (every %d frames), Dust bursts finished while timed: %d (0 = one alive on every frame)" % [landings.count, RETRIGGER_FRAMES, finished.count]
	else:
		line += "; LandingDust never triggered"
	return line


## Called by _run() at the end. Prints each case's mean and spread, then compares the cases that should and should not differ.
func _report() -> void:
	print("")
	print("Per case (ms per frame; mean of the %d repeat means; repeat means min-max; per-frame sd, p95, max over all %d frames):" % [REPEATS, REPEATS * TIMED_FRAMES])
	var stats := {}
	for name in CASES:
		stats[name] = _stats(name)
		var s: Dictionary = stats[name]
		print("  %-44s mean %.4f  [%.4f-%.4f]  sd %.4f  p95 %.4f  max %.4f" % [LABELS[name], s.mean, s.lo, s.hi, s.sd, s.p95, s.max])
		print("      %s" % _notes[name])
	print("")
	print("Differences (b - a, ms per frame), with the noise: the widest repeat-means range of the two cases:")
	_compare(stats, "empty", "base_off", "should differ: the game scene has physics, the player and scripts")
	_compare(stats, "empty", "control", "should differ: 10,000 CPU particles (the instrument check)")
	_compare(stats, "base_off", "effect_a", "brief predicts within 0.05 ms headless (GPU node)")
	_compare(stats, "base_off", "effect_b", "brief predicts within 0.05 ms headless (GPU node)")


## Called by _report(). Works out one case's mean, repeat range and per-frame spread, in milliseconds.
func _stats(name: String) -> Dictionary:
	var means: Array = _means[name]
	var frames: Array = (_frames[name] as Array).duplicate()
	var mean := 0.0
	for m in means:
		mean += m
	mean /= means.size()
	var frame_mean := 0.0
	for f in frames:
		frame_mean += f
	frame_mean /= frames.size()
	var variance := 0.0
	for f in frames:
		variance += (f - frame_mean) * (f - frame_mean)
	variance /= frames.size()
	frames.sort()
	return {
		"mean": mean, "lo": means.min(), "hi": means.max(),
		"sd": sqrt(variance) / 1000.0,
		"p95": frames[int(frames.size() * 0.95)] / 1000.0,
		"max": frames[-1] / 1000.0,
	}


## Called by _report(). Prints one difference and says plainly when two cases read the same within the noise.
func _compare(stats: Dictionary, a: String, b: String, expectation: String) -> void:
	var sa: Dictionary = stats[a]
	var sb: Dictionary = stats[b]
	var diff: float = sb.mean - sa.mean
	var noise: float = maxf(sa.hi - sa.lo, sb.hi - sb.lo)
	var verdict := "SAME within the noise" if absf(diff) <= noise else "differs"
	print("  %s -> %s: %+.4f ms (noise %.4f) %s; %s" % [a, b, diff, noise, verdict, expectation])
