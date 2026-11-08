# Case 4: The shield nobody can pick up

Chapter 4, Scenes, collision and physics. Seeded flaw: a pickup's collision layer and collision mask are swapped, so the player never detects it, while a test that sets the overlap by hand passes. Key terms: collision layer, collision mask, Area2D, detection vs response, bitmask / layer number.

---

# STUDENT PAGE

## Scenario
Lena is a game designer on a 2D dodge game. She wants a shield pickup: when the player touches it, the player is protected for three seconds. In the build she walks straight over the shield and nothing happens. The developer says the agent's report says it works.

## The instruction given to the agent
"Add a shield pickup that the player collects by touching it. The player gets a 3-second shield. Put the pickup on its own physics layer and prove it works with a headless test."

## Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
Added shield.tscn: Area2D "Shield" with CollisionShape2D (circle, r=24).
  Layers (project settings): 1 = player, 2 = mobs, 3 = pickups.
  shield: collision_layer = 0b0001  (bit 1)
          collision_mask  = 0b0100  (bit 3)
  player (unchanged): collision_layer = 1, collision_mask = 2
Wiring: shield.body_entered -> player.activate_shield()  (3.0 s timer)
Test shield_test.gd:
  spawns shield at the player's position, calls
  shield.emit_signal("body_entered", player), waits 181 physics ticks.
  Result: PASS (shield active for 3.0 s, then off).
Summary: shield pickup works; all tests pass.
```

## Questions (10 points)
1. **(5 pts)** What is the flaw in the agent's work, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction that turns "shield pickup works" into evidence.
3. **(2 pts)** Write the corrected instruction you would send to the agent.
4. **(1 pt)** In two sentences and no jargon, explain to Lena why walking over the shield does nothing.

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
The shield's layer and mask are swapped (it sits on the player's layer and looks for pickups), so the engine never reports the player overlapping it, and the test hid this by firing the `body_entered` signal by hand instead of letting physics produce it.

## Terms
- **Full credit (2):** collision layer vs collision mask (what an object is vs what it looks for), stated correctly or the swap named; detection vs response is also acceptable; "emitted the signal by hand / bypassed detection".
- **Half credit (1):** "collision settings are wrong", "wrong layer", "bitmask" with no explanation, "the area is not detecting".
- **No credit:** "needs a bigger shape", "z-index", "the timer is wrong", "signal not connected".

## Acceptable evidence requests
1. "Run a test that moves the player into the shield with the real physics (no hand-emitted signal) and show the shield activates; also show it does not activate when the player is far."
2. "Print the shield's layer and mask and the player's layer and mask; show that the shield's layer is in the player's mask, or the player's layer is in the shield's mask."

**Unacceptable:** "Run the same test again", "check the timer is 3 seconds" (it already passes), "play it and see".

## Traps
- A student may notice the signal was faked but not the mask problem. That is a partial catch (2/3 Catches, 1 Term).
- "Signal not connected" is wrong: the connection is fine. No credit.
- Both the shield being on the player's layer and the mask pointing at layer 3 (where nothing is) are consequences of one swap; accept either description.

- Partial catch: a student who sees only that the test emitted the signal by hand (and not the layer/mask swap) scores Catches 2, Term 1 at most. Naming the swap and the hand-emitted signal is full marks. A "race condition / call_deferred" diagnosis earns Fix 0 to 1 and no Term.
**CAP RULE:** if the flaw is missed, the case maximum is 5/10.

*Check with a game developer before first use: the layer/mask reading of the report.*

## Scored sample answers
**Strong (9/10).** Q1: "The shield's layer and mask are swapped. It is on layer 1, the player's layer, and its mask looks for layer 3, where nothing lives; the player's mask is 2, so the player does not look for the shield either. The engine never detects the overlap. The test passed only because it emitted the signal by hand." Q2: "Run a test where the real player moves into the shield with physics and check the shield activates." Q3: "Put the shield on layer 3 (pickups) and set its mask to 1 (player). Rewrite the test to walk the player in through physics and remove the hand-emitted signal." Q4: "The game treats the shield and the player as things that do not look at each other, so touching does not count." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: all correct; Q4 is vague about why they do not look at each other.*

**Typical (6/10).** Q1: "The test is fake because it emits the signal. The layers look wrong too." Q2: "Test it by moving the player." Q3: "Fix the layers and run the test properly." Q4: "The shield is not set up to notice the player." *Catches 3; Term 1 (says "layers", no layer/mask distinction); Evidence 1 (moving the player is right, no pass/fail); Fix 0 (no specific instruction); Scope 1.* Total 6. *Reason: sees the problem, never says which setting is swapped or how to confirm.*

**Fluent but wrong (3/10).** Q1: "The Area2D should be a RigidBody2D so that it generates contact reports; the signal timing is also off by one physics tick." Q2: "Add a profiler capture of physics step cost." Q3: "Convert the pickup to a RigidBody2D with contact_monitor enabled." Q4: "The pickup needs a more solid body." *Catches 0 (changes the node type; a pickup should be an Area2D and not block); Term 0; Evidence 1 (a measurement, wrong target); Fix 1 (specific action, wrong one); Scope 1.* Total 3. *Reason: confident vocabulary, but misses the layer/mask and the faked signal.*
