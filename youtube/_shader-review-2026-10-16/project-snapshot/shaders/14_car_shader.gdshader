// 14_car_shader.gdshader
//
// SOURCE     shader_lessons/14_carShader.cgfx 
// WHAT THE ORIGINAL DID
//   The 09 cube-map model with finer control over the reflection and a second highlight:
//     rim      = (pow(1 - N.E, fresnelPower) * fresnelIntensity + fresnelOffset) * (lambert + ambient)
//     reflect  = rim * pow(cubeColour, reflectionContrast)          (contrast raises the colour to a power)
//     specular = pow(R.L, power) * colour  +  pow(R.L, power2) * colour2     (a tight and a wide highlight on the same R.L)
//     result   = (lambert + ambient) * colour + reflect + specular
//   fresnelOffset (default 0) is a floor that lets some reflection show on surfaces that face the camera.
// WHAT CHANGED
//   - GLSL's pow() needs both arguments to be the same type: pow(vec3, float) does not compile (it did in Cg), so the scalar contrast is
//     widened with vec3(reflection_contrast). This one was met by running.
//   - Cube map, camera vector and normal as in 09.
// FINDING  see CONVERSION-NOTES.md.

shader_type spatial;
render_mode unshaded;

uniform vec3 shader_color : source_color = vec3(1.0);
uniform vec3 light_direction = vec3(0.5, -0.8, -0.6);   // direction the light travels, world space
uniform vec3 ambient_color : source_color = vec3(0.15);
uniform float fresnel_power : hint_range(0.0, 10.0, 0.01) = 3.0;
uniform float fresnel_intensity : hint_range(0.0, 10.0, 0.01) = 1.0;
uniform float fresnel_offset : hint_range(0.0, 10.0, 0.01) = 0.0;
uniform float reflection_contrast : hint_range(0.0, 10.0, 0.01) = 1.0;
uniform float specular_power : hint_range(0.1, 100.0, 0.01) = 30.0;
uniform vec3 specular_color : source_color = vec3(1.0);
uniform float specular_power2 : hint_range(0.1, 100.0, 0.01) = 30.0;
uniform vec3 specular_color2 : source_color = vec3(1.0);
uniform samplerCube reflection_map : source_color, filter_linear;

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

	vec3 cube_map = texture(reflection_map, r).rgb;

	vec3 lambert = vec3(clamp(dot(l, n), 0.0, 1.0));

	float r_dot_l = clamp(dot(r, l), 0.0, 1.0);
	vec3 specular = pow(r_dot_l, specular_power) * specular_color + pow(r_dot_l, specular_power2) * specular_color2;

	vec3 fresnel = (pow(1.0 - clamp(dot(e, n), 0.0, 1.0), fresnel_power) * fresnel_intensity + fresnel_offset) * (lambert + ambient_color);

	vec3 total_spec = (fresnel * pow(cube_map, vec3(reflection_contrast))) + specular;

	ALBEDO = (lambert + ambient_color) * shader_color + total_spec;
}
