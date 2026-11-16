// 10_vertex_anim.gdshader
//
// SOURCE     shader_lessons/10_vertexAnim.cgfx  
// WHAT THE ORIGINAL DID
//   The 05 Phong model with a vertex animation: every vertex is pushed along the vector vertOffset by
//   sin(time * animationSpeed + position.x * animationFrequency), in OBJECT space, before the matrices are applied.
//   Its default vertOffset is (0,0,0), so out of the box nothing moves.
// WHAT CHANGED
//   - The Cg writes the deformed position into the clip-space output; in Godot the idiomatic place is VERTEX (object space),
//     which Godot then carries through the model/view/projection matrices itself. Same space, same arithmetic.
//   - Cg's  time : Time  becomes the built-in TIME (seconds). Godot's TIME is one global clock for the whole
//     game. That Maya's Time semantic counted seconds is assumed, not verified.
//   - What the original did NOT do, kept as written: the normal is not recomputed after the deformation and the camera vector is built
//     from the UNdeformed position, so the lighting follows the original shape, not the waving one.
//   - outColor.a = fresnel was written in the Cg, but its technique is Opaque, so the alpha was never used: dropped here.
// FINDING  see CONVERSION-NOTES.md.

shader_type spatial;
render_mode unshaded;

uniform vec3 shader_color : source_color = vec3(1.0);
uniform vec3 light_direction = vec3(0.5, -0.8, -0.6);   // direction the light travels, world space
uniform vec3 ambient_color : source_color = vec3(0.15);
uniform float fresnel_power : hint_range(0.0, 10.0, 0.01) = 3.0;
uniform float specular_power : hint_range(0.1, 100.0, 0.01) = 30.0;
uniform vec3 specular_color : source_color = vec3(1.0);
uniform vec3 vert_offset = vec3(0.0);                                       // object space; the Cg default (0,0,0) means no motion
uniform float animation_frequency : hint_range(0.1, 10.0, 0.01) = 1.0;
uniform float animation_speed : hint_range(0.1, 10.0, 0.01) = 1.0;

varying vec3 world_normal;
varying vec3 eye_vector;

void vertex() {
	world_normal = MODEL_NORMAL_MATRIX * NORMAL;                              // not recomputed after the deformation (as in the original)
	vec3 world_pos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;                  // the UNdeformed position (as in the original)
	vec3 world_camera_pos = INV_VIEW_MATRIX[3].xyz;
	eye_vector = world_camera_pos - world_pos;

	VERTEX = VERTEX + sin(TIME * animation_speed + VERTEX.x * animation_frequency) * vert_offset;
}

void fragment() {
	vec3 n = normalize(world_normal);
	vec3 l = normalize(-light_direction);
	vec3 e = normalize(eye_vector);
	vec3 r = -reflect(e, n);

	vec3 lambert = vec3(clamp(dot(l, n), 0.0, 1.0));
	vec3 specular = pow(clamp(dot(r, l), 0.0, 1.0), specular_power) * specular_color;
	vec3 fresnel = pow(1.0 - clamp(dot(e, n), 0.0, 1.0), fresnel_power) * (lambert + ambient_color);
	vec3 total_spec = fresnel + specular;

	ALBEDO = (lambert + ambient_color) * shader_color + total_spec;
}
