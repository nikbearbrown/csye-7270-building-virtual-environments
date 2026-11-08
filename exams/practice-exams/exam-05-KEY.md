# CSYE 7270 Building Virtual Environments: practice exam 05: KEY

Total 100 points. Statement key: T = true (check it), F = false (leave it blank).

---

**1.** A particle effect and a window need different transparency settings. Check each statement that is true about blend modes.  *(5 points)*

- [ ] A. Alpha blending mixes by opacity, so a half-transparent window shows the scene behind it.
- [ ] B. Multiply blending darkens what is behind it, which suits shadows and tints.
- [ ] C. Additive blending can make a surface darker than the background.
- [ ] D. A blend mode sets how a surface's output colour is combined with the colour already on screen.
- [ ] E. Additive blending adds colour to what is behind it, so fire and glows look brighter.

**Key:** A=T B=T C=F D=T E=T  |  `MA-jargon.38`  |  *Jargon test: shaders and materials*  |  source: Blend mode

- A (true): Alpha is opacity.
- B (true): Multiplying by a value of 1 or less keeps or darkens.
- C (false): Adding non-negative colour cannot darken.
- D (true): The blend mode is the combining rule.
- E (true): Adding light brightens, so overlapping glows brighten.

**2.** An agent edits a script to add a field, then tries to set it on the component, and the editor shows compilation errors. Which statements are correct? Check each statement that is true.  *(5 points)*

- [ ] A. Hiding the console errors makes the new component definition usable.
- [ ] B. Repeating the field assignment repairs a compiler error.
- [ ] C. A serialized field is a field Unity stores with the component, such as a public field.
- [ ] D. The field is available as soon as the script file is saved.
- [ ] E. A compilation error means the new script version is not loaded, so the component keeps its old layout.

**Key:** A=F B=F C=T D=F E=T  |  `MA-unity.10`  |  *Unity, Spark and agent workflows*  |  source: compilation and serialized field

- A (false): Display filtering does not fix compilation.
- B (false): The cause is in the code or dependencies.
- C (true): Serialization is what makes a field settable in the editor.
- D (false): Saved bytes do not mean the code compiled.
- E (true): The old compiled definition stays in use.

**3.** Two Unreal Actors reference one material instance asset. A designer wants only the first Actor to change appearance. Check each statement that is true.  *(5 points)*

- [ ] A. The word instance in the name means the asset is private to one Actor.
- [ ] B. An Actor's label names the material it uses.
- [ ] C. Two Actors that reference the same material instance asset share its parameter values.
- [ ] D. A dynamic material instance is a saved asset in the content folder.
- [ ] E. A material instance asset is a saved child of a parent material with changed parameters.

**Key:** A=F B=F C=T D=F E=T  |  `MA-unreal.11`  |  *Unreal and agent workflows*  |  source: Material instance scope

- A (false): Several Actors can reference one instance asset.
- B (false): A label is a display name only.
- C (true): Editing the shared asset affects both.
- D (false): A dynamic material instance is created at runtime.
- E (true): The instance overrides parameters of its parent.

**4.** Match each described behaviour to its camera term. Check each statement that is true.  *(5 points)*

- [ ] A. An explosion rattles the view for a moment, so the term is camera limits.
- [ ] B. Small twitches of the player should not move the view, so the term is deadzone.
- [ ] C. The camera stops scrolling at the left edge of the level, so the term is look-ahead.
- [ ] D. The camera gently trails the player and catches up, so the term is look-ahead.
- [ ] E. A fast runner needs to see more of the level ahead, so the term is look-ahead.

**Key:** A=F B=T C=F D=F E=T  |  `MA-jargon.54`  |  *Jargon test: from the essay prompts*  |  source: Pick the camera term for a behaviour

- A (false): A brief rattle is screen shake.
- B (true): A deadzone ignores movement inside a region.
- C (false): Stopping at the edge is camera limits (bounds).
- D (false): Trailing and catching up is smoothing (damping).
- E (true): Look-ahead offsets the framing in the direction of travel.

**5.** A designer asks for a button that "eases in" or "eases out" when it appears. Check each statement that is true.  *(5 points)*

- [ ] A. Ease-in starts slowly and speeds up.
- [ ] B. Linear interpolation changes the value at a constant rate.
- [ ] C. Ease-out starts quickly and slows down toward the end.
- [ ] D. Ease-in-out is slow at both the start and the end, and quicker in the middle.
- [ ] E. Ease-out means the animation plays backward after it finishes.

**Key:** A=T B=T C=T D=T E=F  |  `MA-jargon.12`  |  *Jargon test: animation movement*  |  source: Easing curves

- A (true): Ease-in accelerates from rest.
- B (true): Linear means a straight line from start to end.
- C (true): Ease-out decelerates into the final value.
- D (true): Ease-in-out combines both.
- E (false): Direction of playback is a separate setting from easing.

**6.** An agent reports: "The test for the damage function passes. I generated the expected value by running the function and pasting its output." Check each statement that is true.  *(5 points)*

- [ ] A. The test is strong, since it passes on the current code.
- [ ] B. The test is weak: it asserts that the function returns what it returned, so it cannot find a wrong formula.
- [ ] C. The test becomes strong once the pasted value is moved into a named constant in the test file.
- [ ] D. A follow-up that gives evidence is: change the damage formula on purpose and report whether the test then fails.
- [ ] E. A follow-up that gives evidence is: run the same test a second time.

**Key:** A=F B=T C=F D=T E=F  |  `MA-k02.27`  |  *Jargon test: reading agent output*  |  source: Evidence versus claim

- A (false): It passes whatever the code does, because the expected value is the code's own output.
- B (true): The expected value comes from the code under test, so the assertion holds even when the formula is wrong.
- C (false): A constant holds the same copied output, so a wrong formula still passes.
- D (true): A test that stays green after a deliberate break cannot detect faults, so this check exposes it.
- E (false): The same test passes again for the same reason, so it adds no independent check.

**7.** A level designer writes "coyote time 0.1 s" in the spec. Check each statement that is a correct unpacking into a checkable constraint.  *(5 points)*

- [ ] A. The timer starts when the player presses the jump button.
- [ ] B. A jump press 0.08 s after walking off a ledge still jumps.
- [ ] C. After a real jump the window is cleared, so a second press during the same fall does not give a second jump.
- [ ] D. A jump press 0.08 s before landing still jumps when the character lands.
- [ ] E. The timer starts at the moment the character leaves the floor without jumping.

**Key:** A=F B=T C=T D=F E=T  |  `MA-k01.6`  |  *Jargon test: compress and decompress*  |  source: Coyote time

- A (false): Starting at the press would build a buffer, not a grace window that opens after leaving the ground.
- B (true): The press arrives inside the 0.1 s grace window, so the jump is accepted.
- C (true): Clearing it prevents coyote time from turning into a free double jump.
- D (false): That behaviour is a jump buffer, a separate feature that remembers early presses, not coyote time.
- E (true): That moment opens the short grace window in which a jump is still allowed after walking off an edge.

**8.** An agent changes five of ten lights before a tool fails, and the contract gives no transactions. Check each statement that is true about recovery.  *(5 points)*

- [ ] A. A transaction is a set of independent edits that each commit on their own.
- [ ] B. Overwriting without a precondition check is safe even if another editor changed the same object.
- [ ] C. A recovery record stores each object's identity, original value, attempted value and observed outcome.
- [ ] D. A precondition check confirms the current state matches what is expected before a change is made.
- [ ] E. Restoring means finishing the remaining edits, and resuming means re-applying the original values.

**Key:** A=F B=F C=T D=T E=F  |  `MA-verification.19`  |  *Agent testing, troubleshooting and engine comparisons*  |  source: Recovery record, precondition, transaction

