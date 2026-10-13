shader_type canvas_item;

void light() {
	vec3 rgb = COLOR.rgb * LIGHT_COLOR.rgb * LIGHT_ENERGY;
	LIGHT = vec4(rgb, LIGHT_COLOR.a);
}
