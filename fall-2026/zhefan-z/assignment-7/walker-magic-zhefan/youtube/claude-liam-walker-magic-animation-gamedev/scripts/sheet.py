"""Phase 1: write beat_sheet.json from SCRIPT.md.

Adapted from the Assignment 6 film's sheet.py. Narration is taken verbatim from SCRIPT.md (the Your Turn beat
already ends with Liam's sign-off). Measured narration already in the sheet is kept when the text is unchanged,
so re-running this never silently invalidates generated audio.
"""
from common import REEL, SLUG, TITLE, BUILD, load_json, save_json, script_narration

COMPOSER = {'topic': 'CSYE 7270 · reconstructed prompt, not a saved chat', 'greeting': 'Jambo, Liam',
            'runningText': '', 'folderLabel': 'walker-magic', 'modelLabel': 'Claude Code',
            'effortLabel': '', 'placeholder': ''}

WB = {'pattern': 'GodotDevWorkbench'}
# id, heading, visual kind, extra
BEATS = [
    ('B00', 'Walker opening', 'remotion', {'pattern': 'ClaudeComposerAsk', 'props': {
        **COMPOSER,
        'command': 'Please use Walker to convert my game design document\nabout a fire mage and a cave wolf into two animation\n'
                   'clips: a run cycle that loops and a lunge that commits —\neach pinned first, keyed as data in the scene files,\n'
                   'read back by tests and checked tick by tick\nagainst the game.',
        'output': ['features/player/player.tscn · run: 4 cells, 10 fps, LOOP_LINEAR, discrete',
                   'features/wolf/wolf.tscn · lunge: cutout rig, 89 ticks, LOOP_NONE',
                   'test_pin_behaviour.gd · 8 scenarios, 16 checks / 0 failures at 30, 60 and 144 fps',
                   'test_anim_edges.gd · 13 checks / 0 failures at 30, 60 and 144 fps'],
        'segment': TITLE}}),
    ('B01', 'What got built', 'remotion', {'pattern': 'BrutalistHesitantWriter', 'props': {
        'text': 'Two clips:\na run, a lunge.\nAnimation\nis drawing.',
        'triggerWords': 'drawing', 'replacementWords': 'timing',
        'fontSize': 235, 'lineSpacing': 1.02, 'mistakeRate': 0, 'hesitateWithin': 0, 'hesitateBetween': 0, 'charMs': 32,
        'jitter': 0, 'seed': SLUG, 'face': 'serif', 'align': 'center'}, 'lead_silence_s': 0.8}),
    ('B02', 'Before and after, the same tick', 'still', {}),
    ('B03', 'The run, in play', 'capture', {}),
    ('B04', 'The lunge in both facings, in play', 'capture', {}),
    ('B05', 'An early cast cancels the growl, in play', 'capture', {}),
    ('B06', 'Clip 2: route and source', 'still', {}),
    ('B07', 'The phase table becomes keys (code)', 'remotion', WB),
    ('B08', 'Read back, and logged in the game (result)', 'still', {}),
    ('B09', 'Clip 1: route and source', 'still', {}),
    ('B10', 'The run clip (code)', 'remotion', WB),
    ('B11', 'The run, cell by cell (result)', 'still', {}),
    ('B12', 'One authority (code)', 'remotion', WB),
    ('B13', 'Land, run, cell zero (result)', 'still', {}),
    ('B14', 'Pin first', 'still', {}),
    ('B15', 'The change (code)', 'remotion', WB),
    ('B16', 'What the pin saw (result)', 'still', {}),
    ('B17', 'Edges at the phase boundaries', 'still', {}),
    ('B18', 'Two alignment bugs', 'still', {}),
    ('B19', 'Broken on purpose', 'still', {}),
    ('B20', 'The growl window and a second clock', 'still', {}),
    ('B21', 'The run: r0 and three dead ends', 'still', {}),
    ('B22', 'The run: r1 rejected in play, r2 kept', 'still', {}),
    ('B23', 'Beyond the requirements: the torches (code)', 'remotion', WB),
    ('B24', 'The flicker, measured in the capture (result)', 'still', {}),
    ('B25', 'Embers, afterimage, readability', 'still', {}),
    ('B26', 'Limitations', 'still', {}),
    ('B27', 'Who did what', 'still', {}),
    ('B28', 'Verdict', 'remotion', {'pattern': 'ClaudeVerdictArtifact', 'props': {
        'artifactTitle': 'Verdict', 'artifactHeading': 'Built · measured · judged · open'}}),   # lines: media.py
    ('B29', 'Your Turn', 'remotion', {'pattern': 'ClaudeComposerAsk', 'props': {
        **COMPOSER, 'topic': 'CSYE 7270 · suggested prompt, not a saved chat', 'greeting': 'Your turn.',
        'runningText': 'paste this into Claude…', 'output': [],
        'command': 'Please use Walker to add in-between frames to my mage\'s\nrun so the planted foot stops sliding. First predict,\n'
                   'in pixels, how far the body moves while one cell is held\nat 110 px/s and 10 fps; then measure the foot in a\n'
                   'windowed Movie Maker strip, and show the behaviour pin\nstill matches tick for tick.',
        'segment': 'Your Turn'}}),
    ('B30', 'Regular outro', 'outro', {'pattern': 'ClaudeTitleOutro', 'props': {'title': TITLE, 'slug': SLUG}}),
]

