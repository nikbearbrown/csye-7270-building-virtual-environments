# BUILD-LOG - Key Terms: Particles and VFX

Built end to end by Claude Code with `exam-prep-deck-films/tools/build_film.py` (Bear asked for the CSYE 7270 Key Terms films, 2026-11-13).

## 2026-11-13 20:08 - stages: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks

`python3 make_film.py 14 ...` exit 0, 3 s
- claude-liam-lecture-key-terms-particles-and-vfx: 64 beats (58 deck steps), 0 already voiced, about 28.7 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
- factcheck_check.py exit 0 (0 clean, 1 advisories, 2 blocker)
`python3 generate_audio_kokoro.py claude-liam-lecture-key-terms-particles-and-vfx --only ...` exit 0, 280 s
- voiced 64 beat(s); all 64 beats have audio, 1264.9 s
`python3 pad_audio.py claude-liam-lecture-key-terms-particles-and-vfx ...` exit 0, 6 s
- pad_audio: 18 beat(s) padded; total 1271.1 s
`python3 whisper_check.py claude-liam-lecture-key-terms-particles-and-vfx ...` exit 0, 90 s
- whisper: 64 beats, 0 flagged, lowest 0.88
`python3 make_film.py 14 ...` exit 0, 3 s
- claude-liam-lecture-key-terms-particles-and-vfx: 64 beats (58 deck steps), 64 already voiced, about 21.2 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
`python3 bookends.py claude-liam-lecture-key-terms-particles-and-vfx ...` exit 0, 65 s
- bookends: BOPEN: 1 drawn frames, 15.83 s; BIDEA: 267 drawn frames, 17.04 s; BDEFS: 783 drawn frames, 35.67 s; BVDT: 466 drawn frames, 22.67 s; BHTF: 439 drawn frames, 19.42 s; BOUT: 1 drawn frames, 4.38 s; portrait: /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/professor-bear/professor-bear-1x1-264.jpg
`python3 deck_capture.py claude-liam-lecture-key-terms-particles-and-vfx ...` exit 0, 259 s
- captured 58 deck beats into /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-particles-and-vfx/media
`art run claude-liam-lecture-key-terms-particles-and-vfx --height ...` exit 0, 578 s
- [run] GATE L — beat-mix lint
- [run] GATE SHAPE — finance chart-shape enforcement
- [run] GATE V — frame-level visual QC on the compiled reel
- [gate-v] frames=128 BLOCKER=0 MAJOR=0 → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-particles-and-vfx/_qc/REPORT.md
- [run] done → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-particles-and-vfx  (QC gates: on)
`art final claude-liam-lecture-key-terms-particles-and-vfx --local ...` exit 0, 395 s
- [typecheck] §8.10 B1505: SKIP
- [typecheck] §8.10 B1506: SKIP
- [typecheck] §8.10 BVDT: SKIP
- [typecheck] §8.10 BHTF: SKIP
- [typecheck] §8.10 BOUT: SKIP
- [typecheck] GATE T: PASS
- [typecheck] (Gate T is the type-size check: it measures the smallest text in each beat of the finished film and fails any beat whose text is too small to read on a screen. TYPECHECK.md lists which beats and why.)
- [art] motion histogram: screen:58  graphic:6
- [art] SKIN LINT: NO RENDERABLE BEATS: no beat carries a shot.remotion.pattern or Manim annotation — the pipeline will render NOTHING and every slot becomes a YOU-slate. The sheet was authored without the scene contract.
- [art] build stamp → beat_sheet.json (64/64 filled)
- [art] wrote /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-particles-and-vfx/exports/landscape/claude-liam-lecture-key-terms-particles-and-vfx.mp4  (1272.5s, audio: per-beat timeline (source audio preserved), drawtext: 
- [art] slots: 64/64 filled — BOPEN:VIDEO BIDEA:VIDEO BDEFS:VIDEO B0101:VIDEO B0102:VIDEO B0103:VIDEO B0104:VIDEO B0201:VIDEO B0202:VIDEO B0203:VIDEO B0301:VIDEO B0302:VIDEO B0303:VIDEO B0304:VIDEO B0401:VIDEO B0402:VIDEO B0403:VIDEO B0404:VIDEO B0501:VIDEO B0502:VIDEO B0503:VIDEO B0504:VIDEO B0601:VI
- bookend structure (Northeastern bookends; toolkit bookend_check not applicable): PASS
- loudness_check exit 0: [loud] checking 64 beats for per-beat silence … | [loud] PASS  -24.41 LUFS  tp=-2.82 dBTP
- master /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-particles-and-vfx/exports/landscape/claude-liam-lecture-key-terms-particles-and-vfx.mp4: 3840x2160 at 24/1, 1272.54 s (21.2 min); sum of audio 1271.13 s; difference +1.41 s; 79 MB
- stages done: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks
