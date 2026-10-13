shader_type canvas_item;

uniform float amplitude = 24.0;
uniform float frequency = 8.0;
uniform float speed = 3.0;

void vertex() {
	VERTEX.y += sin(UV.x * frequency - TIME * speed) * amplitude * UV.x;
}
