# Case 9: The death burst nobody sees

Chapter 9, Particle effects. Seeded flaw: the burst effect is parented to the creep that is freed in the same frame, so the particles disappear with it, while the test only checks the emitter's properties. Key terms: parenting, burst / one-shot, node lifetime, local vs world coordinates, state vs visual intent.

---

# STUDENT PAGE

## Scenario
Jing is the designer of a 2D dodge game. When the player's shield pops a creep she wants a small burst of sparks at the spot where the creep was. The agent added the effect and reports success, but when Jing plays she sees the creep vanish with no sparks at all.

## The instruction given to the agent
"When a creep is destroyed, play a one-shot burst of 24 sparks at its position. Make sure it works."

## Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
Added GPUParticles2D "Burst" as a child of the Creep scene.
  amount = 24, one_shot = true, explosiveness = 1.0, lifetime = 0.6
creep.gd:
  func die():
      $Burst.emitting = true
      queue_free()
Headless test (9/9 PASS):
  - Burst.amount == 24
  - Burst.one_shot == true
  - Burst.emitting == true after die()
Conclusion: the death burst works; a burst of 24 sparks plays at the creep's position.
```

## Questions (10 points)
1. **(5 pts)** What is the flaw in the agent's work, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction that turns "the burst works" into evidence.
3. **(2 pts)** Write the corrected instruction to the agent.
4. **(1 pt)** In two sentences and no jargon, tell Jing why she sees no sparks.

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
The burst is a child of the creep, and `queue_free()` removes the creep and its children in the same frame, so the particles are deleted before they are drawn; the test only checked the emitter's settings (state), not that particles live on screen (visual intent).

## Terms
- **Full credit (2):** parenting (attach the effect to something that outlives the creep, e.g. the level, in world coordinates); node lifetime; state vs visual intent.
- **Half credit (1):** "the node is freed", "queue_free is the problem", "effect is deleted", with no parenting or lifetime reasoning.
- **No credit:** "too few particles", "lifetime too short", "needs a GPU particle shader", "CPU vs GPU".

## Acceptable evidence requests
1. "In a headless test, kill a creep, step 10 physics ticks, then count live particle nodes in the scene tree and require at least 1 burst node with emitting or particles alive; fail if there are none."
2. "Report the burst node's parent and show it is not the freed creep; then a screenshot 0.1 s after the death showing sparks."

**Unacceptable:** "Check amount is 24" (already tested), "run the test again", "make the burst longer".

## Traps
- Students may blame `emitting = true` timing. The setting is fine; the freed parent is the problem.
- "Switch to CPUParticles2D" does not fix the problem; it is a trap that sounds technical.
- A student who says to spawn the effect as its own scene at the creep's position (world coordinates, freed after lifetime) has the correct fix even without the term "parenting".

**CAP RULE:** if the flaw is missed, the case maximum is 5/10.

## Scored sample answers
**Strong (9/10).** Q1: "The Burst is parented to the creep, which is freed on the next line, so the effect is deleted with it. This is a parenting and node-lifetime error. The test checked the emitter's properties (state), not that sparks appear." Q2: "Kill a creep, step ten ticks, and require a live burst node in the tree." Q3: "Make the burst its own scene instead of a child of the creep." Q4: "The sparks were stuck to the creep, and when the creep vanished they vanished too." *Catches 3, Term 2, Evidence 2, Fix 1, Scope 1.* Total 9. *Reason: all correct, but the fix does not say where the new scene goes or when it is freed.*

**Typical (6/10).** Q1: "queue_free removes the creep and the sparks with it." Q2: "Check that sparks exist after the creep dies." Q3: "Don't free the creep right away." Q4: "The sparks vanish with the creep, as the instruction was done in the wrong order." *Catches 3; Term 1 (queue_free, no parenting or lifetime); Evidence 1 (right idea, no way to count or pass/fail); Fix 1 (delaying the free would show the sparks, but leaves the effect tied to the creep); Scope 0 (the last clause is confusing).* Total 6. *Reason: right catch, thin on terms and method.*

**Fluent but wrong (3/10).** Q1: "GPUParticles2D has no collision with the CPU simulation path; switching to CPUParticles2D with local coordinates avoids the GPU process material overhead." Q2: "Profile the particle cost with the monitors." Q3: "Replace the node with CPUParticles2D." Q4: "The graphics card cannot draw the sparks." *Catches 0; Term 0 (CPU/GPU and local coordinates named, but not the cause); Evidence 1 (a measurement, wrong target); Fix 1 (specific action, wrong); Scope 1.* Total 3. *Reason: particle vocabulary that skips the freed parent.*
