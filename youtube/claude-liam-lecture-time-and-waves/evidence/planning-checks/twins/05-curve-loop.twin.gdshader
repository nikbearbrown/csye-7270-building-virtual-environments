shader_type canvas_item;
uniform float tv = 0.0;

uniform sampler2D curve;

void fragment() {
	float t = fract(tv * 0.5);
	float k = texture(curve, vec2(t, 0.0)).r;
	vec3 teal = vec3(0.37, 0.64, 0.57);
	vec3 cream = vec3(0.98, 0.97, 0.96);
	COLOR = vec4(mix(teal, cream, k), 1.0);
}
