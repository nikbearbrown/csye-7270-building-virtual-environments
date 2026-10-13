shader_type canvas_item;

uniform float sweep = 0.0;

void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	float t = fract(atan(p.y, p.x) / TAU + 0.25);
	if (t < sweep) {
		COLOR = texture(TEXTURE, UV);
	} else {
		COLOR = vec4(0.0);
	}
}
