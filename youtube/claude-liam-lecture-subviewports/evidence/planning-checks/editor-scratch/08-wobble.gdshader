shader_type canvas_item;
render_mode blend_premul_alpha;

uniform float amplitude = 16.0;
uniform float frequency = 10.0;
uniform float speed = 3.0;

void vertex() {
	VERTEX.y += sin(UV.x * frequency + TIME * speed) * amplitude;
}

void fragment() {
	COLOR = texture(TEXTURE, UV);
}
