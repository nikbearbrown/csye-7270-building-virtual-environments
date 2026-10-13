shader_type canvas_item;

uniform sampler2D noise_tex;
uniform sampler2D ramp_tex : source_color;
uniform float progress : hint_range(0.0, 1.0) = 0.0;

void fragment() {
	float n = texture(noise_tex, UV).r;
	float cut = mix(-0.1, 1.0, progress);
	if (n <= cut) discard;
	float heat = 1.0 - (n - cut) / 0.1;
	vec3 fire = texture(ramp_tex, vec2(heat, 0.5)).rgb;
	if (heat > 0.0) COLOR.rgb = fire;
}
