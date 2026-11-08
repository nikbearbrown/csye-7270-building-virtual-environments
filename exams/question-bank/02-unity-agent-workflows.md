# Unity, Spark and agent workflows

## MA-unity.1

Unity Spark is described as a browser-based game-creation experience, and a Unity MCP integration exposes editor capabilities to an external assistant. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Installing an MCP server gives access to Spark.
- [ ] B. Two products from one vendor share the same project workflow.
- [ ] C. Spark names a product experience, while an MCP integration names an interface to editor capabilities.
- [ ] D. Spark is the expanded name of the acronym MCP.
- [ ] E. What an installed MCP server can do is found by inspecting the tools it advertises.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: An interface does not grant a separate product.
- B: Workflow compatibility needs evidence.
- C: They are different kinds of thing.
- D: MCP stands for Model Context Protocol.
- E: Capabilities come from discovery, not from a product name.

**Source:** Spark versus MCP

## MA-unity.2

A teammate says, "Unity Spark is Unity's MCP, so installing an MCP server gives us Spark." Which statements correct the wording? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Evaluating an installed MCP integration begins by opening Spark in a browser.
- [ ] B. Installing an interface gives access to a separate product experience.
- [ ] C. Spark is evaluated by listing its MCP tools.
- [ ] D. MCP stands for Model Context Protocol.
- [ ] E. Spark is a creation experience, not a protocol.

**Key:** A=F B=F C=F D=T E=T

**Why:**

- A: An integration is evaluated through its own tools.
- B: Access to a product is not a side effect of an interface.
- C: Spark is a product experience judged on the games it produces.
- D: That is the expansion of the acronym.
- E: The two words name different categories.

**Source:** correcting a mixed-up claim

## MA-unity.3

A vendor note says an older in-editor MCP server is deprecated and a CLI-hosted MCP server replaces it. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Deprecating one server retires the MCP protocol.
- [ ] B. A replacement server's tool catalog can differ, so tool names and contracts are checked again.
- [ ] C. Deprecated means still present but discouraged and planned for removal.
- [ ] D. A pilot in a small project is unnecessary once a vendor note exists.
- [ ] E. Deleting the project's scenes is the first migration step.

**Key:** A=F B=T C=T D=F E=F

**Why:**

- A: A component lifecycle is not a protocol lifecycle.
- B: Names and arguments are not carried over by assumption.
- C: It is a lifecycle label for a component.
- D: A pilot exposes compatibility problems before production.
- E: Migrating a connection does not touch game content.

**Source:** deprecation and replacement

## MA-unity.4

A team plans to migrate from an older MCP server to its replacement. Which statements use the terms correctly? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A query that reads is the riskiest first test of a new connection.
- [ ] B. A reversible edit is a change that is impossible to undo.
- [ ] C. A checkpoint is a recoverable snapshot of the project and configuration taken before the change.
- [ ] D. A query that reads changes the scene slightly.
- [ ] E. A rollback route is a documented way to return to the previous setup.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: Reading is low risk compared with writing.
- B: Reversible means it can be undone.
- C: It lets the team return to a known state.
- D: A query reads and does not modify.
- E: Rollback undoes the migration.

**Source:** migration terms

## MA-unity.5

A Unity automation package offers direct command-line commands and an MCP interface to the same editor operations. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Both routes need the editor operation's result checked.
- [ ] B. An MCP tool advertises an input schema that describes its arguments.
- [ ] C. Direct commands can automate a task without a language-model inference.
- [ ] D. Which route is usable depends on whether the agent host supports MCP tools or can run shell commands.
- [ ] E. Direct commands need no authorization because no MCP message is sent.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: The interface does not prove correctness.
- B: The schema is part of the tool definition.
- C: A script can call known operations directly.
- D: Hosts differ in the interfaces they offer.
- E: They can still change project state.

**Source:** CLI versus MCP

## MA-unity.6

Two Unity projects are open and each has a scene named Arena. An agent is asked to add a light to one project's Arena. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The most recently opened editor is the target.
- [ ] B. A scene name is ambiguous across projects, so an asset path within a named project is a better selector.
- [ ] C. A successful tool connection identifies the intended project.
- [ ] D. A light in either Arena satisfies the request.
- [ ] E. The agent verifies project identity as well as scene identity.

**Key:** A=F B=T C=F D=F E=T

**Why:**

- A: Recency is not user intent.
- B: Qualified identifiers remove the ambiguity.
- C: Connectivity does not show the user's intent.
- D: The destination project is part of the request.
- E: A shared scene name is ambiguous.

**Source:** project and scene identity

## MA-unity.7

