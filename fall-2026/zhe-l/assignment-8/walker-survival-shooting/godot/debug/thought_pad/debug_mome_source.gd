extends Node

const CLIPBOARD_EMPTY := "empty"
const CLIPBOARD_TEXT := "text"
const TEST_DOCUMENTS := {
	1: {
		"name": "Introduction",
		"extension": ".mome",
		"content": "Here I cast aside my dignity.",
		"read_only": true,
	},
	2: {
		"name": "My Notes",
		"extension": ".mome",
		"content": "This is a memo you can edit.\nTry typing and selecting text here.",
		"read_only": false,
	},
}

var _clipboard: Dictionary = {"kind": CLIPBOARD_EMPTY}

func get_document(_device_uid: int, file_uid: int) -> Dictionary:
	return TEST_DOCUMENTS[file_uid].duplicate()


func set_clipboard_text(_device_uid: int, text: String) -> bool:
	_clipboard = {"kind": CLIPBOARD_TEXT, "text": text}
	return true


func get_clipboard(_device_uid: int) -> Dictionary:
	return _clipboard.duplicate()
