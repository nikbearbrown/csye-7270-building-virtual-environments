extends RefCounted
## XP, level-up card offers, weapon/passive levels and the Sunflare evolution.

const Tuning = preload("res://features/tuning.gd")

signal leveled_up(level: int)

const WEAPON_MAX := 3
const PASSIVE_MAX := {"damage": 5, "haste": 5, "speed": 5, "magnet": 5, "hp": 2}
const CARD_TEXT := {
	"beam_rate": ["Beam: Quick Wick", "Beam fires 25% faster"],
	"beam_pierce": ["Beam: Long Wick", "Beam passes through one more enemy"],
	"moth_new": ["Lamp-Moths", "Two moths circle you and burn what they touch"],
	"moth_count": ["Moths: Another Wing", "One more orbiting moth"],
	"moth_radius": ["Moths: Wider Flight", "Moths circle further out"],
	"pass_damage": ["Hotter Flame", "All weapons deal 20% more damage"],
	"pass_haste": ["Quick Hands", "All weapons attack 12% faster"],
	"pass_speed": ["Light Boots", "Move 12 px/s faster"],
	"pass_magnet": ["Magnet Satchel", "Collect oil from further away"],
	"pass_hp": ["Thick Glass", "+4 max HP, healed now"],
	"heal": ["Trim the Wick", "Restore 3 HP"],
	"sunflare": ["SUNFLARE LIGHTHOUSE", "Beam and moths fuse into a pulsing burst of light"],
}

var xp := 0
var level := 1
var pending_levelups := 0
var beam_level := 1
var beam_pierce := 1
var beam_cooldown_ticks: int = Tuning.BEAM_BASE_COOLDOWN
var moth_level := 0
var moth_count := 0
var moth_radius: float = Tuning.MOTH_BASE_RADIUS
var passive := {"damage": 0, "haste": 0, "speed": 0, "magnet": 0, "hp": 0}
var evolved_sunflare := false

## Every level needs more than the one before: the table, then each step one bigger than the last (46, 53, 61, ...).
func xp_needed() -> int:
	var table: Array = Tuning.XP_TO_LEVEL
	var i := level - 1
	if i < table.size():
		return int(table[i])
	var need := int(table[-1])
	var step := int(table[-1]) - int(table[-2])
	for k in i - table.size() + 1:
		step += 1
		need += step
	return need

## Returns how many levels were gained. Each one emits leveled_up and is queued.
func add_xp(amount: int) -> int:
	xp += amount
	var gained := 0
	while xp >= xp_needed():
		xp -= xp_needed()
		level += 1
		gained += 1
		leveled_up.emit(level)
	pending_levelups += gained
	return gained

func damage_mult() -> float:
	return 1.0 + Tuning.DAMAGE_PER_LEVEL * int(passive["damage"])

func attack_rate_mult() -> float:
	return 1.0 + Tuning.HASTE_PER_LEVEL * int(passive["haste"])

## Card title with the level it would reach, e.g. "Quick Hands (4/5)" for passives.
func card_title(card: String) -> String:
	var title: String = CARD_TEXT[card][0]
	if card.begins_with("pass_"):
		var k := card.trim_prefix("pass_")
		return "%s (%d/%d)" % [title, int(passive[k]) + 1, int(PASSIVE_MAX[k])]
	return title

func evolution_ready() -> bool:
	return beam_level >= WEAPON_MAX and moth_level >= WEAPON_MAX and not evolved_sunflare

func eligible_cards() -> Array[String]:
	var out: Array[String] = []
	if not evolved_sunflare:
		if beam_level < WEAPON_MAX:
			out.append_array(["beam_rate", "beam_pierce"])
		if moth_level == 0:
			out.append("moth_new")
		elif moth_level < WEAPON_MAX:
			out.append_array(["moth_count", "moth_radius"])
	for k in ["damage", "haste", "speed", "magnet", "hp"]:
		if int(passive[k]) < int(PASSIVE_MAX[k]):
			out.append("pass_" + k)
	return out

func offer_cards(rng: RandomNumberGenerator) -> Array[String]:
	var pool := eligible_cards()
	for i in range(pool.size() - 1, 0, -1):
		var j := rng.randi_range(0, i)
		var t := pool[i]
		pool[i] = pool[j]
		pool[j] = t
	var out: Array[String] = []
	if evolution_ready():
		out.append("sunflare")
	for c in pool:
		if out.size() >= 3:
			break
		out.append(c)
	while out.size() < 3:
		out.append("heal")
	return out

func apply(card: String) -> void:
	match card:
		"beam_rate":
			beam_level += 1
			beam_cooldown_ticks = maxi(8, roundi(beam_cooldown_ticks * Tuning.BEAM_RATE_FACTOR))
		"beam_pierce":
			beam_level += 1
			beam_pierce += 1
		"moth_new":
			moth_level = 1
			moth_count = 2
		"moth_count":
			moth_level += 1
			moth_count += 1
		"moth_radius":
			moth_level += 1
			moth_radius += Tuning.MOTH_RADIUS_STEP
		"pass_damage", "pass_haste", "pass_speed", "pass_magnet", "pass_hp":
			var k := card.trim_prefix("pass_")
			passive[k] = int(passive[k]) + 1
		"sunflare":
			evolved_sunflare = true
		"heal":
			pass
