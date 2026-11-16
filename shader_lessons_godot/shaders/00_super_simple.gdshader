// 00_super_simple.gdshader
//
// SOURCE     shader_lessons/00_superSimple.cgfx  
//
// WHAT THE ORIGINAL DID
//   The smallest shader that draws anything: a vertex shader that only moves each corner to the screen with the
//   WorldViewProjection matrix, and a pixel shader that returns one user-chosen colour (alpha 1). No normals, no light.
// WHAT CHANGED
//   - Matrix: Cg's  mul(WorldViewProjection, position)  is written out in vertex() as
//     PROJECTION_MATRIX * VIEW_MATRIX * MODEL_MATRIX * vec4(VERTEX, 1.0).  Godot does exactly this for you when POSITION is
//     not written; it is spelled out so the "decoder rings" are visible. Godot matrices are column-major and use the same
//     "matrix on the left, column vector on the right" order as Cg's mul(M, v), so the order of the three matrices carries over.
//   - The Cg semantic ": Diffuse" (Maya's colour-picker widget) becomes the hint ": source_color".
//   - "string description" and the technique/pass block are Maya/CgFX bookkeeping with no Godot equivalent: dropped.
//     (render_mode unshaded = no Godot lighting at all, so the colour goes to the screen as written.)
// FINDING  see CONVERSION-NOTES.md (colour space: the Cg colour went straight to the screen; Godot treats ALBEDO as linear light and encodes it).

shader_type spatial;
render_mode unshaded;

uniform vec3 shader_color : source_color = vec3(1.0);

void vertex() {
	POSITION = PROJECTION_MATRIX * VIEW_MATRIX * MODEL_MATRIX * vec4(VERTEX, 1.0);
}

void fragment() {
	ALBEDO = shader_color;
}
