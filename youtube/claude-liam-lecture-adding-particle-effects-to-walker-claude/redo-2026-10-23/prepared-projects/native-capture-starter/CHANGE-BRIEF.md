# Two effects in an isolated Signal Garden teaching copy

The source is the current Walker Claude Signal Garden, with original copied files and hashes in SOURCE-PROVENANCE.json. This is an instructional derivative, not a recovered pre-particle commit. The original repository, its default game and existing local changes remain untouched.

The milestone burst signals a completed gate-opening or finish event at its world position. The original design uses one root-owned CPUParticles3D emitter: a second event intentionally replaces an active burst at the latest event position. It starts inactive, has 32 particles and a 0.7-second lifetime. This contract and replacement behavior passed state checks. Gameplay decides when events occur; particles have no collision or score authority.

The open-route motes signal that the gate is open while the room remains unfinished, presentation is enabled and the scene is visible. Their 48 particles have a 2-second lifetime. New emission stops on finish, reset or hiding. Pausing retains the emitting property while pausable processing stops. The inherited game loop's early paused return is preserved.

Predictions to check: (1) a root-owned burst remains visible when the player is hidden; (2) hiding the scene stops new motes; (3) pause freezes particle processing without clearing emission; (4) resetting during charge cannot produce a delayed gate event; (5) a replacement burst occupies the latest event position and still finishes. Machine results are in TEST-REPORT.md; native visual findings remain pending.

Proposed independent appearance revisions: the burst sphere radius grows from 0.045 to 0.055 m, with a terracotta age ramp and grow/shrink curve. The motes grow from 0.022 to 0.032 m, use a cyan age ramp and start with a 2-second pre-roll. Both keep the original count, lifetime and gameplay event logic. These are hypotheses for the upcoming before/after view at game scale, not approved visual improvements. Historical course-series tuning is retained separately and is not presented as newly authored evidence.

Provisional budget: reserve at most 2 ms of the approximately 16.7 ms frame target for combined particle work, including drawing. Headless CPU measurements alone cannot establish that budget. Real-renderer cost, interactive behavior and native visual revision checks remain required before approval.
