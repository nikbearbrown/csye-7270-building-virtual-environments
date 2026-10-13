shader_type canvas_item;

uniform float power = 1.0;

void fragment() {
	float v = pow(UV.x, power);
	COLOR = vec4(vec3(v), 1.0);
}
