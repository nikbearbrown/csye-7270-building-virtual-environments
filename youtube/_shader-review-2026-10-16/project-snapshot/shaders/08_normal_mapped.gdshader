// 08_normal_mapped.gdshader
//
// SOURCE     shader_lessons/08_normal_mapped.cgfx  
//
// WHAT THE ORIGINAL DID
//   07 plus a tangent-space normal map. The map's RGB is unpacked (x * 2 - 1) and used as weights on three world-space vectors,
//   the surface tangent, binormal and normal; the sum (normalised) replaces the vertex normal in ALL the lighting terms.
// WHAT CHANGED
//   - Tangent and binormal: Cg mul(WorldInverseTranspose, tangent / binormal); here MODEL_NORMAL_MATRIX * TANGENT / BINORMAL, the same
//     matrix applied the same way. (For tangents the usual choice is the model matrix itself; the two agree for uniform scale.)
//     Godot's built-in meshes supply TANGENT with the right sign in tangent.w and BINORMAL = cross(NORMAL, TANGENT) * w (measured).
//   - GREEN CHANNEL CONVENTION: the Cg adds + green * binormal. In Godot BINORMAL points up the image (the direction v DEcreases),
//     so a map that is "green = up" (OpenGL / Maya style) works as written. A DirectX-style map (green = down) needs the green
//     flipped; lesson 15 does that (see there). The map bundled here is textures/normal_gl.png.
//   - The normal map sampler has NO source_color hint (it holds vectors, not colours): hinting it bends every normal (measured in traps).
//   - Cg's  .rgb * 2 - 1;;  (double semicolon) is a harmless typo of the original.
// FINDING  see CONVERSION-NOTES.md.

shader_type spatial;
render_mode unshaded;

uniform vec3 shader_color : source_color = vec3(1.0);
uniform vec3 light_direction = vec3(0.5, -0.8, -0.6);   // direction the light travels, world space
uniform vec3 ambient_color : source_color = vec3(0.15);
uniform float fresnel_power : hint_range(0.0, 10.0, 0.01) = 3.0;
uniform float specular_power : hint_range(0.1, 100.0, 0.01) = 30.0;
uniform vec3 specular_color : source_color = vec3(1.0);
uniform sampler2D diffuse_map : source_color, hint_default_white, filter_linear_mipmap, repeat_enable;
uniform sampler2D spec_map : hint_default_white, filter_linear_mipmap, repeat_enable;      // R = rim mask, G = specular mask
uniform sampler2D normal_map : hint_normal, filter_linear_mipmap, repeat_enable;           // tangent space, green = up (OpenGL / Maya style)

varying vec3 world_normal;
varying vec3 world_tangent;
varying vec3 world_binormal;
varying vec3 eye_vector;

void vertex() {
	world_normal = MODEL_NORMAL_MATRIX * NORMAL;
	world_tangent = MODEL_NORMAL_MATRIX * TANGENT;
	world_binormal = MODEL_NORMAL_MATRIX * BINORMAL;
	vec3 world_pos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	vec3 world_camera_pos = INV_VIEW_MATRIX[3].xyz;
	eye_vector = world_camera_pos - world_pos;
}

void fragment() {
	// normal mapping: unpack, then weight tangent / binormal / normal
	vec3 tn = texture(normal_map, UV).rgb * 2.0 - 1.0;
	vec3 n = normalize(tn.x * world_tangent + tn.y * world_binormal + tn.z * world_normal);

	vec3 l = normalize(-light_direction);
	vec3 e = normalize(eye_vector);
	vec3 r = -reflect(e, n);

	vec4 color_map = texture(diffuse_map, UV);
	vec4 specular_map = texture(spec_map, UV);

	vec3 lambert = vec3(clamp(dot(l, n), 0.0, 1.0));
	vec3 specular = pow(clamp(dot(r, l), 0.0, 1.0), specular_power) * specular_color;
	vec3 fresnel = vec3(pow(1.0 - clamp(dot(e, n), 0.0, 1.0), fresnel_power));
	vec3 total_spec = (fresnel * specular_map.r) + (specular * specular_map.g);

	ALBEDO = (lambert + ambient_color) * (shader_color * color_map.rgb) + total_spec;
}
