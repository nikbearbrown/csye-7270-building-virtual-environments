shader_type spatial;
render_mode unshaded;

uniform sampler2D mask;
uniform vec3 cream : source_color = vec3(0.98, 0.98, 0.96);
uniform vec3 teal : source_color = vec3(0.37, 0.64, 0.57);

void fragment() {
	float cut = step(0.5, texture(mask, UV).r);
	ALBEDO = mix(cream, teal, cut);
}
