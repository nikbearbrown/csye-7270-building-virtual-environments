class_name Controls
## Input actions for the slice, defined in code so the scene and the headless tests share one map.

const MAP := {
	"move_left": [KEY_A, KEY_LEFT],
	"move_right": [KEY_D, KEY_RIGHT],
	"jump": [KEY_SPACE, KEY_W, KEY_UP],
	"pause": [KEY_ESCAPE],
	"mute_music": [KEY_M],
	"mute_sfx": [KEY_N],
	"restart": [KEY_R],
}


static func ensure() -> void:
	for action: String in MAP:
		if InputMap.has_action(action):
			continue
		InputMap.add_action(action)
		for key: Key in MAP[action]:
			var ev := InputEventKey.new()
			ev.physical_keycode = key
			InputMap.action_add_event(action, ev)
	if not InputMap.has_action("cast"):
		InputMap.add_action("cast")
		var click := InputEventMouseButton.new()
		click.button_index = MOUSE_BUTTON_LEFT
		InputMap.action_add_event("cast", click)
