"""Phase 3: gamedev-evidence.json (source inventory, excerpts, code -> result pairs) and coverage.json.

Adapted from the Assignment 2 film's ledgers.py. Run after media.py and the Remotion renders, so
result-media hashes are final. The inventory is the game folder at the build shown (WALKER_SNAPSHOT,
a git archive of 8d8895c), which is also what `./art godot-gamedev --check --game` reads.

Scope: this film explains what Assignment 3 added. The Assignment 2 2D game inside the same project
is listed as exclusions with that reason (it is explained in the Assignment 2 film); each exclusion
stays visible to a reviewer.
"""
import json
import re
import hashlib

from common import REEL, BUILD, BUILD_FULL, SNAPSHOT, load_json, save_json, sha256, source_lines

TREE = '79ea0965c11386d2b3fac1a8eb39bd20f29f4149'   # git rev-parse 8d8895c:fall-2026/zhefan-z/assignment-3/walker-magic-zhefan
A2_FILM = 'docs/a2/youtube/claude-liam-walker-magic-gamedev/'

COMPONENTS = {
    'a3-blender-assets': ('The three props: the Blender Python Claude Code ran through the MCP (build_*.py, in run order, '
                          'plus the headless export_crystal.py), the saved .blend sources, and the exported .glb files with '
                          'their Godot import settings.', ['B05', 'B06', 'B08', 'B09', 'B10', 'B11', 'B12', 'B13']),
    'a3-prop-room': ('The Godot 3D prop room: floor, one light, a camera, WorldEnvironment, the three props at y = 0 and the '
                     'mage Sprite3D (mage_idle.png, pixel size 0.0226563, Y-billboard; its import kept lossless).',
                     ['B14', 'B15', 'B16']),
    'a3-headless-check': ('test_a3_assets.gd: loads each .glb and the prop room headlessly and compares them with numbers '
                          'copied from CHANGE-BRIEF.md (22 checks, exit 1 on any failure).', ['B17', 'B18']),
}

RULES = [  # (regex on the relative path, component, role)
    (r'^tools/blender/build_(rock|crystal|chest)\.py$', 'a3-blender-assets', 'Blender Python run through the MCP, in run order'),
    (r'^tools/blender/export_crystal\.py$', 'a3-blender-assets', 'headless glTF export of the crystal'),
    (r'^tools/blender/(rock|crystal|chest)\.blend$', 'a3-blender-assets', 'Blender source file'),
    (r'^assets/models/(rock|crystal|chest)\.glb(\.import)?$', 'a3-blender-assets', 'exported .glb or its import settings'),
    (r'^showcase3d/prop_room\.tscn$', 'a3-prop-room', 'the 3D prop room scene'),
    (r'^assets/sprites/mage/mage_idle\.png(\.import)?$', 'a3-prop-room', 'the mage sprite used as the 1.45 m size reference'),
    (r'^tests/test_a3_assets\.gd$', 'a3-headless-check', 'the Assignment 3 headless check'),
]
EXCLUDE = [
    (r'^docs/a2/', 'Assignment 2 submission documents and film records, archived unchanged in b8b7eef (renames only).'),
    (r'^docs/README\.md$', 'Note explaining the archived Assignment 2 documents; not game content.'),
    (r'(^|/)\.gdignore$', 'Empty marker that keeps Godot from importing that folder; no content.'),
    (r'^\.gitignore$', 'Repository configuration, not game content.'),
    (r'.*', 'Assignment 2 2D game (code, scenes, art, audio, tools, tests, design records, project settings), unchanged '
            'in Assignment 3; explained in the Assignment 2 film, ' + A2_FILM + '.'),
]

PAIRS = {
    'B15': ('B16', 'Running with the saved camera and then an orbit: the background is the cave colour, the floor runs to '
                   'the horizon, the props stand at floor height beside the 1.45 m mage, and the mage keeps facing the '
                   'camera as it swings behind; from behind the rock and chest are almost black and the crystal stays blue.'),
    'B17': ('B18', 'The recorded run prints 22 checks / 0 failures; the size lines show measured X × Y × Z equal to the '
                   'brief values copied into the script; headless, so it proves bounds and settings, not looks.'),
}
SOURCE_VIEW_RESULTS = {
    'B05': ('B06', 'Revision 1 look render: the stones overlap as one mass; fit 1.000 (the first build needed X 1.19, Y 1.12).'),
    'B08': ('B09', 'The joined crystal look render after J1: 0.350 × 0.350 × 0.600 m, the hand-rotated cone still leaning.'),
    'B10': ('B11', 'The joined chest look render: the lid with a flat top face; true top 0.600 m (gold shown at metallic 1.0).'),
    'B12': ('B13', 'The recorded .glb read: one node with no transform, height on Y from 0, 60/30/76 triangles, lock at +Z.'),
}


