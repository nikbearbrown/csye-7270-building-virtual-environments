# Case 12: The click that is twice as loud

Chapter 12, Audio and triggers. Seeded flaw: a hit sound's trigger signal is connected twice (once in the editor and once in `_ready`), so each hit starts two voices that add together and clip; the test counts that "a click was triggered". Key terms: signal (connect), voice / polyphony, clipping, bus, handler.

---

# STUDENT PAGE

## Scenario
Rohan is the designer of a rhythm game. Each Perfect or Good hit should play a short click. Playtesters say the clicks are harsh and distorted compared to the music, as if too loud. The agent had added the click and reports that the audio works.

## The instruction given to the agent
"Play a click on every Perfect or Good hit, on the SFX bus, and add a test showing it triggers once per hit."

## Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
Scene: Conductor/HitClick (AudioStreamPlayer, bus: SFX, polyphony 4)
Wiring: judge.hit_judged -> Conductor._on_hit_judged   (connected in the editor)
conductor.gd _ready():
    judge.hit_judged.connect(_on_hit_judged)
_on_hit_judged(grade):
    if grade in ["Perfect", "Good"]:
        $HitClick.play()
Test: forces one Perfect hit and asserts that the click player is "playing"
      afterwards. PASS.
Result: one click per hit; the SFX bus plays at normal level.
```

## Questions (10 points)
1. **(5 pts)** What is the flaw in the agent's work, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction that turns "one click per hit" into evidence.
3. **(2 pts)** Write the corrected instruction to the agent.
4. **(1 pt)** In two sentences and no jargon, tell Rohan why the click sounds harsh.

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
`hit_judged` is connected to the handler twice (editor connection and `connect()` in `_ready`), so one hit calls the handler twice and starts two voices on the polyphonic player that sum, roughly doubling the level and clipping; the test only asserts "is playing", which is true with one or two voices.

## Terms
- **Full credit (2):** a signal connected twice / duplicate connection (handler called twice); voice / polyphony (two voices); clipping.
- **Half credit (1):** "plays twice", "doubled sound", "too loud", "volume is too high" without the double-connection cause.
- **No credit:** "bus volume too high" as the cause; "sample rate"; "attenuation".

## Acceptable evidence requests
1. "Force one Perfect hit and count handler calls and the number of active voices on the click player; require exactly 1 of each."
2. "Count the connections on `hit_judged` and require exactly one."

**Unacceptable:** "Assert it is playing" (already tested), "listen to it", "lower the bus volume and check".

## Traps
- "Lower the volume" hides the problem; the click is still doubled and still in the mix twice.
- A student may find the double connection but not say it summed into clipping; Catches is still full, Term 1.
- The polyphony of 4 is not itself the flaw.

**CAP RULE:** if the flaw is missed, the case maximum is 5/10.

## Scored sample answers
**Strong (9/10).** Q1: "The signal is connected twice: once in the editor and again in code. One hit calls the handler twice and starts two voices, which sum and clip. The test asserted only that the player was playing." Q2: "Force one hit and count the handler calls and the voices; both must be 1." Q3: "Remove one of the two connections, keep the one in code, and assert exactly one connection and one voice per hit." Q4: "The same click was started twice at the same moment, so it adds up to be too loud and crackly." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: all correct; Q4 says "crackly" but does not say it only happens on hits.*

**Typical (6/10).** Q1: "The sound plays twice because it is connected twice." Q2: "Check it plays once." Q3: "Remove one connection." Q4: "It plays two times at once so it is louder." *Catches 3; Term 1 ("connected twice", no voice or clipping); Evidence 0 ("check it plays once" has no way to count); Fix 1 (remove one, no check); Scope 1.* Total 6. *Reason: right cause, thin on method and terms.*

**Fluent but wrong (3/10).** Q1: "The SFX bus is hitting 0 dBFS because there is no headroom; the gain staging must be corrected with a limiter and a side-chain on the music bus." Q2: "Meter the SFX bus peak in dBFS." Q3: "Add a limiter to the SFX bus and reduce the bus gain by 6 dB." Q4: "The volume needs to be set properly." *Catches 0 (treats the symptom, accepts one click per hit); Term 0; Evidence 1 (a meter reading is a real measurement); Fix 1; Scope 1.* Total 3. *Reason: mixing vocabulary that hides the duplicate connection.*
