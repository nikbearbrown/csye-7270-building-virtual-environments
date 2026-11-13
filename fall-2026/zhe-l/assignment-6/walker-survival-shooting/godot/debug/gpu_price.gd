# ============================================================
# Class declaration: what it extends, what the whole script does
# ============================================================
extends SceneTree  # Run with --script in a real window (not headless), so the GPU really draws
## A6 Use It helper for the GPU price: we load the real base.tscn with the lights on, and read the viewport's measured
## GPU render time for three states: Effect B shown, Effect B hidden, and Effect B shown with Effect A bursting.
## It complements the Visual Profiler reading: the profiler is the human check; this prints the same engine measurement
## (RenderingServer.viewport_get_measured_render_time_gpu) as numbers. Vsync is off during the run, so frames are not capped.
## Run from walker-survival-shooting/: godot_console --path godot --script res://debug/gpu_price.gd
## It changes no file. It hides LightDust as "other code" would and emits Player.landed to keep a dust burst alive.

# ============================================================
# Constants: how long each state is measured
# ============================================================
const WARMUP_FRAMES := 120  # Frames we wait after each change before measuring, so the numbers settle
const MEASURE_FRAMES := 300  # Frames we average in each state
const LANDING_EVERY := 48  # In the Effect A state, we announce a landing this often, so one burst is always alive

var _base: Node  # The loaded game scene
var _dust: GPUParticles3D  # Effect B, the light dust in base.tscn
var _player: Node  # The player body, whose landed signal starts Effect A
var _vp: RID  # The root viewport we read the GPU time from


# ============================================================
# Engine callbacks: functions Godot calls automatically at set times
# ============================================================
## Called by Godot once when the script starts. We load the base, turn vsync off, and measure each state in turn.
func _initialize() -> void:
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)  # First we uncap the frame rate
	_base = (load("res://base.tscn") as PackedScene).instantiate()  # Then we load the real game scene
	root.add_child(_base)
	_dust = _base.get_node("LightDust")  # Effect B
	_player = _base.get_node("Player")  # The body that announces landings
	_vp = root.get_viewport_rid()  # The viewport the game draws into
	RenderingServer.viewport_set_measure_render_time(_vp, true)  # And we ask the engine to measure its render time
	_run()  # The measuring runs as a coroutine over many frames


# ============================================================
# Feature functions: the measuring steps
# ============================================================
## Called by _initialize(). Measures the three states one after another, prints them, and quits.
func _run() -> void:
	print("GPU: %s" % RenderingServer.get_video_adapter_name())  # We name the GPU, so the reading is labelled
	var shown := await _measure("Effect B shown (lights on)", false)  # Effect B as the game starts it
	_dust.visible = false  # Then we hide it, as other code would; the listener stops its births
	var hidden := await _measure("Effect B hidden (lights on)", false)  # The same scene without Effect B
	_dust.visible = true  # We show it again; the listener restarts it
	var with_a := await _measure("Effect B shown + Effect A bursting", true)  # And add Effect A on top
	print("Effect B cost: %+.3f ms GPU (shown - hidden)" % (shown - hidden))  # What Effect B adds
	print("Effect A cost: %+.3f ms GPU (with A - shown)" % (with_a - shown))  # What Effect A adds
	quit()  # Done


## Called by _run(). Waits WARMUP_FRAMES, then averages the GPU time over MEASURE_FRAMES and prints mean, min and max.
func _measure(label: String, with_landings: bool) -> float:
	for i in WARMUP_FRAMES:  # First we let the change settle
		await process_frame
	var times: Array[float] = []  # Then we collect one GPU time per frame
	for i in MEASURE_FRAMES:
		if with_landings and i % LANDING_EVERY == 0:  # In the Effect A state we announce a landing now and then
			_player.landed.emit()
		await process_frame
		times.append(RenderingServer.viewport_get_measured_render_time_gpu(_vp))  # The GPU time of the last drawn frame, ms
	var total := 0.0  # We add them up for the mean
	for t in times:
		total += t
	var mean := total / times.size()
	print("%-40s GPU mean %.3f ms  min %.3f  max %.3f  (%d frames)" % [label, mean, times.min(), times.max(), times.size()])
	return mean  # The mean goes back to _run(), which prints the differences
