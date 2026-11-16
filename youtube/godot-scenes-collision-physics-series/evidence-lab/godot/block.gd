extends StaticBody2D
@export var contents: PackedScene
var used := false
func bump() -> void:
    if used:
        return
    used = true
    if contents:
        var item := contents.instantiate() as Node2D
        item.position = position + Vector2(0, -32)
        add_sibling.call_deferred(item)
    # Animate a visual child for a cosmetic bump. A moving solid needs AnimatableBody2D.
