shader_type canvas_item;

uniform vec3 body_color : source_color = vec3(0.37, 0.64, 0.57);
uniform vec3 highlight_color : source_color = vec3(0.55, 0.52, 0.45);
uniform float glow : hint_range(0.0, 1.0) = 0.0;

void fragment() {
	float d = distance(UV, vec2(0.5));
	float disc = 1.0 - smoothstep(0.25, 0.4, d);
	float spot = clamp(1.0 - distance(UV, vec2(0.35)), 0.0, 1.0);
	float highlight = pow(spot, 3.0);
	vec3 rgb = body_color + highlight_color * highlight;
	COLOR = vec4(rgb * (1.0 + glow * 5.0), disc);
}
