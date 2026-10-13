shader_type canvas_item;

void fragment() {
	float gray = COLOR.r;
	COLOR.rgb = vec3(gray);
}
