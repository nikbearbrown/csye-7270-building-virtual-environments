shader_type canvas_item;

uniform float count = 4.0;
uniform float width = 0.5;
uniform float speed = 0.5;

void fragment() {
	float diagonal = UV.x + UV.y;
	float f = fract(diagonal * count - TIME * speed);
	float stripe = step(width, f);
	vec3 gold = vec3(0.925, 0.769, 0.380);
	vec3 cream = vec3(0.980, 0.976, 0.961);
	COLOR = vec4(mix(gold, cream, stripe), 1.0);
}
