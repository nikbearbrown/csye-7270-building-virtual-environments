# Signal Garden specification before implementation

2026-10-12. AI-authored worked example at Bear's direction; human acceptance pending. Add a 3D teaching scene beside Shipping Lane, using the existing Claude mascot. Preserve every original 2D source and test. Assignment 2 assets will arrive later; use authored geometric textures and explicitly temporary synthesized tones.

## Contract

M-01: WASD or arrows move Claude at 3 metres/second on a flat 12 × 6 metre platform. Start marker (-4,0,0); charge-pad marker (-2,0,0); gate at x=1; finish x>3.8. E near the pad starts a committed 0.6-second charge. Motion is locked during charging; subsequent E presses are ignored. Completion latches the gate open. R resets the entire scene. P or Escape pauses simulation and audio. M mutes sound without changing play.

AC-01: Input right for 30 physics ticks moves 1.5 ±0.10 m at 60 ticks/second. Input only, measured against the start marker. No animation may change this.
AC-02: E outside radius 0.8 m stays silent, does not charge, and leaves the gate closed after 60 ticks. Input only from start.
AC-03: Move to the pad with input, press E: charge remains active at 0.3 seconds and gate latches open at 0.6 seconds ±one render frame plus one physics tick. At 30/60/144 render fps physics stays 60 Hz; do not assume integer ticks per render frame.
AC-04: The closed gate blocks travel past x=0.5 (tolerance 0.1 m); open gate allows input travel to the finish. Ordinary input, collider at x=1 as reference.
AC-05: Reset returns within 0.05 m of the named start marker, zero charge, gate closed, no active burst, and no old event audio.
AC-06: Shipping Lane mechanics, keyboard, Clawd, route and feature tests continue to pass. Existing 2D files remain byte-identical.

## Predictions

A collider may remain active after its mesh lifts; check both closed/open travel. A held E may repeatedly trigger charge or audio; count transitions. Frame-counted shader fading may pass at 60 but fail at 30/144; use elapsed simulation time. Rig bone paths may look valid but animate nothing; inspect bone poses and real rendering. A particle may report emitting while invisible; inspect actual frames. Dummy-driver audio meters may miss short sounds; capture samples. MultiMesh may reduce draw submissions without reducing headless CPU time; measure both variants and keep an honest conclusion.

## Boundaries

No new film, upload, GitHub push or Canvas submission. Human fun, art approval, motion feel, listening, device performance and blind-review claims remain unsigned. This build uses Codex; do not represent it as a Claude Code transcript. Proposed future Claude Code prompts are separate from execution records.
