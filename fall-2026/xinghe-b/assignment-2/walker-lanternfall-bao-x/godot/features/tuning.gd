extends RefCounted
## Every gameplay number lives here.

const TICK_HZ := 60
const RUN_SECONDS := 180
const ARENA := Rect2(-960, -540, 1920, 1080)

const PLAYER_SPEED := 90.0
const SPEED_PER_LEVEL := 12.0
const PLAYER_RADIUS := 10.0
const PLAYER_MAX_HP := 10
const HP_PER_LEVEL := 4
const HEAL_AMOUNT := 3
const IFRAME_TICKS := 48
const HURT_POSE_TICKS := 12
const KNOCKBACK := 160.0
const KNOCKBACK_DECAY := 900.0
const FACING_DEADZONE := 0.1

const PICKUP_RADIUS := 28.0
const PICKUP_RADIUS_PER_LEVEL := 20.0
const COLLECT_RADIUS := 8.0
const GEM_PULL_SPEED := 260.0
## Passive cards (Bao, 2026-09-29): damage and attack speed apply to every weapon.
const DAMAGE_PER_LEVEL := 0.2
const HASTE_PER_LEVEL := 0.12
## Monsters spawned later are tougher, in proportion to the time survived: HP x (1 + 0.5 per whole minute).
const ENEMY_HP_GROWTH_PER_MINUTE := 0.5
const XP_TO_LEVEL := [3, 5, 7, 9, 12, 15, 18, 22, 26, 30, 35, 40]

const BEAM_SPEED := 320.0
const BEAM_LIFE_TICKS := 60
## The bolt as drawn (fx_beam.png is 14 x 2 visible px): bullets hit what the player sees.
const BEAM_HALF_LENGTH := 7.0
const BEAM_HALF_WIDTH := 1.0
const BEAM_DAMAGE := 2
const BEAM_BASE_COOLDOWN := 40
const BEAM_RATE_FACTOR := 0.75
const CAST_POSE_TICKS := 8

const MOTH_SPIN := 3.2
const MOTH_BASE_RADIUS := 36.0
const MOTH_RADIUS_STEP := 14.0
const MOTH_HIT_RADIUS := 5.0
const MOTH_DAMAGE := 1
const MOTH_HIT_COOLDOWN := 20

const SUNFLARE_PERIOD := 120
const SUNFLARE_FIRST_DELAY := 30
const SUNFLARE_RADIUS := 240.0
const SUNFLARE_DAMAGE := 6
const SUNFLARE_RING_TICKS := 24
const EVOLVE_POSE_TICKS := 60
const BANNER_TICKS := 120

const SPAWN_DISTANCE := 400.0
## Spawns must land at least this far outside the visible 640x360 view.
const SPAWN_MARGIN := 24.0
const VIEW_HALF := Vector2(320, 180)
const MAX_ENEMIES := 220
## radius: the body that hurts the courier on contact. hit_half: half-extents of the visible sprite that
## the courier's weapons can hit (measured from enemy_moth.png / enemy_wraith.png, 2026-09-29).
const ENEMIES := {
	"moth": {"hp": 2, "speed": 55.0, "radius": 6.0, "hit_half": [11.0, 7.0], "damage": 1, "xp": 1, "frame": 24},
	"wraith": {"hp": 8, "speed": 32.0, "radius": 14.0, "hit_half": [13.0, 19.0], "damage": 2, "xp": 3, "frame": 40},
}
const SPAWN_TABLE := [
	{"until_s": 30, "interval_ticks": 60, "batch": 1, "wraith_chance": 0.0},
	{"until_s": 60, "interval_ticks": 45, "batch": 2, "wraith_chance": 0.1},
	{"until_s": 90, "interval_ticks": 36, "batch": 2, "wraith_chance": 0.2},
	{"until_s": 120, "interval_ticks": 30, "batch": 3, "wraith_chance": 0.25},
	{"until_s": 150, "interval_ticks": 24, "batch": 3, "wraith_chance": 0.3},
	{"until_s": 9999, "interval_ticks": 20, "batch": 4, "wraith_chance": 0.35},
]
