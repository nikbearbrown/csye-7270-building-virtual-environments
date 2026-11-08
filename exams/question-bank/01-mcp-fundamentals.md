# MCP fundamentals

## MA-mcp.1

A designer says, "We use MCP so the AI can drive our editor." Which statements use the terms protocol, model and inference correctly? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. MCP is the model that does the inference.
- [ ] B. Inference is the step where the language model produces output from its input.
- [ ] C. Connecting an MCP server retrains the model on the project's assets.
- [ ] D. MCP is a rendering technique for the editor viewport.
- [ ] E. A protocol is an agreed set of message formats and behaviours between applications.

**Key:** A=F B=T C=F D=F E=T

**Why:**

- A: Inference is done by the language model; MCP is the connection standard around it.
- B: Inference means running the trained model to get a reply.
- C: Connecting a service does not change model weights.
- D: MCP says nothing about drawing; it connects applications to tools and context.
- E: That is the meaning of protocol, and MCP is one.

**Source:** protocol versus model

## MA-mcp.2

An assistant application uses a connector to reach a service that exposes editor operations. Which statements name the roles correctly? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A server can run as a local process on the same machine.
- [ ] B. The client is the part of the host that holds the connection to a server.
- [ ] C. The host is the assistant application the user works in.
- [ ] D. The client is the player character in the level that calls the service.
- [ ] E. The server is the service that exposes tools, resources and prompts.

**Key:** A=T B=T C=T D=F E=T

**Why:**

- A: Server names a role, not a location.
- B: A client maintains one connection to a server on the host's behalf.
- C: The host contains the user interaction and the clients.
- D: The client is the protocol connector, not an in-game character.
- E: Exposing capabilities is the server role.

**Source:** host, client, server

## MA-mcp.3

A teammate writes, "The MCP server in the Claude app calls our editor client to run commands." Which statements correct the wording? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The Claude app is the host, not the server.
- [ ] B. Host and server are synonyms, so the note needs no fix.
- [ ] C. The editor-facing service that offers the commands plays the server role.
- [ ] D. The editor plugin that offers the commands is the client.
- [ ] E. The part of the host that opens the connection is the client, and it calls the server.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: The assistant application is the host.
- B: They are different roles with different jobs.
- C: It supplies the external capabilities.
- D: The service offering commands is the server.
- E: Clients call servers, not the reverse.

**Source:** role words in a note

## MA-mcp.4

Which statements give the correct meaning of the three server primitives? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A tool is an operation the model can invoke with arguments, and it may have side effects.
- [ ] B. A prompt is a reusable message or workflow template that a server offers.
- [ ] C. A tool is readable content identified by a URI.
- [ ] D. A prompt is the text the model writes back to the user.
- [ ] E. A resource is an operation that changes the scene when it is called.

**Key:** A=T B=T C=F D=F E=F

**Why:**

- A: Tools perform actions.
- B: Prompts are templates the client can retrieve.
- C: That describes a resource.
- D: That is the model's reply, not a prompt primitive.
- E: A resource supplies readable context; it is not an action.

**Source:** tool, resource, prompt definitions

## MA-mcp.5

A hypothetical editor server offers a spawn operation with arguments, a scene manifest at a URI, and a reusable lighting-review template. Which statements name the primitives correctly? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The review template is a prompt.
- [ ] B. Retrieving the review template counts as running the review.
- [ ] C. The review template is a tool because it can be reused.
- [ ] D. The spawn operation is a tool.
- [ ] E. The scene manifest is a resource.

**Key:** A=T B=F C=F D=T E=T

**Why:**

- A: Prompts are reusable templates.
- B: Getting instructions does not carry them out.
- C: Reusable message templates are prompts.
- D: It is invoked with inputs to do something.
- E: It is URI-addressed content that a client reads.

**Source:** matching primitives to examples

## MA-mcp.6

