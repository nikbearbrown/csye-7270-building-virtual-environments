shader_type canvas_item;

uniform sampler2D pic : repeat_enable;
uniform float shift = 0.0;
uniform float zoom = 1.0;

void fragment() {
	vec2 uv = UV;
	uv.x += shift;
	uv *= zoom;
	COLOR = texture(pic, uv);
}
