extends Node
## Windowed capture for inspection: 1920×1080 screenshots into evidence/<step>/
## in the repository. It opens a window; run from the repository root:
##   Godot --path game --resolution 1920x1080 --always-on-top res://tests/capture.tscn -- 1a 1b
## Name the steps after "--"; without them it captures every step. Add
## --debug-collisions to draw the collision shapes; those files end in
## "-collisions". --always-on-top keeps macOS from slowing a hidden window.
## - 1a: Rudy's movement poses on flat ground (the spikes and goblins hidden).
## - 1b: the opening, the lit waystone, a fall into a cliff, the respawn, the
##   teleport circle and the end card (STORYBOARD.md panels 1, 5, 6 and 7).
## - 1c: a jump over the spikes, a stomp, a hit from a goblin with the hearts
##   and the flash, and the defeat (panels 2 and 4).
## - 1d: the sword-and-shield pickup, the sword form, a slash that cuts a
##   goblin, and the gear flying off after a hit (panels 3 and 4).
## - 2a: Rudy's generated frames with the outer outline: every pose he can take,
##   facing right and left, and the flash, each cropped around him at game
##   size (520 x 380 px); and two full screens, the opening and the slash.
## - 2b: the Level 1 layers and ground: the opening, each row of spikes
##   (cropped; their art came in after the 2b playtest), both cliffs from beside
##   them and in a jump, a fall into a pit, the squeezed middle run of tiles,
##   the pull-back on the teleport circle, and Rudy over the wheat in both
##   forms and over the sky in a jump, cropped. The spikes, the goblins and the pickup are hidden except
##   in the opening; they are swapped in 2c.
## - 2c: the props, the goblin, the hearts and the end card: the opening; the
##   goblin walking (both frames), stomped and cut; the pickup, the sword form
##   and the gear flying off; the waystone dark, lighting (its ring) and lit
##   (its halo); a hit with the hearts;
##   the teleport circle in the pull-back; and the end card. Cropped around Rudy
##   except the opening, the hit, the circle and the end card.
## - 2d: the title over the opening, the title fading out, and play started.
## - 3: the audio, for Godot's movie maker, which records the game's own mix:
##     Godot --path game --resolution 1920x1080 --always-on-top --write-movie <file>.avi res://tests/capture.tscn -- 3
##   The title with the music under it, then in play a jump, the pickup, a
##   slash, a stomp, a hit from the spikes (the music dips), the pause (the one
##   screenshot), the music muted with M and back, a fall and the respawn (the
##   music dips), and the teleport circle (it fades out) to the silent end
##   card. Each frame's sounds, the music's level and the pause go to
##   3-mix-events.json, which design/tools/plot_mix.py draws under the mix.
## - 5: the evidence for TEST-REPORT.md, from the final build. The moment of
##   each storyboard panel, full screen (panel-1 to panel-7); then every pose
##   Rudy can take, facing right and then left, cropped around him (the poses
##   CHARACTER-SHEET.md names; a respawn always faces right). With
##   --debug-collisions only the poses are captured.
##   design/tools/compare_sheets.py puts them beside the storyboard and the
##   character sheet.

const MAIN := preload("res://app/main.tscn")
const SIZE := Vector2i(1920, 1080)
const CROP := Vector2i(520, 380) ## around Rudy, his soles 300 px from the top
const PNG_STEPS := ["1a", "1b", "1c", "1d", "2a"] ## over the greybox; later full screens show painted art and are saved as JPEG
const JPEG_CROP_STEPS := ["5"] ## sixty crops over painted art: as PNG they would be about 14 MB

var _main: Main
var _rudy: Rudy
var _step := ""
var _mix_log := {} ## step 3: what happened each frame
var _sounds_seen: Dictionary[StringName, int] = {}


func _ready() -> void:
	var steps := Array(OS.get_cmdline_user_args())
	if steps.is_empty():
		steps = ["1a", "1b", "1c", "1d", "2a", "2b", "2c", "2d", "3", "5"]
	for step: String in steps:
		_step = step
		DirAccess.make_dir_recursive_absolute(_out_dir())
		Main.title_shown = step not in ["2d", "3", "5"] # only these steps open on the title
		_main = MAIN.instantiate()
		add_child(_main)
		_rudy = _main.get_node("Rudy")
		await _frames(30)
		match step:
			"1a":
				await _capture_1a()
			"1b":
				await _capture_1b()
			"1c":
				await _capture_1c()
			"1d":
				await _capture_1d()
			"2a":
				await _capture_2a()
			"2b":
				await _capture_2b()
			"2c":
				await _capture_2c()
			"2d":
				await _capture_2d()
			"3":
				await _capture_3()
			"5":
				await _capture_5()
			_:
				push_error("no capture for step %s" % step)
		_main.queue_free()
		await _frames(2)
	get_tree().quit()


