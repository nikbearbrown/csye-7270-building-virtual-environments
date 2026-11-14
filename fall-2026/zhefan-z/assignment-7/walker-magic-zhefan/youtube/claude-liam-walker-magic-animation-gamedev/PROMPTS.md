# PROMPTS — the prompts on screen and the prompts that made this film

## On screen

- **B00 — Reconstructed prompt** (not a saved chat; written for the film from what the assignment did): "Please use Walker to convert my game design document about a fire mage and a cave wolf into two animation clips: a run cycle that loops and a lunge that commits — each pinned first, keyed as data in the scene files, read back by tests and checked tick by tick against the game." The output lines under it are real results (clip settings from the scene files; test counts from the logs: pin 16 / 0, edges 25 / 0).
- **B27 — Suggested prompt** (for the viewer): "Please use Walker to add in-between frames to my mage's run so the planted foot stops sliding. First predict, in pixels, how far the body moves while one cell is held at 110 px/s and 10 fps; then measure the foot in a windowed Movie Maker strip, and show the behaviour pin still matches tick for tick." It targets the author's own next test (FRICTIONAL.md:26, "in-betweens for the planted foot"), asks for a prediction first, and keeps the pin as the check that gameplay did not move.

## The film's own prompts

- `prompt-6-film.txt` (committed at f860fed), Part 2: the first cut — one landscape explainer for Assignment 7 with the walker modifier, real engine footage first, every number from the sources, fixtures labelled, MP3 and MP4 out of git.
- `prompt-9-film.txt` (committed at ad7935f), Part 2: bring the film in line with the published film requirements, seven items (listed in FACTCHECK.md, "Requirements"), keep what already meets them, capture new scripted-input footage of a hit in GROWL, LUNGE and RECOVER, about 6–7 minutes, re-run the checker and `art final`, set `human_review_approved` back to false. The build was delegated by the parent Claude Code session, which listed the documents' known inaccuracies (FACTCHECK.md "Corrections") and the rule that this build does not commit.
