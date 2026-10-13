shader_type canvas_item;

void fragment() {
	vec3 c = mix(vec3(0.9), vec3(0.4), 1);
	COLOR = vec4(c, 1.0);
}
