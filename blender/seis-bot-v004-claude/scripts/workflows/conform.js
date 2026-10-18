export const meta = {
  name: 'seis-bot-conform',
  description: 'Assembly critic compares the assembled SEIS bot with the on-model video frames; eight conformers then fix their modules; args = {round, renders:[abs paths], notes}',
  phases: [{ title: 'Critique', detail: 'one critic, whole-figure comparison against the on-model frames' }, { title: 'Conform', detail: 'one conformer per module, in parallel' }],
}

const W = '/PATH/TO/seis-bot-v004-detailed'
const BLENDER = '/Applications/Blender.app/Contents/MacOS/Blender'
const ROUND = (args && args.round) || 1
const RENDERS = (args && args.renders) || []
const NOTES = (args && args.notes) || ''
const EXTRA = (args && args.extra) || ''

const MODULES = ['head', 'shoulder', 'torso', 'pelvis', 'arm', 'hand', 'leg', 'foot']
const BONES = {
  head: 'head, neck', shoulder: 'pauldron.L/R, chest', torso: 'chest, abdomen', pelvis: 'root',
  arm: 'upperarm.L/R, forearm.L/R', hand: 'hand.L/R, thumb1-3 / index1-3 / middle1-3 / ring1-3 / pinky1-3 .L/R',
  leg: 'thigh.L/R, shin.L/R', foot: 'foot.L/R, toes.L/R',
}

const CRITIC_SCHEMA = {
  type: 'object',
  properties: {
    report_path: { type: 'string' },
    silhouette_verdict: { type: 'string', description: 'in 3-5 sentences: how does the assembled figure compare in overall silhouette, proportions and mass with the on-model frames' },
    per_module: {
      type: 'object',
      properties: Object.fromEntries(MODULES.map(m => [m, { type: 'string', description: 'ranked list of the visible problems for this module, biggest first, each with the evidence (which render, which frame)' }])),
      required: MODULES,
    },
  },
  required: ['report_path', 'silhouette_verdict', 'per_module'],
}

const CONFORM_SCHEMA = {
  type: 'object',
  properties: {
    module: { type: 'string' },
    build_ok: { type: 'boolean' },
    objects: { type: 'number' },
    triangles: { type: 'number' },
    build_seconds: { type: 'number' },
    notes_path: { type: 'string' },
    final_renders: { type: 'array', items: { type: 'string' } },
    changes_made: { type: 'string', description: 'the ONMODEL rows and critic items you applied' },
    remaining_issues: { type: 'string' },
  },
  required: ['module', 'build_ok', 'notes_path', 'final_renders', 'changes_made', 'remaining_issues'],
}

phase('Critique')
const critic = await agent(`
You are the ASSEMBLY CRITIC for the SEIS bot (round ${ROUND}): a 2.12 m near-photoreal robot being modelled in Blender, standing A-pose. Bear's 12 video frames are the TOP authority for what "on model" means: ${W}/refs_onmodel/frame_01..12.jpg (odd frames are sharper copies of 01/02, 03/04 ... shots; frame_08 = front bust, frame_02 = seated wide, frame_06 = pointing hand, frame_04 and frame_12 = head from the side, frame_10 = side view at a desk). The single authority text is ${W}/spec/ONMODEL.md (read it completely first; section 6 is the viewer test). The 118 older stills are in ${W}/refs/ and ${W}/reference-review/contact-*.jpg.
THE ASSEMBLED MODEL, renders from the live Blender: ${RENDERS.join(', ')}. ${NOTES}
Do: (1) read ONMODEL.md; (2) LOOK at every assembled render and at the matching on-model frames (build side-by-sides with python3 ${W}/src/side_by_side.py OUT.jpg model.png frame.jpg --h 900 and Read them; crop the important regions with PIL and enlarge); (3) judge silhouette first (mass, proportions, shoulder size, limb thickness, head size, stance), then each region's structure, colour, finish, and the 10 viewer-test features; (4) write ${W}/spec/CRITIC-round${ROUND}.md: executive summary (the 5 things that most make it look off-model), then one section per module (${MODULES.join(', ')}) with a ranked list of concrete, buildable corrections (what is wrong, what it should be, by how much in metres or ratio, which frame shows it), then a list of cross-module fit problems (gaps, interpenetrations, misaligned joints). Be specific and quantitative; do not pad; do not praise.
You may run Blender headless to render extra views of ${W}/src/assemble.py output if you need to (see the docstring), but the supplied renders are the main evidence. Write only under ${W}/spec/. Return the structured result.`,
  { label: 'critic:round' + ROUND, phase: 'Critique', schema: CRITIC_SCHEMA, effort: 'high' })