SHOT_TYPE = {'remotion': 'REMOTION', 'outro': 'REMOTION', 'still': 'STILL', 'capture': 'CAPTURE'}


def main():
    spoken = script_narration()
    old = {}
    path = REEL / 'beat_sheet.json'
    if path.exists():
        old = {b['beat_id']: b for b in load_json(path)['beats']}
    beats = []
    for bid, heading, kind, extra in BEATS:
        text = spoken[bid]
        if kind == 'outro':
            assert text == '', f'{bid} must be unnarrated'
        else:
            assert text, f'{bid} has no narration in SCRIPT.md'
        shot = {'type': SHOT_TYPE[kind], 'source': 'capture' if kind == 'capture' else 'own', 'classification': 'SHOW',
                'visual_intent': heading, 'show': [{'at': 'beat', 'event': heading}]}
        if kind in ('remotion', 'outro'):
            shot['remotion'] = {'pattern': extra['pattern'], 'props': dict(extra.get('props', {}))}
        if kind == 'still':
            shot['motion'] = 'hold'
        if kind == 'capture':
            shot['treatment'] = 'none'
        b = {'beat_id': bid, 'heading': heading, 'narration_text': text, 'engine': 'kokoro',
             'voice': 'am_onyx', 'shot': shot, 'visual_kind': kind}
        if 'lead_silence_s' in extra:
            b['lead_silence_s'] = extra['lead_silence_s']
        if kind == 'outro':
            b.update({'act': 'outro', 'audio_policy': 'silence', 'estimated_duration_s': 6.066667,
                      'actual_duration_s': 6.066667})
        prev = old.get(bid)
        if prev and prev.get('narration_text') == text and text:
            for k in ('audio_file', 'actual_duration_s', 'narration_audio'):
                if k in prev:
                    b[k] = prev[k]
        beats.append(b)
    sheet = {'metadata': {
        'slug': SLUG, 'title': TITLE, 'persona': 'Liam', 'brand': 'claude-liam', 'channel': '@NikBearBrown',
        'palette': 'claude', 'engine': 'kokoro', 'voice': 'am_onyx', 'voice_kokoro': 'am_onyx',
        'fps': 30, 'width': 3840, 'height': 2160, 'aspect_ratio': '16:9', 'fit': 'crop',
        'caption_policy': 'No captions (not requested); no burned captions',
        'skill': 'godot-gamedev', 'modifier': 'walker', 'game_revision': BUILD,
        'capture_source': f'capture/run-01.mp4: the real main scene at {BUILD}, played by capture/driver.gd (scripted '
                          'input through key and mouse events), Movie Maker, windowed, 640x360 at 60 fps (one frame per '
                          'physics tick), shown x5 nearest neighbour; fixtures: captures/ (capture harnesses and preview '
                          'scenes that place the characters)',
        'human_review_approved': False,
        'authorization': 'Author requested the CSYE 7270 Assignment 7 film (prompt-6-film.txt). Local 4K master for the '
                         'author to review; no upload or publication; film records committed, media kept out of git.'},
        'beats': beats}
    save_json(path, sheet)
    words = sum(len(b['narration_text'].split()) for b in beats)
    print(f'wrote {path.name}: {len(beats)} beats; narrated {sum(1 for b in beats if b["narration_text"])}; {words} words')


if __name__ == '__main__':
    main()
