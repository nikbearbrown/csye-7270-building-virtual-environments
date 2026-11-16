# BUILD-LOG - Key Terms: Shader Verification

Built end to end by Claude Code with `exam-prep-deck-films/tools/build_film.py` (Bear asked for the CSYE 7270 Key Terms films, 2026-11-13).

## 2026-11-13 19:54 - stages: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks

`python3 make_film.py 13 ...` exit 0, 0 s
- claude-liam-lecture-key-terms-shader-verification: 56 beats (50 deck steps), 0 already voiced, about 23.9 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
- factcheck_check.py exit 0 (0 clean, 1 advisories, 2 blocker)
`python3 generate_audio_kokoro.py claude-liam-lecture-key-terms-shader-verification --only ...` exit 0, 226 s
- voiced 56 beat(s); all 56 beats have audio, 1036.8 s
`python3 pad_audio.py claude-liam-lecture-key-terms-shader-verification ...` exit 0, 5 s
- pad_audio: 15 beat(s) padded; total 1042.9 s
`python3 whisper_check.py claude-liam-lecture-key-terms-shader-verification ...` exit 0, 72 s
- whisper: 56 beats, 0 flagged, lowest 0.86
`python3 make_film.py 13 ...` exit 0, 0 s
- claude-liam-lecture-key-terms-shader-verification: 56 beats (50 deck steps), 56 already voiced, about 17.4 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
`python3 bookends.py claude-liam-lecture-key-terms-shader-verification ...` exit 0, 53 s
- bookends: BOPEN: 1 drawn frames, 16.46 s; BIDEA: 290 drawn frames, 18.21 s; BDEFS: 573 drawn frames, 26.92 s; BVDT: 448 drawn frames, 22.00 s; BHTF: 494 drawn frames, 21.92 s; BOUT: 1 drawn frames, 4.29 s; portrait: /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/professor-bear/professor-bear-1x1-153.jpg
`python3 deck_capture.py claude-liam-lecture-key-terms-shader-verification ...` exit 0, 195 s
- captured 50 deck beats into /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-shader-verification/media
`art run claude-liam-lecture-key-terms-shader-verification --height ...` exit 0, 496 s
- [run] GATE L — beat-mix lint
- [run] GATE SHAPE — finance chart-shape enforcement
- [run] GATE V — frame-level visual QC on the compiled reel
- [gate-v] frames=112 BLOCKER=0 MAJOR=0 → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-shader-verification/_qc/REPORT.md
- [run] done → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-shader-verification  (QC gates: on)
`art final claude-liam-lecture-key-terms-shader-verification --local ...` exit 0, 276 s
- [typecheck] §8.10 B1305: SKIP
- [typecheck] §8.10 B1306: SKIP
- [typecheck] §8.10 BVDT: SKIP
- [typecheck] §8.10 BHTF: SKIP
- [typecheck] §8.10 BOUT: SKIP
- [typecheck] GATE T: PASS
- [typecheck] (Gate T is the type-size check: it measures the smallest text in each beat of the finished film and fails any beat whose text is too small to read on a screen. TYPECHECK.md lists which beats and why.)
- [art] motion histogram: screen:50  graphic:6
- [art] SKIN LINT: NO RENDERABLE BEATS: no beat carries a shot.remotion.pattern or Manim annotation — the pipeline will render NOTHING and every slot becomes a YOU-slate. The sheet was authored without the scene contract.
- [art] build stamp → beat_sheet.json (56/56 filled)
- [art] wrote /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-shader-verification/exports/landscape/claude-liam-lecture-key-terms-shader-verification.mp4  (1044.0s, audio: per-beat timeline (source audio preserved), drawte
- [art] slots: 56/56 filled — BOPEN:VIDEO BIDEA:VIDEO BDEFS:VIDEO B0101:VIDEO B0102:VIDEO B0103:VIDEO B0104:VIDEO B0201:VIDEO B0202:VIDEO B0203:VIDEO B0204:VIDEO B0301:VIDEO B0302:VIDEO B0401:VIDEO B0402:VIDEO B0403:VIDEO B0404:VIDEO B0501:VIDEO B0502:VIDEO B0503:VIDEO B0504:VIDEO B0601:VIDEO B0602:VI
- bookend structure (Northeastern bookends; toolkit bookend_check not applicable): PASS
- loudness_check exit 0: [loud] checking 56 beats for per-beat silence … | [loud] PASS  -24.45 LUFS  tp=-2.63 dBTP
- master /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-shader-verification/exports/landscape/claude-liam-lecture-key-terms-shader-verification.mp4: 3840x2160 at 24/1, 1044.00 s (17.4 min); sum of audio 1042.92 s; difference +1.08 s; 69 MB
- stages done: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks
