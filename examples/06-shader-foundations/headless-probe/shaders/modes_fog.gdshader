shader_type fog;
uniform float density : hint_range(0.0, 1.0) = 0.2;
void fog() { DENSITY = density; ALBEDO = vec3(1.0); }
