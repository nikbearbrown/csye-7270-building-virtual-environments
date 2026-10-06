extends SceneTree

const BTNode = preload("res://npc/bt/bt_node.gd")
const Selector = preload("res://npc/bt/selector.gd")
const Sequence = preload("res://npc/bt/sequence.gd")
const Condition = preload("res://npc/bt/condition.gd")
const Action = preload("res://npc/bt/action.gd")
const S = BTNode.Status
var checks := 0
var failures := 0

func check(ok: bool, label: String) -> void:
	checks += 1
	if not ok:
		failures += 1
	print("PASS " if ok else "FAIL ", label)

func leaf(name: String, result: S) -> RefCounted:
	return Action.new(func(bb: Dictionary, _delta: float) -> S:
		bb.calls.append(name)
		return result
	)

func _initialize() -> void:
	var bb := {"calls": [], "ready": false}
	var selector = Selector.new([leaf("fail", S.FAILURE), leaf("win", S.SUCCESS), leaf("skip", S.SUCCESS)])
	check(selector.tick(bb, 0.1) == S.SUCCESS and bb.calls == ["fail", "win"],
		"Selector stops at first SUCCESS")
	bb.calls.clear()
	var sequence = Sequence.new([leaf("ok", S.SUCCESS), leaf("fail", S.FAILURE), leaf("skip", S.SUCCESS)])
	check(sequence.tick(bb, 0.1) == S.FAILURE and bb.calls == ["ok", "fail"],
		"Sequence stops at first FAILURE")
	check(Selector.new().tick(bb, 0.1) == S.FAILURE, "empty Selector fails")
	check(Sequence.new().tick(bb, 0.1) == S.SUCCESS, "empty Sequence succeeds")
	check(Condition.new(func(b: Dictionary) -> bool: return b.ready).tick(bb, 0.1) == S.FAILURE,
		"Condition maps false to FAILURE")
	bb.ready = true
	check(Condition.new(func(b: Dictionary) -> bool: return b.ready).tick(bb, 0.1) == S.SUCCESS,
		"Condition maps true to SUCCESS")

	for is_selector in [true, false]:
		bb = {"calls": [], "ticks": 0, "elapsed": 0.0}
		var running = Action.new(func(b: Dictionary, delta: float) -> S:
			b.calls.append("running")
			b.ticks += 1
			b.elapsed += delta
			return S.RUNNING if b.ticks == 1 else S.SUCCESS
		)
		var children := [leaf("first", S.FAILURE if is_selector else S.SUCCESS),
			running, leaf("last", S.SUCCESS)]
		var composite = Selector.new(children) if is_selector else Sequence.new(children)
		var label := "Selector" if is_selector else "Sequence"
		check(composite.tick(bb, 0.25) == S.RUNNING and bb.calls == ["first", "running"],
			label + " propagates RUNNING")
		bb.calls.clear()
		var expected := ["running"] if is_selector else ["running", "last"]
		check(composite.tick(bb, 0.25) == S.SUCCESS and bb.calls == expected and bb.elapsed == 0.5,
			label + " resumes running child with shared blackboard and delta")
		bb.calls.clear()
		composite.tick(bb, 0.1)
		check(bb.calls[0] == "first", label + " restarts after completion")
		bb.ticks = 0
		composite.tick(bb, 0.1)
		composite.reset()
		bb.calls.clear()
		composite.tick(bb, 0.1)
		check(bb.calls[0] == "first", label + " explicit reset forgets running child")
	print("RESULT ", checks, " checks; ", failures, " failures")
	quit(1 if failures else 0)
