shader_type spatial;

// --- 表面组 ---
group_uniforms surface;
uniform vec4 base_tint : source_color = vec4(1.0, 1.0, 1.0, 1.0);
uniform float normal_scale : hint_range(0.0, 2.0, 0.05) = 1.0;
uniform float roughness_scale : hint_range(0.0, 2.0, 0.05) = 1.0;

// --- 结霜组 ---
group_uniforms frost;
uniform vec4 frost_color : source_color = vec4(0.85, 0.92, 1.0, 1.0);
uniform float frost_amount : hint_range(0.0, 1.0, 0.01) = 0.0;

// --- 贴图组 ---
group_uniforms textures;
uniform sampler2D texture_albedo : source_color, filter_linear_mipmap;
uniform sampler2D texture_normal : hint_normal, filter_linear_mipmap;
uniform sampler2D texture_roughness : hint_default_white, filter_linear_mipmap;
group_uniforms;

void fragment() {
    // 1. 采样三张贴图
    vec3 albedo_tex = texture(texture_albedo, UV).rgb;
    float rough_tex = texture(texture_roughness, UV).r;
    vec3 normal_tex = texture(texture_normal, UV).rgb;

    // 2. 岩石基础漫反射计算
    vec3 rock_albedo = albedo_tex * base_tint.rgb;

    // 3. 结霜遮罩计算（粗糙度低的地方先结霜，柔和过渡）
    // 过渡半带宽设为 0.1（总过渡带宽度 0.2）。
    // 门槛 threshold 在 frost_amount 从 0 到 1 时，由 -0.1 线性扩展到 1.1：
    float threshold = mix(-0.1, 1.1, frost_amount);
    // 粗糙度低于 threshold 时结霜越充分，因此用 (threshold - rough_tex) 映射到 [-0.1, 0.1]
    float frost_mask = smoothstep(-0.1, 0.1, threshold - rough_tex);

    // 4. ALBEDO：在岩石颜色和霜色之间按遮罩混合
    ALBEDO = mix(rock_albedo, frost_color.rgb, frost_mask);

    // 5. 粗糙度：岩石基础粗糙度缩放并截断，结霜区域平滑混合到光滑冰面 (定为 0.15)
    float base_roughness = clamp(rough_tex * roughness_scale, 0.0, 1.0);
    float ice_roughness = 0.15;
    ROUGHNESS = mix(base_roughness, ice_roughness, frost_mask);

    // 6. 法线贴图与强度写入
    NORMAL_MAP = normal_tex;
    NORMAL_MAP_DEPTH = normal_scale;
}