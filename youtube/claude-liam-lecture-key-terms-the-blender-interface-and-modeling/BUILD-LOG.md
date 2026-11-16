# BUILD-LOG - Key Terms: The Blender Interface and Modeling

Built end to end by Claude Code with `exam-prep-deck-films/tools/build_film.py` (Bear asked for the CSYE 7270 Key Terms films, 2026-11-13).

## 2026-11-13 18:54 - stages: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks

`python3 make_film.py 08 ...` exit 0, 0 s
- claude-liam-lecture-key-terms-the-blender-interface-and-modeling: 55 beats (49 deck steps), 0 already voiced, about 22.8 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
- factcheck_check.py exit 0 (0 clean, 1 advisories, 2 blocker)
`python3 generate_audio_kokoro.py claude-liam-lecture-key-terms-the-blender-interface-and-modeling --only ...` exit 0, 256 s
- voiced 55 beat(s); all 55 beats have audio, 983.2 s
`python3 pad_audio.py claude-liam-lecture-key-terms-the-blender-interface-and-modeling ...` exit 0, 6 s
- pad_audio: 17 beat(s) padded; total 989.4 s
`python3 whisper_check.py claude-liam-lecture-key-terms-the-blender-interface-and-modeling ...` exit 0, 82 s
- whisper: 55 beats, 3 flagged, lowest 0.82
`python3 make_film.py 08 ...` exit 0, 0 s
- claude-liam-lecture-key-terms-the-blender-interface-and-modeling: 55 beats (49 deck steps), 55 already voiced, about 16.5 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
`python3 bookends.py claude-liam-lecture-key-terms-the-blender-interface-and-modeling ...` exit 0, 59 s
- bookends: BOPEN: 1 drawn frames, 16.38 s; BIDEA: 298 drawn frames, 18.33 s; BDEFS: 525 drawn frames, 24.92 s; BVDT: 493 drawn frames, 24.79 s; BHTF: 447 drawn frames, 19.79 s; BOUT: 1 drawn frames, 4.71 s; portrait: /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/professor-bear/professor-bear-1x1-106.jpg
`python3 deck_capture.py claude-liam-lecture-key-terms-the-blender-interface-and-modeling ...` exit 0, 249 s
- captured 49 deck beats into /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-the-blender-interface-and-modeling/media
`art run claude-liam-lecture-key-terms-the-blender-interface-and-modeling --height ...` exit 0, 462 s
- [run] GATE L — beat-mix lint
- [run] GATE SHAPE — finance chart-shape enforcement
- [run] GATE V — frame-level visual QC on the compiled reel
- [gate-v] frames=110 BLOCKER=0 MAJOR=0 → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-the-blender-interface-and-modeling/_qc/REPORT.md
- [run] done → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-the-blender-interface-and-modeling  (QC gates: on)
`art final claude-liam-lecture-key-terms-the-blender-interface-and-modeling --local ...` exit 0, 280 s
- [typecheck] §8.10 B1505: SKIP
- [typecheck] §8.10 B1506: SKIP
- [typecheck] §8.10 BVDT: SKIP
- [typecheck] §8.10 BHTF: SKIP
- [typecheck] §8.10 BOUT: SKIP
- [typecheck] GATE T: PASS
- [typecheck] (Gate T is the type-size check: it measures the smallest text in each beat of the finished film and fails any beat whose text is too small to read on a screen. TYPECHECK.md lists which beats and why.)
- [art] motion histogram: screen:49  graphic:6
- [art] SKIN LINT: NO RENDERABLE BEATS: no beat carries a shot.remotion.pattern or Manim annotation — the pipeline will render NOTHING and every slot becomes a YOU-slate. The sheet was authored without the scene contract.
- [art] build stamp → beat_sheet.json (55/55 filled)
- [art] wrote /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-the-blender-interface-and-modeling/exports/landscape/claude-liam-lecture-key-terms-the-blender-interface-and-modeling.mp4  (990.6s, audio: per-beat timeline (so
- [art] slots: 55/55 filled — BOPEN:VIDEO BIDEA:VIDEO BDEFS:VIDEO B0101:VIDEO B0102:VIDEO B0103:VIDEO B0104:VIDEO B0201:VIDEO B0202:VIDEO B0203:VIDEO B0301:VIDEO B0302:VIDEO B0401:VIDEO B0402:VIDEO B0403:VIDEO B0501:VIDEO B0502:VIDEO B0503:VIDEO B0504:VIDEO B0601:VIDEO B0602:VIDEO B0701:VIDEO B0702:VI
- bookend structure (Northeastern bookends; toolkit bookend_check not applicable): PASS
- loudness_check exit 0: [loud] checking 55 beats for per-beat silence … | [loud] PASS  -24.47 LUFS  tp=-2.55 dBTP
- master /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-the-blender-interface-and-modeling/exports/landscape/claude-liam-lecture-key-terms-the-blender-interface-and-modeling.mp4: 3840x2160 at 24/1, 990.58 s (16.5 min); sum of audio 989.40 s; difference +1.18 s; 62 MB
- stages done: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks
