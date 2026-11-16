# BUILD-LOG - Key Terms: Game AI, Perception and Pathfinding

Built end to end by Claude Code with `exam-prep-deck-films/tools/build_film.py` (Bear asked for the CSYE 7270 Key Terms films, 2026-11-13).

## 2026-11-13 21:08 - stages: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks

`python3 make_film.py 19 ...` exit 0, 15 s
- claude-liam-lecture-key-terms-game-ai-perception-and-pathfinding: 58 beats (52 deck steps), 0 already voiced, about 23.6 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
- factcheck_check.py exit 0 (0 clean, 1 advisories, 2 blocker)
`python3 generate_audio_kokoro.py claude-liam-lecture-key-terms-game-ai-perception-and-pathfinding --only ...` exit 0, 212 s
- voiced 58 beat(s); all 58 beats have audio, 1025.0 s
`python3 pad_audio.py claude-liam-lecture-key-terms-game-ai-perception-and-pathfinding ...` exit 0, 5 s
- pad_audio: 15 beat(s) padded; total 1030.6 s
`python3 whisper_check.py claude-liam-lecture-key-terms-game-ai-perception-and-pathfinding ...` exit 0, 72 s
- whisper: 58 beats, 0 flagged, lowest 0.88
`python3 make_film.py 19 ...` exit 0, 16 s
- claude-liam-lecture-key-terms-game-ai-perception-and-pathfinding: 58 beats (52 deck steps), 58 already voiced, about 17.2 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
`python3 bookends.py claude-liam-lecture-key-terms-game-ai-perception-and-pathfinding ...` exit 0, 48 s
- bookends: BOPEN: 1 drawn frames, 15.58 s; BIDEA: 320 drawn frames, 18.25 s; BDEFS: 539 drawn frames, 25.38 s; BVDT: 456 drawn frames, 22.42 s; BHTF: 430 drawn frames, 18.96 s; BOUT: 1 drawn frames, 5.04 s; portrait: /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/professor-bear/professor-bear-1x1-159.jpg
`python3 deck_capture.py claude-liam-lecture-key-terms-game-ai-perception-and-pathfinding ...` exit 0, 257 s
- captured 52 deck beats into /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-game-ai-perception-and-pathfinding/media
`art run claude-liam-lecture-key-terms-game-ai-perception-and-pathfinding --height ...` exit 0, 432 s
- [run] GATE L — beat-mix lint
- [run] GATE SHAPE — finance chart-shape enforcement
- [run] GATE V — frame-level visual QC on the compiled reel
- [gate-v] frames=116 BLOCKER=0 MAJOR=0 → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-game-ai-perception-and-pathfinding/_qc/REPORT.md
- [run] done → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-game-ai-perception-and-pathfinding  (QC gates: on)
`art final claude-liam-lecture-key-terms-game-ai-perception-and-pathfinding --local ...` exit 0, 285 s
- [typecheck] §8.10 B1405: SKIP
- [typecheck] §8.10 B1406: SKIP
- [typecheck] §8.10 BVDT: SKIP
- [typecheck] §8.10 BHTF: SKIP
- [typecheck] §8.10 BOUT: SKIP
- [typecheck] GATE T: PASS
- [typecheck] (Gate T is the type-size check: it measures the smallest text in each beat of the finished film and fails any beat whose text is too small to read on a screen. TYPECHECK.md lists which beats and why.)
- [art] motion histogram: screen:52  graphic:6
- [art] SKIN LINT: NO RENDERABLE BEATS: no beat carries a shot.remotion.pattern or Manim annotation — the pipeline will render NOTHING and every slot becomes a YOU-slate. The sheet was authored without the scene contract.
- [art] build stamp → beat_sheet.json (58/58 filled)
- [art] wrote /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-game-ai-perception-and-pathfinding/exports/landscape/claude-liam-lecture-key-terms-game-ai-perception-and-pathfinding.mp4  (1031.6s, audio: per-beat timeline (s
- [art] slots: 58/58 filled — BOPEN:VIDEO BIDEA:VIDEO BDEFS:VIDEO B0101:VIDEO B0102:VIDEO B0103:VIDEO B0104:VIDEO B0201:VIDEO B0202:VIDEO B0203:VIDEO B0204:VIDEO B0301:VIDEO B0302:VIDEO B0303:VIDEO B0401:VIDEO B0402:VIDEO B0403:VIDEO B0404:VIDEO B0501:VIDEO B0502:VIDEO B0601:VIDEO B0602:VIDEO B0603:VI
- bookend structure (Northeastern bookends; toolkit bookend_check not applicable): PASS
- loudness_check exit 0: [loud] checking 58 beats for per-beat silence … | [loud] PASS  -24.58 LUFS  tp=-2.87 dBTP
- master /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-game-ai-perception-and-pathfinding/exports/landscape/claude-liam-lecture-key-terms-game-ai-perception-and-pathfinding.mp4: 3840x2160 at 24/1, 1031.62 s (17.2 min); sum of audio 1030.57 s; difference +1.06 s; 70 MB
- stages done: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks
