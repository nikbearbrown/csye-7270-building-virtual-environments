shader_type canvas_item;

uniform float angle = 1.5708;
uniform vec2 slide = vec2(100.0, 0.0);

mat3 turn_by(float a) {
	vec3 across = vec3(cos(a), sin(a), 0.0);
	vec3 down = vec3(-sin(a), cos(a), 0.0);
	return mat3(across, down, vec3(0.0, 0.0, 1.0));
}

mat3 slide_by(vec2 t) {
	vec3 across = vec3(1.0, 0.0, 0.0);
	vec3 down = vec3(0.0, 1.0, 0.0);
	return mat3(across, down, vec3(t, 1.0));
}

void vertex() {
	mat3 m = slide_by(slide) * turn_by(angle);
	VERTEX = (m * vec3(VERTEX, 1.0)).xy;
}
