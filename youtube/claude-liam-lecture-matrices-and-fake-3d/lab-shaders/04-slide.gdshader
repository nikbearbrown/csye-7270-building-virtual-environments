shader_type canvas_item;

uniform vec2 slide = vec2(100.0, 0.0);

void vertex() {
	vec3 across = vec3(1.0, 0.0, 0.0);
	vec3 down = vec3(0.0, 1.0, 0.0);
	vec3 offset = vec3(slide, 1.0);
	VERTEX = (mat3(across, down, offset) * vec3(VERTEX, 1.0)).xy;
}
