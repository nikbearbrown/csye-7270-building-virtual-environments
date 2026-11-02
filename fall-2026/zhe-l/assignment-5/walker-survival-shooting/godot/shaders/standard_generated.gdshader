// NOTE: Shader automatically converted from Godot Engine 4.7.2.stable's StandardMaterial3D.

// This shader is used on 3D objects.
shader_type spatial;

// Use opaque depth drawing, hide back faces, and use Burley diffuse and GGX specular lighting.
render_mode blend_mix, depth_draw_opaque, cull_back, diffuse_burley, specular_schlick_ggx;

// The base color is multiplied by the color texture.
uniform vec4 albedo : source_color;

// source_color converts the texture's sRGB colors to linear values when sampled.
uniform sampler2D texture_albedo : source_color, filter_linear_mipmap, repeat_enable;

// These two parameters are not used in the code below.
uniform ivec2 albedo_texture_size;
uniform float point_size : hint_range(0.1, 128.0, 0.1);

// Controls how rough the surface is. Higher values make reflections less sharp.
uniform float roughness : hint_range(0.0, 1.0);

// This texture stores metallic data, so it does not use source_color.
// If no texture is assigned, hint_default_white provides a white texture.
uniform sampler2D texture_metallic : hint_default_white, filter_linear_mipmap, repeat_enable;

// Selects which texture channel provides the metallic value.
// For example, vec4(1.0, 0.0, 0.0, 0.0) selects the red channel.
uniform vec4 metallic_texture_channel;

// This texture stores roughness data, so it does not use source_color.
// hint_roughness_r tells Godot that roughness is stored in the red channel.
uniform sampler2D texture_roughness : hint_roughness_r, filter_linear_mipmap, repeat_enable;

// Controls the strength of specular reflections on non-metallic surfaces.
uniform float specular : hint_range(0.0, 1.0, 0.01);

// Controls how metallic the surface is.
uniform float metallic : hint_range(0.0, 1.0, 0.01);

// This texture stores surface directions instead of colors.
// hint_roughness_normal identifies the normal map for roughness processing.
uniform sampler2D texture_normal : hint_roughness_normal, filter_linear_mipmap, repeat_enable;

// Controls the strength of the normal map.
uniform float normal_scale : hint_range(-16.0, 16.0);

// Controls the scale and offset of the first UV set.
// Only the x and y components are used below.
uniform vec3 uv1_scale;
uniform vec3 uv1_offset;

// These parameters are not used because this shader only reads the first UV set.
uniform vec3 uv2_scale;
uniform vec3 uv2_offset;

void vertex() {
	// Scale the model's UV coordinates, then shift them by the offset.
	UV = UV * uv1_scale.xy + uv1_offset.xy;
}

void fragment() {
	// Use the UV coordinates calculated in vertex() for all texture samples.
	vec2 base_uv = UV;

	// Read the color texture and multiply it by the base color.
	vec4 albedo_tex = texture(texture_albedo, base_uv);
	ALBEDO = albedo.rgb * albedo_tex.rgb;

	// Read the metallic texture using the selected channel.
	float metallic_tex = dot(texture(texture_metallic, base_uv), metallic_texture_channel);

	// Multiply the texture value by the metallic parameter.
	METALLIC = metallic_tex * metallic;

	// Set the strength of non-metallic specular reflections.
	SPECULAR = specular;

	// Select the red channel of the roughness texture.
	vec4 roughness_texture_channel = vec4(1.0, 0.0, 0.0, 0.0);
	float roughness_tex = dot(texture(texture_roughness, base_uv), roughness_texture_channel);

	// Multiply the texture value by the roughness parameter.
	ROUGHNESS = roughness_tex * roughness;

	// Read the normal map to add surface detail without changing the mesh.
	NORMAL_MAP = texture(texture_normal, base_uv).rgb;

	// Apply the normal map strength.
	NORMAL_MAP_DEPTH = normal_scale;
}