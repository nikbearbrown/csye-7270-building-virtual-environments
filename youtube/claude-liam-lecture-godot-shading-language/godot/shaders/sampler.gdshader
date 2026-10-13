shader_type canvas_item;
uniform sampler2D image_tex : source_color, filter_nearest;
void fragment() {
    COLOR = texture(image_tex, UV);
}
