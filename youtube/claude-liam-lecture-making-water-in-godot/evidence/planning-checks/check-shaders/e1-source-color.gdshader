shader_type spatial;
render_mode unshaded;
uniform vec3 typed : source_color = vec3(0.10, 0.45, 0.70);
uniform vec3 plain = vec3(0.10, 0.45, 0.70);
uniform float use_plain = 0.0;
void fragment() { ALBEDO = mix(typed, plain, use_plain); }
