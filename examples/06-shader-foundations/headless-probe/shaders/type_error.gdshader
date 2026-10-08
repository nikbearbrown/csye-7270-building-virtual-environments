shader_type canvas_item;

uniform float flash_amount : hint_range(0.0, 1.0) = 0.0;

void fragment() {
	vec3 c = texture(TEXTURE, UV);
	COLOR = vec4(c, 1.0);
}
