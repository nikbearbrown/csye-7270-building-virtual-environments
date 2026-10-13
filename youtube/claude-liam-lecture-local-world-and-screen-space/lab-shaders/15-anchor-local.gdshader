shader_type canvas_item;

varying vec2 position;

void vertex() {
	position = VERTEX;
}

void fragment() {
	float stripe = step(0.5, fract(position.x / 64.0));
	COLOR.rgb = mix(COLOR.rgb, vec3(1.0), stripe);
}
