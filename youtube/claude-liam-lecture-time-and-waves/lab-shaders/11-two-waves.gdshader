shader_type canvas_item;

void fragment() {
	float big = 0.04 * sin(TAU * (UV.x - TIME * 0.4) * 2.0);
	float small = 0.015 * sin(TAU * (UV.x - TIME * 0.7) * 5.0);
	COLOR = texture(TEXTURE, vec2(UV.x, UV.y + big + small));
}
