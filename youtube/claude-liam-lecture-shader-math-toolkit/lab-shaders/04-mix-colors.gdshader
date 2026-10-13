shader_type canvas_item;

void fragment() {
	vec3 teal = vec3(0.37, 0.64, 0.57);
	vec3 gold = vec3(0.96, 0.80, 0.45);
	COLOR = vec4(mix(teal, gold, UV.x), 1.0);
}
