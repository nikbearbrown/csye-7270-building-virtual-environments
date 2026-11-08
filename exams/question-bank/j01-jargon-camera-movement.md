# Jargon test: camera movement

## MA-jargon.1

A director describes camera moves to a coding agent, and the agent builds exactly the move that the word names. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A roll spins the camera around the direction it is looking, which tips the horizon.
- [ ] B. A tilt turns the camera left or right on the spot, without changing where the camera is.
- [ ] C. A pan turns the camera up or down on the spot, without changing where the camera is.
- [ ] D. A tilt lifts the camera straight up on a crane while it keeps facing the same way.
- [ ] E. A pan moves the camera sideways through the scene while it keeps facing the same way.

**Key:** A=T B=F C=F D=F E=F

**Why:**

- A: A roll rotates about the viewing direction, so the horizon line tilts.
- B: Left and right rotation is a pan; a tilt is up and down.
- C: Up and down rotation is a tilt; a pan is left and right.
- D: Moving the camera body straight up or down is a pedestal (or crane move); a tilt is only a rotation.
- E: Sideways movement of the camera body is a truck, not a pan.

**Source:** Pan, tilt and roll

## MA-jargon.2

A level designer wants the camera to change position, not just direction. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A dolly moves the camera forward or backward along the direction it is facing.
- [ ] B. A dolly turns the camera to the left or right without moving its position.
- [ ] C. A truck is a change of lens focal length that makes the subject look closer.
- [ ] D. A truck moves the camera left or right while it keeps facing the same way.
- [ ] E. A pedestal moves the camera left or right while it keeps facing the same way.

**Key:** A=T B=F C=F D=T E=F

**Why:**

- A: Dolly in and dolly out are movements along the view direction.
- B: Turning on the spot is a pan.
- C: A change of focal length is a zoom, and nothing about it moves the camera body.
- D: Truck left and truck right are sideways movements of the camera body.
- E: Left and right movement of the camera body is a truck; a pedestal is up or down.

**Source:** Dolly, truck and pedestal

## MA-jargon.3

A developer asks for a "zoom" on a boss reveal and gets a different feel than expected. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A zoom changes the field of view or focal length while the camera stays where it is.
- [ ] B. When the camera dollies toward a subject, nearby and distant objects shift against each other (parallax); a zoom does not produce that shift.
- [ ] C. In an engine, changing the camera's field-of-view value is a dolly, not a zoom.
- [ ] D. A zoom in and a dolly in give the same perspective because both make the subject larger on screen.
- [ ] E. Moving the camera node closer to the subject changes its field of view.

**Key:** A=T B=T C=F D=F E=F

**Why:**

- A: A zoom is a lens change, so the camera body does not move.
- B: A dolly changes the camera's position, so objects at different depths move differently on screen; a zoom just magnifies the same view.
- C: Field of view is the lens angle, so editing it is a zoom; a dolly moves the camera body.
- D: The subject grows in both cases, but the relationship between near and far objects differs.
- E: Position and field of view are separate camera properties.

**Source:** Zoom versus dolly

## MA-jargon.4

A game prompt says "make the camera follow the player". Check each statement that is true about the terms involved. Each statement is worth 1 point (5 points total).

- [ ] A. An orbit moves the camera around a subject along a curved path while the subject stays framed.
- [ ] B. Smoothing (damping) on a follow camera makes it jump straight onto the target in a single frame.
- [ ] C. An orbit and a pan are the same move, because both rotate the camera.
- [ ] D. A follow camera and a camera that stays in one place and only turns to face the target are the same thing.
- [ ] E. A follow camera keeps tracking a moving target, usually with some smoothing.

**Key:** A=T B=F C=F D=F E=T

**Why:**

- A: In an orbit the camera body travels around the subject.
- B: Smoothing spreads the catch-up over time, so the camera trails slightly instead of jumping.
- C: A pan turns the camera in place; an orbit changes the camera position.
- D: A camera that only turns toward a target is a look-at (or fixed tracking) camera; a follow camera also changes position.
- E: A follow camera moves with its target; smoothing softens the motion.

**Source:** Orbit and follow camera

## MA-jargon.5

A 2D platformer camera needs tuning words an agent can act on. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Screen shake is a constant sideways offset that leaves the camera shifted after the impact.
- [ ] B. A deadzone is the screen area where the engine skips drawing objects.
- [ ] C. Look-ahead shifts the framing behind the player so more of the ground already crossed is visible.
- [ ] D. A deadzone is a region around the screen centre where the target can move without the camera moving.
- [ ] E. Look-ahead shifts the framing in the direction of travel so the player sees more of what is coming.

**Key:** A=F B=F C=F D=T E=T

**Why:**

- A: Shake is brief and fades back to zero, so the camera returns to its normal framing.
- B: A deadzone concerns camera movement, not drawing.
- C: That would be the opposite of look-ahead.
- D: Inside the deadzone the camera holds still; leaving it makes the camera move.
- E: Look-ahead leads the target in its direction of travel.

**Source:** Deadzone, look-ahead and screen shake

## MA-jargon.6

A designer describes a camera behaviour in plain words and a student must name it. Check each statement in which the name fits the description. Each statement is worth 1 point (5 points total).

- [ ] A. Calling it a pan fits "the camera moves closer to the hero through the crowd".
- [ ] B. Calling it an orbit fits "the camera swings around the hero while the hero stays in the centre of the frame".
- [ ] C. Calling it a dolly fits "the lens narrows so the hero fills the frame while the camera stays still".
- [ ] D. Calling it a truck fits "the camera glides sideways along the street while still facing the same way".
- [ ] E. Calling it a tilt fits "the camera swings up from the hero's boots to her face without changing position".

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: Moving closer is a dolly in.
- B: Travelling around a subject while keeping it framed is an orbit.
- C: A lens change with no camera movement is a zoom.
- D: Sideways camera movement is a truck.
- E: Up or down rotation without moving is a tilt.

**Source:** Pick the precise camera term

## MA-jargon.7

A student types this to a coding agent: "Pan the camera 5 metres closer to the player, then zoom out by moving the camera back." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. "Zoom out by moving the camera back" mixes terms; moving the camera backward is a dolly out.
- [ ] B. The prompt is precise because it states a distance.
- [ ] C. "Pan" is correct because the camera changes position.
- [ ] D. "Pan" is the wrong word for moving 5 metres closer; the move is a dolly in.
- [ ] E. "Zoom out" is correct whenever the camera node's position changes.

**Key:** A=T B=F C=F D=T E=F

**Why:**

- A: A true zoom out widens the lens and leaves the camera where it is.
- B: A distance does not repair wrong move names, so the agent could build the wrong move.
- C: A pan does not change position.
- D: A pan is a rotation; moving along the view direction is a dolly.
- E: Position changes are dollies, trucks or pedestals; a zoom is a lens change.

**Source:** Spot the wrong word in a camera prompt

## MA-jargon.8

A vague prompt reads "make the camera feel more alive when the player gets hit". Check each rewrite that uses the exact camera jargon correctly to ask for a sensible hit effect. Each statement is worth 1 point (5 points total).

- [ ] A. "Add a deadzone around the player when hit so the camera freezes in place."
- [ ] B. "Truck the camera up and down on hit so it looks up at the player."
- [ ] C. "On hit, briefly reduce the field of view by a few degrees (a quick zoom in), then ease it back."
- [ ] D. "Add screen shake on hit: 0.2 seconds, small random offset of the camera position, with the amplitude decaying to zero."
- [ ] E. "Dolly the lens narrower when hit."

**Key:** A=F B=F C=T D=T E=F

**Why:**

- A: A deadzone is a framing region for following; it does not freeze the camera on an event.
- B: Up and down movement is a pedestal, and looking up is a tilt; a truck is sideways.
- C: A field-of-view punch is a valid zoom effect and is described with exact terms.
- D: This names the effect, its duration, what moves and how it fades.
- E: A dolly moves the camera body; a narrower lens is a zoom.

**Source:** Rewrite a vague camera prompt

## MA-jargon.9

An agent is asked to make a follow camera "less jerky". Check each statement that is true about the settings it may adjust. Each statement is worth 1 point (5 points total).

- [ ] A. A wider deadzone makes the camera react to small movements sooner.
- [ ] B. A higher smoothing (damping) speed makes the camera catch up to the target more slowly.
- [ ] C. A larger look-ahead distance shifts the framing farther in the direction of travel.
- [ ] D. A camera that follows a physics body is not affected by whether the camera and the body update on the same tick.
- [ ] E. Turning smoothing on makes the camera snap onto the target instantly.

**Key:** A=F B=F C=T D=F E=F

**Why:**

- A: A wider deadzone makes the camera ignore more small movement.
- B: A higher smoothing speed closes the gap faster.
- C: Look-ahead distance is the size of that forward shift.
- D: Mismatched update rates between the body and the camera are a common cause of visible jitter.
- E: Smoothing spreads the move over time; instant snapping is the absence of smoothing.

**Source:** Follow-camera tuning words

## MA-jargon.10

A student must tell an agent which projection and lens words apply. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Field of view is the distance between the camera and its subject.
- [ ] B. A wider field of view shows more of the scene and exaggerates perspective.
- [ ] C. Camera limits (bounds) keep the camera from showing space outside the level.
- [ ] D. In a perspective camera, objects farther away look smaller.
- [ ] E. In an orthographic camera, an object's size on screen does not depend on its distance.

**Key:** A=F B=T C=T D=T E=T

**Why:**

- A: Field of view is an angle, not a distance.
- B: A wide lens fits more in view and makes depth differences look stronger.
- C: Limits clamp the camera position so the level edge stays off screen.
- D: Perspective projection shrinks distant objects.
- E: Orthographic projection has no foreshortening with distance.

**Source:** Projection, field of view and camera limits

