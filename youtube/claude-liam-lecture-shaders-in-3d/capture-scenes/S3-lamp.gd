extends Node
# S3: spheres under one directional lamp. Variant from S_VARIANT: "a" one sphere, lamp OFF until lamp_on() (C03a); "1" one sphere, lamp on and turning
# (C03); "2" two spheres (lit, unshaded) (C04); "3" three spheres (lit, unshaded, empty light()) (C05). The lamp's yaw is -65 + 360 t / 14 (harness clock).
# Reference: verify4-lamp.gd and verify10-lamp-start.gd. Ambient white, energy 0.25; lamp energy 1.0, pitch -30.
var lamp: DirectionalLight3D
var turning := true
var fixed_yaw := -65.0
func harness_setup(ctx: Dictionary) -> void:
	var variant := OS.get_environment("S_VARIANT")
	var C = load("/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shaders-in-3d/capture-scenes/_common.gd")
	var stage := Node3D.new()
	add_child(stage)
	var env := Environment.new()
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color.WHITE
	env.ambient_light_energy = 0.25
	var we := WorldEnvironment.new()
	we.environment = env
	stage.add_child(we)
	lamp = DirectionalLight3D.new()
	lamp.light_energy = 1.0
	stage.add_child(lamp)
	var files := ["02-flat-teal-3d.gdshader"]
	var xs := [0.0]
	var size := 1.8
	if variant == "2":
		files = ["02-flat-teal-3d.gdshader", "07-flat-teal-3d-unshaded.gdshader"]; xs = [-0.7, 0.7]; size = 2.4
	elif variant == "3":
		files = ["02-flat-teal-3d.gdshader", "07-flat-teal-3d-unshaded.gdshader", "08-flat-teal-3d-empty-light.gdshader"]; xs = [-1.15, 0.0, 1.15]; size = 2.8
	for i in range(files.size()):
		var mi := MeshInstance3D.new()
		var sm := SphereMesh.new()
		sm.radius = 0.5
		sm.height = 1.0
		mi.mesh = sm
		mi.material_override = C.mat_of(files[i])
		mi.position = Vector3(xs[i], 0, 0)
		stage.add_child(mi)
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = size
	cam.position = Vector3(0, 0, 5)
	stage.add_child(cam)
	cam.current = true
	if variant == "a":
		turning = false
		lamp.light_energy = 0.0
	lamp.rotation_degrees = Vector3(-30, fixed_yaw, 0)
func lamp_on() -> void:
	lamp.light_energy = 1.0
func harness_frame(t: float) -> void:
	if turning:
		lamp.rotation_degrees = Vector3(-30, -65.0 + 360.0 * t / 14.0, 0)
