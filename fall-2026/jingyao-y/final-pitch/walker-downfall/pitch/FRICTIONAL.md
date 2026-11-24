# FRICTIONAL — pitch film log

## 2026-11-23

- **The assignment assumes a project that has not started.** About 80% of this game is already built. Decision (author): pitch what it is, what exists and what is left, instead of following the five-day template beat for beat.
- **Outline revisions (author's calls):**
  - Risk is framed only as "the system is big and needs more time to verify and balance".
  - The remaining work is music, cross-system optimisation and bug testing.
  - "Out" lists only multiplayer.
  - A separate "first playable piece" section was dropped. The core loop already runs and the film opens on it.
- **First narration draft was too long.** It was 729 words, about 4:50, over the 4-minute limit. It was cut to 475 words, then silence was padded under the capture beats, for 3:20 in total.
- **Profiling claim.** The Vulkan → D3D12 mine figure (~9 → ~150 fps on an RTX 4060 Laptop) was measured on 2026-10-24, but no log was committed. The film says it was "measured once" and that the log will be committed.
- **Isolating the capture.** The clone's `config/name` was changed so that the capture's `user://` (save slots, settings) cannot touch the real game's saves.
- **Exit crash during capture.** Every Movie Maker run segfaulted at exit (exit 139), after the log was written and the AVI was finalised. This is the known static-cache crash at exit. Not fixed here; noted in CAPTURE.md.
- **First takes that failed:**
  - `mine`: the driver kept fighting for 75 s and never reached the descent, so no route map. A separate `route` clip was added, with a logged teleport beside the marker.
  - `camp`: E opened a nearby weapon crate, not the beacon. The script fell back to `camp_extract()`, which is what the beacon calls. This is logged and labelled on screen.
  - `bridge`, take 1: the walk target was computed across the bridge, so she stood still. Take 2: the bridge's `a`/`b` fields are link indices, not points, and the script errored. Take 3: walking along `dir` through `centre` worked.
- **Watermarked clips.** The A5–A7 film clips carry the old @NikBearBrown watermark, and the assignment forbids the instructor's handle. B06 was rebuilt from the raw captures and evidence stills instead.
- **Gate V failed twice:**
  - First run: 28 BLOCKER. The full-width "CONSTRUCTED" banner crossed the title-safe area, and full-frame gameplay was flagged as edge-bleed and low contrast. Fixes: the banner was moved inside the safe area; capture beats now declare `qc.full_bleed`, with contrast measured on their label strip and a written reason.
  - Second run: 2 MAJOR, an underfilled end card. A frame and larger type fixed it.
  - Final: 0 BLOCKER, 0 MAJOR.
- **Name on screen.** The end card first showed a full name. It was changed to "Jingyao Y", matching the course repository's public name.
- **A5 still removed from B06 (author's call).** B06 now shows only the A6 particle frames and the A7 sword-wave frames. The A5 fire is still named in the narration, and its evidence is the B10 pixel claim. Re-compiled; Gate V is 0 BLOCKER, 0 MAJOR. New SHA-256 in README.
- **B06 narration changed (author's call).** "the fire shader" was cut, so the line now names only what is on screen: "the GPU particles and the animation rigs". Only B06 was regenerated with Kokoro, then padded with 6 s of silence as before. Film is now 199.6 s; Gate V 0 BLOCKER, 0 MAJOR.
- **Film uploaded by the author:** https://youtu.be/waHo7Zp4W48 (linked in README).
- **Still open:**
  - Copy `pitch/` into the walker repository, commit, and tag `a8`.
