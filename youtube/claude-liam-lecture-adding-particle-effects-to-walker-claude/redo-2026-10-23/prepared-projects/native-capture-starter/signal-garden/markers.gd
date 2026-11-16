extends Node3D
# Same decorative markers in two representations, selectable for parity and pricing.
var mode := "nodes"
var count := 48
var nodes: Array[MeshInstance3D] = []
var fixed_positions: Array[Vector3] = []
var clock := 0.0
func _ready() -> void:
	process_mode = Node.PROCESS_MODE_PAUSABLE
	var mesh := BoxMesh.new()
	mesh.size = Vector3(0.035, 0.08, 0.035)
	var mat := StandardMaterial3D.new()
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.albedo_color = Color("659c93")
	mesh.material = mat
	for i in range(count):
		var obj := MeshInstance3D.new()
		obj.mesh = mesh
		add_child(obj)
		nodes.append(obj)
		fixed_positions.append(Vector3(-5.5 + fmod(i * 0.47, 11.0), 0.25, -2.65 if i % 2 else 2.65))
	update_markers(0.0)
func position_for(i: int, time: float) -> Vector3:
	return Vector3(-5.5 + fmod(i * 0.47, 11.0), 0.25 + sin(time * 2.0 + i) * 0.06, -2.65 if i % 2 else 2.65)
func update_markers(time: float) -> void:
	for i in range(count):
		var pos := fixed_positions[i] + Vector3(0, sin(time * 2.0 + i) * 0.06, 0) if mode == "cached" else position_for(i, time)
		nodes[i].position = pos
func observed_position(i: int) -> Vector3:
	return nodes[i].position
func _physics_process(delta: float) -> void:
	clock += delta
	update_markers(clock)
