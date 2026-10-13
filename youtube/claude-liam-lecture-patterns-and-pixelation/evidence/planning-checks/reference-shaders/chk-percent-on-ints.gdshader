shader_type canvas_item;

// Evidence only. The same operator on integers (Expected: compiles; 5 % 2 = 1).
void fragment() {
	int a = 5 % 2;
	COLOR = vec4(float(a), 0.0, 0.0, 1.0);
}
