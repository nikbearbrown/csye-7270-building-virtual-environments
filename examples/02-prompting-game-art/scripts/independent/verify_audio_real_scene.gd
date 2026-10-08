extends SceneTree
## Independent check (not written by the agent). Loads the REAL main scene
## (res://game/main.tscn, where the agent wired AudioCues) and drives Clawd only
## through the player's existing test inputs: hold right, press jump at x marks.
## It never writes position, velocity or state. It skips the jump mark at x=292
## so Clawd walks into the spikes at x=320..344. Logs the physics frame of each
## gameplay event and of each cue. Run with --fixed-fps 60.
var game: Node
var cues: Node
var frame := 0
var last_jumps := 0
var last_state := -1
var last_jp := 0
var last_fp := 0
var events: Array[String] = []
var marks: Array[float] = [138.0]   # one jump before the spikes, then none

func _initialize() -> void:
	call_deferred("start")

func start() -> void:
	game = (load("res://game/main.tscn") as PackedScene).instantiate()
	game.test_mode = true
	root.add_child(game)
	cues = game.get_node_or_null("AudioCues")
	print("AudioCues in main.tscn: ", cues != null)
	game.start_session()
	physics_frame.connect(tick)

func tick() -> void:
	frame += 1
	var p = game.player
	p.test_control = true
	p.test_axis = 1.0
	p.test_jump_held = false
	if not marks.is_empty() and p.position.x >= marks[0] and p.is_on_floor():
		p.test_jump_pressed = true
		marks.pop_front()
	if p.jumps != last_jumps:
		if p.jumps > last_jumps: events.append("frame %d: player.jumps -> %d" % [frame, p.jumps])
		last_jumps = p.jumps
	if game.state != last_state:
		events.append("frame %d: state -> %s" % [frame, ["MENU","PLAYING","PAUSED","DYING","COMPLETE"][game.state]])
		last_state = game.state
	if cues.jump_plays != last_jp:
		events.append("frame %d: jump cue #%d" % [frame, cues.jump_plays]); last_jp = cues.jump_plays
	if cues.fail_plays != last_fp:
		events.append("frame %d: fail cue #%d" % [frame, cues.fail_plays]); last_fp = cues.fail_plays
	if frame >= 240:
		physics_frame.disconnect(tick)
		for e in events: print(e)
		print("deaths=", game.deaths, " jump_plays=", cues.jump_plays, " fail_plays=", cues.fail_plays, " music_plays=", cues.music_plays)
		game.free()
		quit()
