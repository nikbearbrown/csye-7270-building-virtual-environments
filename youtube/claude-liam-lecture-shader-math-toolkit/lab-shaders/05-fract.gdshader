shader_type canvas_item;

uniform float count = 4.0;

void fragment() {
	float v = fract(UV.x * count);
	COLOR = vec4(vec3(v), 1.0);
}
