# BUILD-LOG - Key Terms: Choices and Challenge

Built end to end by Claude Code with `exam-prep-deck-films/tools/build_film.py` (Bear asked for the CSYE 7270 Key Terms films, 2026-11-13).

## 2026-11-13 17:40 - stages: sheet, voice, pad, whisper

`python3 make_film.py 02 ...` exit 0, 5 s
- claude-liam-lecture-key-terms-choices-and-challenge: 45 beats (39 deck steps), 0 already voiced, about 16.4 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
- factcheck_check.py exit 0 (0 clean, 1 advisories, 2 blocker)
`python3 generate_audio_kokoro.py claude-liam-lecture-key-terms-choices-and-challenge --only ...` exit 0, 351 s
- voiced 45 beat(s); all 45 beats have audio, 724.1 s
`python3 pad_audio.py claude-liam-lecture-key-terms-choices-and-challenge ...` exit 0, 3 s
- pad_audio: 14 beat(s) padded; total 729.3 s
`python3 whisper_check.py claude-liam-lecture-key-terms-choices-and-challenge ...` exit 0, 111 s
- whisper: 45 beats, 0 flagged, lowest 0.89
- stages done: sheet, voice, pad, whisper

## 2026-11-13 17:52 - stages: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks

`python3 make_film.py 02 ...` exit 0, 12 s
- claude-liam-lecture-key-terms-choices-and-challenge: 45 beats (39 deck steps), 45 already voiced, about 12.2 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 5 s
- factcheck_check.py exit 0 (0 clean, 1 advisories, 2 blocker)
- voiced 0 beat(s); all 45 beats have audio, 729.3 s
`python3 pad_audio.py claude-liam-lecture-key-terms-choices-and-challenge ...` exit 0, 15 s
- pad_audio: 0 beat(s) padded; total 729.3 s
`python3 whisper_check.py claude-liam-lecture-key-terms-choices-and-challenge ...` exit 0, 455 s
- whisper: 45 beats, 0 flagged, lowest 0.89
`python3 make_film.py 02 ...` exit 0, 2 s
- claude-liam-lecture-key-terms-choices-and-challenge: 45 beats (39 deck steps), 45 already voiced, about 12.2 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
`python3 bookends.py claude-liam-lecture-key-terms-choices-and-challenge ...` exit 0, 58 s
- bookends: BOPEN: 1 drawn frames, 16.08 s; BIDEA: 277 drawn frames, 18.25 s; BDEFS: 463 drawn frames, 22.21 s; BVDT: 493 drawn frames, 23.50 s; BHTF: 457 drawn frames, 20.21 s; BOUT: 1 drawn frames, 4.25 s; portrait: /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/professor-bear/professor-bear-1x1-80.jpg
`python3 deck_capture.py claude-liam-lecture-key-terms-choices-and-challenge ...` exit 0, 191 s
- captured 39 deck beats into /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-choices-and-challenge/media
`art run claude-liam-lecture-key-terms-choices-and-challenge --height ...` exit 0, 521 s
- [run] GATE L — beat-mix lint
- [run] GATE SHAPE — finance chart-shape enforcement
- [run] GATE V — frame-level visual QC on the compiled reel
- [gate-v] frames=90 BLOCKER=0 MAJOR=0 → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-choices-and-challenge/_qc/REPORT.md
- [run] done → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-choices-and-challenge  (QC gates: on)
`art final claude-liam-lecture-key-terms-choices-and-challenge --local ...` exit 0, 308 s
- [typecheck] §8.10 B1305: SKIP
- [typecheck] §8.10 B1306: SKIP
- [typecheck] §8.10 BVDT: SKIP
- [typecheck] §8.10 BHTF: SKIP
- [typecheck] §8.10 BOUT: SKIP
- [typecheck] GATE T: PASS
- [typecheck] (Gate T is the type-size check: it measures the smallest text in each beat of the finished film and fails any beat whose text is too small to read on a screen. TYPECHECK.md lists which beats and why.)
- [art] motion histogram: screen:39  graphic:6
- [art] SKIN LINT: NO RENDERABLE BEATS: no beat carries a shot.remotion.pattern or Manim annotation — the pipeline will render NOTHING and every slot becomes a YOU-slate. The sheet was authored without the scene contract.
- [art] build stamp → beat_sheet.json (45/45 filled)
- [art] wrote /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-choices-and-challenge/exports/landscape/claude-liam-lecture-key-terms-choices-and-challenge.mp4  (730.2s, audio: per-beat timeline (source audio preserved), dra
- [art] slots: 45/45 filled — BOPEN:VIDEO BIDEA:VIDEO BDEFS:VIDEO B0101:VIDEO B0102:VIDEO B0103:VIDEO B0104:VIDEO B0201:VIDEO B0202:VIDEO B0203:VIDEO B0301:VIDEO B0302:VIDEO B0401:VIDEO B0402:VIDEO B0501:VIDEO B0502:VIDEO B0601:VIDEO B0602:VIDEO B0701:VIDEO B0702:VIDEO B0801:VIDEO B0802:VIDEO B0803:VI
- bookend structure (Northeastern bookends; toolkit bookend_check not applicable): PASS
- loudness_check exit 0: [loud] checking 45 beats for per-beat silence … | [loud] PASS  -24.45 LUFS  tp=-2.78 dBTP
- master /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-choices-and-challenge/exports/landscape/claude-liam-lecture-key-terms-choices-and-challenge.mp4: 3840x2160 at 24/1, 730.21 s (12.2 min); sum of audio 729.34 s; difference +0.87 s; 44 MB
- stages done: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks
