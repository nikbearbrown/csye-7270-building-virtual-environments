shader_type canvas_item;

void fragment() {
	float x = abs(UV.x - 0.5);
	float y = abs(UV.y - 0.5);
	float d = distance(UV, vec2(0.5));
	float plus = max(step(x, 0.03), step(y, 0.03));
	float gap = step(d, 0.2);
	float blob = step(d, 0.1);
	float mask = max(plus - gap, 0.0) + blob;
	COLOR = vec4(0.37, 0.64, 0.57, mask);
}
