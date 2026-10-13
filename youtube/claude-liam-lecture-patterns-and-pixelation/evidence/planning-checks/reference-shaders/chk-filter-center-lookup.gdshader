shader_type canvas_item;

// Evidence only. The same middle-of-the-cell lookup as lab-shaders/06-pixelate-center.gdshader, but the picture is a sampler uniform
// so its filter can be chosen: FILTER_NEAREST (hint filter_nearest) or the smooth default (hint filter_linear).
uniform sampler2D picture : filter_linear, repeat_disable;
uniform float blocks = 16.0;

void fragment() {
	vec2 uv = (floor(UV * blocks) + 0.5) / blocks;
	COLOR = texture(picture, uv);
}
