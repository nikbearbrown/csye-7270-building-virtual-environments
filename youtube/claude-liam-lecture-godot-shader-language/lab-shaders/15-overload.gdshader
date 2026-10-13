shader_type canvas_item;

vec3 get_color(int t) {
	return vec3(0.37, 0.64, 0.57);
}
vec3 get_color(float t) {
	return vec3(0.95, 0.80, 0.50);
}

void fragment() {
	vec3 left = get_color(1);
	vec3 right = get_color(1.0);
	COLOR = vec4(UV.x < 0.5 ? left : right, 1.0);
}
