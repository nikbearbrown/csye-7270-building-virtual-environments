shader_type spatial;
render_mode unshaded;

uniform float activation : hint_range(0.0, 1.0) = 0.0;
uniform vec4 quiet_color : source_color = vec4(0.40, 0.16, 0.09, 1.0);
uniform vec4 active_color : source_color = vec4(0.12, 0.72, 0.52, 1.0);

void fragment() {
	ALBEDO = mix(quiet_color.rgb, active_color.rgb, activation);
}
