# COMPONENTS.md

Components this film explains. They are hashed in `gamedev-evidence.json` against a pristine clone of `111bf6e`.

| Component | Beats | What enters → what changes → what the player sees/hears | Trade-off |
|---|---|---|---|
| `lappland-states` | B03 → B04 | Facing and action → `LapplandAnimator3D` picks a row (5 drawn, 3 mirrored) and a column range from `ACTIONS` → a different generated atlas cell on screen. | No blending. States read instantly, but SW ≈ S and the N frames barely differ (generated drift, open). |
| `warehouse-event-sounds` | B05 → B06, B07 | `RoomReveal` edge signals → `FieldAudio.play(cue)` → the generated light switch on each bank, and lights-off on exit. | Hatch and shelf are wired and counted but silent: their files were never generated. |
| `music-loops-and-stings` | B08 → B09, B10, B14 | `GameManager` state (base / field / pause / settle) → `GameMusic._switch`, `_set_paused`, `end_run` → base loop, field loop frozen on pause, one sting per run end. | One field track serves all three regions. Gemini ignored the BPM and bar counts in the prompts, so the cuts follow the measured structure. |
| `relic-icon-pipeline` | B11 → B12 | Brief row → gpt-image painting → `reduce_generated.py` (crop, nearest-neighbour to 64, 23 colours, outline) → `RelicIcons` → `AK.relic_icon` at whole multiples of 72. | Automatic reduction gives speckle (43% isolated pixels). The author accepted the look. |
| `fresh-clone-assets` | B13 → B14, B16 | `.gitignore` decides what a clone has → the `music/` rule removed `audio/music/` → silent camp. `/music/` restores it. | Ignore rules are global patterns, and a broad one silently drops runtime files. |
| `audio-tests` | B15 → B16 | Scripted warehouse walk → `FieldAudio.counts` → pass/fail per event, loop points, pause, stings, mute. | It teleports between rooms, so it proves counts, not feel or loudness. |
| `environments` | B02, B04, B06 | Generated surfaces and prop groups, plus the assembled Rhodes base, loaded by `FieldArt` / `BaseMap`. | Low-contrast ground keeps red warnings readable. There is no numeric contrast check. |
| `assignment-documents` | B01, B02, B17 | Retrospective design docs and the asset log. | Written after generation, and labelled so. |

Everything else in the snapshot is listed under `exclusions` with a reason (other gameplay systems, other art batches, the Chinese design docs).
