"""narration.py — every spoken line of the lecture, in beat order. Liam, in for Bear (Kokoro am_onyx).

Film 1 of 3 of "CSYE 7270: Start Here". The film is FOR the course CSYE 7270, so the course is named (metadata.course) in BOPEN and BIDEA only.
Sources (viewer-facing: ideas only, no book or chapter named): the real Walker records in walker-jumpman and walker-jumpman-clawd
(see _conducting-series-evidence/walker-evidence/conducting-records.md, exact file:line for every number) and the supervision ideas in
INFO 7375 (conducting AI, solve-verify asymmetry, five capacities, computational skepticism). None of those sources discuss games: the
game mapping is labelled as the course's own extension (B15).
Rules: "three-D model" for a 3D model, "A. I. model" for an AI model (Bear, 2026-10-06). Numbers are spelled out so Kokoro reads them as meant.
Acronyms Kokoro mangles are spelled out in the narration only; on-screen text keeps the real spelling.
"""

SLUG = "claude-liam-lecture-csye-7270-conducting-ai-for-games"
TITLE = "Conducting AI for Games"
GREETING = "Ciao"
SERIES = "CSYE 7270: Start Here"
COURSE = "CSYE 7270"
VIDEO_NUMBER = 1
VIDEO_COUNT = 3
TITLE_LINES = ["Conducting", "AI for Games"]
OPENING_DESCRIPTION = "What the AI does, and what stays with you"

BOPEN = ("C S Y E seven two seven zero, Start Here. Conducting A. I. for Games. "
         "Learn what the A. I. does when it builds a game, what stays with you, and how to tell the difference.")

ACTS = [
    ("I", "The Empty Podium"),
    ("II", "What the AI Does, What You Do"),
    ("III", "A Real Record"),
    ("IV", "Why You Check the World"),
    ("V", "How the Course Works"),
]

# (beat_id, act index, narration)
BODY = [
    # ── ACT I · the empty podium ─────────────────────────────────────────────────────────
    ("B01", 0, "In this course, the A. I. writes the code. Claude Code or Codex reads your project, edits it, runs it, and reports back. You do not type the game."),
    ("B02", 0, "That sounds like less work. It is different work. And it is the work this course teaches."),
    ("B03", 0, "Picture an orchestra where every player has just got better. Every instrument improved, and nobody is conducting. Each player is brilliant. Nobody is holding the whole performance. The podium is empty."),
    ("B04", 0, "That is a game built by an A. I. with nobody directing. Each script can be fluent. Each scene can look right. And the game can still be wrong, because nobody held the whole thing."),
    ("B05", 0, "So the question for this course is not, can the A. I. write the code? It can. The question is what is left for you, and how to do it well."),

    # ── ACT II · what the AI does, what you do ───────────────────────────────────────────
    ("B06", 1, "Start with an asymmetry. Making an answer and checking an answer are different jobs. The A. I. made the first one cheap. It did not make the second one cheap."),
    ("B07", 1, "And it gets harder, not easier. The faster the A. I. makes things, the more there is to check. The channel for making gets wider. The gate for checking stays person-sized."),
    ("B08", 1, "Be careful with that claim. It is an argument with limits, not a law. A tool that runs your game and measures it does check something. But a person chose that check. And a person decides whether the result is what was meant."),
    ("B09", 1, "Now the split, as this course uses it. The A. I. does the typing: scenes, scripts, placeholder art, repeated variants, and tests from a clear description."),
    ("B10", 1, "You do the deciding. You decide what the game is for, and who it is for. An A. I. will build any version you hand it, flawlessly, including the wrong one."),
    ("B11", 1, "You hear that something is wrong before any check says so. A jump that cannot clear the gap. An enemy that cannot be dodged. A number that is too perfect."),
    ("B12", 1, "You choose which checks matter, and you look at the real running game, not the report about it."),
    ("B13", 1, "You judge whether it is fun, whether it is fair, whether it means what you intended. Taste and intent are yours."),
    ("B14", 1, "And you sign what ships. The A. I. faces no consequence. You do."),
    ("B15", 1, "One honest note. These ideas come from teaching people to supervise A. I. in medicine, law and software. Games are where this course applies them. That application is ours, and you will be testing it."),

    # ── ACT III · a real record ──────────────────────────────────────────────────────────
    ("B16", 2, "So here is a real record. The course uses a small platformer called Walker Jumpman. An A. I. built it in a day, from one request: build a simple level."),
    ("B17", 2, "Its first run of twenty-five automatic checks failed four. Dead on respawn. Restart counted as a death. A route with no safe landing. The A. I. fixed the game, and the next run passed all twenty-five, seventy-one seconds later."),
    ("B18", 2, "Look at how the record says it did it. The jump tuning and the acceptance tolerances were not weakened. The test stayed hard. The game changed."),
    ("B19", 2, "Then came a second step. Its author wanted the player to be a coding agent, drawn as Clawd, the Claude mascot. One change. Not the whole game."),
    ("B20", 2, "In its change brief, the A. I. named three ways it could go wrong. The wide body might overhang the collision box. A jump animation on a jumping body might make two jump arcs. And eighteen animations might be mistaken for eighteen abilities."),
    ("B21", 2, "Then it changed the drawing and the animation choice only. The physics, the tuning, the level and the hazards were left alone. A separate test compared one thousand nine hundred and forty-four numbers against an independent reference."),
    ("B22", 2, "The first prediction held up. The arms stick out past the left edge of the world. The record does not hide it. It leaves it open, for a person to judge in play."),

    # ── ACT IV · why you check the world ─────────────────────────────────────────────────
    ("B23", 3, "Now the part that matters for this course. The machine checks were not always right. One recording of the gallery came with a receipt that said pass. It held three hundred and forty-three frames. The plan needed five hundred and forty."),
    ("B24", 3, "The A. I. noticed, rejected the recording, kept it as evidence, and changed its method to require six hundred frames."),
    ("B25", 3, "Another recording ended with exit code zero, the code that means success. It had no completion receipt, and only four hundred and sixteen of six hundred frames. In the record's own words: exit code zero did not establish success."),
    ("B26", 3, "Even careful wording can outrun its check. The record says the physics function is byte-identical. True. That check compares one function. The same file changed by thirty-three lines."),
    ("B27", 3, "That is the asymmetry, in a real project. A success statement records what was said. The state records what actually changed. You read the state."),
    ("B28", 3, "And these records were written by the A. I. itself. They are candid. But look for the human finding in them. There is none. The human play-test is still marked pending. Eight design questions are still open, each with a person's name on it."),
    ("B29", 3, "That is not a flaw to hide. It is the point. The machine can tell you a hundred things passed. Only a person can say whether it is fun."),

    # ── ACT V · how the course works ─────────────────────────────────────────────────────
    ("B30", 4, "So here is how this course runs. You direct Claude Code or Codex to build real games in Godot, an engine you will meet in the next film."),
    ("B31", 4, "You start from a brief you write. You ask for one change at a time. You predict how it can fail before it is built, and you choose the check."),
    ("B32", 4, "You keep a log: what the A. I. did, what you decided, what you doubted. That log is the evidence of your work."),
    ("B33", 4, "Two more films complete this start. Why Godot. And what Walker is: the rules the A. I. works under."),
    ("B34", 4, "Anyone can use an A. I. to write code. This course is about conducting it."),
]

