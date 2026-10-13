shader_type canvas_item;

void fragment() {
	vec4 c = vec4(0.4, 0.7, 0.6, 1.0);
	vec3 a = c.rgb;
	vec2 b = c.xy;
	COLOR = vec4(b, a.b, 1.0);
}
