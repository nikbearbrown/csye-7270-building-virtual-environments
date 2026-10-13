shader_type canvas_item;

void vertex() {
	corner_uv = UV;
}

varying vec2 corner_uv;

void fragment() {
	COLOR = vec4(corner_uv, 0.5, 1.0);
}
