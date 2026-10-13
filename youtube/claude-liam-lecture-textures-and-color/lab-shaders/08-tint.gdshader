shader_type canvas_item;

uniform vec3 tint : source_color = vec3(1.0, 0.7, 0.5);

void fragment() {
	COLOR.rgb *= tint;
}
