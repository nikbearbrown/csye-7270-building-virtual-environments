# RIFF — what the evidence says, beyond the script

> Observations from the gated takes and recorded outputs, for a reviewer. Not narrated unless the script says so.

- **The growl is fair but fast.** In run-01 the wolf switches from its run pose to the open-mouthed pose and stands still for 0.5 s (about 7.62–8.12 s) before it dashes; the mage was still running for the first 0.16 s of it. On screen the telegraph reads mainly as "it stopped", so B15 labels it. There is no growl sound in this slice (the low growl is reserved for the boss in CONCEPT pillar 4).
- **The defeat flash comes on the second hit.** The white flash the narration mentions is most visible at the second fireball, when the wolf is already at point-blank range after its lunge; the scripted route casts while the wolf overlaps her, because the lunge carried it into her. Honest gameplay, kept by the author's decision.
- **Silence is part of the design.** After SFX-CLEAR the take is digitally silent (−inf dBFS), as CHANGE-BRIEF predicted; the B18 slot ends in that silence before cutting to run-02.
- **Mute is total.** With both buses muted, the take's audio is digitally silent, including the cast (run-03, 2.92–3.4 s).
- **What the test cannot see.** `test_sound_triggers.gd` runs on a dummy audio driver; it counts requests. That a cast is audible over the music (+3 to +5 dB RMS in the cast windows) comes from the captures and from playtest 5, not from the test.
