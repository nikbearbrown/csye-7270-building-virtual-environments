// 03_lambert_ambient.gdshader
//
// SOURCE     shader_lessons/03_lambert_ambient.cgfx 
//
// WHAT THE ORIGINAL DID
//   Lambert plus an ambient floor: (lambert + ambientColor) * surface colour. ambientColor defaults to 0.15 grey, so the
//   unlit side is never pure black. Note the ambient is ADDED to the light term and then multiplied by the surface colour.
// WHAT CHANGED
//   Same conversion as 02, plus the ambient_color uniform (": Diffuse" -> ": source_color").
//   Nothing clamps the sum: at the lit pole of a white surface the value is 1.0 + 0.15 = 1.15 before the screen clips it,
//   exactly as the original's 8-bit framebuffer would have.
// FINDING  see CONVERSION-NOTES.md (colour space: the Godot ambient floor is 0.15 sRGB = 0.0196 linear = 0.15 when encoded back).

shader_type spatial;
render_mode unshaded;

uniform vec3 shader_color : source_color = vec3(1.0);
uniform vec3 light_direction = vec3(0.5, -0.8, -0.6);   // direction the light travels, world space
uniform vec3 ambient_color : source_color = vec3(0.15);

varying vec3 world_normal;

void vertex() {
	world_normal = MODEL_NORMAL_MATRIX * NORMAL;
}

void fragment() {
	vec3 n = normalize(world_normal);
	vec3 l = normalize(-light_direction);
	vec3 lambert = vec3(clamp(dot(l, n), 0.0, 1.0));
	ALBEDO = (lambert + ambient_color) * shader_color;
}
