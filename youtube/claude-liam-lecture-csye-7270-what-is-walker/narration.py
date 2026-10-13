"""narration.py — every spoken line of the lecture, in beat order. Liam, in for Bear (Kokoro am_onyx).

Film 3 of 3 of "CSYE 7270: Start Here". FOR the course CSYE 7270, so the course is named (metadata.course) in BOPEN and BIDEA only.
Sources: the Walker framework repo (rules with file:line in the scratchpad brief), the REAL publisher run on 2026-10-09
(_conducting-series-evidence/walker-evidence/ANALYSIS.md, installed/), the real conducting records of walker-jumpman and walker-jumpman-clawd
(walker-evidence/conducting-records.md). HONESTY: Walker's rules are conventions, not enforcement; the installed Godot guide is C# while the example
games are GDScript; the public (committed) version installs less than the working tree; no human finding exists in the Clawd records.
Rules: "three-D model" for a 3D model, "A. I. model" for an AI model. Numbers spelled out for Kokoro; on-screen text keeps the real spelling.
"""

SLUG = "claude-liam-lecture-csye-7270-what-is-walker"
TITLE = "What Is Walker, and Why"
GREETING = "Bonjour"
SERIES = "CSYE 7270: Start Here"
COURSE = "CSYE 7270"
VIDEO_NUMBER = 3
VIDEO_COUNT = 3
TITLE_LINES = ["What Is Walker,", "and Why"]
OPENING_DESCRIPTION = "The rules an AI works under, and their limits"

BOPEN = ("C S Y E seven two seven zero, Start Here. What Is Walker, and Why. "
         "Learn what rules an A. I. works under when it builds your game, and how much a rule can actually do.")

ACTS = [
    ("I", "The Problem Walker Answers"),
    ("II", "The Loop and Who Decides"),
    ("III", "What the AI Must Not Do"),
    ("IV", "How the AI Writes Code"),
    ("V", "Walker in Action"),
    ("VI", "What Walker Is Not"),
]

BODY = [
    # ── ACT I · the problem ──────────────────────────────────────────────────────────────
    ("B01", 0, "Walker is a framework for building games with an A. I. agent. It is not a game. It is not an engine. It is written instructions, a few tools, and a way of working."),
    ("B02", 0, "It starts from one sentence. A. I. made execution cheap. It did not make judgment cheap."),
    ("B03", 0, "Walker began as rules for working with Unity, with a hard line down the middle: the agent works the text, the human works the asset layer. That first version was documents. The tooling was never built."),
    ("B04", 0, "Today's Walker targets Godot. It carries an open-source game-building tool called Godogen, under the M I T licence, and keeps its attribution. Walker added a design skill on top, so far only in the working copy."),

    # ── ACT II · the loop and who decides ────────────────────────────────────────────────
    ("B05", 1, "Walker's working loop has six steps. Game brief. Build. Play-test. Inspect. Revise. Export."),
    ("B06", 1, "Each step produces something, and stops somewhere. Build produces a runnable project, not a claim that it is finished. Export produces a package and evidence. Publishing is a separate step."),
    ("B07", 1, "And the split is stated in one line. The agent helps execute and check changes. The human decides what the game should be, and whether it feels right."),

    # ── ACT III · what the AI must not do ────────────────────────────────────────────────
    ("B08", 2, "Now the part you came for: what the A. I. must not do. Start with scope. It must not switch engines silently. It must not cut requirements, stretch the schedule, spend money or publish, just to keep the loop running."),
    ("B09", 2, "Drafting a task is not permission to run it. A direct request for a complete draft allows the draft, with its assumptions named. It does not allow inventing approvals."),
    ("B10", 2, "Next, gates. There are four: vision, systems, world and scope. Only a human signs them. The agent never signs a gate."),
    ("B11", 2, "Then, proof. Judge progress from the running game, never from a clean build. A successful build is not evidence of a successful human play-test. The game's own file adds: never invent human play-tests or test passes. And if a test fails, never weaken the test to make it pass."),
    ("B12", 2, "Then, money and safety. The asset tools call paid services, and every call costs real money, so the agent confirms before the first. Never commit credentials. Writing files on your own computer is not publishing to GitHub. Uploading is a separate action."),
    ("B13", 2, "And finally, size. Make one reviewable change. Predict how it could fail before you build it."),

    # ── ACT IV · how the AI writes code ──────────────────────────────────────────────────
    ("B14", 3, "How the agent writes the code is covered too, in two layers. Layer one is installed in every game: a Godot guide. It says build, then import, then run headless. Verify against the installed Godot instead of guessing its interface. And judge from the running game."),
    ("B15", 3, "Layer two is a set of conventions for G D script. Type every variable. Children talk to parents with signals, never by reaching up the tree. Build small, single-purpose scenes. The Clawd game also keeps each feature's files together."),
    ("B16", 3, "Here is the honest problem. The installed guide assumes C sharp. The example games, and the design skill installed beside it, use G D script. Walker's own readme says the publisher does not yet select a G D script guide."),
    ("B17", 3, "And the G D script conventions are a prompt you can copy, not something the publisher installs. Today, the example games are written in G D script, and the conventions are not written into any game's instructions."),

    # ── ACT V · Walker in action ─────────────────────────────────────────────────────────
    ("B18", 4, "I ran Walker's publisher for real. One command. Six lines of output. It installed fifty-four files: a twelve-line instruction file, a Godot guide, a settings file that ignores generated files, and two skills. No game."),
    ("B19", 4, "Here is the twelve-line instruction file. It tells the agent to build from the design document, not from memory of the chat. To judge progress from the running game. And to finish with a short video of the game, and watch it back before calling the work done."),
    ("B20", 4, "Now the rules at work, on one real change: turning the player into Clawd. One change, not the whole game. Three predicted failures, named in the brief. Physics left alone."),
    ("B21", 4, "The first prediction came true. The broad arms stick out past the left edge, and the character passes in front of world labels. The record leaves it open, for a person to judge in play."),
    ("B22", 4, "The proof rules caught things too. A recording with a pass receipt had only three hundred and forty-three of five hundred and forty frames. Rejected, and kept. Another ended with exit code zero and no receipt. Rejected, and kept. The rule was: preserve failed receipts."),
    ("B23", 4, "And what did a human find? The record holds no human finding. The play-test is marked pending. The four design gates are unsigned. The rule says never invent them, and it was followed."),

    # ── ACT VI · what Walker is not ──────────────────────────────────────────────────────
    ("B24", 5, "So what is Walker not? It is not an enforcer. Gates are recorded in a status file the agent could edit. Walker's own document says gate validation is a convention the skill follows, not code that enforces it."),
    ("B25", 5, "It is not finished. The command-line adapter is still a specification. Walker ships no test framework. And on the day this was recorded, the public version on GitHub installed only the asset tool, an eleven-line instruction file, a Godot guide and an ignore file. The larger kit was not yet published."),
    ("B26", 5, "So why use it? Because a rule written down is a rule you can check the agent against. The value is the habit. Predict. Change one thing. Run the real game. Keep the failed receipts. And leave the judgment to the human."),
]

BIDEA = ("Bonjour. This is Liam, in for Bear. In C S Y E seven two seven zero, the A. I. works under a set of rules called Walker. "
         "The shortcut is to picture Walker as software that stops the A. I. from doing wrong. This film shows what it really is: "
         "a written set of rules and a habit, and what that can and cannot do.")

BDEFS = ("Five terms. Walker is a framework: written instructions and a few tools for building games with an A. I. agent. "
         "A game design document is the written description of what the game is. "
         "A play-test is a person playing the game to see how it feels. "
         "A gate is a point where work stops until a person approves. "
         "And a convention is a rule that is followed because it was asked, not because anything enforces it.")

BDEFS_TERMS = [
    ("Walker", "written instructions and tools for building games with an AI agent"),
    ("Game design document", "the written description of what the game is"),
    ("Playtest", "a person playing the game to see how it feels"),
    ("Gate", "a point where work stops until a person approves"),
    ("Convention", "a rule followed because it was asked, not enforced"),
]

BIDEA_TEXT = ("Walker is software that stops the AI.", "software that stops the AI", "rules the AI is held to")

BVDT_HEADING = "What Is Walker, and Why"
BVDT_LINES = [
    "Walker is written rules and a habit, not software.",
    "The loop: brief, build, playtest, inspect, revise, export.",
    "The human decides what the game is and whether it feels right.",
    "No silent scope, no invented approvals, no weakened tests.",
    "The installed guide and the example games disagree on language.",
    "A rule you can check is a rule you can hold the agent to.",
]
BVDT_NARRATION = ("Let's recap with Claude. Walker is written rules and a habit, not software. "
                  "The loop: brief, build, play-test, inspect, revise, export. "
                  "The human decides what the game is and whether it feels right. "
                  "No silent scope, no invented approvals, no weakened tests. "
                  "The installed guide and the example games disagree on language. "
                  "A rule you can check is a rule you can hold the agent to.")

BHTF_PROMPT = ("Write me a manifest for building a small game with you, in at most twelve lines. It must say what you must not do without my approval, "
               "what counts as proof that something works, and which decisions only I can make. "
               "Then tell me which of those rules you could break without anything stopping you.")
BHTF_CHECKS = ["Check: does each rule name something I can look at in the running game?",
               "Check: do I know which rules are only conventions?"]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT +
                  " Then check two things yourself. Does each rule name something you can look at in the running game? "
                  "And do you know which rules are only conventions?")
BHTF_SEGMENT = "Write the Rules, Then Test Them"
TOPIC = "CSYE 7270 · WHAT IS WALKER"
TAGS = ["CSYE 7270", "Walker", "Godot", "Game development", "AI agents", "Claude Code", "Codex", "Nik Bear Brown"]
