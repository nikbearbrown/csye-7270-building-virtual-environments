shader_type canvas_item;

uniform float zoom = 1.0;

void fragment() {
	vec2 uv = UV * zoom;
	vec2 inside = step(vec2(0.0), uv) * step(uv, vec2(1.0));
	COLOR = texture(TEXTURE, uv);
	COLOR.a *= inside.x * inside.y;
}
