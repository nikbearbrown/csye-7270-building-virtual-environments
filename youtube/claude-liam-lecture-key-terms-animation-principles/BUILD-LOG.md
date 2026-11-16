# BUILD-LOG - Key Terms: Animation Principles

Built end to end by Claude Code with `exam-prep-deck-films/tools/build_film.py` (Bear asked for the CSYE 7270 Key Terms films, 2026-11-13).

## 2026-11-13 20:17 - stages: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks

`python3 make_film.py 15 ...` exit 0, 2 s
- claude-liam-lecture-key-terms-animation-principles: 61 beats (55 deck steps), 0 already voiced, about 25.4 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
- factcheck_check.py exit 0 (0 clean, 1 advisories, 2 blocker)
`python3 generate_audio_kokoro.py claude-liam-lecture-key-terms-animation-principles --only ...` exit 0, 271 s
- voiced 61 beat(s); all 61 beats have audio, 1061.0 s
`python3 pad_audio.py claude-liam-lecture-key-terms-animation-principles ...` exit 0, 5 s
- pad_audio: 16 beat(s) padded; total 1067.2 s
`python3 whisper_check.py claude-liam-lecture-key-terms-animation-principles ...` exit 0, 104 s
- whisper: 61 beats, 0 flagged, lowest 0.88
`python3 make_film.py 15 ...` exit 0, 3 s
- claude-liam-lecture-key-terms-animation-principles: 61 beats (55 deck steps), 61 already voiced, about 17.8 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
`python3 bookends.py claude-liam-lecture-key-terms-animation-principles ...` exit 0, 70 s
- bookends: BOPEN: 1 drawn frames, 14.58 s; BIDEA: 291 drawn frames, 18.29 s; BDEFS: 780 drawn frames, 35.50 s; BVDT: 456 drawn frames, 22.75 s; BHTF: 435 drawn frames, 19.21 s; BOUT: 1 drawn frames, 4.29 s; portrait: /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/professor-bear/professor-bear-1x1-175.jpg
`python3 deck_capture.py claude-liam-lecture-key-terms-animation-principles ...` exit 0, 292 s
- captured 55 deck beats into /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-animation-principles/media
`art run claude-liam-lecture-key-terms-animation-principles --height ...` exit 0, 536 s
- [run] GATE L — beat-mix lint
- [run] GATE SHAPE — finance chart-shape enforcement
- [run] GATE V — frame-level visual QC on the compiled reel
- [gate-v] frames=122 BLOCKER=0 MAJOR=0 → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-animation-principles/_qc/REPORT.md
- [run] done → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-animation-principles  (QC gates: on)
`art final claude-liam-lecture-key-terms-animation-principles --local ...` exit 0, 268 s
- [typecheck] §8.10 B1505: SKIP
- [typecheck] §8.10 B1506: SKIP
- [typecheck] §8.10 BVDT: SKIP
- [typecheck] §8.10 BHTF: SKIP
- [typecheck] §8.10 BOUT: SKIP
- [typecheck] GATE T: PASS
- [typecheck] (Gate T is the type-size check: it measures the smallest text in each beat of the finished film and fails any beat whose text is too small to read on a screen. TYPECHECK.md lists which beats and why.)
- [art] motion histogram: screen:55  graphic:6
- [art] SKIN LINT: NO RENDERABLE BEATS: no beat carries a shot.remotion.pattern or Manim annotation — the pipeline will render NOTHING and every slot becomes a YOU-slate. The sheet was authored without the scene contract.
- [art] build stamp → beat_sheet.json (61/61 filled)
- [art] wrote /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-animation-principles/exports/landscape/claude-liam-lecture-key-terms-animation-principles.mp4  (1068.3s, audio: per-beat timeline (source audio preserved), draw
- [art] slots: 61/61 filled — BOPEN:VIDEO BIDEA:VIDEO BDEFS:VIDEO B0101:VIDEO B0102:VIDEO B0103:VIDEO B0104:VIDEO B0201:VIDEO B0202:VIDEO B0203:VIDEO B0204:VIDEO B0301:VIDEO B0302:VIDEO B0303:VIDEO B0401:VIDEO B0402:VIDEO B0403:VIDEO B0501:VIDEO B0502:VIDEO B0503:VIDEO B0504:VIDEO B0601:VIDEO B0602:VI
- bookend structure (Northeastern bookends; toolkit bookend_check not applicable): PASS
- loudness_check exit 0: [loud] checking 61 beats for per-beat silence … | [loud] PASS  -24.46 LUFS  tp=-2.75 dBTP
- master /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-animation-principles/exports/landscape/claude-liam-lecture-key-terms-animation-principles.mp4: 3840x2160 at 24/1, 1068.29 s (17.8 min); sum of audio 1067.15 s; difference +1.14 s; 72 MB
- stages done: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks
