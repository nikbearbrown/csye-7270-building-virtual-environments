shader_type canvas_item;

uniform float flip : hint_range(0.0, 1.0) = 0.0;
uniform float tip : hint_range(0.0, 0.5) = 0.1;

mat3 around_x(float a) {
	vec3 x_arrow = vec3(1.0, 0.0, 0.0);
	vec3 y_arrow = vec3(0.0, cos(a), sin(a));
	vec3 z_arrow = vec3(0.0, -sin(a), cos(a));
	return mat3(x_arrow, y_arrow, z_arrow);
}

mat3 around_y(float a) {
	vec3 x_arrow = vec3(cos(a), 0.0, -sin(a));
	vec3 y_arrow = vec3(0.0, 1.0, 0.0);
	vec3 z_arrow = vec3(sin(a), 0.0, cos(a));
	return mat3(x_arrow, y_arrow, z_arrow);
}

void vertex() {
	mat3 m = around_x(TAU * tip) * around_y(TAU * flip);
	VERTEX = (m * vec3(VERTEX, 0.0)).xy;
}
