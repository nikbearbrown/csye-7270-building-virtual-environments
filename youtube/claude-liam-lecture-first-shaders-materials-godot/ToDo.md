# ToDo — claude-liam-lecture-first-shaders-materials-godot

What this is: the list of things that wait for Bear, and the one list of what the build session does. Why: nothing in this film waits for a human-supplied file (every picture is machine-made from real captures or drawn), but a few decisions change the narration, and the build session may not change the narration.
Found: layout stage done 2026-10-16; nothing voiced, rendered, staged or published.
Note: `./brutalist.art/art todo` rewrites this file from the beat ledger. Run before BOPEN's card exists it wrongly lists BOPEN as "1 slot(s) need YOU" (BOPEN is built by the title-card builder, BUILD-PROMPT step 4; nobody supplies it). The same decisions are kept in `BUILD-LOG.md` (Open items) so a regenerated ToDo.md loses nothing.

0 slot(s) need YOU for a file. The next step is the build session (see BUILD-PROMPT.md): audio, stills check, review cut, 4K master, gates.

## Decide BEFORE the build (each one changes the narration, so it cannot be done during the build)
1. **Length.** Estimated 957 s (about 16 min at 3.2 words per second); your target was 10 to 14 minutes. The assignment is 46 KB (the sibling's was 28 KB, a 13.4-minute film). Cheapest cuts, by estimated seconds, and what each costs:
   - B57 more recorded mistakes, 13 s (the Ag X enum, the ignored import key, the ambient-occlusion pass; B56 keeps the "agent gets it wrong" idea)
   - B46 the code-made normal map, 14 s (loses "a Sobel-filtered picture passes; curl-free means a surface exists, not the right one"; B44-B45 keep the curl check and the calibration)
   - B55B the "done means" list, 15 s
   - B70 what goes on GitHub, 17 s (loses the exclusions and the tag; B71 keeps the clean-clone verification)
   - B65 in play, 9 s and B66 the interface sweep, 10 s: these two are assignment requirements (your own playtest, a sweep of every uniform), so cutting them means the film stops mentioning them
   The first three save about 42 s (to roughly 15.2 minutes); all six together are about 78 s and bring it to roughly 14.6 minutes. Anything beyond that cuts more of the assignment. Tell me which to drop, or keep all of it, and I will edit `narration.py`, `lanes/` and the sheet before the build.
2. **Series line on the title card.** BOPEN says "C S Y E seventy-two seventy, Virtual Environments" because the course's full title ("CSYE 7270 Virtual Environments and Real-Time 3D", 47 characters) does not fit the card's 42-character budget. Playlist at posting time: the sibling film's playlist name is "Virtual Environments and Real-Time 3D"; this film's `metadata.playlist` is the short form. Confirm the name before `art post`.
3. **Pronunciations to listen for** (the dictionary was not changed; phonemes were checked without audio): "Go-doe" (Godot), "Ag X" (the AgX tone mapper), "Aces", "Sobel", "U V", "S R G B", "G L S L", "Hallo" in BIDEA. Anything heard wrong goes to you, not into `brutalist.art/runtime/pronunciation/liam.json`.

## Decide any time (do not block the build)
4. **Poly Haven logo.** B08 and B45 name Poly Haven in text; there is no logo for it in `brutalist.art/icons/logos/`. Adding one needs a download from polyhaven.com and your yes.
5. **The `claude-code` logo and GATE T (B06, B07, B55).** The terracotta mark lands after the clip midpoint on purpose. If GATE T reads it as accent text, a toolkit exemption (`STRUCTURAL_TERRACOTTA_PATTERNS`) is yours to grant; the build will report it, not edit the toolkit.
6. **Lab frames are an earlier take (14 Oct 01:52, scripted input)**; the panel text differs from today's `verification.gd`. A fresh capture would need the editor-capture driver and the Lab lock. Keep as labelled, or ask for a fresh capture.
7. **Real Shader Editor strips.** B50 draws the generated shader's lines from the file's own text because the real dark strips fail GATE T at 4K. B49 carries the real editor frames. Say so if you want the real strips back at the cost of a GATE T exemption.
8. **Soft-wrapped code rows** (B19, B24, B38, B50, B53): the characters are verbatim; the continuation hook is a drawing convention. Say if you would rather have smaller type.
9. **Listen first.** Nobody has heard or seen any of it.

## For the build session (everything else)
- Follow `BUILD-PROMPT.md` exactly: voice, `prepare_audio.py`, `make_sheet.py`, `retime_cues.py`, Whisper check, title card, pace pass, stills, review cut, 4K master, every gate to PASS, `bookend_check.py`. Log every fix in `BUILD-LOG.md`.
- Re-check B63 and B64 at 85 % first (their last recorded 4K run is older than their last scene edit).
- Never publish, stage or commit.
