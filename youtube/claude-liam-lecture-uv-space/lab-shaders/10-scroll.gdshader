shader_type canvas_item;

uniform sampler2D pic : repeat_enable;

void fragment() {
	vec2 uv = UV;
	uv.x += TIME * 0.1;
	COLOR = texture(pic, uv);
}