func _capture_1a() -> void:
	for path: String in ["Level1/Hazards", "Level1/Enemies"]:
		var threats: Node2D = _main.get_node(path)
		threats.process_mode = Node.PROCESS_MODE_DISABLED
		threats.visible = false
	await _shot("idle")
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _rudy.pose == &"CHAR-RUN-A")
	await _shot("run-a")
	await _until(func() -> bool: return _rudy.pose == &"CHAR-RUN-B")
	await _shot("run-b")
	await _frames(40) # let the camera start following
	Input.action_press(&"jump")
	await _until(func() -> bool: return _rudy.pose == &"CHAR-RISE")
	await _frames(10)
	await _shot("rise")
	Input.action_release(&"jump")
	await _until(func() -> bool: return _rudy.pose == &"CHAR-FALL")
	await _frames(10)
	await _shot("fall")
	await _until(func() -> bool: return _rudy.pose == &"CHAR-RUN-A")
	Input.action_release(&"move_right")
	Input.action_press(&"move_left")
	await _frames(30)
	await _shot("run-left")
	Input.action_release(&"move_left")
	await _frames(20)
	await _shot("idle-left")


func _capture_1b() -> void:
	var waystone: Waystone = _main.get_node("Level1/Waystone")
	var portal: Portal = _main.get_node("Level1/Portal")
	await _shot("opening") # panel 1, without the title
	# Run past the waystone and stop beside it.
	_rudy.global_position = Vector2(waystone.global_position.x - 500.0, 840.0)
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _rudy.global_position.x > waystone.spawn_point.global_position.x - 30.0)
	Input.action_release(&"move_right")
	await _frames(60)
	await _shot("waystone-lit")
	# Walk into the first cliff (panel 5).
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _rudy.global_position.y > 950.0)
	Input.action_release(&"move_right")
	await _shot("cliff-fall")
	await _until(func() -> bool: return _rudy.mode == Rudy.Mode.RESPAWNING)
	await _frames(28) # the fade-in is over
	await _shot("respawn")
	await _until(func() -> bool: return _main.state == Main.State.PLAYING)
	# Onto the teleport circle (panel 6), then the end card.
	_rudy.global_position = Vector2(portal.global_position.x - 600.0, 840.0)
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _main.state == Main.State.COMPLETE)
	Input.action_release(&"move_right")
	await _frames(100) # the light has risen and the camera has pulled back
	await _shot("teleport-circle")
	var hud: Hud = _main.get_node("Hud")
	await _until(func() -> bool: return hud.is_showing_end_card())
	await _frames(5)
	await _shot("end-card")


func _capture_1c() -> void:
	var spikes: Spikes = _main.get_node("Level1/Hazards/SpikesA")
	var goblin_a: Goblin = _main.get_node("Level1/Enemies/GoblinA")
	var goblin_b: Goblin = _main.get_node("Level1/Enemies/GoblinB")
	# Over the spikes, toward the first goblin (panel 2).
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _rudy.global_position.x >= spikes.global_position.x - 180.0)
	Input.action_press(&"jump")
	await _until(func() -> bool: return _rudy.global_position.x >= spikes.global_position.x)
	Input.action_release(&"jump")
	await _shot("over-the-spikes")
	# Keep running until he has landed past them: let go in the air and he drops onto them.
	await _until(func() -> bool:
		return _rudy.is_on_floor() and _rudy.global_position.x > spikes.global_position.x + 100.0)
	Input.action_release(&"move_right")
	# From here the goblins hold still, so each shot is set up exactly.
	for goblin: Goblin in [goblin_a, goblin_b]:
		goblin.speed = 0.0
	# Onto a goblin from above: the stomp.
	await _until(func() -> bool: return _rudy.mode == Rudy.Mode.PLAY and _rudy.is_on_floor())
	_rudy.global_position = Vector2(goblin_a.global_position.x, 840.0 - Goblin.HEIGHT - 120.0)
	_rudy.velocity = Vector2(0, 100)
	await _frames(1)
	await _until(func() -> bool: return goblin_a.dead)
	await _frames(4)
	await _shot("stomp")
	await _until(func() -> bool: return _rudy.is_on_floor())
	# Walking into a goblin, three times: a heart each, the knockback and the
	# flash (panel 4), then the defeat.
	for shot: String in ["hurt", "hurt-again", "defeat"]:
		await _until(func() -> bool:
			return _rudy.mode == Rudy.Mode.PLAY and _rudy.is_on_floor() and not _rudy.is_invulnerable())
		_rudy.global_position = Vector2(goblin_b.global_position.x - 120.0, 840.0)
		_rudy.velocity = Vector2.ZERO
		await _frames(2)
		var hearts := _rudy.hearts
		Input.action_press(&"move_right")
		await _until(func() -> bool: return _rudy.hearts < hearts)
		Input.action_release(&"move_right")
		await _frames(30 if shot == "defeat" else 4)
		await _shot(shot)


