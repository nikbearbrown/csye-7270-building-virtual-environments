# Assignment 1: Extend Walker Jumpman

## B00 — One assignment, one traceable game

Please use Walker to inspect Jumpman, then help me change its character and extend its first level. I'm Liam, in for Professor Bear. This is Assignment One for C S Y E seventy-two seventy. We will connect setup, source code, and the running game, then show what you must change and verify.

## B01 — Do not merely copy it

The assignment is not to copy a working game. It is to extend one and explain the consequences. Each code excerpt here is followed by its visible result. The footage shows the unchanged starter, driven by scripted input. Your character, extension, and human playtest are still your work to do.

## B02 — 1 · Download the regular Godot engine

Start with the regular Godot Engine, not the dot net edition. This Mac demonstration uses the official macOS download page. The starter was verified with version four point seven point two and G D Script. On another operating system, choose its matching download. These exercises also assume your course Claude Code access; separate A P I credits are not required.

## B03 — 2 · Download both repositories

Clone Walker and Walker Jumpman into a working folder, or use Code, Download ZIP on each GitHub page and unzip them. Keep both repository addresses exact. One important limitation: the public Walker README still describes its older Unity workflow. Do not mistake that for a Godot installer. Jumpman is a standalone Godot project and can run without a Walker executable.

## B04 — 3 · Import the existing game

In Godot's Project Manager, choose Import and locate godot slash project dot godot inside the Jumpman download. Import and edit, then press F six only for a selected scene, or F five to run the project. Use F five here. The starter already selects its main scene. Creating a new empty project would not import this game.

## B05 — Observe the baseline first

Watch the starter at normal simulation speed: the first step, spikes, two gaps, another step, and the finish. The completion screen leads to a clean replay. This is one recorded scripted route, not proof that every route works. Before editing, play the original yourself and keep that baseline in your test report.

## B06 — Your two required changes

Assignment One has two concrete changes: a recognizable new main character, not just a rename or recolor, and a level extension beyond the starter with at least two new landings that require jumps. Move the finish to the new end. A longer empty floor is not the extension. Preserve the existing movement and recovery behavior while you change one concern at a time.

## B07 — Character art is drawing code

Here is the character's drawing code. The first rectangle gives the body its dark outline. The blue rectangle sits inside it. The orange strip is the scarf, followed by feet and an eye that changes side with facing. There is no sprite sheet to replace. For your first revision, change this visual identity while leaving movement alone.

## B08 — The rectangles become a character

Now those rectangles are visible, enlarged from the actual Godot drawing routine. The scarf crosses the body and the eye shifts with facing. This is a staged art preview, not gameplay. Judge the silhouette here, then check the new character at game size, against the background, while moving and jumping.

## B09 — The collision box is a different object

The collision shape is eighteen by twenty-eight game units, centered fourteen units above the player's origin. That places the origin at the feet. These lines, not the scarf drawing, define the rectangle used for physics. Preserve this contract initially so an art change does not secretly become a movement change.

## B10 — The scarf is not the collision boundary

The diagnostic outline comes from the actual CollisionShape node in this staged preview. Notice how the scarf protrudes beyond the physics rectangle. Appearance and collision already differ slightly in the starter. If your redesign makes that difference misleading, inspect it in motion and explain any intentional collider change instead of assuming the art changed physics.

## B11 — Movement uses rates, not teleports

Horizontal velocity moves toward a target using acceleration while a key is pressed and deceleration when it is released. Facing changes with the direction. Gravity updates vertical velocity separately. Tuning lives in the player resource; the remaining jump logic limits when another jump is allowed. Do not raise those limits to disguise an impossible new landing.

## B12 — Watch acceleration and braking

The player moves left to the boundary, accelerates to the right, then stops when the input is released. Opposing keys cancel. Watch the eye follow the chosen direction. This normal-input recording is the visible result of the movement code. Preserve those controls while replacing the art, and separately test jump, landing, and the one-jump contract.

## B13 — Level geometry starts as data

The level file lists rectangles as x, y, width, and height. Solids become both drawn platforms and physical bodies when the session builds the world. The finish is a separate trigger. Extend this layout with two meaningful new jump landings, update the level width, and move the finish. Do not confuse adding a rectangle with proving that it is reachable.

## B14 — Data becomes steps, gaps, and a finish

Follow the feet across the platforms. The player lands on real solids, clears the gaps, and eventually touches the finish trigger. Those are the observable consequences of the layout. Your new section should ask for actual jumps and remain reachable with the original movement. A successful starter route does not validate coordinates you have not tested yet.

