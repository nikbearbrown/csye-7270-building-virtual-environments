#[compute]
#version 450
layout(local_size_x = 8, local_size_y = 1, local_size_z = 1) in;
layout(set = 0, binding = 0, std430) restrict buffer Data { float v[]; } data;
void main() { data.v[gl_GlobalInvocationID.x] *= 2.0 }
