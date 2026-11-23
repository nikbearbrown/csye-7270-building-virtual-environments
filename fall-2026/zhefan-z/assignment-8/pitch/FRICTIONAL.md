# FRICTIONAL — Assignment 8 (pitch film)

Zhefan Zhang (zhefan-z). Written with claude.ai from my sessions of 2026-11-20 to 2026-11-22 (my words translated from Chinese where needed). claude.ai planned and drafted the documents and prompts; Claude Code (Opus 5.5, manual permissions) checked them, captured, built the film and committed at my request; I made every decision below.

## 2026-11-20 — choosing the project

- **My choices:** an HD-2D vertical slice of my walker-magic game, a Windows desktop build, target role gameplay programmer. I picked HD-2D knowing it is the riskiest option, because the 2D-to-3D move is a real, nameable risk and my Assignment 7 pin is a ready test for it.
- **Comparable games:** only games I have played: Octopath Traveler, Metal Slug, Hollow Knight. claude.ai drafted their one-line descriptions; I confirmed each matched what I played.
- **Overruled a suggestion:** claude.ai suggested building a one-room HD-2D prototype first so the pitch could show 3D running. I chose not to; everything 3D in the film is labelled constructed.
- **Added during the discussion (mine):** a flashier look from simple renderer features (depth of field, bloom, fog, the fireball as a light, set dressing, hit-stop, a boss entrance) and four short, skippable story scenes with portraits.

## 2026-11-20 — the concept portraits (Gemini 4)

- The first full-body witch came back with a glowing halo above her head. claude.ai pointed out that a halo like that is the signature of another game's characters; I had Gemini remove it. The halo versions were not kept (recorded in `ART-PROMPTS.md`).
- Three-quarter "talking" dialogue portraits did not work: Gemini kept drawing her facing front. I used a 2×2 expression sheet instead (curious, determined, victory, sad).
- I asked Gemini to make her look like a more experienced adventurer; my exact wording was not kept. The two full-body images then had different skirts and boots; I regenerated until they matched, and used only that set.
- Some versions came back on a white background, which is hard to cut out around her white hair. claude.ai suggested framing the portraits in boxes instead of cutting them out.

## 2026-11-21 — the assignment changed

- The first film (3:37) followed the Canvas text. While building it, Claude Code read `origin/main` and found the instructor's updated Assignment 8 (`135fc9d0`, 2026-11-20): the film is now built from a GDD, with the game in brief, sixteen GDD beats and an appendix. Canvas still showed the original. I decided to meet both versions.
- **Scope changes (mine, logged here as the assignment allows):** one level became two to three short levels with the boss last; the Assignment 4 "Great Hearth" story became a simple one (cross the cave, beat the great wolf); no save system (a campfire is only a rest and restart point); the heal spell is found in the first chest; the frame-rate target is 60 fps at 1080p on my RTX 5060 laptop, to be measured.
- claude.ai drafted `GDD.md` 2.0 from my answers and my Assignment 4 GDD.

## 2026-11-21 — mistakes caught before they were committed

Claude Code checked every "Built" claim against the game at `840b501` and stopped before committing. Each of these was a claude.ai drafting error:
- The Jump row said "only from the ground"; the game allows a jump 0.08 s after leaving an edge and buffers a press 0.10 s before landing (`tuning.gd`).
- The GDD called my Assignment 4 GDD "version 1.0"; the PDF has no version number. It is now cited as the Canvas PDF of 2026-10-15, with a copy in `A4-GDD.pdf`.
- `ART-PROMPTS.md` gave the film's label wording wrongly and said two images were on white when the files I kept are on green.
- The brief called "2D sprites placed in 3D" new to me; my Assignment 3 prop room already had the mage as a static billboard. Corrected to: a whole 3D level where the sprites run and fight is new.

## 2026-11-21 — the rebuilt film failed a gate

The GDD-based rebuild ran 7:11. Its first final export failed the render-integrity gate: a pale drawing on the question 1 card scored 0.24 contrast against a floor of 0.30. Claude Code darkened it; the re-run passed.

## 2026-11-22 — cutting to under four minutes

- **My proposal:** keep the full GDD in the documents and cut the film to 3:30–3:55 around the seven questions. claude.ai pointed out that the updated assignment requires every GDD section as its own beat in the film (7 points). **My decision:** keep all sixteen beats but cut each to one short sentence.
- Claude Code reached 3:46 without dropping a required beat. It caught its own labelling slip first (one combined beat labelled all three revisions "Assignment 5" and gave one frame rate for captures at two rates) and fixed it before the export. Both gates passed on the first run.
- Lost in the cut: the hit during the lunge (the dash that cannot be cancelled) is no longer on screen; the GDD and earlier captures still record it.
- I watched the final film and uploaded it to Google Drive with link sharing.

## Who did what

- **Me:** the project, the role, the scope and every cut; the comparable games I played; the story, the four scenes and their lines; generating every portrait in Gemini and choosing which to keep; deciding to meet both versions of the assignment; watching the film.
- **claude.ai:** the brief, GDD, art-prompt record, README and this file, drafted from my answers; the image prompts; the prompts for Claude Code.
- **Claude Code:** checking every claim against the code and the records; the captures; the stills, narration, film and gates; the build records; the commits I asked for.

## Still open

- Whether the gameplay stays a 2D layer with a 3D backdrop or moves to 3D bodies held to a plane: the one-room test will decide.
- Two levels or three.
- The campfire line is not written yet.
