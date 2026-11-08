# Chapter 12: Audio and triggers

## MA-ch12.1

A Godot game has background music, a menu click and the footsteps of an enemy walking around a 3D world. The developer chooses between a plain AudioStreamPlayer and a positional AudioStreamPlayer3D for each. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Attenuation is the drop in loudness as the distance between a positional source and the listener grows.
- [ ] B. The menu click suits a positional player, so that it pans and fades like the rest of the 3D world.
- [ ] C. For a positional player, the listener is the point whose position and orientation define what is heard, and in Godot 3D it defaults to the active camera.
- [ ] D. The listener is the object that emits a positional sound, so each positional sound needs its own listener at its source.
- [ ] E. A plain AudioStreamPlayer is non-positional, so its loudness does not depend on where the camera is.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: Attenuation, also called falloff, is the distance-dependent loss of level.
- B: A menu click has no place in the world, and a positional player would change its level and pan with the camera.
- C: A positional sound is heard relative to a listener, which Godot takes from the current camera unless told otherwise.
- D: The listener is the receiver (the ears), and one is active at a time.
- E: A non-positional player ignores listener position, which suits music and interface sounds.

**Source:** Positional audio, listener, attenuation

## MA-ch12.2

A developer tells a coding agent: 'Play a click when the button is pressed.' Check each statement that is true about what the wording leaves out. Each statement is worth 1 point (5 points total).

- [ ] A. A signal is connected to a handler that calls play() on a stream player holding a stream.
- [ ] B. The instruction already fixes the bus, the loudness and the behaviour on rapid presses.
- [ ] C. The player's playing flag reading true after play() shows that the click reached the output and is audible.
- [ ] D. A muted bus on the route to Master silences the click even though the player reports that it is playing.
- [ ] E. A sound can be audible and still be routed to a different bus than intended.

**Key:** A=T B=F C=F D=T E=T

**Why:**

- A: Game logic wires an event to a handler that starts a player.
- B: The sentence names an event and a sound; bus, level and overlap behaviour are left to guesswork.
- C: The flag shows a voice was started and says nothing about routing, level or mute.
- D: Mute and level apply along the bus chain.
- E: A misrouted sound can still be heard, so audibility does not verify routing.

**Source:** Wiring an event to a sound: signal, handler, bus

## MA-ch12.3

A stream player is set to -6 dB and routed to an SFX bus whose fader is -6 dB, and that bus sends to Master at 0 dB. Check each statement that is true about the decibel vocabulary. Each statement is worth 1 point (5 points total).

- [ ] A. dBFS states a level relative to digital full scale, where 0 dBFS is the loudest value a digital signal can hold.
- [ ] B. A linear slider value from 0.0 to 1.0 passed straight to a bus as dB behaves like a linear volume knob.
- [ ] C. Gain staging means one -6 dB stage is enough to reach the level of the whole chain, so the later stages are ignored.
- [ ] D. Decibels are a logarithmic scale, so gains in series add and the two -6 dB stages give about -12 dB.
- [ ] E. A change of about -6 dB roughly halves the amplitude.

**Key:** A=T B=F C=F D=T E=T

**Why:**

- A: dBFS counts down from digital full scale.
- B: Decibels are logarithmic, so a linear slider needs converting to dB.
- C: Gain staging is the set of level changes along the chain, and each stage contributes.
- D: Decibel gains in series add.
- E: A factor of 10^(-6/20) is about 0.5.

**Source:** Decibel, gain, dBFS

## MA-ch12.4

A game has Music, SFX and Voice buses that each send to Master, with a settings slider per bus. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A reverb on the SFX bus also processes the Music bus.
- [ ] B. Separate buses let the player change the music level without changing the effects level.
- [ ] C. Master is the final bus, so muting it silences the sounds routed to it directly or through child buses.
- [ ] D. Muting Master silences just the sounds played straight onto Master.
- [ ] E. Muting the SFX bus also silences the Music bus, because both feed Master.

**Key:** A=F B=T C=T D=F E=F

**Why:**

