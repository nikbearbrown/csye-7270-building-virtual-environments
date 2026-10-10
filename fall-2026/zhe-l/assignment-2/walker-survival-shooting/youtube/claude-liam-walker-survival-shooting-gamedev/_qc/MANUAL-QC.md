# Manual QC — final export

- File: `claude-liam-walker-survival-shooting-gamedev.mp4` (not in GitHub), 3840x2160, 30 fps, H.264 + AAC 48 kHz,
  413.37 s, SHA-256 `2cde5517c1f96affd17101d9ba1718bc7b689fcc60cdaa16cec5b9c991123e0a` (matches `.verified.json`, status `ready`).
- Gate V (`_qc/REPORT.md`): 42 frames, 0 BLOCKER, 0 MAJOR. GATE T (`TYPECHECK.md`): PASS.
- Frames inspected by Claude at 15/50/85 % of every beat (contact sheets in `_qc/`), and six frames of the final file.
- Audio measured in the final file: B09 lead 0.8 s silence; power on max -14.2 dB, power off -16.3 dB, button -8.9 dB
  (same as the source FLACs: no processing); outro voice then 1.0 s silence (no jingle).
- Defects found and fixed during the build: B08 right column overflow; B05/B15/B16 table type too small; B10 tree and
  B11 code clipped; B13 notes clipped; dense-mode titles wrapping; GATE T false positives on serif section headings;
  Gate V edge-bleed from the components' handle offset (toolkit fix, see SOURCES.md); jumbled pan frames (recaptured).
- Remaining minor issues (not blocking): B11 shows line 81 half cut at the panel bottom (line 80, the key line, is
  fully visible); the Verdict card (B18) leaves the lower page empty, as the stock component does.
- Not checked by a human yet: Claude cannot listen. The designer must watch and listen to the whole film.
