// 01_base.gdshader
//
// SOURCE     shader_lessons/01_base.cgfx 
//
// WHAT THE ORIGINAL DID
//   The "foundation" shader. Compared with 00 it receives the surface normal, turns it into a WORLD-space normal with the
//   WorldInverseTranspose matrix, and in the pixel shader returns  saturate(dot(towardLight, normal)) * colour.
//   That IS a Lambert diffuse shader.
// WHAT CHANGED
//   - Normal: Cg  mul(WorldInverseTranspose, normal).xyz  becomes  MODEL_NORMAL_MATRIX * NORMAL  in vertex() and travels to
//     fragment() in a varying. (In vertex() Godot's NORMAL is the mesh's own object-space normal; in fragment() the same name
//     means VIEW space. That is why the world-space normal is carried in our own varying.)
//   - saturate(x) does not exist in Godot: clamp(x, 0.0, 1.0).
//   - Light: the uniform keeps the Cg meaning of "lightDirection : Direction": the direction the light TRAVELS, world space;
//     the shader negates it to get the vector pointing AT the light. The Cg default (0,1,0) sent light upward and lit only
//     the underside of the object; the default here is a light coming from the upper left, in front, so the lit side faces the camera.
//   - matrices World and ViewInverse were declared but never read in this file: dropped.
// FINDING  01_base and 02_lambert are the same shader (only a blank line moved); see CONVERSION-NOTES.md.

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
