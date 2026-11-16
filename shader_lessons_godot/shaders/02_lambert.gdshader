// 02_lambert.gdshader
//
// SOURCE     shader_lessons/02_lambert.cgfx  
//
// WHAT THE ORIGINAL DID
//   Lambert diffuse: brightness = how directly the surface faces the light = dot(normal, towardLight), floored at zero,
//   times the surface colour. Its header says it ADDS the light direction and the normal pass-through to the base shader;
//   in fact 01_base already has both, and the two files compute the same thing.
// WHAT CHANGED
//   Identical conversion to 01_base: world-space normal from MODEL_NORMAL_MATRIX, saturate -> clamp, unshaded render mode,
//   light_direction = direction the light travels in world space (default changed from the Cg (0,1,0), which lit the underside).
// FINDING  same as 01: no behavioural difference from 01_base; see CONVERSION-NOTES.md.

shader_type spatial;
render_mode unshaded;

uniform vec3 shader_color : source_color = vec3(1.0);
uniform vec3 light_direction = vec3(0.5, -0.8, -0.6);   // direction the light travels, world space

varying vec3 world_normal;

void vertex() {
	world_normal = MODEL_NORMAL_MATRIX * NORMAL;
}

void fragment() {
	vec3 n = normalize(world_normal);
	vec3 l = normalize(-light_direction);
	vec3 lambert = vec3(clamp(dot(l, n), 0.0, 1.0));
	ALBEDO = lambert * shader_color;
}
