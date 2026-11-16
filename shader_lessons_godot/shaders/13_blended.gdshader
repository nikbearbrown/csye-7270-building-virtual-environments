// 13_blended.gdshader
//
// SOURCE     shader_lessons/13_blended.cgfx 
// WHAT THE ORIGINAL DID
//   Lighting from 05 (Lambert + ambient + rim + Phong, no maps for the lighting) with a COLOUR chosen per pixel by a blend map:
//     colour = shaderColor * blend.r + blendedColor * blend.b + thirdColor * blend.g
//   Note the channel order: red picks the first colour, BLUE picks the second ("blended"), GREEN picks the third. Defaults: red, blue, green.
// WHAT CHANGED
//   - The blend map has no source_color hint: it is a set of weights. (If it was painted as colours and saved as a colour picture, the
//     decision to hint it or not changes every weight in between; see CONVERSION-NOTES.md.)
//   - The three colour uniforms are colour pickers (source_color), as in the original's ": Diffuse".
//   - The outColor.a = fresnel line of the Cg is dropped (Opaque technique: alpha unused).
// FINDING  see CONVERSION-NOTES.md.

shader_type spatial;
render_mode unshaded;

uniform vec3 shader_color : source_color = vec3(1.0, 0.0, 0.0);
uniform vec3 blended_color : source_color = vec3(0.0, 0.0, 1.0);
uniform vec3 third_color : source_color = vec3(0.0, 1.0, 0.0);
uniform vec3 light_direction = vec3(0.5, -0.8, -0.6);   // direction the light travels, world space
uniform vec3 ambient_color : source_color = vec3(0.15);
uniform float fresnel_power : hint_range(0.0, 10.0, 0.01) = 3.0;
uniform float specular_power : hint_range(0.1, 100.0, 0.01) = 30.0;
uniform vec3 specular_color : source_color = vec3(1.0);
uniform sampler2D blend_map : hint_default_white, filter_linear_mipmap, repeat_enable;

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

	vec3 blend = texture(blend_map, UV).rgb;
	vec3 final_color = shader_color * blend.r + blended_color * blend.b + third_color * blend.g;

	vec3 lambert = vec3(clamp(dot(l, n), 0.0, 1.0));
	vec3 specular = pow(clamp(dot(r, l), 0.0, 1.0), specular_power) * specular_color;
	vec3 fresnel = pow(1.0 - clamp(dot(e, n), 0.0, 1.0), fresnel_power) * (lambert + ambient_color);
	vec3 total_spec = fresnel + specular;

	ALBEDO = (lambert + ambient_color) * final_color + total_spec;
}
