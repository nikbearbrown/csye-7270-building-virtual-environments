shader_type canvas_item;
uniform float amplitude = 20.0;
void vertex() {
    VERTEX.x += amplitude * sin(TIME);
}