A scene has twenty instances of a lamp prefab, and one named lamp should turn blue. Which statements use the terms correctly? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Reverting an override returns the instance to the prefab's value.
- [ ] B. A prefab instance is a placed copy in the scene that stays linked to its prefab asset.
- [ ] C. Deleting the prefab asset is a way to isolate one lamp.
- [ ] D. An override changes a value on one instance without changing the prefab asset.
- [ ] E. Applying an override to the prefab keeps the change on one instance.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: Revert discards the per-instance difference.
- B: Instances derive from the prefab asset.
- C: That damages the reusable asset.
- D: Overrides are per-instance differences.
- E: Applying writes the change into the prefab asset, so other instances pick it up.

**Source:** prefab instance versus asset

## MA-unity.8

Twenty lamps reference one material asset, and one lamp should be blue. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A MaterialPropertyBlock overrides properties for one renderer without editing the material asset.
- [ ] B. A material instance is a per-renderer copy, so changing it leaves the other lamps alone.
- [ ] C. Moving a lamp makes its material reference independent.
- [ ] D. Looking at the selected lamp shows that the other lamps are unchanged.
- [ ] E. Editing the shared material asset changes each renderer that references it.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: It is a per-renderer property override.
- B: Instancing separates one renderer from the shared asset.
- C: Transform changes do not clone materials.
- D: Unchanged lamps need their own check.
- E: The reference is shared.

**Source:** shared material versus instance

## MA-unity.9

An agent changes one wall's material colour, and several other walls change too. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Moving the changed wall gives its material an independent copy.
- [ ] B. The walls reference the same material asset, which explains the propagation.
- [ ] C. Editing the shared material is the correct fix whatever the intended scope.
- [ ] D. The extra changes show a transport fault in the MCP connection.
- [ ] E. A screenshot of the selected wall shows the scope was correct.

**Key:** A=F B=T C=F D=F E=F

**Why:**

- A: A transform does not clone a material.
- B: One definition feeds each consumer.
- C: The intended scope decides whether to edit the asset or use a per-object approach.
- D: Shared asset semantics already explain them.
- E: It does not show unintended changes elsewhere.

**Source:** shared asset propagation

## MA-unity.10

An agent edits a script to add a field, then tries to set it on the component, and the editor shows compilation errors. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Hiding the console errors makes the new component definition usable.
- [ ] B. Repeating the field assignment repairs a compiler error.
- [ ] C. A serialized field is a field Unity stores with the component, such as a public field.
- [ ] D. The field is available as soon as the script file is saved.
- [ ] E. A compilation error means the new script version is not loaded, so the component keeps its old layout.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: Display filtering does not fix compilation.
- B: The cause is in the code or dependencies.
- C: Serialization is what makes a field settable in the editor.
- D: Saved bytes do not mean the code compiled.
- E: The old compiled definition stays in use.

**Source:** compilation and serialized field

## MA-unity.11

After a script change, an agent plans its repair steps. Which statements use the terms correctly? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Suppressing the error message counts as addressing the diagnostics.
- [ ] B. The sequence is compile, reload, inspect the component, set the field, read it back, then test the behaviour.
- [ ] C. A read-back means reading the value from the editor after setting it.
- [ ] D. Compiler diagnostics are the messages that name the location and cause of an error.
- [ ] E. Reading the script file's text is equivalent to a read-back from the component.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: The cause remains.
- B: Each step depends on the one before.
- C: It confirms the stored state.
- D: They guide the code fix.
- E: The component's loaded state is a different thing.

**Source:** repair and read-back

## MA-unity.12

A tool reports a successful scene edit, but after closing and reopening the project the change is gone. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A success result can describe a completed mutation without a completed save.
- [ ] B. In-memory state is the scene as the open editor holds it, and saved state is the scene file on disk.
- [ ] C. The missing change shows the language model forgot the scene.
- [ ] D. Reopening the saved scene is a persistence check.
- [ ] E. A dirty scene is one with unsaved changes.

**Key:** A=T B=T C=F D=T E=T

**Why:**

- A: The tool contract defines what success covers.
- B: They can differ until a save.
- C: Persistence is an editor and storage matter.
- D: It tests whether the change survives a reload.
- E: The editor marks such scenes as dirty.

**Source:** in-memory versus saved

## MA-unity.13

A texture file was copied into a Unity project and the editor is still importing it. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An import error shows that the file was not copied.
- [ ] B. The file's presence on disk shows the asset is ready.
- [ ] C. Copying the file again is a way to wait for import.
- [ ] D. Assigning a placeholder proves the requested texture imported.
- [ ] E. A file on disk becomes an asset the engine can use once the editor imports it.

**Key:** A=F B=F C=F D=F E=T

**Why:**

- A: Copying and importing are separate steps.
- B: Filesystem presence and engine readiness differ.
- C: Duplicates add ambiguity.
- D: A placeholder is a different asset.
- E: Import is the processing step.

**Source:** import readiness

## MA-unity.14

