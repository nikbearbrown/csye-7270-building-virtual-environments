extends "res://tests/harness.gd"
const Session = preload("res://game/session.gd")
const GS = preload("res://game/game_state.gd")
const Tuning = preload("res://features/tuning.gd")
const Art = preload("res://features/art.gd")
const BeamShot = preload("res://features/weapons/beam_shot.gd")
const Ground = preload("res://features/world/ground.gd")
var game

func fresh(seed_value: int = 1, no_spawn: bool = true) -> void:
	if is_instance_valid(game):
		game.free()
	game = Session.new()
	game.test_mode = true
	game.test_no_spawn = no_spawn
	root.add_child(game)
	game.start_run(seed_value)

func run() -> void:
	suite = "gameplay"
	# every generated asset listed in the manifest must actually load (a fresh clone needs the import step first)
	var manifest = JSON.parse_string(FileAccess.get_file_as_string("res://assets/manifest.json"))
	var missing: Array = []
	for asset_id in manifest:
		for rel in manifest[asset_id]:
			var res_path: String = "res://" + str(rel).trim_prefix("godot/")
			if not ResourceLoader.exists(res_path) or load(res_path) == null:
				missing.append(res_path)
	check("generated-assets-load", missing.is_empty() and manifest.size() == 23, {"assets": manifest.size(), "not_loaded": missing})
	await fresh()
	check("run-starts-playing", game.state.current == GS.PLAYING and game.tick_count == 0 and game.player.hp == Tuning.PLAYER_MAX_HP)
	var poses: Array = game.player.POSES
	var sheet_ok: bool = game.player.sheet == null or game.player.sheet.get_width() == 32 * poses.size()
	var origin: Vector2 = game.player.SPRITE_ORIGIN
	var torso_ok := true
	var torso := {}
	if game.player.sheet:
		var img: Image = game.player.sheet.get_image()
		var navy := Color("#2E3A59")
		for pose in ["idle", "walk_contact", "walk_passing", "cast", "levelup", "sunflare", "victory"]:
			var i: int = poses.find(pose)
			var sum := Vector2.ZERO
			var n := 0
			for y in 32:
				for x in 32:
					var c := img.get_pixel(i * 32 + x, y)
					if c.a > 0.5 and c.is_equal_approx(navy):
						sum += Vector2(x, y)
						n += 1
			var centre := sum / maxi(n, 1)
			torso[pose] = [snappedf(centre.x, 0.1), snappedf(centre.y, 0.1)]
			torso_ok = torso_ok and n > 0 and absf(centre.x - origin.x) <= 1.5 and absf(centre.y - origin.y) <= 1.5
	check("hurtbox-centred-on-torso", game.player.sheet == null or torso_ok, {"sprite_origin": [origin.x, origin.y], "coat_centres": torso})
	check("pose-table-matches-sheet", poses.size() == 10 and not ("turn_side" in poses) and not ("turn_back" in poses) and sheet_ok, {"poses": poses})
	game.test_axis = Vector2.RIGHT
	game.step_ticks(60)
	check("move-speed", absf(game.player.position.x - 90.0) < 0.5, {"x": game.player.position.x})
	check("walk-pose", game.player.pose in ["walk_contact", "walk_passing", "cast"], {"pose": game.player.pose})
	await fresh()
	game.test_axis = Vector2(1, 1)
	game.step_ticks(60)
	check("diagonal-normalized", absf(game.player.position.length() - 90.0) < 0.5, {"dist": game.player.position.length()})
	game.test_axis = Vector2(-1, 0)
	game.step_ticks(1)
	check("facing-left", game.player.facing == -1)
	game.test_axis = Vector2(0.08, 1)
	game.step_ticks(5)
	check("facing-deadzone", game.player.facing == -1)
	game.test_axis = Vector2.ZERO
	game.step_ticks(20)
	check("idle-pose", game.player.pose in ["idle", "cast"], {"pose": game.player.pose})
	game.test_axis = Vector2.LEFT
	game.step_ticks(1200)
	check("arena-clamp", game.player.position.x >= Tuning.ARENA.position.x, {"x": game.player.position.x})

	await fresh()
	game.spawn_enemy("moth", Vector2(80, 0))
	var kills := [0]
	game.enemy_killed.connect(func(_p): kills[0] += 1)
	game.step_ticks(2)
	check("cast-pose-on-fire", game.player.pose == "cast", {"pose": game.player.pose})
	game.step_ticks(38)
	check("beam-kills-moth", kills[0] == 1 and game.gems.size() == 1 and game.enemies.is_empty(), {"kills": kills[0], "gems": game.gems.size()})
	var picked := [0]
	game.gem_collected.connect(func(_v): picked[0] += 1)
	game.test_axis = Vector2.RIGHT
	game.step_ticks(60)
	check("gem-flies-and-collects", picked[0] == 1 and game.prog.xp == 1 and game.gems.is_empty(), {"xp": game.prog.xp})

	# monsters get tougher with time, proportionally (Bao, 2026-09-29)
	await fresh()
	var m0 = game.spawn_enemy("moth", Vector2(300, 0))
	game.tick_count = 59 * Tuning.TICK_HZ
	var m59 = game.spawn_enemy("moth", Vector2(300, 20))
	game.tick_count = 60 * Tuning.TICK_HZ
	var m1 = game.spawn_enemy("moth", Vector2(300, 40))
	game.tick_count = 120 * Tuning.TICK_HZ
	var w2x = game.spawn_enemy("wraith", Vector2(300, 80))
	check("enemy-hp-grows-with-time", is_equal_approx(m0.hp, 2.0) and is_equal_approx(m59.hp, 2.0) and is_equal_approx(m1.hp, 3.0) and is_equal_approx(w2x.hp, 16.0), {"moth_0s": m0.hp, "moth_59s": m59.hp, "moth_60s": m1.hp, "wraith_120s": w2x.hp})
	await fresh()
	for i in 5:
		game.prog.apply("pass_damage")
	for i in 5:
		game.prog.apply("pass_haste")
	check("damage-card-scales-weapons", is_equal_approx(game.weapon_damage(Tuning.BEAM_DAMAGE), 4.0), {"beam": game.weapon_damage(Tuning.BEAM_DAMAGE)})
	check("haste-card-shortens-beam-cooldown", game.beam_cooldown() == 25, {"cooldown": game.beam_cooldown()})

	# the market map (Bao, 2026-09-29: "整体地图再丰富一点材料"): streets of stalls and carts, lantern posts,
	# crates, puddles and leaves; decoration only, deterministic, clear of the spawn plaza, inside the arena
	var ground = game.ground
	var kinds := {}
	var in_arena := true
	var plaza_clear := true
	for p in ground.props:
		kinds[p["kind"]] = int(kinds.get(p["kind"], 0)) + 1
		in_arena = in_arena and Tuning.ARENA.grow(-24).has_point(p["pos"])
		plaza_clear = plaza_clear and p["pos"].length() > ground.PLAZA_RADIUS
	var every_kind := true
	for k in ["stall", "cart", "post", "crates", "puddle", "leaves"]:
		every_kind = every_kind and int(kinds.get(k, 0)) >= 3
	check("map-has-every-prop-kind", every_kind, {"counts": kinds})
	check("map-props-inside-arena-and-clear-of-plaza", in_arena and plaza_clear)
	# Bao, 2026-09-29: "整体地图应该破碎一点" — broken up, not two tidy streets
	var bands := {}
	for p in ground.props:
		if p["kind"] in ["stall", "cart"]:
			bands[int(floor(p["pos"].y / 60.0))] = true
	check("map-is-broken-up", bands.size() >= 8, {"stall_rows": bands.size()})
	var overlaps := 0
	for i in ground.solids.size():
		for j in range(i + 1, ground.solids.size()):
			if ground.solids[i].intersects(ground.solids[j]):
				overlaps += 1
	check("props-do-not-overlap", overlaps == 0, {"overlapping_pairs": overlaps})
	# solid props block the courier (Bao, 2026-09-29: "路灯这些有阻挡效果"); decals and enemies do not
	check("map-has-solids", ground.solids.size() >= 30, {"solids": ground.solids.size()})
	var box: Rect2 = ground.solids[0]
	game.player.position = Vector2(box.position.x - 30, box.get_center().y)
	game.test_axis = Vector2.RIGHT
	game.step_ticks(90)
	var inside := Rect2(box.position - Vector2(Tuning.PLAYER_RADIUS, Tuning.PLAYER_RADIUS) * 0.9, box.size + Vector2(Tuning.PLAYER_RADIUS, Tuning.PLAYER_RADIUS) * 1.8).has_point(game.player.position)
	check("props-block-the-courier", not inside and game.player.position.x < box.position.x, {"box": str(box), "courier": str(game.player.position)})
	var before_y: float = game.player.position.y
	game.test_axis = Vector2(1, 1).normalized()
	game.step_ticks(30)
	check("courier-slides-along-props", game.player.position.y > before_y + 10.0 and game.player.position.x < box.position.x, {"moved_y": game.player.position.y - before_y})
	var puddle_pos: Vector2 = Vector2.ZERO
	for p in ground.props:
		if p["kind"] == "puddle":
			puddle_pos = p["pos"]
			break
	check("decals-do-not-block", not ground.blocks(puddle_pos, Tuning.PLAYER_RADIUS) or _near_solid(ground, puddle_pos))
	var ghost = game.spawn_enemy("wraith", box.get_center())
	ghost.hp = 9999
	game.step_ticks(5)
	check("enemies-pass-through-props", box.grow(20).has_point(ghost.position), {"wraith": str(ghost.position)})

	var synced := true
	var measured := {}
	for kind in ["stall", "cart", "crates"]:
		var t: Texture2D = ground.tex.get(kind)
		if t == null:
			continue
		var used := t.get_image().get_used_rect()
		var expect := Rect2(Vector2(used.position) - t.get_size() / 2 + Vector2(2, 2), Vector2(used.size) - Vector2(4, 4))
		var fixed: Rect2 = ground.SOLID_BOX[kind]
		measured[kind] = str(expect)
		synced = synced and fixed.position.distance_to(expect.position) <= 1.0 and fixed.size.distance_to(expect.size) <= 1.0
	check("solid-boxes-match-sprites", synced, {"from_sprites": measured})
	# Bao, 2026-09-30: puddles and leaves drawn half-transparent so they never outshine the courier or the gems
	check("decals-are-subtle", ground.DECAL_ALPHA >= 0.4 and ground.DECAL_ALPHA <= 0.6, {"alpha": ground.DECAL_ALPHA})
	var again = Ground.new()
	again.build()
	check("map-layout-deterministic", again.props == ground.props)
	again.free()

	# enemies always arrive from off-screen, even with the courier in a corner (review finding)
	await fresh()
	var spots := [Vector2.ZERO, Tuning.ARENA.position + Vector2(30, 30), Vector2(Tuning.ARENA.end.x - 30, 0), Vector2(0, Tuning.ARENA.end.y - 30)]
	var visible := 0
	var outside_arena := 0
	var r := RandomNumberGenerator.new()
	r.seed = 5
	for spot in spots:
		game.player.position = spot
		var view: Rect2 = game.view_rect()
		var wave := []
		for i in 50:
			wave.append({"kind": "moth", "angle": r.randf() * TAU})
		for e in game.spawn_wave(wave):
			if view.grow(Tuning.SPAWN_MARGIN - 1).has_point(e.position):
				visible += 1
			if not Tuning.ARENA.has_point(e.position):
				outside_arena += 1
		for e in game.enemies.duplicate():
			game.enemies.erase(e)
			e.free()
	check("spawns-arrive-off-screen", visible == 0 and outside_arena == 0, {"visible_spawns": visible, "outside_arena": outside_arena, "of": 200})

	# bullets hit what you see (Bao, playtest 2026-09-29: "子弹打到怪物之后要求消失")
	await fresh()
	game.beam_timer = 99999
	var wing = game.spawn_enemy("moth", Vector2(0, -100))
	wing.speed = 0.0
	var s1 = BeamShot.new()
	s1.setup(Vector2(10, -150), Vector2.DOWN, 1)
	game.actors.add_child(s1)
	game.shots.append(s1)
	game.step_ticks(20)
	check("beam-stops-on-moth-wing", game.shots.is_empty() and wing.dead, {"shots_left": game.shots.size(), "moth_dead": wing.dead})
	await fresh()
	game.beam_timer = 99999
	var hood = game.spawn_enemy("wraith", Vector2(120, 0))
	hood.speed = 0.0
	var s2 = BeamShot.new()
	s2.setup(Vector2(60, -18), Vector2.RIGHT, 1)
	game.actors.add_child(s2)
	game.shots.append(s2)
	game.step_ticks(20)
	check("beam-stops-on-wraith-hood", game.shots.is_empty() and hood.hp < Tuning.ENEMIES["wraith"]["hp"], {"shots_left": game.shots.size(), "wraith_hp": hood.hp})
	await fresh()
	game.beam_timer = 99999
	var clear = game.spawn_enemy("moth", Vector2(0, -100))
	clear.speed = 0.0
	var s3 = BeamShot.new()
	s3.setup(Vector2(20, -150), Vector2.DOWN, 1)
	game.actors.add_child(s3)
	game.shots.append(s3)
	game.step_ticks(20)
	check("beam-misses-when-clear-of-sprite", game.shots.size() == 1 and not clear.dead, {"shots_left": game.shots.size()})

	await fresh()
	var above = game.spawn_enemy("moth", Vector2(0, -90))
	var decoy = game.spawn_enemy("moth", Vector2(300, 0))
	game.test_axis = Vector2.ZERO
	game.step_ticks(20)
	check("beam-aims-nearest", above.dead and not decoy.dead, {"nearest_dead": above.dead, "far_dead": decoy.dead})

	await fresh()
	game.prog.add_xp(3)
	game.tick()
	check("levelup-opens", game.state.current == GS.LEVELUP and game.offered.size() == 3 and game.player.pose == "levelup", {"offered": game.offered})
	var frozen: int = game.tick_count
	game.step_ticks(30)
	check("levelup-freezes-sim", game.tick_count == frozen)
	check("choose-card", game.choose_card(0) and game.state.current == GS.PLAYING and game.prog.pending_levelups == 0)
	check("choose-card-rejected-when-playing", not game.choose_card(0))

	await fresh()
	game.prog.add_xp(3 + 5 + 7)
	var opens := 0
	for i in 10:
		game.tick()
		if game.state.current == GS.LEVELUP:
			opens += 1
			game.choose_card(0)
	check("levelup-queue", opens == 3 and game.prog.pending_levelups == 0, {"opens": opens})

	await fresh()
	game.toggle_pause()
	game.prog.add_xp(3)
	game.step_ticks(10)
	check("levelup-while-paused", game.state.current == GS.PAUSED)
	game.toggle_pause()
	game.tick()
	check("levelup-after-unpause", game.state.current == GS.LEVELUP)

	await fresh()
	var hurts: Array = []
	game.player_hurt.connect(func(_hp): hurts.append(game.tick_count))
	var w = game.spawn_enemy("wraith", Vector2.ZERO)
	w.hp = 9999
	for i in 150:
		w.position = game.player.position
		game.tick()
	var spaced := true
	for i in range(1, hurts.size()):
		spaced = spaced and hurts[i] - hurts[i - 1] >= Tuning.IFRAME_TICKS
	check("hurt-iframes", hurts.size() == 4 and spaced, {"hurt_ticks": hurts})
	check("hurt-knockback-and-hp", game.player.hp == Tuning.PLAYER_MAX_HP - 8)

	await fresh()
	game.player.hp = 1
	var w2 = game.spawn_enemy("wraith", game.player.position)
	w2.hp = 9999
	game.tick()
	check("death-lost", game.state.current == GS.LOST and game.player.pose == "defeat")
	var t_end: int = game.tick_count
	game.step_ticks(10)
	check("lost-freezes-sim", game.tick_count == t_end)

	await fresh()
	game.tick_count = Tuning.RUN_SECONDS * Tuning.TICK_HZ - 1
	game.tick()
	check("won-at-3min", game.state.current == GS.WON and game.player.pose == "victory")

	await fresh()
	var terminal := [0]
	game.state.changed.connect(func(_f, t):
		if t == GS.WON or t == GS.LOST:
			terminal[0] += 1)
	game.tick_count = Tuning.RUN_SECONDS * Tuning.TICK_HZ - 1
	game.player.hp = 1
	var w3 = game.spawn_enemy("wraith", game.player.position)
	w3.hp = 9999
	game.tick()
	check("death-and-timer-same-tick", terminal[0] == 1 and game.state.current == GS.LOST)

	await fresh()
	var evo := [0]
	game.evolved.connect(func(): evo[0] += 1)
	for c in ["beam_rate", "beam_pierce", "moth_new", "moth_count", "moth_radius"]:
		game.prog.apply(c)
	game.prog.add_xp(3)
	game.tick()
	check("sunflare-offered", game.offered[0] == "sunflare", {"offered": game.offered})
	game.choose_card(0)
	var ring = game.spawn_enemy("moth", Vector2(200, 0))
	game.step_ticks(Tuning.SUNFLARE_FIRST_DELAY + 1)
	check("sunflare-evolves-once", evo[0] == 1 and game.orbit_positions().is_empty() and game.shots.is_empty() and game.player.empowered)
	check("sunflare-burst-kills", game.enemies.is_empty() and game.banner_ticks > 0)

	await fresh(5, false)
	game.player.hp = 1
	game.step_ticks(20000)
	var lost_first: bool = game.state.is_terminal()
	game.start_run(5)
	check("restart-resets", lost_first and game.state.current == GS.PLAYING and game.tick_count == 0 and game.enemies.is_empty() and game.gems.is_empty() and game.player.hp == Tuning.PLAYER_MAX_HP and game.prog.level == 1)

	# a missing asset must change nothing but the look: same seeded run with and without art, and the
	# placeholders must actually draw (frames are rendered before the session is freed)
	var with_art := await _seeded_summary(9)
	Art.disabled = true
	var without_art := await _seeded_summary(9)
	var placeholder_sheet = game.player.sheet
	Art.disabled = false
	check("missing-art-same-run-and-draws", with_art == without_art and placeholder_sheet == null, {"with_art": with_art, "without_art": without_art})

	await fresh(3, false)
	var chosen: Array = []
	for t in Tuning.RUN_SECONDS * Tuning.TICK_HZ + 10:
		if game.state.is_terminal():
			break
		if game.state.current == GS.LEVELUP:
			chosen.append(game.offered[0])
			game.choose_card(0)
		var a := float(t) / 90.0
		game.test_axis = Vector2(cos(a), sin(a))
		game.tick()
	check("long-run-smoke", game.state.is_terminal(), {"state": GS.NAMES[game.state.current], "seconds": game.tick_count / 60, "kills": game.kills, "level": game.prog.level, "cards": chosen})
	await fresh()
	check("hud-shows-xp-need", _has(game.hud.lines(), "XP 0/3"), {"lines": game.hud.lines()})
	check("hud-shows-timer-hp-level", _has(game.hud.lines(), "0:00") and _has(game.hud.lines(), "HP 10/10") and _has(game.hud.lines(), "Lv 1"), {"lines": game.hud.lines()})
	game.prog.add_xp(3)
	game.tick()
	check("hud-shows-cards", _has(game.hud.lines(), "[1]") and _has(game.hud.lines(), "[3]"), {"lines": game.hud.lines()})
	game.choose_card(0)
	game.toggle_pause()
	check("hud-shows-paused", _has(game.hud.lines(), "PAUSED"))
	game.toggle_pause()
	game.player.hp = 1
	var wx = game.spawn_enemy("wraith", game.player.position)
	wx.hp = 9999
	game.tick()
	check("hud-shows-lost-and-retry", _has(game.hud.lines(), "The lamp went out") and _has(game.hud.lines(), "R / Y to retry"))
	game.audio.toggle_bus("Music")
	check("hud-shows-mute-state", _has(game.hud.lines(), "MUSIC off"))
	game.audio.toggle_bus("Music")
	await fresh()
	for c in ["beam_rate", "beam_pierce", "moth_new", "moth_count", "moth_radius"]:
		game.prog.apply(c)
	game.prog.add_xp(3)
	game.tick()
	game.choose_card(0)
	game.player.hp = 1
	var wb = game.spawn_enemy("wraith", game.player.position)
	wb.hp = 9999
	game.step_ticks(40)
	check("end-panel-hides-banner-and-ring", game.state.current == GS.LOST and not _has(game.hud.lines(), "SUNFLARE LIGHTHOUSE") and not game.fx.ring_visible(), {"lines": game.hud.lines()})
	# storyboard camera moves (visual only; the simulation never reads the camera)
	await fresh()
	for c in ["beam_rate", "beam_pierce", "moth_new", "moth_count", "moth_radius"]:
		game.prog.apply(c)
	game.prog.add_xp(3)
	game.tick()
	game.choose_card(game.offered.find("sunflare"))
	game.step_ticks(game.camera.SUNFLARE_OUT_TICKS)
	var zoomed_out: float = game.camera.zoom.x
	game.step_ticks(game.camera.SUNFLARE_BACK_TICKS + 5)
	check("camera-sunflare-zoom-out", zoomed_out < 0.8 and is_equal_approx(game.camera.zoom.x, 1.0), {"at_peak": zoomed_out, "after": game.camera.zoom.x})

	await fresh()
	var wt = game.spawn_enemy("wraith", game.player.position)
	wt.hp = 9999
	game.tick()
	var tilt: float = game.camera.rotation
	game.enemies.erase(wt)
	wt.queue_free()
	game.step_ticks(Tuning.HURT_POSE_TICKS + 2)
	check("camera-hurt-tilt", absf(tilt) > 0.02 and is_zero_approx(game.camera.rotation), {"tilt": tilt, "after": game.camera.rotation})

	# the title push-in and the fog lifting run on real time, because the simulation is stopped then
	game.free()
	game = Session.new()
	game.test_mode = true
	game.test_no_spawn = true
	root.add_child(game)
	var z0: float = game.camera.zoom.x
	await create_timer(0.6).timeout
	check("camera-menu-push-in", game.state.current == GS.MENU and z0 < game.camera.zoom.x and game.camera.zoom.x <= 1.0, {"start": z0, "after": game.camera.zoom.x})
	game.start_run(1)
	check("camera-reset-on-start", is_equal_approx(game.camera.zoom.x, 1.0) and is_zero_approx(game.camera.rotation))
	game.tick_count = Tuning.RUN_SECONDS * Tuning.TICK_HZ - 1
	game.tick()
	await create_timer(0.6).timeout
	check("fog-lifts-on-win", game.state.current == GS.WON and game.camera.fog_lift() > 0.1 and game.camera.zoom.x < 1.0, {"lift": game.camera.fog_lift(), "zoom": game.camera.zoom.x})
	completed = true

func _has(lines: PackedStringArray, needle: String) -> bool:
	for l in lines:
		if needle in l:
			return true
	return false

func _near_solid(ground, p: Vector2) -> bool:
	for r in ground.solids:
		if r.grow(Tuning.PLAYER_RADIUS).has_point(p):
			return true
	return false

func _seeded_summary(seed_value: int) -> Dictionary:
	await fresh(seed_value, false)
	game.test_axis = Vector2(1, 0.3)
	for i in 600:
		if game.state.current == GS.LEVELUP:
			game.choose_card(0)
		game.tick()
	for i in 2:
		await process_frame
	return {"state": GS.NAMES[game.state.current], "tick": game.tick_count, "kills": game.kills, "level": game.prog.level,
		"hp": game.player.hp, "x": snappedf(game.player.position.x, 0.01), "y": snappedf(game.player.position.y, 0.01)}
