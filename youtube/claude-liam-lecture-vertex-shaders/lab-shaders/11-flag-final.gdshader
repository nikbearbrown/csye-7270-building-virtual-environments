shader_type canvas_item;

uniform float amplitude = 24.0;
uniform float frequency = 8.0;
uniform float speed = 3.0;

void vertex() {
	float phase = UV.x * frequency - TIME * speed;
	VERTEX.y += sin(phase) * amplitude * UV.x;
	COLOR.rgb *= 0.9 + 0.1 * cos(phase) * UV.x;
}