A parent object is translated ten units along one axis with identity rotation and scale, and its child has local position zero. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A child's local transform is applied relative to its parent's transform.
- [ ] B. A world-origin requirement needs a conversion or a tool that accepts world coordinates.
- [ ] C. World position is measured from the scene origin, while local position is measured from the parent.
- [ ] D. The child sits at the parent's world position.
- [ ] E. Local position zero puts the child at the world origin.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: Local space is the parent's space.
- B: The coordinate space must match the requirement.
- C: Those are the two reference frames.
- D: Zero local offset means the parent's origin.
- E: The parent's translation contributes.

**Source:** local versus world

## MA-unity.15

A designer asks an agent, "Put some checkpoints in the level." Which rewrites use exact terms? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Create three instances of the existing checkpoint prefab asset in the named scene of the named project.
- [ ] B. Find the prefab by its display name alone.
- [ ] C. Leave the prefab asset unchanged unless an approved change is named.
- [ ] D. Set each instance's world-space position to the supplied coordinates, with units stated.
- [ ] E. Make three new prefab assets in the level.

**Key:** A=T B=F C=T D=T E=F

**Why:**

- A: It separates instance, asset, scene and project.
- B: Display names can repeat.
- C: It protects the shared definition.
- D: It names the space and the units.
- E: Placed objects in a scene are instances, not new assets.

**Source:** exact instruction for a Unity agent

## MA-unity.16

An agent imports a mesh, creates a prefab and places instances in three steps. Import succeeds and prefab creation fails. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Cleanup removes assets of unknown origin along with the failed attempt's artifacts.
- [ ] B. An idempotent operation repeated gives the same final state as running it once.
- [ ] C. Identifying the first failed stage guides which step to retry.
- [ ] D. A targeted retry reuses the verified import instead of creating duplicates.
- [ ] E. A partial failure means some steps completed and others did not.

**Key:** A=F B=T C=T D=T E=T

**Why:**

- A: Only artifacts known to belong to the attempt are removed.
- B: Idempotence makes retries safe.
- C: Recovery starts at the failure.
- D: The import is already good.
- E: Here import completed and the later steps did not.

**Source:** partial failure and idempotence

## MA-unity.17

A team proposes a tool that sets the intensity of one identified light, instead of giving the agent a general script evaluator. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A narrow tool still needs authorization because it writes to the project.
- [ ] B. A narrow tool validates the light's identity and an allowed intensity range.
- [ ] C. A free-text request to be careful enforces the same limits as argument validation.
- [ ] D. A narrow tool is free of bugs because it is narrow.
- [ ] E. Reporting the previous and resulting intensity supports review and recovery.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: A narrow write is still a write.
- B: Validation narrows the operation.
- C: Instructions are not a technical boundary.
- D: Its implementation still needs verification.
- E: It records the actual change.

**Source:** narrow tool versus script evaluator

## MA-unity.18

A team compares a general script evaluator with three narrow lighting tools. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. If a legitimate operation is missing, the right step is to extend the narrow tools.
- [ ] B. A general evaluator has a larger blast radius, since it can act far beyond lighting edits.
- [ ] C. Least privilege means giving the agent the smallest set of permissions its task needs.
- [ ] D. Logging old and new values and affected identifiers gives an audit record.
- [ ] E. A general evaluator is the safer design because it is flexible.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: Improvising with undocumented calls bypasses the contract.
- B: Blast radius is the reach of a possible mistake.
- C: Narrow tools apply that principle.
- D: An audit record supports review.
- E: Flexibility widens what can go wrong.

**Source:** scope and least privilege

## MA-unity.19

A team receives a playable prototype from an AI-assisted game-creation workflow. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Being able to create a prototype shows support for the team's export workflow.
- [ ] B. A convincing demonstration shows the team can maintain the project.
- [ ] C. Acceptance criteria are written, testable conditions that decide whether a deliverable is accepted.
- [ ] D. Performance is judged on the target device, not in a browser preview.
- [ ] E. Provenance describes where assets came from and under what rights they may be used.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: Export capability is checked separately.
- B: Maintainability needs working with the deliverable.
- C: They turn requirements into checks.
- D: A preview does not show release performance.
- E: It matters for distribution.

**Source:** evaluating a generated prototype

## MA-unity.20

A browser demo looks impressive, but the team needs keyboard controls, a save system and a defined target platform. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Accessible keyboard controls, such as remapping, are requirements to test.
- [ ] B. Each requirement is turned into an observable check, such as pressing a key and watching the result.
- [ ] C. Generated assets carry no usage restrictions.
- [ ] D. Save and load behaviour is checked by saving, restarting and loading.
- [ ] E. A browser demo counts as a build for the target platform.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: Accessibility is checked by use.
- B: Observable means it can be seen to pass or fail.
- C: Rights and dependencies are checked.
- D: It tests persistence across a restart.
- E: The target platform needs its own build.

**Source:** prototype acceptance
