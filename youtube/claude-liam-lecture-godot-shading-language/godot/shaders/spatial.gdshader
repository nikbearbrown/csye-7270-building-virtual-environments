shader_type spatial;
uniform vec4 tint : source_color = vec4(1.0, 0.5, 0.2, 1.0);
void fragment() {
    ALBEDO = tint.rgb;
    ROUGHNESS = 0.65;
}
