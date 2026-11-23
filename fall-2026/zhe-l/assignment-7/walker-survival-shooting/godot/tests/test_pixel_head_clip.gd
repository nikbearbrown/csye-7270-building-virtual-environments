# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
extends SceneTree  # Extends SceneTree: run directly with --script, no scene needed
## A7 read-back test for the sprite clip (the pixel head in the tablet OS taskbar), checked against CHANGE-BRIEF "Cycle spec" and "The sheet".
## Run: ./scripts/run-test.sh test_pixel_head_clip.gd 60
## What it can prove: the clip's only track resolves to a real Sprite2D and its frame property, uses discrete updates, keys frames 0-7 every 0.25 s,
## never keys a cell the sheet does not have, loops with no duplicate across the wrap, the slicing matches the brief, the head sits at the far left
## of the taskbar, and played at a fixed rate the frame steps exactly on the key times.
## What it cannot prove: whether the head reads well or drifts in its cell (headless mode draws nothing; that is the frame strip and my eyes).

# ============================================================
# Constants: the numbers from the brief
# ============================================================
const HEAD_SCENE := "res://computer_system/tablet_os/system/pixel_head/pixel_head.tscn"  # The head scene the clip lives in
const TABLET_OS_SCENE := "res://computer_system/tablet_os/tablet_os.tscn"  # The tablet OS scene whose taskbar holds the head
const CLIP := &"idle"  # The clip's name in the head's AnimationPlayer
const TRACK_PATH := "Sprite2D:frame"  # The one track: the Sprite2D's frame number
const FRAME_COUNT := 8  # Cycle spec: 8 frames
const KEY_INTERVAL := 0.25  # 4 fps: one key every 0.25 s
const LENGTH := 2.0  # Clip length
const HFRAMES := 8  # Grid: 8 across
const VFRAMES := 1  # Grid: 1 down
const CELL := Vector2i(56, 56)  # Cell size in pixels
const FPS := 60  # The wrapper pins --fixed-fps 60
const EPS := 0.0001  # Tolerance on times

# ============================================================
# Member variables: what the test records while it runs
# ============================================================
var failures := 0  # How many checks failed

# ============================================================
# Engine callbacks: functions Godot calls automatically at set times (these act as the entry points)
# ============================================================
## Called by Godot once when the script starts as the SceneTree. Starts the whole test.
func _initialize() -> void:
	_run()


# ============================================================
# Functions: the parts of the test
# ============================================================
## The whole test: read the clip's structure, check the slicing and the taskbar placement, then play it and watch the frame; print the result and quit.
func _run() -> void:
	var head: Control = load(HEAD_SCENE).instantiate()  # First we build the head scene on its own
	root.add_child(head)  # and put it in the tree, so node paths resolve and the AnimationPlayer autoplays
	var player := head.get_node("AnimationPlayer") as AnimationPlayer
	var sprite := head.get_node("Sprite2D") as Sprite2D
	_check_clip(player, sprite)
	_check_slicing(sprite)
	_check_taskbar()
	await _check_playback(player, sprite)
	print("== %s: %d failure(s) ==" % ["ALL PASS" if failures == 0 else "FAILED", failures])
	quit(1 if failures > 0 else 0)


## Records one check: prints PASS if it passed, otherwise prints FAIL and counts it.
func _check(ok: bool, what: String) -> void:
	print(("  PASS  " if ok else "  FAIL  ") + what)
	if not ok:
		failures += 1


## The clip's structure: one value track that resolves to Sprite2D.frame, discrete, 8 keys 0-7 every 0.25 s, LOOP_LINEAR, step 0.25, no duplicate across the wrap.
func _check_clip(player: AnimationPlayer, sprite: Sprite2D) -> void:
	_check(player.has_animation(CLIP), "the head's AnimationPlayer has the clip \"idle\"")
	_check(player.autoplay == String(CLIP), "the clip autoplays")
	_check(player.callback_mode_process == AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_IDLE, "it advances on the process tick (brief: The two clocks)")
	var anim := player.get_animation(CLIP)
	_check(anim.get_track_count() == 1, "exactly one track")
	_check(anim.track_get_type(0) == Animation.TYPE_VALUE, "the track is a value track")
	_check(String(anim.track_get_path(0)) == TRACK_PATH, "the track path is Sprite2D:frame")
	var target := player.get_node(player.root_node).get_node_or_null(NodePath(String(anim.track_get_path(0)).get_slice(":", 0)))  # The node the track names, resolved from the player's root node
	_check(target == sprite, "the track's node resolves to the real Sprite2D")
	var path := anim.track_get_path(0)
	var sub := String(path.get_subname(0)) if path.get_subname_count() > 0 else ""  # The property the track itself names (a value track's subname is a property)
	var has_property := false
	for prop in sprite.get_property_list():
		if target != null and prop["name"] == sub:
			has_property = true  # The property the track names really exists on the node it resolves to
	_check(has_property, "the track's own property \"%s\" exists on the node it names" % sub)
	_check(anim.value_track_get_update_mode(0) == Animation.UPDATE_DISCRETE, "the frame track uses discrete updates")
	_check(anim.loop_mode == Animation.LOOP_LINEAR, "loop mode is LOOP_LINEAR")
	_check(absf(anim.length - LENGTH) < EPS, "length is 2.0 s")
	_check(absf(anim.step - KEY_INTERVAL) < EPS, "Animation.step is 0.25 s (one frame at 4 fps)")
	_check(anim.track_get_key_count(0) == FRAME_COUNT, "8 keys")
	var max_cell := HFRAMES * VFRAMES - 1  # The last cell the sheet has
	for i in anim.track_get_key_count(0):
		var t := anim.track_get_key_time(0, i)
		var v := int(anim.track_get_key_value(0, i))
		_check(absf(t - i * KEY_INTERVAL) < EPS and v == i, "key %d at %.2f s keys frame %d" % [i, i * KEY_INTERVAL, i])
		_check(v >= 0 and v <= max_cell, "key %d keys a cell the sheet has (0..%d)" % [i, max_cell])
	var last := anim.track_get_key_count(0) - 1
	_check(int(anim.track_get_key_value(0, last)) != int(anim.track_get_key_value(0, 0)), "seam: the last key's frame differs from the first (no duplicate across the wrap)")
	_check(absf((anim.length - anim.track_get_key_time(0, last)) - KEY_INTERVAL) < EPS, "seam: last key to length = the key interval (0.25 s)")


## The slicing from the brief: 8 x 1 cells of 56 x 56 px, and the sheet is exactly that size.
func _check_slicing(sprite: Sprite2D) -> void:
	_check(sprite.hframes == HFRAMES and sprite.vframes == VFRAMES, "Sprite2D hframes 8, vframes 1")
	var size := Vector2i(sprite.texture.get_size())
	_check(size == Vector2i(CELL.x * HFRAMES, CELL.y * VFRAMES), "the sheet is 448 x 56 px, so each cell is 56 x 56 (got %s)" % size)
	_check(sprite.texture_filter == CanvasItem.TEXTURE_FILTER_NEAREST, "pixel art is drawn with nearest filtering")


## The head sits at the far left of the taskbar, left of the window buttons.
func _check_taskbar() -> void:
	var os: Control = load(TABLET_OS_SCENE).instantiate()
	var row := os.get_node("Taskbar/Row")
	var first := row.get_child(0)
	_check(first.scene_file_path == HEAD_SCENE, "the taskbar's first item is the pixel head")
	_check(row.get_child(1).name == &"TaskbarButtons", "the window buttons come right after it")
	os.free()


## Plays the clip at the fixed rate and reads the frame each 0.25 s: 0, 1 ... 7, then back to 0 after the wrap.
func _check_playback(player: AnimationPlayer, sprite: Sprite2D) -> void:
	player.play(CLIP)
	player.seek(0.0, true)  # We start exactly at time 0
	var frames_per_key := int(KEY_INTERVAL * FPS)  # 15 rendered frames per key at 60 fps
	for f in frames_per_key / 2:
		await process_frame  # We move to the middle of the first key's 0.25 s, so a reading never lands exactly on a key time
	var seen: Array[int] = []
	for i in FRAME_COUNT + 1:
		seen.append(sprite.frame)  # We read the frame in the middle of each 0.25 s: about 0.12, 0.37 ... 2.12 s
		for f in frames_per_key:
			await process_frame
	var expected: Array[int] = [0, 1, 2, 3, 4, 5, 6, 7, 0]
	_check(seen == expected, "played at 60 fps the frame is %s in the middle of each 0.25 s, through the wrap (expected %s)" % [seen, expected])
