class_name RudyLook
extends Node2D
## Rudy's generated frames (ASSET-LOG.md), one per pose asset ID in
## CHARACTER-SHEET.md, made by design/tools/matte_sprites.py into frames/.
## Every frame shares one canvas with the body origin (his soles, on the
## torso's centre line) at the same texture px, and is stored at 2 texture px
## per game px; the Sprite child draws it at half scale with that origin on
## this node's, as frames.json says. The controller flips this node to face
## left and fades it while he flashes. The Sprite's material adds the outer
## outline (systems/art/outline.gdshader), and it draws with mipmaps so the
## hair's fine lines do not shimmer at half scale.
## The sword form's frames show the sword and shield he holds, so nothing is
## drawn over them. CHAR-SWORD-BLOCK waits for blocking (build step 4).

const FRAMES: Dictionary[StringName, Texture2D] = {
	&"CHAR-IDLE": preload("res://content/rudy/frames/CHAR-IDLE.png"),
	&"CHAR-RUN-A": preload("res://content/rudy/frames/CHAR-RUN-A.png"),
	&"CHAR-RUN-B": preload("res://content/rudy/frames/CHAR-RUN-B.png"),
	&"CHAR-RISE": preload("res://content/rudy/frames/CHAR-RISE.png"),
	&"CHAR-FALL": preload("res://content/rudy/frames/CHAR-FALL.png"),
	&"CHAR-HURT": preload("res://content/rudy/frames/CHAR-HURT.png"),
	&"CHAR-DEFEAT": preload("res://content/rudy/frames/CHAR-DEFEAT.png"),
	&"CHAR-RESPAWN": preload("res://content/rudy/frames/CHAR-RESPAWN.png"),
	&"CHAR-CELEBRATE": preload("res://content/rudy/frames/CHAR-CELEBRATE.png"),
	&"CHAR-SWORD-IDLE": preload("res://content/rudy/frames/CHAR-SWORD-IDLE.png"),
	&"CHAR-SWORD-RUN-A": preload("res://content/rudy/frames/CHAR-SWORD-RUN-A.png"),
	&"CHAR-SWORD-RUN-B": preload("res://content/rudy/frames/CHAR-SWORD-RUN-B.png"),
	&"CHAR-SWORD-RISE": preload("res://content/rudy/frames/CHAR-SWORD-RISE.png"),
	&"CHAR-SWORD-FALL": preload("res://content/rudy/frames/CHAR-SWORD-FALL.png"),
	&"CHAR-SWORD-SLASH": preload("res://content/rudy/frames/CHAR-SWORD-SLASH.png"),
	&"CHAR-SWORD-BLOCK": preload("res://content/rudy/frames/CHAR-SWORD-BLOCK.png"),
}

var pose: StringName = &"CHAR-IDLE"

@onready var _sprite: Sprite2D = $Sprite


func show_pose(id: StringName) -> void:
	if id == pose:
		return
	if not FRAMES.has(id):
		push_error("Rudy has no frame for the pose %s" % id)
		return
	pose = id
	_sprite.texture = FRAMES[id]


## The frame on screen now.
func frame() -> Texture2D:
	return _sprite.texture