- A: A bus effect processes the sounds routed through that bus.
- B: Each bus is an independent control point for level, mute and effects.
- C: Master ends the chain.
- D: Child buses feed Master, so muting it silences them too.
- E: Buses with a shared parent do not affect each other.

**Source:** Bus, master bus, bus effect

## MA-ch12.5

A designer says: 'When a character speaks, the music should get quieter, then come back up when the speech ends.' The developer passes it to an agent as 'pause the music during dialogue'. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Calling stop() on the music and later play() resumes from where it stopped.
- [ ] B. Ducking needs the music and the voice to share one stream player.
- [ ] C. Ducking is the automatic, temporary lowering of one group of sounds while another is active.
- [ ] D. A paused track and a ducked track sound the same to the player.
- [ ] E. Ducking can be driven by a side-chain, where an effect on the music bus reacts to the level of the voice.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: Stop discards position, so play() restarts from the beginning.
- B: Music and voice normally sit on separate players and buses.
- C: Ducking lowers and then restores the level on its own.
- D: A paused track is silent and frozen; a ducked track plays on quietly.
- E: Side-chain compression makes one bus's level follow another's signal.

**Source:** Ducking, side-chain

## MA-ch12.6

A designer wants a chime when the player walks into a glowing zone, while the player keeps walking through the zone. A developer asks for 'a zone collider that plays a chime'. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Collision layers or filtering keep enemies and projectiles from playing the chime.
- [ ] B. Placing a chime player inside the zone makes the audio system detect the overlap and play it with no code.
- [ ] C. A trigger (Area in Godot, trigger collider in Unity, overlap volume in Unreal) reports overlap as an event and does not block.
- [ ] D. A solid collider is the right choice, because it reports contact and lets the player pass.
- [ ] E. The chime should start from the enter event, which marks the start of the overlap.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: Layers and masks decide which objects count.
- B: Game logic detects the overlap and calls the player.
- C: A trigger observes and raises events.
- D: A solid collider blocks; passing through is what a trigger does.
- E: The enter event fires at the start of the overlap, the moment for the chime.

**Source:** Trigger versus collider

## MA-ch12.7

