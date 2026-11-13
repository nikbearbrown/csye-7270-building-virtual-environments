"""Phase 3: gamedev-evidence.json (source inventory, excerpts, code -> result pairs).

Adapted from the Assignment 6 film's ledgers.py. Run after footage.py, media.py and the Remotion renders, so
result-media hashes are final. The inventory is the game folder at the build shown (WALKER_SNAPSHOT, a git archive of
f860fed), which is also what `./art godot-gamedev --check --game` reads.

Scope: this film explains what Assignment 7 added (the files changed between 027a0ab, the copy of the Assignment 6
project, and f860fed). Everything else is listed as an exclusion with that reason; each exclusion stays visible.
"""
import re

from common import REEL, BUILD, BUILD_FULL, TREE, SNAPSHOT, load_json, save_json, sha256, source_lines

COMPONENTS = {
    'a7-run-clip': ('Clip 1, the mage run: features/player/player.tscn holds one clip per state (run: a discrete frame '
                    'track over the 4-cell sheet, 0.4 s, LOOP_LINEAR); player.gd only calls play() from _set_state(); the '
                    'r2 sheet and its cleaning tool, the r0 sheet and its packing tool, the rejected far-leg tool, the '
                    'Gemini inputs and outputs with their prompt log, and the run preview scene.',
                    ['B03', 'B09', 'B10', 'B11', 'B12', 'B13', 'B21', 'B22']),
    'a7-lunge-rig': ('Clip 2, the wolf lunge: a cutout rig under Facing (two region_rect parts of the A2 lunge image on hip '
                     'and shoulder pivots) keyed as resource text in features/wolf/wolf.tscn (lunge, 89 ticks, LOOP_NONE); '
                     'wolf.gd plays it on GROWL entry and seeks the recovery section on a growl hit; the afterimage node; '
                     'the lunge preview scene.', ['B04', 'B05', 'B06', 'B07', 'B08', 'B15', 'B25']),
    'a7-motion-reference': ('The Muybridge plates (Animal Locomotion, 1887: plate 707 dog galloping, plate 60 man running), '
                            'public domain, with their provenance; reference only.', ['B06', 'B09']),
    'a7-cave-lights': ('Beyond the requirements: two PointLight2D torches with a looping continuous-track flicker clip, '
                       '144 embers, and their placement in game/main.tscn (with the lighter world darkening).',
                       ['B23', 'B24', 'B25']),
    'a7-pin-and-tests': ('The checks around both clips: the behaviour pin, the edges test, the clip read-backs with the '
                         'shared track_problems() helpers, the structure and afterimage tests, the growl-cancel probe, the '
                         'capture harnesses for the fixture strips, and the figure tool.',
                         ['B08', 'B11', 'B13', 'B14', 'B16', 'B17', 'B18', 'B19', 'B20']),
}

RULES = [  # (regex on the relative path, component, role)
    (r'^features/player/player\.(gd|tscn)$', 'a7-run-clip', 'player script or scene: state clips, _set_state(), _play()'),
    (r'^assets/sprites/mage/mage_run_(cycle_)?sheet\.png(\.import)?$', 'a7-run-clip', 'run sheet (r2 cycle or r0 pair) or its import settings'),
    (r'^tools/(clean_run_cycle\.py|pack_run_sheet\.gd|make_contact_far_legs\.gd)$', 'a7-run-clip', 'tool that wrote a run sheet or a rejected attempt'),
    (r'^design/a7/(?!reference/)', 'a7-run-clip', 'Gemini input reference or raw output for the run'),
    (r'^design/IMAGE-PROMPTS-from-chat\.md$', 'a7-run-clip', 'image prompt log (run prompts v1-v3 added in A7)'),
    (r'^previews/run_preview\.(gd|tscn)$', 'a7-run-clip', 'run preview scene (fixture)'),
    (r'^features/wolf/(wolf\.(gd|tscn)|lunge_afterimage\.gd)$', 'a7-lunge-rig', 'wolf script, scene with the rig and clips, or the afterimage'),
    (r'^previews/lunge_preview\.(gd|tscn)$', 'a7-lunge-rig', 'lunge preview scene (fixture)'),
    (r'^design/a7/reference/', 'a7-motion-reference', 'Muybridge plate or its provenance'),
    (r'^effects/(cave_lights|embers)\.tscn$', 'a7-cave-lights', 'torch lights with the flicker clip, or the embers'),
    (r'^game/main\.tscn$', 'a7-cave-lights', 'main scene: lights, embers and darkening added in A7'),
    (r'^tests/(anim_checks|capture_look|capture_lunge|capture_run_game|probe_growl_cancel|test_afterimage|test_anim_edges|'
     r'test_anim_structure|test_clip_flicker|test_clip_lunge|test_clip_run|test_pin_behaviour)\.gd$', 'a7-pin-and-tests',
     'A7 test, probe, shared check helpers or capture harness'),
    (r'^tools/make_figures\.py$', 'a7-pin-and-tests', 'draws captures/figures/ from the logs'),
]
EXCLUDE = [
    (r'^docs/a6/', 'Assignment 6 film records, moved unchanged from youtube/ into docs/a6/ in Assignment 7 (862984a); '
                   'the template for this film.'),
    (r'^docs/a[235]/', 'Assignment 2, 3 and 5 submission documents and film records, archived unchanged.'),
    (r'^docs/README\.md$', 'Note explaining the archived documents; not game content.'),
    (r'(^|/)\.gdignore$', 'Empty marker that keeps Godot from importing that folder; no content.'),
    (r'^\.git(ignore|attributes)$', 'Repository configuration, not game content.'),
    (r'.*', 'Assignments 2-6 game content (2D game, fireball and its A6 effects, level, audio, HUD, A3 prop room, A5 '
            'shaders and materials, tools, earlier tests, design records, project settings), unchanged in Assignment 7 '
            '(copied at 027a0ab); explained in the earlier films in docs/a2, docs/a3, docs/a5 and docs/a6.'),
]

PAIRS = {
    'B07': ('B08', 'The read-back of the lunge clip (test_clip_lunge 17 / 0: every track resolves, key times equal frames '
                   '/ 60, length 89/60, LOOP_NONE) beside the rig values logged per tick in the game at the keyed frames '
                   '(fixture capture by tests/capture_lunge.gd), overlaid as an onion skin.'),
    'B10': ('B11', 'Scripted input, real engine output: the frame track in play, one crop per physics tick (frames 20-44); '
                   'the sheet cell changes after 6, 6, 6, 7 ticks on entry, then 5, 6, 6, 7 per loop; test_clip_run 16 / 0.'),
    'B12': ('B13', 'Scripted input, real engine output: around the landing, FALL changes to RUN on frame 346 and the run '
                   'clip starts at cell 0, because _set_state() plays the clip from 0 on every state change.'),
    'B15': ('B16', 'The pin timeline for hit_growl before and after the change: from tick 24 GROWL becomes RECOVER, the '
                   'lunge and its armed hitbox disappear; only hit_growl and kill changed in the re-pin.'),
    'B23': ('B24', 'Scripted input, real engine output: the mean brightness of the left torch pool across capture frames '
                   '0-440 follows the flicker clip’s TorchLeft:energy keys (correlation 0.95); test_clip_flicker 11 / 0.'),
}


def inventory(root):
    return sorted(p.relative_to(root).as_posix() for p in root.rglob('*')
                  if p.is_file() and not any(x in ('.godot', '.git') for x in p.relative_to(root).parts)
                  and p.suffix != '.uid')


def evidence():
    root = SNAPSHOT
    sheet = load_json(REEL / 'beat_sheet.json')
    beats = {b['beat_id']: b for b in sheet['beats']}
    files, exclusions = [], []
    members = {c: [] for c in COMPONENTS}
    for rel in inventory(root):
        hit = next(((c, role) for pat, c, role in RULES if re.search(pat, rel)), None)
        if hit:
            c, role = hit
            files.append({'path': rel, 'sha256': sha256(root / rel), 'role': role, 'component_ids': [c]})
            members[c].append(rel)
            continue
        exclusions.append({'path': rel, 'reason': next(why for pat, why in EXCLUDE if re.search(pat, rel))})
    components = [{'id': c, 'explanation': text, 'beat_ids': bids, 'files': members[c]}
                  for c, (text, bids) in COMPONENTS.items()]
    for c in components:
        assert c['files'], f"{c['id']} has no files"
    excerpts, pairs = [], []
    for bid, b in beats.items():
        if 'excerpt' not in b:
            continue
        e = b['excerpt']
        text = source_lines(root, e['path'], e['start_line'], e['end_line'])
        assert text == b['shot']['remotion']['props']['code'], f'{bid}: displayed code differs from source'
        excerpts.append({'beat_id': bid, **e, 'text': text})
        result, observation = PAIRS[bid]
        media = beats[result]['shot']['evidence_media']
        pairs.append({'code_beat': bid, 'result_beat': result, 'observation': observation,
                      'media': {'path': media, 'sha256': sha256(REEL / media)}})
    data = {'schema_version': 1, 'teaching_contract': 'code-then-result-v1', 'game': 'walker-magic',
            'source_revision': BUILD, 'source_revision_full': BUILD_FULL, 'source_tree': TREE,
            'note': 'Result media are cards built from capture/run-01 (scripted input, real engine output, the game at '
                    'f860fed; see CAPTURE.md), from the author’s committed fixture captures and log figures in captures/, '
                    'and from recorded test logs. B18 shows single source lines as a reconstructed source view, outside '
                    'GodotDevWorkbench.',
            'files': files, 'components': components, 'excerpts': excerpts, 'exclusions': exclusions,
            'code_result_pairs': pairs}
    save_json(REEL / 'gamedev-evidence.json', data)
    print(f'gamedev-evidence.json: {len(files)} files, {len(exclusions)} exclusions, {len(excerpts)} excerpts, '
          f'{len(pairs)} pairs')


if __name__ == '__main__':
    assert SNAPSHOT, 'set WALKER_SNAPSHOT to a git archive of walker-magic-zhefan at f860fed'
    evidence()
