class_name Layers
extends RefCounted
const WORLD := 1
const ONE_WAY := 2
const PLAYER := 3
const ENEMY := 4
const PICKUP := 5
const HAZARD := 6
const DEBRIS := 7
static func bit(layer: int) -> int:
    assert(layer >= 1 and layer <= 32)
    return 1 << (layer - 1)
