# Build the prepared lecture

You are running from `/Users/bear/Documents/CoWork/bear-textbooks/books`. This is stage two of the lecture skill. Read this file completely, then build the film. Keep the prepared narration and teaching design. Fix the smallest failing unit when a gate fails, and log the change. No paid generation, staging, publishing, or git push is authorized or needed.

## Identity and scope

- Title: Triggers and Colliders in Godot
- Course and playlist: CSYE 7270 Building Virtual Environments
- Voice: Liam, in for Bear; free local Kokoro am_onyx; channel @NikBearBrown
- Reel: /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot
- Toolkit: /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art; never substitute a hyphenated or underscored sibling.
- Skill: /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/skills/make/lecture/SKILL.md
- 29 beats: opening three, four act cards, 19 body beats, closing three. About 6:14 is an unmeasured estimate, not a timing constraint.
- 4 Manim classes, literal Scene subclasses in one self-contained scenes.py for Gate A.

## What is complete

Read these absolute paths:

- /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/NARRATION.md — spoken text
- /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/content.json — authoritative body and bookend content; make_sheet.py regenerates the sheet
- /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/make_sheet.py and /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/beat_sheet.json — complete sheet, measured-audio preservation
- /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/scenes.py — custom mechanisms and measured charts
- /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/ACTS.md — full-source coverage and explicit omissions
- /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/SHOTLIST.md — lane auditions, source rungs, motion claims
- /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/FACTCHECK.md — corrections, tested and untested claims
- /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/SOURCES.md — local sources and official URLs
- /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/CHECKS-REPORT.md — preparation checks; final gates remain unrun
- /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/godot/project.godot — isolated scripted lab, not a finished game
- /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/evidence/physics-results.json and /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/evidence/supplemental-results.json — 32 passing checks
- /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/evidence/rendered-lab.log and /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/evidence/supplemental.log — current successful logs
- /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/evidence/source-audit.json — exact recorded static-search argv and output
- /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/evidence/source-hashes.json — artifact provenance
- /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/evidence/excerpt-map.json — code excerpt source ranges
- /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/captures — real native engine and official documentation captures
- /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/CAPTURE.md — evidence reproduction, only if changes justify rerunning
- /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/CONVENTIONS.md — suggested class-project policy, not edits to another repository

The real evidence was captured and inspected. The film stills and audio have not been generated. Do not mark a rendered gate passed on the strength of preparation checks.

## Commands, in order

Run these from books/. Every reel path is absolute.

```bash
python3 /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/validate_package.py
python3 /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/scripts/generate_audio_kokoro.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot
python3 /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/prepare_audio.py
python3 /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/make_sheet.py
python3 /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/scripts/align.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot
python3 /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/prepare_opening.py
python3 /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/preflight.py
```

Now LOOK at every generated Manim end frame and Remotion 25/50/95% frame. Build a labeled contact sheet, inspect it, and log what was actually seen. Check the custom equations at 15/50/85% in their final 16:9 composition. Inspect all long code lines and actual documentation camera targets. Rewrap or split only a failed visual unit without changing its claim; retain exact executed source and evidence attribution. Do not accept tiny unreadable type to keep a line on screen.

Check word alignment against the real speech. scenes.py resolves named phrase cues from mp3/words.json and otherwise uses relative fallbacks; verify the matched cue format against current align.py output. Refine cue timing when a fallback or line highlight lands early. That is timing repair, not permission to rewrite the lecture. Code lineCues are provisional until aligned. Re-run make_sheet after any measured audio change, then align again if needed.

Once stills are acceptable:

```bash
./brutalist.art/art run /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot --height 2160
python3 /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/scripts/type_check.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot
./brutalist.art/art final /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot --height 2160 --fps 24 --out /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/exports/landscape
python3 /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/scripts/bookend_check.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot
```

