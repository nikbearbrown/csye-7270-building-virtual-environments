shader_type canvas_item;

uniform float tint_amount : hint_range(0.0, 1.0) = 0.0;
uniform vec4 tint_color : source_color = vec4(0.6, 0.88, 1.0, 1.0);
uniform float tint_strength : hint_range(0.0, 1.0) = 0.4;

void fragment() {
COLOR.rgb = mix(COLOR.rgb, tint_color.rgb, tint_amount * tint_strength);
}
