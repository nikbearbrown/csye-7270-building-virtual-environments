shader_type canvas_item;
varying float horizontal;
void vertex() {
    horizontal = UV.x;
}
void fragment() {
    COLOR = vec4(vec3(horizontal), 1.0);
}
