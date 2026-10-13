shader_type canvas_item;

void fragment() {
	COLOR.rgb = vec3(FRAGCOORD.xy * SCREEN_PIXEL_SIZE, 0.8);
}
