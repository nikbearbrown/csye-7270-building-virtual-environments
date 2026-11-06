extends Node2D
## Windowed GPU price scene for the two effects (CHANGE-BRIEF "Price predictions and budget": GPU time in the Visual
## Profiler, Debugger panel). Over the real cave background and ground at in-game scale (640x360 view, 2x on a
## 1280x720 window). The load is previews/effect_load.gd, the same driver tests/cost_effects.gd prices headless.
## Keys (none of them is used by game/controls.gd):
##   1  both effects off
##   2  Effect A at its bound: 6 impacts alive, each replaced as it frees itself
##   3  Effect B at its heaviest: 6 flying full trails, about 6 detached fading trails, 6 refilling (an upper bound)
##   F8 toggle vsync for this window (DisplayServer.window_set_vsync_mode); project settings are not changed
## Optional user argument to start in a case: -- --case=2
## From fall-2026/zhefan-z/assignment-6/, windowed:
##   Godot_v4.7.2-stable_win64.exe --path walker-magic-zhefan --resolution 1280x720 res://previews/gpu_price.tscn

const LOAD := preload("res://previews/effect_load.gd")
const NAMES := {
	LOAD.Mode.OFF: "1  both effects off",
	LOAD.Mode.A: "2  Effect A: 6 impacts alive",
	LOAD.Mode.B: "3  Effect B: 6 flying + 6 fading (+6 refilling)",
}

@onready var load_driver: Node = $Load
@onready var label: Label = $UI/Info


func _ready() -> void:
	load_driver.target = $Effects
	var start := LOAD.Mode.OFF
	for arg: String in OS.get_cmdline_user_args():
		if arg.begins_with("--case="):
			start = clampi(int(arg.trim_prefix("--case=")) - 1, 0, 2) as LOAD.Mode
	set_case(start)


func set_case(m: LOAD.Mode) -> void:
	load_driver.set_mode(m)
	print(JSON.stringify({"gpu_price": "case", "case": NAMES[m]}))


func _unhandled_input(event: InputEvent) -> void:
	var key := event as InputEventKey
	if key == null or not key.pressed or key.echo:
		return
	match key.physical_keycode:
		KEY_1:
			set_case(LOAD.Mode.OFF)
		KEY_2:
			set_case(LOAD.Mode.A)
		KEY_3:
			set_case(LOAD.Mode.B)
		KEY_F8:
			var off := DisplayServer.window_get_vsync_mode() == DisplayServer.VSYNC_DISABLED
			DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_ENABLED if off else DisplayServer.VSYNC_DISABLED)
		_:
			return
	get_viewport().set_input_as_handled()


func _process(_delta: float) -> void:
	var vsync := DisplayServer.window_get_vsync_mode() != DisplayServer.VSYNC_DISABLED
	var c: Dictionary = load_driver.counts()
	label.text = "Case %s\nFPS %d  (%.2f ms)   vsync %s\nimpacts %d   trails: flying %d, refilling %d, fading %d\n1 off   2 Effect A   3 Effect B   F8 vsync" % [
		NAMES[load_driver.mode], Engine.get_frames_per_second(), 1000.0 / maxf(Engine.get_frames_per_second(), 1.0),
		"on" if vsync else "off", c.impacts, c.flying_trails, c.refilling_trails, c.detached_trails]


func _exit_tree() -> void:
	print(JSON.stringify({"gpu_price": "exit", "case": NAMES[load_driver.mode], "counts": load_driver.counts(),
		"fps": Engine.get_frames_per_second()}))
