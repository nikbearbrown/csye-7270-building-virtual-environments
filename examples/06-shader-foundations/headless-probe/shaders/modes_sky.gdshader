shader_type sky;
void sky() { COLOR = mix(vec3(0.2, 0.3, 0.8), vec3(1.0), EYEDIR.y * 0.5 + 0.5); }
