shader_type canvas_item;
uniform vec4 tint : source_color = vec4(0.85, 0.25, 0.12, 1.0);
uniform float amount : hint_range(0.0, 1.0) = 0.0;
void fragment() {
    vec4 base = COLOR;
    COLOR = vec4(mix(base.rgb, tint.rgb,
        clamp(amount, 0.0, 1.0)), base.a);
}
