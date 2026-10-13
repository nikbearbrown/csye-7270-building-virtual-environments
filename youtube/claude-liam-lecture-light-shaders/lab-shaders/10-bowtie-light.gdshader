shader_type canvas_item;

void light() {
	float mask = step(0.9, abs(LIGHT_DIRECTION.x));
	vec3 rgb = COLOR.rgb * LIGHT_COLOR.rgb * LIGHT_ENERGY * mask;
	LIGHT = vec4(rgb, LIGHT_COLOR.a);
}
