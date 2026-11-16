extends Node
# S2: a quad, a box and a sphere with ONE shared material, each tilted -20 deg about X and swinging +-50 deg about Y (a sine, period 8 s).
# Reference: verify9-three-meshes-picture.gd. The swing is computed from the harness clock (harness_frame).
var nodes := []
func harness_setup(ctx: Dictionary) -> void:
	var mat: ShaderMaterial = ctx["materials"]["main"]
	var stage := Node3D.new()
	add_child(stage)
	var q := QuadMesh.new(); q.size = Vector2(1.0, 1.0)
	var b := BoxMesh.new(); b.size = Vector3(1.0, 1.0, 1.0)
	var s := SphereMesh.new()
	var meshes := [q, b, s]
	var xs := [-1.35, 0.0, 1.35]
	for i in range(3):
		var mi := MeshInstance3D.new()
		mi.mesh = meshes[i]
		mi.material_override = mat
		mi.position = Vector3(xs[i], 0, 0)
		stage.add_child(mi)
		nodes.append(mi)
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = 2.6
	cam.position = Vector3(0, 0, 5)
	stage.add_child(cam)
	cam.current = true
	harness_frame(0.0)
func harness_frame(t: float) -> void:
	var yaw := 50.0 * sin(TAU * t / 8.0)
	for n in nodes:
		n.rotation_degrees = Vector3(-20, yaw, 0)