An agent remembers a tool name from a tutorial, but the connected server does not list it. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Tool discovery means asking the server for the tools it advertises and then calling one of those.
- [ ] B. A name remembered from a tutorial substitutes for the advertised tool definition.
- [ ] C. Two servers can advertise differently named or shaped tools for the same goal.
- [ ] D. An input schema is the list of tools a server has installed.
- [ ] E. Renaming a scene object to the tutorial's tool name makes the server advertise that tool.

**Key:** A=T B=F C=T D=F E=F

**Why:**

- A: Discovery grounds the call in the live server.
- B: Names and arguments differ between integrations.
- C: Tool catalogs are implementation-specific.
- D: A schema describes one tool's arguments.
- E: Object names do not register server operations.

**Source:** tool discovery

## MA-mcp.7

A move tool's input schema lists object_id (a string) and distance (a number). It gives no units or coordinate space. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Reading back the resulting transform checks the effect beyond schema validity.
- [ ] B. Units and coordinate space are semantics that come from the tool contract or an inspected example.
- [ ] C. Because distance is a number, the unit is metres by default.
- [ ] D. A request that passes schema validation targets the intended object.
- [ ] E. Schema validation checks the type and shape of arguments, not what the values mean.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: A read-back is verification of the outcome.
- B: They are not in the type.
- C: A type does not carry a unit.
- D: Identity is checked separately.
- E: Semantics are outside what a type check covers.

**Source:** schema versus semantics

## MA-mcp.8

A trace shows JSON-RPC messages between a client and a server. Which statements use the terms correctly? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The id is the index of the target actor in the level.
- [ ] B. A well-formed JSON message shows the requested edit succeeded.
- [ ] C. A response carries the same id as the request it answers.
- [ ] D. A missing response to a notification shows the connection is broken.
- [ ] E. A notification carries no id and gets no response.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: The id correlates messages; it is not an engine identity.
- B: Syntax says nothing about the operation's result.
- C: The id pairs a reply with its request.
- D: No reply is expected for a notification.
- E: Notifications are one-way messages.

**Source:** JSON-RPC correlation

## MA-mcp.9

Two integrations carry MCP messages over stdio and over Streamable HTTP. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Switching transport translates Unity components into Unreal components.
- [ ] B. A transport carries messages and does not define the editor operations.
- [ ] C. A transport fault can stop a valid request from reaching the server.
- [ ] D. With stdio, the client launches the server as a subprocess and exchanges messages over its standard streams.
- [ ] E. Streamable HTTP can reach a server on the same machine.

**Key:** A=F B=T C=T D=T E=T

**Why:**

- A: A transport does not convert engine data.
- B: Delivery and scene-editing semantics are separate layers.
- C: Delivery can fail before execution.
- D: That is how the stdio transport works.
- E: HTTP does not imply a remote service.

**Source:** transports

## MA-mcp.10

A tool call returns a structured reply saying the named scene object could not be found. Which statements describe the failure correctly? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. This is a transport failure, so the next step is changing the network port.
- [ ] B. The object identity is irrelevant to the next investigation.
- [ ] C. Reinstalling the language model is the first diagnosis the evidence supports.
- [ ] D. A structured reply shows that the object was modified.
- [ ] E. This is a tool execution error: the operation ran and reported failure in its result.

**Key:** A=F B=F C=F D=F E=T

**Why:**

- A: The reply arrived, so delivery worked.
- B: The error concerns the target, so identity and scene state are next.
- C: Nothing points at the model.
- D: The reply states the opposite.
- E: Domain failure travels inside a successful exchange.

**Source:** layered errors

## MA-mcp.11

A client and a server both say they support MCP, yet initialization fails. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A small call that reads without modifying is a low-risk interoperability check before edits.
- [ ] B. Each side declares the protocol revision it supports during initialization.
- [ ] C. A tutorial's handshake sequence is enough evidence of the current requirements.
- [ ] D. A capability is a rendering feature of the engine exposed to the client.
- [ ] E. The MCP name guarantees both sides support the same revision.

