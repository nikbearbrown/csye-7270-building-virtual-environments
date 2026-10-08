extends SceneTree
## Chapter-author correction for Lab B's last check. The agent's test_pcg.gd
## wrote a hand-built flat row into Ground instead of a generated level. This
## writes every validator-accepted level (seeds 1..200, width 40) into Ground,
## one at a time, drops the player above its first solid column, and checks the
## player comes to rest on a tile at that column's height.
const TILE := 16.0
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	var gen = load("res://pcg/level_generator.gd").new()
	var val = load("res://pcg/level_validator.gd").new()
	var accepted := 0
	var landed := 0
	for s in range(1, 201):
		var level: Array = gen.generate(s, 40)
		if not val.validate(level).is_empty():
			continue
		accepted += 1
		var world: Node = load("res://world.tscn").instantiate()
		root.add_child(world)
		var ground: TileMapLayer = world.get_node("Ground")
		ground.clear()
		world.get_node("Secret").clear()
		var first := 0
		while int(level[first]) == -1:
			first += 1
		for c in level.size():
			if int(level[c]) != -1:
				ground.set_cell(Vector2i(c, int(level[c])), 0, Vector2i(0, 0))
		var player: CharacterBody2D = world.get_node("Player")
		player.position = Vector2(first * TILE + TILE / 2, int(level[first]) * TILE - 40)
		player.velocity = Vector2.ZERO
		for i in 120:
			await physics_frame
		var expected_y: float = int(level[first]) * TILE - 7.0
		var ok := player.is_on_floor() and absf(player.position.y - expected_y) < 2.0
		if ok:
			landed += 1
		else:
			print("seed ", s, " did not land as expected: on_floor=", player.is_on_floor(), " y=", player.position.y, " expected~", expected_y)
		world.queue_free()
		await process_frame
	print("RESULT accepted=", accepted, " landed_on_first_column=", landed)
	quit(0 if landed == accepted else 1)
