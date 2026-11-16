# BUILD-LOG - Key Terms: The Unreal Editor

Built end to end by Claude Code with `exam-prep-deck-films/tools/build_film.py` (Bear asked for the CSYE 7270 Key Terms films, 2026-11-13).

## 2026-11-13 22:16 - stages: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks

`python3 make_film.py 25 ...` exit 0, 2 s
- claude-liam-lecture-key-terms-the-unreal-editor: 67 beats (61 deck steps), 0 already voiced, about 27.3 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
- factcheck_check.py exit 0 (0 clean, 1 advisories, 2 blocker)
`python3 generate_audio_kokoro.py claude-liam-lecture-key-terms-the-unreal-editor --only ...` exit 0, 309 s
- voiced 67 beat(s); all 67 beats have audio, 1156.8 s
`python3 pad_audio.py claude-liam-lecture-key-terms-the-unreal-editor ...` exit 0, 6 s
- pad_audio: 16 beat(s) padded; total 1163.1 s
`python3 whisper_check.py claude-liam-lecture-key-terms-the-unreal-editor ...` exit 0, 121 s
- whisper: 67 beats, 0 flagged, lowest 0.88
`python3 make_film.py 25 ...` exit 0, 2 s
- claude-liam-lecture-key-terms-the-unreal-editor: 67 beats (61 deck steps), 67 already voiced, about 19.4 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
`python3 bookends.py claude-liam-lecture-key-terms-the-unreal-editor ...` exit 0, 58 s
- bookends: BOPEN: 1 drawn frames, 16.25 s; BIDEA: 311 drawn frames, 18.88 s; BDEFS: 573 drawn frames, 26.92 s; BVDT: 463 drawn frames, 21.83 s; BHTF: 462 drawn frames, 20.46 s; BOUT: 1 drawn frames, 4.17 s; portrait: /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/professor-bear/professor-bear-1x1-231.jpg
`python3 deck_capture.py claude-liam-lecture-key-terms-the-unreal-editor ...` exit 0, 310 s
- captured 61 deck beats into /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-the-unreal-editor/media
`art run claude-liam-lecture-key-terms-the-unreal-editor --height ...` exit 0, 507 s
- [run] GATE L — beat-mix lint
- [run] GATE SHAPE — finance chart-shape enforcement
- [run] GATE V — frame-level visual QC on the compiled reel
- [gate-v] frames=134 BLOCKER=0 MAJOR=0 → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-the-unreal-editor/_qc/REPORT.md
- [run] done → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-the-unreal-editor  (QC gates: on)
`art final claude-liam-lecture-key-terms-the-unreal-editor --local ...` exit 0, 375 s
- [typecheck] §8.10 B1505: SKIP
- [typecheck] §8.10 B1506: SKIP
- [typecheck] §8.10 BVDT: SKIP
- [typecheck] §8.10 BHTF: SKIP
- [typecheck] §8.10 BOUT: SKIP
- [typecheck] GATE T: PASS
- [typecheck] (Gate T is the type-size check: it measures the smallest text in each beat of the finished film and fails any beat whose text is too small to read on a screen. TYPECHECK.md lists which beats and why.)
- [art] motion histogram: screen:61  graphic:6
- [art] SKIN LINT: NO RENDERABLE BEATS: no beat carries a shot.remotion.pattern or Manim annotation — the pipeline will render NOTHING and every slot becomes a YOU-slate. The sheet was authored without the scene contract.
- [art] build stamp → beat_sheet.json (67/67 filled)
- [art] wrote /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-the-unreal-editor/exports/landscape/claude-liam-lecture-key-terms-the-unreal-editor.mp4  (1164.5s, audio: per-beat timeline (source audio preserved), drawtext: 
- [art] slots: 67/67 filled — BOPEN:VIDEO BIDEA:VIDEO BDEFS:VIDEO B0101:VIDEO B0102:VIDEO B0103:VIDEO B0104:VIDEO B0201:VIDEO B0202:VIDEO B0203:VIDEO B0204:VIDEO B0205:VIDEO B0301:VIDEO B0302:VIDEO B0303:VIDEO B0401:VIDEO B0402:VIDEO B0403:VIDEO B0501:VIDEO B0502:VIDEO B0601:VIDEO B0602:VIDEO B0603:VI
- bookend structure (Northeastern bookends; toolkit bookend_check not applicable): PASS
- loudness_check exit 0: [loud] checking 67 beats for per-beat silence … | [loud] PASS  -24.64 LUFS  tp=-2.66 dBTP
- master /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-the-unreal-editor/exports/landscape/claude-liam-lecture-key-terms-the-unreal-editor.mp4: 3840x2160 at 24/1, 1164.50 s (19.4 min); sum of audio 1163.10 s; difference +1.40 s; 76 MB
- stages done: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks
