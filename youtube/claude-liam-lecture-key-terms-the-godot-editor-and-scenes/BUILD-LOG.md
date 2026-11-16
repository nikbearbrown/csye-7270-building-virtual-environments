# BUILD-LOG - Key Terms: The Godot Editor and Scenes

Built end to end by Claude Code with `exam-prep-deck-films/tools/build_film.py` (Bear asked for the CSYE 7270 Key Terms films, 2026-11-13).

## 2026-11-13 14:30 - stages: sheet, voice, pad, whisper

`python3 make_film.py 05 ...` exit 0, 3 s
- claude-liam-lecture-key-terms-the-godot-editor-and-scenes: 61 beats (55 deck steps), 0 already voiced, about 25.9 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
- factcheck_check.py exit 1 (0 clean, 1 advisories, 2 blocker)
`python3 generate_audio_kokoro.py claude-liam-lecture-key-terms-the-godot-editor-and-scenes --only ...` exit 0, 396 s
- voiced 61 beat(s); all 61 beats have audio, 1086.9 s
`python3 pad_audio.py claude-liam-lecture-key-terms-the-godot-editor-and-scenes ...` exit 0, 4 s
- pad_audio: 16 beat(s) padded; total 1092.5 s
`python3 whisper_check.py claude-liam-lecture-key-terms-the-godot-editor-and-scenes ...` exit 0, 41 s
- whisper: 61 beats, 2 flagged, lowest 0.81
- stages done: sheet, voice, pad, whisper

## 2026-11-13 16:52 - stages: resheet, card, capture, review, final, checks

`python3 make_film.py 05 ...` exit 0, 14 s
- claude-liam-lecture-key-terms-the-godot-editor-and-scenes: 61 beats (55 deck steps), 61 already voiced, about 18.2 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
`python3 bookends.py claude-liam-lecture-key-terms-the-godot-editor-and-scenes ...` exit 0, 60 s
- bookends: BOPEN: 1 drawn frames, 16.00 s; BIDEA: 275 drawn frames, 17.42 s; BDEFS: 666 drawn frames, 30.92 s; BVDT: 434 drawn frames, 21.04 s; BHTF: 427 drawn frames, 18.88 s; BOUT: 1 drawn frames, 4.46 s; portrait: /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/professor-bear/professor-bear-1x1-147.jpg
`python3 deck_capture.py claude-liam-lecture-key-terms-the-godot-editor-and-scenes ...` exit 0, 251 s
- captured 55 deck beats into /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-the-godot-editor-and-scenes/media
`art run claude-liam-lecture-key-terms-the-godot-editor-and-scenes --height ...` exit 0, 2511 s
- [run] GATE L — beat-mix lint
- [run] GATE SHAPE — finance chart-shape enforcement
- [run] GATE V — frame-level visual QC on the compiled reel
- [gate-v] frames=122 BLOCKER=0 MAJOR=0 → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-the-godot-editor-and-scenes/_qc/REPORT.md
- [run] done → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-the-godot-editor-and-scenes  (QC gates: on)
`art final claude-liam-lecture-key-terms-the-godot-editor-and-scenes --local ...` exit 0, 396 s
- [typecheck] §8.10 B1505: SKIP
- [typecheck] §8.10 B1506: SKIP
- [typecheck] §8.10 BVDT: SKIP
- [typecheck] §8.10 BHTF: SKIP
- [typecheck] §8.10 BOUT: SKIP
- [typecheck] GATE T: PASS
- [typecheck] (Gate T is the type-size check: it measures the smallest text in each beat of the finished film and fails any beat whose text is too small to read on a screen. TYPECHECK.md lists which beats and why.)
- [art] motion histogram: screen:55  graphic:6
- [art] SKIN LINT: NO RENDERABLE BEATS: no beat carries a shot.remotion.pattern or Manim annotation — the pipeline will render NOTHING and every slot becomes a YOU-slate. The sheet was authored without the scene contract.
- [art] build stamp → beat_sheet.json (61/61 filled)
- [art] wrote /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-the-godot-editor-and-scenes/exports/landscape/claude-liam-lecture-key-terms-the-godot-editor-and-scenes.mp4  (1093.8s, audio: per-beat timeline (source audio pr
- [art] slots: 61/61 filled — BOPEN:VIDEO BIDEA:VIDEO BDEFS:VIDEO B0101:VIDEO B0102:VIDEO B0103:VIDEO B0104:VIDEO B0201:VIDEO B0202:VIDEO B0203:VIDEO B0204:VIDEO B0301:VIDEO B0302:VIDEO B0303:VIDEO B0304:VIDEO B0401:VIDEO B0402:VIDEO B0403:VIDEO B0404:VIDEO B0501:VIDEO B0502:VIDEO B0503:VIDEO B0601:VI
- bookend structure (Northeastern bookends; toolkit bookend_check not applicable): PASS
- loudness_check exit 0: [loud] checking 61 beats for per-beat silence … | [loud] PASS  -24.52 LUFS  tp=-2.93 dBTP
- master /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-the-godot-editor-and-scenes/exports/landscape/claude-liam-lecture-key-terms-the-godot-editor-and-scenes.mp4: 3840x2160 at 24/1, 1093.75 s (18.2 min); sum of audio 1092.54 s; difference +1.21 s; 66 MB
- stages done: resheet, card, capture, review, final, checks
