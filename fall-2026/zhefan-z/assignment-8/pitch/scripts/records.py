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
    seg0 = {s: next(r['f'] for r in rows if r['seg'] == s) for s in ('run', 'lunges', 'cancel', 'lunge_hit')}
    # 2026-11-22 tightened spans: G04 shows run frames 140-360, G05 lunges 870-1030 and cancel 1520-1590
    run_on = first(rows, lambda r: r.get('ps') == 'RUN' and rows[r['f'] - 1].get('ps') != 'RUN', 140)
    idle = first(rows, lambda r: r.get('ps') == 'IDLE', run_on)
    rise = first(rows, lambda r: r.get('ps') == 'RISE', seg0['run'])
    land = first(rows, lambda r: r.get('ps') == 'RUN', rise)
    growl1 = first(rows, lambda r: r.get('ws') == 'GROWL', seg0['lunges'])
    lunge1 = first(rows, lambda r: r.get('ws') == 'LUNGE', growl1)
    growl2 = first(rows, lambda r: r.get('ws') == 'GROWL' and r.get('wface') == 1, seg0['lunges'])
    hurt = first(rows, lambda r: r.get('ps') == 'HURT', seg0['lunges'])
    growl_c = first(rows, lambda r: r.get('ws') == 'GROWL', seg0['cancel'])
    cast = next(r['frame'] for r in ins if r['kind'] == 'cast_fired' and r['segment'] == 'cancel')
    hit = next(r for r in ins if r['kind'] == 'wolf_hit' and r['segment'] == 'cancel')
    hit2 = next(r for r in ins if r['kind'] == 'wolf_hit' and r['segment'] == 'lunge_hit')
    rec2 = first(rows, lambda r: r.get('ws') == 'RECOVER', hit2['frame'])
    patrol = first(rows, lambda r: r.get('ws') == 'PATROL', hit['frame'])
    assert hit['prev_state'] == 'GROWL' and hit['state'] == 'RECOVER'
    assert hit2['prev_state'] == 'LUNGE' and hit2['state'] == 'LUNGE'
    assert all(not r.get('mon') for r in rows if r['seg'] == 'cancel'), 'the cancel segment armed the hitbox'
    assert 140 <= run_on < rise and land + 10 <= 360 and 1515 <= cast <= 1555 and 870 <= growl1 and hurt + 20 <= 1030
    assert 1520 <= growl_c and patrol <= 1590
    frows, fins = frame_rows('run-02'), input_rows('run-02')
    failed = next(r for r in fins if r['kind'] == 'failed')
    fall = first(frows, lambda r: r.get('ps') == 'FALL')
    assert 250 <= fall < failed['frame'] <= 385 and failed['reason']
    feats = [
        ('run_cycle', 'run-01', 'G04', 140, run_on, rise, f'D held again: the mage starts the four-frame run (frame {run_on}).',
         'Move: A/D or the arrows (GDD 4).'),
        ('jump', 'run-01', 'G04', rise - 20, rise, land + 10, f'Space at the pit edge: RISE on frame {rise}, lands in '
         f'RUN on {land}.', 'Jump: Space, W or Up; coyote time and buffer are source facts (tuning.gd), not shown.'),
        ('aimed_fireball', 'run-01', 'G04', 1515, cast, hit['frame'], f'A click on the wolf casts a fireball (frame '
         f'{cast}) that flies to the aim point.', 'Aim and cast with the mouse (GDD 4).'),
        ('pit_fail', 'run-02', 'G04', 250, failed['frame'], 385, f"No jump: the mage falls (frame {fall}) and fails on "
         f"frame {failed['frame']}; the HUD shows the reason: {failed['reason']}.", 'Lose and restart (GDD 4); the '
         'reload is skipped under the capture harness (test_mode) and stated, not shown.'),
        ('wolf_growl_telegraph', 'run-01', 'G05', 870, growl1, lunge1, f'The wolf enters GROWL on frame {growl1} when '
         f'the mage comes into sight, and lunges on {lunge1}.', 'The phase table in play (GDD 5).'),
        ('wolf_lunge_hurts_mage', 'run-01', 'G05', growl2, hurt, hurt + 20, f'The wolf growls facing right (frame '
         f'{growl2}), lunges and the mage is hurt on frame {hurt}.', 'A hit costs a heart (GDD 5).'),
        ('hurt_tint', 'run-01', 'G05', hurt - 5, hurt, hurt + 20, 'The mage tints red and blinks while she cannot be '
         'hit again.', 'Health: tint, blink, invulnerability (GDD 5).'),
        ('growl_cancel', 'run-01', 'G05', growl_c, hit['frame'], patrol, f"The hit lands on frame {hit['frame']} with "
         f"the wolf in GROWL; it goes to RECOVER with no lunge; HP {hit['hp_before']} -> {hit['hp_after']}.",
         'A hit during the growl cancels the lunge (GDD 5).'),
        ('fireball_particles', 'run-01', 'G05', cast, hit['frame'], hit['frame'] + 20, 'The trail behind the fireball '
         'and the impact burst on the wolf.', 'Particles exist today; question 7 shows the Assignment 6 capture.'),
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
        'captures': {c: {'path': f'capture/{c}.mp4', 'sha256': sha256(REEL / 'capture' / f'{c}.mp4'),
                         'build_id': BUILD_ID, 'method': 'scripted-input', 'input_log': f'capture/{c}-inputs.jsonl'}
                     for c in ('run-01', 'run-02')},
        'features': [{'id': i, 'status': 'implemented',
                      'evidence': [{'capture': c, 'beat_id': b, 'start_s': t(s), 'action_s': t(a), 'end_s': t(e),
                                    'observation': o, 'riff': r}]} for i, c, b, s, a, e, o, r in feats]
                    + [{'id': i, 'status': 'planned', 'reason': why, 'evidence': []} for i, why in planned],
        'not_shown_implemented': 'The level reload after a fail (skipped under test_mode), a fail at 0 HP, a hit during the lunge (the dash commits; captured in run-01 frames 2040-2148, not in the tightened film), the exit '
                                 'and clear, Esc pause, M/N mutes and R restart exist at 840b501 and are not shown: '
                                 'this pitch is not a complete walkthrough, and no beat claims one.',
    }
    save_json(REEL / 'coverage.json', cov)

    sheet = load_json(REEL / 'beat_sheet.json')
    # SHOTLIST.md was committed for the first cut; committed docs only get dated additions, so the first cut's table
    # is kept as written and this run's table is (re)written under the dated heading below.
    mark = '## Tightened to under four minutes — 2026-11-22'
    old = (REEL / 'SHOTLIST.md').read_text(encoding='utf-8') if (REEL / 'SHOTLIST.md').exists() else ''
    keep = old.split(mark)[0].rstrip() + '\n\n' if old else ''
    t0, lines = 0.0, [mark, '',
                      'The rebuilt film cut to under four minutes (prompt-3-tighten.txt); the tables above (first cut, '
                      'rebuild) are kept as committed. Generated by `scripts/records.py` from `beat_sheet.json` (durations as measured and '
                      'padded).', '',
                      '| Beat | Part | Start s | Length s | Heading | Picture | Label on screen | Media |', '|---|---|---:|---:|---|---|---|---|']
    pic = {'capture': 'real captured play', 'still': 'still card', 'audio': "the game's own audio, with its picture"}
    lab = {'real': 'Real (revision shown)', 'constructed': 'Constructed', 'figure': 'Figure from the logs · 840b501'}
    mixed = {'P01': 'Real frame 1544 (840b501) + Generated portrait + Constructed card',
             'G09': 'Real game sprites (840b501) + Generated portraits',
             'G10': 'Left: real (840b501 sprites, figure, prop render, frame) + one Generated portrait; right: '
                    'Constructed - proposed, not built',
             'A05': "Constructed card of PROJECT-BRIEF.md's asset table"}
    for b in sheet['beats']:
        d = b['actual_duration_s']
        m = f"media/{b['beat_id']}.{'png' if b['visual_kind'] == 'still' else 'mp4'}"
        lines.append(f"| {b['beat_id']} | {b['part']} | {t0:.2f} | {d:.2f} | {b['heading']} | {pic[b['visual_kind']]} | "
                     f"{mixed.get(b['beat_id'], lab.get(b['label']))} | {m} |")
        t0 += d
    lines += ['', f'Total: {t0:.2f} s.', '']
    (REEL / 'SHOTLIST.md').write_text(keep + '\n'.join(lines), encoding='utf-8')
    print('coverage.json:', len(feats), 'implemented,', len(planned), 'planned; SHOTLIST total', round(t0, 2))


if __name__ == '__main__':
    main()
