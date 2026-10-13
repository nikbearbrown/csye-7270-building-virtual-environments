shader_type canvas_item;
// Calculator, not shown in the film. Each column of the view is one cell; the cell's value v is written as the red channel (v + 1) / 4,
// so -1 reads 0.0, 0 reads 0.25, 1 reads 0.5, 2 reads 0.75. run-calc.py decodes it. Every number the film works by hand is computed here.

float cell(int i) {
	float d1 = distance(vec2(0.62, 0.66), vec2(0.5));
	float L = distance(vec2(0.62, 0.66), vec2(0.5, 0.5)) - length(vec2(0.62, 0.66) - vec2(0.5));
	// --- the pixel worked by hand, and step's argument order
	if (i == 0) return abs(d1 - 0.2) < 0.000001 ? 1.0 : 0.0;   // distance is exactly 0.2 (within 1e-6)
	if (i == 1) return step(0.3, 0.2);                          // step(edge, x), x below the edge: 0
	if (i == 2) return step(0.2, 0.3);                          // x above the edge: 1
	if (i == 3) return step(0.3, 0.3);                          // x equal to the edge: 1
	if (i == 4) return step(0.4, 0.3);                          // 0
	if (i == 5) return abs(L) < 0.000001 ? 1.0 : 0.0;           // distance(a, b) equals length(a - b)
	// --- the ring in numbers: outer 0.35, inner 0.30, pixels at distance 0.20, 0.33, 0.45
	if (i == 6) return step(0.20, 0.35) - step(0.20, 0.30);
	if (i == 7) return step(0.33, 0.35) - step(0.33, 0.30);
	if (i == 8) return step(0.45, 0.35) - step(0.45, 0.30);
	// --- overlap sum and the hole: (a, b, hole) = (1,0,0) (1,1,0) (1,1,1) (0,0,0)
	if (i == 9)  return 1.0 + 0.0 - 0.0;
	if (i == 10) return 1.0 + 1.0 - 0.0;
	if (i == 11) return 1.0 + 1.0 - 1.0;
	if (i == 12) return min(1.0 + 1.0, 1.0) - 0.0;
	if (i == 13) return min(1.0 + 1.0, 1.0) - 1.0;
	// --- below zero: a bite taken where no disc was drawn (disc 0 - bite 1), then a spot added
	if (i == 14) return 0.0 - 1.0;                              // -1
	if (i == 15) return 0.0 - 1.0 + 1.0;                        // the spot's pixel in the bite: back to 0 (the spot never shows)
	if (i == 16) return max(0.0 - 1.0, 0.0) + 1.0;              // with max first: 1 (the spot shows)
	if (i == 17) return min(2.0, 1.0);
	if (i == 18) return max(-1.0, 0.0);
	// --- multiplying masks stays a mask
	if (i == 19) return 1.0 * 1.0;
	if (i == 20) return 1.0 * 0.0;
	if (i == 21) return max(1.0, 1.0);                          // union in the cross centre: 1 (a sum would give 2)
	if (i == 22) return 1.0 - 1.0;                              // not (one minus the mask)
	if (i == 23) return max(1.0 - 1.0, 0.0);
	return 0.0;
}

void fragment() {
	int i = int(floor(UV.x * 24.0));
	float v = cell(i);
	COLOR = vec4((v + 1.0) / 4.0, 0.0, 0.0, 1.0);
}