A pressure plate click is wired to a callback that runs on each physics step while an overlap persists (Unity's OnTriggerStay). At 50 steps per second, players hear a buzzing, machine-gun click while they stand on the plate. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A trigger has no event for the start of an overlap.
- [ ] B. A stay callback fires on each physics step during the overlap, restarting the click about once per 20 ms.
- [ ] C. Raising polyphony removes the cause of the buzzing.
- [ ] D. Starting the click from the enter event plays it once at the start of the overlap, and an exit event marks leaving.
- [ ] E. A longer click file fixes the buzzing, because a longer sound is restarted less often.

**Key:** A=F B=T C=F D=T E=F

**Why:**

- A: Triggers report enter, stay and exit.
- B: 50 steps per second gives a callback every 20 ms.
- C: More voices let the retriggers overlap and make it noisier.
- D: Enter and exit mark the transitions of an overlap.
- E: The callback still fires on each step.

**Source:** Enter, stay and exit events

## MA-ch12.8

A developer asks an agent: 'Make the engine hum loop while the car drives, and make the horn honk once per press.' The project is Godot. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A one-shot is a sound that is triggered once per session and then disabled.
- [ ] B. A hum recorded with a fade-out at the end makes a good loop, since the fade hides the join.
- [ ] C. Restarting with play() from the finished handler is as seamless as the stream's built-in loop.
- [ ] D. A seamless loop ends at the same level and phase at which it begins.
- [ ] E. In Godot, whether a sound loops is set on the stream resource.

**Key:** A=F B=F C=F D=T E=T

**Why:**

- A: A one-shot plays through once per trigger and can be triggered again.
- B: A fade-out dips the volume at each pass, so the loop pulses.
- C: Restarting after finished can leave a gap.
- D: The loop point should match in level and phase.
- E: Loop settings live on the stream, while the player plays what it is given.

**Source:** One-shot, loop, loop point

## MA-ch12.9

A stream player cuts off its oldest voice when play() is called beyond its maximum polyphony. A 60 ms click is triggered at 0 ms, 40 ms and 80 ms on the same player. Check each statement that is true about the vocabulary. Each statement is worth 1 point (5 points total).

- [ ] A. With a polyphony of 2, the three clicks need three voices at one instant.
- [ ] B. Polyphony is the number of voices a player can sound at once.
- [ ] C. With a polyphony of 1, the click at 40 ms cuts off the click that started at 0 ms.
- [ ] D. A voice is one playing instance of a sound.
- [ ] E. Polyphony is the length of a sound.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: At most two clicks overlap at an instant, so two voices suffice.
- B: Polyphony counts simultaneous voices.
- C: A single voice is replaced by the newest trigger.
- D: A voice is one instance in progress.
- E: Length is duration, not polyphony.

**Source:** Polyphony and voice

## MA-ch12.10

A rhythm game judges a tap within 50 ms of a beat. One version sums frame delta into a song-time variable; another reads the music player's playback position. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Calling play() in the same frame as the tap makes the hit sound start exactly on the beat.
- [ ] B. The reported playback position includes device latency and is exact to the sample.
- [ ] C. Judging taps against the audio clock, corrected for latency, tracks what the player hears.
- [ ] D. Summed frame delta can drift away from the audio actually playing, since frame time and audio run on different clocks.
- [ ] E. Audio is mixed in blocks, so the reported position advances in coarse steps.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: Playback starts at the next mix boundary, then output latency adds delay.
- B: The position ignores output latency and updates by block.
- C: The audio clock is the reference the music follows.
- D: Game loop and audio hardware are separate clocks.
- E: Mixing happens in chunks.

**Source:** Audio clock, mixing block, output latency

## MA-ch12.11

An inverse-distance falloff lowers a sound by about 6 dB for each doubling of distance from the listener. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. Reverb is a kind of attenuation.
- [ ] B. The listener is the sound source whose level is being reduced.
- [ ] C. Attenuation raises a sound's level as the source moves away.
- [ ] D. An inverse law reaches zero at a finite distance, so no maximum distance setting is needed.
- [ ] E. Attenuation and falloff are two words for the loss of level with distance.

**Key:** A=F B=F C=F D=F E=T

**Why:**

- A: Reverb adds reflections; attenuation lowers level.
- B: The listener is the receiver.
- C: Attenuation lowers the level.
- D: An inverse law keeps getting smaller without reaching zero, so engines add a maximum distance.
- E: Both describe distance-dependent level loss.

**Source:** Attenuation, falloff, maximum distance

## MA-ch12.12

A game plays an explosion when an enemy dies. The agent made the stream player a child of the enemy, called play() and freed the enemy. Players hear nothing or a clipped pop. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Checking 'health <= 0' on each frame is the same as a death signal, since both start the sound when the enemy dies.
- [ ] B. Raising the volume fixes the problem.
- [ ] C. Freeing a node frees its children, including the stream player.
- [ ] D. Playing from a node that outlives the enemy avoids the cut-off.
- [ ] E. A died signal emitted once, with an audio handler responding, separates the enemy's lifetime from the sound's.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: Polling is true on each frame the condition holds and restarts the sound repeatedly.
- B: The sound is being destroyed, not quiet.
- C: Children live and die with their parent.
- D: The player needs an owner that survives the sound.
- E: A signal fires once and decouples emitter and listener.

**Source:** Signal versus polling; node lifetime

## MA-ch12.13

Audio designers want to change footstep sounds without code edits. Gameplay code asks for a cue named 'footstep_stone', and the audio data decides which recordings play. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A cue is a bus that other sounds are routed through.
- [ ] B. Unreal's Sound Cue is a node graph that combines and modifies sounds and is played by reference.
- [ ] C. The same gameplay event can request different cues, such as stone or grass, so the cue name carries the situation.
- [ ] D. A cue can choose among recordings and vary pitch or volume slightly.
- [ ] E. A cue is a named request for a sound event, and its mapping to recordings can change without gameplay code changes.

**Key:** A=F B=T C=T D=T E=T

**Why:**

- A: A bus is a routing channel; a cue is a named sound event.
- B: Sound Cue fits the cue idea.
- C: Choosing the cue name from state gives varied sounds.
- D: Variation reduces repetition.
- E: A cue separates what happened from which files play.

**Source:** Cue

## MA-ch12.14

In Godot, a pause menu pauses the scene tree. A developer asks an agent: 'The menu click should still sound while paused, the music should resume where it left off, and restart should reload the level.' Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A sound that survives a reload is attached to the scene being reloaded.
- [ ] B. A menu-click player plays normally while the tree is paused without a change to its process mode.
- [ ] C. stop() then play() resumes from where it stopped.
- [ ] D. After a scene reload, music players from the old scene keep playing from their position.
- [ ] E. A stream player in its default process mode pauses with the tree and resumes after.

**Key:** A=F B=F C=F D=F E=T

**Why:**

- A: Surviving a reload means living outside the scene, such as in an autoload.
- B: A paused player needs a process mode that keeps it running.
- C: Stop discards position; pausing the stream keeps it.
- D: Reloading frees the old players and creates new ones.
- E: Audio nodes follow the tree's pause.

**Source:** Process mode, autoload, pause versus stop

## MA-ch12.15

A cave region adds reverb to the SFX bus from the cave trigger's enter event and removes it on the exit event. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The reverb also colours the Music bus.
- [ ] B. Enter and exit events are paired, and a missed exit can leave the reverb on.
- [ ] C. Reverb on a bus is the same as positional attenuation.
- [ ] D. The reverb applies to sound effects routed through the SFX bus, including ones from far outside the cave.
- [ ] E. The cave trigger blocks the player, or its exit event will not fire.

**Key:** A=F B=T C=F D=T E=F

**Why:**

- A: Only sounds routed through SFX are processed.
- B: A toggle driven by two events is correct only if both arrive.
- C: Reverb adds reflections; attenuation lowers level with distance.
- D: A bus effect is not positional.
- E: A trigger reports enter and exit without blocking.

**Source:** Bus effect versus attenuation; enter and exit

## MA-ch12.16

A developer moves between engines and gives an agent the engine's term for each audio idea. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. In Unity, an AudioClip is the imported sound and an AudioSource is the component that plays it.
- [ ] B. Unity's AudioListener acts like a microphone, and a scene works with one.
- [ ] C. Unity's Audio Mixer groups play the role that buses play in Godot.
- [ ] D. Unreal's Play Sound at Location does not follow an actor, so a moving enemy needs an attached audio component.
- [ ] E. Unreal's Play Sound 2D applies distance attenuation, so it suits sounds that belong in the world.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: Unity separates the asset from the playing component.
- B: The listener is the receiver.
- C: Mixer groups route, set level and add effects like buses.
- D: An attached component travels with the actor.
- E: Play Sound 2D plays without attenuation, for interface sounds.

**Source:** Engine audio vocabulary

## MA-ch12.17

A developer rewrites 'Add a click sound when the button is pressed' as a precise instruction. Check each statement that is true about wording that fits. Each statement is worth 1 point (5 points total).

- [ ] A. 'Play a short non-looping stream on a non-positional player' names the sound type and player.
- [ ] B. 'The playing flag is true' proves the click is audible.
- [ ] C. 'Set the level in dB relative to the music and say what happens on rapid presses' fills gaps in the original.
- [ ] D. 'Connect the pressed signal to a handler that calls play()' names the trigger.
- [ ] E. 'Route it to the SFX bus, which sends to Master' names the bus.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: A one-shot on a non-positional player suits an interface sound.
- B: The flag does not show routing or audibility.
- C: Level and overlap behaviour are left open by the original.
- D: Signal, handler and play() describe the wiring.
- E: The bus decides level, mute and effects.

**Source:** Rewriting an audio prompt with exact terms

## MA-ch12.18

A coin should chime and vanish when touched while the player passes through, and a closed door should thud and stop the player. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The coin is a trigger and its chime starts from the enter event.
- [ ] B. Game logic receives the event and calls the audio player.
- [ ] C. A stay callback restarts the sound on each physics step while the player stands in the zone.
- [ ] D. The chime player should be a child of the coin.
- [ ] E. The door should be a trigger, so the player passes through while the thud plays.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: A trigger reports overlap without blocking.
- B: Audio does not decide when to play.
- C: Stay fires continuously, so the retrigger buzzes.
- D: Freeing the coin would cut the chime off.
- E: A door that stops the player is a solid collider, with the thud on a contact event.

**Source:** Trigger, collider, contact event

## MA-ch12.19

A game has music, effects and voice buses. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A bus is a channel with its own level, mute and effects whose output goes to a parent bus.
- [ ] B. On a single bus, music and effects are hard to balance independently.
- [ ] C. The master bus is the bus for music.
- [ ] D. A linear slider value is converted to dB before being applied.
- [ ] E. Ducking lowers the music level for good.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: Buses are mixing and routing channels.
- B: Separate control needs separate buses.
- C: Master receives the whole mix.
- D: Decibels are logarithmic.
- E: Ducking is temporary and restores itself.

**Source:** Bus layout, slider conversion, ducking

## MA-ch12.20

A developer tells an agent: 'Make the robot's footsteps 3D.' Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Music and the menu click suit positional players too.
- [ ] B. The positional player should be attached to the robot so it moves with it.
- [ ] C. The listener stands in for the player's ears and is typically the active camera.
- [ ] D. Attenuation lowers the level with distance, optionally to a maximum distance.
- [ ] E. The listener should be attached to the robot.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: They have no place in the world.
- B: A positional source follows its node.
- C: Level and pan are computed relative to the listener.
- D: Distance sets loudness, and a maximum distance cuts the sound off.
- E: The listener belongs to the player's view.

**Source:** Making a sound positional

## MA-ch12.21

A rhythm game compares taps with the music. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Frame time and audio hardware run on the same clock.
- [ ] B. A test with no sound device proves the sound lines up with the beat as heard.
- [ ] C. A sound begins the instant play() is called.
- [ ] D. Output latency is the delay between a sample being mixed and being heard.
- [ ] E. Latency should be compensated or made adjustable.

**Key:** A=F B=F C=F D=T E=T

**Why:**

- A: They are separate clocks.
- B: Lining up as heard needs a person with speakers.
- C: Playback begins at the next mix boundary.
- D: That delay is output latency.
- E: Judgment should match what the player hears.

**Source:** Output latency, mix boundary

## MA-ch12.22

A test asserts that a stream player's playing property is true right after the hit event and prints PASS. A reviewer says it proves little. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Measuring the signal on the bus is stronger than reading a flag.
- [ ] B. A negative case, where a miss stays silent, strengthens the test.
- [ ] C. The flag shows that the event reached the handler and play() was called.
- [ ] D. Audibility and balance against the music are judged by a person on real hardware.
- [ ] E. The flag shows which bus the sound reached.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: A measurement shows signal and level.
- B: A miss that stays silent shows the trigger discriminates.
- C: The trigger path is wired.
- D: Audibility needs a listener.
- E: The flag says nothing about routing.

**Source:** Verifying triggering and routing

## MA-ch12.23

A shooter needs a rapid gunshot (10 per second, 0.5 s tail), a rain ambience for the whole level and a horn that honks while a key is held. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A polyphony limit needs no rule about which voice to drop.
- [ ] B. The gunshot is a looping sound because it repeats ten times a second.
- [ ] C. The horn can be a loop that starts on key down and stops on key up.
- [ ] D. A single-voice player cuts off the oldest sound when triggered again, chopping gunshot tails.
- [ ] E. The rain is a looping ambience whose loop points are seamless.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: When the voices are full, a policy such as dropping the oldest or quietest is chosen.
- B: Each gunshot is a one-shot; repetition comes from triggers.
- C: A held honk fits a loop gated by the key.
- D: Retriggering a single voice cuts the tail.
- E: A seam click or gap is audible if the loop points do not match.

**Source:** One-shot, loop, polyphony choices
