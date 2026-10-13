shader_type canvas_item;

uniform float flip : hint_range(0.0, 1.0) = 0.0;
uniform vec2 pivot = vec2(-64.0, 0.0);

void vertex() {
	float a = TAU * flip;
	vec3 x_arrow = vec3(cos(a), 0.0, -sin(a));
	vec3 y_arrow = vec3(0.0, 1.0, 0.0);
	vec3 z_arrow = vec3(sin(a), 0.0, cos(a));
	vec3 p = vec3(VERTEX - pivot, 0.0);
	p = mat3(x_arrow, y_arrow, z_arrow) * p;
	VERTEX = p.xy + pivot;
}
