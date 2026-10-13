shader_type canvas_item;
void fragment() {
    mat2 m = mat2(vec2(1.0, 2.0), vec2(3.0, 4.0));
    vec2 result = m * vec2(1.0, 0.0);
    COLOR = vec4(result / 4.0, 0.0, 1.0);
}
