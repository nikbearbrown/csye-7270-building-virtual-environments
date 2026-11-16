// 05_phong.gdshader
//
// SOURCE     shader_lessons/05_phong.cgfx  
// WHAT THE ORIGINAL DID
//   04 plus a Phong specular highlight: reflect the surface-to-eye vector about the normal, flip it, and compare with the
//   direction to the light:  pow(saturate(dot(R, toLight)), specularPower) * specularColor, added to the result.
//   A bigger specularPower gives a smaller, sharper spot.
// WHAT CHANGED
//   - Cg reflect(I, N) and GLSL/Godot reflect(I, N) are the same function, I - 2 dot(N, I) N. The original passes the
//     SURFACE-TO-EYE vector as I (reflect expects a vector pointing toward the surface), so it negates the result:
//     R = -reflect(e, n) = 2 dot(n, e) n - e, which is the mirror direction a ray would have to take from the surface to reach the eye.
//     Carried over unchanged.
//   - Everything else as in 04.
// FINDING  see CONVERSION-NOTES.md (highlight position and size at power 30).

shader_type spatial;
render_mode unshaded;

uniform vec3 shader_color : source_color = vec3(1.0);
uniform vec3 light_direction = vec3(0.5, -0.8, -0.6);   // direction the light travels, world space
uniform vec3 ambient_color : source_color = vec3(0.15);
uniform float fresnel_power : hint_range(0.0, 10.0, 0.01) = 3.0;
uniform float specular_power : hint_range(0.1, 100.0, 0.01) = 30.0;
uniform vec3 specular_color : source_color = vec3(1.0);

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

	vec3 specular = pow(clamp(dot(r, l), 0.0, 1.0), specular_power) * specular_color;
	vec3 lambert = vec3(clamp(dot(l, n), 0.0, 1.0));
	vec3 fresnel = pow(1.0 - clamp(dot(e, n), 0.0, 1.0), fresnel_power) * (lambert + ambient_color);

	ALBEDO = (lambert + ambient_color) * shader_color + fresnel + specular;
}
