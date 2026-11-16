# BUILD-LOG - Key Terms: Animation and Interaction

Built end to end by Claude Code with `exam-prep-deck-films/tools/build_film.py` (Bear asked for the CSYE 7270 Key Terms films, 2026-11-13).

## 2026-11-13 20:44 - stages: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks

`python3 make_film.py 17 ...` exit 0, 0 s
- claude-liam-lecture-key-terms-animation-and-interaction: 60 beats (54 deck steps), 0 already voiced, about 26.2 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
- factcheck_check.py exit 0 (0 clean, 1 advisories, 2 blocker)
`python3 generate_audio_kokoro.py claude-liam-lecture-key-terms-animation-and-interaction --only ...` exit 0, 214 s
- voiced 60 beat(s); all 60 beats have audio, 1104.0 s
`python3 pad_audio.py claude-liam-lecture-key-terms-animation-and-interaction ...` exit 0, 5 s
- pad_audio: 18 beat(s) padded; total 1110.6 s
`python3 whisper_check.py claude-liam-lecture-key-terms-animation-and-interaction ...` exit 0, 76 s
- whisper: 60 beats, 0 flagged, lowest 0.88
`python3 make_film.py 17 ...` exit 0, 0 s
- claude-liam-lecture-key-terms-animation-and-interaction: 60 beats (54 deck steps), 60 already voiced, about 18.5 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
`python3 bookends.py claude-liam-lecture-key-terms-animation-and-interaction ...` exit 0, 53 s
- bookends: BOPEN: 1 drawn frames, 16.12 s; BIDEA: 300 drawn frames, 18.88 s; BDEFS: 535 drawn frames, 25.25 s; BVDT: 444 drawn frames, 22.46 s; BHTF: 447 drawn frames, 19.75 s; BOUT: 1 drawn frames, 4.42 s; portrait: /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/professor-bear/professor-bear-1x1-249.jpg
`python3 deck_capture.py claude-liam-lecture-key-terms-animation-and-interaction ...` exit 0, 271 s
- captured 54 deck beats into /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-animation-and-interaction/media
`art run claude-liam-lecture-key-terms-animation-and-interaction --height ...` exit 0, 511 s
- [run] GATE L — beat-mix lint
- [run] GATE SHAPE — finance chart-shape enforcement
- [run] GATE V — frame-level visual QC on the compiled reel
- [gate-v] frames=120 BLOCKER=0 MAJOR=0 → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-animation-and-interaction/_qc/REPORT.md
- [run] done → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-animation-and-interaction  (QC gates: on)
`art final claude-liam-lecture-key-terms-animation-and-interaction --local ...` exit 0, 271 s
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
- [art] wrote /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-animation-and-interaction/exports/landscape/claude-liam-lecture-key-terms-animation-and-interaction.mp4  (1111.9s, audio: per-beat timeline (source audio preser
- [art] slots: 60/60 filled — BOPEN:VIDEO BIDEA:VIDEO BDEFS:VIDEO B0101:VIDEO B0102:VIDEO B0103:VIDEO B0104:VIDEO B0201:VIDEO B0202:VIDEO B0203:VIDEO B0301:VIDEO B0302:VIDEO B0303:VIDEO B0401:VIDEO B0402:VIDEO B0403:VIDEO B0404:VIDEO B0501:VIDEO B0502:VIDEO B0503:VIDEO B0504:VIDEO B0601:VIDEO B0602:VI
- bookend structure (Northeastern bookends; toolkit bookend_check not applicable): PASS
- loudness_check exit 0: [loud] checking 60 beats for per-beat silence … | [loud] PASS  -24.54 LUFS  tp=-2.73 dBTP
- master /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-animation-and-interaction/exports/landscape/claude-liam-lecture-key-terms-animation-and-interaction.mp4: 3840x2160 at 24/1, 1111.88 s (18.5 min); sum of audio 1110.62 s; difference +1.26 s; 74 MB
- stages done: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks
