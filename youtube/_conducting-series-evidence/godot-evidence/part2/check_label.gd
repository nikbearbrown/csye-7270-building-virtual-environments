extends SceneTree

const EXPECTED := "Hello from a text file"

func _initialize() -> void:
	var packed: PackedScene = load("res://pong.tscn")
	if packed == null:
		print("FAIL: could not load res://pong.tscn")
		quit(1)
		return
	var root: Node = packed.instantiate()
	if root == null:
		print("FAIL: could not instantiate res://pong.tscn")
		quit(1)
		return
	var label: Label = root.get_node_or_null("HelloLabel") as Label
	if label == null:
		print("FAIL: HelloLabel node not found (or not a Label)")
		root.free()
		quit(1)
		return
	print("HelloLabel text: ", label.text)
	var ok: bool = label.text == EXPECTED
	print("PASS" if ok else "FAIL: text mismatch")
	root.free()
	quit(0 if ok else 1)
