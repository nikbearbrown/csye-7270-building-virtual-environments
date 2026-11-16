// 09_cube_mapped.gdshader
//
// SOURCE     shader_lessons/09_cube_mapped.cgfx  
// WHAT THE ORIGINAL DID
//   The 05 Phong model (no colour, spec or normal maps) plus an environment (cube) map read along the reflection vector.
//   The cube-map colour is multiplied by the RIM term and added to the specular: total_spec = fresnel * cube + specular.
// WHAT CHANGED
//   - samplerCUBE / texCUBE -> samplerCube / texture(). The world-space reflection vector indexes the cube map directly. Godot needs a
//     Cubemap resource: the six PNGs in textures/ (cube_px ... cube_nz) are assembled into one by scripts/lessons.gd with
//     Cubemap.create_from_images(), faces in the order +X, -X, +Y, -Y, +Z, -Z. Face orientation was verified by running (traps).
//   - WrapR/S/T = ClampToEdge: cubes are sampled without repeat in Godot (nothing to set).
//   - The original's vertex shader passed texCoord along; this pixel shader never reads it: dropped.
// FINDING  the header says "basic phong shader with an added cube map", but because the cube map is weighted by the rim term, a
//   surface that faces the camera shows NO reflection at all; it only appears toward the silhouette. See CONVERSION-NOTES.md.

shader_type spatial;
render_mode unshaded;

uniform vec3 shader_color : source_color = vec3(1.0);
uniform vec3 light_direction = vec3(0.5, -0.8, -0.6);   // direction the light travels, world space
uniform vec3 ambient_color : source_color = vec3(0.15);
uniform float fresnel_power : hint_range(0.0, 10.0, 0.01) = 3.0;
uniform float specular_power : hint_range(0.1, 100.0, 0.01) = 30.0;
uniform vec3 specular_color : source_color = vec3(1.0);
uniform samplerCube reflection_map : source_color, filter_linear;

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

	vec3 cube_map = texture(reflection_map, r).rgb;

	vec3 lambert = vec3(clamp(dot(l, n), 0.0, 1.0));
	vec3 specular = pow(clamp(dot(r, l), 0.0, 1.0), specular_power) * specular_color;
	vec3 fresnel = pow(1.0 - clamp(dot(e, n), 0.0, 1.0), fresnel_power) * (lambert + ambient_color);
	vec3 total_spec = (fresnel * cube_map) + specular;

	ALBEDO = (lambert + ambient_color) * shader_color + total_spec;
}
