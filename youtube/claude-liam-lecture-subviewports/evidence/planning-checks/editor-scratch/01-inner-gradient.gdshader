shader_type canvas_item;

void fragment() {
	vec4 tex = texture(TEXTURE, UV);
	vec3 gold = vec3(0.93, 0.76, 0.35);
	COLOR = vec4(mix(tex.rgb, gold, UV.y), tex.a);
}
