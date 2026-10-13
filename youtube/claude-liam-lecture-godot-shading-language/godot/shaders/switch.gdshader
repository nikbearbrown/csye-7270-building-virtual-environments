shader_type canvas_item;
uniform int mode = 1;
void fragment() {
    float value = 0.0;
    switch (mode) {
        case 1: value = 0.25; break;
        case 2: value = 0.75; break;
        default: value = 0.1; break;
    }
    COLOR = vec4(vec3(value), 1.0);
}
