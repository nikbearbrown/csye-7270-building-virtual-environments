# Agent testing, troubleshooting and engine comparisons

## MA-verification.1

An agent reports that a generated jump mechanic is done. Its offered evidence is a saved script and a screenshot of the character standing on the floor. Check each statement that is true about claims and evidence. Each statement is worth 1 point (5 points total).

- [ ] A. A screenshot of a standing character is behavioural evidence for jumping.
- [ ] B. An editor screenshot is evidence about how a packaged build runs on the target device.
- [ ] C. Evidence for a jump comes from driving input through the mechanic and observing the resulting trajectory.
- [ ] D. A saved script file is evidence that the script compiles.
- [ ] E. A completion message is a claim, not a test result.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: A still image of a character at rest does not exercise the jump.
- B: The editor and a packaged build are different environments.
- C: Behavioural evidence shows the mechanic responding to input over time.
- D: A file can be saved with invalid code, so saving is not compile validation.
- E: A claim states a result; a test result is something that was run and observed.

**Source:** Claim versus evidence

## MA-verification.2

A checkpoint test writes the expected position into the save data and then asserts that the save data equals that same position. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The test exercises the trigger path of the checkpoint.
- [ ] B. A behavioural test compares the observed result with a value written by the test setup.
- [ ] C. A behavioural test drives the player through the trigger and then observes the saved position.
- [ ] D. Adding more assertions of the same kind turns the test into a behavioural test.
- [ ] E. This assertion is a tautology: it compares a value with the one the test just set.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: Assigning the value directly bypasses trigger activation.
- B: Taking the expected value from the setup is what makes the test circular.
- C: The behaviour under test is the response to entering the trigger.
- D: Repeating a tautology does not exercise the missing behaviour.
- E: A tautological assertion is true whatever the game does.

**Source:** Behavioural test versus tautology

## MA-verification.3

A test starts the player before a checkpoint, moves through its trigger, resets the player and checks the respawn location. The random seed and the simulation step are fixed. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The observed respawn position, compared with the requirement, is acceptance evidence.
- [ ] B. A negative case, such as respawning before a checkpoint was activated, checks that the feature rejects what it should reject.
- [ ] C. Fixing the seed and the step guarantees freedom from nondeterminism caused by threads and external state.
- [ ] D. A fixed simulation step ties a frame count to a known amount of simulated time.
- [ ] E. Fixing the random seed makes the random inputs of a run repeatable.

**Key:** A=T B=T C=F D=T E=T

**Why:**

- A: Acceptance evidence is an observation measured against the stated requirement.
- B: A negative case tests the failure path, not just the success path.
- C: Other sources of nondeterminism, such as scheduling, can remain.
- D: With a fixed step, each tick advances the simulation by the same amount.
- E: A seed makes a pseudo-random sequence replay identically.

**Source:** Deterministic tests, negative case, acceptance evidence

## MA-verification.4

A hypothetical create-prop tool times out, and the editor may have created the prop before the reply was lost. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An idempotency key lets a repeated request have the same effect as a single request.
- [ ] B. A timeout means the operation was rolled back.
- [ ] C. After a timeout the outcome is unknown: the operation may or may not have run.
- [ ] D. Repeating a non-idempotent create without checking can produce a duplicate.
- [ ] E. Idempotent means that the operation is undone when it fails.

**Key:** A=T B=F C=T D=T E=F

**Why:**

- A: An idempotent operation tied to a key can be retried safely.
- B: Rollback is a separate guarantee and a timeout does not imply it.
- C: A lost reply says nothing about whether the editor executed the call.
- D: The first attempt may have succeeded, so a second create adds another prop.
- E: Idempotent describes repeat safety, not undoing failed work.

**Source:** Timeout, idempotency

## MA-verification.5

A game test passes on some runs and fails on others with unchanged code. It uses a random spawn position and waits a fixed number of rendered frames while the simulation speed varies. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A flaky test is one that gives different results on unchanged code.
- [ ] B. Rerunning until one pass appears is a fix for the intermittent failure.
- [ ] C. Deleting the failing assertion repairs the nondeterminism.
- [ ] D. Waiting for a fixed number of rendered frames is more robust than waiting for a condition with a time bound.
- [ ] E. Recording the random seed lets a failing run be replayed.

