# Case 11: Walk and run as two states

Chapter 11, Animation and interaction. Seeded flaw: a state machine with separate walk and run states and a speed threshold was built where a blend space driven by the speed parameter was needed, so the pose pops at the threshold. Key terms: blend space (blend tree), state machine, parameter, threshold, cross-fade.

---

# STUDENT PAGE

## Scenario
Nia is the lead designer of a 3D platformer. The robot should walk slowly with a light stick push, jog with a bit more, and run with a full push, changing smoothly with how far the stick is pushed. After the agent's change the robot looks fine standing still or at a full run, but between those it snaps between poses as the stick passes a point.

## The instruction given to the agent
"Make the robot's locomotion animation respond smoothly to how hard the stick is pushed. Verify it."

## Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
AnimationTree root: AnimationNodeStateMachine
  states: idle, walk, run
  transitions:
    idle -> walk  : condition speed > 0.1
    walk -> run   : condition speed > 4.0, xfade 0.2 s
    run  -> walk  : condition speed < 3.5, xfade 0.2 s
    walk -> idle  : condition speed < 0.1
  parameter "speed" set each physics tick from velocity.length().
Test: scripted input ramps speed 0 -> 6 -> 0.
      State sequence observed: idle, walk, run, walk, idle. PASS.
Result: locomotion responds smoothly to stick pressure. The state machine
with a 0.2 s cross-fade makes the transitions smooth.
```

## Questions (10 points)
1. **(5 pts)** What is the flaw in the agent's design and report, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction that turns "responds smoothly" into evidence.
3. **(2 pts)** Write the corrected instruction to the agent.
4. **(1 pt)** In two sentences and no jargon, tell Nia why the robot snaps between poses.

---

# TA RUBRIC PAGE (not for students)

## The fixed rubric
| Row | Pts | Awarded for |
|---|---|---|
| Catches the flaw | 3 | Q1 |
| Exact term | 2 | Q1 |
| Asks for evidence | 2 | Q2 |
| Fix or next step | 2 | Q3 |
| Scope and plain language | 1 | Q4 |

## The flaw in one sentence
Continuous input (how hard the stick is pushed) needs a blend space (blend tree) that mixes walk and run clips by the speed parameter, but the agent used discrete states with a threshold, so the pose jumps at the threshold; the test checked the order of states, not smoothness.

## Terms
- **Full credit (2):** blend space / blend tree driven by a parameter (speed); state machine vs blend space; threshold.
- **Half credit (1):** "should blend instead", "needs smoothing", "cross-fade is too short".
- **No credit:** "needs a longer cross-fade" as the only fix; "root motion"; "needs IK".

## Acceptable evidence requests
1. "Ramp speed from 0 to 6 in small steps and print the blend weights or the bone pose each step; the pose must change a little each step with no jump larger than a set limit."
2. "Sample the pose at speed 3.9, 4.0 and 4.1 and show the difference between consecutive samples is small."

**Unacceptable:** "Check the state sequence again" (already claimed), "watch it", "make the cross-fade longer and test".

## Traps
- A longer cross-fade only hides the jump and delays the response; do not credit it as the fix.
- A student may say "a state machine is fine, just add more states (jog)". That keeps the thresholds; Fix 0 to 1.
- A state machine remains right for idle vs jump; the best answers keep it at the top level and put the blend space inside the locomotion state.

- "Log the blend value each tick" or "watch the legs" scores Evidence 1 unless it sets a pass/fail rule (a maximum step between consecutive samples) or samples around the 4.0 threshold. "Lengthen the cross-fade" or "add more states" scores Fix 0.
**CAP RULE:** if the flaw is missed, the case maximum is 5/10.

## Scored sample answers
**Strong (9/10).** Q1: "The agent used separate walk and run states with a threshold. Smooth control by stick pressure needs a blend space driven by speed. At 4.0 the state flips and the pose snaps; the cross-fade only softens it. The test checked state order, not smoothness." Q2: "Sample the pose at 3.9, 4.0 and 4.1 and show consecutive samples differ little." Q3: "Put walk and run into a one-dimensional blend space driven by speed, inside a locomotion state, and keep the state machine for idle and jump. Re-run the sampling." Q4: "It switches from one animation to another at a line instead of mixing them gradually, so the change is sudden." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: all correct; Q4 does not mention the stick.*

**Typical (6/10).** Q1: "It should blend walk and run instead of switching states." Q2: "Test the robot at different speeds." Q3: "Use a blend tree for walk and run." Q4: "It jumps from walk to run when you push a bit more." *Catches 3; Term 1 (blend tree named but no parameter or threshold link); Evidence 0 ("different speeds" has no measurement); Fix 1 (blend tree, no parameter); Scope 1.* Total 6. *Reason: right idea, plain, not testable.*

**Fluent but wrong (3/10).** Q1: "The cross-fade is too short and the transition priority is wrong; add exit-time transitions and an Any State node to guarantee reachability." Q2: "Enumerate all the transitions and verify reachability of each state." Q3: "Lengthen the cross-fade to 0.6 s and add exit-time transitions." Q4: "The transitions are too quick." *Catches 0; Term 0 (state-machine terms, not the cause); Evidence 1 (reachability is a real check, not for this flaw); Fix 1; Scope 1.* Total 3. *Reason: state-machine vocabulary used to polish the wrong tool.*