phase('Conform')
const common = (m) => `
You are the CONFORMER for module "${m}" on the SEIS bot (round ${ROUND}), a highly detailed, near-photoreal Blender 5.1 model (2.12 m robot). A builder and a refiner already wrote ${W}/parts/${m}.py from the 118 still images. Bear has since supplied 12 video frames that are "the most on-model references" he has and told us to STAY CLOSE TO THEM. Your job: make this module match the on-model frames, without breaking what already works.

READ FIRST, completely: (1) ${W}/spec/ONMODEL.md (the authority: apply EVERY row for your module that is CHANGE / ADD / DELETE with confidence high or medium; for low-confidence rows, apply only if the frames clearly show it); (2) ${W}/spec/CRITIC-round${ROUND}.md, section for "${m}" plus the cross-module list (the whole-figure critic compared the assembled model with the frames); (3) ${W}/spec/BIBLE.md (conventions, bones, quality bar); (4) the current ${W}/parts/${m}.py and its NOTES/REVIEW; (5) ${W}/src/seis_lib.py, seis_mat.py (materials were UPDATED to the on-model clean look: names teal, bronze (clean olive-gold band metal), gold (bright champagne trim), red, silver (pewter), gunmetal, dark, darkdisc, white, eye, eyecore, stone, dais; the "wear" property now means GOLD TRIM STRENGTH: wear=0 means no gold line, default 1), seis_spec.py (DIM values were updated; the joint positions are unchanged), run_part.py.
LOOK at the on-model frames and crops for your region: ${W}/refs_onmodel/ and ${W}/spec/crops/onmodel*/ (and the onmodel_*.md reports they came from). The frames are soft video frames: trust silhouette, colour, counts and arrangement; where a detail is blurry keep the stills detail but match the on-model colour and proportion.

CURRENT ASSEMBLY (so you can see your module in context): ${RENDERS.join(', ')}.
Bones for your objects: ${BONES[m]}. Build left, mirror right unless asymmetric. Interfaces: neighbours are also being conformed now; use seis_spec joint positions and keep your joint plugs so no gaps open.

WORK LOOP: run ${BLENDER} -b --factory-startup --python ${W}/src/run_part.py -- ${m} --views front,three_q,left --clay --context --ghost <the other seven modules, comma separated, that exist in ${W}/parts/> (outputs to ${W}/parts/_out/${m}/), then put your render next to the matching frame crop with side_by_side.py and READ the image. Fix the biggest on-model difference first (silhouette and size, then structure and counts, then colour and finish, then small details). Edit parts/${m}.py incrementally; rebuild after every batch; at least 6 render-compare iterations. Keep build() under 90 s, the BIBLE triangle budget, a material and a bone on every object, no open meshes (run_part prints AUDIT lines), real bevels. Do not edit shared toolkit files (seis_lib, seis_mat, seis_stage, seis_spec, run_part, assemble); helper code goes in your own modules; other conformers are running at the same time on this Mac (700x900 at 24-48 samples while iterating).
When done: append a "Conform round ${ROUND}" section to ${W}/parts/${m}.NOTES.md (which ONMODEL rows and critic items you applied, what you could not do, final render paths, absolute), and return the structured result. Only claim what you verified in a render.
${EXTRA}`

const results = await parallel(MODULES.map(m => () =>
  agent(common(m), { label: 'conform:' + m, phase: 'Conform', schema: CONFORM_SCHEMA, effort: 'high' })))
const ok = results.filter(Boolean)
log(`${ok.length}/${MODULES.length} modules conformed`)
return { critic, results: ok }
