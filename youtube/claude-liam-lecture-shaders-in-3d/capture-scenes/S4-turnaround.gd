extends Node
# S4: two quads turning about Y: left default culling (07 unshaded), right cull_disabled (09 two-sided). Both turn 0 to 360 across the first 0.8 of the clip
# (CLIP_L seconds, from the environment), then hold. Reference: verify5-cull-turnaround.gd.
var left: MeshInstance3D
var right: MeshInstance3D
var clip_l := 12.0
func harness_setup(ctx: Dictionary) -> void:
	var C = load("/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shaders-in-3d/capture-scenes/_common.gd")
	if OS.get_environment("CLIP_L") != "":
		clip_l = float(OS.get_environment("CLIP_L"))
	var stage := Node3D.new()
	add_child(stage)
	left = mk(C.mat_of("07-flat-teal-3d-unshaded.gdshader"), -0.85)
	right = mk(C.mat_of("09-two-sided.gdshader"), 0.85)
	stage.add_child(left)
	stage.add_child(right)
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = 2.4
	cam.position = Vector3(0, 0, 5)
	stage.add_child(cam)
	cam.current = true
func mk(m: ShaderMaterial, x: float) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	var q := QuadMesh.new()
	q.size = Vector2(1.2, 1.2)
	mi.mesh = q
	mi.material_override = m
	mi.position = Vector3(x, 0, 0)
	return mi
func harness_frame(t: float) -> void:
	var yaw := 360.0 * clampf(t / (0.8 * clip_l), 0.0, 1.0)
	left.rotation_degrees = Vector3(0, yaw, 0)
	right.rotation_degrees = Vector3(0, yaw, 0)
