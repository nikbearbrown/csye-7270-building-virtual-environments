shader_type canvas_item;

uniform float wind : hint_range(0.0, 1.0) = 0.0;
uniform float amplitude = 0.06;
uniform float frequency = 3.0;
uniform float speed = 0.5;

void fragment() {
	float cycles = (UV.x - TIME * speed) * frequency;
	float wave = amplitude * wind * sin(TAU * cycles) * UV.x;
	COLOR = texture(TEXTURE, vec2(UV.x, UV.y + wave));
}
