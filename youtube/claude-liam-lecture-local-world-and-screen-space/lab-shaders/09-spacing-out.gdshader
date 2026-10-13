shader_type canvas_item;
uniform sampler2D sky : repeat_enable;
uniform float tile_size = 512.0;
uniform float amount : hint_range(0.0, 1.0) = 0.0;
varying vec2 world_position;

void vertex() {
	world_position = (MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy;
}

void fragment() {
	vec3 stars = texture(sky, world_position / tile_size).rgb;
	COLOR.rgb = mix(COLOR.rgb, stars, amount);
}
