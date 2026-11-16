extends RefCounted
# shared helpers of the capture scenes (copied node setups of the verify*.gd references; nothing re-derived)
const LAB := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shaders-in-3d/lab-shaders/"
static func mat_of(file: String) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = FileAccess.get_file_as_string(LAB + file)
	var m := ShaderMaterial.new()
	m.shader = sh
	return m
static func ortho(parent: Node, size: float, pos: Vector3) -> Camera3D:
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = size
	cam.position = pos
	parent.add_child(cam)
	cam.current = true
	return cam
