shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture;
uniform float amount : hint_range(0.0, 1.0) = 1.0;

void fragment() {
	vec3 c = texture(screen_texture, SCREEN_UV).rgb;
	float gray = dot(c, vec3(0.299, 0.587, 0.114));
	COLOR.rgb = mix(c, vec3(gray), amount);
}
