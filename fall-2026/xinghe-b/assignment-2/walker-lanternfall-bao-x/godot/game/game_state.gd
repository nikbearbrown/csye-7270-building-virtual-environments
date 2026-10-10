extends RefCounted
## Single source of truth for run state.

signal changed(from: int, to: int)

enum { MENU, PLAYING, LEVELUP, PAUSED, WON, LOST }
const NAMES := ["menu", "playing", "levelup", "paused", "won", "lost"]
const ALLOWED := {
	MENU: [PLAYING],
	PLAYING: [LEVELUP, PAUSED, WON, LOST],
	LEVELUP: [PLAYING],
	PAUSED: [PLAYING],
	WON: [],
	LOST: [],
}

var current: int = MENU

func go(to: int) -> bool:
	if not (to in ALLOWED[current]):
		return false
	var from := current
	current = to
	changed.emit(from, to)
	return true

## Any non-menu state may restart into a fresh PLAYING run.
func restart() -> bool:
	if current == MENU:
		return false
	var from := current
	current = PLAYING
	changed.emit(from, PLAYING)
	return true

func is_terminal() -> bool:
	return current == WON or current == LOST
