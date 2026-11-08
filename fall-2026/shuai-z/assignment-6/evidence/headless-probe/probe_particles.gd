extends SceneTree
## Checks CLAUDE.md's headless facts about particles on this machine:
##   1. which display server and renderer the run gets;
##   2. which class and property names Godot 4.7.2 has, for every name the
##      brief uses, and that the Godot 3 names are absent;
##   3. which node state a test can observe: emitting, one_shot, amount_ratio,
##      visibility, a container's instance count, and when a one-shot burst
##      stops emitting and sends finished;
##   4. whether anything drawn can be observed: capture_rect() (the particles'
##      simulated bounds, read back from the renderer) and the frame itself;
##   5. headless CPU time per frame for an empty scene, 20,000 GPU particles
##      and 20,000 CPU particles (headless only, and only with --fixed-fps,
##      because without it the frame loop sleeps toward 6.9 ms and hides the
##      work; Chapter 9).
##
## From assignment-6/:
##   timeout 300 godot --headless --fixed-fps 60 --path evidence/headless-probe --script res://probe_particles.gd
## and once windowed, for the contrast in parts 1, 3 and 4:
##   timeout 300 godot --fixed-fps 60 --path evidence/headless-probe --script res://probe_particles.gd

const CLASSES := ["GPUParticles2D", "CPUParticles2D", "ParticleProcessMaterial",
	"GradientTexture1D", "GradientTexture2D", "CurveTexture"]
const GODOT3_CLASSES := ["Particles2D", "ParticlesMaterial"]
const GPU_PROPS := ["amount", "amount_ratio", "lifetime", "one_shot", "explosiveness",
	"randomness", "preprocess", "fixed_fps", "emitting", "local_coords",
	"visibility_rect", "use_fixed_seed", "seed", "texture", "process_material",
	"trail_enabled"]
const PPM_PROPS := ["particle_flag_disable_z", "particle_flag_align_y", "direction",
	"spread", "gravity", "initial_velocity_min", "initial_velocity_max",
	"damping_min", "damping_max", "lifetime_randomness", "scale_min", "scale_max",
	"scale_curve", "color_ramp", "hue_variation_min", "hue_variation_max",
	"emission_shape", "emission_box_extents"]
const GODOT3_PPM_PROPS := ["initial_velocity", "scale", "damping", "hue_variation",
	"flag_disable_z", "flag_align_y"]
const TEXTURE_PROPS := {
	"GradientTexture2D": ["width", "height", "fill", "fill_from", "fill_to", "gradient"],
	"GradientTexture1D": ["width", "gradient"],
	"CurveTexture": ["width", "curve"],
}

var _headless := false
var _finished_frame := -1
var _frame := 0


func _initialize() -> void:
	_run()


func _run() -> void:
	_headless = DisplayServer.get_name() == "headless"
	_part1_renderer()
	_part2_names()
	await _part3_state()
	await _part4_drawn()
	await _part5_price()
	printerr("PROBE done; quitting with code 0")
	quit(0)


func _part1_renderer() -> void:
	printerr("PROBE 1 display server '%s', rendering method '%s', driver '%s', video adapter '%s'" % [
		DisplayServer.get_name(), RenderingServer.get_current_rendering_method(),
		RenderingServer.get_current_rendering_driver_name(), RenderingServer.get_video_adapter_name()])


func _has_props(cls: String, names: Array) -> String:
	var have := {}
	for p in ClassDB.class_get_property_list(cls):
		have[p.name] = true
	var missing := names.filter(func(n): return not have.has(n))
	return "%d of %d present%s" % [names.size() - missing.size(), names.size(),
		"" if missing.is_empty() else ", missing %s" % [missing]]


func _part2_names() -> void:
	for cls in CLASSES:
		printerr("PROBE 2 class %s exists: %s" % [cls, ClassDB.class_exists(cls)])
	for cls in GODOT3_CLASSES:
		printerr("PROBE 2 Godot 3 class %s exists: %s" % [cls, ClassDB.class_exists(cls)])
	printerr("PROBE 2 GPUParticles2D %s: %s" % [GPU_PROPS, _has_props("GPUParticles2D", GPU_PROPS)])
	printerr("PROBE 2 ParticleProcessMaterial %s: %s" % [PPM_PROPS, _has_props("ParticleProcessMaterial", PPM_PROPS)])
	for cls in TEXTURE_PROPS:
		printerr("PROBE 2 %s %s: %s" % [cls, TEXTURE_PROPS[cls], _has_props(cls, TEXTURE_PROPS[cls])])
	var have := {}
	for p in ClassDB.class_get_property_list("ParticleProcessMaterial"):
		have[p.name] = true
	var present_g3 := GODOT3_PPM_PROPS.filter(func(n): return have.has(n))
	printerr("PROBE 2 Godot 3 names on ParticleProcessMaterial %s: present %s" % [GODOT3_PPM_PROPS, present_g3])
	for p in ClassDB.class_get_property_list("ParticleProcessMaterial"):
		if p.name in present_g3:
			printerr("PROBE 2   '%s' is a %s with usage %d (STORAGE %s, EDITOR %s)" % [p.name, type_string(p.type), p.usage,
				p.usage & PROPERTY_USAGE_STORAGE != 0, p.usage & PROPERTY_USAGE_EDITOR != 0])
	var scene := load("res://godot3_names.tscn") as PackedScene
	var node := scene.instantiate() as GPUParticles2D
	var m := node.process_material as ParticleProcessMaterial
	printerr("PROBE 2 a scene file with Godot 3 lines 'initial_velocity = 300.0' and 'scale = 2.0' loads: initial_velocity_min/_max %s/%s, scale_min/_max %s/%s (defaults 0/0 and 1/1)" % [
		m.initial_velocity_min, m.initial_velocity_max, m.scale_min, m.scale_max])
	node.free()


