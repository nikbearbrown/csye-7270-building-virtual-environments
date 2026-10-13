extends SceneTree
# Check 10: the one-line vertex count shown in the film's last beat, run exactly as written inside a node's _ready().
#   print($Flag.mesh.surface_get_arrays(0)[Mesh.ARRAY_VERTEX].size())
# The scene has a MeshInstance2D named Flag with a QuadMesh cut 31 x 7. Expected output: 297.
const V = preload("res://vscene.gd")
const SRC := "extends Node2D\nfunc _ready():\n\tprint($Flag.mesh.surface_get_arrays(0)[Mesh.ARRAY_VERTEX].size())\n"

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	V.setup(root, 640, 360)
	var holder := Node2D.new()
	var s := GDScript.new()
	s.source_code = SRC
	s.reload()
	holder.set_script(s)
	var flag := V.quad(Vector2(384, 168), 31, 7, V.checker_image(384, 168, 24), Vector2(320, 180))
	flag.name = "Flag"
	holder.add_child(flag)
	print("--- output of the line, run in _ready() ---")
	root.add_child(holder)
	await V.frames(self, 2)
	print("--- end ---")
	quit(0)
