# Case 14: The guard that cannot decide

Chapter 14, Game AI and systems. Seeded flaw: a guard's state machine switches between chase and patrol at a single sight-range threshold, so it flickers when the player stands near the boundary; the test only checks the two far cases. Key terms: hysteresis, flicker, finite state machine, transition, sight range, threshold.

---

# STUDENT PAGE

## Scenario
Aisha is the designer of a stealth game. Guards should notice the player within a sight range and give chase, then give up when the player escapes. In play, a guard standing with the player at the edge of its vision rapidly alternates between chasing and patrolling and looks "twitchy". The agent says the AI is finished.

## The instruction given to the agent
"Make the guard chase the player when within sight range and go back to patrolling when the player is out of sight. Test it."

## Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
Guard FSM: states patrol, chase.
  patrol -> chase : distance_to_player < SIGHT (200 px)
  chase  -> patrol: distance_to_player >= SIGHT (200 px)
Test guard_test.gd:
  player at 150 px  -> expect state == chase   PASS
  player at 250 px  -> expect state == patrol  PASS
Result: 2/2 pass. Both transitions are verified.
The guard behaves correctly at all distances.
```

## Questions (10 points)
1. **(5 pts)** What is the flaw in the agent's work, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction that turns "behaves correctly at all distances" into evidence.
3. **(2 pts)** Write the corrected instruction to the agent.
4. **(1 pt)** In two sentences and no jargon, tell Aisha why the guard looks twitchy.

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
Both transitions use the same 200 px threshold, so a player hovering near 200 px flips the guard between states every tick (flicker) and the fix is hysteresis (a larger distance to stop chasing than to start); the test only checked 150 px and 250 px, far from the boundary.

## Terms
- **Full credit (2):** hysteresis (different thresholds to enter and leave); flicker; boundary / edge case near the threshold.
- **Half credit (1):** "needs a delay", "a cooldown", "the guard switches too fast", "needs smoothing".
- **No credit:** "use A*", "use a behavior tree" as the only answer, "increase sight range", "navigation mesh".

## Acceptable evidence requests
1. "Move the player slowly back and forth across 190 to 210 px for 100 ticks and count state changes; require at most 1 or 2 changes, not one per tick."
2. "Test the boundary: player at 199, 200 and 201 px, and a path that wobbles around 200; report the state each tick."

**Unacceptable:** "Test at 100 px and 300 px" (already done), "play it", "run the same test twice".

## Traps
- A behavior tree is a valid design change but does not by itself stop flicker; do not credit it as a fix unless re-evaluation/memory is explained.
- A short timer (minimum time in state) also reduces flicker; credit Fix 1 to 2 and Term 1, since it is not hysteresis.
- "Increase the sight range" moves the problem and does not remove it.

**CAP RULE:** if the flaw is missed, the case maximum is 5/10.

## Scored sample answers
**Strong (9/10).** Q1: "Both transitions use one threshold, 200 px, so near the edge the guard flickers between chase and patrol. It needs hysteresis. The tests used 150 and 250 px, far from the boundary." Q2: "Move the player back and forth across 190 to 210 px for 100 ticks and count state changes." Q3: "Start chasing under 200 px but only return to patrol past 260 px, and add a boundary test that counts changes." Q4: "The guard has one line for 'I see you' and the same one for 'I lost you', so it flips back and forth at the line." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: all correct; Q4 uses "line" without saying what the line is.*

**Typical (6/10).** Q1: "The guard flickers near 200 px because the number is the same both ways." Q2: "Test the player at the edge." Q3: "Make it use two different distances." Q4: "The guard keeps changing its mind at the edge." *Catches 3; Term 1 ("flickers" described, no hysteresis); Evidence 0 ("at the edge" has no pass/fail); Fix 1 (two distances, no values or test); Scope 1.* Total 6. *Reason: right idea, plain, thin on method.*

**Fluent but wrong (3/10).** Q1: "The FSM should be replaced by a behavior tree with a selector and a blackboard so priorities are re-evaluated every tick, and pathfinding should use A* with an admissible heuristic." Q2: "Verify the navigation mesh is baked correctly." Q3: "Rewrite the guard as a behavior tree using A*." Q4: "The guard needs a smarter brain." *Catches 0; Term 0; Evidence 1 (a check, wrong target); Fix 1; Scope 1.* Total 3. *Reason: AI buzzwords, no sign it saw the shared threshold.*
