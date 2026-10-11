extends Resource
## Values from GDD 0.2.0. A shared resource for gameplay and fixtures.
@export var speed: float = 160.0
@export var acceleration: float = 1280.0
@export var deceleration: float = 1920.0
@export var jump_velocity: float = -320.0
@export var gravity: float = 960.0
@export var terminal_velocity: float = 480.0
@export var coyote_ticks: int = 6
@export var buffer_ticks: int = 6

# D1/D2 additions (CHANGE-BRIEF 0.1.0 section 3). The eight values above are
# the starter's and are deliberately unchanged.
@export var air_jumps: int = 1
@export var air_dashes: int = 1
@export var dash_speed: float = 400.0
@export var dash_ticks: int = 10

# D3 additions (CHANGE-BRIEF revision 0.3.0). windup + active + recovery must
# sum to attack_ticks; the hitbox is live only for the active span.
@export var attack_ticks: int = 16
@export var attack_windup_ticks: int = 4
@export var attack_active_ticks: int = 9
@export var attack_reach: float = 30.0
