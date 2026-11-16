# BUILD-LOG - Key Terms: Blender to Godot

Built end to end by Claude Code with `exam-prep-deck-films/tools/build_film.py` (Bear asked for the CSYE 7270 Key Terms films, 2026-11-13).

## 2026-11-13 19:08 - stages: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks

`python3 make_film.py 09 ...` exit 0, 2 s
- claude-liam-lecture-key-terms-blender-to-godot: 55 beats (49 deck steps), 0 already voiced, about 23.2 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
- factcheck_check.py exit 0 (0 clean, 1 advisories, 2 blocker)
`python3 generate_audio_kokoro.py claude-liam-lecture-key-terms-blender-to-godot --only ...` exit 0, 237 s
- voiced 55 beat(s); all 55 beats have audio, 1023.3 s
`python3 pad_audio.py claude-liam-lecture-key-terms-blender-to-godot ...` exit 0, 4 s
- pad_audio: 15 beat(s) padded; total 1028.8 s
`python3 whisper_check.py claude-liam-lecture-key-terms-blender-to-godot ...` exit 0, 39 s
- whisper: 55 beats, 3 flagged, lowest 0.74
`python3 make_film.py 09 ...` exit 0, 4 s
- claude-liam-lecture-key-terms-blender-to-godot: 55 beats (49 deck steps), 55 already voiced, about 17.1 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
`python3 bookends.py claude-liam-lecture-key-terms-blender-to-godot ...` exit 0, 54 s
- bookends: BOPEN: 1 drawn frames, 12.75 s; BIDEA: 276 drawn frames, 17.08 s; BDEFS: 545 drawn frames, 25.58 s; BVDT: 451 drawn frames, 22.67 s; BHTF: 480 drawn frames, 21.29 s; BOUT: 1 drawn frames, 4.04 s; portrait: /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/professor-bear/professor-bear-1x1-80.jpg
`python3 deck_capture.py claude-liam-lecture-key-terms-blender-to-godot ...` exit 0, 224 s
- captured 49 deck beats into /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-blender-to-godot/media
`art run claude-liam-lecture-key-terms-blender-to-godot --height ...` exit 0, 462 s
- [run] GATE L — beat-mix lint
- [run] GATE SHAPE — finance chart-shape enforcement
- [run] GATE V — frame-level visual QC on the compiled reel
- [gate-v] frames=110 BLOCKER=0 MAJOR=0 → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-blender-to-godot/_qc/REPORT.md
- [run] done → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-blender-to-godot  (QC gates: on)
`art final claude-liam-lecture-key-terms-blender-to-godot --local ...` exit 0, 297 s
- [typecheck] §8.10 B1305: SKIP
- [typecheck] §8.10 B1306: SKIP
- [typecheck] §8.10 BVDT: SKIP
- [typecheck] §8.10 BHTF: SKIP
- [typecheck] §8.10 BOUT: SKIP
- [typecheck] GATE T: PASS
- [typecheck] (Gate T is the type-size check: it measures the smallest text in each beat of the finished film and fails any beat whose text is too small to read on a screen. TYPECHECK.md lists which beats and why.)
- [art] motion histogram: screen:49  graphic:6
- [art] SKIN LINT: NO RENDERABLE BEATS: no beat carries a shot.remotion.pattern or Manim annotation — the pipeline will render NOTHING and every slot becomes a YOU-slate. The sheet was authored without the scene contract.
- [art] build stamp → beat_sheet.json (55/55 filled)
- [art] wrote /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-blender-to-godot/exports/landscape/claude-liam-lecture-key-terms-blender-to-godot.mp4  (1029.8s, audio: per-beat timeline (source audio preserved), drawtext: no
- [art] slots: 55/55 filled — BOPEN:VIDEO BIDEA:VIDEO BDEFS:VIDEO B0101:VIDEO B0102:VIDEO B0103:VIDEO B0104:VIDEO B0201:VIDEO B0202:VIDEO B0203:VIDEO B0301:VIDEO B0302:VIDEO B0303:VIDEO B0401:VIDEO B0402:VIDEO B0403:VIDEO B0404:VIDEO B0501:VIDEO B0502:VIDEO B0503:VIDEO B0601:VIDEO B0602:VIDEO B0603:VI
- bookend structure (Northeastern bookends; toolkit bookend_check not applicable): PASS
- loudness_check exit 0: [loud] checking 55 beats for per-beat silence … | [loud] PASS  -24.49 LUFS  tp=-2.59 dBTP
- master /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-blender-to-godot/exports/landscape/claude-liam-lecture-key-terms-blender-to-godot.mp4: 3840x2160 at 24/1, 1029.83 s (17.2 min); sum of audio 1028.83 s; difference +1.00 s; 64 MB
- stages done: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks
