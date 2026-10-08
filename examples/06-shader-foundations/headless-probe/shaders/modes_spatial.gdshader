shader_type spatial;
uniform sampler2D albedo_tex : source_color;
uniform sampler2D normal_tex : hint_normal;
void vertex() { VERTEX.y += sin(TIME) * 0.1; }
void fragment() { ALBEDO = texture(albedo_tex, UV).rgb; NORMAL_MAP = texture(normal_tex, UV).rgb; ROUGHNESS = 0.5; }
void light() { DIFFUSE_LIGHT += clamp(dot(NORMAL, LIGHT), 0.0, 1.0) * ATTENUATION * LIGHT_COLOR; }
