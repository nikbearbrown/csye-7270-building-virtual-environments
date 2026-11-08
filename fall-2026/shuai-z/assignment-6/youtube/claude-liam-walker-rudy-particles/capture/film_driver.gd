extends Node
## Film-only autoload, added to an isolated copy of game/ (never to the project
## itself). The real main scene, res://app/main.tscn, boots as F5 runs it; this
## node presses the same input actions a player would, through
## Input.action_press(), the way the game's state tests do. It never calls the
## effects driver, never starts, stops or moves an emitter, and assigns nothing
## in the game. Each drawn frame it prints the state the film needs to label
## what that frame shows: Rudy's place and mode, whether the sword's hitbox is
## live, how many SlashSparks bursts are alive, whether RunDust is emitting,
## and whether the tree is paused.
##
## Take: the title; Enter; run right (the dust starts); jump the first spikes
## (the dust stops in the air and starts again on landing); jump over the first
## goblin; walk into the sword; stop; one cut; five cuts as fast as the game
## allows (two bursts alive at once); turn and cut facing left, twice;
## run left, pause while running (the dust holds still), resume, stop; turn right,
## jump and cut at the top of the jump (sparks against the sky); wait for the
## second goblin to walk towards him and cut it (it hides while its sparks are
## still alive); cut and pause at once (the sparks hold still), resume; quit.
## Waits are in physics
## ticks (60 a second).

var _main: Node
var _rudy: Node
var _bursts: Node
var _dust: GPUParticles2D
var _goblin_a: Node2D
var _goblin_b: Node2D
var _sword_box: CollisionShape2D
var _frame := 0


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS # keeps logging, and can resume, while the tree is paused
	process_priority = 1000 # print after every other _process()
	await get_tree().process_frame
	_main = get_tree().current_scene
	_rudy = _main.get_node("Rudy")
	_bursts = _main.get_node("Effects/SlashBursts")
	_dust = _main.get_node("DustTrail/RunDust")
	_goblin_a = _main.get_node("Level1/Enemies/GoblinA")
	_goblin_b = _main.get_node("Level1/Enemies/GoblinB")
	_sword_box = _rudy.get_node("SwordHitbox/Shape")
	_play()


func _process(_delta: float) -> void:
	if _rudy == null:
		return
	print("frame %d drawn %d x %.1f y %.1f mode %d facing %d floor %s vx %.0f gear %d live %s bursts %d dust %s paused %s hearts %d gB %.0f deadB %s visB %s" % [
		_frame, Engine.get_frames_drawn(), _rudy.global_position.x, _rudy.global_position.y, _rudy.mode,
		_rudy.facing, _rudy.is_on_floor(), _rudy.velocity.x, _rudy.gear, not _sword_box.disabled,
		_bursts.get_child_count(), _dust.emitting, get_tree().paused, _rudy.hearts,
		_goblin_b.global_position.x, _goblin_b.dead, _goblin_b.visible])
	_frame += 1


func _play() -> void:
	await _ticks(60)
	print("step: Enter on the title")
	await _tap(&"restart")
	await _ticks(60)
	print("step: run right")
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _rudy.global_position.x >= 930.0, 300)
	print("step: jump the first spikes")
	await _tap(&"jump")
	await _until(func() -> bool: return _rudy.is_on_floor() and _rudy.global_position.x > 1150.0, 120)
	print("step: landed; on towards the first goblin")
	await _until(func() -> bool: return _goblin_a.global_position.x - _rudy.global_position.x < 190.0, 300)
	print("step: jump over the first goblin")
	await _tap(&"jump")
	await _until(func() -> bool: return _rudy.is_on_floor() and _rudy.global_position.x > _goblin_a.global_position.x + 60.0, 120)
	print("step: landed; on to the sword")
	await _until(func() -> bool: return _rudy.gear != 0, 400)
	print("step: the sword")
	await _until(func() -> bool: return _rudy.global_position.x >= 2620.0, 60)
	Input.action_release(&"move_right")
	print("step: stop")
	await _ticks(50)
	print("step: one cut")
	await _tap(&"slash")
	await _ticks(50)
	print("step: five cuts as fast as the game allows")
	for i in 5:
		await _tap(&"slash")
		await _ticks(18)
	await _ticks(40)
	print("step: turn left and cut twice")
	await _hold(&"move_left", 4)
	await _ticks(12)
	for i in 2:
		await _tap(&"slash")
		await _ticks(18)
	await _ticks(40)
	print("step: run left (still facing left)")
	Input.action_press(&"move_left")
	await _ticks(40)
	print("step: pause while running")
	await _tap(&"pause")
	await _ticks(70)
	print("step: resume")
	await _tap(&"pause")
	await _ticks(12)
	Input.action_release(&"move_left")
	print("step: stop")
	await _ticks(40)
	print("step: turn right, run, jump and cut at the top of the jump")
	await _hold(&"move_right", 4)
	await _ticks(10)
	Input.action_press(&"move_right")
	await _ticks(20)
	await _tap(&"jump")
	await _ticks(20)
	await _tap(&"slash")
	await _until(func() -> bool: return _rudy.is_on_floor(), 120)
	Input.action_release(&"move_right")
	print("step: landed")
	await _ticks(40)
	print("step: wait until the second goblin walks towards him")
	await _until(func() -> bool: return _goblin_b.facing == -1 and _goblin_b.global_position.x - _rudy.global_position.x < 650.0, 400)
	print("step: walk to the second goblin")
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _goblin_b.global_position.x - _rudy.global_position.x < 170.0, 300)
	Input.action_release(&"move_right")
	print("step: wait for the goblin to come within reach")
	await _until(func() -> bool: return _goblin_b.global_position.x - _rudy.global_position.x < 92.0, 300)
	print("step: cut the second goblin")
	await _tap(&"slash")
	await _ticks(60)
	print("step: cut, then pause at once")
	await _tap(&"slash")
	await _ticks(8)
	await _tap(&"pause")
	print("step: paused")
	await _ticks(70)
	print("step: resume")
	await _tap(&"pause")
	await _ticks(60)
	print("step: quit")
	get_tree().quit()


func _ticks(n: int) -> void:
	for i in n:
		await get_tree().physics_frame


func _until(condition: Callable, max_ticks: int) -> void:
	for i in max_ticks:
		if condition.call():
			return
		await get_tree().physics_frame
	print("step: TIMED OUT")


func _hold(action: StringName, ticks: int) -> void:
	Input.action_press(action)
	await _ticks(ticks)
	Input.action_release(action)


func _tap(action: StringName) -> void:
	Input.action_press(action)
	await _ticks(2)
	Input.action_release(action)
