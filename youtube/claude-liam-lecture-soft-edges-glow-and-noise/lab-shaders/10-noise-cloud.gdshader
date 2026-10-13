shader_type canvas_item;

uniform sampler2D noise : repeat_enable;

void fragment() {
	float d = distance(UV, vec2(0.5));
	float disc = 1.0 - smoothstep(0.25, 0.4, d);
	float n = texture(noise, UV).r;
	COLOR = vec4(0.37, 0.64, 0.57, disc * n);
}
