# BUILD-LOG - Key Terms: Materials and Textures

Built end to end by Claude Code with `exam-prep-deck-films/tools/build_film.py` (Bear asked for the CSYE 7270 Key Terms films, 2026-11-13).

## 2026-11-13 19:42 - stages: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks

`python3 make_film.py 12 ...` exit 0, 4 s
- claude-liam-lecture-key-terms-materials-and-textures: 60 beats (54 deck steps), 0 already voiced, about 26.6 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
- factcheck_check.py exit 0 (0 clean, 1 advisories, 2 blocker)
`python3 generate_audio_kokoro.py claude-liam-lecture-key-terms-materials-and-textures --only ...` exit 0, 262 s
- voiced 60 beat(s); all 60 beats have audio, 1187.0 s
`python3 pad_audio.py claude-liam-lecture-key-terms-materials-and-textures ...` exit 0, 6 s
- pad_audio: 20 beat(s) padded; total 1193.8 s
`python3 whisper_check.py claude-liam-lecture-key-terms-materials-and-textures ...` exit 0, 74 s
- whisper: 60 beats, 1 flagged, lowest 0.86
`python3 make_film.py 12 ...` exit 0, 4 s
- claude-liam-lecture-key-terms-materials-and-textures: 60 beats (54 deck steps), 60 already voiced, about 19.9 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
`python3 bookends.py claude-liam-lecture-key-terms-materials-and-textures ...` exit 0, 50 s
- bookends: BOPEN: 1 drawn frames, 15.08 s; BIDEA: 296 drawn frames, 19.08 s; BDEFS: 672 drawn frames, 31.00 s; BVDT: 468 drawn frames, 23.25 s; BHTF: 445 drawn frames, 19.67 s; BOUT: 1 drawn frames, 4.25 s; portrait: /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/professor-bear/professor-bear-1x1-123.jpg
`python3 deck_capture.py claude-liam-lecture-key-terms-materials-and-textures ...` exit 0, 256 s
- captured 54 deck beats into /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-materials-and-textures/media
`art run claude-liam-lecture-key-terms-materials-and-textures --height ...` exit 0, 504 s
- [run] GATE L — beat-mix lint
- [run] GATE SHAPE — finance chart-shape enforcement
- [run] GATE V — frame-level visual QC on the compiled reel
- [gate-v] frames=120 BLOCKER=0 MAJOR=0 → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-materials-and-textures/_qc/REPORT.md
- [run] done → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-materials-and-textures  (QC gates: on)
`art final claude-liam-lecture-key-terms-materials-and-textures --local ...` exit 0, 345 s
- [typecheck] §8.10 B1505: SKIP
- [typecheck] §8.10 B1506: SKIP
- [typecheck] §8.10 BVDT: SKIP
- [typecheck] §8.10 BHTF: SKIP
- [typecheck] §8.10 BOUT: SKIP
- [typecheck] GATE T: PASS
- [typecheck] (Gate T is the type-size check: it measures the smallest text in each beat of the finished film and fails any beat whose text is too small to read on a screen. TYPECHECK.md lists which beats and why.)
- [art] motion histogram: screen:54  graphic:6
- [art] SKIN LINT: NO RENDERABLE BEATS: no beat carries a shot.remotion.pattern or Manim annotation — the pipeline will render NOTHING and every slot becomes a YOU-slate. The sheet was authored without the scene contract.
- [art] build stamp → beat_sheet.json (60/60 filled)
- [art] wrote /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-materials-and-textures/exports/landscape/claude-liam-lecture-key-terms-materials-and-textures.mp4  (1195.0s, audio: per-beat timeline (source audio preserved), 
- [art] slots: 60/60 filled — BOPEN:VIDEO BIDEA:VIDEO BDEFS:VIDEO B0101:VIDEO B0102:VIDEO B0103:VIDEO B0104:VIDEO B0201:VIDEO B0202:VIDEO B0203:VIDEO B0301:VIDEO B0302:VIDEO B0303:VIDEO B0401:VIDEO B0402:VIDEO B0403:VIDEO B0404:VIDEO B0501:VIDEO B0502:VIDEO B0503:VIDEO B0601:VIDEO B0602:VIDEO B0603:VI
- bookend structure (Northeastern bookends; toolkit bookend_check not applicable): PASS
- loudness_check exit 0: [loud] checking 60 beats for per-beat silence … | [loud] PASS  -24.50 LUFS  tp=-2.35 dBTP
- master /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-materials-and-textures/exports/landscape/claude-liam-lecture-key-terms-materials-and-textures.mp4: 3840x2160 at 24/1, 1195.04 s (19.9 min); sum of audio 1193.80 s; difference +1.24 s; 77 MB
- stages done: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks
