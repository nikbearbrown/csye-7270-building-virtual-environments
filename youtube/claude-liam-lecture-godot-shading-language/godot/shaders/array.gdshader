shader_type canvas_item;
void fragment() {
    float weights[3] = float[3](0.2, 0.3, 0.5);
    COLOR = vec4(weights[1], 0.0, 0.0, 1.0);
}
