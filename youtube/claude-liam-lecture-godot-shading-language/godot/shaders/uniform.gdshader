shader_type canvas_item;
uniform vec4 tint : source_color = vec4(1.0);
uniform float amount : hint_range(0.0, 1.0) = 0.0;
uniform int mode : hint_enum("Off", "Tint", "Mask") = 0;
void fragment() {
    COLOR = tint;
}
