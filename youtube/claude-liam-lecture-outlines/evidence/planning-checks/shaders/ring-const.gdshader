shader_type canvas_item;
// check shader for the cost timing only: the ring outline of lab-shaders/10-ring.gdshader with the sixteen directions written out as constants (no sine or cosine per pixel)
uniform vec4 line_color : source_color = vec4(0.25, 0.25, 0.75, 1.0);
uniform float thickness : hint_range(0.0, 8.0) = 1.0;
const vec2 DIRS[16] = vec2[16](
	vec2(1.0, 0.0),
	vec2(0.92388, 0.382683),
	vec2(0.707107, 0.707107),
	vec2(0.382683, 0.92388),
	vec2(0.0, 1.0),
	vec2(-0.382683, 0.92388),
	vec2(-0.707107, 0.707107),
	vec2(-0.92388, 0.382683),
	vec2(-1.0, 0.0),
	vec2(-0.92388, -0.382683),
	vec2(-0.707107, -0.707107),
	vec2(-0.382683, -0.92388),
	vec2(-0.0, -1.0),
	vec2(0.382683, -0.92388),
	vec2(0.707107, -0.707107),
	vec2(0.92388, -0.382683)
);

void fragment() {
	float around = 0.0;
	for (int i = 0; i < 16; i++) {
		around += texture(TEXTURE, UV + DIRS[i] * TEXTURE_PIXEL_SIZE * thickness).a;
	}
	vec4 color = texture(TEXTURE, UV);
	COLOR = mix(color, line_color, min(around, 1.0) * (1.0 - color.a));
}
