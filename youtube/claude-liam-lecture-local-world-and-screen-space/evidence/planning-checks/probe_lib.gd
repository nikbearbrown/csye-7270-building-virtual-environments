extends RefCounted
# probe_lib.gd: shared helper for the layout checks of "Local, World and Screen Space".
# One shader (ENC) writes a chosen number as a 16-bit value into the red and green channels; read() decodes it from a pixel.
# Fragment centers sit at +0.5, so floor() of an interpolated pixel position is the integer pixel index (robust to float error).
# Encoded value = floor(v * scale + 1024): red = high byte, green = low byte (both /255). Exact for 8-bit framebuffers.

const ENC := """
shader_type canvas_item;
uniform int which = 0;
uniform float scale = 1.0;
varying vec2 l;
varying vec2 w;
varying vec2 s;
varying vec2 sw;      // WRONG ORDER on purpose: MODEL_MATRIX * CANVAS_MATRIX
varying vec2 wd;      // w = 0 instead of 1: a direction, not a place
varying vec2 m3;      // the last column of MODEL_MATRIX
void vertex() {
	l = VERTEX;
	w = (MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy;
	s = (CANVAS_MATRIX * MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy;
	sw = (MODEL_MATRIX * CANVAS_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy;
	wd = (MODEL_MATRIX * vec4(VERTEX, 0.0, 0.0)).xy;
	m3 = MODEL_MATRIX[3].xy;
}
vec4 enc(float v) {
	float i = floor(v * scale + 1024.0);
	return vec4(floor(i / 256.0) / 255.0, mod(i, 256.0) / 255.0, 0.0, 1.0);
}
void fragment() {
	float v = 0.0;
	if (which == 0) v = l.x;
	else if (which == 1) v = l.y;
	else if (which == 2) v = w.x;
	else if (which == 3) v = w.y;
	else if (which == 4) v = s.x;
	else if (which == 5) v = s.y;
	else if (which == 6) v = VERTEX.x;
	else if (which == 7) v = VERTEX.y;
	else if (which == 8) v = FRAGCOORD.x;
	else if (which == 9) v = FRAGCOORD.y;
	else if (which == 10) v = SCREEN_UV.x;
	else if (which == 11) v = SCREEN_UV.y;
	else if (which == 12) v = SCREEN_PIXEL_SIZE.x;
	else if (which == 13) v = SCREEN_PIXEL_SIZE.y;
	else if (which == 14) v = TEXTURE_PIXEL_SIZE.x;
	else if (which == 15) v = TEXTURE_PIXEL_SIZE.y;
	else if (which == 16) v = sw.x;
	else if (which == 17) v = sw.y;
	else if (which == 18) v = wd.x;
	else if (which == 19) v = wd.y;
	else if (which == 20) v = m3.x;
	else if (which == 21) v = m3.y;
	else if (which == 22) v = UV.x;
	else if (which == 23) v = UV.y;
	COLOR = enc(v);
}
"""

const NAMES := ["local.x", "local.y", "world.x", "world.y", "screen_by_matrices.x", "screen_by_matrices.y",
	"VERTEX_in_fragment.x", "VERTEX_in_fragment.y", "FRAGCOORD.x", "FRAGCOORD.y", "SCREEN_UV.x", "SCREEN_UV.y",
	"SCREEN_PIXEL_SIZE.x", "SCREEN_PIXEL_SIZE.y", "TEXTURE_PIXEL_SIZE.x", "TEXTURE_PIXEL_SIZE.y",
	"wrong_order_MODEL_x_CANVAS.x", "wrong_order_MODEL_x_CANVAS.y", "w0_direction.x", "w0_direction.y", "MODEL_MATRIX[3].x", "MODEL_MATRIX[3].y", "UV.x", "UV.y"]

var tree: SceneTree


func _init(t: SceneTree) -> void:
	tree = t


func frames(n: int) -> void:
	for i in range(n):
		await tree.process_frame


func grab() -> Image:
	RenderingServer.force_draw(false)
	return tree.root.get_texture().get_image()


func make_enc_material() -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = ENC
	var mat := ShaderMaterial.new()
	mat.shader = sh
	return mat


func decode(c: Color, scale: float) -> float:
	var hi := roundi(c.r * 255.0)
	var lo := roundi(c.g * 255.0)
	return (float(hi * 256 + lo) - 1024.0) / scale


# Reads one encoded number at pixel (px, py) from the current frame. `mat` must be on the node(s) that cover the pixel.
func read(mat: ShaderMaterial, which: int, scale: float, px: int, py: int) -> float:
	mat.set_shader_parameter("which", which)
	mat.set_shader_parameter("scale", scale)
	await frames(2)
	var img := grab()
	return decode(img.get_pixel(px, py), scale)


func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))


func white_texture(n: int) -> ImageTexture:
	var im := Image.create(n, n, false, Image.FORMAT_RGBA8)
	im.fill(Color.WHITE)
	return ImageTexture.create_from_image(im)
