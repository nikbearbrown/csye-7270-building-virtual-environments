shader_type canvas_item;
void fragment() {
    float weights[3] = float[3](0.2, 0.3, 0.5);
    float total = 0.0;
    for (int i = 0; i < weights.length(); i++) {
        total += weights[i];
    }
    COLOR = vec4(vec3(total), 1.0);
}
