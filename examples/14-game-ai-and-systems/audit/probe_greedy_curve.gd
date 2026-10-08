extends SceneTree
## Chapter-author follow-up to Lab A (written by hand, not by the Codex run).
## Trains exactly as test_qlearning.gd does, and after every episode evaluates
## the greedy policy from the start cell with exploration off. Greedy
## evaluation calls choose_action(state, false), which draws no random numbers,
## so the training sequence is identical to test_qlearning.gd's.
## Reports the first episode after which the greedy path is optimal (8 steps,
## no pit) and stays optimal for every remaining episode.

const GridWorld := preload("res://rl/gridworld.gd")
const QLearner := preload("res://rl/q_learner.gd")
const EPISODES := 500


func _initialize() -> void:
	call_deferred("run")


func greedy_steps(learner) -> int:
	var world := GridWorld.new()
	var state := world.reset()
	while not world.done:
		var result: Dictionary = world.step(learner.choose_action(state, false))
		state = result.state
		if result.pit:
			return -1
	return world.steps if world.position == GridWorld.GOAL else -1


func run() -> void:
	var seed_value := 42
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--seed="):
			seed_value = argument.trim_prefix("--seed=").to_int()
	var world := GridWorld.new()
	var learner := QLearner.new(seed_value)
	var optimal_since := -1
	var first_optimal := -1
	var flips := 0
	var last_optimal := false
	for episode in range(1, EPISODES + 1):
		learner.set_training_episode(episode - 1, EPISODES)
		var state := world.reset()
		while not world.done:
			var action := learner.choose_action(state)
			var result := world.step(action)
			learner.update(state, action, result.reward, result.state, result.terminated)
			state = result.state
		var optimal := greedy_steps(learner) == 8
		if optimal and first_optimal == -1:
			first_optimal = episode
		if optimal and not last_optimal:
			optimal_since = episode
		if optimal != last_optimal and episode > 1:
			flips += 1
		last_optimal = optimal
		if episode % 50 == 0:
			print("episode=%d greedy_steps=%d" % [episode, greedy_steps(learner)])
	print("seed=%d first_episode_greedy_optimal=%d optimal_and_stayed_optimal_from=%d greedy_optimal_flips=%d" % [seed_value, first_optimal, optimal_since if last_optimal else -1, flips])
	quit(0 if last_optimal else 1)