func _capture_1d() -> void:
	var pickup: SwordPickup = _main.get_node("Level1/SwordPickup")
	var spikes: Spikes = _main.get_node("Level1/Hazards/SpikesA")
	var goblin_b: Goblin = _main.get_node("Level1/Enemies/GoblinB")
	goblin_b.speed = 0.0 # it holds still for the slash
	# Running up to the pickup (panel 3, in play).
	_rudy.global_position = Vector2(pickup.global_position.x - 330.0, 840.0)
	await _frames(2)
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _rudy.global_position.x >= pickup.global_position.x - 90.0)
	await _shot("pickup")
	await _until(func() -> bool: return _rudy.gear == Rudy.Gear.SWORD)
	Input.action_release(&"move_right")
	await _until(func() -> bool: return _rudy.is_on_floor() and _rudy.velocity.x == 0.0)
	await _frames(10)
	await _shot("sword-idle")
	# A cut that reaches a goblin.
	_rudy.global_position = Vector2(goblin_b.global_position.x - 70.0, 840.0)
	await _frames(4)
	Input.action_press(&"slash")
	await _until(func() -> bool: return goblin_b.dead)
	Input.action_release(&"slash")
	await _frames(2)
	await _shot("slash")
	await _until(func() -> bool: return not _rudy.is_slashing())
	# A hit takes the gear: it flies off (panel 4).
	_rudy.global_position = Vector2(spikes.global_position.x - 200.0, 840.0)
	await _frames(2)
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _rudy.gear == Rudy.Gear.NONE)
	Input.action_release(&"move_right")
	await _frames(8)
	await _shot("gear-flies")


func _capture_2a() -> void:
	await _shot("opening")
	var hazards: Node2D = _main.get_node("Level1/Hazards")
	var enemies: Node2D = _main.get_node("Level1/Enemies")
	for threats: Node2D in [hazards, enemies]:
		threats.process_mode = Node.PROCESS_MODE_DISABLED
		threats.visible = false
	# The default form's movement, as in 1a.
	await _shot("idle", true)
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _rudy.pose == &"CHAR-RUN-A")
	await _shot("run-a", true)
	await _until(func() -> bool: return _rudy.pose == &"CHAR-RUN-B")
	await _shot("run-b", true)
	Input.action_press(&"jump")
	await _until(func() -> bool: return _rudy.pose == &"CHAR-RISE")
	await _frames(10)
	await _shot("rise", true)
	Input.action_release(&"jump")
	await _until(func() -> bool: return _rudy.pose == &"CHAR-FALL")
	await _frames(8)
	await _shot("fall", true)
	await _until(func() -> bool: return _rudy.is_on_floor())
	Input.action_release(&"move_right")
	Input.action_press(&"move_left")
	await _frames(30)
	Input.action_release(&"move_left")
	await _frames(20)
	await _shot("idle-left", true)
	# The spikes: the hit, the flash, then the defeat and the respawn.
	hazards.process_mode = Node.PROCESS_MODE_INHERIT
	hazards.visible = true
	var spikes: Spikes = hazards.get_node("SpikesA")
	_rudy.global_position = Vector2(spikes.global_position.x - 220.0, 840.0)
	await _frames(2)
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _rudy.mode == Rudy.Mode.HURT)
	Input.action_release(&"move_right")
	var look: Node2D = _rudy.get_node("Look")
	await _until(func() -> bool: return look.modulate.a == 1.0) # between flashes
	await _shot("hurt", true)
	await _until(func() -> bool: return _rudy.is_on_floor() and look.modulate.a < 1.0)
	await _shot("flash", true)
	await _until(func() -> bool: return _rudy.mode == Rudy.Mode.PLAY and not _rudy.is_invulnerable())
	_rudy.hearts = 1 # the next hit is the last heart
	_rudy.global_position = Vector2(spikes.global_position.x - 220.0, 840.0)
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _rudy.mode == Rudy.Mode.DEFEATED)
	Input.action_release(&"move_right")
	await _frames(20)
	await _shot("defeat", true)
	await _until(func() -> bool: return _rudy.mode == Rudy.Mode.RESPAWNING)
	await _frames(28) # the fade-in is over
	await _shot("respawn", true)
	await _until(func() -> bool: return _main.state == Main.State.PLAYING)
	hazards.process_mode = Node.PROCESS_MODE_DISABLED
	hazards.visible = false
	# The sword form: the pickup, its movement, its idle and the slash.
	var pickup: SwordPickup = _main.get_node("Level1/SwordPickup")
	_rudy.global_position = Vector2(pickup.global_position.x - 300.0, 840.0)
	await _frames(2)
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _rudy.gear == Rudy.Gear.SWORD)
	await _until(func() -> bool: return _rudy.pose == &"CHAR-SWORD-RUN-A")
	await _shot("sword-run-a", true)
	await _until(func() -> bool: return _rudy.pose == &"CHAR-SWORD-RUN-B")
	await _shot("sword-run-b", true)
	Input.action_press(&"jump")
	await _until(func() -> bool: return _rudy.pose == &"CHAR-SWORD-RISE")
	await _frames(10)
	await _shot("sword-rise", true)
	Input.action_release(&"jump")
	await _until(func() -> bool: return _rudy.pose == &"CHAR-SWORD-FALL")
	await _frames(8)
	await _shot("sword-fall", true)
	await _until(func() -> bool: return _rudy.is_on_floor())
	Input.action_release(&"move_right")
	await _frames(30)
	await _shot("sword-idle", true)
	Input.action_press(&"slash")
	await _until(func() -> bool: return _rudy.pose == &"CHAR-SWORD-SLASH")
	Input.action_release(&"slash")
	await _frames(6)
	await _shot("slash", true)
	await _shot("slash-full")
	# On the teleport circle.
	var portal: Portal = _main.get_node("Level1/Portal")
	_rudy.global_position = Vector2(portal.global_position.x - 400.0, 840.0)
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _main.state == Main.State.COMPLETE)
	Input.action_release(&"move_right")
	await _frames(40)
	await _shot("celebrate", true)


