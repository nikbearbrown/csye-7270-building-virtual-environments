# Superseded first design of five pictures

**What this is.** The first versions of the shaders for B18, B19, B25, B26 and B27 (and the line order of the crosshair file), with their renders, their Lab rows and their model check, kept because they were run and matched the model, then replaced.
**Why.** An independent review of the layout found two teaching problems that no render can show: B18 and B19 used `abs`, `max` and a cross before the film teaches them, and the arms of B25 to B27 changed names and swapped the roles of x and y between beats. Rather than delete the runs, they are kept here, labelled, so the change is auditable.
**Found.** The first designs were correct (0 of 230,400 pixels differed from the model) and are not used anywhere in the film. Replaced by: a disc with a bite and a spot (08, 09; circles, `step`, subtraction and, in the fix, `max`), and vertical arms built from the same three conditions in the same order as the crosshair (12, 13, 14); the crosshair's `make_arms` now computes the vertical pair first (the same pixels: all 16 crosshair renders re-ran identical).

## What is here

- `shaders/`: the old `08-negative-eats-dot`, `09-negative-fixed` (a plus-shaped cross, a round gap, a round dot: `plus - gap + blob`), `12-arm-rectangle`, `13-arms-gap`, `14-four-arms` (horizontal arms first, `thin` for the width) and the old `17-crosshair` (horizontal pair first).
- `png/`: their 480 by 480 Forward+ renders from the first batch.
- `lab-results-superseded.jsonl`: the Lab rows of the first batch for these five pictures and their Compatibility twins.
- `analysis-masks-superseded.txt`: the first batch's model check (0 pixels differ in every row).
