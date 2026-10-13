shader_type canvas_item;

// Numbers that appear on screen in the matrix-product beats. Row k is green when check k is true, red when false.
// Rows 15 and 16 are NEGATIVE CONTROLS: they are deliberately false and must be red.
mat3 turn_by(float a) {
	vec3 across = vec3(cos(a), sin(a), 0.0);
	vec3 down = vec3(-sin(a), cos(a), 0.0);
	return mat3(across, down, vec3(0.0, 0.0, 1.0));
}

mat3 slide_by(vec2 t) {
	vec3 across = vec3(1.0, 0.0, 0.0);
	vec3 down = vec3(0.0, 1.0, 0.0);
	return mat3(across, down, vec3(t, 1.0));
}

bool near(vec3 a, vec3 b) { return length(a - b) < 0.0001; }

mat2 turn2() {
	float a = TAU / 4.0;
	return mat2(vec2(cos(a), sin(a)), vec2(-sin(a), cos(a)));
}

mat3 around_y(float a) {
	return mat3(vec3(cos(a), 0.0, -sin(a)), vec3(0.0, 1.0, 0.0), vec3(sin(a), 0.0, cos(a)));
}

mat3 around_x(float a) {
	return mat3(vec3(1.0, 0.0, 0.0), vec3(0.0, cos(a), sin(a)), vec3(0.0, -sin(a), cos(a)));
}

bool check(int k) {
	mat3 R = turn_by(TAU / 4.0);               // a quarter turn
	mat3 T = slide_by(vec2(100.0, 0.0));
	vec3 v = vec3(30.0, 20.0, 1.0);
	float a = 0.7854;
	vec2 pv = vec2(-64.0, -64.0);
	if (k == 0) return near((T * R)[2], vec3(100.0, 0.0, 1.0));      // turn first, then slide: the slide survives untouched
	if (k == 1) return near((R * T)[2], vec3(0.0, 100.0, 1.0));      // slide first, then turn: the turn carries the slide round
	if (k == 2) return near((T * R) * v, T * (R * v));               // one product = the two tables one after the other
	if (k == 3) return !near((T * R)[2], (R * T)[2]);                // order matters
	if (k == 4) {                                                    // the pivot product = subtract the pivot, turn, add it back
		vec3 viaMatrix = slide_by(pv) * turn_by(a) * slide_by(-pv) * vec3(10.0, -20.0, 1.0);
		vec2 d = vec2(10.0, -20.0) - pv;
		vec2 viaSteps = (mat2(vec2(cos(a), sin(a)), vec2(-sin(a), cos(a))) * d) + pv;
		return length(viaMatrix.xy - viaSteps) < 0.001;
	}
	if (k == 5) return near(slide_by(pv) * turn_by(a) * slide_by(-pv) * vec3(pv, 1.0), vec3(pv, 1.0));   // the pivot does not move
	if (k == 6) return near(around_y(a) * vec3(1.0, 0.0, 0.0), vec3(cos(a), 0.0, -sin(a))) && near(around_y(a) * vec3(0.0, 1.0, 0.0), vec3(0.0, 1.0, 0.0));
	if (k == 7) return near(around_x(a) * vec3(0.0, 1.0, 0.0), vec3(0.0, cos(a), sin(a))) && near(around_x(a) * vec3(1.0, 0.0, 0.0), vec3(1.0, 0.0, 0.0));
	if (k == 8) return near(mat3(1.0) * v, v);                      // mat3(1.0) is the identity
	if (k == 9) return near(T * v, vec3(130.0, 20.0, 1.0));           // the slide worked example
	if (k == 10) return mat2(vec2(3.0, 4.0), vec2(5.0, 6.0)) * vec2(0.0) == vec2(0.0);   // a two by two cannot move the origin
	if (k == 11) {                                                   // scale, turn, slide: with a UNIFORM scale the order of scale and turn does not matter
		mat3 S = mat3(vec3(1.5, 0.0, 0.0), vec3(0.0, 1.5, 0.0), vec3(0.0, 0.0, 1.0));
		return near((T * S * R) * v, (T * R * S) * v);
	}
	if (k == 12) {                                                   // ... but with a NON-uniform scale it does
		mat3 S = mat3(vec3(2.0, 0.0, 0.0), vec3(0.0, 1.0, 0.0), vec3(0.0, 0.0, 1.0));
		return !near((T * S * R) * v, (T * R * S) * v);
	}
	if (k == 13) {                                                   // the flip table is a 3D turn: mixing it with the 'slide' tables (third number = 1) moves the pivot
		vec3 viaMixedTables = slide_by(pv) * around_y(a) * slide_by(-pv) * vec3(pv, 1.0);
		return !near(viaMixedTables, vec3(pv, 1.0));
	}
	if (k == 14) return mat3(turn2()) == turn_by(TAU / 4.0);        // mat3 of a mat2 pads with zeros and a one: the same table as the 3x3 turn
	if (k == 15) return near((T * R)[2], vec3(0.0, 100.0, 1.0));     // CONTROL: must be false
	if (k == 16) return near((R * T)[2], vec3(100.0, 0.0, 1.0));     // CONTROL: must be false
	return false;
}

void fragment() {
	int k = int(floor(UV.y * 18.0));
	COLOR = check(k) ? vec4(0.0, 1.0, 0.0, 1.0) : vec4(1.0, 0.0, 0.0, 1.0);
}
