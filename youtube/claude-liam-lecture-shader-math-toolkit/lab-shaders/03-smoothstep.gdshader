shader_type canvas_item;

uniform float width = 0.3;

void fragment() {
	float v = smoothstep(0.5 - width, 0.5 + width, UV.x);
	COLOR = vec4(vec3(v), 1.0);
}
