shader_type canvas_item;

void light() {
	vec2 aim = vec2(cos(TIME), sin(TIME));
	float agree = dot(-LIGHT_DIRECTION.xy, aim);
	float beam = step(0.95, agree);
	vec3 rgb = COLOR.rgb * LIGHT_COLOR.rgb * LIGHT_ENERGY * beam;
	LIGHT = vec4(rgb, LIGHT_COLOR.a);
}
