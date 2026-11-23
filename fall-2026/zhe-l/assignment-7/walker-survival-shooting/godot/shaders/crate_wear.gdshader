shader_type spatial;

uniform sampler2D rust_albedo : source_color, filter_linear_mipmap, repeat_enable;
uniform sampler2D wear_mask : filter_linear_mipmap, repeat_enable;

group_uniforms paint;
uniform vec4 paint_color : source_color = vec4(0.260, 0.283, 0.190, 1.0);
uniform float paint_roughness : hint_range(0.0, 1.0) = 0.85;

group_uniforms wear;
uniform float wear_amount : hint_range(0.0, 1.0) = 0.1;
uniform float wear_softness : hint_range(0.0, 0.2) = 0.0;

group_uniforms mapping;
uniform float texture_scale : hint_range(0.1, 10.0) = 2.0;

group_uniforms;

const float RUST_ROUGHNESS = 0.79;
const float MIN_WEAR_SOFTNESS = 0.001;

void vertex() {
    if (abs(NORMAL.x) > 0.5) {
        UV = VERTEX.zy;
    } else if (abs(NORMAL.y) > 0.5) {
        UV = VERTEX.xz;
    } else {
        UV = VERTEX.xy;
    }

    UV *= texture_scale;
}

void fragment() {
    vec3 rust = texture(rust_albedo, UV).rgb;
    float height = texture(wear_mask, UV).r;
    float width = max(wear_softness, MIN_WEAR_SOFTNESS);
    float w = 1.0 - smoothstep(wear_amount - width, wear_amount + width, height);

    ALBEDO = mix(paint_color.rgb, rust, w);
    ROUGHNESS = mix(paint_roughness, RUST_ROUGHNESS, w);
}