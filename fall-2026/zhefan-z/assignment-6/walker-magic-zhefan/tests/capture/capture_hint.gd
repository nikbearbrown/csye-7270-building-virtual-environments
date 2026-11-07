extends "res://tests/capture/capture_common.gd"
## Hint-experiment capture (CHANGE-BRIEF section 3). Open tests/capture/capture_hint.tscn, F6, press F9.
## Samples the centre of each of the three bands on each quad: u = 1/6, 1/2, 5/6, v = 1/2, placed on the
## quad from the QuadMesh's own vertex/UV arrays and projected with Camera3D.unproject_position.

const BANDS := [1.0 / 6.0, 0.5, 5.0 / 6.0]
const STORED := [64, 128, 192]   # greys_3x1.png, written by tools/write_hint_png.gd

@onready var camera: Camera3D = $HintExperiment/Camera3D
@onready var quads: Array[MeshInstance3D] = [$HintExperiment/QuadSourceColor, $HintExperiment/QuadRawData]


func bindings() -> Dictionary:
	return {"F9": "capture hint_quads.png and sample the three band centres on each quad"}


func on_key(keycode: Key) -> void:
	if keycode == KEY_F9:
		run_capture()


## Local position of (u, v) on the mesh's first surface, from the corners whose UVs are (0, 0), (1, 0), (0, 1).
func uv_to_local(mesh: Mesh, u: float, v: float) -> Vector3:
	var arrays := mesh.surface_get_arrays(0)
	var verts: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
	var uvs: PackedVector2Array = arrays[Mesh.ARRAY_TEX_UV]
	var corner := {}
	for i in verts.size():
		corner[Vector2i(roundi(uvs[i].x), roundi(uvs[i].y))] = verts[i]
	var p00: Vector3 = corner[Vector2i(0, 0)]
	return p00 + (corner[Vector2i(1, 0)] - p00) * u + (corner[Vector2i(0, 1)] - p00) * v


func encode(x: float) -> float:
	return 12.92 * x if x <= 0.0031308 else 1.055 * pow(x, 1.0 / 2.4) - 0.055


func run_capture() -> void:
	busy = true
	var file := "hint_quads.png"
	var img := await capture(file)
	var rows: Array[Dictionary] = []
	for mi in quads:
		var mat := mi.get_surface_override_material(0) as ShaderMaterial
		var use_source_color: bool = mat.get_shader_parameter("use_source_color")
		for i in BANDS.size():
			var local := uv_to_local(mi.mesh, BANDS[i], 0.5)
			var world := mi.global_transform * local
			var pos := camera.unproject_position(world)
			# CHANGE-BRIEF section 3's model: with source_color the stored value, without it encode(stored).
			var expected: float = STORED[i] if use_source_color else encode(STORED[i] / 255.0) * 255.0
			rows.append(sample(img, "%s band %d" % [mi.name, i], file, pos, {"quad": mi.name,
				"material": mat.resource_path, "use_source_color": use_source_color, "uv": [BANDS[i], 0.5],
				"world": [world.x, world.y, world.z], "stored": STORED[i], "section_3_prediction": expected,
				"in_front_of_camera": not camera.is_position_behind(world)}))
	write_json("hint_pixels.json", {"scene": scene_file_path, "image_size": [img.get_width(), img.get_height()],
		"samples": rows})
	busy = false
