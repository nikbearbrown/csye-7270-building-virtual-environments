class_name Fireball
extends Area2D
## Flies in a straight line from the staff crystal toward the aim point. Destroyed by walls and
## ground (world layer) with a short burst; enemies are hit through `hit_enemy` (S4).

const SPEED := 260.0
const LIFETIME := 2.0
const DAMAGE := 1
const BURST := preload("res://features/fireball/burst.tscn")

var direction := Vector2.RIGHT
var _age := 0.0
var _spent := false


func _ready() -> void:
	collision_layer = 1 << 3            # player_attack
	collision_mask = (1 << 0) | (1 << 2)  # world, enemy
	rotation = direction.angle()        # the art points right
	body_entered.connect(_on_body_entered)


func _physics_process(delta: float) -> void:
	position += direction * SPEED * delta
	_age += delta
	if _age > LIFETIME:
		queue_free()


func _on_body_entered(body: Node) -> void:
	if body.has_method("take_damage"):
		body.take_damage(DAMAGE)
	explode()


## Burst at the current position, then remove. Safe to call twice in one frame.
func explode() -> void:
	if _spent:
		return
	_spent = true
	var burst := BURST.instantiate()
	burst.global_position = global_position
	get_parent().add_child(burst)
	set_deferred("monitoring", false)
	queue_free()
