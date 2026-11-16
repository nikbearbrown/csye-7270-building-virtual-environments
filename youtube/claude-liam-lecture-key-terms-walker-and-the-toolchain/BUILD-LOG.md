# BUILD-LOG - Key Terms: Walker and the Toolchain

Built end to end by Claude Code with `exam-prep-deck-films/tools/build_film.py` (Bear asked for the CSYE 7270 Key Terms films, 2026-11-13).

## 2026-11-13 17:48 - stages: sheet, voice, pad, whisper

`python3 make_film.py 04 ...` exit 0, 6 s
- claude-liam-lecture-key-terms-walker-and-the-toolchain: 52 beats (46 deck steps), 0 already voiced, about 20.2 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
- factcheck_check.py exit 0 (0 clean, 1 advisories, 2 blocker)
`python3 generate_audio_kokoro.py claude-liam-lecture-key-terms-walker-and-the-toolchain --only ...` exit 0, 695 s
- voiced 52 beat(s); all 52 beats have audio, 861.5 s
`python3 pad_audio.py claude-liam-lecture-key-terms-walker-and-the-toolchain ...` exit 0, 17 s
- pad_audio: 15 beat(s) padded; total 866.7 s
`python3 whisper_check.py claude-liam-lecture-key-terms-walker-and-the-toolchain ...` exit 0, 72 s
- whisper: 52 beats, 1 flagged, lowest 0.76
- stages done: sheet, voice, pad, whisper

## 2026-11-13 22:32 - stages: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks

`python3 make_film.py 04 ...` exit 0, 3 s
- claude-liam-lecture-key-terms-walker-and-the-toolchain: 52 beats (46 deck steps), 52 already voiced, about 14.4 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
- factcheck_check.py exit 0 (0 clean, 1 advisories, 2 blocker)
- voiced 0 beat(s); all 52 beats have audio, 866.7 s
`python3 pad_audio.py claude-liam-lecture-key-terms-walker-and-the-toolchain ...` exit 0, 3 s
- pad_audio: 0 beat(s) padded; total 866.7 s
`python3 whisper_check.py claude-liam-lecture-key-terms-walker-and-the-toolchain ...` exit 0, 62 s
- whisper: 52 beats, 1 flagged, lowest 0.76
`python3 make_film.py 04 ...` exit 0, 3 s
- claude-liam-lecture-key-terms-walker-and-the-toolchain: 52 beats (46 deck steps), 52 already voiced, about 14.4 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
`python3 bookends.py claude-liam-lecture-key-terms-walker-and-the-toolchain ...` exit 0, 52 s
- bookends: BOPEN: 1 drawn frames, 13.88 s; BIDEA: 291 drawn frames, 18.04 s; BDEFS: 417 drawn frames, 20.29 s; BVDT: 393 drawn frames, 19.50 s; BHTF: 443 drawn frames, 19.54 s; BOUT: 1 drawn frames, 4.25 s; portrait: /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/professor-bear/professor-bear-1x1-119.jpg
`python3 deck_capture.py claude-liam-lecture-key-terms-walker-and-the-toolchain ...` exit 0, 188 s
- captured 46 deck beats into /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-walker-and-the-toolchain/media
`art run claude-liam-lecture-key-terms-walker-and-the-toolchain --height ...` exit 0, 430 s
- [run] GATE L — beat-mix lint
- [run] GATE SHAPE — finance chart-shape enforcement
- [run] GATE V — frame-level visual QC on the compiled reel
- [gate-v] frames=104 BLOCKER=0 MAJOR=0 → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-walker-and-the-toolchain/_qc/REPORT.md
- [run] done → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-walker-and-the-toolchain  (QC gates: on)
`art final claude-liam-lecture-key-terms-walker-and-the-toolchain --local ...` exit 0, 193 s
- [typecheck] §8.10 B1305: SKIP
- [typecheck] §8.10 B1306: SKIP
- [typecheck] §8.10 BVDT: SKIP
- [typecheck] §8.10 BHTF: SKIP
- [typecheck] §8.10 BOUT: SKIP
- [typecheck] GATE T: PASS
- [typecheck] (Gate T is the type-size check: it measures the smallest text in each beat of the finished film and fails any beat whose text is too small to read on a screen. TYPECHECK.md lists which beats and why.)
- [art] motion histogram: screen:46  graphic:6
- [art] SKIN LINT: NO RENDERABLE BEATS: no beat carries a shot.remotion.pattern or Manim annotation — the pipeline will render NOTHING and every slot becomes a YOU-slate. The sheet was authored without the scene contract.
- [art] build stamp → beat_sheet.json (52/52 filled)
- [art] wrote /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-walker-and-the-toolchain/exports/landscape/claude-liam-lecture-key-terms-walker-and-the-toolchain.mp4  (867.7s, audio: per-beat timeline (source audio preserved
- [art] slots: 52/52 filled — BOPEN:VIDEO BIDEA:VIDEO BDEFS:VIDEO B0101:VIDEO B0102:VIDEO B0103:VIDEO B0104:VIDEO B0201:VIDEO B0202:VIDEO B0203:VIDEO B0301:VIDEO B0302:VIDEO B0303:VIDEO B0401:VIDEO B0402:VIDEO B0403:VIDEO B0501:VIDEO B0502:VIDEO B0503:VIDEO B0601:VIDEO B0602:VIDEO B0603:VIDEO B0701:VI
- bookend structure (Northeastern bookends; toolkit bookend_check not applicable): PASS
- loudness_check exit 0: [loud] checking 52 beats for per-beat silence … | [loud] PASS  -24.56 LUFS  tp=-2.61 dBTP
- master /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-walker-and-the-toolchain/exports/landscape/claude-liam-lecture-key-terms-walker-and-the-toolchain.mp4: 3840x2160 at 24/1, 867.71 s (14.5 min); sum of audio 866.67 s; difference +1.04 s; 50 MB
- stages done: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks
