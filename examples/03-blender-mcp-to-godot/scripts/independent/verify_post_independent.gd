extends SceneTree
## Independent check (not written by the agent). Reads the placement from
## game.tscn instead of a hard-coded constant, finds the floor with a ray that
## EXCLUDES the post's own collider, and measures how much of the pennant sits
## inside the convex collider. Run with --fixed-fps 60.
var frames := 0
var game: Node

func _initialize() -> void:
	call_deferred("start")

func start() -> void:
	game = (load("res://game.tscn") as PackedScene).instantiate()
	root.add_child(game)
	physics_frame.connect(tick)

func find_post(n: Node) -> Node3D:
	if n.scene_file_path == "res://props/checkpoint_post.glb":
		return n as Node3D
	for c in n.get_children():
		var r := find_post(c)
		if r: return r
	return null

func tick() -> void:
	frames += 1
	if frames < 10: return
	physics_frame.disconnect(tick)
	var post := find_post(game)
	print("post node: ", post.name, " global origin ", post.global_transform.origin)
	var body: StaticBody3D = post.find_children("*", "StaticBody3D", true, false)[0]
	var space := root.get_world_3d().direct_space_state
	var o := post.global_transform.origin
	for offset in [Vector3.ZERO, Vector3(0.45, 0, 0), Vector3(-1.0, 0, 0), Vector3(0, 0, 1.0)]:
		var q := PhysicsRayQueryParameters3D.create(o + offset + Vector3(0, 0.5, 0), o + offset + Vector3(0, -3, 0))
		q.exclude = [body.get_rid()]
		var hit := space.intersect_ray(q)
		if hit.is_empty():
			print("offset ", offset, ": no floor hit within 3 m below")
		else:
			print("offset ", offset, ": floor y ", snappedf(hit.position.y, 0.0001), "; post base y ", snappedf(o.y, 0.0001), "; gap ", snappedf(o.y - hit.position.y, 0.0001), " m; hit ", hit.collider.name)
	# Collider versus pennant
	var shape := (body.get_child(0) as CollisionShape3D).shape as ConvexPolygonShape3D
	var cmin := Vector3(INF, INF, INF); var cmax := -cmin
	for p in shape.points:
		cmin = cmin.min(p); cmax = cmax.max(p)
	var pen: MeshInstance3D = post.find_child("Pennant", true, false)
	var pa := pen.get_aabb()
	var overlap_x := maxf(0.0, minf(cmax.x, pa.end.x) - maxf(cmin.x, pa.position.x))
	print("collider box ", cmin, " .. ", cmax)
	print("pennant AABB x ", snappedf(pa.position.x, 0.001), "..", snappedf(pa.end.x, 0.001), " y ", snappedf(pa.position.y, 0.001), "..", snappedf(pa.end.y, 0.001))
	print("pennant x-range inside the collider's bounding box (not its surface): ", snappedf(overlap_x, 0.001), " of ", snappedf(pa.size.x, 0.001), " m")
	# Sample the pennant quad (post-local x 0.08..0.48, y 1.55..1.80, z 0) on a
	# 1 cm grid and ask the physics server which samples lie inside the post's collider.
	var inside := 0; var total := 0; var max_x_inside := -1.0
	for i in range(41):
		for j in range(26):
			var local := Vector3(0.08 + 0.01 * i, 1.55 + 0.01 * j, 0.0)
			var pq := PhysicsPointQueryParameters3D.new()
			pq.position = post.global_transform * local
			var hits := space.intersect_point(pq)
			total += 1
			for h in hits:
				if h.collider == body:
					inside += 1; max_x_inside = maxf(max_x_inside, local.x); break
	print("pennant samples inside collider: ", inside, " of ", total, "; furthest inside at local x = ", snappedf(max_x_inside, 0.001))
	var col_vol := (cmax - cmin).x * (cmax - cmin).y * (cmax - cmin).z
	print("collider volume ", snappedf(col_vol, 0.0001), " m^3")
	# Player capsule read from the scene, not a constant
	var player: Node = (load("res://player/player.tscn") as PackedScene).instantiate()
	var cap := (player.find_child("CollisionCapsule", true, false) as CollisionShape3D).shape as CapsuleShape3D
	print("player capsule height ", cap.height, " radius ", cap.radius)
	player.free()
	game.free()
	quit()
