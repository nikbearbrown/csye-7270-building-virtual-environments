shader_type canvas_item;

/* A note for people,
   over two lines. */
void fragment() {
	vec3 c = vec3(UV, 0.5);
	// c = 0.4 + 0.6 * c; // soften
	COLOR = vec4(c, 1.0);
}
