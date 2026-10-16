extends SceneTree
## Balance probe (not a pass/fail suite): plays seeded runs with a circling bot and a flee bot.
const Session = preload("res://game/session.gd")
const GS = preload("res://game/game_state.gd")
const Tuning = preload("res://features/tuning.gd")

func _initialize() -> void:
	call_deferred("_main")

func _main() -> void:
	for bot in ["smart"]:
		for seed_value in [1, 2, 3]:
			var g = Session.new()
			g.test_mode = true
			root.add_child(g)
			g.start_run(seed_value)
			var evo_at := -1
			for t in Tuning.RUN_SECONDS * Tuning.TICK_HZ + 10:
				if g.state.is_terminal():
					break
				if g.state.current == GS.LEVELUP:
					var i: int = g.offered.find("sunflare")
					if i >= 0:
						evo_at = g.tick_count / 60
					elif bot == "smart":
						for want in ["beam_rate", "beam_pierce", "moth_new", "moth_count", "moth_radius", "pass_damage", "pass_haste", "pass_magnet", "pass_speed", "pass_hp", "heal"]:
							i = g.offered.find(want)
							if i >= 0:
								break
					g.choose_card(maxi(i, 0))
				var a := float(t) / 90.0
				var axis := Vector2(cos(a), sin(a))
				if bot == "flee" or bot == "smart":
					var push := Vector2.ZERO
					for e in g.enemies:
						var d: Vector2 = g.player.position - e.position
						if d.length() < (90.0 if bot == "smart" else 160.0):
							push += d.normalized() * ((90.0 if bot == "smart" else 160.0) - d.length())
					if push.length() > 1.0:
						axis = (push.normalized() + axis * 0.3).normalized()
					elif bot == "smart" and not g.gems.is_empty():
						# nothing close: walk to the nearest gem, as a player would
						var best: Vector2 = g.gems[0].position
						for gem in g.gems:
							if gem.position.distance_to(g.player.position) < best.distance_to(g.player.position):
								best = gem.position
						axis = (best - g.player.position).normalized()
				g.test_axis = axis
				g.tick()
			printerr("%s seed %d: %s at %d s, level %d, kills %d, evolved at %d" % [bot, seed_value, GS.NAMES[g.state.current], g.tick_count / 60, g.prog.level, g.kills, evo_at])
			g.free()
	quit()
