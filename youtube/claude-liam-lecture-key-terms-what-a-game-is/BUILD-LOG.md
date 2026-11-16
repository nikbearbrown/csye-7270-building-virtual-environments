# BUILD-LOG - Key Terms: What a Game Is

Built end to end by Claude Code with `exam-prep-deck-films/tools/build_film.py` (Bear asked for the CSYE 7270 Key Terms films, 2026-11-13).

## 2026-11-13 17:00 - stages: sheet, voice, pad, whisper

`python3 make_film.py 01 ...` exit 0, 0 s
- claude-liam-lecture-key-terms-what-a-game-is: 49 beats (43 deck steps), 0 already voiced, about 19.3 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
- factcheck_check.py exit 0 (0 clean, 1 advisories, 2 blocker)
`python3 generate_audio_kokoro.py claude-liam-lecture-key-terms-what-a-game-is --only ...` exit 0, 2348 s
- voiced 49 beat(s); all 49 beats have audio, 812.5 s
`python3 pad_audio.py claude-liam-lecture-key-terms-what-a-game-is ...` exit 0, 4 s
- pad_audio: 14 beat(s) padded; total 817.8 s
`python3 whisper_check.py claude-liam-lecture-key-terms-what-a-game-is ...` exit 0, 41 s
- whisper: 49 beats, 0 flagged, lowest 0.90
- stages done: sheet, voice, pad, whisper

## 2026-11-13 17:52 - stages: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks

`python3 make_film.py 01 ...` exit 0, 0 s
- claude-liam-lecture-key-terms-what-a-game-is: 49 beats (43 deck steps), 49 already voiced, about 13.6 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 7 s
- factcheck_check.py exit 0 (0 clean, 1 advisories, 2 blocker)
- voiced 0 beat(s); all 49 beats have audio, 817.8 s
`python3 pad_audio.py claude-liam-lecture-key-terms-what-a-game-is ...` exit 0, 16 s
- pad_audio: 0 beat(s) padded; total 817.8 s
`python3 whisper_check.py claude-liam-lecture-key-terms-what-a-game-is ...` exit 0, 459 s
- whisper: 49 beats, 0 flagged, lowest 0.90
`python3 make_film.py 01 ...` exit 0, 0 s
- claude-liam-lecture-key-terms-what-a-game-is: 49 beats (43 deck steps), 49 already voiced, about 13.6 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
`python3 bookends.py claude-liam-lecture-key-terms-what-a-game-is ...` exit 0, 63 s
- bookends: BOPEN: 1 drawn frames, 14.21 s; BIDEA: 299 drawn frames, 17.46 s; BDEFS: 672 drawn frames, 31.00 s; BVDT: 457 drawn frames, 22.46 s; BHTF: 442 drawn frames, 19.54 s; BOUT: 1 drawn frames, 3.75 s; portrait: /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/professor-bear/professor-bear-1x1-125.jpg
`python3 deck_capture.py claude-liam-lecture-key-terms-what-a-game-is ...` exit 0, 216 s
- captured 43 deck beats into /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-what-a-game-is/media
`art run claude-liam-lecture-key-terms-what-a-game-is --height ...` exit 0, 547 s
- [run] GATE L — beat-mix lint
- [run] GATE SHAPE — finance chart-shape enforcement
- [run] GATE V — frame-level visual QC on the compiled reel
- [gate-v] frames=98 BLOCKER=0 MAJOR=0 → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-what-a-game-is/_qc/REPORT.md
- [run] done → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-what-a-game-is  (QC gates: on)
`art final claude-liam-lecture-key-terms-what-a-game-is --local ...` exit 0, 365 s
- [typecheck] §8.10 B1305: SKIP
- [typecheck] §8.10 B1306: SKIP
- [typecheck] §8.10 BVDT: SKIP
- [typecheck] §8.10 BHTF: SKIP
- [typecheck] §8.10 BOUT: SKIP
- [typecheck] GATE T: PASS
- [typecheck] (Gate T is the type-size check: it measures the smallest text in each beat of the finished film and fails any beat whose text is too small to read on a screen. TYPECHECK.md lists which beats and why.)
- [art] motion histogram: screen:43  graphic:6
- [art] SKIN LINT: NO RENDERABLE BEATS: no beat carries a shot.remotion.pattern or Manim annotation — the pipeline will render NOTHING and every slot becomes a YOU-slate. The sheet was authored without the scene contract.
- [art] build stamp → beat_sheet.json (49/49 filled)
- [art] wrote /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-what-a-game-is/exports/landscape/claude-liam-lecture-key-terms-what-a-game-is.mp4  (818.9s, audio: per-beat timeline (source audio preserved), drawtext: no — PI
- [art] slots: 49/49 filled — BOPEN:VIDEO BIDEA:VIDEO BDEFS:VIDEO B0101:VIDEO B0102:VIDEO B0103:VIDEO B0104:VIDEO B0201:VIDEO B0202:VIDEO B0203:VIDEO B0204:VIDEO B0301:VIDEO B0302:VIDEO B0401:VIDEO B0402:VIDEO B0403:VIDEO B0501:VIDEO B0502:VIDEO B0503:VIDEO B0504:VIDEO B0601:VIDEO B0602:VIDEO B0603:VI
- bookend structure (Northeastern bookends; toolkit bookend_check not applicable): PASS
- loudness_check exit 0: [loud] checking 49 beats for per-beat silence … | [loud] PASS  -24.46 LUFS  tp=-2.68 dBTP
- master /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-what-a-game-is/exports/landscape/claude-liam-lecture-key-terms-what-a-game-is.mp4: 3840x2160 at 24/1, 818.88 s (13.6 min); sum of audio 817.79 s; difference +1.09 s; 46 MB
- stages done: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks
