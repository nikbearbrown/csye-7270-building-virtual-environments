shader_type canvas_item;

uniform float radius : hint_range(0, 0.5) = 0.3;

void fragment() {
	float d = distance(UV, vec2(0.5));
	float inside = step(d, radius);
	COLOR = vec4(0.37, 0.64, 0.57, inside);
}
