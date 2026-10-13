shader_type canvas_item;

void light() {
	vec3 rgb = COLOR.rgb * LIGHT_COLOR.rgb * LIGHT_ENERGY;
	float bands = floor(LIGHT_COLOR.a * 4.0) / 4.0;
	LIGHT = vec4(rgb, bands);
}
