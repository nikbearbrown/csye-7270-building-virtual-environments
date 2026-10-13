shader_type canvas_item;
void fragment() {
    vec4 c = vec4(0.2, 0.6, 0.9, 1.0);
    vec3 swapped = c.bgr;
    vec2 pair = c.xx;
    COLOR = vec4(swapped, 1.0);
}
