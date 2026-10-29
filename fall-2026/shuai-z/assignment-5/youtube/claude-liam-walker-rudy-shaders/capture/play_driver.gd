extends Node
## Film-only autoload, added to an isolated copy of game/ (never to the project
## itself). The real main scene, res://app/main.tscn, boots as F5 runs it; this
## node presses the same input actions a player would, through
## Input.action_press(), the way game/tests/invulnerable_tint_checks.gd does.
## It never calls take_hit(), respawn_at() or set_shader_parameter(), and
## assigns nothing in the game. Each frame it prints what the hearts' material
## holds, so the film can say which value each frame shows.
##
## Take: the title; Enter; move_right into the first spikes (hit 1); back onto
## the spikes inside the window, which is ignored; step off; the window runs
## out; a second hit; the window runs out; the last heart, and the respawn's
## window; quit. Waits are in physics ticks (60 a second).

var _main: Node
var _rudy: Node
var _material: ShaderMaterial
var _frame := 0


func _ready() -> void:
	process_priority = 1000 # print after every other _process(), as the test's sampler does
	await get_tree().process_frame
	_main = get_tree().current_scene
	_rudy = _main.get_node("Rudy")
	_material = (_main.get_node("Hud/Hearts") as Control).material as ShaderMaterial
	_play()


func _process(_delta: float) -> void:
	if _material == null:
		return
	var value: Variant = _material.get_shader_parameter(&"tint_amount")
	print("frame %d tint_amount %.6f hearts %d invulnerable %s mode %d" % [
		_frame, 0.0 if value == null else float(value), _rudy.hearts, _rudy.is_invulnerable(), _rudy.mode])
	_frame += 1


func _play() -> void:
	await _frames(90)
	print("step: Enter on the title")
	await _tap(&"restart")
	await _frames(90)
	print("step: move_right into the first spikes")
	await _hold_until(&"move_right", func() -> bool: return _rudy.hearts < 3, 600)
	await _wait_until(func() -> bool: return _rudy.mode == Rudy.Mode.PLAY and _rudy.is_on_floor(), 120)
	print("step: move_right back onto the spikes inside the window")
	var spikes: Area2D = _main.get_node("Level1/Hazards/SpikesA")
	await _hold_until(&"move_right", func() -> bool: return spikes.overlaps_body(_rudy), 120)
	print("step: move_left off the spikes")
	await _hold_until(&"move_left", func() -> bool: return not spikes.overlaps_body(_rudy), 120)
	await _hold(&"move_left", 6)
	await _wait_until(func() -> bool: return not _rudy.is_invulnerable(), 120)
	print("step: the window has run out")
	await _frames(90)
	print("step: move_right into the spikes again (hit 2)")
	await _hold_until(&"move_right", func() -> bool: return _rudy.hearts < 2, 600)
	await _wait_until(func() -> bool: return not _rudy.is_invulnerable(), 120)
	print("step: the window has run out")
	await _frames(90)
	print("step: move_right into the spikes, the last heart (hit 3)")
	await _hold_until(&"move_right", func() -> bool: return _rudy.hearts < 1, 600)
	await _wait_until(func() -> bool: return _rudy.mode == Rudy.Mode.RESPAWNING, 300)
	print("step: the respawn")
	await _wait_until(func() -> bool: return _rudy.mode == Rudy.Mode.PLAY and not _rudy.is_invulnerable(), 300)
	print("step: the respawn's window has run out")
	await _frames(90)
	get_tree().quit()


func _frames(n: int) -> void:
	for i in n:
		await get_tree().physics_frame


func _wait_until(condition: Callable, max_ticks: int) -> void:
	for i in max_ticks:
		if condition.call():
			return
		await get_tree().physics_frame


func _hold_until(action: StringName, condition: Callable, max_ticks: int) -> void:
	Input.action_press(action)
	await _wait_until(condition, max_ticks)
	Input.action_release(action)


func _hold(action: StringName, ticks: int) -> void:
	Input.action_press(action)
	await _frames(ticks)
	Input.action_release(action)


func _tap(action: StringName) -> void:
	Input.action_press(action)
	await _frames(2)
	Input.action_release(action)
