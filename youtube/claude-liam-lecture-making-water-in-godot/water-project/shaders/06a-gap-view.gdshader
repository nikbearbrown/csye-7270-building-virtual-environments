shader_type spatial;
render_mode unshaded, blend_mix, depth_draw_opaque, cull_back;

uniform sampler2D depth_tex : hint_depth_texture, repeat_disable, filter_nearest;
uniform float shore_width : hint_range(0.05, 1.5) = 1.0;

// distance from the camera to the opaque scene behind this pixel
float scene_depth(vec2 screen_uv, mat4 inv_projection) {
	float depth = texture(depth_tex, screen_uv).x;
#if CURRENT_RENDERER == RENDERER_COMPATIBILITY
	vec3 ndc = vec3(screen_uv, depth) * 2.0 - 1.0;
#else
	vec3 ndc = vec3(screen_uv * 2.0 - 1.0, depth);
#endif
	vec4 view = inv_projection * vec4(ndc, 1.0);
	return -view.z / view.w;
}

void fragment() {
	float gap = scene_depth(SCREEN_UV, INV_PROJECTION_MATRIX) + VERTEX.z;
	float near = 1.0 - clamp(gap / shore_width, 0.0, 1.0);
	ALBEDO = mix(vec3(0.16, 0.42, 0.58), vec3(1.0), near);
	ALPHA = 0.999;
}
