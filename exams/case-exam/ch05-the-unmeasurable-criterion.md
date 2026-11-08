# Case 5: The checkpoint that "activates quickly"

Chapter 5, The GDD and virtual worlds. Seeded flaw: the acceptance criterion is not checkable (no number, no tolerance), and the test sets the player's position directly instead of producing the contact through play, so it cannot fail. Key terms: acceptance criterion, tolerance, given-when-then, direct state write, false pass.

---

# STUDENT PAGE

## Scenario
Ravi is the producer of a 3D platformer. The design document says players should be able to save progress at checkpoint pads. He wants the agent to build the pad and prove it works, because the last pad "worked in the test" but players walked over it without it saving.

## The instruction given to the agent
"Write an acceptance criterion for the checkpoint pad, build it, and write a test that proves the criterion is met."

## Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
Acceptance criterion (GDD section 4.2):
  "When the player reaches the checkpoint pad, it should activate
   quickly and feel responsive."
Implementation: pad.tscn (Area3D), body_entered -> save_checkpoint().
Test checkpoint_test.gd:
  player.global_position = pad.global_position
  await get_tree().physics_frame
  assert(pad.is_active)           # PASS
Result: 1/1 tests pass. The criterion is met.
```

## Questions (10 points)
1. **(5 pts)** What is wrong with this criterion and test, and what are the exact terms for the problems?
2. **(2 pts)** Write the one check or instruction that turns "the criterion is met" into evidence.
3. **(2 pts)** Write the corrected criterion or instruction you would give the agent.
4. **(1 pt)** In two sentences and no jargon, explain to Ravi why the earlier pad could pass its test and still fail with players.

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
The criterion ("quickly", "responsive") has no number or tolerance so nothing can fail it, and the test teleports the player onto the pad (a direct state write) instead of making the player walk in, so it skips the very contact the pad depends on and passes whatever the pad does.

## Terms
- **Full credit (2):** acceptance criterion that is measurable / checkable / has a tolerance; direct state write / teleport instead of scripted input; false pass; given-when-then.
- **Half credit (1):** "criterion is vague", "test is too simple", "not realistic", with no further term.
- **No credit:** "needs more tests", "the pad should be bigger", "use a different node".

## Acceptable evidence requests
1. "Rewrite the criterion as: given the player on the ground 3 m from the pad, when scripted input walks onto it, then `pad.is_active` is true within 0.2 s (12 physics ticks); run it and show both the pass and a failing run with the pad moved away."
2. "Run the test with scripted input, not a position write, and show it fails if the pad's collision shape is deleted."

**Unacceptable:** "play it and see if it feels responsive", "add more asserts", "make the test longer".

## Traps
- A student may only criticise the vague wording and not the position write: Catches 2/3 at most.
- A student who only criticises the position write and not the wording: Catches 2/3.
- "Feels responsive" is a human check; asking for a human playtest in addition is fine and shows scope sense, but is not a replacement for a measurable criterion.

**CAP RULE:** if the flaw is missed, the case maximum is 5/10.

## Scored sample answers
**Strong (9/10).** Q1: "The criterion has no tolerance, so nothing can fail it; 'quickly' needs a number. The test teleports the player by setting position, a direct state write, so it never uses real contact and is a false pass." Q2: "Given-when-then: given the player 3 m away, when scripted input walks in, then the pad is active within 12 ticks. Show it fails when the collision shape is removed." Q3: "Rewrite the criterion with the number, drive the player by scripted input, and add a negative case." Q4: "The test put the player on the pad by magic instead of walking, so it never tested walking." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: all correct; "by magic" is not a plain reason players failed.*

**Typical (6/10).** Q1: "The criterion is too vague and the test just moves the player." Q2: "Add a real test with walking." Q3: "Say how many seconds it should take." Q4: "The test did not play the game like a person." *Catches 3 (both issues); Term 1 (vague, moves the player; no term); Evidence 0 (no pass/fail); Fix 1 (number only); Scope 1.* Total 6. *Reason: sees both, plain, but never states a checkable test.*

**Fluent but wrong (3/10).** Q1: "The criterion should be formalised as a SMART requirement and the implementation should use a signal bus decoupled from the Area3D to improve testability." Q2: "Increase code coverage with additional unit tests." Q3: "Refactor the pad into a state machine with an event bus." Q4: "The code was not modular enough." *Catches 0; Term 0; Evidence 1 (more tests is a check in a general sense); Fix 1 (an action, off target); Scope 1.* Total 3. *Reason: software-engineering vocabulary that never touches the missing number or the position write.*
