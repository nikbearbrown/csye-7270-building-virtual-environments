# Chapter 0: The toolchain

## MA-ch00.1

A developer starts a Godot editor executable from a terminal window by typing its program name followed by `--path my_game --headless`, instead of double-clicking the editor icon. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The shell is the program that reads the typed line, splits it into a program name and arguments, and starts that program.
- [ ] B. Writing `MY_VAR=1` before the program name passes a flag called MY_VAR to the engine.
- [ ] C. A coding agent can run the same typed command a person would, which is why the command line is a natural way for an agent to start and check a game.
- [ ] D. `--headless` is a flag: an option written after the program name that changes how this one run behaves.
- [ ] E. Accepting typed options means a separate command-line edition of the engine has to be installed, because the editor application takes no options.

**Key:** A=T B=F C=T D=T E=F

**Why:**

- A: The shell interprets the typed command and launches the program; the terminal window displays text and passes keystrokes.
- B: That syntax sets an environment variable for the started process; it is not a flag.
- C: Typed commands are text, so an agent can issue them and read their output and exit status.
- D: Flags are the options a command-line program accepts, and they alter the behaviour of that invocation.
- E: The same executable that opens the editor accepts command-line options.

**Source:** CLI, shell and flags

## MA-ch00.2

A developer runs a Godot project with the `--headless` flag and a test script that drives the game for 600 frames. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. In headless mode the engine loads the scene files but skips running game scripts, since scripts matter when something is drawn.
- [ ] B. Scripts, physics and signals still run, so a test can read a counter, a label's text or which signal fired.
- [ ] C. No window is opened and audio goes to a dummy driver, so the run produces neither picture nor sound.
- [ ] D. A headless run that exits successfully shows the game looks correct on a player's screen.
- [ ] E. A headless test can confirm that a score label is readable on screen by inspecting the frame the engine rendered.

**Key:** A=F B=T C=T D=F E=F

**Why:**

- A: Scripts run normally; headless removes the window and sound, not the logic.
- B: Game logic is unaffected; a headless test observes state, not pixels.
- C: Headless means no display and no audio output.
- D: A successful exit says nothing about what is rendered.
- E: Headless mode draws no frame, so there are no pixels to inspect.

**Source:** Headless mode

## MA-ch00.3

A test script for a game runs without a window. When it finishes, the shell reports the program's exit code. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Quitting with a nonzero code when a check fails lets a script detect the failure without reading printed text.
- [ ] B. A program that prints error messages to its error output has a nonzero exit code, because the two go together.
- [ ] C. A nonzero exit code is a sign of a crash; a test that reports a failed check leaves the code at 0 and signals the failure in its printed text.
- [ ] D. An exit code is a small integer a program hands back to the program that started it, and by convention 0 means success.
- [ ] E. An exit code of 0 shows that the test contained meaningful checks, since an empty test would have failed.

**Key:** A=T B=F C=F D=T E=F

**Why:**

- A: The exit code is the machine-readable verdict.
- B: A program can print errors and still exit 0.
- C: Test programs commonly exit nonzero on purpose when a check fails.
- D: This is the standard process-status convention.
- E: A test with no assertions also exits 0.

**Source:** Exit codes

## MA-ch00.4

A headless test script is supposed to call a quit function after its last check. A bug raises an error before the quit call is reached, and the engine keeps running its main loop with no window to close. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Running the command under a timeout utility turns a stuck test into a failure after a set number of seconds.
- [ ] B. A sensible timeout is longer than a healthy run takes, with some margin.
- [ ] C. The process can run indefinitely: nothing tells it to stop and no window exists to close.
- [ ] D. A timeout speeds up a slow test by telling the engine to skip waiting between frames.
- [ ] E. Because the script's last line calls quit, a timeout adds no protection.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: A timeout turns a hang into a detectable failure.
- B: A limit that is too short kills healthy runs and creates false failures.
- C: With no quit call and no window, the main loop does not end by itself.
- D: A timeout stops the run when the limit is hit; it does not speed anything up.
- E: If an error stops execution before that line, the quit call is not reached.

**Source:** Timeouts

## MA-ch00.5

