# Unreal and agent workflows

## MA-unreal.1

An Unreal editor MCP server lets an external assistant call editor operations. A designer asks whether this makes the assistant the NPC's runtime AI. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Editor automation and runtime AI are two names for the same role.
- [ ] B. An MCP server connected to the editor becomes the NPC's behaviour in the packaged build.
- [ ] C. An MCP server exposes tools that an external assistant can call.
- [ ] D. A tool call that places an Actor is an example of runtime AI.
- [ ] E. Runtime AI is the NPC's decision logic executing while the game is played.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: One changes the project; the other controls behaviour in play.
- B: The packaged game needs its own gameplay logic.
- C: A server publishes named operations (tools) that a client can invoke.
- D: Placing an Actor is editor automation, a development-time change.
- E: Runtime means during play of the built or running game.

**Source:** Editor automation versus runtime AI

## MA-unreal.2

An Unreal MCP endpoint responds, but the agent cannot find the expected scene-editing tools. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Renaming an Actor adds a missing tool to the server.
- [ ] B. A catalog is the list of tools a server currently advertises.
- [ ] C. A transport is the same thing as a tool.
- [ ] D. A toolset is a group of related tools that is enabled as a unit.
- [ ] E. A reachable endpoint shows the transport works but does not show the needed tool is in the catalog.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: Actor labels do not register tool implementations.
- B: The catalog is what the client can discover and call.
- C: A transport carries messages; a tool is a named operation.
- D: Toolsets let a server expose tools in enabled groups.
- E: Connectivity and tool availability are separate.

**Source:** Endpoint, tool, toolset, catalog

## MA-unreal.3

An Unreal level has twelve Actors created from one Blueprint class. A designer wants one placed Actor to start with a different health value. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A Blueprint class is a template, and a placed Actor is an instance of it.
- [ ] B. An override is an instance value that differs from the class default.
- [ ] C. An instance-level change and a class-default change name the same edit.
- [ ] D. Customizing one instance requires deleting its Blueprint class.
- [ ] E. Editing a class default can reach instances that have not overridden that value.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: The class defines defaults; each placement is an instance.
- B: Overrides replace the inherited default on that instance.
- C: They differ in scope: one object versus the template.
- D: Instances can carry overrides while the class stays in place.
- E: Non-overridden instances inherit the default.

**Source:** Class, instance, override

## MA-unreal.4

An Unreal Actor shows a mesh but a projectile passes through it. A hypothetical tool can inspect and set its components. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A visible mesh implies a Block response toward projectiles.
- [ ] B. A component is a part attached to an Actor, such as a mesh or a collision shape.
- [ ] C. A collision response such as Block, Overlap or Ignore says how a component reacts to another object.
- [ ] D. An Actor's label sets its collision response.
- [ ] E. A mesh's visibility setting is the same property as its collision response.

**Key:** A=F B=T C=T D=F E=F

**Why:**

- A: Rendering and collision are separate settings.
- B: Actors are built from components.
- C: The response setting decides blocking versus passing through.
- D: A label is a display name, not physics configuration.
- E: Visibility affects drawing; collision response affects physics.

**Source:** Component and collision response

## MA-unreal.5

An agent edits a Blueprint graph and reports that it compiles. The requirement is that a door opens when the player holds a key. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A Blueprint graph is a network of nodes joined by execution and data wires.
- [ ] B. Testing a no-key case and a has-key case exercises both sides of the branch.
- [ ] C. Compile success means the graph is structurally valid, not that it matches the requirement.
- [ ] D. A branch node chooses between execution paths using a Boolean condition.
- [ ] E. A compile error and a logic bug are the same kind of fault.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: Graph is the term for the node network.
- B: Each side of the condition needs its own test case.
- C: Compiling does not test the key condition.
- D: Branch splits flow on true or false.
- E: A compile error is structural; a logic bug compiles but behaves wrongly.

**Source:** Compile versus correct logic

## MA-unreal.6

An Unreal tool runs its calls in a queue on the game thread. An agent must create an Actor and then configure it. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Latency is the count of tools a server exposes.
- [ ] B. Concurrent calls are ones that wait for the previous call to finish.
- [ ] C. Serial execution runs calls one after another.
- [ ] D. Throughput is the delay before a single reply arrives.
- [ ] E. A tool that returns before its work is done is called synchronous.

**Key:** A=F B=F C=T D=F E=F

**Why:**

- A: Latency is the delay before a reply.
- B: Concurrent calls overlap in time.
- C: Each call finishes before the next starts.
- D: Throughput is how much work completes per unit time.
- E: That is asynchronous; synchronous returns when done.

**Source:** Serial, concurrent, latency, throughput

## MA-unreal.7

