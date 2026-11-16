extends Node
# S1: the signal pad on a flat quad (C01) or a box beside a quad (C14). Variant from the environment variable S_VARIANT: "single" | "two".
# Reference: evidence/planning-checks/verify2-pad-on-quad-and-box.gd part (c). Material kept under materials["pad"].
const _UNUSED := 0
func harness_setup(ctx: Dictionary) -> void:
	var variant := OS.get_environment("S_VARIANT")
	var mat: ShaderMaterial = ctx["materials"]["main"]
	ctx["materials"]["pad"] = mat
	var stage := Node3D.new()
	add_child(stage)
	var quad := MeshInstance3D.new()
	var q := QuadMesh.new()
	q.size = Vector2(1.55, 1.55)
	quad.mesh = q
	quad.rotation_degrees = Vector3(-90, 0, 0)          # lay it flat, like the pad's top face
	quad.material_override = mat
	stage.add_child(quad)
	var size := 2.6
	if variant == "two":
		var box := MeshInstance3D.new()
		var b := BoxMesh.new()
		b.size = Vector3(1.55, 0.10, 1.55)
		box.mesh = b
		box.position = Vector3(-1.1, 0, 0)
		box.material_override = mat
		stage.add_child(box)
		quad.position = Vector3(1.1, 0, 0)
		size = 3.2
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = size
	cam.position = Vector3(5.8, 9, 11).normalized() * 12.0
	stage.add_child(cam)
	cam.current = true
	cam.look_at(Vector3.ZERO)
