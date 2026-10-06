class_name Tuning
## Player tuning (predictions from CHANGE-BRIEF; adjusted after playtest). Pixels and seconds.

const RUN_SPEED := 110.0
const GROUND_ACCEL := 900.0
const AIR_ACCEL := 700.0
const GRAVITY := 900.0
const JUMP_VELOCITY := -330.0     # apex = v^2 / 2g = 60 px; airtime 0.73 s -> about 80 px at RUN_SPEED (pit is 60 px)
const JUMP_CUT_VELOCITY := -120.0 # releasing jump early caps the upward speed (shorter hop)
const MAX_FALL_SPEED := 420.0
const COYOTE_TIME := 0.08         # jump still allowed this long after leaving an edge
const JUMP_BUFFER := 0.10         # a jump pressed this long before landing still counts
