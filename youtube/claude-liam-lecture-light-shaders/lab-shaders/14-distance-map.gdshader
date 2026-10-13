shader_type canvas_item;

void light() {
	float d = length(LIGHT_VERTEX.xy - LIGHT_POSITION.xy);
	LIGHT = vec4(vec3(d / 1000.0), 1.0);
}
