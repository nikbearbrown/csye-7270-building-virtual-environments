shader_type canvas_item;

void fragment() {
	vec4 tex = texture(TEXTURE, UV);
	vec3 red = vec3(0.85, 0.22, 0.2);
	COLOR = vec4(mix(tex.rgb, red, step(0.5, UV.y)), tex.a);
}
