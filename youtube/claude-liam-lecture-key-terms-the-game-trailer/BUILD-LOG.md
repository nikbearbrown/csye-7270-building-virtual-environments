# BUILD-LOG - Key Terms: The Game Trailer

Built end to end by Claude Code with `exam-prep-deck-films/tools/build_film.py` (Bear asked for the CSYE 7270 Key Terms films, 2026-11-13).

## 2026-11-13 21:41 - stages: sheet, voice, pad, whisper, resheet, card, capture, review, final, checks

`python3 make_film.py 22 ...` exit 0, 2 s
- claude-liam-lecture-key-terms-the-game-trailer: 58 beats (52 deck steps), 0 already voiced, about 24.8 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
- factcheck_check.py exit 0 (0 clean, 1 advisories, 2 blocker)
`python3 generate_audio_kokoro.py claude-liam-lecture-key-terms-the-game-trailer --only ...` exit 0, 207 s
- voiced 58 beat(s); all 58 beats have audio, 1022.2 s
`python3 pad_audio.py claude-liam-lecture-key-terms-the-game-trailer ...` exit 0, 5 s
- pad_audio: 16 beat(s) padded; total 1028.0 s
`python3 whisper_check.py claude-liam-lecture-key-terms-the-game-trailer ...` exit 0, 74 s
- whisper: 58 beats, 0 flagged, lowest 0.89
`python3 make_film.py 22 ...` exit 0, 2 s
- claude-liam-lecture-key-terms-the-game-trailer: 58 beats (52 deck steps), 58 already voiced, about 17.1 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
`python3 bookends.py claude-liam-lecture-key-terms-the-game-trailer ...` exit 0, 51 s
- bookends: BOPEN: 1 drawn frames, 14.88 s; BIDEA: 286 drawn frames, 17.42 s; BDEFS: 761 drawn frames, 34.92 s; BVDT: 444 drawn frames, 21.75 s; BHTF: 419 drawn frames, 18.50 s; BOUT: 1 drawn frames, 3.92 s; portrait: /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/professor-bear/professor-bear-1x1-69.jpg
`python3 deck_capture.py claude-liam-lecture-key-terms-the-game-trailer ...` exit 0, 204 s
- captured 52 deck beats into /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-the-game-trailer/media
`art run claude-liam-lecture-key-terms-the-game-trailer --height ...` exit 0, 447 s
- [run] GATE L — beat-mix lint
- [run] GATE SHAPE — finance chart-shape enforcement
- [run] GATE V — frame-level visual QC on the compiled reel
- [gate-v] frames=116 BLOCKER=0 MAJOR=0 → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-the-game-trailer/_qc/REPORT.md
- [run] done → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-the-game-trailer  (QC gates: on)
`art final claude-liam-lecture-key-terms-the-game-trailer --local ...` exit 2, 11 s
```
[typecheck] §8.10 B0602: SKIP
[typecheck] §8.10 B0603: SKIP
[typecheck] §8.10 B0701: SKIP
[typecheck] §8.10 B0702: SKIP
[typecheck] §8.10 B0801: SKIP
[typecheck] §8.10 B0802: SKIP
[typecheck] §8.10 B0803: SKIP
[typecheck] §8.10 B0901: SKIP
[typecheck] §8.10 B0902: SKIP
[typecheck] §8.10 B0903: SKIP
[typecheck] §8.10 B1001: SKIP
[typecheck] §8.10 B1002: SKIP
[typecheck] §8.10 B1101: SKIP
[typecheck] §8.10 B1102: SKIP
[typecheck] §8.10 B1103: SKIP
[typecheck] §8.10 B1201: SKIP
[typecheck] §8.10 B1202: SKIP
[typecheck] §8.10 B1203: SKIP
[typecheck] §8.10 B1301: SKIP
[typecheck] §8.10 B1302: SKIP
[typecheck] §8.10 B1303: SKIP
[typecheck] §8.10 B1304: SKIP
[typecheck] §8.10 B1401: SKIP
[typecheck] §8.10 B1402: SKIP
[typecheck] §8.10 B1403: SKIP
[typecheck] §8.10 B1404: SKIP
[typecheck] §8.10 B1405: SKIP
[typecheck] §8.10 B1501: SKIP
[typecheck] §8.10 B1502: SKIP
[typecheck] §8.10 B1503: SKIP
[typecheck] §8.10 B1504: SKIP
[typecheck] §8.10 B1505: SKIP
[typecheck] §8.10 B1506: SKIP
[typecheck] §8.10 BVDT: SKIP
[typecheck] §8.10 BHTF: SKIP
[typecheck] §8.10 BOUT: SKIP
[typecheck] GATE T: FAIL (1 pixel beats, 0 sweep, 0 shape)
[typecheck] (Gate T is the type-size check: it measures the smallest text in each beat of the finished film and fails any beat whose text is too small to read on a screen. TYPECHECK.md lists which beats and why.)
[art final] GATE T BLOCKED: the type-size check found text too small to read. TYPECHECK.md lists each one — fix before final cut.
[art final] See: /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-the-game-trailer/TYPECHECK.md
```

## 2026-11-13 21:58 - stages: resheet, card, capture, review, final, checks

`python3 make_film.py 22 ...` exit 0, 5 s
- claude-liam-lecture-key-terms-the-game-trailer: 58 beats (52 deck steps), 58 already voiced, about 17.1 min
`python3 -c import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))) beat_sheet.json ...` exit 0, 1 s
`python3 bookends.py claude-liam-lecture-key-terms-the-game-trailer ...` exit 0, 57 s
- bookends: BOPEN: 1 drawn frames, 14.88 s; BIDEA: 286 drawn frames, 17.42 s; BDEFS: 761 drawn frames, 34.92 s; BVDT: 444 drawn frames, 21.75 s; BHTF: 419 drawn frames, 18.50 s; BOUT: 1 drawn frames, 3.92 s; portrait: /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/professor-bear/professor-bear-1x1-69.jpg
`python3 deck_capture.py claude-liam-lecture-key-terms-the-game-trailer ...` exit 0, 4 s
- captured 52 deck beats into /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-the-game-trailer/media
`art run claude-liam-lecture-key-terms-the-game-trailer --height ...` exit 0, 313 s
- [run] GATE L — beat-mix lint
- [run] GATE SHAPE — finance chart-shape enforcement
- [run] GATE V — frame-level visual QC on the compiled reel
- [gate-v] frames=116 BLOCKER=0 MAJOR=0 → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-the-game-trailer/_qc/REPORT.md
- [run] done → /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-the-game-trailer  (QC gates: on)
`art final claude-liam-lecture-key-terms-the-game-trailer --local ...` exit 2, 14 s
```
[typecheck] §8.10 B0602: SKIP
[typecheck] §8.10 B0603: SKIP
[typecheck] §8.10 B0701: SKIP
[typecheck] §8.10 B0702: SKIP
[typecheck] §8.10 B0801: SKIP
[typecheck] §8.10 B0802: SKIP
[typecheck] §8.10 B0803: SKIP
[typecheck] §8.10 B0901: SKIP
[typecheck] §8.10 B0902: SKIP
[typecheck] §8.10 B0903: SKIP
[typecheck] §8.10 B1001: SKIP
[typecheck] §8.10 B1002: SKIP
[typecheck] §8.10 B1101: SKIP
[typecheck] §8.10 B1102: SKIP
[typecheck] §8.10 B1103: SKIP
[typecheck] §8.10 B1201: SKIP
[typecheck] §8.10 B1202: SKIP
[typecheck] §8.10 B1203: SKIP
[typecheck] §8.10 B1301: SKIP
[typecheck] §8.10 B1302: SKIP
[typecheck] §8.10 B1303: SKIP
[typecheck] §8.10 B1304: SKIP
[typecheck] §8.10 B1401: SKIP
[typecheck] §8.10 B1402: SKIP
[typecheck] §8.10 B1403: SKIP
[typecheck] §8.10 B1404: SKIP
[typecheck] §8.10 B1405: SKIP
[typecheck] §8.10 B1501: SKIP
[typecheck] §8.10 B1502: SKIP
[typecheck] §8.10 B1503: SKIP
[typecheck] §8.10 B1504: SKIP
[typecheck] §8.10 B1505: SKIP
[typecheck] §8.10 B1506: SKIP
[typecheck] §8.10 BVDT: SKIP
[typecheck] §8.10 BHTF: SKIP
[typecheck] §8.10 BOUT: SKIP
[typecheck] GATE T: FAIL (1 pixel beats, 0 sweep, 0 shape)
[typecheck] (Gate T is the type-size check: it measures the smallest text in each beat of the finished film and fails any beat whose text is too small to read on a screen. TYPECHECK.md lists which beats and why.)
[art final] GATE T BLOCKED: the type-size check found text too small to read. TYPECHECK.md lists each one — fix before final cut.
[art final] See: /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-key-terms-the-game-trailer/TYPECHECK.md
```
