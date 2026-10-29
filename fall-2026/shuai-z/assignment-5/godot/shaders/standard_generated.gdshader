// NOTE: Shader automatically converted from Godot Engine 4.7.2.stable's StandardMaterial3D.
// Converted parameter values and texture bindings live in the ShaderMaterial, not in this standalone shader file.

// A spatial shader shades 3D surfaces. These modes control blending, depth writes, culling, diffuse lighting, and specular lighting.
shader_type spatial;
render_mode blend_mix, depth_draw_opaque, cull_back, diffuse_burley, specular_schlick_ggx;

// Base color multiplier; source_color identifies this uniform as color data.
uniform vec4 albedo : source_color;
// Read the albedo texture as sRGB color, with linear and mipmap filtering and repeating UVs.
uniform sampler2D texture_albedo : source_color, filter_linear_mipmap, repeat_enable;
// Texture size parameter retained by the generator; unused by this version of vertex() and fragment().
uniform ivec2 albedo_texture_size;
// Point size parameter retained by the generator; unused by the current mesh shading code.
uniform float point_size : hint_range(0.1, 128.0, 0.1);

// Roughness multiplier, applied to the sampled roughness texture value.
uniform float roughness : hint_range(0.0, 1.0);
// Metallic values are data, so there is no source_color hint. An unbound texture defaults to white: all channels are 1.
uniform sampler2D texture_metallic : hint_default_white, filter_linear_mipmap, repeat_enable;
// RGBA channel weights; for example, dot() with (1, 0, 0, 0) selects only the red channel.
uniform vec4 metallic_texture_channel;
// Read roughness as data; hint_roughness_r identifies a roughness texture that uses its red channel.
uniform sampler2D texture_roughness : hint_roughness_r, filter_linear_mipmap, repeat_enable;

// Specular reflection parameter for nonmetallic surfaces, evaluated by Godot's lighting model.
uniform float specular : hint_range(0.0, 1.0, 0.01);
// Metallic multiplier: 0 represents a nonmetal and 1 represents a metal.
uniform float metallic : hint_range(0.0, 1.0, 0.01);

// Read the normal texture as data, preserving the generated hint_roughness_normal hint without adding source_color.
uniform sampler2D texture_normal : hint_roughness_normal, filter_linear_mipmap, repeat_enable;
// Normal map strength, passed to NORMAL_MAP_DEPTH.
uniform float normal_scale : hint_range(-16.0, 16.0);

// Scale and offset for the first UV set; this shader uses only the xy components of these vec3 uniforms.
uniform vec3 uv1_scale;
uniform vec3 uv1_offset;
// Second UV set parameters retained by the generator; unused by the current code.
uniform vec3 uv2_scale;
uniform vec3 uv2_offset;

void vertex() {
	// Scale each vertex's UV, then add the offset. The transformed UV is interpolated into fragment().
	UV = UV * uv1_scale.xy + uv1_offset.xy;
}

void fragment() {
	// Use the same UV coordinates for all textures to align color, roughness, and normal details.
	vec2 base_uv = UV;

	// texture() returns RGBA. Multiply only RGB by the base color, leaving ALPHA unwritten.
	vec4 albedo_tex = texture(texture_albedo, base_uv);
	ALBEDO = albedo.rgb * albedo_tex.rgb;

	// dot() computes a weighted sum of the sampled RGBA channels, then the metallic parameter scales the result.
	float metallic_tex = dot(texture(texture_metallic, base_uv), metallic_texture_channel);
	METALLIC = metallic_tex * metallic;
	// Pass the material's specular reflection parameter directly to the renderer.
	SPECULAR = specular;

	// The fixed weights (1, 0, 0, 0) select only the roughness texture's red channel.
	vec4 roughness_texture_channel = vec4(1.0, 0.0, 0.0, 0.0);
	float roughness_tex = dot(texture(texture_roughness, base_uv), roughness_texture_channel);
	// The generated shader scales roughness by multiplication; weathered_stone instead adds an offset.
	ROUGHNESS = roughness_tex * roughness;

	// Normal Map: Enabled
	// Pass the sampled 0-1 normal encoding directly to NORMAL_MAP for Godot to interpret as a tangent-space normal.
	NORMAL_MAP = texture(texture_normal, base_uv).rgb;
	// Set normal map strength separately without modifying the sampled values.
	NORMAL_MAP_DEPTH = normal_scale;
}
