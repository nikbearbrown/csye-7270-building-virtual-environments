"""Write the A6 film's paperwork from the current beat sheet (run after audio + media)."""
from pathlib import Path
import json
import subprocess

REEL = Path(__file__).resolve().parents[1]
GAME = REEL.parents[1]
sheet = json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))
beats = sheet["beats"]
head = subprocess.run(["git", "-C", str(GAME), "log", "-1", "--format=%H"], capture_output=True, text=True).stdout.strip()


def write(name, text):
    (REEL / name).write_text(text.strip() + "\n", encoding="utf-8")


def kind(b):
    return b["shot"].get("remotion", {}).get("pattern", "Real engine evidence (media/%s.mp4)" % b["beat_id"])


write("COMPONENTS.md", "# A6 components\n\nCode beats are Godot editor reconstructions (source path and lines on screen); each is followed by the real result it produces.\n\n" +
      "\n".join(f"- {b['beat_id']}: {kind(b)} — {b['shot']['show'][0]['event']}" for b in beats))
t, rows = 0.0, []
for b in beats:
    d = b.get("actual_duration_s", b.get("estimated_duration_s", 0))
    rows.append(f"| {b['beat_id']} | {t:.2f}–{t + d:.2f} s | {b['shot']['show'][0]['event']} |")
    t += d
write("SHOTLIST.md", "# Shot list\n\nMeasured narration is the clock (Kokoro am_onyx). Captures play at their recorded 30 fps; a take shorter than its beat is replayed once and labelled REPLAY on screen; still boards are held. The conformed timeline is written by the compiler.\n\n| Beat | Approximate span | Visible sequence |\n|---|---|---|\n" + "\n".join(rows))
write("PROMPTS.md", "# Prompts\n\nThe opening prompt is a suggested demonstration prompt (a reconstruction for the Walker bookend), not a transcript of the session that built A6. The Your Turn prompt is a bounded viewer exercise.\n\n" +
      "\n\n".join(b["shot"]["remotion"]["props"]["command"] for b in beats if b["shot"].get("remotion", {}).get("pattern") == "ClaudeComposerAsk"))
write("FACTCHECK.md", f"""# Fact check

Every number spoken or shown was checked against the files below at commit `{head}` (working-tree hashes in gamedev-evidence.json).

- Event sites: `_hit_spark(target)` is called at entities/player.gd 915 (basic hit), 977 (Lappland cross) and 1784 (Amiya cut); the function is lines 948–954 and adds the burst to `game`.
- Feedback mapping: entities/fire_pit.gd 104–110, `ratio = LOW_RATIO + (1 - LOW_RATIO) * clamp(burn_left / FULL_FIRE)` with LOW_RATIO 0.3, FULL_FIRE 120; `amount` is not written.
- Intent blocks: CHANGE-BRIEF.md 52–62 (A) and 205–212 (B), shown verbatim.
- Sparks: amount 14, lifetime 0.35, randomness 0.4, one_shot, explosiveness 1.0, local_coords false (effects/hit_spark.tscn 177–191); sphere r 0.1, spread 180, velocity 3–6, gravity −9.8, damping 6–10, hue ±0.03 (79–95).
- Puff draw: blend_mode 0 (MIX), unshaded, billboard 3 (particles), vertex colour as albedo (145–152); QuadMesh_puff 1.0 × 1.0 since r1 (154–156; brief r4). Before r1 it was 0.5.
- Effect A r1 (TUNING.md): proposal and prediction committed in cc9ebfaf before any edit; first declined ("Don't change."), later approved; edit bac2d460; strips ca1b6142. Predicted the snow patch 630–650 × 378–386 ≤ 150 on frames 15/20; measured 158.3 on every frame in r0-snow and r1-snow (miss). Changes confined to 621–661 × 340–376. City patch ≤ 3 levels (held). User verdict: "Keep."
- Strip r0: bursts at frames 10 and 16, seeds 7370/7371, the log reports 0 HitSpark nodes at frame 50; Claude's still reading and the user's "I can see it splashing outward" are quoted from TUNING.md (translated).
- r0-snow: 158.3 luminance on every frame (TUNING.md, Claude's measurement); the user's "I can see it" / "Barely see a little."
- Effect B r0/r0b/r1: occlusion diagnosis withdrawn after the user's screenshot; fixture fixed with seed_rng + pit 1; Flames quad 0.30 → 0.55, warm px r0b 72/58/76/36 → r1 170/164/162/108 (frames 12/40/54/70); top rose 2–3 px, predicted ≥ 5 (miss); verdict "Keep."
- Shader: shaders/particles_generated.gdshader line 140 (initial velocity from min/max), 161–162 (scale curve, colour ramp), 236 (AMOUNT_RATIO skip). Attempt 1 (evidence/a6/step6/) lacks the sphere radius, ramp and curve; the on-screen diff is the actual `diff` output.
- Tests: config 165/0 (A) and 123/0 (B); M1 exit 1 with "got 0.0, 6.0"; M1b exit 0; M2 exit 1 "got 4.0, 4.0"; A state 0 failures (22 PASS); B state 0 failures, monitor 11846 samples, 352 ratios, 0 violations; suites 78/89 before, 82/93 after (logs/baseline-*/summary.txt). These logs predate r1 except the config result, which the main session re-ran after r1 (165/0, TUNING.md).
- Prices: cost_effects SUMMARY (empty 0.0032 ms, game_off 7.6759 ms, A_8 +0.0248 ± 0.0287, B_1 −0.0132, B_all +0.0621; all within 2 SE). GPU: Update GPU Particles 0.14 ms (A) and 0.09 ms (B) from the user's screenshots, budgets 0.25 / 0.15 ms, predictions 0.05 / 0.06. Both prices predate Effect A r1 (TEST-REPORT order note).
- New captures (B03, B05, B11, B19): see SOURCES.md; event frames come from their capture logs.
- Not claimed: human play footage, fun, legibility for players in general, the draw-step GPU cost, the boss-arena fire on screen.
""")
write("SOURCES.md", f"""# Film sources

Game: Downfall (walker-downfall), Godot 4.7.2-stable, Forward+ / D3D12, RTX 4060 Laptop GPU. Filmed from git commit `{head}`; the ledger hashes the working tree, which had no tracked-file modifications at filming (gamedev-evidence.json source_revision).

## Code shown
Exact excerpts listed in gamedev-evidence.json (path, lines, text). Editor views are Godot editor reconstructions (GodotDevWorkbench), not screen recordings.

## Existing engine evidence (same build, hashed in the ledger)
- FIXTURE captures: captures/hit_spark/r0, r0-snow, r1, r1-snow; captures/fire_pit_flames/r0, r0b, r1 (Movie Maker, 30 fps, preview scenes).
- USER SCREENSHOTS: evidence/a6/gpu/*.png (Visual Profiler), evidence/a6/user/fire_pit_preview_occluded_by_boulders.png.
- Mutation fixture frame: evidence/a6/mutations/m1_godot3_name_frame12_fixture.png. Logs: logs/*.log, evidence/a6/mutations/*.log.

## New captures for this film (capture/, gitignored; commands and logs beside the frames)
All windowed Godot 4.7.2 Movie Maker, `--fixed-fps 30`, 1280×720, run by tools/run_captures.sh from this folder. No game file was edited; the two helper scripts live in tools/ and are loaded with `--script`.
- capture/a_play (B03): tools/capture_play.gd — SCRIPTED-INPUT fixture: real main.tscn and loop, real left-mouse events (as tests/test_hit_spark_state.gd), fixture dummy enemies; city, seed 2026; hit_spark.tscn at r1 (Puff 1.0; sha256 in effect-hashes.txt). A first take (capture/a_play_take1_r0settings_occluded, Puff 0.5) was not used: a map prop hid the dummy.
- capture/b_loop (B05): previews/fire_pit_flames_preview.tscn -- --loop, 540 frames.
- capture/a_loop_city (B11): previews/hit_spark_preview.tscn -- --loop, 660 frames; captured after the r1 edit (Puff 1.0).
- capture/b_states (B21): tools/capture_fire_states.gd — fixture with an on-screen FIXTURE label: feed, tree pause, hide/show, burn to 24 s, burn to 0 via FirePit.feed()/burn().
Enlargements use nearest neighbour and are labelled with their factor. Takes shorter than their beat are replayed once and labelled REPLAY. Nothing is retimed.

## Textures
None sourced; the effects use GradientTexture2D/1D and CurveTexture written inside the scene files (SOURCES.md of the game).

## Toolkit, voice, music
Brutalist toolkit (local brutalist.art): godot-gamedev skill, walker modifier; ai-explainer chassis; riff. Voice: local Kokoro am_onyx (Liam, in for Bear), not a clone. Outro: locked ClaudeTitleOutro with the toolkit's stock jingle (outro-audio.json). No paid calls, no Higgsfield, no captions.
""")
write("RIFF.md", """# Evidence-led commentary

| Artifact + range | Visible observation | Interpretation / limit | Next experiment |
|---|---|---|---|
| capture/a_play (B03), frames 26–200 | 8 bursts while held; pairs 3 frames apart overlap; a 1-HP dummy disappears and its burst finishes | Overlap and freed-parent rules hold in one scripted run; the older pink mesh spark dominates the frame | Compare legibility with the mesh spark off (not done) |
| capture/b_loop (B05) | lit at once, thinner after frame 250, out after 400 | Feedback loop reads at default zoom only as a small tuft | Zoomed-in strip at camera size 12 |
| r0 strip + crops (B07, B09) | flash on trigger frame, specks by 15, empty by 30 | Stills under-sell motion; the user's verdict in motion overruled Claude | — |
| capture/a_loop_city (B11) | repeated pairs, sparks brake and darken | Motion carries the throw | — |
| r0-snow / r1-snow (B13, B15) | puff barely visible; r1 darkens the body only | Fading alpha keeps the large puff transparent; prediction missed; kept by the user | Raise the puff's mid-life alpha, predict first |
| r0/r0b/r1 fire (B17, B19) | occluded pit → open pit → bigger core | Height did not follow quad size (miss) | Raise velocity or lifetime for height |
| capture/b_states (B21) | freeze, hide/show, thin, die out | Matches the headless B1–B6 assertions on screen for one run | — |
| r1 frames 12/40/54 (B23) | lean differs per frame | Turbulence visible; embers not | Larger ember quads |
| Visual Profiler screenshots (B34) | Update GPU Particles 0.14 / 0.09 ms | Process step only; single frames; before r1 | Multi-frame average, draw step |

Observations are separated from source explanations. No claim about fun, fairness or accessibility follows from these captures.
""")
write("CHECKS-REPORT.md", f"""# Teaching checks

{len(beats)} beats: 16 code beats each followed immediately by its real result; 2 further evidence boards (GPU price, credits); 5 bookend beats. 0 PUNT.

Teaching arc: FRAMEWORK ✓ (emission / process / draw before tuning) | WORKED EXAMPLE ✓ (r0 → r1 on both effects, with predictions) | FALSIFIABILITY ✓ (mutations, two prediction misses, wrong diagnosis) | SCAFFOLDED TASK ✓ (Your Turn: one setting, one prediction, the human's verdict) | BOOKENDS ✓ (composer → hesitant writer → body → verdict → Your Turn → locked outro) | NO-SOURCE-NO-VERDICT ✓ (every verdict quoted from TUNING/TEST-REPORT).

Held still boards are evidence comparisons with legible crops; motion beats use native takes at recorded speed.
""")
write("BUILD-PROMPT.md", """# Rebuild the A6 film

Use the delivered A6 project and the local Brutalist toolkit. Preserve the game and the A5 film. Set PYTHONUTF8=1 and use the interpreter with kokoro-onnx (python3). Never publish; no paid calls.

1. Re-read CHANGE-BRIEF (Revisions), TUNING, TEST-REPORT, FRICTIONAL. Recheck excerpt line ranges in tools/film.py.
2. `python3 tools/film.py author` (resets measured fields) — only for a new build.
3. `python3 runtime/scripts/generate_audio_kokoro.py REEL` (am_onyx), then `python3 tools/attach_outro.py`.
4. If capture/ is missing: `tools/run_captures.sh a_play b_states a_loop_city b_loop` (windowed Movie Maker, 30 fps; touches only capture/ and Godot's .godot cache).
5. `python3 tools/make_media.py`, then look at frames of every media/BXX.mp4.
6. `python3 runtime/scripts/remotion_scenes.py REEL --only B02` (pilot, inspect), then all.
7. `python3 tools/write_records.py`; `python3 tools/film.py ledger`; `./art godot-gamedev --check REEL --game GAME`.
8. `./art final REEL --height 2160 --fps 30 --out REEL/exports/landscape`.
9. `python3 tools/review_film.py`; inspect _qc frames (2 fps contact sheets and 15/50/85 % per beat); record in _qc/REPORT.md. Refresh the ledger and rerun the checker.
""")
write("BUILD-LOG.md", """# Build log

- Captures: a first a_play take was hidden behind a dumpster (map prop); the dummy was moved to the other side and the take recaptured (first take kept, unused). An overlapping duplicate capture run was stopped and its partial folders deleted.
- Mid-build the user approved and kept Effect A r1 (Puff 0.5 → 1.0). The Effect A section was restructured (r0-snow → proposal → r1 strips → verdict) and narration regenerated after the verdict arrived. a_play and a_loop_city were captured after the r1 edit and are labelled so.
- Pilot B02 (GodotDevWorkbench) inspected; the bottom cue label was changed to the full note text.
- Still boards were re-laid out after review for larger crops and type.
- remotion_scenes.py updates the toolkit's gitignored runtime/remotion/_bench/consumers.json index (its own generated index); no other toolkit file was changed by this build.
- The toolkit's documented scripts/type_check.py is not present in this install; no automated type-check pass is claimed. Frame review is manual (see _qc/REPORT.md).
""")
print("records written; commit", head)
