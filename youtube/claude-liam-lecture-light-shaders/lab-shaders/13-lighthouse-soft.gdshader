shader_type canvas_item;

uniform float cutoff : hint_range(0.5, 0.99) = 0.9;

void light() {
	vec2 aim = vec2(cos(TIME), sin(TIME));
	float agree = dot(-LIGHT_DIRECTION.xy, aim);
	float beam = smoothstep(cutoff, 0.99, agree);
	vec3 rgb = COLOR.rgb * LIGHT_COLOR.rgb * LIGHT_ENERGY * beam;
	LIGHT = vec4(rgb, LIGHT_COLOR.a);
}
