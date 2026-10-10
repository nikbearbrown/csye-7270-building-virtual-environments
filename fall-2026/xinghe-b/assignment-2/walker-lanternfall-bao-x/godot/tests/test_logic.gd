extends "res://tests/harness.gd"
const GS = preload("res://game/game_state.gd")
const Gate = preload("res://audio/sfx_gate.gd")
const Prog = preload("res://features/progression/progression.gd")

func run() -> void:
	suite = "logic"
	_state_tests()
	_progression_tests()
	_gate_tests()
	completed = true

func _state_tests() -> void:
	var s = GS.new()
	var changes: Array = []
	s.changed.connect(func(f, t): changes.append([f, t]))
	check("state-menu-rejects-won", not s.go(GS.WON) and s.current == GS.MENU)
	check("state-menu-to-playing", s.go(GS.PLAYING) and s.current == GS.PLAYING)
	check("state-levelup-roundtrip", s.go(GS.LEVELUP) and s.go(GS.PLAYING))
	check("state-pause-roundtrip", s.go(GS.PAUSED) and not s.go(GS.LEVELUP) and s.go(GS.PLAYING))
	s.go(GS.LOST)
	check("state-terminal-is-sticky", not s.go(GS.PLAYING) and not s.go(GS.WON) and s.is_terminal())
	check("state-restart-from-terminal", s.restart() and s.current == GS.PLAYING)
	check("state-signal-log", changes.size() == 7 and changes[-1] == [GS.LOST, GS.PLAYING], {"changes": changes})
	var m = GS.new()
	check("state-restart-not-from-menu", not m.restart())

func _progression_tests() -> void:
	var p = Prog.new()
	var levels: Array = []
	p.leveled_up.connect(func(l): levels.append(l))
	var gained: int = p.add_xp(3 + 5 + 7)
	check("prog-multi-level", gained == 3 and p.level == 4 and p.pending_levelups == 3 and levels == [2, 3, 4], {"gained": gained, "levels": levels})
	var rng := RandomNumberGenerator.new()
	rng.seed = 42
	var offer: Array[String] = p.offer_cards(rng)
	var unique := {}
	for c in offer: unique[c] = true
	check("prog-offer-three-unique", offer.size() == 3 and unique.size() == 3 and not ("sunflare" in offer), {"offer": offer})
	var early: Array[String] = p.eligible_cards()
	check("prog-branches-offered", "beam_rate" in early and "beam_pierce" in early and "moth_new" in early and not ("moth_count" in early), {"eligible": early})
	p.apply("beam_rate")
	check("prog-beam-rate", p.beam_level == 2 and p.beam_cooldown_ticks == 30, {"cooldown": p.beam_cooldown_ticks})
	p.apply("beam_pierce")
	p.apply("moth_new")
	p.apply("moth_count")
	check("prog-not-ready-at-moth-2", not p.evolution_ready() and not ("sunflare" in p.offer_cards(rng)))
	p.apply("moth_radius")
	check("prog-maxed-weapons", p.beam_level == 3 and p.moth_level == 3 and p.moth_count == 3 and p.beam_pierce == 2)
	var evo: Array[String] = p.offer_cards(rng)
	check("prog-sunflare-offered-first", p.evolution_ready() and evo[0] == "sunflare" and evo.size() == 3, {"offer": evo})
	p.apply("sunflare")
	var after: Array[String] = p.eligible_cards()
	check("prog-after-evolve-no-weapon-cards", p.evolved_sunflare and not p.evolution_ready() and not ("beam_rate" in after) and not ("moth_count" in after), {"eligible": after})
	var guard := 0
	while not p.eligible_cards().is_empty() and guard < 100:
		p.apply(p.eligible_cards()[0])
		guard += 1
	check("prog-exhausted-pool-pads-heal", p.offer_cards(rng) == ["heal", "heal", "heal"], {"applied": guard})
	# Bao, 2026-09-29: new cards — damage, weapon attack speed; pickup range and move speed go to 5 levels
	var c = Prog.new()
	var pool: Array[String] = c.eligible_cards()
	check("prog-new-passives-offered", "pass_damage" in pool and "pass_haste" in pool and "pass_magnet" in pool and "pass_speed" in pool, {"pool": pool})
	for i in 5:
		c.apply("pass_damage")
		c.apply("pass_speed")
	check("prog-passive-caps", not ("pass_damage" in c.eligible_cards()) and not ("pass_speed" in c.eligible_cards()) and int(c.passive["damage"]) == 5 and int(c.passive["speed"]) == 5)
	check("prog-damage-mult", is_equal_approx(c.damage_mult(), 2.0), {"mult": c.damage_mult()})
	for i in 3:
		c.apply("pass_haste")
	check("prog-attack-rate-mult", is_equal_approx(c.attack_rate_mult(), 1.36), {"mult": c.attack_rate_mult()})
	check("prog-card-title-shows-level", c.card_title("pass_haste") == "Quick Hands (4/5)" and c.card_title("beam_rate") == "Beam: Quick Wick", {"haste": c.card_title("pass_haste")})
	# Bao, 2026-09-29: "每升一次等级后续所需要的经验会增加" — every level must need more XP than the last
	var q = Prog.new()
	var needs: Array = []
	for lv in range(1, 31):
		q.level = lv
		needs.append(q.xp_needed())
	var rising := true
	for i in range(1, needs.size()):
		rising = rising and needs[i] > needs[i - 1]
	check("prog-xp-need-always-increases", rising and needs[0] == 3 and needs[11] == 40, {"needs_lv1_to_30": needs})
	var a = Prog.new(); var b = Prog.new()
	var r1 := RandomNumberGenerator.new(); r1.seed = 7
	var r2 := RandomNumberGenerator.new(); r2.seed = 7
	check("prog-deterministic", a.offer_cards(r1) == b.offer_cards(r2))

func _gate_tests() -> void:
	var g = Gate.new({"kill": {"cooldown_ms": 60, "max_voices": 3}, "evolve": {"once": true, "max_voices": 1}, "hurt": {"cooldown_ms": 800, "max_voices": 1}})
	check("gate-first-plays", g.request("kill", 0, 0))
	check("gate-cooldown-blocks", not g.request("kill", 30, 1))
	check("gate-cooldown-releases", g.request("kill", 60, 1))
	check("gate-voice-cap", not g.request("kill", 200, 3) and g.request("kill", 200, 2))
	check("gate-hurt-boundary-inclusive", g.request("hurt", 0, 0) and not g.request("hurt", 799, 0) and g.request("hurt", 800, 0))
	check("gate-once", g.request("evolve", 0, 0) and not g.request("evolve", 99999, 0))
	g.reset()
	check("gate-reset", g.request("evolve", 0, 0) and g.request("kill", 0, 0))
	check("gate-unknown-id-single-voice", g.request("mystery", 0, 0) and not g.request("mystery", 1, 1))
