extends Node2D
# Node-based baseline for benchmarking against bullets.gd.
# One Area2D + CollisionShape2D + Sprite2D per bullet; one manager script moves them.
# Matches bullets.gd: radius 8, same speed range, same spawn/wrap rules,
# collision_layer=1 / collision_mask=0.

const SPEED_MIN := 20
const SPEED_MAX := 80

const bullet_image := preload("res://bullet.png")

## Set before the node enters the tree to override the default count.
var bullet_count: int = 500

var bullets: Array = []


class BulletData:
	var node: Area2D
	var speed: float
	var position: Vector2:
		get:
			return node.position
		set(v):
			node.position = v


func _ready() -> void:
	var circle := CircleShape2D.new()
	circle.radius = 8.0
	var vp := get_viewport_rect()

	for _i in bullet_count:
		var data := BulletData.new()
		data.speed = randf_range(SPEED_MIN, SPEED_MAX)

		var area := Area2D.new()
		area.monitoring = false
		area.monitorable = true
		area.collision_layer = 1
		area.collision_mask = 0

		var col := CollisionShape2D.new()
		col.shape = circle
		area.add_child(col)

		var spr := Sprite2D.new()
		spr.texture = bullet_image
		area.add_child(spr)

		area.position = Vector2(
			randf_range(0, vp.size.x) + vp.size.x,
			randf_range(0, vp.size.y)
		)
		data.node = area
		add_child(area)
		bullets.push_back(data)


func _physics_process(delta: float) -> void:
	var offset := get_viewport_rect().size.x + 16.0
	for data: BulletData in bullets:
		var pos := data.node.position
		pos.x -= data.speed * delta
		if pos.x < -16.0:
			pos.x = offset
		data.node.position = pos
