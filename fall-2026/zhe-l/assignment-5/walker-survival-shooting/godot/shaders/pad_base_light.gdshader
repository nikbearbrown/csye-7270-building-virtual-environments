shader_type spatial;
render_mode unshaded;
uniform vec4 cold_white: source_color = vec4(0.902, 0.969, 0.969, 1.0);
uniform float pad_light_data:hint_range(0.0, 1.0) = 0.0;
void fragment(){
	ALBEDO = mix(vec3(0.0), cold_white.rgb, pad_light_data);
}