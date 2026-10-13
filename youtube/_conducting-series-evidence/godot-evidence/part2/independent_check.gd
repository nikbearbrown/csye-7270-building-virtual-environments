extends SceneTree
# Independent check, written by the evidence agent (not by the demo agent).
# Lives OUTSIDE the project folder. Loads res://pong.tscn, walks the whole
# instantiated tree, and checks the new Label plus every original node.

const EXPECTED_TEXT := "Hello from a text file"
const ORIGINAL_NODES := [
	".", "Background", "Left", "Left/Sprite2D", "Left/Collision",
	"Right", "Right/Sprite2D", "Right/Collision", "Ball", "Ball/Sprite2D",
	"Ball/Collision", "Separator", "LeftWall", "LeftWall/Collision",
	"RightWall", "RightWall/Collision", "Ceiling", "Ceiling/Collision",
	"Floor", "Floor/Collision", "Camera2D",
]

func _walk(n: Node, out: Array) -> void:
	out.append(n)
	for c in n.get_children():
		_walk(c, out)

func _initialize() -> void:
	var failures := 0
	var packed := load("res://pong.tscn") as PackedScene
	if packed == null:
		print("INDEPENDENT FAIL: res://pong.tscn did not load")
		quit(2)
		return
	var state := packed.get_state()
	print("PackedScene node_count: ", state.get_node_count())
	var root := packed.instantiate()
	var all: Array = []
	_walk(root, all)
	print("Instantiated nodes: ", all.size())
	for p in ORIGINAL_NODES:
		if root.get_node_or_null(p) == null:
			print("MISSING original node: ", p)
			failures += 1
	print("Original nodes present: ", ORIGINAL_NODES.size() - failures, "/", ORIGINAL_NODES.size())
	var labels: Array = []
	for n in all:
		if n is Label:
			labels.append(n)
			print("Label found: path=", root.get_path_to(n), " class=", n.get_class(), " parent=", n.get_parent().name, " text=\"", n.text, "\"")
	if labels.size() != 1:
		print("Expected exactly 1 Label, found ", labels.size())
		failures += 1
	elif labels[0].text != EXPECTED_TEXT or labels[0].get_parent() != root:
		print("Label text or parent wrong")
		failures += 1
	# Scripts on the original nodes still attached?
	for p in ["Left", "Right", "Ball", "LeftWall", "RightWall", "Ceiling", "Floor"]:
		var s = root.get_node(p).get_script()
		print("script on ", p, ": ", s.resource_path if s else "NONE")
		if s == null:
			failures += 1
	print("Signal connections on Left: ", root.get_node("Left").get_signal_connection_list("area_entered").size())
	root.free()
	print("INDEPENDENT RESULT: ", "PASS" if failures == 0 else "FAIL (%d)" % failures)
	quit(0 if failures == 0 else 1)
