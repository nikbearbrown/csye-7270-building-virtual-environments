shader_type canvas_item;
void fragment() {
    if (UV.x < 0.5) {
        COLOR = vec4(0.2, 0.2, 0.2, 1.0);
    } else {
        COLOR = vec4(0.9, 0.9, 0.9, 1.0);
    }
}
