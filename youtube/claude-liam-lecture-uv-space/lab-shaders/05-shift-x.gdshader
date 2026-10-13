shader_type canvas_item;

uniform float amount = 0.0;

void fragment() {
	vec2 uv = UV;
	uv.x -= amount;
	COLOR = texture(TEXTURE, uv);
}
