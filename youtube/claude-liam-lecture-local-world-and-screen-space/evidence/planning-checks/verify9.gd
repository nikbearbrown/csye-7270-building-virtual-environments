extends SceneTree
# verify9.gd: what the matrices actually contain (so the 4 by 4 tables drawn in B09, B13 and B27 are true).
#   M1  MODEL_MATRIX of a plain sprite at (600,400): all 16 entries, as the shader reads them (column by column)
#   M2  MODEL_MATRIX of the same sprite scaled 2 and turned 30 degrees
#   M3  CANVAS_MATRIX with the camera at (890,460), then panned to (990,460), then zoomed 2x on (600,400)
# Run: godot --path <project dir> --script res://verify9.gd

const Lib := preload("res://probe_lib.gd")
var lib

const SH := """
shader_type canvas_item;
uniform int mat_id = 0;     // 0 = MODEL_MATRIX, 1 = CANVAS_MATRIX
uniform int col = 0;
uniform int row = 0;
varying float v;
void vertex() {
	mat4 m = mat_id == 0 ? MODEL_MATRIX : CANVAS_MATRIX;
	v = m[col][row];
}
void fragment() {
	float i = floor(v * 1000.0 + 8000000.0);      // 3 decimals, offset so negatives encode (v from -8000 to +8777)
	float r = floor(i / 65536.0);
	float g = floor((i - r * 65536.0) / 256.0);
	float b = i - r * 65536.0 - g * 256.0;
	COLOR = vec4(r / 255.0, g / 255.0, b / 255.0, 1.0);
}
"""


func _initialize() -> void:
	call_deferred("run")


func dump(mat: ShaderMaterial, mat_id: int, px: int, py: int) -> Array:
	var out: Array = []
	for c in range(4):
		var column: Array = []
		for r in range(4):
			mat.set_shader_parameter("mat_id", mat_id)
			mat.set_shader_parameter("col", c)
			mat.set_shader_parameter("row", r)
			await lib.frames(2)
			var col: Color = lib.grab().get_pixel(px, py)
			var i := roundi(col.r * 255.0) * 65536 + roundi(col.g * 255.0) * 256 + roundi(col.b * 255.0)
			column.append(snappedf((float(i) - 8000000.0) / 1000.0, 0.001))
		out.append(column)
	return out


func run() -> void:
	lib = Lib.new(self)
	root.size = Vector2i(1280, 720)
	await lib.frames(3)
	var sh := Shader.new()
	sh.code = SH
	var mat := ShaderMaterial.new()
	mat.shader = sh
	var spr := Sprite2D.new()
	spr.texture = lib.white_texture(128)
	spr.position = Vector2(600, 400)
	spr.material = mat
	root.add_child(spr)
	var cam := Camera2D.new()
	cam.position = Vector2(890, 460)
	root.add_child(cam)
	cam.make_current()
	await lib.frames(4)

	var m1 = await dump(mat, 0, 300, 300)
	lib.out("M1-MODEL_MATRIX-plain-sprite-at-600-400", {"columns": m1, "note": "m[col][row]; the last column (index 3) is the node's position and w", "last_column": m1[3]})
	var c1 = await dump(mat, 1, 300, 300)
	lib.out("M3a-CANVAS_MATRIX-camera-890-460", {"columns": c1, "last_column": c1[3]})
	cam.position = Vector2(990, 460)
	await lib.frames(4)
	var c2 = await dump(mat, 1, 300, 300)
	lib.out("M3b-CANVAS_MATRIX-camera-990-460", {"columns": c2, "last_column": c2[3]})
	cam.position = Vector2(600, 400)
	cam.zoom = Vector2(2, 2)
	await lib.frames(4)
	var c3 = await dump(mat, 1, 640, 360)
	lib.out("M3c-CANVAS_MATRIX-camera-zoom-2-on-600-400", {"columns": c3, "last_column": c3[3]})
	var m1z = await dump(mat, 0, 640, 360)
	lib.out("M1z-MODEL_MATRIX-unchanged-by-the-zoom", {"columns": m1z, "last_column": m1z[3]})
	cam.zoom = Vector2(1, 1)
	cam.position = Vector2(640, 360)
	spr.scale = Vector2(2, 2)
	spr.rotation = deg_to_rad(30.0)
	await lib.frames(4)
	var m2 = await dump(mat, 0, 640, 400)
	lib.out("M2-MODEL_MATRIX-scaled-2-turned-30", {"columns": m2, "x_axis": m2[0], "y_axis": m2[1], "last_column": m2[3],
		"expected_x_axis": [2.0 * cos(deg_to_rad(30.0)), 2.0 * sin(deg_to_rad(30.0))], "expected_y_axis": [-2.0 * sin(deg_to_rad(30.0)), 2.0 * cos(deg_to_rad(30.0))]})
	quit(0)
