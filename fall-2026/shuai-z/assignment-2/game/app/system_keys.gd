class_name SystemKeys
extends Node
## The keys that work even while the game is paused, read by this node because
## the level itself stops then (CHANGE-BRIEF.md, music behavior):
## - Esc asks the level to pause or resume play (Main.toggle_pause);
## - M mutes or unmutes the Music bus, and N the SFX bus. These are bus mutes:
##   nothing in the game reads them, and they last until the game closes.
## It reads the keys' state each frame, as Main reads Enter, so the checks can
## press them with Input.action_press.

@onready var _main: Main = get_parent()


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS


func _process(_delta: float) -> void:
	if Input.is_action_just_pressed(&"pause"):
		_main.toggle_pause()
	if Input.is_action_just_pressed(&"mute_music"):
		toggle_mute(Music.BUS)
	if Input.is_action_just_pressed(&"mute_sfx"):
		toggle_mute(Sfx.BUS)


static func toggle_mute(bus_name: StringName) -> void:
	var bus := AudioServer.get_bus_index(bus_name)
	AudioServer.set_bus_mute(bus, not AudioServer.is_bus_mute(bus))