Render Remotion through the toolkit's runtime/scripts/remotion_scenes.py, in the foreground. Never hand-roll npx remotion render, skip a gate, or fabricate an approval record. Keep superseded clips in /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-triggers-and-colliders-in-godot/_superseded/ before rebuilding an affected unit. The normal compiler must rebuild body beats; no verified_body_reuse shortcut is authorized for this unrendered film.

## Timing and bookend contracts

- BOPEN says the course, exact title, then a brief purpose. The fully populated portrait card appears at frame zero and holds for measured narration. prepare_opening.py uses the approved title template and writes media/BOPEN.mp4; compiler muxes the narration.
- Portrait is seeded by this reel slug; evidence/portrait-selection.txt records the selection. Label it Professor Bear, with Liam narrator credit.
- BIDEA has 0.8 s lead silence and its full correction must finish. BDEFS has four prerequisite terms.
- BVDT has 0.5 s lead silence and four recap sentences, two at a time.
- BHTF props.command is exactly the narration. Show the two learner checks.
- BOUT speaks the exact title and “At Nik Bear Brown.”; 1 s silent tail; no music or subline.
- prepare_audio.py applies declared pauses once, hashes the output, and measures it. If the current TTS script already applies these exact pauses, inspect the files first and avoid double-padding; document any adaptation.
- Runtime follows measured audio. Do not speed up speech or stretch action to hit the estimated 6:14.
- No video numbers, series counts, burned captions, or fabricated live sessions.

## Known traps and evidence limits

- Current BOPEN integration explicitly uses shot.type CARD; legacy JSON schema excludes it. Runtime validation accepts the mandated contract. Do not rewrite shared schema or drop the required opening to appease that legacy mismatch.
- Physics step distance is not a guarantee against tunneling. B38 shows an actual swept counterexample, not a failed collision that we hid.
- 72 px is the continuous jump design target. The measured apex is about 75.23 px and the illustrative ±10% band is 64.8–79.2 px. Keep those distinctions.
- Native outputs are scripted experiments, not normal-input playthroughs. Platform displacement is tested; carrying/leaving behavior is not. Enemy latch/bounce is tested; simultaneous corner priority is not. Drop-through clearance and device-wide stability are not claimed.
- A first graphics attempt used a nonexistent own_world_2d property; corrected to world_2d. A second set the canvas transform before attachment; corrected order. Those old errors remain in first/second-attempt logs; current successful logs have neither error.
- One versioned Nodes and Scenes URL showed a security page. The ordinary stable URL succeeded and is recorded as the resolved URL. Never use the security-page capture as lesson evidence.
- Documentation uses its own appearance; conceptual diagrams use the lecture palette. Do not pretend a conceptual diagram is an engine screenshot.
- No external course reference game was supplied. Do not claim it was audited or modified.

## Required exit checks

All normal fact, static/render, visual, typography, audio and bookend gates must PASS. Inspect final 3840×2160 frames across every act, listen to all narration, check GDScript/API pronunciations and course name, confirm exact closing speech plus silent tail, and verify final runtime against the audio sum and frame rounding. Probe the actual master and record its absolute path and measured duration. A file existing is not a visual or audio pass.

STOP after the verified master. Report its absolute path, measured runtime, lane histogram, and any failed or unrun check. Do not stage, publish, or push.

B46A now uses a labeled official-document excerpt in ClaudeCodeBeat. Its four short quotations match sources/docs-migration.txt. A later live recapture was rate-limited; do not replace this beat with the unrelated table visible in the older migration PNG.


## Split-film additions

This film is a standalone lesson, not the combined source lecture. Only classes and beats in its content.json are in scope. Run all commands against this reel. Source modifications belong here; do not modify the original combined reel. New comparison evidence adds 21 checks; it is separate from the inherited 32. Do not add those counts as if all cases were re-executed for each film.

Read evidence/excerpt-map.json for derived hierarchy and explicitly selected-line excerpts. BT10 describes a damage-timer policy, not a tested implementation. Multiple-actor door races, save persistence, force sweep validation and scene deletion while occupied remain outside the recorded experiment. Keep those limits in the narration.
