shader_type canvas_item;

uniform vec3 tint : source_color;
uniform float speed = 2.0;

vec3 breathe(vec3 base, float t) {
	float wave = 0.5 + 0.5 * sin(t);
	return mix(vec3(0.9), base, wave);
}

void fragment() {
	vec3 color = breathe(tint.rgb, TIME * speed);
	COLOR = vec4(color, tint.a);
}
