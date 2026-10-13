shader_type canvas_item;
void fragment() {
    bool enabled = true;
    int count = 5;
    float gain = float(count) / 10.0;
    COLOR = enabled ? vec4(gain, 0.0, 0.0, 1.0) : vec4(0.0);
}
