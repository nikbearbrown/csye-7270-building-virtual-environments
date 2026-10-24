"""Phase 1: write beat_sheet.json from the approved SCRIPT.md.

Narration is taken verbatim from SCRIPT.md (the one approved addition is the
Your Turn sign-off the skill requires, marked SIGN_OFF). Measured narration
(audio_file, actual_duration_s) already in the sheet is kept when the text is
unchanged, so re-running this never silently invalidates generated audio.
"""
from common import REEL, SLUG, TITLE, BUILD, load_json, save_json, script_narration

SIGN_OFF = ' Liam, in for Bear.'   # godot-gamedev SKILL.md: "Liam signs off in Your Turn."

COMPOSER = {'topic': 'CSYE 7270 · reconstructed prompt, not a saved chat', 'greeting': 'Hello, Bear',
            'runningText': '', 'output': [], 'folderLabel': 'walker-magic', 'modelLabel': 'Claude Code',
            'effortLabel': '', 'placeholder': ''}

# id, heading, visual kind, extra
BEATS = [
    ('B01', 'Walker opening', 'remotion', {'pattern': 'ClaudeComposerAsk', 'props': {
        **COMPOSER,
        'command': 'Please use Walker to convert my game design document\nabout a young fire mage carrying the only warm light\nthrough a dark cave into a small Godot asset slice.',
        'segment': TITLE}}),
    ('B02', 'What got built', 'remotion', {'pattern': 'BrutalistHesitantWriter', 'props': {
        'text': 'This film is about the generated assets.', 'triggerWords': 'generated',
        'replacementWords': 'designed', 'fontSize': 100, 'mistakeRate': 0, 'hesitateWithin': 0,
        'hesitateBetween': 0, 'charMs': 60, 'jitter': 0, 'seed': SLUG, 'face': 'serif', 'align': 'center'}}),
    ('B03', 'The assignment, and the build shown', 'still', {}),
    ('B04', 'Concept and pillars', 'remotion', {'pattern': 'GodotDesignBoard'}),
    ('B05', 'Asset trace 1/5: the design', 'still', {}),
    ('B06', 'Asset trace 2/5: the prompt', 'video', {}),
    ('B07', 'Asset trace 3/5: the raw output', 'still', {}),
    ('B08', 'Asset trace 4/5: the edits (code)', 'remotion', {'pattern': 'ClaudeCodeBeat'}),
    ('B09', 'Asset trace 4/5: the edits (result)', 'still', {}),
    ('B10', 'Asset trace 5/5: in the engine (code)', 'remotion', {'pattern': 'GodotDevWorkbench'}),
    ('B11', 'Asset trace 5/5: in the engine (result)', 'footage', {'take': 'run-01'}),
    ('B12', 'Cause and effect (code)', 'remotion', {'pattern': 'ClaudeCodeBeat'}),
    ('B13', 'Cause and effect (result)', 'video', {'take': 'run-01'}),
    ('B14', 'Cast (code)', 'remotion', {'pattern': 'GodotDevWorkbench'}),
    ('B15', 'Cast and the wolf (result)', 'footage', {'take': 'run-01'}),
    ('B16', 'Sound wiring (code)', 'remotion', {'pattern': 'GodotDevWorkbench'}),
    ('B17', 'Sound wiring (result)', 'footage', {'take': 'run-01 + run-02'}),
    ('B18', 'SLICE AUDIO — no narration', 'slice', {'take': 'run-01 + run-02'}),
    ('B19', 'Mute (code)', 'remotion', {'pattern': 'GodotDevWorkbench'}),
    ('B20', 'Mute (result), with a SLICE AUDIO slot', 'footage', {'take': 'run-03'}),
    ('B21', 'The automated check (code)', 'remotion', {'pattern': 'GodotDevWorkbench'}),
    ('B22', 'The automated check (result)', 'still', {}),
    ('B23', 'Models, contributions and credits', 'still', {}),
    ('B24', 'Verdict', 'remotion', {'pattern': 'ClaudeVerdictArtifact', 'props': {
        'artifactTitle': 'Verdict', 'artifactHeading': 'Implemented · limits · human judgment'}}),   # lines: media.py
    ('B25', 'Your Turn', 'remotion', {'pattern': 'ClaudeComposerAsk', 'props': {
        **COMPOSER, 'topic': 'CSYE 7270 · suggested prompt, not a saved chat',
        'command': "Please use Walker to shorten the wolf's growl\nfrom 0.5 s to a third of a second. Predict the hurt count\nin the real-lunge test, then run it.",
        'segment': 'Your Turn'}}),
    ('B26', 'Regular outro', 'outro', {'pattern': 'ClaudeTitleOutro', 'props': {'title': TITLE, 'slug': SLUG}}),
]

SHOT_TYPE = {'remotion': 'REMOTION', 'outro': 'REMOTION', 'still': 'STILL', 'video': 'VIDEO',
             'footage': 'FOOTAGE', 'slice': 'FOOTAGE'}


def main():
    spoken = script_narration()
    old = {}
    path = REEL / 'beat_sheet.json'
    if path.exists():
        old = {b['beat_id']: b for b in load_json(path)['beats']}
    beats = []
    for bid, heading, kind, extra in BEATS:
        text = spoken[bid] + (SIGN_OFF if bid == 'B25' else '')
        if kind in ('slice', 'outro'):
            assert text == '', f'{bid} must be unnarrated'
        else:
            assert text, f'{bid} has no narration in SCRIPT.md'
        shot = {'type': SHOT_TYPE[kind], 'source': 'own', 'classification': 'SHOW',
                'visual_intent': heading, 'show': [{'at': 'beat', 'event': heading}]}
        if kind in ('remotion', 'outro'):
            shot['remotion'] = {'pattern': extra['pattern'], 'props': dict(extra.get('props', {}))}
        if kind in ('still',):
            shot['motion'] = 'hold'
        b = {'beat_id': bid, 'heading': heading, 'narration_text': text, 'engine': 'kokoro',
             'voice': 'am_onyx', 'shot': shot, 'visual_kind': kind}
        if 'take' in extra:
            b['gameplay_take'] = extra['take']
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
        'capture_source': '5266946 (runtime files identical to 74c0443)',
        'human_review_approved': False,
        'authorization': 'Author requested the CSYE 7270 Assignment 2 film. Local 4K master for the author to review; '
                         'no upload, publication or README/SUBMISSION record until the author has watched it.',
        'audio_note': 'SLICE AUDIO beats (B18, B20 slot) use the same Movie Maker take audio cut to the same interval '
                      'as their video; verbal approval from the instructor the method is acceptable.'},
        'beats': beats}
    save_json(path, sheet)
    print(f'wrote {path.name}: {len(beats)} beats; narrated {sum(1 for b in beats if b["narration_text"])}')


if __name__ == '__main__':
    main()
