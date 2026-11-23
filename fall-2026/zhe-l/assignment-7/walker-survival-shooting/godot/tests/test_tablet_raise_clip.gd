# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
extends SceneTree  # Extends SceneTree: run directly with --script, no scene needed
## A7 read-back test for the rig clip (the one-handed tablet raise) and the two hold poses, all imported from main_character.glb.
## Checked against CHANGE-BRIEF "Phase table" and "Import settings".
## Run: ./scripts/run-test.sh test_tablet_raise_clip.gd 60
## What it can prove: every track resolves to a real Skeleton3D bone, the raise's keys sit on the 30 fps frame grid from frame 0 to frame 20 (so every
## phase boundary, 7, 16 and 20, is a key), Animation.step is one frame, nothing loops, and the loop modes are written in the importer's settings.
## What it cannot prove: whether the motion reads right (that is the frame strip and my eyes).

# ============================================================
# Constants: the numbers from the brief
# ============================================================
const GLB := "res://assets/characters/main_character/main_character.glb"  # The imported character
const GLB_IMPORT := "res://assets/characters/main_character/main_character.glb.import"  # Its import settings, where the loop modes must live
const RAISE := &"tablet_raise_one_hand"  # The committing clip
const HOLDS := [&"tablet_hold_hip", &"tablet_hold_one_hand"]  # The one-frame hold poses
const FPS := 30.0  # The brief's frame rate
const LAST_FRAME := 20  # The raise runs frames 0-20
const PHASE_STARTS := [0, 7, 16]  # Startup, active and recovery begin on these frames
const TABLET_BONE := "tablet"  # The bone the tablet hangs on
const EPS := 0.0005  # Tolerance on times (a bit under a frame's 1/60 of slack)

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
## The whole test: build the imported character, read every clip's structure and the import settings, print the result and quit.
func _run() -> void:
	var scene: Node = load(GLB).instantiate()  # First we build the imported character
	root.add_child(scene)  # and put it in the tree so its node paths resolve
	var player := scene.find_children("*", "AnimationPlayer", true, false)[0] as AnimationPlayer
	var skeleton := scene.find_children("*", "Skeleton3D", true, false)[0] as Skeleton3D
	for clip in [RAISE] + HOLDS:
		_check(player.has_animation(clip), "the .glb has the clip %s" % clip)
	_check_tracks_resolve(player, skeleton)
	_check_raise(player.get_animation(RAISE))
	for clip in HOLDS:
		var hold := player.get_animation(clip)
		_check(hold.loop_mode == Animation.LOOP_NONE, "%s does not loop" % clip)
		_check(hold.length <= 1.0 / FPS + EPS, "%s is a single pose (length %.4f s)" % [clip, hold.length])
	_check_import_settings()
	print("== %s: %d failure(s) ==" % ["ALL PASS" if failures == 0 else "FAILED", failures])
	quit(1 if failures > 0 else 0)


## Records one check: prints PASS if it passed, otherwise prints FAIL and counts it.
func _check(ok: bool, what: String) -> void:
	print(("  PASS  " if ok else "  FAIL  ") + what)
	if not ok:
		failures += 1


## Every track of every clip names the real Skeleton3D and a bone it really has (a wrong name would move nothing and raise no error).
func _check_tracks_resolve(player: AnimationPlayer, skeleton: Skeleton3D) -> void:
	var base := player.get_node(player.root_node)  # Track paths are relative to the player's root node
	for clip in [RAISE] + HOLDS:
		var anim := player.get_animation(clip)
		var bad := []  # The tracks that do not resolve, so a failure names them
		var tablet_tracks := 0
		for i in anim.get_track_count():
			var path := anim.track_get_path(i)
			var node := base.get_node_or_null(NodePath(String(path).get_slice(":", 0)))
			var bone := String(path.get_subname(0)) if path.get_subname_count() > 0 else ""
			if node != skeleton or skeleton.find_bone(bone) == -1:
				bad.append(String(path))
			elif bone == TABLET_BONE:
				tablet_tracks += 1
		_check(anim.get_track_count() > 0 and bad.is_empty(), "%s: all %d tracks resolve to a Skeleton3D bone %s" % [clip, anim.get_track_count(), "" if bad.is_empty() else str(bad.slice(0, 3))])
		_check(tablet_tracks >= 2, "%s: the tablet bone has position and rotation tracks" % clip)


## The raise against the phase table: length 20 frames, step one frame, no loop, keys on the frame grid from 0 to 20, so 0, 7, 16 and 20 are all keys.
func _check_raise(anim: Animation) -> void:
	_check(anim.loop_mode == Animation.LOOP_NONE, "the raise does not loop (LOOP_NONE)")
	_check(absf(anim.length - LAST_FRAME / FPS) < EPS, "the raise is 20 frames long (%.4f s)" % anim.length)
	_check(absf(anim.step - 1.0 / FPS) < EPS, "Animation.step is one frame at 30 fps (%.4f s)" % anim.step)
	var off_grid := 0
	var tablet_frames := {}
	for i in anim.get_track_count():
		var bone := String(anim.track_get_path(i).get_subname(0))
		for k in anim.track_get_key_count(i):
			var frame := anim.track_get_key_time(i, k) * FPS
			if absf(frame - roundf(frame)) > EPS * FPS or roundf(frame) < 0 or roundf(frame) > LAST_FRAME:
				off_grid += 1  # A key between frames, or outside 0-20
			if bone == TABLET_BONE:
				tablet_frames[int(roundf(frame))] = true
	_check(off_grid == 0, "every key sits on a 30 fps frame between 0 and 20 (%d off)" % off_grid)
	for f in PHASE_STARTS + [LAST_FRAME]:
		_check(tablet_frames.has(f), "the tablet bone has a key on frame %d (a phase boundary)" % f)
	var keyed := tablet_frames.keys()
	keyed.sort()
	print("  INFO  the tablet bone is keyed on frames %s (the .glb has a key on every frame; Godot's importer drops the repeated keys where the bone stands still)" % [keyed])


## The loop modes live in the importer's per-animation settings (so a re-import keeps them), not only in the imported scene.
func _check_import_settings() -> void:
	var cfg := ConfigFile.new()
	_check(cfg.load(GLB_IMPORT) == OK, "main_character.glb.import loads")
	var subs: Dictionary = cfg.get_value("params", "_subresources", {})
	var anims: Dictionary = subs.get("animations", {})
	for clip in [RAISE] + HOLDS:
		var settings: Dictionary = anims.get(String(clip), {})
		_check(settings.has("settings/loop_mode") and int(settings["settings/loop_mode"]) == Animation.LOOP_NONE,
			"the importer's settings give %s loop_mode = LOOP_NONE" % clip)
