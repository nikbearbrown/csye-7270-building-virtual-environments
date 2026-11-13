# Riff notes — claude-liam-walker-survival-shooting-a6-gamedev

Commentary is limited to what the inspected output shows. Each riff below names the evidence it rests on.

- **"A few warm dots"** (B05): read from the r0 fixture strip itself (5–8 px specks, warm tint, nothing at frame 50) and the user's own first verdict in TUNING r0.
- **"It edited before my approval"** (B06): the session transcript timestamps recorded in TUNING r1 (edit 07:56:36 UTC, prediction 07:57:19 UTC).
- **"The physics engine pushed the player up out of the floor"** (B07): TEST-REPORT Step 3 (y = 0.247278 on frame 1, 0.250177 on frame 2).
- **"No pile-up"** (B08): the six logged landings in `capture/landing-run-02.log`, and the clip itself (one cloud at a time).
- **"Gone that frame / back already spread out"** (B16): pixel comparisons of `lights-film-01` (CAPTURE.md §2) and the fixture strip readings in TUNING.
- **"Near zero says nothing about the GPU"** (B25): the cost log's own header line (dummy renderer) and the 10,000-CPU-particle control.
- **"A human lands, not a mech"** (B28): the user's words in TUNING r1.
