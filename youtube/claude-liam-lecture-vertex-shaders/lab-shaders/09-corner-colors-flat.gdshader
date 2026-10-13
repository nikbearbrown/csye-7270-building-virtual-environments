shader_type canvas_item;

varying flat vec3 tint;

void vertex() {
	tint = vec3(UV.x, UV.y, 1.0 - UV.x);
}

void fragment() {
	COLOR = vec4(tint, 1.0);
}