func _capture_2b() -> void:
	await _shot("opening")
	# Each row of spikes, with the outline, between two wheat tufts.
	for spikes: Spikes in _main.get_node("Level1/Hazards").get_children():
		_rudy.global_position = Vector2(spikes.global_position.x - 170.0, 840.0)
		_main._snap_camera()
		await _frames(10)
		await _shot("spikes-" + String(spikes.name).right(1).to_lower(), true)
	for path: String in ["Level1/Hazards", "Level1/Enemies", "Level1/SwordPickup"]:
		var hidden: Node2D = _main.get_node(path)
		hidden.process_mode = Node.PROCESS_MODE_DISABLED
		hidden.visible = false
	# Beside each cliff, then over it.
	for cliff: Array in [["first-cliff", 4300.0], ["second-cliff", 6400.0]]:
		_rudy.global_position = Vector2(cliff[1] - 160.0, 840.0)
		_main._snap_camera()
		await _frames(20)
		await _shot(cliff[0])
		Input.action_press(&"move_right")
		await _until(func() -> bool: return _rudy.global_position.x >= cliff[1] - 90.0)
		Input.action_press(&"jump")
		await _until(func() -> bool: return _rudy.global_position.x >= cliff[1] + 100.0)
		Input.action_release(&"jump")
		await _shot(cliff[0] + "-jump")
		if cliff[0] == "first-cliff":
			await _shot("jump-over-sky", true)
		await _until(func() -> bool: return _rudy.is_on_floor())
		Input.action_release(&"move_right")
		await _frames(20)
	# The middle run of tiles, squeezed to fit between the cliffs.
	_rudy.global_position = Vector2(5450.0, 840.0)
	_main._snap_camera()
	await _frames(20)
	await _shot("middle-run")
	# Rudy over the generated wheat, in both forms, cropped for the readability check.
	await _shot("on-wheat", true)
	_rudy.equip_sword()
	await _frames(5)
	await _shot("sword-on-wheat", true)
	# A fall into the first pit (panel 5).
	_rudy.global_position = Vector2(4220.0, 840.0)
	_main._snap_camera()
	await _frames(10)
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _rudy.global_position.y > 960.0)
	Input.action_release(&"move_right")
	await _shot("fall")
	await _until(func() -> bool: return _main.state == Main.State.PLAYING)
	# The pull-back on the teleport circle (panel 6).
	var portal: Portal = _main.get_node("Level1/Portal")
	_rudy.global_position = Vector2(portal.global_position.x - 500.0, 840.0)
	_main._snap_camera()
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _main.state == Main.State.COMPLETE)
	Input.action_release(&"move_right")
	await _frames(100) # the light has risen and the camera has pulled back
	await _shot("teleport-circle")


