extends RefCounted
static func cell_at(tiles: TileMapLayer, point: Vector2, normal: Vector2) -> Vector2i:
    # Two pixels is a lab-specific probe distance; tune for tile size and transforms.
    var probe := point - normal * 2.0
    return tiles.local_to_map(tiles.to_local(probe))
