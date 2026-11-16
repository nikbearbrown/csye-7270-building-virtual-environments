// 06_diffuse_mapped.gdshader
//
// SOURCE     shader_lessons/06_diffuse_mapped.cgfx  
//
// WHAT THE ORIGINAL DID
//   The full 05 lighting model (Lambert + ambient + rim + Phong) with the first texture read: a colour map multiplies the
//   surface colour before lighting. Rim and specular are added on top, unmultiplied by the texture.
// WHAT CHANGED
//   - The texture is a normal Godot sampler2D. The original gave it AddressU/V = Wrap: in Godot that is the hint repeat_enable
//     (Godot's default is repeat_disable = clamp to the edge, so a texture that tiles needs the hint).
//   - ": source_color" on the sampler tells Godot the picture is sRGB and must be converted to linear light before the
//     lighting arithmetic. The Cg read the raw numbers and did everything in display space.
//   - UV: Cg TEXCOORD0 -> Godot's built-in UV. Maya's UV origin is bottom-left and Godot's is top-left; Godot's mesh importers
//     flip V for imported meshes, so the shader itself needs no flip.
//   - The vertex shader of the original also built a tangent and binormal that this pixel shader never uses: dropped.
//   - The original declared its colour texture as TextureType "Cube" (labelled "Reflection Texture") although it is read with tex2D:
//     a copy-paste slip in the Cg's metadata. Here it is a plain 2D texture.
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

	vec3 lambert = vec3(clamp(dot(l, n), 0.0, 1.0));
	vec3 specular = pow(clamp(dot(r, l), 0.0, 1.0), specular_power) * specular_color;
	vec3 fresnel = pow(1.0 - clamp(dot(e, n), 0.0, 1.0), fresnel_power) * (lambert + ambient_color);
	vec3 total_spec = fresnel + specular;

	ALBEDO = (lambert + ambient_color) * (shader_color * color_map.rgb) + total_spec;
}