## B15 — A useful bug seam: hazard art

The hazard drawing reads each hazard's horizontal position, but its vertical coordinates are hard-coded to three hundred twenty and three hundred four. That is a seam students can miss. Move hazard data vertically without updating its drawing and the picture may no longer match the collision. Trace both sides of the change.

## B16 — Visible spikes, failure, and retry

Walk into the visible spikes. The game names the failure, increments the retry count, and returns the player to the start. The starter drawing and collision agree in this run. If you move or redraw hazards, repeat this test. A dangerous object should fail where it looks dangerous, and the retry should still be cheap.

## B17 — The camera depends on the level width

This camera line looks one hundred units ahead of the player and clamps the camera center between the start and the level width minus three hundred twenty. That half-width comes from the logical six-forty-wide view. A wider level changes the camera boundary. It does not automatically extend hard-coded background drawing or reposition every label.

## B18 — The world moves; the interface stays

Watch the world scroll as the player approaches the end. The title and control hints stay fixed because the interface is separate from the world camera. After extending the map, inspect both new landings, the right edge, the finish label, and the background. Test what the player can see before a jump, not only whether the jump is physically possible.

## B19 — The progress bar hides another dependency

The progress bar subtracts the original spawn x, sixty-four, then divides by eight hundred fifty-two. That is the original distance from spawn to the finish trigger. Moving the finish without revisiting this expression can make the bar fill too early. A game can be playable and still tell the player the wrong thing.

## B20 — Watch the bar approach the old finish

Look at the thin green bar below the controls. It grows along this recorded route and reaches its end near the old finish. After your extension, compare that visual promise with the actual new goal. Verify the interface and level together; checking only the platform coordinates would miss this dependency.

## B21 — Pause switches the player off

Pause changes the session state and disables the player. Resume restores playing, then clears the pending jump request and requires a release. This is a local pause contract, not a blanket pause of the entire scene tree. Preserve it while adding your new section, and test the controls after a restart as well.

## B22 — Pause, resume, restart, and menu

Escape pauses the jump, Enter resumes, and R restarts. The recording also exercises a simulated focus-loss event and a return to the menu. Those are scripted checks, not a student playtest. Repeat the meaningful cases yourself after the extension. Recovery and navigation belong to the game, not just the happy path to the flag.

## B23 — Tests are evidence with a scope

The starter includes mechanical tests, keyboard-event tests, a route helper, and a staged screenshot helper. Some tests set up internal state; a passing report is not the same as a human playing. Keep the baseline checks, add checks for your new landings and relocated finish, and update route fixtures when the geometry changes. Never delete a useful assertion merely to get green output.

## B24 — Predict, inspect, and revise once

Write your change brief before prompting. Predict at least two ways the work might fail, such as a misleading silhouette or a camera that hides the next landing. Build one change, play it, inspect the cause, and make one documented revision. Keep the first failed attempt in Frictional. An honest struggle log is evidence of learning, not a contest to look effortless.

## B25 — 100 points, every ten days

The assignment is one hundred points, with a ten-day cadence and the actual deadline in Canvas. Sixty points cover implementation and explanation: character, level, verification, and the required film. Ten cover the honest Frictional log, ten the matching GitHub and Canvas version, and twenty are the relative quartile after the whole group is reviewed. Meeting the other criteria does not guarantee those comparative points.

## B26 — Ship source, a film, and the same version

Use Brutalist's Godot walkthrough or game-development skill with the Walker bookends to make a landscape four-K explainer. Show your new character, both new landings, failure and recovery, and code followed by its result. Put text and source on GitHub; put videos and large media in the designated media storage and link them. Match the submitted commit in Canvas. Name the human and A I contributions and follow Professor Bear's linked A I policy.

## B27 — The verdict

The verdict: do not submit a changed screenshot. Submit a changed, playable system whose behavior you can explain. The A I can draft code, tests, art, and narration. You choose the goal, inspect the evidence, judge whether the result serves the player, and defend the submission. Production polish helps communication; it cannot replace a correct game or an honest explanation.

## B28 — Your turn

Your turn. Please inspect Walker Jumpman. Propose a distinct character and two new landings. Preserve movement; list tests before editing. Use that prompt in Claude Code with the course's Walker context, then review the plan before accepting changes. Keep your predictions, play the extension yourself, and explain one revision the evidence made you choose. Liam, in for Professor Bear.

## B29 — Regular outro

[Regular stock outro only.]

