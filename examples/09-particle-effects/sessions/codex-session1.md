# Chapter 9 — Codex cost-measurement session

Readable rendering of the raw transcript in the same folder. Tool results are trimmed to 1,500 characters; scratch paths are shortened to `<scratch>/`.

**Codex thread** `01a0e415-7eeb-7001-a0e9-ca805b58fad5`

**Agent:**

I’ll add only the new benchmark script under `godot/tests`, verify the project’s local instructions and Godot executable, then run the exact headless command and report its unedited output.

**Command 1** (exit 0): `/bin/zsh -lc "pwd && rg --files -g 'AGENTS.md' -g 'godot/project.godot' -g 'godot/tests/**' | sed -n '1,120p' && command -v godot || command -v godot4 || true"`

```text
<scratch>/ch09/walker-2d-dodge-the-creeps
godot/project.godot
godot/tests/test_particles.gd
godot/tests/test_particles.gd.uid
/opt/homebrew/bin/godot

```

**Command 2** (exit 0): `/bin/zsh -lc "sed -n '1,240p' godot/tests/test_particles.gd && sed -n '1,160p' godot/project.godot && git status --short"`

```text
extends SceneTree

var failures := 0

func _initialize() -> void:
	call_deferred("run")

func check(ok: bool, label: String) -> void:
	if not ok:
		failures += 1
	print("PASS " if ok else "FAIL ", label)

func click(button: Button) -> void:
	for down in [true, false]:
		var event := InputEventMouseButton.new()
		event.position = button.get_global_rect().get_center()
		event.global_position = event.position
		event.button_index = MOUSE_BUTTON_LEFT
		event.pressed = down
		root.push_input(event, true)
		await process_frame

func run() -> void:
	seed(123)
	root.size = Vector2i(480, 720)
	var game: Node = load("res://main.tscn").instantiate()
	root.add_child(game)
	await process_frame
	await process_frame

	var player: Area2D = game.get_node("Player")
	var burst: GPUParticles2D = game.get_node("DeathBurst")

	# Static property checks — independent of rendering or gameplay state.
	check(burst.texture is GradientTexture2D, "texture is GradientTexture2D (soft round dot)")
	var mat := burst.process_material as ParticleProcessMaterial
	check(mat != null and mat.particle_flag_disable_z, "particle_flag_disable_z enabled for 2D")

	# Before any game starts the burst must be silent.
	check(not burst.emitting, "not emitting at load, before Start")

	await click(game.get_node("HUD/StartButton"))
	await process_frame

	# Still quiet after Start; fire has not been triggered yet.
	check(not burst.emitting, "not emitting after Start, before hit")

	# Capture the player's position now; force a h
… [7593 more characters trimmed]
```

**Agent:**

The benchmark will measure wall-clock time across 300 `process_frame` advances, after a 60-frame warm-up. Each particle configuration gets three independent emitter runs; the empty scene gets one comparable baseline run. Cleanup includes the requested two-frame gap.

**File change:** add `<scratch>/ch09/walker-2d-dodge-the-creeps/godot/tests/particle_cost.gd`

**Agent:**

The exact command is running successfully under Godot 4.7.2. Its dummy renderer reports `gl_compatibility` and a blank adapter name; the benchmark cases are still progressing. The startup log-file and macOS certificate warnings are environmental and have not stopped execution.

**Command 3** (exit 0): `/bin/zsh -lc 'godot --headless --path godot --script res://tests/particle_cost.gd'`

```text
Empty scene baseline: 6.899873 ms/frame
GPUParticles2D amount=1000: min=6.900733 ms/frame, mean=6.901907 ms/frame, max=6.902820 ms/frame
GPUParticles2D amount=10000: min=6.896440 ms/frame, mean=6.899294 ms/frame, max=6.900993 ms/frame
GPUParticles2D amount=50000: min=6.897453 ms/frame, mean=6.898870 ms/frame, max=6.899927 ms/frame
CPUParticles2D amount=1000: min=6.896293 ms/frame, mean=6.897669 ms/frame, max=6.898887 ms/frame
CPUParticles2D amount=10000: min=6.900270 ms/frame, mean=6.902518 ms/frame, max=6.906860 ms/frame
CPUParticles2D amount=50000: min=6.898803 ms/frame, mean=6.899192 ms/frame, max=6.899420 ms/frame

```