- A (false): A transaction groups edits so that they commit together or not at all.
- B (false): Blind overwrites can destroy concurrent work.
- C (true): The record lets the state be reconstructed after a failure.
- D (true): A precondition check avoids overwriting unrelated changes.
- E (false): Resuming finishes the remaining edits, and restoring re-applies verified original values.

**9.** Two integrations carry MCP messages over stdio and over Streamable HTTP. Which statements are correct? Check each statement that is true.  *(5 points)*

- [ ] A. Switching transport translates Unity components into Unreal components.
- [ ] B. A transport carries messages and does not define the editor operations.
- [ ] C. A transport fault can stop a valid request from reaching the server.
- [ ] D. With stdio, the client launches the server as a subprocess and exchanges messages over its standard streams.
- [ ] E. Streamable HTTP can reach a server on the same machine.

**Key:** A=F B=T C=T D=T E=T  |  `MA-mcp.9`  |  *MCP fundamentals*  |  source: transports

- A (false): A transport does not convert engine data.
- B (true): Delivery and scene-editing semantics are separate layers.
- C (true): Delivery can fail before execution.
- D (true): That is how the stdio transport works.
- E (true): HTTP does not imply a remote service.

**10.** A door rotates from 0 to 90 degrees over 1 second. Check each statement that is true about telling a keyframe, interpolation and easing apart.  *(5 points)*

- [ ] A. Reaching 45 degrees at 0.5 s is interpolation.
- [ ] B. Keyframe is the name for the computed value between two endpoints.
- [ ] C. 0 degrees at 0.0 s and 90 degrees at 1.0 s are keyframes.
- [ ] D. Easing is the name for the authored value at a chosen time.
- [ ] E. Slow in, slow out is keyframing.

**Key:** A=T B=F C=T D=F E=F  |  `MA-ch10.24`  |  *None*  |  source: Keyframe, interpolation and easing

- A (true): Interpolation computes in-between values.
- B (false): That describes interpolation.
- C (true): A keyframe is an authored value at a time.
- D (false): That describes a keyframe.
- E (false): Slow in, slow out is easing.

**11.** A student says "enemy hits" and the agent builds the wrong thing. Check each statement that is true.  *(5 points)*

- [ ] A. A hitbox is normally a trigger, since it needs to detect an overlap and not block.
- [ ] B. A hitbox is an area on an attacker that deals damage when it overlaps a target.
- [ ] C. A hurtbox is an area on a character that can receive damage.
- [ ] D. A hurtbox is the weapon area that deals the damage.
- [ ] E. A hitbox and a hurtbox are the same area with two names.

**Key:** A=T B=T C=T D=F E=F  |  `MA-jargon.46`  |  *Jargon test: sprite sheets, rigs, colliders and state machines*  |  source: Hitbox and hurtbox

- A (true): Detection is enough, so triggers fit.
- B (true): A hitbox is the attack volume.
- C (true): A hurtbox is the vulnerable volume.
- D (false): The weapon area is the hitbox.
- E (false): They play opposite roles.

**12.** A scene holds 2000 enemies, and each runs a per-frame update that checks whether the player is near. A developer asks an agent to cut that cost. Check each statement that is true.  *(5 points)*

- [ ] A. Reacting to an event costs more per frame than polling for idle objects.
- [ ] B. Switching off the per-frame callback on idle enemies removes their polling cost until they are switched back on.
- [ ] C. Event-driven code runs when something happens, so idle objects add nothing per frame.
- [ ] D. Polling checks a condition on each update even when nothing has changed, so its cost grows with the number of objects.
- [ ] E. Polling and event-driven are two names for the same technique.

**Key:** A=F B=T C=T D=T E=F  |  `MA-vocab.14`  |  *Engine vocabulary (Godot, Unity, Unreal)*  |  source: Polling versus event-driven cost

- A (false): An event has no per-frame cost for idle objects.
- B (true): An object without a per-frame callback pays nothing for it.
- C (true): Events invoke code at the moment of change.
- D (true): Polling repeats the same check at the update rate whether or not the answer changed.
- E (false): Polling asks again and again; an event is pushed when the change occurs.

**13.** A studio considers running an unfamiliar MCP package with the developer's project access. Check each statement that is true.  *(5 points)*

- [ ] A. A disposable project is a throwaway copy used to test untrusted code.
- [ ] B. A popular package is a verified package.
- [ ] C. A dependency is code a package relies on, and it runs with the same permissions.
- [ ] D. A sandbox is a restricted environment that limits what code can touch.
- [ ] E. Pinning fixes a dependency to a specific reviewed version or revision.

**Key:** A=T B=F C=T D=T E=T  |  `MA-security.12`  |  *Agent security and local versus cloud execution*  |  source: Supply chain vocabulary

- A (true): Damage there is cheap.
- B (false): Popularity is not verification.
- C (true): It adds to the trusted code.
- D (true): It confines a process.
- E (true): Pinning keeps the reviewed code in use.

**14.** A designer asks for "a 12 frame walk cycle with keyframes on frames 1, 4 and 7". Check each statement that is correct.  *(5 points)*

- [ ] A. Keyframes on frames 1, 4 and 7 mean frames 2, 3, 5 and 6 stay blank until the agent adds keyframes there.
- [ ] B. A keyframe is a stored value at a specific time, and the frames between come from interpolation in an animation track.
- [ ] C. A frame is one displayed image in time, and a sprite sheet cell holds one.
- [ ] D. Counting an animation's length in frames tells you how many keyframes it holds.
- [ ] E. A frame and a keyframe are the same thing, so 12 frames means 12 keyframes.

**Key:** A=F B=T C=T D=F E=F  |  `MA-k03.7`  |  *Jargon test: false friends*  |  source: Frame versus keyframe

- A (false): The in-between frames get values by interpolation, so adding more keyframes would change the requested animation.
- B (true): Keyframes are the stored values, so the agent adds three keys to the track and lets playback fill in the rest.
- C (true): The agent should plan twelve cells in the sheet because each frame is one displayed image.
- D (false): Keyframes are only the stored values, so a twelve frame animation can hold three keyframes and an agent counting frames would add too many.
- E (false): They are different, and an agent treating them as equal would build twelve keys instead of three.

**15.** An agent is asked to make a follow camera "less jerky". Check each statement that is true about the settings it may adjust.  *(5 points)*

- [ ] A. A wider deadzone makes the camera react to small movements sooner.
- [ ] B. A higher smoothing (damping) speed makes the camera catch up to the target more slowly.
- [ ] C. A larger look-ahead distance shifts the framing farther in the direction of travel.
- [ ] D. A camera that follows a physics body is not affected by whether the camera and the body update on the same tick.
- [ ] E. Turning smoothing on makes the camera snap onto the target instantly.

**Key:** A=F B=F C=T D=F E=F  |  `MA-jargon.9`  |  *Jargon test: camera movement*  |  source: Follow-camera tuning words

- A (false): A wider deadzone makes the camera ignore more small movement.
- B (false): A higher smoothing speed closes the gap faster.
- C (true): Look-ahead distance is the size of that forward shift.
- D (false): Mismatched update rates between the body and the camera are a common cause of visible jitter.
- E (false): Smoothing spreads the move over time; instant snapping is the absence of smoothing.

**16.** A platformer feels unfair because jumps fail by a hair. Check each statement that is true about the forgiveness terms.  *(5 points)*

- [ ] A. A jump buffer helps a player who presses jump a moment early.
- [ ] B. Coyote time helps a player who presses jump a moment late.
- [ ] C. Coyote time makes the character fall more slowly after leaving a ledge.
- [ ] D. Coyote time is a short grace window after leaving a ledge in which a jump is still allowed.
- [ ] E. A jump buffer remembers a jump press made just before landing and performs the jump on landing.

**Key:** A=T B=T C=F D=T E=T  |  `MA-jargon.23`  |  *Jargon test: game movement*  |  source: Coyote time and jump buffer

- A (true): Early presses are held until landing.
- B (true): Late presses still count inside the window.
- C (false): It changes when a jump is allowed, not the fall speed.
- D (true): Coyote time extends the ground check after the feet leave.
- E (true): The input is stored for a few frames and used when the character lands.

**17.** A vague prompt reads "make the sword look cool". Check each rewrite that uses exact shader and material terms correctly.  *(5 points)*

- [ ] A. "Use additive blend mode on the whole opaque blade so it looks like steel."
- [ ] B. "Add a fragment shader that scrolls the UV over time to make a glint pass along the blade."
- [ ] C. "Give the blade a vertex roughness of 0.2 and a UV metallic of 1."
- [ ] D. "Add an emission colour of pale blue to the blade's fuller, at low strength."
- [ ] E. "Set the blade's metallic to 1 and roughness to 0.2, and add a normal map for the engraving."

**Key:** A=F B=T C=F D=T E=T  |  `MA-jargon.40`  |  *Jargon test: shaders and materials*  |  source: Rewrite a vague shader prompt

- A (false): Additive blending makes a surface glow like light; it is not how steel is shaded.
- B (true): Scrolling UVs in the fragment stage animates a glint across the texture.
- C (false): Roughness and metallic are material parameters, not vertex or UV properties.
- D (true): Emission supplies self-lit colour.
- E (true): Metallic, roughness and a normal map are used for their meanings.

**18.** A team proposes a tool that sets the intensity of one identified light, instead of giving the agent a general script evaluator. Which statements are correct? Check each statement that is true.  *(5 points)*

- [ ] A. A narrow tool still needs authorization because it writes to the project.
- [ ] B. A narrow tool validates the light's identity and an allowed intensity range.
- [ ] C. A free-text request to be careful enforces the same limits as argument validation.
- [ ] D. A narrow tool is free of bugs because it is narrow.
- [ ] E. Reporting the previous and resulting intensity supports review and recovery.

**Key:** A=T B=T C=F D=F E=T  |  `MA-unity.17`  |  *Unity, Spark and agent workflows*  |  source: narrow tool versus script evaluator

- A (true): A narrow write is still a write.
- B (true): Validation narrows the operation.
- C (false): Instructions are not a technical boundary.
- D (false): Its implementation still needs verification.
- E (true): It records the actual change.

**19.** A designer tells an agent: Put five checkpoints in the level at these spots. Check each statement that is true.  *(5 points)*

- [ ] A. Placing adds an instance to the level and editing the Blueprint changes the class.
- [ ] B. Rotation is the term for how large an object is.
- [ ] C. A nickname for an asset is a more precise reference than its asset path.
- [ ] D. A transform combines location, rotation and scale.
- [ ] E. World-space coordinates are measured from the level origin, and relative coordinates from a parent.

**Key:** A=T B=F C=F D=T E=T  |  `MA-unreal.14`  |  *Unreal and agent workflows*  |  source: Placement and transform vocabulary

- A (true): Placement and class editing differ in scope.
- B (false): Size is scale; rotation is orientation.
- C (false): A full path names one asset unambiguously.
- D (true): Those three values describe placement.
- E (true): The coordinate space has to be stated.

**20.** An agent is told to build the locomotion and jump logic. Check each statement that is true.  *(5 points)*

- [ ] A. A parameter is the rule that decides when to switch states.
- [ ] B. A blend tree has one active state and moves between states by transitions.
- [ ] C. A transition is a rule with a condition, such as "on the ground" changing to false.
- [ ] D. An instruction naming the parameter, the clips and the transition conditions removes guessing.
- [ ] E. A parameter is a named value, such as speed, that the logic reads.

**Key:** A=F B=F C=T D=T E=T  |  `MA-jargon.66`  |  *Jargon test: from the essay prompts*  |  source: Transition and parameter

- A (false): That is a transition.
- B (false): That describes a state machine.
- C (true): It decides when the active state changes.
- D (true): Each missing name would otherwise be a guess.
- E (true): Parameters feed transition conditions and blend trees.
