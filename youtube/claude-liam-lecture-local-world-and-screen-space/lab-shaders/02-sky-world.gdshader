shader_type canvas_item;

uniform sampler2D sky : repeat_enable;
uniform float tile_size = 512.0;

varying vec2 position;

void vertex() {
	position = (MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy;
}

void fragment() {
	COLOR.rgb = texture(sky, position / tile_size).rgb;
}
