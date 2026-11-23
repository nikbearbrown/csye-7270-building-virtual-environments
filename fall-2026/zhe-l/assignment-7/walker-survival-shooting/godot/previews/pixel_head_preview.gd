# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
extends Control  # The preview's root: a full-window panel with the head on it
## A7 preview for the sprite clip (the pixel head): the real head scene, enlarged 6x with nearest filtering on a taskbar-coloured panel, so a Movie Maker
## strip or my own eyes can check registration (the head must not drift in its cell, only bob 1 px and blink) and the seam over several wraps.
## Run (from the walker-survival-shooting folder):
##   godot --path godot res://previews/pixel_head_preview.tscn --write-movie "$PWD/captures/pixel_head/r0/frame.png" --fixed-fps 8 --quit-after 81 > logs/pixel_head_r0.log
##   (at --fixed-fps 8 there are two rendered frames per 0.25 s cell; read the odd frames, which sit in the middle of each cell. Recording at exactly 4 fps
##   samples on the key times themselves, where float rounding can show one cell twice: a capture artefact, not a duplicate in the clip. 81 frames = five wraps)

# ============================================================
# Constants: how big and where
# ============================================================
const HEAD_SCENE := "res://computer_system/tablet_os/system/pixel_head/pixel_head.tscn"  # The real head scene from the taskbar
const ZOOM := 6.0  # Enlarged 6x, so each sheet pixel is a 6 x 6 block
const TASKBAR_COLOUR := Color(0.02, 0.2, 0.5, 1)  # The taskbar's colour in tablet_os.tscn, as the background

# ============================================================
# Member variables: what the preview keeps while it runs
# ============================================================
var _sprite: Sprite2D  # The head's Sprite2D, read for the log
var _frame := 0  # Rendered frames since the start

# ============================================================
# Engine callbacks: functions Godot calls automatically at set times (these act as the entry points)
# ============================================================
## Godot calls this once when the preview starts: we paint the background, add the head enlarged in the middle, and print the log header.
func _ready() -> void:
	var background := ColorRect.new()  # First the taskbar-coloured background over the whole window
	background.color = TASKBAR_COLOUR
	background.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(background)
	var head: Control = load(HEAD_SCENE).instantiate()  # Then the real head scene, which autoplays its clip
	head.scale = Vector2(ZOOM, ZOOM)
	head.position = get_viewport_rect().size / 2.0 - head.custom_minimum_size * ZOOM / 2.0  # centred in the window
	add_child(head)
	_sprite = head.get_node("Sprite2D") as Sprite2D
	print("FRAME movie sprite_frame")


## Godot calls this once per rendered frame: we print which cell the head shows, so frame N of the capture lines up with log line N.
func _process(_delta: float) -> void:
	print("FRAME %d %d" % [_frame, _sprite.frame])
	_frame += 1
