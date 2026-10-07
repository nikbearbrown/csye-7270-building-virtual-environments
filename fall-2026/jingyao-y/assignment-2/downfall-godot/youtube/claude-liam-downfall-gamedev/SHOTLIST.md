# SHOTLIST.md

| Beat | Act | Visual | Source |
|---|---|---|---|
| B00 | ASK | ClaudeComposerAsk: reconstructed Walker prompt | Remotion |
| B01 | BLUF | Hesitant writer: "Design first, then generate" → "Generated first, documented after" | Remotion |
| B02 | GAMEPLAY | Base hall walk with base music (narrated) | `hall` 1.0–27.1 s |
| B03 | MECHANISM | `lappland_animator_3d.gd:38-42`, the state → cell table | GodotDevWorkbench |
| B04 | RESULT | WASD facing turns, then combo against city enemies | `combat` 0.7–19.8 s |
| B05 | MECHANISM | `game_manager.gd:157-160`, signals → cues | GodotDevWorkbench |
| B06 | RESULT | Warehouse walk-in: banks light, racks rise | `warehouse` 2.0–18.4 s |
| B07 | SLICE AUDIO | The same walk, start to finish, game audio only, labelled | `warehouse` 2.0–34.9 s, `clock: source` |
| B08 | MECHANISM | `game_music.gd:70-82`, `end_run` | GodotDevWorkbench |
| B09 | RESULT | Esc pause and resume; floor 31 fight and death | `combat` 33.8–41.0 s + `death` 1.6–13.1 s (window ends 1.5 s after the settle frame) |
| B10 | SLICE AUDIO | Death and STING-FAIL over 行动失败, game audio only, labelled | `death` 12.1–24.9 s (from the settle frame), `clock: source` |
| B11 | MECHANISM | `reduce_generated.py:58-71` | GodotDevWorkbench |
| B12 | RESULT | Raw painting → 72 px icon → engine R window (still images, labelled) | `images/B12-asset-trace.png` |
| B13 | MECHANISM | `.gitignore` diff: `music/` → `/music/` | GitHubCodeDiff (real diff of 111bf6e) |
| B14 | RESULT | Camp with music, real click on 撤离, 行动结束 settlement | `extract` 0.7–11.2 s |
| B15 | MECHANISM | `test_audio.gd:66-78`, counting checks | GodotDevWorkbench |
| B16 | RESULT | Recorded `run_all.ps1` output from the fresh clones (still, labelled) | `images/B16-test-output.png` |
| B17 | VERDICT | Working / fixed / open / human playtest pending | ClaudeVerdictArtifact |
| B18 | HANDOFF | "Your turn" fresh-clone prompt | ClaudeComposerAsk |
| B19 | OUTRO | Locked title outro | ClaudeTitleOutro |
