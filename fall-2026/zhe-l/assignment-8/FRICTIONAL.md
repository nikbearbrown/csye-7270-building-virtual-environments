# FRICTIONAL — Final project pitch (Assignment 8)

My Assignment 7 log is in `../assignment-7/FRICTIONAL.md`.

## Entries

### 2026-11-25 — Choosing the final project, writing PROJECT-BRIEF and the beat sheet

- **Date and what I was working on:** 2026-11-25. Reading the assignment, deciding what the final project is, writing the seven answers as `PROJECT-BRIEF.md`, turning them into a one-picture-per-beat `beat_sheet.json`, translating the narration into English and trying it with the voice.
- **I tried / expected:**
  - My original idea was an extraction shooter in the spirit of Escape from Tarkov. But shooting and extraction already have many examples, and a game that only does those would be ordinary. So this demo puts the tablet system first.
  - I had Claude sort out what exists and what will exist, then discussed with it what the film should contain, what to stress, and what to ask the instructor.
- **What happened:**
  - One of the risks Claude listed was a "keyboard conflict": the world does not stop while the tablet is open, so what happens to WASD while typing? This does not hold: my design already settles it (with the tablet in both hands the character cannot walk and every key goes to the tablet; with one hand, the keys only control the character), and it is written in my game map. Claude wrote the risk without checking.
  - Claude said "our verification records are more complete than most of the class". I asked where it saw that: it had not looked at any other student's work, so the claim had no basis. It withdrew it, and the film does not say it.
  - At first Claude said "the memo is just a tool inside the tablet; it does not touch the world", and suggested that the first piece be an app that changes the world. I explained the memo design: a quest gives only the final goal, each faction writes its testimony in memos, and the player copies, compares and finds the holes, then acts in their own way, so the memo itself is part of interacting with the world. Claude recorded this design in my game map.
  - Translating the comparable games, Claude rewrote my "ESC menu" as "pause menu", then caught it itself: it did not know whether The Phantom Pain really pauses when the computer is open, and a wrong statement there would be a false claim about another game, so it went back to my words.
  - The toolkit's show-tell opening ("Liam, in for Bear"), its "Your Turn" beat and its closing ("At Nik Bear Brown") carry the instructor's name and credit line, which this assignment does not allow. The narration speaks as me (Zhe Liu) instead, and those beats are declared exempt. Whether the gates complain about that is a question for the instructor.
  - The first narration, estimated from its length in Chinese, came to about 5 minutes, over the 4-minute limit. Cutting repeated wording and then four pieces of content (the code examples only on screen, the hours in one sentence, and so on) brought the measured English voice to 210.8 s.
- **What I did:**
  - Decided: the final project is built around the tablet system; the target role is technical game designer, and the readers are recruiters and hiring managers; the export is a Windows desktop build on Forward+; what it does not do for now is shooting, extraction and looting (they will come later); the first piece is the smallest clue loop; the proof is real captured play; the keys are explained only in the README; the risk is "too big for one person", answered by building the core idea first, writing code that is easy to fix and extend, and commissioning the art from a friend.
  - Gave the comparable games and my own observations: Metal Gear Solid V: The Phantom Pain (about 320 hours), Subnautica and Abiotic Factor (more than 100 hours each), and Escape from Tarkov. I have played Barotrauma for 900 hours, but it did not give me much inspiration for this, so it is left out.
  - Went through all 19 beats one by one and changed several: the quest example became "find this thing for me"; the technical points are kept short, and the narration does not name assignments; "drives that are plugged in" was removed; I listened to the English voice and approved the pronunciation.
- **What Claude or another person contributed:** Claude Code (Claude Opus 5.5) read my design document, my game map and my earlier assignment records, sorted out the exists / will-exist lists, drafted PROJECT-BRIEF, the 19 beats' narration and its English translation, estimated the length and proposed the cuts, and made a trial voice with the local Kokoro am_onyx voice. All four mistakes above were Claude's: I pointed out the first three, and it caught the fourth itself.
- **What I understand now / still do not understand:**
- **Evidence and next step:** `pitch/PROJECT-BRIEF.md` and `pitch/beat_sheet.json` (uploaded once translated); the trial voice stays in my local film folder and is not uploaded. Next: upload the project copy and capture real play.

---

### 2026-11-25 — Uploading my current project, comments stripped, as the A8 starting point

- **Date and what I was working on:** 2026-11-25. Everything the film calls "existing" has to point to a commit, but the tablet system, This PC, the ThoughtPad window and the two-handed hold were only in my working folder. I put the current project into `assignment-8/` in the course repository.
- **I tried / expected:** My working project's code comments are in Chinese, and the course repository must not contain Chinese. I decided to remove the comments instead of translating them; all that matters is that the behaviour is unchanged. The animation tests (the five A7 scripts) are not ported this time.
- **What happened:**
  - My working project was snapshotted at 23:19; everything after that was done on the snapshot, and the working project was not touched.
  - The comments were removed from 33 GDScript files and 2 shaders; a line-by-line check confirmed that only comments, blank lines and the lines loading the Chinese translations were removed.
  - Removing comments was not enough: the translation tables had a Chinese column, and the debug stand-in data, the context-menu test labels and two software definitions (`.tres`) held Chinese strings; the two ATTRIBUTION files were in Chinese. The Chinese columns were dropped and the rest put into English. The two `.tres` files are normally generated from my item spreadsheet by a conversion script; this time they were edited by hand in the uploaded copy only.
  - The conversion script `tools/convert_file_types.py` and my game map are in Chinese and are not uploaded this time.
  - The six tests were run on the snapshot with comments and on the stripped copy, with the same results: 55 / 29 / 157 / 27 / 110 / 41 PASS, every exit code 0. The first import printed 8 lines saying a `.translation` file could not be opened (those files are generated during import); the test logs after that contain no errors.
- **What I did:** Decided to remove the comments instead of translating them; decided not to port the animation tests this time (so beat B12 now says "the screen glow and the effects have automated tests"); decided to upload the current version; decided on `assignment-8/` as the folder.
- **What Claude or another person contributed:** Claude Code (Claude Opus 5.5) wrote the scripts that strip the comments, check each line and replace the strings with English, translated the two ATTRIBUTION files, ran the pre-upload checks (no Chinese, no local paths, no keys or large files), and ran the tests twice.
- **What I understand now / still do not understand:**
- **Evidence and next step:** `walker-survival-shooting/godot/`, `walker-survival-shooting/logs/`, `walker-survival-shooting/scripts/run-test.sh`. Next: capture the film's real play from this commit.

## GitHub pushes

| Date | Commit note |
|---|---|
| 2026-11-25 | First A8 upload: the project copy with comments stripped (snapshot of 23:19), the test logs, run-test.sh, and this FRICTIONAL. |