**Key:** A=T B=T C=F D=F E=F

**Why:**

- A: It tests communication without changing the scene.
- B: Revision is negotiated at the start of the connection.
- C: Lifecycle rules change between revisions.
- D: Capabilities are optional protocol features each side declares.
- E: A product label is not a compatibility guarantee.

**Source:** revision and capabilities

## MA-mcp.12

A resource read returned a list of lights, and a designer then deleted one. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The deletion turns the earlier response into a protocol error.
- [ ] B. Re-resolving the target means looking the object up again by identifier before editing.
- [ ] C. A stale snapshot is data that no longer matches the live scene.
- [ ] D. Reading a resource locks the scene against later editor changes.
- [ ] E. The returned list is a snapshot of the scene at read time.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: The response was valid when produced.
- B: It confirms the object still exists.
- C: Staleness is the mismatch with current state.
- D: A read does not freeze the scene.
- E: It records state at one moment.

**Source:** stale snapshot

## MA-mcp.13

Two engine servers both advertise a tool described as creating an object. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Creating an object may yield an Actor in Unreal and a GameObject in Unity, which are different engine concepts.
- [ ] B. MCP standardizes communication, not a universal game-editor API.
- [ ] C. The argument schemas of the two tools can differ.
- [ ] D. Matching descriptions mean matching side effects.
- [ ] E. A shared protocol makes asset files loadable in both engines.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: The same intent maps to different engine objects.
- B: Operations stay engine-specific.
- C: Each server defines its own tool contract.
- D: Behaviour must be checked, not inferred from a description.
- E: Asset formats are outside the protocol.

**Source:** interoperability limits

## MA-mcp.14

An operator sets a limit of ten edit attempts for an agent that edits and tests a scene. Which statements use the terms correctly? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Reaching the limit shows the scene is correct.
- [ ] B. Dropping a failing requirement satisfies it.
- [ ] C. Comparing observed state with the requested outcome after an edit is verification.
- [ ] D. A stopping condition is the same thing as an acceptance criterion.
- [ ] E. A retry limit is a stopping condition that bounds the repair loop.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: A limit stops work; it does not accept the result.
- B: Changing the target hides the failure.
- C: Verification checks the result, not just that a call was made.
- D: Acceptance asks whether the outcome meets the request; stopping asks when to quit.
- E: It ends repeated attempts.

**Source:** bounded loop

## MA-mcp.15

Check each statement that correctly separates inference, tool execution and gameplay execution. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Inference is the language model producing its reply.
- [ ] B. Where the server is deployed is separate from where inference runs.
- [ ] C. Gameplay execution is the MCP server running the player's scripts as the game is played.
- [ ] D. Tool execution is the server carrying out an operation in the editor.
- [ ] E. Tool execution is the language model predicting the next token.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: The model computes the reply.
- B: Local or remote deployment is a configuration choice.
- C: Gameplay runs in the game runtime.
- D: The server performs the requested operation.
- E: That is inference.

**Source:** inference versus execution

## MA-mcp.16

A designer asks an agent, "Hook the AI up to the lighting stuff." Which statements are exact rewrites? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Expose create-light as a tool with arguments for target scene and intensity.
- [ ] B. Expose the scene inventory as a resource.
- [ ] C. Reading the inventory resource first lets the agent choose where to call the create-light tool.
- [ ] D. Expose the review checklist as a resource that runs the review when read.
- [ ] E. Expose the reusable checklist as a prompt template.

**Key:** A=T B=T C=T D=F E=T

**Why:**

- A: An operation with inputs is a tool.
- B: Readable context fits the resource primitive.
- C: Context informs the action.
- D: Reading a resource supplies content and does not run a review.
- E: Reusable templates are prompts.

**Source:** mapping a vague request to primitives

## MA-mcp.17

A move-object tool is specified for an editor where several objects share a display name. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An unambiguous identifier should select the target, not the display name.
- [ ] B. An offset moves relative to the current position, while an absolute destination sets the final position.
- [ ] C. The contract states units and coordinate space.
- [ ] D. An offset and an absolute destination give the same result regardless of the starting position.
- [ ] E. A display name is a unique identifier.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: Display names can repeat.
- B: They are different input meanings.
- C: Without them the number is ambiguous.
- D: They agree only by coincidence.
- E: Several objects share it.

**Source:** tool contract

## MA-mcp.18

A tool call reached the server but nothing appears in the editor. Which symptoms are matched to the right layer? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A rejection saying a required argument is missing is an argument validation failure.
- [ ] B. An edit applied in the wrong scene is found by verification against the request.
- [ ] C. A connected status indicator shows the operation executed.
- [ ] D. An engine error logged while the operation ran is a delivery failure.
- [ ] E. A request with no matching response points first at delivery.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: Validation checks the arguments before execution.
- B: Verification compares the scene with the requested outcome.
- C: Connection status says nothing about execution.
- D: That is an execution failure.
- E: Responses are matched by id.

**Source:** diagnostic layers

## MA-mcp.19

A studio uses a cloud-hosted model with a local Unity editor server. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Sending project context to the remote model crosses a data-disclosure boundary.
- [ ] B. Context filtering is the control for the permission boundary.
- [ ] C. The two boundaries are one boundary, so one control covers both.
- [ ] D. A local server keeps project context off the remote model.
- [ ] E. Invoking a tool that edits the local project crosses a permission boundary.

**Key:** A=T B=F C=F D=F E=T

**Why:**

- A: Content leaves the machine.
- B: Filtering limits disclosure; scoped tools limit permission.
- C: Disclosure and permission are distinct.
- D: Context passed through the host still reaches the model.
- E: An action needs authorization.

**Source:** data and permission boundaries

## MA-mcp.20

A plugin works with client X but fails with client Y. Which statement describes a sound investigation? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Comparing a minimal trace of read calls separates transport, discovery and capability problems.
- [ ] B. Retesting on the production scene gives the lowest risk.
- [ ] C. Recording the supported protocol revisions is unnecessary evidence.
- [ ] D. Failing with client Y shows the plugin does not implement MCP.
- [ ] E. Inventing a method the specification does not define is a valid way to force a connection.

**Key:** A=T B=F C=F D=F E=F

**Why:**

- A: It isolates the layer without changing the scene.
- B: An isolated project limits risk.
- C: Revision differences are a common cause.
- D: It works with client X.
- E: Unsupported methods hide the mismatch.

**Source:** compatibility investigation

## MA-mcp.21

A human and an agent edit the same level, and the agent planned from an inventory read minutes earlier. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A lock is unnecessary when the agent is faster than the human.
- [ ] B. The inventory is a stale observation, not the current authority.
- [ ] C. On a conflict the agent should stop or replan from fresh state.
- [ ] D. A precondition check compares current state with the snapshot before a write.
- [ ] E. Silently overwriting counts as resolving a conflict.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: Speed does not prevent conflicting writes.
- B: The scene may have changed since the read.
- C: It avoids overwriting the human's work.
- D: It detects conflicting changes.
- E: It discards the other edit.

**Source:** concurrent editing

## MA-mcp.22

A checkpoint-placing workflow is shared between Unity and Unreal. Which statements are correct? Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Creating objects and referencing assets belongs to the shared layer.
- [ ] B. Tool names and argument meanings can be reused between adapters without checking.
- [ ] C. The shared layer holds intent, such as count, locations and activation behaviour.
- [ ] D. An adapter maps the shared intent onto an engine's own operations.
- [ ] E. Passing verification in one engine shows the other engine passes.

**Key:** A=F B=F C=T D=T E=F

**Why:**

- A: Those are engine-specific.
- B: Each adapter's contract differs.
- C: Intent is engine-neutral.
- D: Adapters hold the engine-specific part.
- E: Gameplay is verified in each engine separately.

**Source:** shared layer and adapter
