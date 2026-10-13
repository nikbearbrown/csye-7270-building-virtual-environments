shader_type canvas_item;
void fragment() {
    int n = 0;
    while (n < 3) {
        n += 1;
    }
    COLOR = vec4(float(n) / 3.0);
}
