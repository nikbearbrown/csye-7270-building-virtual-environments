# BUILD-LOG - Key Terms: Pacing and Guidance

Built end to end by Claude Code with `exam-prep-deck-films/tools/build_film.py` (Bear asked for the CSYE 7270 Key Terms films, 2026-11-13).

## 2026-11-13 18:19 - stages: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks

`python3 make_film.py 03 ...` exit 0, 0 s
- claude-liam-lecture-key-terms-pacing-and-guidance: 48 beats (42 deck steps), 0 already voiced, about 18.2 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
- factcheck_check.py exit 0 (0 clean, 1 advisories, 2 blocker)
`python3 generate_audio_kokoro.py claude-liam-lecture-key-terms-pacing-and-guidance --only ...` exit 0, 233 s
- voiced 48 beat(s); all 48 beats have audio, 787.6 s
`python3 pad_audio.py claude-liam-lecture-key-terms-pacing-and-guidance ...` exit 0, 3 s
- pad_audio: 15 beat(s) padded; total 792.8 s
`python3 whisper_check.py claude-liam-lecture-key-terms-pacing-and-guidance ...` exit 0, 43 s
- whisper: 48 beats, 0 flagged, lowest 0.89
`python3 make_film.py 03 ...` exit 0, 0 s
- claude-liam-lecture-key-terms-pacing-and-guidance: 48 beats (42 deck steps), 48 already voiced, about 13.2 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
`python3 bookends.py claude-liam-lecture-key-terms-pacing-and-guidance ...` exit 0, 77 s
- bookends: BOPEN: 1 drawn frames, 16.96 s; BIDEA: 309 drawn frames, 18.92 s; BDEFS: 582 drawn frames, 27.12 s; BVDT: 458 drawn frames, 22.62 s; BHTF: 457 drawn frames, 20.21 s; BOUT: 1 drawn frames, 4.17 s; portrait: /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/professor-bear/professor-bear-1x1-153.jpg
`python3 deck_capture.py claude-liam-lecture-key-terms-pacing-and-guidance ...` exit 0, 222 s
- captured 42 deck beats into /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-pacing-and-guidance/media
`art run claude-liam-lecture-key-terms-pacing-and-guidance --height ...` exit 0, 476 s
- [run] GATE L — beat-mix lint
- [run] GATE SHAPE — finance chart-shape enforcement
- [run] GATE V — frame-level visual QC on the compiled reel
- [gate-v] frames=96 BLOCKER=0 MAJOR=0 → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-pacing-and-guidance/_qc/REPORT.md
- [run] done → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-pacing-and-guidance  (QC gates: on)
`art final claude-liam-lecture-key-terms-pacing-and-guidance --local ...` exit 0, 285 s
- [typecheck] §8.10 B1405: SKIP
- [typecheck] §8.10 B1406: SKIP
- [typecheck] §8.10 BVDT: SKIP
- [typecheck] §8.10 BHTF: SKIP
- [typecheck] §8.10 BOUT: SKIP
- [typecheck] GATE T: PASS
- [typecheck] (Gate T is the type-size check: it measures the smallest text in each beat of the finished film and fails any beat whose text is too small to read on a screen. TYPECHECK.md lists which beats and why.)
- [art] motion histogram: screen:42  graphic:6
- [art] SKIN LINT: NO RENDERABLE BEATS: no beat carries a shot.remotion.pattern or Manim annotation — the pipeline will render NOTHING and every slot becomes a YOU-slate. The sheet was authored without the scene contract.
- [art] build stamp → beat_sheet.json (48/48 filled)
- [art] wrote /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-pacing-and-guidance/exports/landscape/claude-liam-lecture-key-terms-pacing-and-guidance.mp4  (793.8s, audio: per-beat timeline (source audio preserved), drawtex
- [art] slots: 48/48 filled — BOPEN:VIDEO BIDEA:VIDEO BDEFS:VIDEO B0101:VIDEO B0102:VIDEO B0103:VIDEO B0104:VIDEO B0201:VIDEO B0202:VIDEO B0203:VIDEO B0301:VIDEO B0302:VIDEO B0401:VIDEO B0402:VIDEO B0403:VIDEO B0501:VIDEO B0502:VIDEO B0601:VIDEO B0602:VIDEO B0701:VIDEO B0702:VIDEO B0801:VIDEO B0802:VI
- bookend structure (Northeastern bookends; toolkit bookend_check not applicable): PASS
- loudness_check exit 0: [loud] checking 48 beats for per-beat silence … | [loud] PASS  -24.53 LUFS  tp=-2.81 dBTP
- master /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-pacing-and-guidance/exports/landscape/claude-liam-lecture-key-terms-pacing-and-guidance.mp4: 3840x2160 at 24/1, 793.83 s (13.2 min); sum of audio 792.84 s; difference +0.99 s; 45 MB
- stages done: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks
