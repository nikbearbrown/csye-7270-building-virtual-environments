# FRICTIONAL.md — Assignment 6

Written by the agent (Claude Code, Claude Opus 5.5) from the session record,
commits, logs and the user's recorded replies, 2026-11-07. The user's own words
are quoted (translated from Chinese, original in brackets). Nothing here claims
a human experience the user did not report. The A5 log is at tag `a5`.

## Who did what

| | Agent (Claude Code + six delegated agent sessions) | User |
|---|---|---|
| Choices | proposed the two effects after auditing the game's particles | chose them; chose the upload location; asked for "only what the course requires" [只传本次课程要求的] and that it "can be opened and checked" [上传的内容需要能够被打开检查]; asked for English write-ups [记得翻译成英文] |
| Writing | CHANGE-BRIEF.md and its revisions, every prediction and strip reading, reviews, TUNING/TEST-REPORT/README/SOURCES/this file, all commits | — |
| Code | sessions 2/3/4/5/7 (`prompts/`, `sessions/`): effect scenes, config/state tests, previews, wiring, cost script; main session: probes, fixtures (`play_check`, `gpu_price`, scratch scene), `--loop`/`--snow`/`--pit`/`seed_rng` fixes | — |
| Runtime checks | prepared each window and checklist | every runtime verdict, both tuning decisions, the Step 6 editor conversion, the Visual Profiler readings |

The course runs agent steps as `claude -p` sessions. The `claude` CLI is not
installed on this machine, so, as in A5, each step ran as a delegated agent
session given the prompt verbatim plus written tool rules in place of
`--allowedTools`; the transcripts are in `sessions/` (labelled excerpts where
over ~1 MB). This is a deviation from the course command, not a hidden one.

## What was tried and what happened

1. **Upload scope changed twice.** The first plan copied the whole 3.8 GB game.
   The user asked for only what A6 requires, then for something a reviewer can
   open. The agent undid the unpushed snapshot commits and tracked the export
   whitelist plus tests (648 MB, 3961 files; commit `6b39df56`). Checked by a
   fresh clone at the end (TEST-REPORT).
2. **Headless one-shot emitters lie.** The probe (`tests/a6_probe_headless.gd`)
   showed a one-shot `GPUParticles3D` reads `emitting == false` from frame 1 and
   never emits `finished` headlessly. Expected: `finished` would free the
   burst. Response: HitSpark frees itself on its own 0.55 s timer; the state
   test counts nodes (brief r1, `97c7abd1`).
3. **First strip vs the user's eyes (TUNING Effect A r0).** The agent read r0 as
   "sparks too small to read outward". The user, watching it move: "I can see
   it splashing outward" [看得出向外迸溅]. Still frames lost the motion; the
   user's verdict stood and nothing was changed on the agent's reading.
4. **Effect A's only proposal was declined** (TUNING Effect A r1): the Puff
   barely showed on snow ("Barely see a little" [勉强看到一点]); the agent proposed
   a larger quad; the user first said "Don't change" [不改], then later asked
   for it ("Change effect A's puff" [把effect A的烟团改了]). Applied with the
   prediction written before the decline; the predicted darkening of the snow
   did not happen (only the body darkened); the user kept it [保留]
   (`bac2d460`, `ca1b6142`).
5. **Wrong diagnosis on the fire pit** (TUNING Effect B r1). User: "Blocked by
   the stones, can't see it" [被石头挡上了看不到]. The agent blamed the emitter
   height and wrote a prediction; the user's screenshot showed level boulders.
   Two fixture faults explained it: `fixed_map_seed` alone did not make the
   floor repeatable (3 or 4 pits, moving), and pit 0 had the player on it. The
   agent withdrew the proposal, seeded every RNG stream and chose an open pit
   (`1c0a4e78`). The underlying level bug was parked for after A6 at the user's
   request ("Do A6 first, fix it after" [先做a6，做完再修]).
6. **The kept revision** (TUNING Effect B r2): "Looks smothered in the wood; the
   fire should be bigger" [像是闷在木头里，火应该更大] → Flames quad 0.30 → 0.55,
   approved [批准，改吧], predicted ≥ 2× warm pixels and ≥ 5 px higher; measured
   2.2–2.8× but only 2–3 px higher (miss recorded), kept by the user [保留]
   (`ccb4097c`, `c6429399`, `73c0d1c9`).
7. **Mutations.** The Godot 3 float spelling `initial_velocity = 3.0` failed the
   config test and silently ran in game; the Vector2 spelling passed because
   4.7.2 keeps `initial_velocity` as a compatibility alias (`df0c2f39`).
8. **Real input headless.** The Step 3 session found that
   `Input.parse_input_event` never reaches `GameManager._input` headless (why
   the old `test_lappland_input` fails); its test also pushes the event into the
   root window. The Step 5 session found E/Esc needed `Input.flush_buffered_events()`.
9. **The process shader** could not be dumped by script (no shader RID from
   GDScript). The user converted it in the editor; the first conversion was a
   stale default shader (point emission, no ramp/curve). After the user toggled
   the emission shape, the second was complete (`1add28db`, TEST-REPORT).
10. **Pricing.** The cost script's empty scene (3 µs) proved it was not timing
    itself; both effects were indistinguishable from the control headless. The
    GPU fixture first used F7/F8, which the user found stop the running scene
    [摁f8就关了]; keys moved to U/I/O. The user's Visual Profiler frames gave the
    process step: A 0.14 ms, B 0.09 ms (`70bad4ea`).

## Agent mistakes caught

- Wrong occlusion diagnosis (5), caught by the user's screenshot.
- Non-deterministic fixture (5), found while chasing it.
- F7/F8 keys (10), caught by the user.
- Step 2 session deleted a `.wav` beyond the `rm` scope it was given; harmless,
  noted. Step 3 session used `cp` outside its allowed Bash list for a log copy.
- Godot's `--import` rewrote 1549 `.import` files to LF; committed separately
  so it would not hide real diffs (`3290679b`).

## Accepted, modified, rejected

The agent accepted the sessions' code after reading every diff; it modified
the previews (loop/snow/seed/pit fixes) and rejected nothing outright. The
user declined one tuning proposal and later approved it, approved and kept
both revisions, and redirected one diagnosis.

## Still uncertain

Effect A's draw-step GPU cost; embers' visibility at default zoom; whether the
boss-arena fire behaves on screen as the headless test says; the vsync-off FPS
comparison (not done).