func _capture_2c() -> void:
	await _shot("opening")
	var goblin_a: Goblin = _main.get_node("Level1/Enemies/GoblinA")
	var goblin_b: Goblin = _main.get_node("Level1/Enemies/GoblinB")
	# The goblin walking toward him, in each walk frame; he turns to face it.
	_rudy.global_position = Vector2(goblin_a.global_position.x + 220.0, 840.0)
	_main._snap_camera()
	await _frames(2)
	Input.action_press(&"move_left")
	await _frames(3) # a tap turns him in place
	Input.action_release(&"move_left")
	var art: Sprite2D = goblin_a.get_node("Art")
	await _until(func() -> bool: return art.texture == Goblin.WALK_A)
	await _shot("goblin-walk-a", true)
	await _until(func() -> bool: return art.texture == Goblin.WALK_B)
	await _shot("goblin-walk-b", true)
	goblin_a.speed = 0.0
	# A stomp: the squashed frame.
	_rudy.global_position = Vector2(goblin_a.global_position.x, 840.0 - Goblin.HEIGHT - 120.0)
	_rudy.velocity = Vector2(0, 100)
	await _until(func() -> bool: return goblin_a.dead)
	await _shot("stomp", true)
	# The pickup, then the sword form beside a goblin, and a cut.
	var pickup: SwordPickup = _main.get_node("Level1/SwordPickup")
	_rudy.global_position = Vector2(pickup.global_position.x - 160.0, 840.0)
	_main._snap_camera()
	await _frames(20)
	await _shot("pickup", true)
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _rudy.gear == Rudy.Gear.SWORD)
	Input.action_release(&"move_right")
	goblin_b.speed = 0.0
	_rudy.global_position = Vector2(goblin_b.global_position.x - 160.0, 840.0)
	_main._snap_camera()
	await _frames(20)
	await _shot("sword-and-goblin", true)
	_rudy.global_position = Vector2(goblin_b.global_position.x - 70.0, 840.0)
	await _frames(4)
	Input.action_press(&"slash")
	await _until(func() -> bool: return goblin_b.dead)
	Input.action_release(&"slash")
	await _frames(2)
	await _shot("slash", true)
	await _until(func() -> bool: return not _rudy.is_slashing())
	# A hit takes the gear: it flies off; the next takes a heart (the hearts in the HUD).
	var spikes: Spikes = _main.get_node("Level1/Hazards/SpikesA")
	_rudy.global_position = Vector2(spikes.global_position.x - 200.0, 840.0)
	_main._snap_camera()
	await _frames(2)
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _rudy.gear == Rudy.Gear.NONE)
	Input.action_release(&"move_right")
	await _frames(8)
	await _shot("gear-flies", true)
	await _until(func() -> bool: return _rudy.mode == Rudy.Mode.PLAY and not _rudy.is_invulnerable())
	_rudy.global_position = Vector2(spikes.global_position.x - 200.0, 840.0)
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _rudy.hearts < 3)
	Input.action_release(&"move_right")
	await _frames(4)
	await _shot("hit-hearts")
	# The waystone, dark, then lit.
	await _until(func() -> bool: return _rudy.mode == Rudy.Mode.PLAY and _rudy.is_on_floor() and not _rudy.is_invulnerable())
	var waystone: Waystone = _main.get_node("Level1/Waystone")
	_rudy.global_position = Vector2(waystone.global_position.x - 200.0, 840.0)
	_main._snap_camera()
	await _frames(20)
	await _shot("waystone-dark", true)
	Input.action_press(&"move_right")
	await _until(func() -> bool: return waystone.lit)
	Input.action_release(&"move_right")
	await _frames(12)
	await _shot("waystone-ring", true)
	await _until(func() -> bool: return not waystone.is_ringing())
	await _hold(&"move_right", 14) # a step past it, so it shows beside him
	await _frames(10)
	await _shot("waystone-lit", true)
	# The teleport circle, pulled back, then the end card.
	var portal: Portal = _main.get_node("Level1/Portal")
	_rudy.global_position = Vector2(portal.global_position.x - 500.0, 840.0)
	_main._snap_camera()
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _main.state == Main.State.COMPLETE)
	Input.action_release(&"move_right")
	await _frames(100)
	await _shot("teleport-circle")
	var hud: Hud = _main.get_node("Hud")
	await _until(func() -> bool: return hud.is_showing_end_card())
	await _frames(30)
	await _shot("end-card")


func _capture_2d() -> void:
	await _shot("title")
	await _press_in_process(&"restart")
	await _frames(8) # halfway through the fade
	await _shot("title-fading")
	await _frames(30)
	await _shot("play")


