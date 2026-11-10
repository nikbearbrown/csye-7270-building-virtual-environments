shader_type spatial;
render_mode unshaded;

uniform sampler2D greys_source_color : source_color, filter_nearest;
uniform sampler2D greys_raw : filter_nearest;
uniform bool use_source_color = true;

void fragment() {
    if (use_source_color) {
        ALBEDO = texture(greys_source_color, UV).rgb;
    } else {
        ALBEDO = texture(greys_raw, UV).rgb;
    }
}