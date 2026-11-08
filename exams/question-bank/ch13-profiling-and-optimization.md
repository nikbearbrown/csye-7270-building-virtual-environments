# Chapter 13: Profiling and optimization

## MA-ch13.1

A team talks about speed using the terms frame time, frame budget, FPS and refresh rate. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A larger frame budget goes with a higher target frame rate.
- [ ] B. FPS and frame time are reciprocals, so losing the same number of FPS costs more milliseconds at a low frame rate than at a high one.
- [ ] C. Frame time is the duration of one frame, measured in milliseconds.
- [ ] D. Refresh rate is the number of frames the GPU renders each second.
- [ ] E. A frame budget is the longest frame time that still meets the target frame rate, about 16.7 ms at 60 Hz.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: A higher target rate leaves less time per frame, so the budget gets smaller.
- B: Because FPS is the reciprocal of frame time, equal FPS drops are not equal millisecond costs.
- C: Frame time is the time one frame takes, usually given in milliseconds.
- D: Refresh rate is how often the display updates, not how often the GPU renders.
- E: The budget is 1000 divided by the target rate, so 60 Hz gives about 16.7 ms.

**Source:** Frame time, frame budget, FPS, refresh rate

## MA-ch13.2

A capture shows most frames finishing quickly but a few frames taking much longer. Check each statement that is true about the terms used to describe it. Each statement is worth 1 point (5 points total).

- [ ] A. Stutter is the name for a high average frame rate.
- [ ] B. A hitch is a single frame that takes much longer than the frames around it.
- [ ] C. A frame-time graph shows a hitch as a spike above the budget line.
- [ ] D. The mean frame time is the best number for exposing hitches, because slow frames dominate it.
- [ ] E. The 99th percentile frame time is the value that 99 percent of frames stay at or below, so it exposes rare slow frames.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: Stutter is uneven frame delivery that the player can see, not a high frame rate.
- B: A hitch is one long frame among shorter ones.
- C: Plotting frame time per frame makes a hitch appear as a spike.
- D: A mean is pulled very little by a few slow frames, so it hides hitches.
- E: A high percentile reports the slow end of the distribution that an average hides.

**Source:** Hitch, stutter, mean versus percentile frame time

## MA-ch13.3

A game takes 22 ms per frame on the target phone. Lowering the render resolution does not change frame time. Check each statement that is true about the terms involved. Each statement is worth 1 point (5 points total).

- [ ] A. An unchanged frame time after lowering resolution suggests the frame is not fill-rate bound.
- [ ] B. GPU-bound means GPU work such as shading sets the length of the frame.
- [ ] C. Lowering resolution reduces pixel work, so it helps a frame that is limited by fill rate.
- [ ] D. CPU-bound means CPU-side work such as game logic, physics or draw-call submission sets the length of the frame.
- [ ] E. Fill rate is the number of draw calls the CPU can submit each second.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: If fewer pixels did not help, pixel shading was not the limit.
- B: A GPU-bound frame waits on rendering work.
- C: Fewer pixels means less fragment work, which helps when fill rate is the limit.
- D: A CPU-bound frame waits on CPU work.
- E: Fill rate is how many pixels the GPU can write per second, not a CPU submission rate.

**Source:** CPU-bound, GPU-bound, fill rate

## MA-ch13.4

A renderer runs the main thread, the render thread and the GPU as a pipeline. Check each statement that is true about bottlenecks. Each statement is worth 1 point (5 points total).

- [ ] A. Game script logic runs on the render thread.
- [ ] B. Speeding up a stage that is not the bottleneck leaves the frame time unchanged.
- [ ] C. The bottleneck is the stage with the longest time per frame, and it sets the pace.
- [ ] D. In a pipeline, frame time is the sum of the times of the stages.
- [ ] E. After a bottleneck is removed, another stage can become the new bottleneck.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: Game logic runs on the main thread; the render thread prepares and submits drawing work.
- B: Only improving the bottleneck shortens the frame.
- C: The slowest stage limits throughput.
- D: Pipeline stages overlap in time, so the slowest one sets frame time rather than the sum.
- E: Once the slowest stage speeds up, the next slowest becomes the limit.

**Source:** Bottleneck, main thread, render thread, pipeline

## MA-ch13.5

A scene has 1,000 small props, each with its own draw call, and it is slow on the CPU. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. Draw call and triangle are two names for the same measurement.
- [ ] B. Triangle count and draw-call count are separate costs that can be tuned apart.
- [ ] C. A draw call is a command from the CPU asking the GPU to draw geometry with a given mesh, material and state.
- [ ] D. Draw-call cost is mostly GPU shading work.
- [ ] E. A frame with many small draw calls can be CPU-bound even when the triangle count is low.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: A draw call is a command; a triangle is a piece of geometry.
- B: A scene can have few triangles and many calls, or the reverse.
- C: A draw call submits a batch of geometry plus the state to draw it.
- D: Each call costs CPU submission and validation time, not mainly shading.
- E: Per-call overhead can dominate with many small objects.

**Source:** Draw call versus triangle count

## MA-ch13.6

A developer is choosing between batching, instancing and a texture atlas to cut draw calls. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Instancing draws many copies of one mesh and one material in a single call, with per-instance data such as transform.
- [ ] B. Batching merges geometry that shares a material into fewer draw calls.
- [ ] C. A texture atlas packs many images into one texture, so objects that show different images can share a material.
- [ ] D. Instancing draws many copies of different meshes with different materials in one call.
- [ ] E. Giving each object its own unique material makes batching easier.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: Per-instance data such as transform is supplied alongside the shared mesh.
- B: Shared material is the condition for merging into fewer calls.
- C: An atlas lets different pictures live in one texture and one material.
- D: Instances share one mesh and one material.
- E: Unique materials split the groups and defeat batching.

**Source:** Batching, instancing, texture atlas

## MA-ch13.7

A developer tells a coding agent: "The grass is slow. Use instancing." The grass is 50,000 blades, each a separate scene node with its own mesh and material. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Instancing needs one shared blade mesh, one shared material and a per-instance list of transforms.
- [ ] B. If the grass is slow because of overdraw, fewer draw calls will fix it.
- [ ] C. Instancing reduces the number of triangles the GPU processes for the grass.
- [ ] D. The saving from instancing comes from fewer pixels being shaded.
- [ ] E. The word instancing in the prompt also asks the agent to add level of detail and culling.

**Key:** A=T B=F C=F D=F E=F

**Why:**

- A: Instancing needs a shared mesh and material plus per-copy data.
- B: Overdraw is shading cost on the GPU, which draw-call count does not touch.
- C: Each copy still has its triangles processed; only submission overhead falls.
- D: Instancing cuts draw calls, not shaded pixels.
- E: Level of detail and culling are separate terms and would have to be requested.

**Source:** Instancing in an agent prompt

## MA-ch13.8

A scene is slow because eight full-screen semi-transparent smoke layers are shaded for each pixel. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Overdraw is a cost on the CPU.
- [ ] B. A fragment is a candidate pixel produced by rasterization that the fragment shader processes.
- [ ] C. Merging the overlapping planes into one mesh removes the overdraw.
- [ ] D. Fill rate is how many pixels the GPU can write per second, and stacked transparent layers strain it.
- [ ] E. Overdraw is the same screen pixel being shaded more than once in a frame.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: Overdraw is shading work on the GPU.
- B: Each fragment is a potential pixel that gets shaded.
- C: A merged mesh still covers the same pixels the same number of times.
- D: Fill rate limits pixel output, and each layer adds more of it.
- E: Eight layers over one pixel give an overdraw factor of eight.

**Source:** Fragment, overdraw, fill rate

## MA-ch13.9

A 3D game draws a city, and the developer wants fewer objects submitted. Check each statement that is true about culling terms. Each statement is worth 1 point (5 points total).

- [ ] A. Frustum culling removes a building hidden behind a wall when the building is inside the view volume.
- [ ] B. Occlusion culling skips objects that are inside the view volume but hidden behind other geometry.
- [ ] C. A culled object is not submitted, which saves the draw calls and shading work it would have caused.
- [ ] D. Frustum culling skips objects that lie outside the camera's view volume.
- [ ] E. Backface culling discards individual triangles that face away from the camera.

**Key:** A=F B=T C=T D=T E=T

**Why:**

- A: Being inside the frustum is not the same as being visible, which is the gap occlusion culling fills.
- B: Occlusion culling tests visibility against other geometry.
- C: Culling decides what not to draw, so the culled cost disappears.
- D: The frustum is the volume the camera can see.
- E: Backface culling works on triangles, not whole objects.

