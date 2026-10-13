shader_type canvas_item;

void light() {
	float across = LIGHT_DIRECTION.x * 0.5 + 0.5;
	vec3 rgb = COLOR.rgb * LIGHT_COLOR.rgb * LIGHT_ENERGY * across;
	LIGHT = vec4(rgb, LIGHT_COLOR.a);
}
