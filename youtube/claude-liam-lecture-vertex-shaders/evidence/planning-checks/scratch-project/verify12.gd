extends SceneTree
# Check 12: the GDScript card of beat B15 (the quad-mesh recipe) runs exactly as shown, inside a node's _ready(), and gives 25 vertices.
#   var mesh := QuadMesh.new()
#   mesh.size = Vector2(320, 320)
#   mesh.subdivide_width = 3
#   mesh.subdivide_depth = 3
#   $Quad.mesh = mesh
# The node tree: a Node2D (script below) with a child MeshInstance2D named Quad. Expected: vertices 25, triangles 32.
const V = preload("res://vscene.gd")
const SRC := "extends Node2D\nfunc _ready():\n\tvar mesh := QuadMesh.new()\n\tmesh.size = Vector2(320, 320)\n\tmesh.subdivide_width = 3\n\tmesh.subdivide_depth = 3\n\t$Quad.mesh = mesh\n"

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	V.setup(root, 640, 360)
	var holder := Node2D.new()
	var s := GDScript.new()
	s.source_code = SRC
	var err := s.reload()
	holder.set_script(s)
	var quad := MeshInstance2D.new()
	quad.name = "Quad"
	quad.position = Vector2(320, 180)
	holder.add_child(quad)
	root.add_child(holder)
	await V.frames(self, 3)
	var arr := quad.mesh.surface_get_arrays(0)
	V.out("12-b15-recipe-as-shown", {"script_reload_error": err, "vertices": arr[Mesh.ARRAY_VERTEX].size(), "triangles": arr[Mesh.ARRAY_INDEX].size() / 3,
		"size": [(quad.mesh as QuadMesh).size.x, (quad.mesh as QuadMesh).size.y], "subdivide_width": (quad.mesh as QuadMesh).subdivide_width, "subdivide_depth": (quad.mesh as QuadMesh).subdivide_depth})
	quit(0)
