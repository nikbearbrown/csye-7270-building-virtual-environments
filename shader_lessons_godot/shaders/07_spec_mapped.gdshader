// 07_spec_mapped.gdshader
//
// SOURCE     shader_lessons/07_spec_mapped.cgfx  
//
// WHAT THE ORIGINAL DID
//   06 plus a second texture, the "spec map", used as a per-channel mask: its RED channel scales the rim term and its GREEN
//   channel scales the Phong highlight (blue is unused). Texture-controlled shininess.
// WHAT CHANGED
//   - Second sampler, no source_color hint: it holds masks (numbers), not colours. Hinting a mask as a colour would convert it
//     to linear light: a 0.5 mask would arrive as about 0.21 (computed from the sRGB curve; the conversion itself was measured on a texel, see CONVERSION-NOTES.md T8).
//   - Cg declared the colour texture as "Cube" again (see 06): dropped.
// FINDING  06 multiplies the rim by (lambert + ambient); here the rim is NOT multiplied by the lighting any more (the Cg line
//   changed between 06 and 07), so the rim glows on the dark side too. Kept as written. See CONVERSION-NOTES.md.

shader_type spatial;
render_mode unshaded;

uniform vec3 shader_color : source_color = vec3(1.0);
uniform vec3 light_direction = vec3(0.5, -0.8, -0.6);   // direction the light travels, world space
uniform vec3 ambient_color : source_color = vec3(0.15);
uniform float fresnel_power : hint_range(0.0, 10.0, 0.01) = 3.0;
uniform float specular_power : hint_range(0.1, 100.0, 0.01) = 30.0;
uniform vec3 specular_color : source_color = vec3(1.0);
uniform sampler2D diffuse_map : source_color, hint_default_white, filter_linear_mipmap, repeat_enable;
uniform sampler2D spec_map : hint_default_white, filter_linear_mipmap, repeat_enable;   // R = rim mask, G = specular mask

varying vec3 world_normal;
varying vec3 eye_vector;

void vertex() {
	world_normal = MODEL_NORMAL_MATRIX * NORMAL;
	vec3 world_pos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	vec3 world_camera_pos = INV_VIEW_MATRIX[3].xyz;
	eye_vector = world_camera_pos - world_pos;
}

void fragment() {
	vec3 n = normalize(world_normal);
	vec3 l = normalize(-light_direction);
	vec3 e = normalize(eye_vector);
	vec3 r = -reflect(e, n);

	vec4 color_map = texture(diffuse_map, UV);
	vec4 specular_map = texture(spec_map, UV);

	vec3 lambert = vec3(clamp(dot(l, n), 0.0, 1.0));
	vec3 specular = pow(clamp(dot(r, l), 0.0, 1.0), specular_power) * specular_color;
	vec3 fresnel = vec3(pow(1.0 - clamp(dot(e, n), 0.0, 1.0), fresnel_power));   // no (lambert + ambient) factor here, unlike 04 to 06
	vec3 total_spec = (fresnel * specular_map.r) + (specular * specular_map.g);

	ALBEDO = (lambert + ambient_color) * (shader_color * color_map.rgb) + total_spec;
}
