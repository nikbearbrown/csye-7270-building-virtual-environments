extends SubViewport
# Harness shim, not game code (same as Signal Garden's): scripts written for the root Window may assign content_scale_size, a Window-only property.
var content_scale_size := Vector2i.ZERO
