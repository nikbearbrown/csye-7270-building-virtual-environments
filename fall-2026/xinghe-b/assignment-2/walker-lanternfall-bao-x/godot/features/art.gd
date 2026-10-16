extends RefCounted
## Loads generated art if it exists; returns null so every drawer can fall back to a placeholder.

const PC_SHEET := "res://assets/art/pc_sheet.png"
const MOTH := "res://assets/art/enemy_moth.png"
const WRAITH := "res://assets/art/enemy_wraith.png"
const GROUND := "res://assets/art/env_ground_tile.png"
const STALL := "res://assets/art/env_stall.png"
const POST := "res://assets/art/env_lantern_post.png"
const CRATES := "res://assets/art/env_crates.png"
const CART := "res://assets/art/env_noodle_cart.png"
const PUDDLE := "res://assets/art/env_puddle.png"
const LEAVES := "res://assets/art/env_leaves.png"
const BEAM := "res://assets/art/fx_beam.png"
const ORBIT_MOTH := "res://assets/art/fx_orbit_moth.png"
const SUNFLARE := "res://assets/art/fx_sunflare.png"
const GEM := "res://assets/art/pickup_gem.png"

static var disabled := false

static func texture(path: String) -> Texture2D:
	if disabled or not ResourceLoader.exists(path):
		return null
	return load(path)
