shader_type particles;

uniform vec3 initial_velocity = vec3(0.0, -120.0, 0.0);
uniform vec3 gravity = vec3(0.0, 98.0, 0.0);

void start() {
	if (RESTART_POSITION) {
		TRANSFORM = EMISSION_TRANSFORM;
	}
	if (RESTART_VELOCITY) {
		VELOCITY = initial_velocity;
	}
}

void process() {
	VELOCITY += gravity * DELTA;
}
