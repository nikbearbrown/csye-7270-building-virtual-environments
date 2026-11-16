extends Node
# S5: a face-on square, node named Pad (QuadMesh 1.8, orthographic size 2.0 at z 3), material_override = ShaderMaterial of the --shader. The methods hold the
# lines shown on screen (B27, B28). Variant not needed: C07 uses the UV-colors shader as the --shader and no calls. Reference: verify3-attach-set-tween.gd.
func harness_setup(ctx: Dictionary) -> void:
	var mat: ShaderMaterial = ctx["materials"]["main"]
	ctx["materials"]["pad"] = mat
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = 2.0
	cam.position = Vector3(0, 0, 3)
	add_child(cam)
	cam.current = true
	var pad := MeshInstance3D.new()
	pad.name = "Pad"
	var q := QuadMesh.new()
	q.size = Vector2(1.8, 1.8)
	pad.mesh = q
	pad.material_override = mat
	add_child(pad)
func fire() -> void:
	$Pad.material_override.set_shader_parameter("activation", 1.0)
func set_start() -> void:
	var material = $Pad.material_override
	material.set_shader_parameter("activation", 0.0)
func start_tween() -> void:
	var material = $Pad.material_override
	var tween := create_tween()
	tween.tween_property(material, "shader_parameter/activation", 1.0, 2.0)
