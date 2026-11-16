"""Phase 1: write beat_sheet.json from the approved SCRIPT.md.

Narration is taken verbatim from SCRIPT.md (plus the Your Turn sign-off the skill requires,
SIGN_OFF). Measured narration already in the sheet is kept when the text is unchanged, so
re-running this never silently invalidates generated audio.
"""
from common import REEL, SLUG, TITLE, BUILD, load_json, save_json, script_narration

SIGN_OFF = ' Liam, in for Bear.'   # godot-gamedev SKILL.md: "Liam signs off in Your Turn."

COMPOSER = {'topic': 'CSYE 7270 · reconstructed prompt, not a saved chat', 'greeting': 'Hello, Liam',
            'runningText': '', 'folderLabel': 'walker-magic', 'modelLabel': 'Claude Code',
            'effortLabel': '', 'placeholder': ''}

# id, heading, visual kind, extra
BEATS = [
    ('B00', 'Walker opening', 'remotion', {'pattern': 'ClaudeComposerAsk', 'props': {
        **COMPOSER,
        'command': 'Please use Walker to convert my game design document\nabout a fire mage in a cold cave into three simple\n'
                   '3D props — a rock, a crystal and a treasure chest —\nbuilt in Blender through the MCP and checked in Godot.',
        'output': ['rock.glb · 1.0 × 0.8 × 0.7 m · 60 triangles',
                   'crystal.glb · 0.35 × 0.35 × 0.6 m · 30 triangles',
                   'chest.glb · 0.8 × 0.5 × 0.6 m · 76 triangles',
                   'test_a3_assets.gd · 22 checks / 0 failures'],
        'segment': TITLE}}),
    ('B01', 'What got built', 'remotion', {'pattern': 'BrutalistHesitantWriter', 'props': {
        'text': 'Three 3D props\nfor a 2D cave game.\nThe check passed:\nthe look is right.',
        'triggerWords': 'look', 'replacementWords': 'size',
        'fontSize': 190, 'mistakeRate': 0, 'hesitateWithin': 0, 'hesitateBetween': 0, 'charMs': 50, 'jitter': 0,
        'seed': SLUG, 'face': 'serif', 'align': 'center'}}),
    ('B02', 'The assignment, and this game', 'still', {}),
    ('B03', 'Learning the window', 'still', {}),
    ('B04', 'The prompt and the approval', 'still', {}),
    ('B05', 'Rock, Revision 1 (code)', 'still', {}),
    ('B06', 'Rock (result)', 'still', {}),
    ('B07', 'The hand edit', 'still', {}),
    ('B08', 'Crystal (code)', 'still', {}),
    ('B09', 'Crystal (result)', 'still', {}),
    ('B10', 'Chest lid (code)', 'still', {}),
    ('B11', 'Chest (result)', 'still', {}),
    ('B12', 'Export (code)', 'still', {}),
    ('B13', 'Export (result)', 'still', {}),
    ('B14', "The author's look in Godot", 'still', {}),
    ('B15', 'The scene fixes (code)', 'remotion', {'pattern': 'GodotDevWorkbench'}),
    ('B16', 'The running scene (result)', 'footage', {'take': 'run-01'}),
    ('B17', 'The headless check (code)', 'remotion', {'pattern': 'GodotDevWorkbench'}),
    ('B18', 'The headless check (result)', 'still', {}),
    ('B19', 'What Claude got wrong', 'still', {}),
    ('B20', 'Verdict', 'remotion', {'pattern': 'ClaudeVerdictArtifact', 'props': {
        'artifactTitle': 'Verdict', 'artifactHeading': 'Built · measured · judged · unknown'}}),   # lines: media.py
    ('B21', 'Your Turn', 'remotion', {'pattern': 'ClaudeComposerAsk', 'props': {
        **COMPOSER, 'topic': 'CSYE 7270 · suggested prompt, not a saved chat', 'greeting': 'Your turn.',
        'runningText': 'paste this into Claude…', 'output': [],
        'command': 'Please use Walker to add a torch beside my treasure chest:\none prop from basic shapes, under 150 triangles,\n'
                   'warm emission, origin at its base. Before building,\npredict its bounding box in metres, then add a line to\n'
                   'my headless asset check that fails if the prediction is wrong.',
        'segment': 'Your Turn'}}),
    ('B22', 'Regular outro', 'outro', {'pattern': 'ClaudeTitleOutro', 'props': {'title': TITLE, 'slug': SLUG}}),
]

SHOT_TYPE = {'remotion': 'REMOTION', 'outro': 'REMOTION', 'still': 'STILL', 'footage': 'FOOTAGE'}


def main():
    spoken = script_narration()
    old = {}
    path = REEL / 'beat_sheet.json'
    if path.exists():
        old = {b['beat_id']: b for b in load_json(path)['beats']}
    beats = []
    for bid, heading, kind, extra in BEATS:
        text = spoken[bid] + (SIGN_OFF if bid == 'B21' else '')
        if kind == 'outro':
            assert text == '', f'{bid} must be unnarrated'
        else:
            assert text, f'{bid} has no narration in SCRIPT.md'
        shot = {'type': SHOT_TYPE[kind], 'source': 'own', 'classification': 'SHOW',
                'visual_intent': heading, 'show': [{'at': 'beat', 'event': heading}]}
        if kind in ('remotion', 'outro'):
            shot['remotion'] = {'pattern': extra['pattern'], 'props': dict(extra.get('props', {}))}
        if kind == 'still':
            shot['motion'] = 'hold'
        b = {'beat_id': bid, 'heading': heading, 'narration_text': text, 'engine': 'kokoro',
             'voice': 'am_onyx', 'shot': shot, 'visual_kind': kind}
        if 'take' in extra:
            b['gameplay_take'] = extra['take']
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
        'capture_source': f'{BUILD} (git archive of walker-magic-zhefan; capture copy with a 3840x2160 root viewport '
                          'and the camera harness only, see CAPTURE.md)',
        'human_review_approved': False,
        'authorization': 'Author requested the CSYE 7270 Assignment 3 film. Local 4K master for the author to review; '
                         'no upload, publication or README/SUBMISSION record until the author has watched it.'},
        'beats': beats}
    save_json(path, sheet)
    print(f'wrote {path.name}: {len(beats)} beats; narrated {sum(1 for b in beats if b["narration_text"])}')


if __name__ == '__main__':
    main()
