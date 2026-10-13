shader_type canvas_item;
// Not shown in the film. A reference answer to the film's "Your turn" prompt, to prove its two checks can be met:
// (1) thickness 0 draws nothing; (2) the ring is round on a square view and oval on a wide one.
uniform float radius : hint_range(0, 1) = 0.6;
uniform float thickness : hint_range(0, 1) = 0.3;

void fragment() {
	float d = distance(UV, vec2(0.5));
	float r = radius * 0.4;
	float t = thickness * 0.1;
	float ring = step(d, r + t) - step(d, r);
	COLOR = vec4(0.37, 0.64, 0.57, ring);
}