def inventory(root):
    return sorted(p.relative_to(root).as_posix() for p in root.rglob('*')
                  if p.is_file() and not any(x in ('.godot', '.git') for x in p.relative_to(root).parts)
                  and p.suffix != '.uid')


def snapshot_hash(root, rels):
    """Content hash of the source snapshot (coverage.json build_id): sha256 over 'path sha256' lines, LF, sorted."""
    h = hashlib.sha256()
    for rel in rels:
        h.update(f'{rel} {sha256(root / rel)}\n'.encode())
    return h.hexdigest()


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
    views = []
    for bid, b in beats.items():
        if 'source_view' not in b:
            continue
        v = b['source_view']
        result, observation = SOURCE_VIEW_RESULTS[bid]
        media = beats[result]['shot']['evidence_media']
        views.append({'beat_id': bid, **v, 'text': source_lines(root, v['path'], v['start_line'], v['end_line']),
                      'result_beat': result, 'observation': observation,
                      'media': {'path': media, 'sha256': sha256(REEL / media)}})
    data = {'schema_version': 1, 'teaching_contract': 'code-then-result-v1', 'game': 'walker-magic',
            'source_revision': BUILD, 'source_revision_full': BUILD_FULL, 'source_tree': TREE,
            'note': 'B05, B08, B10 and B12 show Blender Python (run inside Blender through the MCP) in a source-view card, '
                    'not in a Godot editor reconstruction; their exact excerpts and result beats are under source_views. '
                    'The snapshot is a git archive written with core.autocrlf=true, so text files there have CRLF line '
                    'endings; hashes are of those bytes.',
            'files': files, 'components': components, 'excerpts': excerpts, 'exclusions': exclusions,
            'code_result_pairs': pairs, 'source_views': views}
    save_json(REEL / 'gamedev-evidence.json', data)
    print(f'gamedev-evidence.json: {len(files)} files, {len(exclusions)} exclusions, {len(excerpts)} excerpts, '
          f'{len(pairs)} pairs, {len(views)} source views')
    return snapshot_hash(root, inventory(root))


def coverage(build_id):
    rows = [json.loads(l) for l in (REEL / 'capture' / 'run-01-camera.jsonl').read_text(encoding='utf-8').splitlines()]
    plan = rows[0]['plan']
    data = {'schema_version': 1,
            'game': {'name': 'walker-magic', 'build_id': build_id, 'revision': BUILD,
                     'build_id_method': 'sha256 over sorted "path sha256" lines of the snapshot (no .godot, no .uid)'},
            'captures': {'run-01': {'path': 'capture/run-01.avi', 'sha256': sha256(REEL / 'capture' / 'run-01.avi'),
                                    'build_id': build_id, 'method': 'scripted-input',
                                    'method_note': 'scripted camera: the harness moves only the Camera node; the prop room '
                                                   'has no gameplay input', 'input_log': 'capture/run-01-camera.jsonl'}},
            'features': [
                {'id': 'prop-room-scene', 'status': 'implemented', 'evidence': [{
                    'capture': 'run-01', 'beat_id': 'B16', 'start_s': 0.0, 'action_s': plan['hold'] / 60,
                    'end_s': (plan['hold'] + plan['orbit'] + plan['tail']) / 60,
                    'observation': 'Saved camera for 2 s, then a 180-degree orbit: props on the floor beside the 1.45 m '
                                   'mage; the mage faces the camera throughout (Y-billboard).',
                    'riff': 'From behind, one light leaves the rock and chest almost black; a flat sprite always shows '
                            'her front.'}]}]}
    save_json(REEL / 'coverage.json', data)
    print('coverage.json written')


if __name__ == '__main__':
    assert SNAPSHOT, 'set WALKER_SNAPSHOT to a git archive of walker-magic-zhefan at 8d8895c'
    coverage(evidence())