A test tool returns a job identifier with the status accepted before a pressure-plate test finishes. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Polling means the server pushes a message to the client when it is done.
- [ ] B. A job identifier lets the client ask later about that specific job.
- [ ] C. An idempotent operation has a different effect each time it is repeated.
- [ ] D. A timeout status is the same as a failed status.
- [ ] E. Accepted or running is a different status from passed.

**Key:** A=F B=T C=F D=F E=T

**Why:**

- A: Polling is the client repeatedly asking; pushing is a notification.
- B: The identifier names the running job.
- C: Idempotent means repeating it has the same effect as doing it once.
- D: A timeout leaves the outcome unknown.
- E: Launching is not the same as finishing successfully.

**Source:** Asynchronous job status

## MA-unreal.8

An Unreal agent places Actors in a level and sees them in the editor. The request is a level that a teammate can open. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A dirty asset has changes in memory that are not yet saved.
- [ ] B. A dependency is an asset another asset refers to, and the level needs it present on the teammate's side.
- [ ] C. Saving an unrelated level writes the edited Actors into the requested level.
- [ ] D. A commit is the same as a save in the editor.
- [ ] E. A screenshot of the viewport is evidence of persistence.

**Key:** A=T B=T C=F D=F E=F

**Why:**

- A: Dirty marks unsaved edits.
- B: Referenced content has to travel with the level.
- C: Each level is saved on its own.
- D: Saving writes the package; a commit records files in version control.
- E: It shows appearance in memory, not saved content.

**Source:** Saved state, package, dependency

## MA-unreal.9

A hypothetical tool can launch an automation test for a pressure plate that should open a door. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Setting the door's open flag directly bypasses the trigger being tested.
- [ ] B. A fixture is the log produced after a test.
- [ ] C. An assertion is a check that a stated condition holds.
- [ ] D. A regression test checks that earlier working behaviour still works after a change.
- [ ] E. A flaky test gives the same result on each run.

**Key:** A=T B=F C=T D=T E=F

**Why:**

- A: It skips the causal path under test.
- B: A fixture is the prepared setup state.
- C: Assertions turn the expected result into a pass or fail.
- D: Regression means something that used to work broke.
- E: Flaky means the result varies without a code change.

**Source:** Test terms

## MA-unreal.10

An agent changes an Actor during a play session, but the designer expected the saved level to change. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A runtime instance and the authoring level asset are the same object.
- [ ] B. A change to a play-session Actor is transient and is discarded when play ends.
- [ ] C. Play-in-editor runs a temporary copy of the level's Actors.
- [ ] D. Authoring data is the saved level and asset content that lasts on disk.
- [ ] E. Persisting a change means leaving the play session running longer.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: They are different objects with different persistence.
- B: Transient means not persisted.
- C: The play world is separate from the authored level.
- D: Authoring is what a save writes.
- E: Persistence needs a save to the authoring data.

**Source:** Authoring versus runtime state

## MA-unreal.11

Two Unreal Actors reference one material instance asset. A designer wants only the first Actor to change appearance. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The word instance in the name means the asset is private to one Actor.
- [ ] B. An Actor's label names the material it uses.
- [ ] C. Two Actors that reference the same material instance asset share its parameter values.
- [ ] D. A dynamic material instance is a saved asset in the content folder.
- [ ] E. A material instance asset is a saved child of a parent material with changed parameters.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: Several Actors can reference one instance asset.
- B: A label is a display name only.
- C: Editing the shared asset affects both.
- D: A dynamic material instance is created at runtime.
- E: The instance overrides parameters of its parent.

**Source:** Material instance scope

## MA-unreal.12

A custom tool replaces selected placeholder Actors with approved props and must keep each transform. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A preflight check validates inputs before a change is made.
- [ ] B. Rollback means restoring the earlier state after a failed operation.
- [ ] C. An invariant is a condition that stays true across the operation, such as an unchanged transform.
- [ ] D. A partial failure leaves some targets changed and others not.
- [ ] E. An atomic operation can stop with some targets changed and others unchanged.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: Preflight runs before mutation.
- B: Rollback undoes the change.
- C: The transform is the property to preserve.
- D: Mixed outcomes are what the term names.
- E: Atomic means the whole change happens or none of it does.

**Source:** Batch operation vocabulary

## MA-unreal.13

An Unreal MCP service is set up for same-machine use. A teammate proposes forwarding its port so a remote agent can connect. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Binding to a different address supplies authentication.
- [ ] B. Port forwarding extends who can reach an endpoint.
- [ ] C. Authentication and authorization are two names for checking identity.
- [ ] D. Authentication verifies who is calling, and authorization decides what that caller may do.
- [ ] E. Binding to loopback makes an endpoint reachable from the same machine.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: An address controls reachability, not identity.
- B: It opens a new route to the service.
- C: Authorization decides what an identified caller may do.
- D: They are separate checks.
- E: Loopback is the local-only address.

**Source:** Binding, reachability, authentication

## MA-unreal.14

A designer tells an agent: Put five checkpoints in the level at these spots. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Placing adds an instance to the level and editing the Blueprint changes the class.
- [ ] B. Rotation is the term for how large an object is.
- [ ] C. A nickname for an asset is a more precise reference than its asset path.
- [ ] D. A transform combines location, rotation and scale.
- [ ] E. World-space coordinates are measured from the level origin, and relative coordinates from a parent.

**Key:** A=T B=F C=F D=T E=T

**Why:**

- A: Placement and class editing differ in scope.
- B: Size is scale; rotation is orientation.
- C: A full path names one asset unambiguously.
- D: Those three values describe placement.
- E: The coordinate space has to be stated.

**Source:** Placement and transform vocabulary

## MA-unreal.15

A Blueprint door compiles but opens twice from one visit by the player. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The tick event fires once when the level loads.
- [ ] B. An overlap event fires when two collision components begin to intersect.
- [ ] C. A Boolean variable is another word for an event.
- [ ] D. A duplicate binding registers the same handler twice, so one event runs it twice.
- [ ] E. Begin overlap and end overlap name the same event.

**Key:** A=F B=T C=F D=T E=F

**Why:**

- A: Tick fires each frame.
- B: Overlap is intersection of collision shapes.
- C: A Boolean holds true or false; an event is a signal.
- D: Double registration causes repeated action.
- E: They fire at entry and at exit.

**Source:** Events and bindings

## MA-unreal.16

A designer writes to an agent: Change the Blueprint so this one chest is gold. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A precise rewrite is: Override the material on this placed chest instance.
- [ ] B. This one chest is a Blueprint class reference.
- [ ] C. Override is the term for an instance value that differs from the class default.
- [ ] D. A Blueprint edit changes the class default for chests that have not overridden it.
- [ ] E. Blueprint names the class, so for one placed chest instance is the precise word.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: Override states the per-instance difference.
- B: It names a placed object, an instance.
- C: That is the standard meaning.
- D: Non-overridden instances inherit the change.
- E: The request is scoped to one instance.

**Source:** Wrong word in a prompt

## MA-unreal.17

An agent tool reports its results. Check the vocabulary used about tools. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A query tool and a mutating tool are both called read-only.
- [ ] B. A parameter is the value supplied in one call, and an argument is the name in the schema.
- [ ] C. A tool's result is the name of the tool.
- [ ] D. A mutating tool is one that changes project state.
- [ ] E. A read-only tool changes the scene it inspects.

**Key:** A=F B=F C=F D=T E=F

**Why:**

- A: Only the query tool is read-only.
- B: The terms are swapped: parameters are declared, arguments are supplied.
- C: A result is what the tool returns.
- D: Mutating means writing or altering.
- E: Read-only means no change to state.

**Source:** Tool, parameter, result

## MA-unreal.18

A tool replaced four of ten placeholder Actors, failed on the fifth and stopped. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A per-target result lists the outcome for each object separately.
- [ ] B. An aggregate success message is a per-object record.
- [ ] C. Resuming continues from the failed step, and rollback restores the earlier state.
- [ ] D. Resume and rollback are two words for the same recovery.
- [ ] E. A target identity is a stable reference to one object, such as its object path, not its label.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: It makes partial completion visible.
- B: Aggregate hides individual outcomes.
- C: Those are the two recovery directions.
- D: Resume continues forward; rollback restores the earlier state.
- E: Labels can repeat; identities distinguish objects.

**Source:** Recovery terms

## MA-unreal.19

An agent reports work done after several checks. Check the vocabulary used about verification. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Compile and play test name the same activity.
- [ ] B. Acceptance criteria are conditions that define when work counts as done.
- [ ] C. A smoke test is a long review of rare edge cases.
- [ ] D. Diagnostics are the assets a test places in the level.
- [ ] E. To validate an asset is to check it against rules, and to test is to run it and observe behaviour.

**Key:** A=F B=T C=F D=F E=T

**Why:**

- A: Compiling checks structure; play testing observes behaviour.
- B: They set the pass line before work starts.
- C: A smoke test is a quick check that the basics run.
- D: Diagnostics are messages and logs explaining a result.
- E: Validation inspects; testing exercises.

**Source:** Validate, test, accept, diagnose

## MA-unreal.20

An Unreal agent is asked about basic object vocabulary. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An asset is a saved piece of content such as a mesh, a material or a Blueprint.
- [ ] B. Spawn means to remove an Actor from the level.
- [ ] C. An Actor is an object that can be placed or spawned in a level.
- [ ] D. A level is a type of component.
- [ ] E. A component is a piece of functionality or data attached to an Actor.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: Assets are stored content files.
- B: Spawn creates an Actor at runtime.
- C: Actor is the base placeable object.
- D: A level is a container of Actors.
- E: Components make up an Actor.

**Source:** Actor, component, asset, spawn
