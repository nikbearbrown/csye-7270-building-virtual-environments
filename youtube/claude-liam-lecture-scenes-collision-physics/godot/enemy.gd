extends CharacterBody2D
signal defeated
var dead := false
func _ready() -> void:
    $Top.body_entered.connect(on_top)
    $Side.body_entered.connect(on_side)
func on_top(body: Node2D) -> void:
    if dead or not body is CharacterBody2D or body.velocity.y <= 0:
        return
    dead = true
    if body.has_method("bounce"):
        body.bounce()
    $Top.set_deferred("monitoring", false)
    $Side.set_deferred("monitoring", false)
    set_deferred("collision_layer", 0)
    defeated.emit()
func on_side(body: Node2D) -> void:
    if not dead and body.has_method("take_hit"):
        body.take_hit()
# Deliberately minimal: define priority for simultaneous side/top contacts in a game.