func _capture_3() -> void:
	_mix_log = {"fps": Engine.physics_ticks_per_second, "frames": [], "music_db": [], "music_playing": [],
		"music_muted": [], "sfx_muted": [], "paused": [], "state": [], "sounds": [], "music_starts": [], "music_pos": []}
	_sounds_seen = Sfx.counts.duplicate()
	get_tree().process_frame.connect(_log_mix)
	var level: Node2D = _main.get_node("Level1")
	await _frames(90) # the title, with the music under it
	await _press_in_process(&"restart")
	await _frames(60)
	await _hold(&"jump", 3)
	await _frames(60)
	# The pickup, then a slash.
	var pickup: SwordPickup = level.get_node("SwordPickup")
	_rudy.global_position = Vector2(pickup.global_position.x - 160.0, 840.0)
	_main._snap_camera()
	await _frames(20)
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _rudy.gear == Rudy.Gear.SWORD)
	Input.action_release(&"move_right")
	await _frames(45)
	await _hold(&"slash", 3)
	await _frames(45)
	# A stomp.
	var goblin: Goblin = level.get_node("Enemies/GoblinB")
	goblin.speed = 0.0
	_rudy.global_position = Vector2(goblin.global_position.x, 840.0 - Goblin.HEIGHT - 120.0)
	_rudy.velocity = Vector2(0, 100)
	_main._snap_camera()
	await _until(func() -> bool: return goblin.dead)
	await _frames(60)
	# A hit from the spikes: the gear flies off, and the music dips.
	var spikes: Spikes = level.get_node("Hazards/SpikesA")
	_rudy.global_position = Vector2(spikes.global_position.x - 200.0, 840.0)
	_main._snap_camera()
	await _frames(20)
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _rudy.mode == Rudy.Mode.HURT)
	Input.action_release(&"move_right")
	await _frames(90)
	# The pause, then the music muted for a moment.
	await _press_in_process(&"pause")
	await _frames(30)
	await _shot("paused")
	await _frames(90)
	await _press_in_process(&"pause")
	await _frames(45)
	await _press_in_process(&"mute_music")
	await _frames(90)
	await _press_in_process(&"mute_music")
	await _frames(45)
	# A fall into the first cliff, and the respawn.
	var waystone: Waystone = level.get_node("Waystone")
	_rudy.global_position = Vector2(waystone.global_position.x - 300.0, 840.0)
	_main._snap_camera()
	await _frames(20)
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _main.state == Main.State.DYING)
	Input.action_release(&"move_right")
	await _until(func() -> bool: return _main.state == Main.State.PLAYING)
	await _frames(60)
	# The teleport circle, then the silent end card.
	var portal: Portal = level.get_node("Portal")
	_rudy.global_position = Vector2(portal.global_position.x - 300.0, 840.0)
	_main._snap_camera()
	await _frames(20)
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _main.state == Main.State.COMPLETE)
	Input.action_release(&"move_right")
	var hud: Hud = _main.get_node("Hud")
	await _until(func() -> bool: return hud.is_showing_end_card())
	await _frames(120)
	get_tree().process_frame.disconnect(_log_mix)
	var path := _out_dir().path_join("3-mix-events.json")
	FileAccess.open(path, FileAccess.WRITE).store_string(JSON.stringify(_mix_log))
	print("saved %s (%d frames)" % [path.get_file(), _mix_log.frames.size()])


func _capture_5() -> void:
	if not get_tree().debug_collisions_hint:
		await _capture_panels()
	for dir: int in [1, -1]:
		await _fresh_main()
		await _capture_poses(dir)


## The moment of each storyboard panel, in the order of a run.
func _capture_panels() -> void:
	var level: Node2D = _main.get_node("Level1")
	var hud: Hud = _main.get_node("Hud")
	await _shot("panel-1") # the title over the opening
	await _press_in_process(&"restart")
	await _frames(30)
	# Panel 2: running at the spikes, at the top of the jump over them, the goblin ahead.
	var spikes: Spikes = level.get_node("Hazards/SpikesA")
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _rudy.global_position.x >= spikes.global_position.x - 200.0)
	Input.action_press(&"jump")
	await _until(func() -> bool: return not _rudy.is_on_floor())
	Input.action_release(&"jump")
	await _until(func() -> bool: return _rudy.velocity.y >= 0.0)
	await _shot("panel-2")
	Input.action_release(&"move_right")
	# Panel 3: just after the pickup, in the sword form.
	var pickup: SwordPickup = level.get_node("SwordPickup")
	_rudy.global_position = Vector2(pickup.global_position.x - 200.0, 840.0)
	_main._snap_camera()
	await _frames(20)
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _rudy.gear == Rudy.Gear.SWORD)
	Input.action_release(&"move_right")
	await _frames(8)
	await _shot("panel-3")
	# Panel 4: walking into a goblin knocks the gear away; the hearts stay at three.
	var goblin: Goblin = level.get_node("Enemies/GoblinB")
	_rudy.global_position = Vector2(goblin.global_position.x - 260.0, 840.0)
	_main._snap_camera()
	await _frames(20)
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _rudy.gear == Rudy.Gear.NONE)
	Input.action_release(&"move_right")
	await _frames(6)
	await _shot("panel-4")
	# Panel 5: light the waystone, fall into the first cliff, and get back up beside it.
	await _until(func() -> bool: return _rudy.mode == Rudy.Mode.PLAY and _rudy.is_on_floor())
	var waystone: Waystone = level.get_node("Waystone")
	_rudy.global_position = Vector2(waystone.global_position.x - 300.0, 840.0)
	_main._snap_camera()
	await _frames(20)
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _main.state == Main.State.DYING)
	Input.action_release(&"move_right")
	await _until(func() -> bool: return _rudy.mode == Rudy.Mode.RESPAWNING)
	await _frames(28) # the fade-in is over
	await _shot("panel-5")
	# Panel 6: onto the teleport circle; the light has risen and the camera pulled back.
	await _until(func() -> bool: return _main.state == Main.State.PLAYING)
	var portal: Portal = level.get_node("Portal")
	_rudy.global_position = Vector2(portal.global_position.x - 500.0, 840.0)
	_main._snap_camera()
	await _frames(20)
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _main.state == Main.State.COMPLETE)
	Input.action_release(&"move_right")
	await _frames(100)
	await _shot("panel-6")
	# Panel 7: the end card.
	await _until(func() -> bool: return hud.is_showing_end_card())
	await _frames(30)
	await _shot("panel-7")


