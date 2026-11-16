// 11_uv_manip.gdshader
//
// SOURCE     shader_lessons/11_uv_manip.cgfx  
// WHAT THE ORIGINAL DID
//   The full 08 model (colour, spec and normal maps) with the texture coordinates reworked per pixel:
//     uv = ((texCoord - 0.5) * scale + translate + time * speed) + 0.5
//   so the scale (tiling) happens around the CENTRE of the texture, translate shifts it, and speed scrolls it over time. One
//   float4 holds scale.xy and translate.xy; a float2 holds the scroll speed (default 0,0, so nothing scrolls).
// WHAT CHANGED
//   - Same arithmetic in fragment(), reading Godot's UV and TIME. The new uv feeds ALL three texture reads.
//   - Wrap addressing matters here: any uv outside 0..1 needs repeat_enable (Godot's default is clamp), so all three samplers carry it.
//   - A larger scale means MORE copies (the texture shrinks), not a zoom in: that is how the formula reads, kept.
//   - Scrolling the normal map scrolls the lighting detail with the picture, but the tangent frame stays attached to the mesh.
// FINDING  see CONVERSION-NOTES.md.

shader_type spatial;
render_mode unshaded;

uniform vec3 shader_color : source_color = vec3(1.0);
uniform vec3 light_direction = vec3(0.5, -0.8, -0.6);   // direction the light travels, world space
uniform vec3 ambient_color : source_color = vec3(0.15);
uniform float fresnel_power : hint_range(0.0, 10.0, 0.01) = 3.0;
uniform float specular_power : hint_range(0.1, 100.0, 0.01) = 30.0;
uniform vec3 specular_color : source_color = vec3(1.0);
uniform vec2 speed_xy = vec2(0.0);                                  // uv units per second
uniform vec4 uv_scale_translate = vec4(1.0, 1.0, 0.0, 0.0);         // xy = scale about the centre, zw = translate
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
	vec2 uv = ((UV - 0.5) * uv_scale_translate.xy + uv_scale_translate.zw + (TIME * speed_xy)) + 0.5;

	vec3 tn = texture(normal_map, uv).rgb * 2.0 - 1.0;
	vec3 n = normalize(tn.x * world_tangent + tn.y * world_binormal + tn.z * world_normal);

	vec3 l = normalize(-light_direction);
	vec3 e = normalize(eye_vector);
	vec3 r = -reflect(e, n);

	vec4 color_map = texture(diffuse_map, uv);
	vec4 specular_map = texture(spec_map, uv);

	vec3 lambert = vec3(clamp(dot(l, n), 0.0, 1.0));
	vec3 specular = pow(clamp(dot(r, l), 0.0, 1.0), specular_power) * specular_color;
	vec3 fresnel = vec3(pow(1.0 - clamp(dot(e, n), 0.0, 1.0), fresnel_power));
	vec3 total_spec = (fresnel * specular_map.r) + (specular * specular_map.g);

	ALBEDO = (lambert + ambient_color) * (shader_color * color_map.rgb) + total_spec;
}
