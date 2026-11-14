shader_type canvas_item;
// White hit flash: mixes the sprite's colour toward white, keeping its alpha (pillar 3: hits read muted).

uniform float flash : hint_range(0.0, 1.0) = 0.0;

void fragment() {
	vec4 tex = texture(TEXTURE, UV);
	COLOR = vec4(mix(tex.rgb, vec3(1.0), flash), tex.a);
}
