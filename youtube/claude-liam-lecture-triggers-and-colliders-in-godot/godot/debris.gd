extends Node2D
func shatter(at: Vector2) -> void:
    spawn.call_deferred(at)
func spawn(at: Vector2) -> void:
    for direction in [Vector2(-1,-2), Vector2(1,-2), Vector2(-1,-1), Vector2(1,-1)]:
        var piece := RigidBody2D.new()
        piece.position = at
        piece.collision_layer = Layers.bit(Layers.DEBRIS)
        piece.collision_mask = Layers.bit(Layers.WORLD)
        var collider := CollisionShape2D.new()
        var box := RectangleShape2D.new()
        box.size = Vector2(8,8)
        collider.shape = box
        piece.add_child(collider)
        add_child(piece)
        piece.apply_central_impulse(direction * 120.0)
        get_tree().create_timer(3.0).timeout.connect(piece.queue_free)