BIDEA = ("Ciao. This is Liam, in for Bear. In C S Y E seven two seven zero, an A. I. writes the code for your games. "
         "The shortcut is to think that leaves nothing for you to do. This film is about the opposite: what is left, and why it is the whole job.")

BDEFS = ("Five terms. Conducting means directing an A. I.'s work: choosing the goal, hearing what is off, and deciding what goes out. "
         "A coding agent is an A. I. that reads your project, edits it, and runs commands. "
         "To verify is to check an answer against the real thing, not against the A. I.'s say-so. "
         "A receipt is a saved record of what a check found. "
         "And play-feel is whether a game feels right in the hands, which only a person can judge.")

BDEFS_TERMS = [
    ("Conducting", "directing an AI's work: the goal, the doubt, the decision"),
    ("Coding agent", "an AI that reads your project, edits it, and runs commands"),
    ("Verify", "check against the real thing, not the AI's say-so"),
    ("Receipt", "a saved record of what a check found"),
    ("Play-feel", "whether a game feels right in the hands"),
]

BIDEA_TEXT = ("An AI writes the game,\nso there is nothing left for me to do.", "so there is nothing left for me to do",
              "and everything left is mine to decide")

BVDT_HEADING = "Conducting AI for Games"
BVDT_LINES = [
    "The AI writes the code. You conduct it.",
    "Making is cheap now. Checking is not.",
    "You decide what the game is for.",
    "You hear what is wrong, and choose the check.",
    "A passing check is a claim, not the game.",
    "You judge the feel, and you sign what ships.",
]
BVDT_NARRATION = ("Let's recap with Claude. The A. I. writes the code. You conduct it. "
                  "Making is cheap now. Checking is not. "
                  "You decide what the game is for. "
                  "You hear what is wrong, and choose the check. "
                  "A passing check is a claim, not the game. "
                  "You judge the feel, and you sign what ships.")

BHTF_PROMPT = ("I want to make a small game. Before you write any code, ask me what the game is for and who it is for. "
               "Then tell me three ways it could be built wrong that would still run, and the check that would catch each. "
               "Wait for my answer before you build anything.")
BHTF_CHECKS = ["Check: can I say what each wrong version would look like on screen?",
               "Check: I choose the first thing to test, not the AI."]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT +
                  " Then check two things yourself. Can you say what each wrong version would look like on the screen? "
                  "And did you, not the A. I., choose the first thing to test?")
BHTF_SEGMENT = "Predict It, Then Check It"
TOPIC = "CSYE 7270 · CONDUCTING AI FOR GAMES"
TAGS = ["CSYE 7270", "Conducting AI", "Game development", "Godot", "Walker", "AI agents", "Claude Code", "Nik Bear Brown"]
