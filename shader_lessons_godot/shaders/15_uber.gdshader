// 15_uber.gdshader
//
// SOURCE     shader_lessons/15_uber.cgfx 
// WHAT THE ORIGINAL DID
//   The final shader: everything so far, rebuilt.
//   - Ambient is a two-colour HEMISPHERE blend, not one grey: mix(bottomColor, topColor, saturate(dot(up, normal))). Anything facing
//     down or sideways-down gets bottomColor; the top colour fades in only above the horizon.
//   - A fake subsurface: lambert = saturate(dot(L,N) * (1 - spread) + spread + subsurfaceColor). subsurfaceColor is a vec3 ADDED inside
//     the saturate, so with the default (0.1, 0, 0) the dark side is a faint red instead of black; spread softens the terminator.
//   - lightColor scales the diffuse and the rim.  Normal map, colour map, spec map and cube map are all used.
//   - The spec map is packed DIFFERENTLY from 07/08: RED masks the Phong highlight, BLUE masks the reflection (the rim is not masked).
//   - Reflection = pow(cube, contrast) * intensity * specMap.b, added after the rim and specular.
// WHAT CHANGED
//   - Normal map green channel: the Cg uses  worldNormal.y * -binormal  (minus). 08 does not. A minus there means this file's maps were
//     DirectX-style (green = down); 08's work as OpenGL-style. Kept as the uniform flip_green, default TRUE (as written in the Cg);
//     the stage binds textures/normal_dx.png (the same height field, green inverted) to this lesson so it looks right.
//   - Cg lerp -> mix, saturate -> clamp, pow(vec3, float) -> pow(vec3, vec3(float)).
//   - The ambientColor local of the Cg is renamed ambient; the commented-out debug line of the original is not carried over.
//   - The texture reads and the cube read as in 08 / 09.
// FINDING  see CONVERSION-NOTES.md.

shader_type spatial;
render_mode unshaded;

uniform vec3 shader_color : source_color = vec3(1.0);
uniform vec3 light_direction = vec3(0.5, -0.8, -0.6);   // direction the light travels, world space
uniform vec3 light_color : source_color = vec3(1.0);
uniform vec3 top_color : source_color = vec3(0.15);
uniform vec3 bottom_color : source_color = vec3(0.0);
uniform float fresnel_power : hint_range(0.0, 10.0, 0.01) = 3.0;
uniform float specular_power : hint_range(0.1, 100.0, 0.01) = 30.0;
uniform vec3 specular_color : source_color = vec3(1.0);
uniform vec3 subsurface_color : source_color = vec3(0.1, 0.0, 0.0);
uniform float subsurface_spread : hint_range(0.0, 1.0, 0.01) = 0.0;
uniform float reflection_intensity : hint_range(0.0, 10.0, 0.01) = 1.0;
uniform float reflection_contrast : hint_range(0.0, 10.0, 0.01) = 1.0;
uniform bool flip_green = true;   // the Cg's  * -binormal
uniform sampler2D diffuse_map : source_color, hint_default_white, filter_linear_mipmap, repeat_enable;
uniform sampler2D spec_map : hint_default_white, filter_linear_mipmap, repeat_enable;   // R = specular mask, B = reflection mask
uniform sampler2D normal_map : hint_normal, filter_linear_mipmap, repeat_enable;        // tangent space; the Cg expects green = down
uniform samplerCube reflection_map : source_color, filter_linear;

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
	vec3 tn = texture(normal_map, UV).rgb * 2.0 - 1.0;
	vec3 binormal = flip_green ? -world_binormal : world_binormal;
	vec3 n = normalize(tn.x * world_tangent + tn.y * binormal + tn.z * world_normal);

	vec3 l = normalize(-light_direction);
	vec3 e = normalize(eye_vector);
	vec3 r = -reflect(e, n);
	vec3 cube_map = texture(reflection_map, r).rgb;

	vec4 color_map = texture(diffuse_map, UV);
	vec4 specular_map = texture(spec_map, UV);

	vec3 ambient = mix(bottom_color, top_color, clamp(dot(vec3(0.0, 1.0, 0.0), n), 0.0, 1.0));

	vec3 lambert = clamp((dot(l, n) * (1.0 - subsurface_spread) + subsurface_spread) + subsurface_color, 0.0, 1.0);

	vec3 specular = pow(clamp(dot(r, l), 0.0, 1.0), specular_power) * specular_color * specular_map.r;

	vec3 fresnel = pow(1.0 - clamp(dot(e, n), 0.0, 1.0), fresnel_power) * lambert * light_color;

	vec3 total_spec = (fresnel + specular) + (pow(cube_map, vec3(reflection_contrast)) * reflection_intensity * specular_map.b);

	ALBEDO = (ambient + light_color * lambert) * (shader_color * color_map.rgb) + total_spec;
}
