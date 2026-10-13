shader_type spatial;

uniform float roughness : hint_range(0.0, 1.0) = 0.5;
uniform float metallic : hint_range(0.0, 1.0) = 0.0;
uniform float glow : hint_range(0.0, 1.0) = 0.0;
uniform float alpha : hint_range(0.0, 1.0) = 1.0;

void fragment() {
	ALBEDO = vec3(0.37, 0.64, 0.57);
	ROUGHNESS = roughness;
	METALLIC = metallic;
	EMISSION = vec3(0.9, 0.5, 0.1) * glow;
	ALPHA = alpha;
}
