class_name Fireball
extends Area2D
## Flies in a straight line from the staff crystal toward the aim point. Destroyed by walls and
## ground (world layer) with a short burst; enemies are hit through `hit_enemy` (S4).

const SPEED := 260.0
const LIFETIME := 2.0
const DAMAGE := 1
const BURST := preload("res://features/fireball/burst.tscn")
const IMPACT := preload("res://effects/fireball_impact.tscn")   # A6 Effect A; frees itself after 0.9 s

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
		_release_trail()
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
	var impact := IMPACT.instantiate()   # one new instance per impact, so impacts overlap (CHANGE-BRIEF A4)
	impact.global_position = global_position
	get_parent().add_child(impact)
	_release_trail()
	set_deferred("monitoring", false)
	queue_free()


## A6 Effect B (CHANGE-BRIEF B2): the trail moves to this fireball's parent with its global transform kept, so its
## particles stay where they were drawn, stops emitting and is freed after its particles' lifetime (read from the
## effect scene, never set here). The timer is pausable, so a paused game holds the fading trail.
func _release_trail() -> void:
	var trail := get_node_or_null("FireballTrail") as GPUParticles2D
	if trail == null:
		return
	trail.reparent(get_parent(), true)
	trail.emitting = false
	get_tree().create_timer(trail.lifetime, false).timeout.connect(trail.queue_free)