## Every pose, facing `dir` (1 right, -1 left), cropped around him. The spikes,
## the goblins and the pickup are hidden except where a pose needs them.
func _capture_poses(dir: int) -> void:
	var side := "right" if dir == 1 else "left"
	var move := &"move_right" if dir == 1 else &"move_left"
	var level: Node2D = _main.get_node("Level1")
	var hazards: Node2D = level.get_node("Hazards")
	var pickup: SwordPickup = level.get_node("SwordPickup")
	for node: Node2D in [hazards, level.get_node("Enemies") as Node2D]:
		node.process_mode = Node.PROCESS_MODE_DISABLED
		node.visible = false
	# The default form's movement, between the pickup and the waystone.
	_rudy.global_position = Vector2(2700.0 if dir == 1 else 3400.0, 840.0)
	_main._snap_camera()
	await _frames(20)
	Input.action_press(move)
	await _until(func() -> bool: return _rudy.pose == &"CHAR-RUN-A")
	await _frames(2)
	await _shot("CHAR-RUN-A-" + side, true)
	await _until(func() -> bool: return _rudy.pose == &"CHAR-RUN-B")
	await _frames(2)
	await _shot("CHAR-RUN-B-" + side, true)
	Input.action_press(&"jump")
	await _until(func() -> bool: return _rudy.pose == &"CHAR-RISE")
	await _frames(10)
	await _shot("CHAR-RISE-" + side, true)
	Input.action_release(&"jump")
	await _until(func() -> bool: return _rudy.pose == &"CHAR-FALL")
	await _frames(8)
	await _shot("CHAR-FALL-" + side, true)
	await _until(func() -> bool: return _rudy.is_on_floor())
	Input.action_release(move)
	await _frames(30)
	await _shot("CHAR-IDLE-" + side, true)
	# The spikes: the hit (he turns toward it), then the defeat.
	hazards.process_mode = Node.PROCESS_MODE_INHERIT
	hazards.visible = true
	var spikes: Spikes = hazards.get_node("SpikesA")
	var look: Node2D = _rudy.get_node("Look")
	_rudy.global_position = Vector2(spikes.global_position.x - 220.0 * dir, 840.0)
	_main._snap_camera()
	await _frames(20)
	Input.action_press(move)
	await _until(func() -> bool: return _rudy.mode == Rudy.Mode.HURT)
	Input.action_release(move)
	await _until(func() -> bool: return look.modulate.a == 1.0) # between flashes
	await _shot("CHAR-HURT-" + side, true)
	await _until(func() -> bool: return _rudy.mode == Rudy.Mode.PLAY and not _rudy.is_invulnerable())
	_rudy.hearts = 1 # the next hit is the last heart
	_rudy.global_position = Vector2(spikes.global_position.x - 220.0 * dir, 840.0)
	_main._snap_camera()
	await _frames(2)
	Input.action_press(move)
	await _until(func() -> bool: return _rudy.mode == Rudy.Mode.DEFEATED)
	Input.action_release(move)
	await _frames(20)
	await _shot("CHAR-DEFEAT-" + side, true)
	await _until(func() -> bool: return _rudy.mode == Rudy.Mode.RESPAWNING)
	await _frames(28) # the fade-in is over
	if dir == 1:
		await _shot("CHAR-RESPAWN-" + side, true) # he always gets back up facing right
	await _until(func() -> bool: return _main.state == Main.State.PLAYING)
	hazards.process_mode = Node.PROCESS_MODE_DISABLED
	hazards.visible = false
	# The sword form: the pickup, its movement, its idle and the slash.
	_rudy.global_position = Vector2(pickup.global_position.x - 300.0 * dir, 840.0)
	_main._snap_camera()
	await _frames(20)
	Input.action_press(move)
	await _until(func() -> bool: return _rudy.gear == Rudy.Gear.SWORD)
	await _until(func() -> bool: return _rudy.pose == &"CHAR-SWORD-RUN-A")
	await _frames(2)
	await _shot("CHAR-SWORD-RUN-A-" + side, true)
	await _until(func() -> bool: return _rudy.pose == &"CHAR-SWORD-RUN-B")
	await _frames(2)
	await _shot("CHAR-SWORD-RUN-B-" + side, true)
	Input.action_press(&"jump")
	await _until(func() -> bool: return _rudy.pose == &"CHAR-SWORD-RISE")
	await _frames(10)
	await _shot("CHAR-SWORD-RISE-" + side, true)
	Input.action_release(&"jump")
	await _until(func() -> bool: return _rudy.pose == &"CHAR-SWORD-FALL")
	await _frames(8)
	await _shot("CHAR-SWORD-FALL-" + side, true)
	await _until(func() -> bool: return _rudy.is_on_floor())
	Input.action_release(move)
	await _frames(30)
	await _shot("CHAR-SWORD-IDLE-" + side, true)
	Input.action_press(&"slash")
	await _until(func() -> bool: return _rudy.pose == &"CHAR-SWORD-SLASH")
	Input.action_release(&"slash")
	await _frames(6)
	await _shot("CHAR-SWORD-SLASH-" + side, true)
	# On the teleport circle, run onto from either side.
	var portal: Portal = level.get_node("Portal")
	_rudy.global_position = Vector2(portal.global_position.x - 400.0 * dir, 840.0)
	_main._snap_camera()
	await _frames(20)
	Input.action_press(move)
	await _until(func() -> bool: return _main.state == Main.State.COMPLETE)
	Input.action_release(move)
	await _frames(40)
	await _shot("CHAR-CELEBRATE-" + side, true)


