extends Node
# S6: two quads with NO material; give_shaders() gives the left the 2D shader (18) and the right the 3D shader (19) as material_override.
# Reference: verify8-wrong-shader-type.gd. No lamp, no environment.
var left: MeshInstance3D
var right: MeshInstance3D
func harness_setup(ctx: Dictionary) -> void:
	var stage := Node3D.new()
	add_child(stage)
	left = mk(-0.95)
	right = mk(0.95)
	stage.add_child(left)
	stage.add_child(right)
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = 2.6
	cam.position = Vector3(0, 0, 5)
	stage.add_child(cam)
	cam.current = true
func mk(x: float) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	var q := QuadMesh.new()
	q.size = Vector2(1.4, 1.4)
	mi.mesh = q
	mi.position = Vector3(x, 0, 0)
	return mi
func give_shaders() -> void:
	var C = load("/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shaders-in-3d/capture-scenes/_common.gd")
	left.material_override = C.mat_of("18-two-d-shader-on-a-mesh.gdshader")
	right.material_override = C.mat_of("19-three-d-shader-on-a-mesh.gdshader")