func _make_burst() -> GPUParticles2D:
	var p := GPUParticles2D.new()
	p.amount = 14
	p.lifetime = 0.45
	p.one_shot = true
	p.explosiveness = 1.0
	p.emitting = false
	p.position = Vector2(400, 300)
	var m := ParticleProcessMaterial.new()
	m.particle_flag_disable_z = true
	m.direction = Vector3(1, 0, 0)
	m.spread = 30.0
	m.initial_velocity_min = 260.0
	m.initial_velocity_max = 420.0
	m.gravity = Vector3(0, 700, 0)
	p.process_material = m
	var g := Gradient.new()
	g.set_color(0, Color(1, 1, 1, 1))
	g.set_color(1, Color(1, 1, 1, 0))
	var tex := GradientTexture2D.new()
	tex.width = 32
	tex.height = 32
	tex.fill = GradientTexture2D.FILL_RADIAL
	tex.fill_from = Vector2(0.5, 0.5)
	tex.fill_to = Vector2(1.0, 0.5)
	tex.gradient = g
	p.texture = tex
	return p


func _on_finished() -> void:
	_finished_frame = _frame


func _part3_state() -> void:
	var container := Node2D.new()
	root.add_child(container)
	var burst := _make_burst()
	burst.finished.connect(_on_finished)
	container.add_child(burst)
	await process_frame
	printerr("PROBE 3 before start: emitting %s, one_shot %s, visible in tree %s" % [
		burst.emitting, burst.one_shot, burst.is_visible_in_tree()])
	burst.emitting = true
	var stopped_frame := -1
	_frame = 0
	while _frame < 60:
		await process_frame
		_frame += 1
		if stopped_frame < 0 and not burst.emitting:
			stopped_frame = _frame
	printerr("PROBE 3 one-shot lifetime %.2f s at 60 fps (%.1f frames): emitting went false at frame %d, finished at frame %d" % [
		burst.lifetime, burst.lifetime * 60.0, stopped_frame, _finished_frame])
	burst.amount_ratio = 0.5
	printerr("PROBE 3 amount_ratio set to 0.5 reads back %s" % burst.amount_ratio)
	var second := _make_burst()
	container.add_child(second)
	printerr("PROBE 3 container instance count with two bursts: %d" % container.get_child_count())
	second.emitting = true
	container.hide()
	await process_frame
	printerr("PROBE 3 container hidden one frame after the second burst started: its visible in tree %s, its emitting %s" % [
		second.is_visible_in_tree(), second.emitting])
	container.queue_free()
	await process_frame


func _part4_drawn() -> void:
	var burst := _make_burst()
	root.add_child(burst)
	await process_frame
	burst.emitting = true
	for i in 10:
		await process_frame
	printerr("PROBE 4 capture_rect() 10 frames after a 14-particle burst started: %s" % burst.capture_rect())
	if _headless:
		var texture := root.get_texture()
		var image := texture.get_image() if texture else null
		printerr("PROBE 4 frame read back: %s" % ("an image of %s" % image.get_size() if image else "nothing"))
	else:
		await RenderingServer.frame_post_draw
		var image := root.get_texture().get_image()
		var lit := 0
		for y in image.get_height():
			for x in image.get_width():
				if image.get_pixel(x, y).v > 0.5:
					lit += 1
		printerr("PROBE 4 frame read back: an image of %s with %d bright pixels (v > 0.5) on the default grey (0.3) background" % [image.get_size(), lit])
	burst.queue_free()
	await process_frame


func _time_case(label: String, make: Callable) -> void:
	var means: Array[float] = []
	for rep in 3:
		var parent := Node2D.new()
		root.add_child(parent)
		if make.is_valid():
			make.call(parent)
		for i in 30:
			await process_frame
		var t0 := Time.get_ticks_usec()
		for i in 120:
			await process_frame
		means.append((Time.get_ticks_usec() - t0) / 120.0 / 1000.0)
		parent.queue_free()
		await process_frame
		await process_frame
	means.sort()
	printerr("PROBE 5 %s: min %.4f, mean %.4f, max %.4f ms per frame (3 runs of 120 frames)" % [
		label, means[0], (means[0] + means[1] + means[2]) / 3.0, means[2]])


func _add_gpu(parent: Node2D) -> void:
	for i in 20:
		var p := GPUParticles2D.new()
		p.amount = 1000
		p.lifetime = 1.0
		var m := ParticleProcessMaterial.new()
		m.particle_flag_disable_z = true
		m.initial_velocity_min = 50.0
		m.initial_velocity_max = 100.0
		m.gravity = Vector3(0, 98, 0)
		p.process_material = m
		parent.add_child(p)


func _add_cpu(parent: Node2D) -> void:
	for i in 20:
		var p := CPUParticles2D.new()
		p.amount = 1000
		p.lifetime = 1.0
		p.initial_velocity_min = 50.0
		p.initial_velocity_max = 100.0
		p.gravity = Vector2(0, 98)
		parent.add_child(p)


func _part5_price() -> void:
	if not _headless:
		printerr("PROBE 5 skipped: a windowed run's frame time includes vsync and the GPU, so it is not a headless CPU price")
		return
	printerr("PROBE 5 headless CPU time per frame; the dummy renderer does no GPU work and draws nothing")
	await _time_case("empty scene", Callable())
	await _time_case("20 GPUParticles2D x 1,000 (20,000 particles)", _add_gpu)
	await _time_case("20 CPUParticles2D x 1,000 (20,000 particles)", _add_cpu)
