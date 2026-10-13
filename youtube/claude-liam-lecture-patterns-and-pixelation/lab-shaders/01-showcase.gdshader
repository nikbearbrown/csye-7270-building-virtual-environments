shader_type canvas_item;

uniform float phase : hint_range(0.0, 1.0) = 0.0;

void fragment() {
	vec2 panel = floor(UV * 2.0);
	vec2 p = fract(UV * 2.0);
	vec3 teal = vec3(0.373, 0.639, 0.569);
	vec3 cream = vec3(0.980, 0.976, 0.961);
	vec3 gold = vec3(0.925, 0.769, 0.380);
	vec3 col = cream;
	if (panel.y < 0.5 && panel.x < 0.5) {
		float n = floor(mix(64.0, 12.0, phase));
		vec4 pic = texture(TEXTURE, (floor(p * n) + 0.5) / n);
		col = mix(cream, pic.rgb, pic.a);
	} else if (panel.y < 0.5) {
		vec2 cell = floor(p * 6.0 + vec2(phase * 6.0, 0.0));
		col = mix(teal, cream, mod(cell.x + cell.y, 2.0));
	} else if (panel.x < 0.5) {
		float f = fract((p.x + p.y) * 5.0 - phase * 5.0);
		col = mix(gold, cream, step(0.5, f));
	} else {
		float r = 0.15 + 0.3 * (0.5 + 0.5 * sin(phase * 12.566));
		col = mix(teal, cream, step(r, length(fract(p * 5.0) - 0.5)));
	}
	float inset = min(min(p.x, p.y), min(1.0 - p.x, 1.0 - p.y));
	COLOR = vec4(mix(vec3(0.851, 0.835, 0.792), col, step(0.015, inset)), 1.0);
}
