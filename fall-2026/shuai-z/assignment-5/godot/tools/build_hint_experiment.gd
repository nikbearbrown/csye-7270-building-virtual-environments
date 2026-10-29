extends SceneTree
## Builds res://scenes/hint_experiment.tscn for the hint experiment
## (CHANGE-BRIEF.md section 4): two quads facing the camera, each showing the
## grey strip, A through the sampler with source_color and B through the one
## without. The WorldEnvironment's tonemap is Linear at exposure 1.0, with glow,
## fog and adjustments off. The hint shader is unshaded, so there is no light.
##
## Run from assignment-5/:
##   timeout 120 godot --headless --path godot --script res://tools/build_hint_experiment.gd

const OUT := "res://scenes/hint_experiment.tscn"
const STRIP_SIZE := Vector2(1.5, 0.5) ## m, the strip's 3:1 shape
## name, material, height of its centre (m), label
const QUADS := [
	["QuadA", "res://materials/hint_source_color.tres", 0.35, "A  source_color"],
	["QuadB", "res://materials/hint_plain.tres", -0.35, "B  no hint"],
]


func _init() -> void:
	var root := Node3D.new()
	root.name = "HintExperiment"

	var env := WorldEnvironment.new()
	env.name = "WorldEnvironment"
	var e := Environment.new()
	e.background_mode = Environment.BG_COLOR
	e.background_color = Color("#202830") # dark and blue, so no band is mistaken for it
	e.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	e.tonemap_exposure = 1.0
	e.glow_enabled = false
	e.fog_enabled = false
	e.adjustment_enabled = false
	env.environment = e
	_add(root, env)

	for q: Array in QUADS:
		var quad := MeshInstance3D.new()
		quad.name = q[0]
		var mesh := QuadMesh.new() # faces +Z, towards the camera
		mesh.size = STRIP_SIZE
		quad.mesh = mesh
		quad.material_override = load(q[1] as String) as Material
		quad.position = Vector3(0, q[2], 0)
		_add(root, quad)

		var label := Label3D.new()
		label.name = (q[0] as String) + "Label"
		label.text = q[3]
		label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
		label.pixel_size = 0.004
		label.position = Vector3(-STRIP_SIZE.x / 2.0 - 0.08, q[2], 0)
		_add(root, label)

	var camera := Camera3D.new()
	camera.name = "Camera"
	camera.position = Vector3(0, 0, 2.5)
	camera.fov = 50.0
	camera.current = true
	_add(root, camera)

	var packed := PackedScene.new()
	var err := packed.pack(root)
	if err == OK:
		err = ResourceSaver.save(packed, OUT)
	print("SAVED %s: %s" % [OUT, error_string(err)])
	root.free()
	quit(0 if err == OK else 1)


func _add(parent: Node, child: Node) -> void:
	parent.add_child(child)
	child.owner = parent
