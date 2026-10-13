shader_type canvas_item;

uniform float amount : hint_range(0.0, 1.0) = 0.0;

void fragment() {
	float gray = dot(COLOR.rgb, vec3(0.2126, 0.7152, 0.0722));
	COLOR.rgb = mix(COLOR.rgb, vec3(gray), amount);
}