**Key:** A=T B=F C=F D=F E=T

**Why:**

- A: Flaky names a result that varies without a code change.
- B: One pass can hide a failure that is still intermittent.
- C: Removing the check removes detection and leaves the cause in place.
- D: Rendered frames need not correspond to a fixed amount of simulated time.
- E: With the seed, the same spawn sequence can be recreated.

**Source:** Flaky test, seed, bounded wait

## MA-verification.6

A hypothetical Unity placement tool takes meters and a hypothetical Unreal placement tool takes centimeters. Both place an object a distance along the same world axis. Check each statement that is true about units. Each statement is worth 1 point (5 points total).

- [ ] A. Sending the number 2.5 to both tools gives the same world distance.
- [ ] B. MCP defines the length unit that the tools use.
- [ ] C. A distance of 2.5 meters is 250 in the centimeter-based tool.
- [ ] D. The unit belongs to each tool's contract, so an adapter converts between them.
- [ ] E. Reading the result back in a common unit checks that the conversion was right.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: The same number means different lengths in different units.
- B: A protocol carries messages; each tool decides its own units.
- C: There are one hundred centimeters in a meter.
- D: A contract states the unit and the adapter honours it.
- E: Comparing both outcomes on one basis exposes a conversion error.

**Source:** Units and adapter

## MA-verification.7

A team discusses a performance target for a benchmark scene. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. A frame budget is the time allowed for one frame to reach a target frame rate.
- [ ] B. Frame rate is frames per second, which is the reciprocal of a steady frame time.
- [ ] C. A longer frame time means a higher frame rate.
- [ ] D. An average frame time can hide slow frames, so a benchmark also looks at the spread of frame times.
- [ ] E. Frame time is the duration of one frame, usually given in milliseconds.

**Key:** A=T B=T C=F D=T E=T

**Why:**

- A: The budget is the target period, such as the time of one frame at the desired rate.
- B: Frames per second and seconds per frame are inverses when steady.
- C: They move in opposite directions: more time per frame gives fewer frames per second.
- D: Spikes and stutter appear in the distribution, not in the average.
- E: Frame time is measured per frame, in units of time.

**Source:** Frame time, frame rate, frame budget

## MA-verification.8

An agent raises the frame rate by switching off shadows, but the acceptance criteria require readable character shadows. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Acceptance criteria define what counts as done, and dropping one changes the task rather than meeting it.
- [ ] B. A controlled benchmark compares runs on the same scene and workload.
- [ ] C. Profiling finds the real bottleneck before an optimization is chosen.
- [ ] D. Profiling means guessing which feature is costly and switching it off.
- [ ] E. A higher frame rate alone is acceptance evidence for completion.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: Criteria are the agreed definition of done.
- B: Holding the workload constant lets the change be attributed to the optimization.
- C: A profiler measures where time goes.
- D: Guessing is the opposite of profiling, which is measurement.
- E: Speed that breaks a required feature is a failure against the criteria.

**Source:** Acceptance criteria, benchmark, profiling

## MA-verification.9

A team compares a Unity agent workflow with an Unreal agent workflow; both use MCP. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A representative task benchmark can reveal gaps that the protocol label hides.
- [ ] B. Steps that a person still performs by hand belong in the comparison.
- [ ] C. Using MCP gives both engines equal tool coverage.
- [ ] D. MCP is a protocol, and the tool catalogue is the set of operations a particular server exposes.
- [ ] E. The count of advertised tools measures how useful the workflow is.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: Running real tasks shows what the tools can and cannot do.
- B: Manual steps are part of the real effort of a workflow.
- C: Catalogues differ between servers and engines.
- D: The protocol and the catalogue are different things.
- E: Relevance, reliability and semantics matter more than tool count.

**Source:** MCP versus tool catalogue

## MA-verification.10

An interaction an agent created works in the editor. It must also work as a packaged build on a target device. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Platform-specific behaviour is checked by running on the target platform.
- [ ] B. A packaged build can omit assets that the export configuration does not include.
- [ ] C. Running in the editor and running a packaged build are different environments.
- [ ] D. Reading the agent's packaging plan substitutes for a test on the target device.
- [ ] E. Completing a build is evidence that the interaction behaves correctly when played.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: Target-only failures show up on the target.
- B: Export settings decide which files ship.
- C: The editor loads project files directly; a build uses exported content.
- D: A plan is intent, not execution evidence.
- E: A successful build and correct runtime behaviour are separate facts.

**Source:** Editor versus packaged build

## MA-verification.11

A hypothetical batch tool edits ten lights, and its contract says each edit commits separately. The sixth edit fails. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A rollback restores the earlier state after a failure, and this contract gives no such guarantee.
- [ ] B. Sending ten edits in one request makes them atomic.
- [ ] C. After a partial failure, the next step is to inspect the current state of each light before retrying.
- [ ] D. Under this contract the first five edits can remain applied, which is a partial commit.
- [ ] E. An atomic operation applies in full or leaves the state unchanged, with no half-finished state.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: Rollback is a guarantee that must be stated by the contract.
- B: Grouping requests does not create transactional behaviour.
- C: The current state decides the safe recovery action.
- D: Independent commits allow some edits to persist.
- E: Atomicity means no visible half-finished state.

**Source:** Atomicity, partial commit, rollback

## MA-verification.12

An agent adds a door interaction and also weakens an existing collision assertion so that the suite passes. The weakened assertion was not part of the request. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A diff review covers test files as well as gameplay code.
- [ ] B. A change to a test outside the requested work is scope creep that the agent should report.
- [ ] C. A weakened assertion lowers what a passing suite proves.
- [ ] D. A regression test checks that behaviour that worked before still works.
- [ ] E. A green suite means the same thing whichever assertions were edited.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: Test edits change the acceptance evidence, so they belong in review.
- B: Changes beyond the requested scope need to be disclosed and justified.
- C: Looser checks let more wrong behaviour pass.
- D: A regression test guards against breaking earlier behaviour.
- E: The meaning of a pass depends on the assertions behind it.

**Source:** Scope creep, regression test

## MA-verification.13

An agent says a door that opens only when the player holds a key is complete. A reviewer asks what kinds of evidence would count. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A negative path test checks that the door opens when the key is held.
- [ ] B. Running just the has-key case covers the rejection behaviour.
- [ ] C. Import or compile validation shows that the project loads, not that the door logic is right.
- [ ] D. A negative path test checks that the door stays closed without the key.
- [ ] E. Static inspection reads the implementation and changed assets without running them.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: Opening with the key is the positive path.
- B: The rejection case needs its own test.
- C: Validation is a lower level of evidence than a behavioural test.
- D: The negative path is the rejection case.
- E: Static means examined without execution.

**Source:** Static, positive and negative evidence

## MA-verification.14

An editor tool times out while creating a checkpoint, and the operation has no documented atomicity. Check each statement that is true about recovering. Each statement is worth 1 point (5 points total).

- [ ] A. A bounded search deletes whatever matches a broad pattern.
- [ ] B. A stable identifier, such as a unique name or ID, lets an agent look up whether the object already exists.
- [ ] C. If inspection fails to resolve the state, reporting the outcome as unknown is more accurate than reporting success.
- [ ] D. An existence check before creating again guards against a duplicate.
- [ ] E. An operation record is a copy of the scene taken before editing so edits can be undone.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: A bounded search is limited by identifier or scope so that it finds only the intended object.
- B: An identifier gives a precise handle for the lookup.
- C: An unresolved state is neither a confirmed success nor a confirmed failure.
- D: Checking first avoids creating a second copy.
- E: An operation record is a log of attempted operations and their outcomes.

**Source:** Existence check, stable identifier, operation record

## MA-verification.15

A team writes an engine-neutral specification for a checkpoint and then implements it in Unity and in Unreal. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An engine-neutral specification describes observable behaviour without using one engine's terms.
- [ ] B. Equivalent acceptance cases need identical serialized assets in both engines.
- [ ] C. In Unity, behaviour is attached to a GameObject as components, and in Unreal an Actor holds components and can run Blueprint or C++ logic.
- [ ] D. An adapter maps the specification onto one engine's objects and scripting.
- [ ] E. Local-space and world-space positions are interchangeable, so an adapter need not say which it uses.

**Key:** A=T B=F C=T D=T E=F

**Why:**

- A: Neutral wording lets both engines be judged against the same behaviour.
- B: Cases compare gameplay outcomes, not file formats.
- C: Both engines use an object-plus-components model with different names.
- D: An adapter is the layer that translates a spec into engine terms.
- E: A position means different things in local and world coordinate spaces.

**Source:** Engine-neutral specification, adapter, coordinate space

## MA-verification.16

A game test fails intermittently. It spawns at a random position, and it uses an asset that is imported asynchronously. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An import failure and a gameplay failure are the same cause.
- [ ] B. An asynchronous import finishes later than the request, so a test that proceeds at once may use an asset that is not ready.
- [ ] C. Reporting the first passing rerun is adequate evidence that an intermittent failure is gone.
- [ ] D. A fixed timestep advances the simulation by a different amount depending on rendering speed.
- [ ] E. Rendered frames and elapsed game time are interchangeable when the simulation speed varies.

**Key:** A=F B=T C=F D=F E=F

**Why:**

- A: They are different causes and a test should tell them apart.
- B: Asynchronous means the work completes without blocking the caller.
- C: Intermittent failures need repeated runs under controlled setup.
- D: A fixed timestep advances by a constant amount each tick.
- E: Frame count measures drawing, not simulated time.

**Source:** Asynchronous import, fixed timestep

## MA-verification.17

A team plans a fair comparison of a Unity integration and an Unreal integration for importing props, placing them and running tests. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Two integrations that both use MCP expose identical operation names.
- [ ] B. A fair comparison holds the observable requirements constant across the engines.
- [ ] C. Choosing by the length of a demo is a measured comparison.
- [ ] D. A tool inventory lists the operations each integration exposes, including steps left manual.
- [ ] E. A controlled failure, such as forcing a timeout, shows how each integration recovers.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: The protocol does not fix operation names or coverage.
- B: The same requirements make the results comparable.
- C: A demo is an anecdote, not a measurement.
- D: The inventory records what is actually available.
- E: Injecting a failure tests recovery, not just success.

**Source:** Fair comparison, tool inventory, controlled failure

## MA-verification.18

A test oracle is the source of the expected result in a test. Check each statement that is true about oracles and checks. Each statement is worth 1 point (5 points total).

- [ ] A. Deliberately breaking the activation path to see the test fail checks that the test can detect the bug.
- [ ] B. An oracle taken from the code under test is not independent.
- [ ] C. A negative case proves that the positive case works.
- [ ] D. A tolerance lets a position comparison pass when the difference is small.
- [ ] E. Floating-point positions are compared with exact equality because they are stored with perfect precision.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: A test that cannot fail on broken code gives false confidence.
- B: An independent oracle comes from the requirement, not from the implementation.
- C: Each case tests its own path.
- D: A tolerance is an allowed difference for numeric results.
- E: Floating-point results often differ in the last digits, so a tolerance is used.

**Source:** Test oracle, tolerance, negative case

## MA-verification.19

An agent changes five of ten lights before a tool fails, and the contract gives no transactions. Check each statement that is true about recovery. Each statement is worth 1 point (5 points total).

- [ ] A. A transaction is a set of independent edits that each commit on their own.
- [ ] B. Overwriting without a precondition check is safe even if another editor changed the same object.
- [ ] C. A recovery record stores each object's identity, original value, attempted value and observed outcome.
- [ ] D. A precondition check confirms the current state matches what is expected before a change is made.
- [ ] E. Restoring means finishing the remaining edits, and resuming means re-applying the original values.

**Key:** A=F B=F C=T D=T E=F

**Why:**

- A: A transaction groups edits so that they commit together or not at all.
- B: Blind overwrites can destroy concurrent work.
- C: The record lets the state be reconstructed after a failure.
- D: A precondition check avoids overwriting unrelated changes.
- E: Resuming finishes the remaining edits, and restoring re-applies verified original values.

**Source:** Recovery record, precondition, transaction
