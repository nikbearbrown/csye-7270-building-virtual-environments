// 04_fresnel.gdshader
//
// SOURCE     shader_lessons/04_fresnel.cgfx  
//
// WHAT THE ORIGINAL DID
//   03 plus a rim ("fresnel") term:  pow(1 - saturate(dot(toEye, normal)), fresnelPower) * (lambert + ambient).
//   It is 0 where the surface faces the camera and 1 at the silhouette, so a bigger power gives a thinner rim. The rim is
//   multiplied by the lit amount, so it fades out on the dark side. The vertex shader now also builds the vector from the
//   surface to the camera in world space.
// WHAT CHANGED
//   - Camera position. Cg:  float3(ViewInverse[0].w, ViewInverse[1].w, ViewInverse[2].w).  Cg indexes a matrix by ROW (M[0] is
//     the first row, .w its fourth element), so that reads the translation column. GLSL and Godot index by COLUMN (M[0] is the
//     first column), so the same numbers are INV_VIEW_MATRIX[3].xyz. Godot also offers CAMERA_POSITION_WORLD, the same vector.
//   - World position of the vertex: Cg mul(World, position) -> MODEL_MATRIX * vec4(VERTEX, 1.0).
//   - specularPower / specularColor were declared here but never read: dropped (they arrive in 05).
// FINDING  see CONVERSION-NOTES.md (rim weight at N.E = 1, 0.5, 0.2 for power 3).

shader_type spatial;
render_mode unshaded;

uniform vec3 shader_color : source_color = vec3(1.0);
uniform vec3 light_direction = vec3(0.5, -0.8, -0.6);   // direction the light travels, world space
uniform vec3 ambient_color : source_color = vec3(0.15);
uniform float fresnel_power : hint_range(0.0, 10.0, 0.01) = 3.0;

varying vec3 world_normal;
varying vec3 eye_vector;

void vertex() {
	world_normal = MODEL_NORMAL_MATRIX * NORMAL;
	vec3 world_pos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	vec3 world_camera_pos = INV_VIEW_MATRIX[3].xyz;   // the Cg's ViewInverse[0].w, [1].w, [2].w
	eye_vector = world_camera_pos - world_pos;
}

void fragment() {
	vec3 n = normalize(world_normal);
	vec3 l = normalize(-light_direction);
	vec3 e = normalize(eye_vector);

	vec3 lambert = vec3(clamp(dot(l, n), 0.0, 1.0));
	vec3 fresnel = pow(1.0 - clamp(dot(e, n), 0.0, 1.0), fresnel_power) * (lambert + ambient_color);

	ALBEDO = (lambert + ambient_color) * shader_color + fresnel;
}
