shader_type canvas_item;

uniform float radius = 450.0;
uniform float thickness = 60.0;

void light() {
	float d = length(LIGHT_VERTEX.xy - LIGHT_POSITION.xy);
	float ring = step(radius - thickness, d) - step(radius, d);
	vec3 rgb = COLOR.rgb * LIGHT_COLOR.rgb * LIGHT_ENERGY * ring;
	LIGHT = vec4(rgb, LIGHT_COLOR.a);
}
