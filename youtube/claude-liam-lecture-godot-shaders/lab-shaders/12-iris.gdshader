shader_type canvas_item;

uniform float radius : hint_range(0.0, 0.8) = 0.0;

void fragment() {
	if (distance(UV, vec2(0.5)) > radius) {
		discard;
	}
	COLOR = texture(TEXTURE, UV);
}
