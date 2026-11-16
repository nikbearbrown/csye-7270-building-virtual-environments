# BUILD-LOG - Key Terms: Shader Foundations

Built end to end by Claude Code with `exam-prep-deck-films/tools/build_film.py` (Bear asked for the CSYE 7270 Key Terms films, 2026-11-13).

## 2026-11-13 19:31 - stages: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks

`python3 make_film.py 11 ...` exit 0, 2 s
- claude-liam-lecture-key-terms-shader-foundations: 59 beats (53 deck steps), 0 already voiced, about 25.3 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
- factcheck_check.py exit 0 (0 clean, 1 advisories, 2 blocker)
`python3 generate_audio_kokoro.py claude-liam-lecture-key-terms-shader-foundations --only ...` exit 0, 245 s
- voiced 59 beat(s); all 59 beats have audio, 1102.6 s
`python3 pad_audio.py claude-liam-lecture-key-terms-shader-foundations ...` exit 0, 5 s
- pad_audio: 16 beat(s) padded; total 1108.3 s
`python3 whisper_check.py claude-liam-lecture-key-terms-shader-foundations ...` exit 0, 51 s
- whisper: 59 beats, 1 flagged, lowest 0.84
`python3 make_film.py 11 ...` exit 0, 4 s
- claude-liam-lecture-key-terms-shader-foundations: 59 beats (53 deck steps), 59 already voiced, about 18.5 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
`python3 bookends.py claude-liam-lecture-key-terms-shader-foundations ...` exit 0, 50 s
- bookends: BOPEN: 1 drawn frames, 14.54 s; BIDEA: 311 drawn frames, 18.88 s; BDEFS: 703 drawn frames, 32.25 s; BVDT: 442 drawn frames, 21.75 s; BHTF: 437 drawn frames, 19.29 s; BOUT: 1 drawn frames, 4.12 s; portrait: /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/professor-bear/professor-bear-1x1-139.jpg
`python3 deck_capture.py claude-liam-lecture-key-terms-shader-foundations ...` exit 0, 261 s
- captured 53 deck beats into /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-shader-foundations/media
`art run claude-liam-lecture-key-terms-shader-foundations --height ...` exit 0, 463 s
- [run] GATE L — beat-mix lint
- [run] GATE SHAPE — finance chart-shape enforcement
- [run] GATE V — frame-level visual QC on the compiled reel
- [gate-v] frames=118 BLOCKER=0 MAJOR=0 → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-shader-foundations/_qc/REPORT.md
- [run] done → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-shader-foundations  (QC gates: on)
`art final claude-liam-lecture-key-terms-shader-foundations --local ...` exit 0, 306 s
- [typecheck] §8.10 B1505: SKIP
- [typecheck] §8.10 B1506: SKIP
- [typecheck] §8.10 BVDT: SKIP
- [typecheck] §8.10 BHTF: SKIP
- [typecheck] §8.10 BOUT: SKIP
- [typecheck] GATE T: PASS
- [typecheck] (Gate T is the type-size check: it measures the smallest text in each beat of the finished film and fails any beat whose text is too small to read on a screen. TYPECHECK.md lists which beats and why.)
- [art] motion histogram: screen:53  graphic:6
- [art] SKIN LINT: NO RENDERABLE BEATS: no beat carries a shot.remotion.pattern or Manim annotation — the pipeline will render NOTHING and every slot becomes a YOU-slate. The sheet was authored without the scene contract.
- [art] build stamp → beat_sheet.json (59/59 filled)
- [art] wrote /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-shader-foundations/exports/landscape/claude-liam-lecture-key-terms-shader-foundations.mp4  (1109.6s, audio: per-beat timeline (source audio preserved), drawtext
- [art] slots: 59/59 filled — BOPEN:VIDEO BIDEA:VIDEO BDEFS:VIDEO B0101:VIDEO B0102:VIDEO B0103:VIDEO B0104:VIDEO B0201:VIDEO B0202:VIDEO B0203:VIDEO B0301:VIDEO B0302:VIDEO B0303:VIDEO B0304:VIDEO B0401:VIDEO B0402:VIDEO B0403:VIDEO B0501:VIDEO B0502:VIDEO B0503:VIDEO B0601:VIDEO B0602:VIDEO B0603:VI
- bookend structure (Northeastern bookends; toolkit bookend_check not applicable): PASS
- loudness_check exit 0: [loud] checking 59 beats for per-beat silence … | [loud] PASS  -24.54 LUFS  tp=-2.65 dBTP
- master /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-shader-foundations/exports/landscape/claude-liam-lecture-key-terms-shader-foundations.mp4: 3840x2160 at 24/1, 1109.58 s (18.5 min); sum of audio 1108.35 s; difference +1.23 s; 74 MB
- stages done: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks
