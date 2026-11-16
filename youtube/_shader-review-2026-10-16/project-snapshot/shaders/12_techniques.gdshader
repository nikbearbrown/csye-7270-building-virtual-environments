// 12_techniques.gdshader
//
// SOURCE     shader_lessons/12_techniques.cgfx  
// WHAT THE ORIGINAL DID
//   The 08 model (colour, spec and normal maps) with the rim term also written to the pixel's ALPHA, and FOUR techniques that wrap the
//   same two programs in different render states:
//     Opaque      no states: alpha is ignored
//     AlphaBlend  blending on, back faces culled: the rim becomes transparency (centre clear, silhouette solid)
//     AlphaTest   alpha test GREATER 0.3, back faces culled: keep only the pixels whose rim value is above 0.3
//     Additive    blending on with SrcAlpha / One, back faces culled: the rim is ADDED to what is behind
//   The host (Maya) picks one technique at a time.  No technique in this file has more than ONE pass.
// WHAT CHANGED
//   Godot has no techniques inside one shader: a blend mode is a render_mode, fixed when the shader compiles. The nearest honest
//   equivalent is a compile-time switch: change the single number in  #define TECHNIQUE  and the right render_mode and alpha handling
//   are compiled (0 Opaque, 1 AlphaBlend, 2 AlphaTest, 3 Additive). The verification script builds all four by replacing that line.
//   Another Godot route, not used: four small shaders that #include one shared .gdshaderinc, one material each.
//   - Opaque: Cg sets no cull state (the host default was not stated), so cull_disabled; the closed sphere hides its back faces by depth anyway.
//   - AlphaBlend: the Cg only says AlphaBlendEnable = True and relies on the host's default blend function. It is read as the usual
//     blend (SrcAlpha, OneMinusSrcAlpha) = Godot blend_mix. That reading is an inference, not something the file states.
//   - AlphaTest: alpha = rim, discard when alpha <= 0.3. Godot's ALPHA_SCISSOR_THRESHOLD discards alpha < 0.3 (the two differ only at exactly 0.3).
//   - Additive: BlendFunc (SrcAlpha, One) = Godot blend_add (checked by pixel value in the verification run).
//   - The Cg assigns the float3 rim to the float alpha: only the first component survives. Here, fresnel.x.
//   - Blending happens in Godot's LINEAR light, not in display values (measured), so a half-transparent pixel is lighter than the Cg's.
//   - next_pass would be the Godot answer to a multi-pass technique; this file has no multi-pass technique to carry over.
// FINDING  see CONVERSION-NOTES.md.

shader_type spatial;

#define TECHNIQUE 1

#if TECHNIQUE == 0
render_mode unshaded, cull_disabled;
#elif TECHNIQUE == 1
render_mode unshaded, blend_mix, cull_back;
#elif TECHNIQUE == 2
render_mode unshaded, cull_back;
#elif TECHNIQUE == 3
render_mode unshaded, blend_add, cull_back;
#endif

uniform vec3 shader_color : source_color = vec3(1.0);
uniform vec3 light_direction = vec3(0.5, -0.8, -0.6);   // direction the light travels, world space
uniform vec3 ambient_color : source_color = vec3(0.15);
uniform float fresnel_power : hint_range(0.0, 10.0, 0.01) = 3.0;
uniform float specular_power : hint_range(0.1, 100.0, 0.01) = 30.0;
uniform vec3 specular_color : source_color = vec3(1.0);
uniform sampler2D diffuse_map : source_color, hint_default_white, filter_linear_mipmap, repeat_enable;
uniform sampler2D spec_map : hint_default_white, filter_linear_mipmap, repeat_enable;
uniform sampler2D normal_map : hint_normal, filter_linear_mipmap, repeat_enable;

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

#if TECHNIQUE == 0
	// Opaque: the rim alpha is computed in the Cg but ignored.
#elif TECHNIQUE == 2
	ALPHA = fresnel.x;
	ALPHA_SCISSOR_THRESHOLD = 0.3;
#else
	ALPHA = fresnel.x;
#endif
}
