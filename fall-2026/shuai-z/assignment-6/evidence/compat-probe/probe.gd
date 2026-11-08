extends Node2D
## A throwaway probe, not part of the game, written by Claude Code on
## 2026-11-04 before the Assignment 6 brief. It asks three questions of the
## renderer the game uses (GL Compatibility), on this machine:
## 1. Does a GPUParticles2D with trail_enabled draw? (left third)
## 2. Do damping and a box emission shape work? (middle third: particles leave
##    a 60 x 6 px box at 150 px/s and damping 300 px/s² stops them in 0.5 s,
##    so by frame 30 they sit within about 40 px of the box)
## 3. Can a GPU render time be read? (viewport_get_measured_render_time_gpu)
## The right third is a plain emitter, the reference. Run it windowed, once per
## renderer (README.md gives the commands); --rendering-method overrides the
## project setting for that run only.

var frame := 0
var vp: RID
var gpu: Array[float] = []
var trail: GPUParticles2D


func _ready() -> void:
	vp = get_viewport().get_viewport_rid()
	RenderingServer.viewport_set_measure_render_time(vp, true)
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
	trail = _make(tex, Vector2(160, 180))
	trail.trail_enabled = true
	trail.trail_lifetime = 0.4
	trail.trail_sections = 8
	var damped := _make(tex, Vector2(480, 180))
	var dm := damped.process_material as ParticleProcessMaterial
	dm.emission_shape = ParticleProcessMaterial.EMISSION_SHAPE_BOX
	dm.emission_box_extents = Vector3(30, 3, 0)
	dm.damping_min = 300.0
	dm.damping_max = 300.0
	_make(tex, Vector2(800, 180))
	print("renderer: method=%s driver=%s adapter=%s api=%s" % [RenderingServer.get_current_rendering_method(), RenderingServer.get_current_rendering_driver_name(), RenderingServer.get_video_adapter_name(), RenderingServer.get_video_adapter_api_version()])
	print("read back: trail_enabled=%s damping=%s..%s emission_shape=%d" % [trail.trail_enabled, dm.damping_min, dm.damping_max, dm.emission_shape])


func _make(tex: Texture2D, at: Vector2) -> GPUParticles2D:
	var m := ParticleProcessMaterial.new()
	m.particle_flag_disable_z = true
	m.gravity = Vector3.ZERO
	m.direction = Vector3(1, 0, 0)
	m.spread = 180.0
	m.initial_velocity_min = 150.0
	m.initial_velocity_max = 150.0
	var p := GPUParticles2D.new()
	p.process_material = m
	p.texture = tex
	p.amount = 24
	p.lifetime = 1.0
	p.position = at
	add_child(p)
	return p


func _process(_delta: float) -> void:
	frame += 1
	trail.position = Vector2(160, 180) + Vector2(cos(frame * 0.15), sin(frame * 0.15)) * 50.0
	if frame > 10:
		gpu.append(RenderingServer.viewport_get_measured_render_time_gpu(vp))
	if frame == 40:
		print("gpu ms, frames 11-40: min %s max %s" % [gpu.min(), gpu.max()])
