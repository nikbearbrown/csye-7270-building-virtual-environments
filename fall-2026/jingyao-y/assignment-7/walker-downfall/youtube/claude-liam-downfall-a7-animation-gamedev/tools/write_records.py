"""Write the A7 film's paperwork from the current beat sheet (run after audio + media)."""
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


write("COMPONENTS.md", "# A7 components\n\nCode beats are Godot editor reconstructions (source path and lines on screen); each is followed by the real result it produces.\n\n" +
      "\n".join(f"- {b['beat_id']}: {kind(b)} — {b['shot']['show'][0]['event']}" for b in beats))
t, rows = 0.0, []
for b in beats:
    d = b.get("actual_duration_s", b.get("estimated_duration_s", 0))
    rows.append(f"| {b['beat_id']} | {t:.2f}–{t + d:.2f} s | {b['shot']['show'][0]['event']} |")
    t += d
write("SHOTLIST.md", "# Shot list\n\nMeasured narration is the clock (Kokoro am_onyx). Captures play at their recorded 30 fps; a take shorter than its beat is replayed and labelled REPLAY on screen; still boards are held. The conformed timeline is written by the compiler.\n\n| Beat | Approximate span | Visible sequence |\n|---|---|---|\n" + "\n".join(rows))
write("PROMPTS.md", "# Prompts\n\nThe opening prompt is a suggested demonstration prompt (a reconstruction for the Walker bookend), not a transcript of the sessions that built A7 (those are in the game's prompts/ and sessions/). The Your Turn prompt is a bounded viewer exercise.\n\n" +
      "\n\n".join(b["shot"]["remotion"]["props"]["command"] for b in beats if b["shot"].get("remotion", {}).get("pattern") == "ClaudeComposerAsk"))
write("FACTCHECK.md", f"""# Fact check

Every number spoken or shown was checked against the files below at commit `{head}` (working-tree hashes in gamedev-evidence.json).

- npc_idle (animations/npc_idle.tscn 5–21, 28–40): length 1.33333, loop_mode 1 (LOOP_LINEAR), step 0.0833333, one value track `.:frame`, interp 0, keys at 0 / 0.333333 / 0.666667 / 1 with values 0–3, update 1 (discrete); NpcIdle Sprite3D hframes 4 (vframes default 1), texture npc_closure_idle.png (256×64); AnimationPlayer callback_mode_process 1 (IDLE), autoplay idle.
- track_problems (tests/a7_readback.gd 36–38): the ordinary-track branch `sub in node`; bone and blend-shape branches above it.
- Mutations (logs/a7_mutations/): m1 "FAIL  track_problems is empty  (wave_release track 4: ArmFront has no property rotaton)", RESULT exit=1; m2 FAIL loop_mode (0), exit=1; m3 FAIL key 3 inside the sheet (4), exit=1; m4 both exit=0.
- One authority: world/continuous_world_map.gd 2719–2729 (the seeded draw kept as `phase`, then `clip.seek(...)`); entities/player.gd 362–376 (`_wave_begin` writes Billboard.visible, Rig.scale.x, the sprite's visible). Structure test S7 squad phases [0.3333325, 0.3333325, 0.666665] (logs/test_wave_state_machine_60fps.log) — not all equal, two coincide.
- Two clocks: entities/player.gd 380–388 (`_tick_wave`: advance(delta × rate), wave_frame from _wave_time); D4 lines: r=1 → 12/20/40 unfrozen ticks (16/24/44 with 4 frozen); r=1.5 → 8/14/27 (12/18/31); "every wave tick: clip position == state machine time" PASS at both rates; tolerance 1e-4 s (tests/test_wave_state_machine.gd).
- Phase table (CHANGE-BRIEF.md 155–164): 30 fps, startup 6, active 4, recovery 10; rig keys (animations/lappland_wave_rig.tscn 108–116, ArmBack:rotation) at 0, 0.2, 0.333333, 0.666667, transitions 2 / 1 / 0.5 / 1 (the narration's "transition two eases into the sweep, point five eases out" refers to the first and third), values 0, −0.7, 1.4, 0.
- State table: entities/player.gd 318–331 (WAVE_CLIPS, WAVE_TRANSITIONS 6/10/20).
- r0 strip (the user's capture, captures/wave_release/r0): 27 click, 29 first STARTUP, 36/37 f5/f6 (charge mark gone on 37), 40/41 f9/f10, 49/50 end (TUNING.md). User's words quoted verbatim from TUNING.md.
- Edges (tests/test_wave_edges.gd 198–203; log): 39 passed / 0 failed; f5 no wave, charge 3; f6 wave +1, charge 0; spawn tick position 0.200000.
- Scripted dodges (capture/wave_dodges/capture.log): take 2 dodge at frame 120 in STARTUP → READY at 121, waves 0, charge 3; take 3 dodge at 213 on the first ACTIVE frame → wave out, charge 0; take 4 dodge at 308 in RECOVERY (wave_frame 13) → READY at 309.
- Suites: npc read-back PASS (55), rig read-back PASS (136), pins 11/5 after wiring and 16/0 re-pinned, structure 51/0, edges 39/0; baseline 93 of 103 before, 99 of 108 after (logs/baseline-*/summary.txt).
- Human checks quoted from evidence/a7/human-checks.md and TUNING.md ("All fine", "Reads well", the translated interrupt and contrast reports, "I saw the record. everything is nice, we did a good job.", "Keep r0, no revision").
- Provenance: gpt sol 6.1 (CHANGE-BRIEF r7, animations/ATTRIBUTION.md); terms not supplied.
- Not claimed: human play footage, fun, legibility for players in general, the untested interrupt paths (death, stuns, operator swap, leaving mid-release), edges at r > 1.
""")
write("SOURCES.md", f"""# Film sources

Game: Downfall (walker-downfall), Godot 4.7.2-stable, Forward+ / D3D12, RTX 4060 Laptop GPU. Filmed from git commit `{head}`; game source unchanged since `45cf5845` (TEST-REPORT.md). The ledger hashes the working tree (gamedev-evidence.json source_revision).

## Code shown
Exact excerpts listed in gamedev-evidence.json (path, lines, text). Editor views are Godot editor reconstructions (GodotDevWorkbench), not screen recordings.

## Existing engine evidence (same build, hashed in the ledger)
- The user's FIXTURE capture: captures/wave_release/r0/ frames 27, 29, 36, 37, 40, 41, 49, 50 (previews/wave_release_preview.tscn, Movie Maker, 30 fps, run by the user).
- Logs: logs/*.log, logs/a7_mutations/, logs/baseline-*/summary.txt.
- Images: art/characters/npc/npc_closure_idle.png and animations/lappland_rig/*.png (the actual files, enlarged nearest-neighbour).

## New captures for this film (capture/; commands, logs and source hashes beside the frames)
All windowed Godot 4.7.2 Movie Maker, `--fixed-fps 30`, 1280×720, run by tools/run_captures.sh. No game code, test or A7 document was edited.
- capture/wave_dodges (B20; log lines on B12): previews/film_wave_dodges.tscn, a film fixture written for this film — SCRIPTED-INPUT capture, not human play: real main.tscn and loop, a real click on a still stand-in enemy and real "dash" action events timed by reading the player's state; between takes a real ground click walks her back, and the fixture refills the charge and resets cooldowns and stamina (labelled). The first two runs were discarded: a parse error, then a take where the target lock let her auto-attack into a second release before take 2.
- capture/npc_in_game (B04, B06, B10): previews/npc_idle_in_game.tscn (an A7 review fixture) — the player is placed for framing; frames 40–370 base store, 400–760 the field squad. Cell changes measured by frame differencing every 10 capture frames (capture/npc_ranges.json).
- capture/rig_turntable (B16): previews/wave_rig_turntable.tscn — the rig alone on a grey plane, advanced 1/30 s per frame from capture frame 10.
Enlargements use nearest neighbour and are labelled with their factor. Takes shorter than their beat are replayed and labelled REPLAY. Nothing is retimed.

## Sheet and rig art
Fan art generated with gpt sol 6.1 (the user's statement); terms, date checked and prompts were not supplied (animations/ATTRIBUTION.md).

## Toolkit, voice, music
Brutalist toolkit (local brutalist.art): godot-gamedev skill, walker modifier; ai-explainer chassis; riff. Voice: local Kokoro am_onyx (Liam, in for Bear), not a clone. Outro: locked ClaudeTitleOutro with the toolkit's stock jingle (outro-audio.json). No paid calls, no Higgsfield, no captions.
""")
write("RIFF.md", """# Evidence-led commentary

| Artifact + range | Visible observation | Interpretation / limit | Next experiment |
|---|---|---|---|
| capture/npc_in_game 40–370 (B04, B06) | Closure changes cell every 10 frames, no hitch at the wrap | Matches the key spacing (1/3 s); one fixture run | Five-wrap seam check by the user (done in the game: "All fine") |
| capture/npc_in_game 400–760 (B10) | the three squad figures do not all breathe together | The seek-once rule works on this floor; two of three phases coincide (S7: 1/3, 1/3, 2/3) | Seed with more spread if visible in step |
| logs/a7_mutations (B08) | m1–m3 exit 1 with the right line; m4 passes | The read-back catches a misnamed track the engine would play silently | — |
| r0 frames 27/29/49/50 + wave_dodges log (B12) | sprite ↔ rig swap at the phase edges | One authority over the sprite's visible; no blank frame seen | — |
| test_wave_state_machine log (B14) | clip position = state time every tick, both rates | Clocks agree headlessly; says nothing about the look | — |
| capture/rig_turntable (B16) | wind-up, sweep, settle over 20 frames | Motion is small at 1× zoom; the lean is 2–3 px | Larger lean on the f6 key, prediction first |
| r0 strip (B18) | boundaries 29/37/41/50; the click's big hit flash on 29 | Claude's reading only: the startup may read as "already hit"; the user kept r0 | A readable wind-up (the Your Turn) |
| capture/wave_dodges (B20) | startup dodge keeps the charge; active/recovery dodges after the wave | The edge rule holds in one scripted run | Human play with stuns and death mid-release |

Observations are separated from source explanations. No claim about fun, fairness or accessibility follows from these captures.
""")
write("CHECKS-REPORT.md", f"""# Teaching checks

{len(beats)} beats: 9 code beats each followed immediately by its real result; 3 further evidence boards (overview, tests, human checks and credits); 5 bookend beats. 0 PUNT.

Teaching arc: FRAMEWORK ✓ (the four ideas: keys, one authority, two clocks, frames) | WORKED EXAMPLE ✓ (npc_idle and wave_release, each code → result) | FALSIFIABILITY ✓ (mutations, edges, a pin the agent failed to mark) | SCAFFOLDED TASK ✓ (Your Turn: one number in the phase table, prediction first, the human's verdict) | BOOKENDS ✓ (composer → hesitant writer → body → verdict → Your Turn → locked outro) | NO-SOURCE-NO-VERDICT ✓ (every verdict quoted from TUNING / human-checks / TEST-REPORT).
""")
write("BUILD-PROMPT.md", """# Rebuild the A7 film

Use the delivered A7 project and the local Brutalist toolkit. Preserve the game and the A6 film. Set PYTHONUTF8=1 and use the interpreter with kokoro-onnx (python3). Never publish; no paid calls.

1. Re-read CHANGE-BRIEF (Revisions), TUNING, TEST-REPORT, FRICTIONAL, evidence/a7/human-checks.md. Recheck excerpt line ranges in tools/film.py.
2. `python3 tools/film.py author` (resets measured fields) — only for a new build.
3. `python3 runtime/scripts/generate_audio_kokoro.py REEL` (am_onyx), then `python3 tools/attach_outro.py`.
4. If capture/ is missing: `tools/run_captures.sh wave_dodges npc_in_game rig_turntable` (windowed Movie Maker, 30 fps).
5. `python3 tools/make_media.py`, then look at frames of every media/BXX.mp4.
6. `python3 runtime/scripts/remotion_scenes.py REEL --only B03` (pilot, inspect), then all.
7. `python3 tools/write_records.py`; `python3 tools/film.py ledger`; `./art godot-gamedev --check REEL --game GAME`.
8. `./art final REEL --height 2160 --fps 30 --out REEL/exports/landscape`.
9. `python3 tools/review_film.py`; inspect _qc frames; record in _qc/REPORT.md. Refresh the ledger and rerun the checker.
""")
write("BUILD-LOG.md", """# Build log

- Captures: film_wave_dodges first failed to parse (a member named `ready` clashed with Node.ready); the second run was unusable (her target lock auto-attacked into a release before take 2, so take 2's "startup dodge" landed in that one); the third run ends each take with a real ground click, which walks her back and drops the lock, and removes the teleport. Only the third run is used.
- Pilot B03 (GodotDevWorkbench) showed 11 of 17 lines at 30 px: the keys were cut off. Every code beat was resized to fit and three excerpts trimmed to their teaching lines (B03 7–20, B13 380–388, B17 318–331); the beat sheet props were patched in place to keep the measured audio.
- B12 narration said "frame twenty eight"; the committed r0 frames are 27 and 29, so it was corrected and that beat's audio regenerated.
- Media boards: B08's m3 line first matched a PASS line (fixed to the key-3 FAIL); B02's transparent sheet was composited on paper; text sizes raised on B02/B14/B21/B22; B20's crop re-centred on Lappland.
- The first master (13:32) kept "A clip is a movie." on B01: the hesitant writer matches single words, so the two-word trigger "a movie" never fired. Changed to "movie" → "list of keys"; B01 re-rendered with --force (remotion_scenes skips filled beats without it) and the master re-exported. That export was refused by Gate V (1 MAJOR: B01 underfill, 52% of the safe area at mid-beat, min 55%); B01 fontSize 88 → 100 and re-exported.
- remotion_scenes.py updates the toolkit's gitignored runtime/remotion/_bench/consumers.json index; no other toolkit file was changed.
""")
print("records written; commit", head)
