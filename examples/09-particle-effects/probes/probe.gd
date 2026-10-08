extends SceneTree

var fin := {}

func _initialize() -> void:
	run.call_deferred()

func mk(kind: String) -> Node:
	var p: Node
	match kind:
		"GPU2D":
			var g := GPUParticles2D.new()
			var m := ParticleProcessMaterial.new()
			m.gravity = Vector3(0, 98, 0)
			m.initial_velocity_min = 100.0
			m.initial_velocity_max = 200.0
			g.process_material = m
			p = g
		"CPU2D":
			p = CPUParticles2D.new()
		"GPU3D":
			var g3 := GPUParticles3D.new()
			g3.process_material = ParticleProcessMaterial.new()
			g3.draw_pass_1 = QuadMesh.new()
			p = g3
		"CPU3D":
			var c3 := CPUParticles3D.new()
			c3.mesh = QuadMesh.new()
			p = c3
	p.set("amount", 32)
	p.set("lifetime", 0.5)
	p.set("one_shot", true)
	p.set("explosiveness", 1.0)
	p.set("emitting", false)
	p.name = kind
	p.connect("finished", func(): fin[kind] = Time.get_ticks_msec())
	return p

func run() -> void:
	print("renderer=", RenderingServer.get_current_rendering_method(), " driver=", RenderingServer.get_current_rendering_driver_name(), " video_adapter=", RenderingServer.get_video_adapter_name())
	print("audio_driver=", AudioServer.get_driver_name() if AudioServer.has_method("get_driver_name") else "n/a")
	var kinds := ["GPU2D", "CPU2D", "GPU3D", "CPU3D"]
	var nodes := {}
	var holder2d := Node2D.new(); root.add_child(holder2d)
	var holder3d := Node3D.new(); root.add_child(holder3d)
	for k in kinds:
		var n := mk(k)
		if k.ends_with("2D"): holder2d.add_child(n)
		else: holder3d.add_child(n)
		nodes[k] = n
	await process_frame
	var t0 := Time.get_ticks_msec()
	for k in kinds:
		nodes[k].emitting = true
	await process_frame
	for k in kinds:
		print(k, " after 1 frame: emitting=", nodes[k].emitting)
	await create_timer(0.25).timeout
	for k in kinds:
		var extra := ""
		if nodes[k] is GPUParticles2D or nodes[k] is GPUParticles3D:
			extra = " capture_aabb/rect=" + str(nodes[k].capture_rect() if nodes[k] is GPUParticles2D else nodes[k].capture_aabb())
		print(k, " at 0.25s: emitting=", nodes[k].emitting, extra)
	await create_timer(1.0).timeout
	for k in kinds:
		print(k, " at 1.25s: emitting=", nodes[k].emitting, " finished_ms=", (fin[k] - t0) if fin.has(k) else -1)
	# restart test
	fin.clear()
	t0 = Time.get_ticks_msec()
	for k in kinds:
		nodes[k].restart()
	await process_frame
	for k in kinds:
		print(k, " after restart(): emitting=", nodes[k].emitting)
	await create_timer(1.0).timeout
	for k in kinds:
		print(k, " restart finished_ms=", (fin[k] - t0) if fin.has(k) else -1)
	# CPU particle positions observable? use convert_from_particles? check internal via get_property_list? 
	var c: CPUParticles2D = nodes["CPU2D"]
	print("CPU2D amount=", c.amount, " lifetime=", c.lifetime, " preprocess=", c.preprocess)
	print("Perf object_count=", Performance.get_monitor(Performance.OBJECT_COUNT), " nodes=", Performance.get_monitor(Performance.OBJECT_NODE_COUNT))
	print("Perf draw_calls=", Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME), " objects_in_frame=", Performance.get_monitor(Performance.RENDER_TOTAL_OBJECTS_IN_FRAME), " video_mem=", Performance.get_monitor(Performance.RENDER_VIDEO_MEM_USED))
	quit(0)
