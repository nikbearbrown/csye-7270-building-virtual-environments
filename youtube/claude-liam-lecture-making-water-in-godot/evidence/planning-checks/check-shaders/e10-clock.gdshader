shader_type spatial;
render_mode unshaded;
// E10: shows the shader's TIME as a colour: red = fract(TIME / 4)  (a 4 second period).
void fragment() { ALBEDO = vec3(fract(TIME * 0.25)); }