A developer clones a game project from a repository. The repository holds source images, audio, scenes and small per-asset settings files, but not the engine's generated cache folder. The setup script runs the engine once in import mode before running tests. In Godot terms, check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The cache folder is kept out of version control because it is generated and can be rebuilt.
- [ ] B. The per-asset settings files that record how each asset is imported belong in the repository.
- [ ] C. A missing cache after cloning shows the repository is corrupted.
- [ ] D. Importing rewrites the source image files in place, recompressing their pixels.
- [ ] E. Import converts source assets into the engine's runtime formats and stores them in the cache folder.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: The cache is generated, and the engine reimports when it is missing.
- B: The .import files hold metadata about how assets are imported and are committed.
- C: A fresh clone lacks the cache by design.
- D: Import writes converted copies into the cache and leaves the source file alone.
- E: The engine uses the imported copy at runtime, not the raw PNG or WAV.

**Source:** Import step

## MA-ch00.6

A coding agent has edited several files in a project tracked in a repository. Before accepting anything, the developer wants to know what changed. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A repository is the project's files together with the recorded history of earlier versions.
- [ ] B. A diff shows, line by line, how one version differs from another, such as the working files versus the last commit.
- [ ] C. A commit pushes the change to a shared server so teammates receive it immediately.
- [ ] D. A diff with a few changed lines proves the change works, because a diff lists lines that ran successfully.
- [ ] E. Reading the diff before committing is unnecessary when the agent's own report lists the files it changed.

**Key:** A=T B=T C=F D=F E=F

**Why:**

- A: Version history lets "what changed?" have an exact answer.
- B: A diff records added, removed and changed lines.
- C: A commit records a snapshot in local history; sharing is the separate push step.
- D: A diff records what changed, not whether it behaves correctly.
- E: The report is a claim; stray edits show up in the diff.

**Source:** Repository, diff and commit

## MA-ch00.7

A developer lets a coding agent run shell commands without asking when they match an allow rule. The developer writes one rule for commands starting with `env` and another for commands starting with the game engine's program name. The engine can run a script file given on its command line, and that script may start other programs. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A permission prompt is a chance to review the command or script, not a formality.
- [ ] B. A broad engine rule also lets through code in a script the agent wrote, including code that starts other programs.
- [ ] C. A rule allowing one exact command with fixed arguments is a narrower grant than a wildcard on the program name.
- [ ] D. `env` runs the command given as its arguments, so an `env` rule also allows the program that follows it.
- [ ] E. An allow rule limits what an allowed program does internally once it is running, for example which files it opens.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: The prompt is where a human can catch a command broader than intended.
- B: An allow rule decides which program starts, not what a script run by that program does.
- C: The fewer variations a rule matches, the less it grants.
- D: `env NAME=value program` starts the named program, so the rule is as wide as "run a program".
- E: Allow rules decide which commands start without asking; they do not constrain a running program.

**Source:** Permissions and allowlists

## MA-ch00.8

A coding agent runs in a sandbox that lets it write inside the project folder. During an import step the engine prints an error that it cannot save its settings file, which lives in the user's home directory, yet the import still produces a usable project. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Inside this sandbox the agent can still delete project files, including test output it produced earlier.
- [ ] B. Running in a sandbox confirms that the code the agent writes is correct.
- [ ] C. A sandbox and a permission prompt are one mechanism under two names.
- [ ] D. A sandbox is a technical limit on what a process may read, write or reach.
- [ ] E. The error fits a sandbox blocking a write outside the project folder while writes inside it succeed.

**Key:** A=T B=F C=F D=T E=T

**Why:**

- A: Deleting is a kind of write, and writes inside the workspace are allowed.
- B: A sandbox limits damage; it says nothing about correctness.
- C: A prompt asks a human before a command runs; a sandbox enforces limits on what a running command can touch.
- D: Sandboxes restrict capabilities at the operating-system level.
- E: The settings file is outside the project folder, and the cache is inside it.

**Source:** Sandbox

## MA-ch00.9

Two developers ask a coding agent for a score counter in a two-player paddle game. Developer X writes "add a nice score system". Developer Y lists the observable behaviour (a point goes to the right player when the ball leaves through the left edge), what must not change, which files to read first, how to run the existing checks, and "show me the real command output; do not commit". Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Y's request works as a spec: required behaviour, constraints and a way to check the result.
- [ ] B. Asking for real command output instead of a summary matters: a description is a claim, output can be inspected.
- [ ] C. Adding adjectives such as "robust" and "clean" to X's request turns it into a precise spec.
- [ ] D. X's request leaves the agent to choose where the score is shown, which event changes it and what counts as finished.
- [ ] E. Stating what stays fixed helps, because an agent that is not told may alter related behaviour.

**Key:** A=T B=T C=F D=T E=T

**Why:**

- A: A spec makes "done" decidable; a bare prompt does not.
- B: Output can be checked against a rerun; a summary cannot.
- C: Adjectives add mood, not checkable behaviour or constraints.
- D: Each unstated decision is a place where the agent can build something other than what was meant.
- E: Explicit constraints keep the change bounded.

**Source:** Prompt versus spec

## MA-ch00.10

Yesterday a developer spent an hour in one session teaching a coding agent how to run a project's checks, which need a special flag. Today the developer starts a new session in the same repository and says: "run the checks and fix what fails". No instruction file in the repository mentions the flag. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The agent remembers the flag, because the same underlying model is used and the project is the same.
- [ ] B. The agent deduces the missing flag from the project's name.
- [ ] C. A larger context window lets the agent recall yesterday's session.
- [ ] D. The new session starts without yesterday's conversation; the agent knows what it is given or can read.
- [ ] E. If the agent runs the checks without the flag and they fail, the failure is evidence that the game is broken.

**Key:** A=F B=F C=F D=T E=F

**Why:**

- A: The same model does not carry over a past session's content.
- B: A project-specific flag is written down or discovered; a name does not reveal it.
- C: Window size does not matter; yesterday's text is not in today's context.
- D: Context is the text available now, and a fresh session starts without earlier conversations.
- E: The failure may come from running the checks the wrong way.

**Source:** Context

## MA-ch00.11

A developer asks a coding agent to add a pause feature: pressing the pause key stops the ball, and pressing it again resumes. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A test that sets the game's `paused` variable to true and then checks it is true is a strong acceptance test of the pause key.
- [ ] B. If the new test fails, loosening its checks until it passes gives the same evidence as a pass of the original checks.
- [ ] C. An acceptance test checks the agreed behaviour from the outside, the way a player would exercise it.
- [ ] D. The agent takes the test's expected results from what its finished code does, so the test fits what was built.
- [ ] E. A stronger test sends the pause key through normal input handling and checks that the ball's position stays put.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: It does not exercise the key press, so it passes even if the key is not connected.
- B: A weakened test certifies less.
- C: Acceptance is judged on observable behaviour.
- D: Expected results copied from the code confirm the code; they should come from the required behaviour.
- E: It follows the real chain from input to observable state.

**Source:** Acceptance tests

## MA-ch00.12

A coding agent finishes a change and reports: "Done. All tests pass." The developer considers what each item establishes. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A diff shows which lines changed but not that the changed code behaves correctly.
- [ ] B. After one person plays the game for five minutes, the change counts as verified for other players and machines.
- [ ] C. If the agent pastes the test output, the developer treats the result as verified without rerunning anything.
- [ ] D. A passing automated test with the time step pinned shows the tested state is right under that scripted input; it does not show the game is fun or readable.
- [ ] E. The agent's report is a claim; running the same command yourself and seeing the same output is evidence.

**Key:** A=T B=F C=F D=T E=T

**Why:**

- A: A diff describes the change, not its correctness.
- B: A playtest shows one person's experience on one machine.
- C: Pasted output may come from a differently configured run; reproducing it is the check.
- D: A test speaks to the state it reads, under the inputs it feeds.
- E: Evidence is something the developer can reproduce and inspect.

**Source:** Claim versus evidence

## MA-ch00.13

A test presses the up key for 600 frames and then checks that a paddle has reached the top wall. The paddle's movement is speed times delta, where delta is the real time since the previous frame. With no change to code or test, it passes on 7 of 10 runs on a busy laptop and on 10 of 10 on an idle one. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. This test is flaky: its outcome varies between runs with no change to code or test.
- [ ] B. A test that passes ten times in a row is proven deterministic.
- [ ] C. Re-running until the test passes and keeping that run is a sound fix.
- [ ] D. Seeding the random number generator removes this variation, because the variation comes from randomness.
- [ ] E. A plausible cause is that frame length varies with machine load, so 600 frames span different amounts of game time.

**Key:** A=T B=F C=F D=F E=T

**Why:**

- A: Flaky means the result varies with no change to the code or the test.
- B: Ten passes are consistent with a failure that is rare or load-dependent.
- C: It hides the variation instead of removing its cause.
- D: The unpinned quantity is frame timing, which a random seed does not control.
- E: The test counts frames while the game advances in seconds.

**Source:** Flaky versus deterministic tests

## MA-ch00.14

A game moves a paddle by adding speed times delta each frame, where delta is the game time one frame represents. A test holds the up key for a number of frames. The engine is started with an option that forces a fixed frame rate, so each frame represents the same game time, and the engine does not wait on the wall clock between frames. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. With a higher forced frame rate and the same frame count, the same game time is simulated.
- [ ] B. Holding the key for a stated amount of game time, instead of a frame count, removes the dependence on the frame rate.
- [ ] C. Pinning the time step removes the machine-dependent quantity from the test.
- [ ] D. Forcing the frame rate makes a frame-counting test repeatable, because each frame is the same game time on each machine.
- [ ] E. Because the frame length is pinned, the test takes as many real seconds to run as the game time it simulates.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: More frames per second means less game time per frame, so the same frame count covers less game time.
- B: A test written in game seconds covers the same time at any frame rate.
- C: The pinned step removes the load-dependent frame length.
- D: A pinned time step makes frames equal in game time.
- E: Game time per frame is pinned, but the run takes as long as the machine needs.

**Source:** Fixed frame rate in tests

## MA-ch00.15

A developer wants a coding agent to fix a bug and prove the fix. Several instructions are considered. Check each statement that is true about whether the quoted instruction is precise enough to be checked. Each statement is worth 1 point (5 points total).

- [ ] A. "Do what it takes to get the test suite green." This is precise, because "green" is a measurable state.
- [ ] B. "Do not commit; leave the changes uncommitted so I can read the diff." This keeps acceptance with the developer.
- [ ] C. "Run the regression test headless at a fixed 60 fps; it has to exit 0; paste the command and its full output." This fixes conditions, pass criterion and evidence.
- [ ] D. "Make sure it works now." This is checkable, because "works" covers the test, the build and how the game feels.
- [ ] E. "If an existing test fails, report which and stop; do not edit tests." This blocks the shortcut of rewriting a failing test.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: The state is measurable, but the instruction permits weakening tests to reach it.
- B: It separates making the change from accepting it.
- C: Each element can be verified by rerunning the command.
- D: The word has no pass condition, so readers can interpret it differently.
- E: It forbids the cheapest way to turn red into green.

**Source:** Checkable instructions

## MA-ch00.16

A studio decides whether a coding agent can work on its scene files. One engine saves scenes as human-readable text; another saves its main scene format as binary files. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An agent that hand-edits a text scene can tell the engine will load it, by re-reading the file.
- [ ] B. A binary scene can be reviewed with an ordinary text diff as clearly as a text one.
- [ ] C. An agent can judge what a binary image looks like by reading its bytes as text in a terminal.
- [ ] D. A binary scene file is stored without history in version control, so a bad change has to be repaired by hand.
- [ ] E. A text scene shows up in a version-control diff line by line, so a reviewer sees which node or property changed.

**Key:** A=F B=F C=F D=F E=T

**Why:**

- A: A hand-edited scene can read as well-formed text and still fail to load; the engine is the judge.
- B: A line diff of binary data is not readable.
- C: Pixel content is not recoverable by reading bytes as characters.
- D: Version control stores binary files and can revert them; it cannot show a readable line diff.
- E: Text formats are what line-based diffs are built for.

**Source:** Text versus binary project files

## MA-ch00.17

A developer types to a coding agent: "Add a score to my two-player paddle game and make sure everything still works." Check each statement that is true about rewriting this as a precise instruction. Each statement is worth 1 point (5 points total).

- [ ] A. A new test for the score writes the score variable directly and then asserts it, which exercises the real behaviour.
- [ ] B. "Everything still works" is a checkable constraint, because it names the paddle and ball behaviour that has to stay fixed.
- [ ] C. "A score" is vague; observable behaviour names which player gets a point, for which edge, and where both scores are displayed.
- [ ] D. The original wording lets "works" mean "it runs", lets a test be weakened to pass, and lets unrelated behaviour change.
- [ ] E. A precise rewrite names the command that runs the checks (headless, frame rate pinned, under a timeout, exit 0 as the pass condition) and asks for the real output.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: A test that sets the asserted value cannot fail for the right reason; it should drive the game through normal input.
- B: "Everything" names nothing; the rewrite has to list the behaviour that stays fixed.
- C: Observable terms leave less to guess.
- D: Each is a way the vague wording can go wrong.
- E: Conditions, a pass criterion and evidence make the check repeatable.

**Source:** Vague request rewrite

## MA-ch00.18

A regression test passes on one laptop and fails on another, and sometimes fails then passes on the same laptop with no change to the code. The test presses keys for a fixed number of frames, and the game moves objects by speed times delta. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Another fix is to express the test in game seconds instead of counting rendered frames.
- [ ] B. A deterministic test gives the same result on each run from the same code and inputs.
- [ ] C. One fix is to run the engine with a fixed frame rate so each frame is the same game time.
- [ ] D. The mismatch is that the test counts frames while the game advances in seconds of delta.
- [ ] E. Before blaming the game code, change several variables at once so the cause shows up faster.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: A game-seconds test does not depend on how many frames are drawn.
- B: Determinism means the same inputs give the same result.
- C: A pinned frame rate removes the machine-dependent step.
- D: Frame length depends on load, so the same frame count covers different game time.
- E: Changing one variable at a time, under the pinned configuration, is what separates a flaky test from a code bug.

**Source:** Flaky tests and fixed frame rate

## MA-ch00.19

A developer wants a coding agent to import a game project and run its headless tests, but not to run arbitrary commands. Three options are considered: (a) an allow rule for commands starting with the engine's program name; (b) allow rules for exact commands with fixed arguments; (c) running everything in a sandbox that can write inside the project folder. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Option (a) is wide, because an engine that runs a script file runs whatever code the script contains.
- [ ] B. An allow rule decides which commands run without asking a human, while a sandbox technically limits what a running process can reach.
- [ ] C. Option (b) is narrower and easier to reason about, though an exact-match rule needs updating when the command changes.
- [ ] D. Even with these options the developer still reads new commands and scripts before approving them and reviews the diff before committing.
- [ ] E. Option (c) stops the agent from deleting or overwriting project files.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: A program-name rule is not a boundary on behaviour.
- B: A permission grant and a sandbox are different mechanisms.
- C: A narrow grant is easier to read, at the cost of upkeep.
- D: Human review is not replaced by either mechanism.
- E: A sandbox that allows writes inside the folder allows deletion there too.

**Source:** Permission grant versus sandbox

## MA-ch00.20

A coding agent ran a project's regression test the wrong way, the test failed, and the agent gave a confident but wrong explanation. The developer then added a short section to a standing instruction file in the repository, and the same request produced a correct run. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Project-specific facts such as required flags and setup steps are known to the agent without being written down.
- [ ] B. A fluent explanation is evidence, and the instruction file guarantees identical design choices on each run.
- [ ] C. The section should list exact commands, required options, setup steps such as the import step, the expected result and a time limit.
- [ ] D. The file should say what stays a human decision or is off limits to edit.
- [ ] E. Context is the text available to the agent now, such as instructions, files it has read and command output, and it is limited in size.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: What is not written down is guessed, and the guess can look plausible but be wrong.
- B: A fluent explanation is not evidence, and an instruction file does not fix design choices; the developer still verifies.
- C: These details make the run repeatable.
- D: Limits belong in the file as well.
- E: A new session starts without earlier conversations.

**Source:** Context and instruction files

## MA-ch00.21

A developer wants to verify, without opening a window, that a score label shows the correct number after the ball leaves the left edge. Check each statement that is true about a good headless test. Each statement is worth 1 point (5 points total).

- [ ] A. The test sets the score variable directly and then reads it back to confirm it.
- [ ] B. The test reports through its exit code, 0 for pass and nonzero for fail, plus a readable report.
- [ ] C. The test reads observable state, such as the score counter and the label's text, and pins the time step so the run is repeatable.
- [ ] D. The test shows how the number looks when rendered, including legibility and overlap.
- [ ] E. The test loads the real game scene and drives it through normal input events or by letting the game play until the ball leaves.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: Writing the asserted value directly proves nothing about the game.
- B: The exit code is the machine-readable verdict.
- C: State plus a pinned time step gives a repeatable check.
- D: Headless mode draws no frame, so appearance needs a person looking at a rendered image.
- E: Driving the real game exercises the real behaviour.

**Source:** Headless test design

## MA-ch00.22

A coding agent reports "Done, all tests pass." Check each statement that is true about what an item shows. Each statement is worth 1 point (5 points total).

- [ ] A. A reasonable minimum before accepting is reading the diff, rerunning the pinned test, checking that no test was weakened, and a human playtest for anything about feel.
- [ ] B. The agent's report shows that the agent produced a message, and the developer's own rerun is evidence.
- [ ] C. A clean import and parse check shows that files load and scripts parse, not that behaviour is right.
- [ ] D. A person playing shows what the game does on other machines.
- [ ] E. A build running on the target platform shows the game survives packaging, not that anyone wants to play it.

**Key:** A=T B=T C=T D=F E=T

**Why:**

- A: These checks cover the change, the test and the feel.
- B: A report is a claim; a reproduced result is evidence.
- C: Loading and parsing say nothing about behaviour.
- D: A playtest shows one person's experience on one machine.
- E: A packaged run tests the build, not the experience.

**Source:** Evidence ladder
