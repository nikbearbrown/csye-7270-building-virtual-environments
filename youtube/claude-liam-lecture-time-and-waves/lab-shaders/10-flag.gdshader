shader_type canvas_item;

uniform float amplitude = 0.05;
uniform float frequency = 3.0;
uniform float speed = 0.5;
uniform float offset = 0.0;

void fragment() {
	float cycles = (UV.x - TIME * speed) * frequency + offset;
	float wave = amplitude * sin(TAU * cycles) * UV.x;
	COLOR = texture(TEXTURE, vec2(UV.x, UV.y + wave));
}
