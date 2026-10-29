# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
class_name CharacterIntent  # Global class name: used by the player brain, AI brains and later networking
extends RefCounted  # Reference-counted object: freed automatically when nothing uses it, no manual free()
## A character "intent": what the character wants to do this frame (code rules 6 and 7a).
## Data only, no logic. Filled in by a brain (player input, AI, network) and handed to the body's apply_intent().

# ============================================================
# Constants: enums used in the intent
# ============================================================
## The tablet key's result this frame. The brain decides short or long press; the body only switches state by the table.
enum TabletPress {
	NONE,  # No short press and no long press this frame
	SHORT,  # Short press: released before the long-press time was reached
	LONG,  # Long press: held for the long-press time (counts at once, without waiting for release)
}

# ============================================================
# Member variables: the contents of the intent
# ============================================================
var move := Vector2.ZERO  # Move direction relative to the look direction: x = right (negative = left), y = forward (negative = back)
var look_yaw := 0.0  # Look direction (radians, around Y). Player = camera facing; AI = the direction it is looking
var sprint := false  # Whether to sprint
var jump := false  # Whether jump was just pressed this frame
var aim := false  # Whether aiming (player = holding the right mouse button). While aiming, the body always faces the look direction
var tablet_press := TabletPress.NONE  # Whether the tablet key was a short press, a long press, or neither this frame
