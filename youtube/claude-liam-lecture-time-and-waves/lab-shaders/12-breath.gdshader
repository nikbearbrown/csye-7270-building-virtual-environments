shader_type canvas_item;

uniform sampler2D curve;

void fragment() {
	float k = texture(curve, vec2(fract(TIME * 0.4), 0.0)).r;
	float scale = 1.0 + 0.25 * k;
	vec2 uv = (UV - 0.5) / scale + 0.5;
	COLOR = texture(TEXTURE, uv);
}