**Source:** Frustum, occlusion and backface culling

## MA-ch13.10

A character has three meshes: a detailed one for close-ups, a medium one and a simple one for the distance. Check each statement that is true about level of detail (LOD). Each statement is worth 1 point (5 points total).

- [ ] A. LOD replaces the need for culling, since distant objects cost nothing to draw.
- [ ] B. LOD swaps in a simpler version as the object gets farther away or smaller on screen.
- [ ] C. Cross-fading or tuning the switch distances can reduce popping.
- [ ] D. Popping is the visible jump when the engine switches from one LOD version to another.
- [ ] E. Keeping three LOD versions uses less memory than keeping the detailed mesh alone.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: Cheap objects still cost something, so culling is a separate tool.
- B: LOD chooses a representation by distance or screen size.
- C: Blending or better thresholds hides the swap.
- D: Popping is the visible swap between versions.
- E: Extra versions are extra mesh data held in memory.

**Source:** Level of detail, popping

## MA-ch13.11

A developer tells a coding agent: "Pool the bullets." Each shot currently creates a new bullet and destroys it on impact. Check each statement that is true about object pooling. Each statement is worth 1 point (5 points total).

- [ ] A. Acquire takes an object from the pool and release returns it.
- [ ] B. Pooling creates objects in advance and reuses them instead of creating and destroying them.
- [ ] C. Pool exhaustion is the situation where no free object is left when one is requested, and the code needs a policy for it.
- [ ] D. Idle pooled objects are free, taking up no memory.
- [ ] E. A reused pooled object needs no reset, because it was cleaned when it was created.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: Acquire and release are the two basic pool operations.
- B: A pool trades creation and destruction for reuse.
- C: Exhaustion needs a policy such as growing, skipping the shot or recycling the oldest.
- D: Pooled objects still occupy memory while they wait.
- E: A reused object keeps its old state, so it needs a reset such as position, velocity and timers.

**Source:** Object pooling, acquire, release, exhaustion

## MA-ch13.12

A game written in a language with a tracing garbage collector allocates a small temporary list each frame, and players see short freezes. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. Garbage is allocated memory that is no longer referenced and waits to be reclaimed by the collector.
- [ ] B. Pooling reduces allocation, which means less garbage for the collector.
- [ ] C. Lowering the refresh rate removes the freezes by giving the collector more time.
- [ ] D. Garbage collection manages GPU memory, so a faster GPU shortens the pauses.
- [ ] E. A collection pause is time the collector takes out of a frame, which shows as a hitch.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: Garbage is unreachable memory awaiting reclamation.
- B: Reusing objects avoids creating short-lived garbage.
- C: Refresh rate does not change allocation, which is the cause.
- D: The collector manages CPU-side memory.
- E: The collector's work lands inside a frame as a spike.

**Source:** Garbage, garbage collection, allocation

## MA-ch13.13

A team wants to cut texture memory on a phone. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. The size of a PNG file on disk is the same as the texture's footprint in VRAM.
- [ ] B. A mipmap chain is a series of smaller copies of a texture used when the texture appears small on screen.
- [ ] C. GPU texture compression is the same thing as saving the image as a smaller PNG.
- [ ] D. VRAM is the memory of the GPU, where textures are held for sampling.
- [ ] E. Texture streaming loads textures or mip levels into memory as they are needed.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: VRAM size follows resolution and format, not the file.
- B: Mip levels are pre-shrunk copies for distant or small use.
- C: GPU compression formats stay compressed in memory; PNG is decoded before use.
- D: VRAM is video memory.
- E: Streaming brings in data on demand.

**Source:** VRAM, mipmap, texture compression, streaming

## MA-ch13.14

A developer compares two builds of a system with several timed runs each. Check each statement that is true about benchmarking terms. Each statement is worth 1 point (5 points total).

- [ ] A. A warm-up period is the start of a run that is discarded because shader compilation and cache filling are not steady-state cost.
- [ ] B. One run is enough to show a real difference between two versions.
- [ ] C. Variance is how much results differ from run to run for the same code.
- [ ] D. A difference smaller than the run-to-run spread is within noise.
- [ ] E. The median is the middle value of the sorted samples.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: Start-up work is not representative, so it is dropped before measuring.
- B: A single run cannot separate a real effect from noise.
- C: Variance measures run-to-run spread.
- D: A gap smaller than the normal spread does not show a real change.
- E: Median is the middle of the sorted values.

