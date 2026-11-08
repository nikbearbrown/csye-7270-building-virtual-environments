# Case 1: Movement on the wrong clock

Chapter 1, Walker and Godot. Seeded flaw: a character that moves and collides is driven from `_process` (the per-frame callback) instead of `_physics_process` (the fixed-rate callback). Key terms: `_process`, `_physics_process`, delta, fixed timestep, frame-rate independence, tunnelling.

---

# STUDENT PAGE

## Scenario
Arjun is the designer of a 2D platformer. Playtesters on slower laptops say the hero "sometimes sinks into the floor" and "slips through thin ledges" when the game stutters, while on his desktop it feels fine. He asks a coding agent to fix the hero's movement so it behaves the same on every machine.

## The instruction given to the agent
"The hero's movement feels different on slow machines. Make it behave identically regardless of the machine's speed, and tell me what you changed."

## Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
Diagnosis: speed was applied without scaling by elapsed time.
Change in hero.gd:
  func _process(delta):
      velocity.x = Input.get_axis("left", "right") * SPEED * delta * 60.0
      velocity.y += GRAVITY * delta
      move_and_slide()
Moving every movement line into _process and multiplying by delta makes
the hero frame-rate independent: a 30 FPS machine takes bigger steps that
add up to the same distance per second as a 144 FPS machine.
Verified by reasoning: distance per second is identical at any frame rate.
Status: fixed.
```

## Questions (10 points)
1. **(5 pts)** What is the flaw in the agent's fix, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction that would turn "Status: fixed" into evidence.
3. **(2 pts)** Write the corrected instruction you would send to the agent.
4. **(1 pt)** In two sentences and no jargon, explain to Arjun why slow laptops still have trouble.

---

# TA RUBRIC PAGE (not for students)

## The fixed rubric
| Row | Pts | Awarded for |
|---|---|---|
| Catches the flaw | 3 | Q1 |
| Exact term | 2 | Q1 |
| Asks for evidence | 2 | Q2 |
| Fix or next step | 2 | Q3 |
| Scope and plain language | 1 | Q4, no over-claiming |

## The flaw in one sentence
The hero moves and collides inside `_process`, which runs once per rendered frame at a variable rate, instead of `_physics_process`, the fixed-rate tick physics uses, so on slow machines steps get large and the hero can sink into floors or tunnel through thin colliders; scaling by delta fixes distance per second but not collision.

## Terms
- **Full credit (2):** `_physics_process` / physics tick / fixed timestep, with the explanation that collision needs fixed steps; "tunnelling" used correctly.
- **Half credit (1):** "should use the physics callback" with no reason; "frame-rate independence" alone (the agent claimed it, so naming it only repeats the claim); "delta is wrong".
- **No credit:** "needs a higher frame rate", "gravity too weak", "should cap the FPS".

## Acceptable evidence requests
1. "Run the headless movement test with a deliberately slowed frame rate (e.g. 15 and 144 FPS) and show the hero stays on the floor and cannot pass through the 4-pixel ledge at both."
2. "Move the logic into `_physics_process`, run the existing floor and ledge checks with `--fixed-fps` pinned at two values, and show matching positions after 2 seconds."

**Unacceptable:** "Look at the code again", "run the game on my laptop and see", "verified by reasoning" repeated.

## Traps
- Students may accept "multiplied by delta, so frame-rate independent" because it sounds right. Delta-scaling is necessary but not sufficient here: that is the point of the case.
- The `* 60.0` on velocity before `move_and_slide()` is a second oddity (move_and_slide already uses delta); do not award flaw credit for this alone.
- "Verified by reasoning" is a claim, not a check; do not credit it as evidence.

- "Add a delta clamp / cap the delta" is not the fix and earns no Catches or Fix credit. Noticing that `* delta * 60.0` before `move_and_slide()` double-scales is a correct side remark, but it does not replace naming the wrong clock.
- Repeat-run evidence at two frame rates scores Evidence 1 unless it also checks the floor and the thin ledge.
**CAP RULE:** if the flaw is missed, the case maximum is 5/10.

*Check with a game developer before first use: the physics explanation in this key.*

## Scored sample answers
**Strong (9/10).** Q1: "Movement and collision are in `_process`, which runs at the frame rate. They belong in `_physics_process`, the fixed timestep. At low FPS each step is big enough to sink into the floor or tunnel through a thin ledge; delta only fixes speed, not contact." Q2: "Run the floor and ledge test at 15 and 144 FPS and show no sinking or passing through." Q3: "Move velocity and `move_and_slide` into `_physics_process`, keep gravity there, and remove the `* 60.0`. Re-run the test at two frame rates." Q4: "The game checks for walls only once per picture, and on slow laptops pictures come far apart, so the hero can jump into the floor between checks, which is why the fix has to be about how often the game checks." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: all correct, but Q4 is one long sentence a designer would not follow.*

**Typical (6/10).** Q1: "The movement should be in `_physics_process` instead. `_process` is for drawing." Q2: "Test it on a slow computer." Q3: "Change `_process` to `_physics_process` in hero.gd." Q4: "The game does not check the floor often enough on slow machines." *Catches 3 (right function, brief reason); Term 1 (names the callback, no fixed timestep or tunnelling); Evidence 0 ("a slow computer" is not a repeatable check); Fix 1 (right swap, but leaves the `* 60.0` and no re-test); Scope 1.* Total 6. *Reason: right idea, plain, but no testable evidence.*

**Fluent but wrong (3/10).** Q1: "The agent should use `delta` with `lerp` smoothing and cap the frame rate with `Engine.max_fps` to guarantee consistent frame-rate independence across hardware." Q2: "Profile with the debugger on a low-spec machine." Q3: "Set `Engine.max_fps = 60` and apply a delta-smoothing filter." Q4: "Capping the speed of the game makes it the same for everyone." *Catches 0 (accepts the delta claim and adds caps); Term 0 ("frame-rate independence" repeated, which is the agent's claim); Evidence 1 (profiling is a real measurement, but not of the claimed behaviour); Fix 1 (a concrete instruction, wrong target); Scope 1.* Total 3. *Reason: confident jargon, never moves the work to the physics tick.*
