# BUILD-LOG - Key Terms: Camera

Built end to end by Claude Code with `exam-prep-deck-films/tools/build_film.py` (Bear asked for the CSYE 7270 Key Terms films, 2026-11-13).

## 2026-11-13 21:00 - stages: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks

`python3 make_film.py 18 ...` exit 0, 2 s
- claude-liam-lecture-key-terms-camera: 52 beats (46 deck steps), 0 already voiced, about 19.6 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
- factcheck_check.py exit 0 (0 clean, 1 advisories, 2 blocker)
`python3 generate_audio_kokoro.py claude-liam-lecture-key-terms-camera --only ...` exit 0, 155 s
- voiced 52 beat(s); all 52 beats have audio, 840.9 s
`python3 pad_audio.py claude-liam-lecture-key-terms-camera ...` exit 0, 4 s
- pad_audio: 17 beat(s) padded; total 846.7 s
`python3 whisper_check.py claude-liam-lecture-key-terms-camera ...` exit 0, 67 s
- whisper: 52 beats, 1 flagged, lowest 0.86
`python3 make_film.py 18 ...` exit 0, 2 s
- claude-liam-lecture-key-terms-camera: 52 beats (46 deck steps), 52 already voiced, about 14.1 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
`python3 bookends.py claude-liam-lecture-key-terms-camera ...` exit 0, 50 s
- bookends: BOPEN: 1 drawn frames, 14.88 s; BIDEA: 309 drawn frames, 18.58 s; BDEFS: 390 drawn frames, 19.25 s; BVDT: 430 drawn frames, 21.00 s; BHTF: 416 drawn frames, 18.33 s; BOUT: 1 drawn frames, 3.42 s; portrait: /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/professor-bear/professor-bear-1x1-144.jpg
`python3 deck_capture.py claude-liam-lecture-key-terms-camera ...` exit 0, 177 s
- captured 46 deck beats into /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-camera/media
`art run claude-liam-lecture-key-terms-camera --height ...` exit 0, 353 s
- [run] GATE L — beat-mix lint
- [run] GATE SHAPE — finance chart-shape enforcement
- [run] GATE V — frame-level visual QC on the compiled reel
- [gate-v] frames=104 BLOCKER=0 MAJOR=0 → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-camera/_qc/REPORT.md
- [run] done → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-camera  (QC gates: on)
`art final claude-liam-lecture-key-terms-camera --local ...` exit 0, 223 s
- [typecheck] §8.10 B1805: SKIP
- [typecheck] §8.10 B1806: SKIP
- [typecheck] §8.10 BVDT: SKIP
- [typecheck] §8.10 BHTF: SKIP
- [typecheck] §8.10 BOUT: SKIP
- [typecheck] GATE T: PASS
- [typecheck] (Gate T is the type-size check: it measures the smallest text in each beat of the finished film and fails any beat whose text is too small to read on a screen. TYPECHECK.md lists which beats and why.)
- [art] motion histogram: screen:46  graphic:6
- [art] SKIN LINT: NO RENDERABLE BEATS: no beat carries a shot.remotion.pattern or Manim annotation — the pipeline will render NOTHING and every slot becomes a YOU-slate. The sheet was authored without the scene contract.
- [art] build stamp → beat_sheet.json (52/52 filled)
- [art] wrote /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-camera/exports/landscape/claude-liam-lecture-key-terms-camera.mp4  (847.8s, audio: per-beat timeline (source audio preserved), drawtext: no — PIL overlays)
- [art] slots: 52/52 filled — BOPEN:VIDEO BIDEA:VIDEO BDEFS:VIDEO B0101:VIDEO B0102:VIDEO B0103:VIDEO B0104:VIDEO B0105:VIDEO B0301:VIDEO B0302:VIDEO B0303:VIDEO B0401:VIDEO B0402:VIDEO B0403:VIDEO B0501:VIDEO B0502:VIDEO B0701:VIDEO B0702:VIDEO B0703:VIDEO B0801:VIDEO B0802:VIDEO B0803:VIDEO B0901:VI
- bookend structure (Northeastern bookends; toolkit bookend_check not applicable): PASS
- loudness_check exit 0: [loud] checking 52 beats for per-beat silence … | [loud] PASS  -24.47 LUFS  tp=-2.55 dBTP
- master /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-camera/exports/landscape/claude-liam-lecture-key-terms-camera.mp4: 3840x2160 at 24/1, 847.75 s (14.1 min); sum of audio 846.72 s; difference +1.03 s; 52 MB
- stages done: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks
