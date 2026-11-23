"""Phase 3: coverage.json (the godot-waikthrough evidence contract) and SHOTLIST.md, from the logs and the sheet.

Written by Claude Code for the Assignment 8 pitch film. Every frame number below is looked up in
capture/run-01-frames.jsonl or capture/run-01-inputs.jsonl (the 840b501 capture), never typed in. Capture times are
seconds of capture/run-01.mp4 (60 fps, frame f at f/60 s). Only the 840b501 capture is in coverage.json: the
checker requires every capture to be the same build. The Assignment 5 and 6 footage (B13, B14) is earlier-revision
evidence, recorded in CAPTURE.md and evidence/footage-provenance.json instead.
"""
from common import REEL, REV_A7, load_json, save_json, sha256, frame_rows, input_rows

BUILD_ID = '964c57fecefd0aaf2c4a2394765552baaf71a0a47d9ba6e26671b8f88956aba6'
# = sha256 of `git ls-tree -r 840b501:fall-2026/zhefan-z/assignment-7/walker-magic-zhefan` (CAPTURE.md)


def first(rows, pred, start=0):
    return next(r['f'] for r in rows[start:] if pred(r))


def main():
    rows = frame_rows('run-01')
    ins = input_rows('run-01')
    t = lambda f: round(f / 60.0, 3)
    seg0 = {s: next(r['f'] for r in rows if r['seg'] == s) for s in ('run', 'lunges', 'cancel')}
    # the RUN entry inside B15's span (frames 140-439): the run restarting after the stop
    run_on = first(rows, lambda r: r.get('ps') == 'RUN' and rows[r['f'] - 1].get('ps') != 'RUN', 140)
    assert 140 < run_on < 301, run_on
    rise = first(rows, lambda r: r.get('ps') == 'RISE', seg0['run'])
    land = first(rows, lambda r: r.get('ps') == 'RUN', rise)
    growl2 = first(rows, lambda r: r.get('ws') == 'GROWL' and r.get('wface') == 1, seg0['lunges'])
    hurt = first(rows, lambda r: r.get('ps') == 'HURT', seg0['lunges'])
    growl_c = first(rows, lambda r: r.get('ws') == 'GROWL', seg0['cancel'])
    cast = next(r['frame'] for r in ins if r['kind'] == 'cast_fired' and r['segment'] == 'cancel')
    hit = next(r for r in ins if r['kind'] == 'wolf_hit' and r['segment'] == 'cancel')
    patrol = first(rows, lambda r: r.get('ws') == 'PATROL', hit['frame'])
    assert hit['prev_state'] == 'GROWL' and hit['state'] == 'RECOVER'
    assert all(not r.get('mon') for r in rows if r['seg'] == 'cancel'), 'the cancel segment armed the hitbox'
    feats = [
        ('run_cycle', 'B15', 140, run_on, rise, f'The mage starts the four-frame run again on D (frame {run_on}).',
         'Narration names the run cycle as Assignment 7 work shown at 840b501.'),
        ('jump', 'B15', rise - 20, rise, land + 20, f'Space at the pit edge: RISE on frame {rise}, lands in RUN on {land}.',
         'Shown as part of the run beat; the jump itself is not narrated.'),
        ('aimed_fireball', 'B00', growl_c, cast, hit['frame'], f'A click on the wolf casts a fireball (frame {cast}) '
         'that flies to the aim point.', 'The hook: an aimed cast, early.'),
        ('wolf_growl_telegraph', 'B00', growl_c - 30, growl_c, hit['frame'], f'The wolf enters GROWL on frame '
         f'{growl_c} when the mage comes into sight.', 'The growl warns of the lunge.'),
        ('growl_cancel', 'B00', growl_c, hit['frame'], patrol, f"The hit lands on frame {hit['frame']} with the wolf "
         f"in GROWL; it goes to RECOVER with no lunge; HP {hit['hp_before']} -> {hit['hp_after']}.",
         'An early hit cancels the lunge: the hook and B08.'),
        ('wolf_lunge_hurts_mage', 'B08', growl2, hurt, hurt + 40, f'The wolf growls facing right (frame {growl2}), '
         f'lunges and the mage is hurt on frame {hurt}.', 'The lunge that the cancel prevents.'),
        ('fireball_particles', 'B00', cast, hit['frame'], hit['frame'] + 20, 'The trail behind the fireball and the '
         'impact burst on the wolf.', 'Particles exist today; narrated in B14 from the Assignment 6 capture.'),
        ('hurt_tint', 'B08', hurt - 5, hurt, hurt + 40, 'The mage tints red while she cannot be hit again.',
         'Hurt tint exists today; narrated in B13 from the Assignment 5 capture.'),
    ]
    planned = [
        ('3d_cave_level', 'PROJECT-BRIEF "Will exist": the 3D cave level and its camera; not built.'),
        ('hd2d_look', 'PROJECT-BRIEF "The look (planned)": depth of field, bloom, fog, moving light; not built.'),
        ('story_moments_in_game', 'Four portrait scenes; the portraits exist only as concept art in pitch/art/.'),
        ('heal_spell', 'PROJECT-BRIEF section 5 "In"; not built.'),
        ('great_wolf_boss', 'PROJECT-BRIEF section 5 "In"; not built.'),
        ('spikes_and_boulder', 'PROJECT-BRIEF section 5 "In"; not built.'),
        ('chest_and_campfire_rest_point', 'The chest model exists (Assignment 3, own scene); the rest point is not built.'),
        ('title_and_end_screens', 'PROJECT-BRIEF "Will exist"; not built.'),
        ('windows_export', 'PROJECT-BRIEF section 1; not built.'),
    ]
    cov = {
        'schema_version': 1,
        'game': {'name': 'walker-magic-zhefan (the existing 2D game The Little Flame Witch grows from)',
                 'build_id': BUILD_ID, 'revision': REV_A7},
        'captures': {'run-01': {'path': 'capture/run-01.mp4', 'sha256': sha256(REEL / 'capture' / 'run-01.mp4'),
                                'build_id': BUILD_ID, 'method': 'scripted-input',
                                'input_log': 'capture/run-01-inputs.jsonl'}},
        'features': [{'id': i, 'status': 'implemented',
                      'evidence': [{'capture': 'run-01', 'beat_id': b, 'start_s': t(s), 'action_s': t(a), 'end_s': t(e),
                                    'observation': o, 'riff': r}]} for i, b, s, a, e, o, r in feats]
                    + [{'id': i, 'status': 'planned', 'reason': why, 'evidence': []} for i, why in planned],
        'not_shown_implemented': 'The pit fail and retry, the exit, Esc pause and the A3 prop scene exist at 840b501 '
                                 'and are not in this pitch: it is not a complete walkthrough, and no beat claims one.',
    }
    save_json(REEL / 'coverage.json', cov)

    sheet = load_json(REEL / 'beat_sheet.json')
    t0, lines = 0.0, ['# SHOTLIST — The Little Flame Witch (pitch)', '',
                      'Generated by `scripts/records.py` from `beat_sheet.json` (durations as measured and padded).', '',
                      '| Beat | Start s | Length s | Heading | Picture | Label on screen | Media |', '|---|---:|---:|---|---|---|---|']
    pic = {'capture': 'real captured play', 'still': 'still card'}
    lab = {'real': 'Real capture · scripted input · revision shown', 'constructed': 'Constructed (generated portraits '
           'labelled where used)', 'figure': 'Figure from the logs · Assignment 7 · 840b501',
           'mixed': 'Exists: in git at the revision shown / Will exist: proposed, not built'}
    for b in sheet['beats']:
        d = b['actual_duration_s']
        m = f"media/{b['beat_id']}.{'mp4' if b['visual_kind'] == 'capture' else 'png'}"
        lines.append(f"| {b['beat_id']} | {t0:.2f} | {d:.2f} | {b['heading']} | {pic[b['visual_kind']]} | "
                     f"{lab[b['label']]} | {m} |")
        t0 += d
    lines += ['', f'Total: {t0:.2f} s.', '']
    (REEL / 'SHOTLIST.md').write_text('\n'.join(lines), encoding='utf-8')
    print('coverage.json:', len(feats), 'implemented,', len(planned), 'planned; SHOTLIST total', round(t0, 2))


if __name__ == '__main__':
    main()
