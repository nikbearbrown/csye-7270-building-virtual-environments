shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture,
		repeat_disable, filter_nearest;
uniform float shift : hint_range(-0.5, 0.5) = 0.0;

void fragment() {
	vec2 spot = SCREEN_UV + vec2(shift, 0.0);
	COLOR.rgb = texture(screen_texture, spot).rgb;
}
