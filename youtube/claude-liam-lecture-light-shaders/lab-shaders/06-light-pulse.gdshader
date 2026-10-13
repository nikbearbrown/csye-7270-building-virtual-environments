shader_type canvas_item;

void light() {
	float pulse = abs(sin(TIME * 2.0));
	vec3 rgb = COLOR.rgb * LIGHT_COLOR.rgb * LIGHT_ENERGY * pulse;
	LIGHT = vec4(rgb, LIGHT_COLOR.a);
}
