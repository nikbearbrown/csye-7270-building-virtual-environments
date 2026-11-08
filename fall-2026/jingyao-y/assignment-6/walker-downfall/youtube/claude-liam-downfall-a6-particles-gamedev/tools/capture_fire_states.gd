extends SceneTree
## FILM CAPTURE HELPER (A6 film only; not part of the game or its tests).
## Fixture, not gameplay: the real game on the real Sami floor used by
## previews/fire_pit_flames_preview.gd (seed 2026 + seed_rng, pit 1, the
## "capture" modal so fuel does not burn on its own). The pit's own
## FirePitFlames is driven only through FirePit.feed()/burn() and the tree's
## pause flag / the effect root's visibility, to show on screen what the state
## test asserts headlessly (B1 lit full, B4 tree pause, B5 hide/show, B3 thin,
## B2 out). An on-screen label names each phase.
## Timeline (Movie Maker frames at 30 fps): 10 feed 120 s; 60-105 tree paused;
## 140-170 effect root hidden; 200 burn to 24 s; 260 burn to 0.

var rig: Node
var game: GameManager
var pit: FirePit
var fx: Node3D
var label: Label
var frame := 0

func _initialize() -> void:
	call_deferred("run")

func find_game(node: Node) -> GameManager:
	if node is GameManager: return node
	for child in node.get_children():
		var found := find_game(child)
		if found != null: return found
	return null

func say(text: String) -> void:
	label.text = "FIXTURE (film capture, not gameplay): " + text
	var flames := fx.get_node("Flames") as GPUParticles3D
	print("FILM_STATE frame %d engine_frame %d %s | burn_left %.1f emitting %s amount_ratio %.4f visible %s paused %s" % [frame, Engine.get_process_frames(), text, pit.burn_left, flames.emitting, flames.amount_ratio, fx.visible, paused])

func step(n: int = 1) -> void:
	for i in range(n):
		await process_frame
		frame += 1
		if fx != null and game._hud.visible: game._hud.hide()

func run() -> void:
	rig = load("res://game/main.tscn").instantiate()
	rig.persist_sessions = false
	rig.process_mode = Node.PROCESS_MODE_PAUSABLE
	root.add_child(rig)
	var layer := CanvasLayer.new()
	layer.layer = 100
	layer.process_mode = Node.PROCESS_MODE_ALWAYS
	root.add_child(layer)
	label = Label.new()
	label.position = Vector2(10, 6)
	label.add_theme_font_size_override("font_size", 16)
	label.add_theme_color_override("font_outline_color", Color.BLACK)
	label.add_theme_constant_override("outline_size", 4)
	layer.add_child(label)
	await step(1)
	game = find_game(rig)
	game.fixed_map_seed = 2026
	game.seed_rng(2026)
	await game.start_contract("snow")
	game.open_modal("capture")
	var valid := game.fires.filter(func(f): return is_instance_valid(f))
	pit = valid[1]
	game.player.teleport(game.world_map.nearest_walkable(pit.global_position + Vector3(2.5, 0.0, 0.0)))
	fx = pit.get_node("FirePitFlames") as Node3D
	for child in fx.get_children():
		if child is GPUParticles3D:
			child.use_fixed_seed = true
			child.seed = 7370
	game._hud.hide()
	say("pit cold, burn_left 0")
	while frame < 10: await step()
	pit.feed(120.0 - pit.burn_left)
	say("fed 120 s -> lit, amount_ratio 1.0")
	while frame < 60: await step()
	paused = true
	say("get_tree().paused = true (frozen)")
	while frame < 105: await step()
	paused = false
	say("tree running again")
	while frame < 140: await step()
	fx.visible = false
	say("FirePitFlames.visible = false")
	while frame < 170: await step()
	fx.visible = true
	say("shown again at the current ratio")
	while frame < 200: await step()
	pit.burn(pit.burn_left - 24.0)
	say("burn_left 24 s -> amount_ratio 0.44")
	while frame < 260: await step()
	pit.burn(pit.burn_left)
	say("burn_left 0 -> emitting false; live particles finish")
	while true:
		if game._hud.visible: game._hud.hide()
		await step()
