shader_type canvas_item;

uniform float cells : hint_range(4.0, 64.0) = 24.0;
uniform float radius : hint_range(0.0, 0.7) = 0.4;

void fragment() {
	vec2 p = UV * cells;
	vec2 middle = floor(p + 0.5) / cells;
	vec4 picture = texture(TEXTURE, middle);
	float d = length(fract(p + 0.5) - 0.5);
	float dot_mask = 1.0 - step(radius, d);
	COLOR = vec4(picture.rgb, picture.a * dot_mask);
}
