shader_type canvas_item;

uniform float flash_amount : hint_range(0.0, 1.0) = 0.0;
uniform vec4 flash_color : source_color = vec4(0.14510, 0.20784, 0.29020, 1.0);

void fragment() {
	vec4 col = texture(TEXTURE, UV); // sample the sprite texture explicitly
	col.rgb = mix(col.rgb, flash_color.rgb, flash_amount);
	COLOR = col;
}
