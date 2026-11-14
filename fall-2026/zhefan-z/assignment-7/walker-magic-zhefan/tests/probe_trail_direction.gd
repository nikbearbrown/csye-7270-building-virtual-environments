extends SceneTree
## Assignment 6 probe, not a test (it prints and asserts nothing): does the trail's `direction` (-1, 0) follow the
## emitter's rotation, as for a fireball cast to the left (rotation pi), or is it world space as CHANGE-BRIEF Effect B
## says? And is `gravity` world space? Headless runs no GPU particle process and capture_rect() is empty, so this must
## run WINDOWED on a real GPU. From fall-2026/zhefan-z/assignment-6/:
##   Godot_v4.7.2-stable_win64_console.exe --path walker-magic-zhefan --script res://tests/probe_trail_direction.gd
## Emitters stand still (no fireball motion to mask the direction). Each frame from 0.15 s to 0.6 s it reads
## capture_rect() (the bounds of the live particles) and prints the mean centre per emitter.
## - "calibration": the unchanged trail, rotation 0, placed at (320, 300): a centre near (0, 0) means capture_rect is in
##   the emitter's local frame, near (320, 300) means world.
## - "real_rot0" / "real_rotpi": the unchanged effect scene at rotation 0 and pi.
## - "fast_*": a probe-only duplicate of the material, velocity 200, spread 0, no turbulence, no gravity, radius 0, so
##   the sign along x is unambiguous. "gravity_*": velocity 0, gravity (0, -300), to see whether gravity is world space.
## The effect scene and its resources are never changed: the probe duplicates the material before editing it.

const TRAIL := preload("res://effects/fireball_trail.tscn")
const FROM_S := 0.15
const TO_S := 0.6

var emitters := {}
var sums := {}


func _initialize() -> void:
	call_deferred("run")


func add(name: String, pos: Vector2, rot: float, edit: Callable) -> void:
	var p := TRAIL.instantiate() as GPUParticles2D
	if edit.is_valid():
		var pm := (p.process_material as ParticleProcessMaterial).duplicate() as ParticleProcessMaterial
		edit.call(pm)
		p.process_material = pm
	p.position = pos
	p.rotation = rot
	root.add_child(p)
	emitters[name] = p
	sums[name] = {"n": 0, "centre": Vector2.ZERO, "size": Vector2.ZERO}


func fast(pm: ParticleProcessMaterial) -> void:
	pm.initial_velocity_min = 200.0
	pm.initial_velocity_max = 200.0
	pm.spread = 0.0
	pm.turbulence_enabled = false
	pm.gravity = Vector3.ZERO
	pm.emission_sphere_radius = 0.0


func gravity_only(pm: ParticleProcessMaterial) -> void:
	pm.initial_velocity_min = 0.0
	pm.initial_velocity_max = 0.0
	pm.spread = 0.0
	pm.turbulence_enabled = false
	pm.gravity = Vector3(0, -300, 0)
	pm.emission_sphere_radius = 0.0


func run() -> void:
	print(JSON.stringify({"probe": "trail_direction", "renderer": RenderingServer.get_video_adapter_name(),
		"method": ProjectSettings.get_setting("rendering/renderer/rendering_method")}))
	add("calibration", Vector2(320, 300), 0.0, Callable())
	add("real_rot0", Vector2(160, 60), 0.0, Callable())
	add("real_rotpi", Vector2(480, 60), PI, Callable())
	add("fast_rot0", Vector2(160, 150), 0.0, fast)
	add("fast_rotpi", Vector2(480, 150), PI, fast)
	add("gravity_rot0", Vector2(160, 240), 0.0, gravity_only)
	add("gravity_rotpi", Vector2(480, 240), PI, gravity_only)
	var t := 0.0
	while t < TO_S:
		await process_frame
		t += root.get_process_delta_time()
		if t < FROM_S:
			continue
		for name: String in emitters:
			var r: Rect2 = (emitters[name] as GPUParticles2D).capture_rect()
			if r.size == Vector2.ZERO and r.position == Vector2.ZERO:
				continue
			sums[name].n += 1
			sums[name].centre += r.get_center()
			sums[name].size += r.size
	for name: String in emitters:
		var s: Dictionary = sums[name]
		var e := emitters[name] as GPUParticles2D
		print(JSON.stringify({"emitter": name, "position": e.position, "rotation": snappedf(e.rotation, 0.0001),
			"samples": s.n, "mean_rect_centre": (s.centre / maxi(s.n, 1)).snappedf(0.01),
			"mean_rect_size": (s.size / maxi(s.n, 1)).snappedf(0.01)}))
	quit(0)
