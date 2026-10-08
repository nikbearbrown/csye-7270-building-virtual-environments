extends SceneTree

const GridWorld := preload("res://rl/gridworld.gd")
const QLearner := preload("res://rl/q_learner.gd")
const EPISODES := 500
const WINDOW := 25
const ARROWS := ["↑", "↓", "←", "→"]
var failures := 0


func _initialize() -> void:
	call_deferred("run")


func check(condition: bool, label: String) -> void:
	print(("PASS " if condition else "FAIL ") + label)
	if not condition:
		failures += 1


func test_rules() -> void:
	var world := GridWorld.new()
	check(world.reset() == 0, "start is (0,0)")
	var result := world.step(GridWorld.Action.UP)
	check(world.position == Vector2i.ZERO and is_equal_approx(result.reward, -0.01), "border stays put with step cost")
	world.step(GridWorld.Action.DOWN)
	result = world.step(GridWorld.Action.RIGHT)
	check(result.done and result.pit and result.reward == -1.0, "first pit terminates with -1")
	world.reset()
	for action in [3, 3, 3, 1, 1]:
		result = world.step(action)
	check(result.done and result.pit and result.reward == -1.0, "second pit terminates with -1")
	world.reset()
	for action in [1, 1, 1, 1, 3, 3, 3, 3]:
		result = world.step(action)
	check(result.done and result.success and result.reward == 1.0, "goal terminates with +1")
	world.reset()
	for index in range(49):
		result = world.step(GridWorld.Action.UP)
	check(not result.done, "episode continues through step 49")
	result = world.step(GridWorld.Action.UP)
	check(result.done and not result.terminated and world.steps == 50, "step 50 truncates episode")
	var learner := QLearner.new()
	learner.q_table[1][0] = 2.0
	learner.update(0, 0, -0.01, 1, false)
	check(is_equal_approx(learner.q_table[0][0], 0.189), "Q update bootstraps nonterminal transitions")
	learner.update(0, 1, 1.0, 1, true)
	check(is_equal_approx(learner.q_table[0][1], 0.1), "Q update excludes terminal bootstrap")


func run() -> void:
	var started := Time.get_ticks_msec()
	var seed_value := 42
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--seed=") and argument.trim_prefix("--seed=").is_valid_int():
			seed_value = argument.trim_prefix("--seed=").to_int()
		else:
			check(false, "invalid argument: " + argument)
			quit(1)
			return
	test_rules()
	var world := GridWorld.new()
	var learner := QLearner.new(seed_value)
	var window_return := 0.0
	var window_successes := 0
	var consecutive_successes := 0
	var first_perfect_end := -1
	var first_reported_perfect_end := -1
	print("seed=%d" % seed_value)
	print("episode,mean_return,success_rate,epsilon")
	for episode in range(1, EPISODES + 1):
		learner.set_training_episode(episode - 1, EPISODES)
		var state := world.reset()
		var episode_return := 0.0
		var success := false
		while not world.done:
			var action := learner.choose_action(state)
			var result := world.step(action)
			learner.update(state, action, result.reward, result.state, result.terminated)
			state = result.state
			episode_return += result.reward
			success = result.success
		window_return += episode_return
		window_successes += int(success)
		consecutive_successes = consecutive_successes + 1 if success else 0
		if consecutive_successes == WINDOW and first_perfect_end == -1:
			first_perfect_end = episode
		if episode % WINDOW == 0:
			print("%d,%.6f,%.2f,%.6f" % [episode, window_return / WINDOW, float(window_successes) / WINDOW, learner.epsilon])
			if window_successes == WINDOW and first_reported_perfect_end == -1:
				first_reported_perfect_end = episode
			window_return = 0.0
			window_successes = 0
		if Time.get_ticks_msec() - started >= 55000:
			check(false, "training exceeded 55-second deadline")
			quit(1)
			return
	print("first_perfect_rolling_window_end=%d first_perfect_reported_window_end=%d" % [first_perfect_end, first_reported_perfect_end])
	check(is_equal_approx(learner.epsilon, 0.05), "epsilon reaches 0.05")
	learner.epsilon = 0.0
	var state := world.reset()
	var path: Array[String] = [str(world.position)]
	var entered_pit := false
	while not world.done:
		var result := world.step(learner.choose_action(state, false))
		state = result.state
		entered_pit = entered_pit or result.pit
		path.append(str(world.position))
	print("greedy_path=" + " -> ".join(path))
	check(world.position == GridWorld.GOAL, "greedy policy reaches goal")
	check(not entered_pit, "greedy policy avoids pits")
	check(world.steps == 8, "greedy policy takes minimum 8 steps (Manhattan lower bound)")
	print("Greedy arrows: rows y=0..4, columns x=0..4; terminal cells show unused tie-break action")
	for y in range(GridWorld.SIZE):
		var row: Array[String] = []
		for x in range(GridWorld.SIZE):
			row.append(ARROWS[learner.greedy_action(world.state_id(Vector2i(x, y)))])
		print(" ".join(row))
	check(Time.get_ticks_msec() - started < 60000, "finished within 60 seconds")
	print("%s Q-learning: %d failures" % ["PASS" if failures == 0 else "FAIL", failures])
	quit(0 if failures == 0 else 1)
