shader_type canvas_item;

uniform float softness : hint_range(0.02, 0.4) = 0.15;

void fragment() {
	float width = max(softness, 0.01);
	float d = distance(UV, vec2(0.5));
	float body = 1.0 - smoothstep(0.4 - width, 0.4, d);
	COLOR = vec4(0.37, 0.64, 0.57, body);
}
