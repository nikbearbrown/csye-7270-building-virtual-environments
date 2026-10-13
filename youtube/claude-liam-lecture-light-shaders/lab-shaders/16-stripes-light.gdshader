shader_type canvas_item;

void light() {
	float stripe = step(mod(LIGHT_VERTEX.x, 128.0), 16.0);
	vec3 rgb = COLOR.rgb * LIGHT_COLOR.rgb * LIGHT_ENERGY * stripe;
	LIGHT = vec4(rgb, LIGHT_COLOR.a);
}
