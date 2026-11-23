# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
extends SceneTree  # Extends SceneTree: run directly with --script, no scene needed
## A7 structure test for the tablet animation state machine: asserts CHANGE-BRIEF's state table and transition table against the AnimationTree resource.
## Run: ./scripts/run-test.sh test_tablet_state_machine.gd 60
## What it can prove: the states, the clip each state plays, every transition's condition, cross-fade, switch and advance mode, the expression base node,
## the clock, and that the tablet hangs on the "tablet" bone through the fixed mount. What it cannot prove: how the blends look.

# ============================================================
# Constants: the tables from the brief
# ============================================================
const HUMANOID_SCENE := "res://characters/human/humanoid/humanoid.tscn"  # The body scene that owns the AnimationTree
const STATES := {  # State -> the clip it plays (brief: the two-handed pose is stood in by the one-handed pose until it is posed)
	&"hip": &"tablet_hold_hip",
	&"raise_1h": &"tablet_raise_one_hand",
	&"hold_1h": &"tablet_hold_one_hand",
	&"hold_2h": &"tablet_hold_one_hand",
}
const AUTO := AnimationNodeStateMachineTransition.ADVANCE_MODE_AUTO  # Transitions advance on their own
const IMMEDIATE := AnimationNodeStateMachineTransition.SWITCH_MODE_IMMEDIATE  # Switch at once
const AT_END := AnimationNodeStateMachineTransition.SWITCH_MODE_AT_END  # Switch when the clip has finished
const TRANSITIONS := [  # [from, to, expression, cross-fade seconds, switch mode]
	[&"Start", &"hip", "", 0.0, IMMEDIATE],
	[&"hip", &"raise_1h", "get_tablet_hold() == 1", 0.0, IMMEDIATE],
	[&"raise_1h", &"hold_1h", "", 0.0, AT_END],
	[&"raise_1h", &"hip", "get_tablet_hold() == 0", 0.2, IMMEDIATE],
	[&"raise_1h", &"hold_2h", "get_tablet_hold() == 2", 0.2, IMMEDIATE],
	[&"hip", &"hold_2h", "get_tablet_hold() == 2", 0.2, IMMEDIATE],
	[&"hold_1h", &"hold_2h", "get_tablet_hold() == 2", 0.2, IMMEDIATE],
	[&"hold_2h", &"hold_1h", "get_tablet_hold() == 1", 0.2, IMMEDIATE],
	[&"hold_1h", &"hip", "get_tablet_hold() == 0", 0.2, IMMEDIATE],
	[&"hold_2h", &"hip", "get_tablet_hold() == 0", 0.2, IMMEDIATE],
]
const MOUNT_SCALE := 1.0 / 5.0684  # The fixed offset measured in Godot (CHANGE-BRIEF revision 2026-11-22)
const EPS := 0.001  # Tolerance

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
## The whole test: build the body, then check the tree, the states, the transitions and the tablet's mount; print the result and quit.
func _run() -> void:
	var body: Node = load(HUMANOID_SCENE).instantiate()  # First we build the body on its own
	root.add_child(body)
	await process_frame  # and let it run _ready()
	var tree := body.get_node("AnimationTree") as AnimationTree
	_check_tree(body, tree)
	_check_states(tree.tree_root as AnimationNodeStateMachine)
	_check_transitions(tree.tree_root as AnimationNodeStateMachine)
	_check_mount(body)
	print("== %s: %d failure(s) ==" % ["ALL PASS" if failures == 0 else "FAILED", failures])
	quit(1 if failures > 0 else 0)


## Records one check: prints PASS if it passed, otherwise prints FAIL and counts it.
func _check(ok: bool, what: String) -> void:
	print(("  PASS  " if ok else "  FAIL  ") + what)
	if not ok:
		failures += 1


## The AnimationTree's wiring: its root is a state machine, it reads the imported AnimationPlayer's clips, expressions are evaluated on Humanoid, and it runs on the process tick.
func _check_tree(body: Node, tree: AnimationTree) -> void:
	_check(tree.tree_root is AnimationNodeStateMachine, "the AnimationTree's root is an AnimationNodeStateMachine")
	_check(tree.get_node_or_null(tree.anim_player) is AnimationPlayer, "anim_player resolves to the imported AnimationPlayer")
	_check(tree.get_node_or_null(tree.advance_expression_base_node) == body, "advance_expression_base_node resolves to the Humanoid body")
	_check(tree.callback_mode_process == AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_IDLE, "it advances on the process tick (brief: The two clocks)")
	_check(tree.active, "the AnimationTree is active")
	var player := tree.get_node(tree.anim_player) as AnimationPlayer
	_check(player.autoplay == "" and not player.is_playing(), "the imported AnimationPlayer does not play on its own (one authority)")


## Every state in the brief exists and plays the brief's clip; there are no extra states.
func _check_states(sm: AnimationNodeStateMachine) -> void:
	for state in STATES:
		var node := sm.get_node(state) as AnimationNodeAnimation if sm.has_node(state) else null
		_check(node != null and node.animation == STATES[state], "state %s plays %s" % [state, STATES[state]])
	var names := []
	for name in sm.get_node_list():
		if name != &"Start" and name != &"End":
			names.append(name)
	_check(names.size() == STATES.size(), "exactly the four states in the brief (found %s)" % [names])


## Every transition in the brief exists with its condition, cross-fade, switch mode and auto advance; there are no extra transitions.
func _check_transitions(sm: AnimationNodeStateMachine) -> void:
	_check(sm.get_transition_count() == TRANSITIONS.size(), "exactly %d transitions (found %d)" % [TRANSITIONS.size(), sm.get_transition_count()])
	for want in TRANSITIONS:
		var found := -1
		for i in sm.get_transition_count():
			if sm.get_transition_from(i) == want[0] and sm.get_transition_to(i) == want[1]:
				found = i
		if found == -1:
			_check(false, "transition %s -> %s exists" % [want[0], want[1]])
			continue
		var t := sm.get_transition(found)
		var ok: bool = t.advance_mode == AUTO and t.advance_expression == want[2] and absf(t.xfade_time - want[3]) < EPS and t.switch_mode == want[4]
		_check(ok, "%s -> %s: auto, expression \"%s\", cross-fade %.1f s, switch %s" % [want[0], want[1], want[2], want[3], "at end" if want[4] == AT_END else "immediate"])


## The tablet hangs on the rig's "tablet" bone through the fixed mount (scale 1 / 5.0684, +90 degrees about X), and nothing else holds it.
func _check_mount(body: Node) -> void:
	var tablet := body.get_tablet() as Node3D
	var mount := tablet.get_parent() as Node3D
	var bone := mount.get_parent() as BoneAttachment3D
	_check(bone != null and bone.bone_name == "tablet", "the tablet's grandparent is a BoneAttachment3D on bone \"tablet\"")
	var s := mount.transform.basis.get_scale()
	_check(absf(s.x - MOUNT_SCALE) < EPS and absf(s.y - MOUNT_SCALE) < EPS and absf(s.z - MOUNT_SCALE) < EPS, "the mount's scale is 1 / 5.0684 (got %s)" % s)
	var e := mount.transform.basis.orthonormalized().get_euler() * 180.0 / PI
	_check(absf(e.x - 90.0) < 0.1 and absf(e.y) < 0.1 and absf(e.z) < 0.1, "the mount turns +90 degrees about X (got %s)" % e)
	_check(tablet.transform.is_equal_approx(Transform3D.IDENTITY), "the tablet itself sits at the mount's origin with no extra offset")
