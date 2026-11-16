shader_type spatial;
render_mode unshaded, blend_mix, depth_draw_opaque, cull_back;
// E8: how far below the water is the opaque scene, along the view ray? red = gap / 2 (metres), green = raw depth texture value, blue = water depth / 16.
uniform sampler2D depth_tex : hint_depth_texture, repeat_disable, filter_nearest;
uniform float use_branch = 1.0;

float scene_depth(vec2 screen_uv, mat4 inv_projection, out float raw) {
	raw = texture(depth_tex, screen_uv).x;
	vec3 ndc = vec3(screen_uv * 2.0 - 1.0, raw);
#if CURRENT_RENDERER == RENDERER_COMPATIBILITY
	if (use_branch > 0.5) {
		ndc = vec3(screen_uv, raw) * 2.0 - 1.0;
	}
#endif
	vec4 view = inv_projection * vec4(ndc, 1.0);
	return -view.z / view.w;
}

void fragment() {
	float raw;
	float behind = scene_depth(SCREEN_UV, INV_PROJECTION_MATRIX, raw);
	float gap = behind + VERTEX.z;
	ALBEDO = vec3(clamp(gap, 0.0, 2.0) / 2.0, raw, -VERTEX.z / 16.0);
	ALPHA = 0.999;
}