## A new level in place of the current one, in play.
func _fresh_main() -> void:
	_main.queue_free()
	await _frames(2)
	Main.title_shown = true
	_main = MAIN.instantiate()
	add_child(_main)
	_rudy = _main.get_node("Rudy")
	await _frames(30)


## One frame of step 3, logged before the frame's own processing: the sounds
## that started since the last frame, and the music's state and position.
func _log_mix() -> void:
	var started: Array[String] = []
	for id: StringName in Sfx.counts:
		for i in Sfx.counts[id] - _sounds_seen.get(id, 0):
			started.append(String(id))
		_sounds_seen[id] = Sfx.counts[id]
	_mix_log.frames.append(Engine.get_process_frames())
	_mix_log.music_db.append(snappedf(Music.volume_db(), 0.01))
	_mix_log.music_playing.append(Music.player().playing)
	_mix_log.music_muted.append(AudioServer.is_bus_mute(AudioServer.get_bus_index(Music.BUS)))
	_mix_log.sfx_muted.append(AudioServer.is_bus_mute(AudioServer.get_bus_index(Sfx.BUS)))
	_mix_log.paused.append(get_tree().paused)
	_mix_log.state.append(Main.State.keys()[_main.state])
	_mix_log.sounds.append(started)
	_mix_log.music_starts.append(Music.starts)
	_mix_log.music_pos.append(Music.player().get_playback_position()) # s of the loop mixed so far


## Main and SystemKeys read these keys in _process, so press one at the start of a process frame.
func _press_in_process(action: StringName) -> void:
	await get_tree().process_frame
	Input.action_press(action)
	await get_tree().process_frame
	await get_tree().process_frame
	Input.action_release(action)


func _out_dir() -> String:
	return ProjectSettings.globalize_path("res://").path_join("../evidence/%s" % _step).simplify_path()


## Saves the screen, or with `crop` only the CROP around Rudy.
func _shot(label: String, crop := false) -> void:
	await RenderingServer.frame_post_draw
	var image := get_viewport().get_texture().get_image()
	var rendered := image.get_size()
	if rendered != SIZE:
		image.resize(SIZE.x, SIZE.y, Image.INTERPOLATE_LANCZOS)
	if crop:
		var soles := Vector2i(_rudy.get_global_transform_with_canvas().origin.round())
		var corner := (soles - Vector2i(CROP.x / 2, 300)).clamp(Vector2i.ZERO, SIZE - CROP)
		image = image.get_region(Rect2i(corner, CROP))
	var suffix := "-collisions" if get_tree().debug_collisions_hint else ""
	var as_jpeg := not PNG_STEPS.has(_step) and (not crop or JPEG_CROP_STEPS.has(_step)) # a painted full screen is about 1.5 MB as PNG
	var path := _out_dir().path_join("%s-%s%s.%s" % [_step, label, suffix, "jpg" if as_jpeg else "png"])
	if as_jpeg:
		image.save_jpg(path, 0.9)
	else:
		image.save_png(path)
	print("saved %s (rendered at %d x %d, pose %s)" % [path.get_file(), rendered.x, rendered.y, _rudy.pose])


func _hold(action: StringName, ticks: int) -> void:
	Input.action_press(action)
	await _frames(ticks)
	Input.action_release(action)


func _until(condition: Callable) -> void:
	for i in 600:
		if condition.call():
			return
		await get_tree().physics_frame
	push_error("capture %s: a condition never came true" % _step)


func _frames(n: int) -> void:
	for i in n:
		await get_tree().physics_frame
