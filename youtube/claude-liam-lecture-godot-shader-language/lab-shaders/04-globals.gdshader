shader_type canvas_item;

uniform float level = 0.8;
const vec3 TEAL = vec3(0.37, 0.64, 0.57);
varying vec2 corner_uv;

void vertex() {
	corner_uv = UV;
}

void fragment() {
	COLOR = vec4(TEAL * level * (0.5 + 0.5 * corner_uv.x), 1.0);
}
