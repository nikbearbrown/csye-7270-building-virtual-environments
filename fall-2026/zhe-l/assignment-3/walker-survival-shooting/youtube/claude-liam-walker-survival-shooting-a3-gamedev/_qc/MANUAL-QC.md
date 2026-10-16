# Manual QC — final export

- File: `claude-liam-walker-survival-shooting-a3-gamedev.mp4` (not in GitHub), 3840x2160, 30 fps, H.264 + AAC 48 kHz,
  439.63 s, SHA-256 `84c0d77631bbb73c9f4c3ee07969f70d9846d52b2573bbe6173d110606f24f60`
  (matches `.verified.json`, status `ready`).
- Automated gates on the final: GATE T (`TYPECHECK.md`) PASS; Gate V on the review cut (`_qc/REPORT.md`):
  48 frames, 0 BLOCKER, 0 MAJOR; `./art final` decode and final-frame checks passed.
- Frames inspected by Claude at 15/50/85 % of every beat on the per-beat renders, before the final export
  (contact sheets `_qc/sheet_*.jpg`). The designer asked to skip Claude's frame check of the final MP4 itself;
  the designer watches and listens to the final export.
- Defects found and fixed during the build: workbench source notes rendered empty (wrong prop key); notes column
  clipped the fourth note (cut to three); B12 and B16 excerpts lost their last line at the panel bottom
  (ranges shortened); GATE T failures on B02 (lowercase-only heading runs), B14 (wordy output line),
  B11 / B17 / B18 (dark furniture lines in renders read as overlapping text: crops changed, B17 render removed);
  B11 then no longer showed the desk, so its narration and card were changed; B19 narration overclaim fixed;
  export to the in-reel folder failed on the Windows 260-character path limit and was re-run to a short folder.
- Not checked by a human yet: Claude cannot listen. The designer must watch and listen to the whole film.
