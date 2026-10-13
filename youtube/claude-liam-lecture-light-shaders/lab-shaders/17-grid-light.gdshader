shader_type canvas_item;

void light() {
	vec2 cell = mod(LIGHT_VERTEX.xy, 128.0);
	float lines = max(step(cell.x, 16.0), step(cell.y, 16.0));
	vec3 rgb = COLOR.rgb * LIGHT_COLOR.rgb * LIGHT_ENERGY * lines;
	LIGHT = vec4(rgb, LIGHT_COLOR.a);
}