**Source:** Warm-up, variance, median, noise

## MA-ch13.15

A developer reports: "A steady 60 FPS, so plenty of headroom." The display runs at 60 Hz with vertical sync on, in the editor, on a fast development PC. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A development PC counts as the target hardware if it is faster than the phone.
- [ ] B. Vertical sync caps the frame rate at the refresh rate, which can hide spare time in the frame.
- [ ] C. Vertical sync makes the game's work run faster.
- [ ] D. An editor session or debug build adds overhead that a release build does not have.
- [ ] E. Headroom is the part of the frame budget that is already used.

**Key:** A=F B=T C=F D=T E=F

**Why:**

- A: Target hardware is the device the game ships to.
- B: A frame that finishes early waits for the next refresh, so FPS stays at 60.
- C: Vertical sync waits on the display and does not speed the work.
- D: Tool overhead and extra checks change timings.
- E: Headroom is the unused part of the budget.

**Source:** Vertical sync, build type, target hardware, headroom

## MA-ch13.16

A developer tells a coding agent: "Make the game faster." Check each statement that is a precise rewrite fragment using correct performance terms. Each statement is worth 1 point (5 points total).

- [ ] A. "Optimize the parts of the code that look slow."
- [ ] B. "Boost FPS as much as you can."
- [ ] C. "Profile first to find whether the frame is CPU-bound or GPU-bound, then change one thing and re-measure."
- [ ] D. "Bring frame time to the 16.7 ms budget at 60 Hz on the target phone, measured in a release build."
- [ ] E. "Report the 99th percentile frame time as well as the mean, after discarding a warm-up period."

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: Looks slow is a guess, not a profiled hot spot.
- B: It names no target, device or measurement.
- C: Naming the bottleneck type and one change at a time is exact use of the terms.
- D: It gives a measurable frame-time budget, target device and build type.
- E: It names a percentile and a warm-up period.

**Source:** Rewriting a vague performance prompt

## MA-ch13.17

A scene has 5,000 small separate objects, each with its own draw call, and the frame is CPU-bound. Check each statement that is a sensible instruction to the coding agent. Each statement is worth 1 point (5 points total).

- [ ] A. "Use instancing for the 5,000 props, each with its own mesh and material."
- [ ] B. "Batch the props that share a material to reduce draw calls."
- [ ] C. "Use GPU texture compression to lower the draw-call count."
- [ ] D. "Add LOD meshes to lower the draw-call count."
- [ ] E. "Pack the prop images into a texture atlas so the props can share one material."

**Key:** A=F B=T C=F D=F E=T

**Why:**

- A: Instancing needs one shared mesh and material.
- B: Batching merges geometry that shares a material.
- C: Compression lowers memory, not calls.
- D: LOD cuts triangles at a distance and does not reduce calls.
- E: An atlas makes different images share a material, enabling batching.

**Source:** Choosing batching, instancing or atlas

## MA-ch13.18

A team discusses premature optimization and hot spots. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A profiler reports the fix as well as the slow part.
- [ ] B. A detailed profiling run adds overhead, so its absolute times are inflated.
- [ ] C. A hot spot is a function or frame stage that takes a large share of the frame time.
- [ ] D. Premature optimization is optimizing before measurement shows a need.
- [ ] E. Headroom is the amount by which the frame exceeds its budget.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: A profiler shows data; choosing the change is the developer's work.
- B: Instrumentation slows the program.
- C: Hot spots are where time concentrates.
- D: Optimizing without evidence may miss the real bottleneck.
- E: Headroom is spare budget; exceeding the budget is a miss.

**Source:** Premature optimization, hot spot, profiler overhead

## MA-ch13.19

A developer is learning to use a profiler. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A profiler records where time or memory goes during a run.
- [ ] B. A profiler reports CPU time and GPU time as the same number.
- [ ] C. A capture of one frame at a busy moment is enough for a game whose load changes during play.
- [ ] D. A hot spot is the function that uses the least time.
- [ ] E. A capture should span a representative stretch of play.

**Key:** A=T B=F C=F D=F E=T

**Why:**

- A: Recording time and memory by function or stage is the purpose of a profiler.
- B: CPU and GPU timings are separate readings.
- C: One frame can be unrepresentative.
- D: A hot spot is a large cost, not the smallest.
- E: A representative capture avoids mistaking an outlier for the norm.

**Source:** Profiler, capture

## MA-ch13.20

A game runs out of GPU memory. Check each statement that is true about the options. Each statement is worth 1 point (5 points total).

- [ ] A. Removing the mipmap chain reduces draw calls.
- [ ] B. A texture atlas is a lower-resolution copy used for distant objects.
- [ ] C. Lowering texture resolution reduces memory but loses detail.
- [ ] D. GPU texture compression reduces bytes per pixel at some risk of visible artifacts.
- [ ] E. Texture streaming keeps the full set of textures resident in memory at the same time.

**Key:** A=F B=F C=T D=T E=F

**Why:**

- A: Mipmaps affect memory and sampling, not draw calls.
- B: That describes a mip level; an atlas packs several images into one texture.
- C: Fewer pixels means less memory and less detail.
- D: Compressed formats store fewer bytes per pixel and can add artifacts.
- E: Streaming loads data on demand rather than keeping everything resident.

**Source:** Texture memory options

## MA-ch13.21

A shooter pools its bullets. Check each statement that is true about sizing and operating the pool. Each statement is worth 1 point (5 points total).

- [ ] A. Pool size is set from peak simultaneous demand plus a margin.
- [ ] B. An inactive pooled bullet stays visible and colliding so it is ready to use.
- [ ] C. Pool size is set from the average number of bullets alive, with no margin.
- [ ] D. Releasing an object back to the pool twice is harmless.
- [ ] E. Pooling helps little when objects are few and long-lived.

**Key:** A=T B=F C=F D=F E=T

**Why:**

- A: Peak demand sets the needed count, with margin for spikes.
- B: Inactive objects are hidden with processing and collision disabled.
- C: Average demand would run out at peaks.
- D: A double release can put the same object in the pool twice and cause bugs.
- E: Pooling saves creation cost, which is small for few long-lived objects.

**Source:** Pool sizing and operations

## MA-ch13.22

Classify fixes by the bottleneck they address. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Reducing overdraw is a fix for a GPU-bound frame.
- [ ] B. GPU texture compression is a fix for a CPU-bound frame.
- [ ] C. Simplifying a pixel shader is a fix for a GPU-bound frame.
- [ ] D. Batching is a fix for CPU-side draw-call submission cost.
- [ ] E. Updating AI less often is a fix for CPU-side work.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: Overdraw is GPU pixel work.
- B: Compression saves memory, not CPU time.
- C: A cheaper shader reduces GPU work per pixel.
- D: Fewer calls means less CPU submission time.
- E: Less frequent AI updates cut CPU logic cost.

**Source:** CPU-side versus GPU-side fixes

## MA-ch13.23

A developer says: "I ran it once and version B was faster, so we are switching." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Reporting FPS alone is enough, because an average shows hitches.
- [ ] B. Repeated runs let the developer report the spread.
- [ ] C. Comparing a release build of A with a debug build of B is a fair test.
- [ ] D. Run-to-run noise comes from things such as other processes and thermal effects.
- [ ] E. Frames from the warm-up period are representative of steady-state cost.

**Key:** A=F B=T C=F D=T E=F

**Why:**

- A: Averages hide hitches; percentiles reveal them.
- B: Repetition shows variance.
- C: Build type changes timing, so conditions must match.
- D: Noise sources vary between runs.
- E: Warm-up frames include start-up work and are discarded.

**Source:** Benchmark critique

## MA-ch13.24

A game targets 60 Hz and takes 12 ms per frame. A teammate wants a complex rewrite to save an estimated 0.2 ms. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The game is over budget.
- [ ] B. A game that is within budget is GPU-bound by definition.
- [ ] C. The estimated saving should be confirmed by measurement before counting.
- [ ] D. The headroom is the unused part of the 16.7 ms budget, about 4.7 ms.
- [ ] E. The rewrite targets a confirmed hot spot.

**Key:** A=F B=F C=T D=T E=F

**Why:**

- A: 12 ms is under 16.7 ms.
- B: Being within budget says nothing about CPU or GPU limits.
- C: An estimate is not a measurement.
- D: Headroom is budget minus frame time.
- E: A hot spot needs profile evidence.

**Source:** Headroom, hot spot, premature optimization
