shader_type canvas_item;

void fragment() {
	float stripe = step(0.5, fract(SCREEN_UV.x * 20.0));
	COLOR.rgb = mix(COLOR.rgb, vec3(1.0), stripe);
}