**Command 4** (exit 0): `/bin/zsh -lc "git status --short && git diff --check && git diff -- godot/tests/particle_cost.gd && sed -n '1,240p' godot/tests/particle_cost.gd"`

```text
?? godot/tests/particle_cost.gd
extends SceneTree

const AMOUNTS := [1000, 10000, 50000]
const WARM_UP_FRAMES := 60
const TIMED_FRAMES := 300
const REPEATS := 3


func _initialize() -> void:
	call_deferred("run")


func wait_frames(count: int) -> void:
	for _frame in count:
		await process_frame


func time_frames(count: int) -> float:
	var started_usec := Time.get_ticks_usec()
	await wait_frames(count)
	var elapsed_usec := Time.get_ticks_usec() - started_usec
	return elapsed_usec / 1000.0 / count


func make_gpu_particles(amount: int) -> GPUParticles2D:
	var material := ParticleProcessMaterial.new()
	material.initial_velocity_min = 50.0
	material.initial_velocity_max = 100.0
	material.gravity = Vector3(0.0, 98.0, 0.0)

	var particles := GPUParticles2D.new()
	particles.amount = amount
	particles.lifetime = 1.0
	particles.process_material = material
	particles.emitting = true
	return particles


func make_cpu_particles(amount: int) -> CPUParticles2D:
	var particles := CPUParticles2D.new()
	particles.amount = amount
	particles.lifetime = 1.0
	particles.initial_velocity_min = 50.0
	particles.initial_velocity_max = 100.0
	particles.gravity = Vector2(0.0, 98.0)
	particles.emitting = true
	return particles


func benchmark_case(container: Node2D, type_name: String, amount: int) -> void:
	var means: Array[float] = []
	for _repeat in REPEATS:
		var emitter: Node2D
		if type_name == "GPUParticles2D":
			emitter = make_gpu_particles(amount)
		else:
			emitter = make_cpu_particles(amoun
… [1046 more characters trimmed]
```

**Agent:**

Added [particle_cost.gd](<scratch>/ch09/walker-2d-dodge-the-creeps/godot/tests/particle_cost.gd). No existing game files were edited. The command exited successfully with code 0.

```text
ERROR: Failed to open 'user://logs/godot2026-09-27T14.17.31.log'.
   at: copy (core/io/dir_access.cpp:429)
ERROR: Failed to open log file for writing: user://logs/godot.log
   at: rotate_file (core/io/logger.cpp:169)
Godot Engine v4.7.2.stable.official.ed1daf0bf - https://godotengine.org

ERROR: Condition "ret != noErr" is true. Returning: ""
   at: get_system_ca_certificates (platform/macos/os_macos.mm:1035)
Rendering method: gl_compatibility
Video adapter: 
Headless Godot uses a dummy renderer, so GPU particle simulation and all drawing are not measured.
Empty scene baseline: 6.899873 ms/frame
GPUParticles2D amount=1000: min=6.900733 ms/frame, mean=6.901907 ms/frame, max=6.902820 ms/frame
GPUParticles2D amount=10000: min=6.896440 ms/frame, mean=6.899294 ms/frame, max=6.900993 ms/frame
GPUParticles2D amount=50000: min=6.897453 ms/frame, mean=6.898870 ms/frame, max=6.899927 ms/frame
CPUParticles2D amount=1000: min=6.896293 ms/frame, mean=6.897669 ms/frame, max=6.898887 ms/frame
CPUParticles2D amount=10000: min=6.900270 ms/frame, mean=6.902518 ms/frame, max=6.906860 ms/frame
CPUParticles2D amount=50000: min=6.898803 ms/frame, mean=6.899192 ms/frame, max=6.899420 ms/frame
```

---

**Turn complete** — usage: `{"input_tokens": 158306, "cached_input_tokens": 142464, "cache_write_input_tokens": 0, "output_tokens": 2826, "reasoning_output_tokens": 512}`

