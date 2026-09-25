# Build log

- Read source and mapped course claims to five acts.
- Consulted scene library; reused four canonical bookends. No suitable existing course-specific mechanism scene found.
- Pantry search for walker jumpman godot found no relevant stock; unrelated Walker-name results rejected. Real project evidence selected instead.
- Authoring complete; audio and render pending.

## Production pass — September 10, 2026

- Generated and aligned 34 Liam narration beats locally; no paid voice or image
  generation. Timeline locked to 604.125 seconds at 24 fps, including the regular
  canonical outro jingle. Subtitle checker passed all 205 cues.
- Built 12 Manim mechanisms, 12 course-specific Remotion scenes, six archival
  image treatments, and the five bookends. All scene slots are native 4K.
- Read all nine scene contact sheets (105 samples). Repaired B05's arrow
  connections, enlarged authored footer text, and removed a clipped secondary
  text area from the composer bookends. Last label-size repair targets B16/B19;
  B21 uses the same corrected label style for consistency.
- The type checker originally treated terracotta borders as text and the
  unaltered game's inset UI as newly authored course labels. The reel-local
  adapter classifies structural accents and checks the designed evidence
  headings/footers separately from the archival inset. The full unmasked images
  remain in the contact sheets. No global thresholds were changed.
- Pre-assembly audio preservation passed on all 35 segments. The canonical
  MP3/AAC path contributes measured 21–27 ms priming/rounding, below one 24 fps
  frame. Waveform similarity is checked within a bounded 40 ms alignment window,
  not an unrestricted search that could hide a misplaced sentence.
- Source hashes match all six unchanged originals. Content, frame schema,
  bookend, fact/source and subtitle checks passed. The full first review cut is
  being compiled through the canonical pipeline. Final-master QC remains pending.

## Rebuilding

Do not rerun `scripts/author.cjs` over this existing reel. The authoritative
audio-locked source is `beat_sheet.json`. Use the reel-local adapter for changed
scene slots, `scripts/type-gate.py` for typography, and the sandbox's canonical
`runtime/scripts/compile.py` for review/final assembly. Run `scripts/qc.py`,
`scripts/sweep.py`, `scripts/verify-audio.py`, and the canonical master/loudness/
sharpness/subtitle gates before marking a new master ready. Publication of this
new course overview was subsequently authorized by the user for the CSYE 7270
Virtual Environments and Real-Time 3D playlist on @NikBearBrown.

## Clean-master verification

- Final typography pass: all 35 beats passed after B16/B19/B21 label and padding
  corrections. The old review cut is retained in `exports/review/`; the canonical
  compiler removed its superseded root copy.
- Canonical clean master: 3840×2160, 24 fps, H.264/yuv420p, 604.125 seconds.
  SHA-256: `a1994f2498d3203e870e5fa7801a6390267b4b2ed1fbaa4707afbaeccf1a959d`.
- Final soundtrack matches every one of the 35 source segments. The locked
  outro remains unchanged and has no narration. Loudness: -23.92 LUFS,
  -2.86 dBTP. Master and sharpness gates passed (median LV 350.9).
- Final visual gate passed all 70 sampled frames. The compiled-master sweep
  sampled 1,313 timestamps (1,099 unique decoded pixel frames); the assistant
  viewed all 46 contact pages and made native-frame spot checks. No unresolved
  defect found. The brief dark opening of the outro is its canonical 14-frame
  opacity ramp, verified in the locked component source and left unchanged.
- Hash-bound readiness is recorded in `_qc/publish-ready.json`. This is AI
  verification, not a fabricated human viewing or editorial sign-off. It does
  not claim exhaustive frame-by-frame inspection or complete listening.

## Publication — September 10, 2026 (America/New_York)

- Uploaded the hash-verified clean master privately, then uploaded the existing
  205-cue English SRT. YouTube processing succeeded; source stream was confirmed
  as 3840×2160 at 24 fps.
- Authenticated watch-page Settings showed `Auto (2160p 4K)` and the English
  caption track before publication. Evidence: `_qc/youtube-4k.json`.
- Published [the course film](https://www.youtube.com/watch?v=BGI2S3la5WM) as #1
  in the new public [CSYE 7270 Virtual Environments and Real-Time 3D playlist](https://www.youtube.com/playlist?list=PLMhsxBEsgHFU).
- The first playlist readback preceded YouTube's propagation; retained the
  confirmed playlist ID, then completed publication without creating another
  playlist or uploading another video. API readback confirmed public status and
  position; browser confirmed the playlist and its one video.
- Receipt: `books/youtube/nikbearbrown/claude-liam-csye-7270-virtual-environments/publish.json`
  relative to the shared books parent. Existing course and Walker playlists
  were preserved.
