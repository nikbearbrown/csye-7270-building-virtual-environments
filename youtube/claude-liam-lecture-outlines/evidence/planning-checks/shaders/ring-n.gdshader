shader_type canvas_item;
// check shader: the ring outline with a chosen number of reads (same maths as lab-shaders/08-ring.gdshader, count set by a uniform)
uniform vec4 line_color : source_color = vec4(0.25, 0.25, 0.75, 1.0);
uniform float thickness : hint_range(0.0, 16.0) = 1.0;
uniform int samples = 16;

void fragment() {
	float around = 0.0;
	for (int i = 0; i < samples; i++) {
		float angle = TAU * float(i) / float(samples);
		vec2 dir = vec2(cos(angle), sin(angle));
		around += texture(TEXTURE, UV + dir * TEXTURE_PIXEL_SIZE * thickness).a;
	}
	vec4 color = texture(TEXTURE, UV);
	COLOR = mix(color, line_color, min(around, 1.0) * (1.0 - color.a));
}
