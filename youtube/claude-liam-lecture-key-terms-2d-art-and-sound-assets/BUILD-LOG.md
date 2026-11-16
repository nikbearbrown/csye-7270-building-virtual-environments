# BUILD-LOG - Key Terms: 2D Art and Sound Assets

Built end to end by Claude Code with `exam-prep-deck-films/tools/build_film.py` (Bear asked for the CSYE 7270 Key Terms films, 2026-11-13).

## 2026-11-13 18:21 - stages: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks

`python3 make_film.py 06 ...` exit 0, 2 s
- claude-liam-lecture-key-terms-2d-art-and-sound-assets: 63 beats (57 deck steps), 0 already voiced, about 27.7 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
- factcheck_check.py exit 1 (0 clean, 1 advisories, 2 blocker)
`python3 generate_audio_kokoro.py claude-liam-lecture-key-terms-2d-art-and-sound-assets --only ...` exit 0, 407 s
- voiced 63 beat(s); all 63 beats have audio, 1224.3 s
`python3 pad_audio.py claude-liam-lecture-key-terms-2d-art-and-sound-assets ...` exit 0, 7 s
- pad_audio: 19 beat(s) padded; total 1231.6 s
`python3 whisper_check.py claude-liam-lecture-key-terms-2d-art-and-sound-assets ...` exit 0, 90 s
- whisper: 63 beats, 0 flagged, lowest 0.86
`python3 make_film.py 06 ...` exit 0, 5 s
- claude-liam-lecture-key-terms-2d-art-and-sound-assets: 63 beats (57 deck steps), 63 already voiced, about 20.5 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
`python3 bookends.py claude-liam-lecture-key-terms-2d-art-and-sound-assets ...` exit 0, 69 s
- bookends: BOPEN: 1 drawn frames, 16.46 s; BIDEA: 295 drawn frames, 18.00 s; BDEFS: 783 drawn frames, 35.67 s; BVDT: 444 drawn frames, 22.12 s; BHTF: 436 drawn frames, 19.25 s; BOUT: 1 drawn frames, 4.62 s; portrait: /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/professor-bear/professor-bear-1x1-246.jpg
`python3 deck_capture.py claude-liam-lecture-key-terms-2d-art-and-sound-assets ...` exit 0, 349 s
- captured 57 deck beats into /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-2d-art-and-sound-assets/media
`art run claude-liam-lecture-key-terms-2d-art-and-sound-assets --height ...` exit 0, 636 s
- [run] GATE L — beat-mix lint
- [run] GATE SHAPE — finance chart-shape enforcement
- [run] GATE V — frame-level visual QC on the compiled reel
- [gate-v] frames=126 BLOCKER=0 MAJOR=0 → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-2d-art-and-sound-assets/_qc/REPORT.md
- [run] done → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-2d-art-and-sound-assets  (QC gates: on)
`art final claude-liam-lecture-key-terms-2d-art-and-sound-assets --local ...` exit 0, 373 s
- [typecheck] §8.10 B1505: SKIP
- [typecheck] §8.10 B1506: SKIP
- [typecheck] §8.10 BVDT: SKIP
- [typecheck] §8.10 BHTF: SKIP
- [typecheck] §8.10 BOUT: SKIP
- [typecheck] GATE T: PASS
- [typecheck] (Gate T is the type-size check: it measures the smallest text in each beat of the finished film and fails any beat whose text is too small to read on a screen. TYPECHECK.md lists which beats and why.)
- [art] motion histogram: screen:57  graphic:6
- [art] SKIN LINT: NO RENDERABLE BEATS: no beat carries a shot.remotion.pattern or Manim annotation — the pipeline will render NOTHING and every slot becomes a YOU-slate. The sheet was authored without the scene contract.
- [art] build stamp → beat_sheet.json (63/63 filled)
- [art] wrote /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-2d-art-and-sound-assets/exports/landscape/claude-liam-lecture-key-terms-2d-art-and-sound-assets.mp4  (1232.9s, audio: per-beat timeline (source audio preserved)
- [art] slots: 63/63 filled — BOPEN:VIDEO BIDEA:VIDEO BDEFS:VIDEO B0101:VIDEO B0102:VIDEO B0103:VIDEO B0104:VIDEO B0201:VIDEO B0202:VIDEO B0203:VIDEO B0204:VIDEO B0301:VIDEO B0302:VIDEO B0303:VIDEO B0401:VIDEO B0402:VIDEO B0403:VIDEO B0404:VIDEO B0501:VIDEO B0502:VIDEO B0503:VIDEO B0504:VIDEO B0601:VI
- bookend structure (Northeastern bookends; toolkit bookend_check not applicable): PASS
- loudness_check exit 0: [loud] checking 63 beats for per-beat silence … | [loud] PASS  -24.50 LUFS  tp=-2.81 dBTP
- master /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-2d-art-and-sound-assets/exports/landscape/claude-liam-lecture-key-terms-2d-art-and-sound-assets.mp4: 3840x2160 at 24/1, 1232.92 s (20.5 min); sum of audio 1231.59 s; difference +1.33 s; 75 MB
- stages done: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks
