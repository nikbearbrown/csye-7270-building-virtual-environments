"""Phase 3: gamedev-evidence.json (source inventory, excerpts, code -> result pairs) and coverage.json.

Run after media.py and the Remotion renders, so result-media hashes are final.
The inventory is the game folder at the build shown (WALKER_SNAPSHOT, a git
archive of 74c0443), which is also what `./art godot-gamedev --check --game` reads.
"""
import re
from pathlib import Path

from common import REEL, BUILD, SNAPSHOT, load_json, save_json, sha256, source_lines

TREE_74C0443 = 'c931ac0508576f8970a5e59180835966bd391ad9'   # git rev-parse 74c0443:<game folder>
TREE_5266946 = '93c13d4d5481d7e63e231964415748a58521b6e2'

COMPONENTS = {
    'design-documents': ('The concept, character sheet, storyboard and change brief: the promises the slice is checked '
                         'against (pillars, 64 px size, palette, 14x44 collision, predicted failures).', ['B04', 'B05', 'B12']),
    'character-art-pipeline': ('Gemini outputs (accepted and rejected), the cleanup tool and its config, the cleaned mage '
                               'sprites and the edit log with hashes; palette revision 1 lives here.',
                               ['B06', 'B07', 'B08', 'B09', 'B12', 'B13']),
    'player': ('CharacterBody2D with one texture per state, movement, jump, cast and damage.', ['B10', 'B11', 'B14']),
    'fireball': ('The projectile and its burst, spawned by the cast at the staff tip.', ['B14', 'B15']),
    'wolf': ('Patrol, 0.5 s growl telegraph, lunge, hit flash, down image and removal.', ['B15']),
    'level-and-environment': ('Ground segments, the pit kill zone, the code-drawn exit and the cave art.', ['B11', 'B13']),
    'audio': ('The AudioDirector that only listens to game signals, the buses, the five effects and the music loop, '
              'with their generation and edit records.', ['B16', 'B17', 'B20']),
    'game-flow-and-ui': ('Main scene, input map, session input (pause, M/N mutes), HUD and crosshair.', ['B19', 'B20']),
    'tests': ('Headless suites; test_sound_triggers.gd is the assignment check shown with its recorded output.', ['B21', 'B22']),
    'project-records': ('Sources, models, licenses and test report: the honest accounting.', ['B23', 'B24']),
}

RULES = [  # (regex on the relative path, component, role)
    (r'^(CONCEPT|CHARACTER-SHEET|STORYBOARD|CHANGE-BRIEF)\.md$', 'design-documents', 'design document'),
    (r'^design/storyboard/', 'design-documents', 'storyboard panel'),
    (r'^design/character/(collision|silhouette|pixel-preview-idle-v3|pose-sketches-v1)\.', 'design-documents', 'character-sheet check image'),
    (r'^design/character/(generated|poses)/', 'character-art-pipeline', 'Gemini output or pose reference (accepted, or rejected thumbnail)'),
    (r'^design/checks/', 'character-art-pipeline', 'before/after contact sheet'),
    (r'^tools/(clean_sprites\.py|sprites\.json|sheet_images\.py)$', 'character-art-pipeline', 'sprite cleanup tool / config'),
    (r'^assets/sprites/(mage/|EDIT-LOG\.md|edit-log\.json)', 'character-art-pipeline', 'cleaned sprite, import settings or edit log'),
    (r'^features/player/', 'player', 'player script / scene / tuning'),
    (r'^features/fireball/', 'fireball', 'fireball and burst'),
    (r'^assets/sprites/fx/', 'fireball', 'fireball/burst sprite or import settings'),
    (r'^features/wolf/', 'wolf', 'wolf script / scene / flash shader'),
    (r'^assets/sprites/wolf/', 'wolf', 'wolf sprite or import settings'),
    (r'^features/(level|exit)/', 'level-and-environment', 'level geometry, pit, code-drawn exit'),
    (r'^assets/sprites/env/', 'level-and-environment', 'cave background / ground tile or import settings'),
    (r'^design/environment/', 'level-and-environment', 'environment Gemini output or rejected thumbnail'),
    (r'^(audio/|default_bus_layout\.tres$)', 'audio', 'audio director / placeholder tones / bus layout'),
    (r'^assets/audio/', 'audio', 'effect or music file, import settings or audio edit log'),
    (r'^design/audio/', 'audio', 'sound-effect generation log'),
    (r'^tools/(gen_sfx\.py|sfx_prompts\.json|trim_sfx\.py|make_music_loop\.py)$', 'audio', 'audio generation / edit tool'),
    (r'^(game/|ui/|project\.godot$)', 'game-flow-and-ui', 'main scene, input, session, HUD, crosshair or project settings'),
    (r'^tests/', 'tests', 'headless test suite'),
    (r'^(SOURCES|TEST-REPORT)\.md$', 'project-records', 'sources/licenses or test report'),
]
EXCLUDE = {
    r'^tools/__pycache__/': 'Python bytecode cache that was committed at 74c0443; generated, not authored, not shown.',
    r'^FRICTIONAL\.md$': 'Course process log (who struggled with what); not part of the game or the film’s claims.',
    r'^TODO\.md$': 'Open to-do list; its film items are what this film closes.',
    r'^\.gitignore$': 'Repository configuration, not game content.',
    r'(^|/)\.gdignore$': 'Empty marker that keeps Godot from importing design/ and tools/; no content.',
}

PAIRS = {
    'B10': ('B11', 'The texture swaps with the state in motion: idle, run, rise over the pit, fall, land, then the hurt '
                   'image after the wolf’s hit.'),
    'B14': ('B15', 'Clicks fire one fireball each from the staff tip toward the wolf; two casts, two hits, then the '
                   'down image and the wolf disappears.'),
    'B16': ('B17', 'Each labelled game event in the takes (hurt, two casts, wolf down, fail, clear) is the moment its '
                   'signal fires; the footage is silent here, the sound follows in B18.'),
    'B19': ('B20', 'M brings up “music off (M)”, N “sfx off (N)” and a cast makes no sound; in the slot after, N and M '
                   'restore the effects and the music, heard in the take’s own audio.'),
    'B21': ('B22', 'The recorded run prints 11 checks / 0 failures with per-sound counts equal to the game events; '
                   'headless, so it proves triggers, not audibility.'),
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
        ex = next((why for pat, why in EXCLUDE.items() if re.search(pat, rel)), None)
        if ex:
            exclusions.append({'path': rel, 'reason': ex})
            continue
        hit = next(((c, role) for pat, c, role in RULES if re.search(pat, rel)), None)
        assert hit, f'unassigned file: {rel}'
        c, role = hit
        files.append({'path': rel, 'sha256': sha256(root / rel), 'role': role, 'component_ids': [c]})
        members[c].append(rel)
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
    data = {'schema_version': 1, 'teaching_contract': 'code-then-result-v1', 'game': 'walker-magic',
            'source_revision': BUILD, 'source_tree': TREE_74C0443,
            'note': 'B08 and B12 show the Python cleanup tool in a source-view card, not in a Godot editor '
                    'reconstruction; their exact excerpts are recorded under source_views and checked by media.py.',
            'files': files, 'components': components, 'excerpts': excerpts, 'exclusions': exclusions,
            'code_result_pairs': pairs,
            'source_views': [{'beat_id': bid, **b['source_view'],
                              'text': source_lines(root, b['source_view']['path'], b['source_view']['start_line'],
                                                   b['source_view']['end_line'])}
                             for bid, b in beats.items() if 'source_view' in b]}
    save_json(REEL / 'gamedev-evidence.json', data)
    print(f'gamedev-evidence.json: {len(files)} files, {len(exclusions)} exclusions, {len(excerpts)} excerpts, '
          f'{len(pairs)} pairs')


def coverage():
    prov = load_json(REEL / 'evidence' / 'media-provenance.json')
    ev = prov['take_events_s']['run-01']
    caps = {}
    for take in ('run-01', 'run-02', 'run-03', 'run-04'):
        caps[take] = {'path': f'capture/{take}.avi', 'sha256': sha256(REEL / 'capture' / f'{take}.avi'),
                      'build_id': TREE_5266946, 'runtime_identical_to': f'{BUILD} (tree {TREE_74C0443})',
                      'method': 'scripted-input', 'input_log': f'capture/{take}-inputs.jsonl',
                      'gate': 'PASS against a headless reference (CAPTURE.md)'}
    r = lambda x: round(x, 3)
    feats = [
        ('player-idle-run-rise-fall-land', 'B11', 'run-01', 0.0, ev['jump'], 9.267,
         'Idle, run, rise over the pit, fall and land, each its own texture.'),
        ('player-hurt', 'B15', 'run-01', 4.0, ev['hurt'], 13.5, 'One lunge hit: hearts 5 → 4, hurt image and blink.'),
        ('wolf-growl-telegraph', 'B15', 'run-01', 4.0, ev['growl'], 13.5,
         'The wolf stops in its open-mouthed pose for 0.5 s before the lunge (time derived from the driver log, ±1 tick).'),
        ('cast-fireball', 'B15', 'run-01', 4.0, ev['cast1'], 13.5, 'Two clicks, two fireballs from the staff tip.'),
        ('wolf-defeat', 'B15', 'run-01', 4.0, ev['down'], 13.5, 'Second hit: white flash, down image, then removed after 0.6 s.'),
        ('sfx-events-and-music', 'B18', 'run-01', 7.4, ev['hurt'], 15.6,
         'Heard with no narration: hurt, cast, wolf down, clear; the music stops at the exit.'),
        ('pit-fail-music-stop', 'B18', 'run-02', 3.6, prov['take_events_s']['run-02']['fail'], 6.2,
         'Heard with no narration: the fall, SFX-FAIL, the music stopped.'),
        ('mute-music-and-sfx', 'B20', 'run-03', 0.0, 0.7, 7.8, 'M and N labels, a silent cast, then the effects and music restored.'),
    ]
    data = {'schema_version': 1, 'game': {'name': 'walker-magic', 'build_id': TREE_74C0443, 'revision': BUILD},
            'captures': caps,
            'features': [{'id': fid, 'status': 'implemented', 'evidence': [
                {'capture': take, 'beat_id': bid, 'start_s': r(a), 'action_s': r(act), 'end_s': r(b), 'observation': obs}]}
                for fid, bid, take, a, act, b, obs in feats],
            'not_in_film': [
                {'capture': 'run-02', 'what': 'attempt 2 after the reload (music back from the top, 5 hearts)',
                 'why': 'recorded and gated, but the approved beats end run-02 at the fail'},
                {'capture': 'run-04', 'what': 'Esc pause and resume',
                 'why': 'recorded and gated; the approved beat sheet has no pause beat'}]}
    save_json(REEL / 'coverage.json', data)
    print('coverage.json written')


if __name__ == '__main__':
    assert SNAPSHOT, 'set WALKER_SNAPSHOT to a git archive of the game folder at 74c0443'
    evidence()
    coverage()
