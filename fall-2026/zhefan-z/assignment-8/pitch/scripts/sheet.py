"""Phase 1: write beat_sheet.json from the plan below (narration and visual plan), then, after Kokoro, pad the beats
whose picture needs more time than their words.

    python sheet.py            # (re)write beat_sheet.json from PLAN, keeping measured durations already in it
    python sheet.py --pad      # after generate_audio_kokoro.py: add each beat's lead/tail silence to its mp3
                               # (G11's track is built by audio.py instead: narration, then the game's own sounds)

Written by Claude Code for the Assignment 8 pitch film; rebuilt 2026-11-22 for the updated assignment (prompt-2-gdd.txt):
the film follows the spec's order -- title card with the GDD's metadata, the game in brief, the GDD's sixteen beats,
the seven questions (only what the GDD beats have not already said), the appendix, the silent outro. The narration is
the author's GDD.md and PROJECT-BRIEF.md put into spoken sentences, in the author's first person (Liam's voice speaks
as Zhefan Zhang). Every number in it is in those two files or in a committed log; FACTCHECK.md maps each one.

Labels: each beat names what its picture is -- real (captured play or the game's own files, with the revision),
generated (the Gemini concept art), constructed (drawn for this film), or figure (drawn from committed logs).
"""
import sys

from common import REEL, SLUG, TITLE, AUTHOR, FPS, W, H, REV_A7, load_json, save_json, run

# id, part, heading, kind, label, narration, (lead_s, tail_s) silence added around the measured voice
#   kind: still (a held PNG), capture (gameplay video), audio (G11: a video timed to the game's own sounds)
PLAN = [
    ('T00', 'title', 'Title: The Little Flame Witch, GDD 2.0', 'still', 'constructed',
     "I'm Zhefan Zhang. This pitch is built from my game design document for The Little Flame Witch, "
     "version 2.0, dated November 21, 2026.", (0.4, 0.8)),
    ('P01', 'brief', 'The game in brief', 'still', 'mixed',
     "The Little Flame Witch is an HD-2D cave action game: you aim fireballs with the mouse to fight through a cold "
     "cave. The goal is to reach the bottom and defeat the great wolf that guards it. A pit or losing all your HP "
     "sends you back, and beating the great wolf will end the game.", (0.3, 0.8)),
    ('G01', 'GDD 1', 'GDD 1 · Design pillars', 'still', 'constructed',
     "Section one, the design pillars. Your fire is the only warmth. Every failure is fair. "
     "Readable at a glance, even muted. Small witch, big threat.", (0.3, 0.8)),
    ('G02', 'GDD 2', 'GDD 2 · Core gameplay loop', 'still', 'constructed',
     "The core loop. Moment to moment, you move, jump, aim and fire, and decide whether to shoot a growling wolf early "
     "or step out of reach. In one sitting, you'll clear a level, rest at a campfire and go on to the great wolf. "
     "A short run brings you back for a cleaner one.", (0.3, 0.6)),
    ('G03', 'GDD 3', 'GDD 3 · Player experience goals', 'still', 'constructed',
     "The player should feel small but capable when an early fireball cancels a lunge, safe at a campfire, "
     "tense when the great wolf enters, and relieved when the cave falls quiet.", (0.3, 0.6)),
    ('G04', 'GDD 4', 'GDD 4 · Core mechanics', 'capture', 'real',
     "Core mechanics, built today: A and D or the arrows to run, Space to jump, with a 0.08-second coyote time and no "
     "double jump, and the mouse to aim and cast. A pit or zero HP shows the reason, then the level restarts. "
     "Heal and interact will come later.", (0.3, 1.0)),
    ('G05', 'GDD 5', 'GDD 5 · Systems: the wolf and health', 'capture', 'real',
     "Systems. Each wolf is a state machine with a phase table: growl 31 ticks, lunge 22, recover 36. A hit during "
     "the growl cancels the lunge; once the dash starts, it commits. A hit on the witch costs one of five hearts, "
     "with a tint, a blink and a second of invulnerability. The boss, hazards and campfire will follow.", (0.3, 1.0)),
    ('G06', 'GDD 6', 'GDD 6 · Progression', 'still', 'constructed',
     "Progression: no levelling and no equipment. The witch will gain one thing, the heal spell, from the chest at "
     "the end of level one, while each level adds more wolves, then spikes and a boulder, then the great wolf.",
     (0.3, 0.6)),
    ('G07', 'GDD 7', 'GDD 7 · World and environment', 'still', 'constructed',
     "The world is one cold cave under a mountain, in two to three short levels: the cave mouth, deeper tunnels if "
     "there are three, and the great wolf's den. Its one rule: warmth comes only from fire, so lit places are safe.",
     (0.3, 0.6)),
    ('G08', 'GDD 8', 'GDD 8 · Narrative', 'still', 'constructed',
     "The narrative will be simple: four short, skippable scenes with portraits. She goes down with the only flame "
     "she has, rests at a campfire, is told to turn back, and is let through after the fight.", (0.3, 0.6)),
    ('G09', 'GDD 9', 'GDD 9 · Characters', 'still', 'mixed',
     "Characters: the witch, a pixel sprite in play and a generated portrait in dialogue; the grey cave wolves that "
     "growl before they lunge; and the great wolf, which so far exists only as concept art.", (0.3, 0.6)),
    ('G10', 'GDD 10', 'GDD 10 · Art direction', 'still', 'mixed',
     "Art direction. On the left, what exists: the pixel sprites, the four-frame run cycle, the wolf's lunge rig, my "
     "Assignment 3 props and the cave lights. On the right, the planned HD-2D look: depth of field, bloom, fog, and "
     "the fireball as a moving light.", (0.3, 0.6)),
    ('G11', 'GDD 11', 'GDD 11 · Sound and music', 'audio', 'real',
     "Sound and music, from Assignment 2: a cave theme made with Lyria and cut into a loop, and five effects made with "
     "Stable Audio Open. A boss theme, a campfire theme and new effects will be added. Here they are, from the "
     "game's own files.", (0.3, 0.4)),
    ('G12', 'GDD 12', 'GDD 12 · Feature list', 'still', 'constructed',
     "The feature list. The must column: the 3D cave and camera, the core actions in 3D, wolves with the growl "
     "cancel, two levels, the boss, HP and restart, and a Windows build with a test report. The smallest playable "
     "version: one 3D room, one wolf, and my pin passing.", (0.3, 0.6)),
    ('G13', 'GDD 13', 'GDD 13 · Out of scope', 'still', 'constructed',
     "Out of scope: no multiplayer, no save system, no levelling, equipment or shops, no web export, and none of "
     "Assignment 4's later chapters.", (0.3, 0.6)),
    ('G14', 'GDD 14', 'GDD 14 · Technical requirements', 'still', 'constructed',
     "Technically: Godot 4.7.2 with Forward+, a Windows build, and a target of 60 frames per second at 1080p on my "
     "RTX 5060 Laptop GPU, measured, not claimed. Rooms will go from grey boxes to low-poly Blender pieces, with the "
     "sprites as camera-facing billboards.", (0.3, 0.6)),
    ('G15', 'GDD 15', 'GDD 15 · Risks', 'still', 'constructed',
     "The risks. Moving the 2D game into 3D could break what already works: I'll test one room first, judged by my "
     "Assignment 7 pin, and if it fails, the 2D layer stays and the 3D becomes the backdrop. Three levels may not "
     "fit, so the plan allows two. And if the look misses 60 fps, the costliest effect goes first.", (0.3, 0.6)),
    ('G16', 'GDD 16', 'GDD 16 · Open questions', 'still', 'constructed',
     "Open questions: a 2D layer or 3D bodies on a plane, two levels or three, and whether the pixel sprites read "
     "under depth of field. Each has its test: the one-room spike, the first playable level, and captures from the "
     "first room.", (0.3, 0.6)),
    ('Q01', 'Question 1', 'Question 1 · What it is', 'still', 'constructed',
     "Now the seven questions. What it is: when it's done, a playable Windows desktop build, a zip with an exe, of a "
     "vertical slice from title screen to end screen.", (0.3, 0.6)),
    ('Q02', 'Question 2', 'Question 2 · Why anyone would care', 'still', 'constructed',
     "Why care? It will put Octopath Traveler's HD-2D look together with Metal Slug-style side-scrolling, "
     "with a mouse-aimed fireball. Octopath is turn-based, Metal Slug fires in fixed directions, "
     "Hollow Knight is a large cave with progression; I've played all three. This will be a short action run.",
     (0.3, 0.6)),
    ('Q03', 'Question 3', 'Question 3 · Who opens it, and the first sixty seconds', 'still', 'constructed',
     "Who opens it? A hiring manager or a lead gameplay programmer; my target role is gameplay programmer. "
     "In the first sixty seconds they'll unzip it, double-click the exe, see the controls on the title screen, "
     "skip the opening line with one key, and be playing within a minute.", (0.3, 0.6)),
    ('Q04', 'Question 4', 'Question 4 · What it proves', 'still', 'figure',
     "What will it prove? That I can build and verify gameplay systems. The evidence started in Assignment 7: I "
     "pinned the wolf every physics tick before the growl cancel; only the two scenarios with a hit during the growl "
     "changed; and thirty-eight headless test runs passed in a fresh clone.", (0.3, 0.6)),
    ('Q05', 'Question 5', 'Question 5 · What comes first, and how anyone would know it ran', 'still', 'constructed',
     "What comes first: the core loop in one 3D cave room, where the witch runs, jumps and casts at a wolf. "
     "It ran if my existing behaviour pin passes there and a windowed capture shows it, labelled with its revision.",
     (0.3, 0.6)),
    ('Q07', 'Question 7', 'Question 7 · Why this project: what is new', 'still', 'constructed',
     "Why this project? Half learning, half showing. New to me: HD-2D itself, a lit 3D cave, its camera, "
     "and 2D sprites placed in it.", (0.3, 0.6)),
    ('Q07B', 'Question 7', 'Already have: the hurt tint (Assignment 5)', 'capture', 'real',
     "Already mine: the hurt-tint shader from Assignment 5,", (0.2, 0.0)),
    ('Q07C', 'Question 7', 'Already have: the particles (Assignment 6)', 'capture', 'real',
     "the fireball particles from Assignment 6, measured at about 0.02 and 0.10 milliseconds of GPU time "
     "on an RTX 5060 Laptop GPU,", (0.1, 0.0)),
    ('Q07D', 'Question 7', 'Already have: the run cycle (Assignment 7)', 'capture', 'real',
     "and the run cycle, state machines and tests from Assignment 7.", (0.1, 0.0)),
    ('A01', 'Appendix', 'Appendix · Exists today', 'capture', 'real',
     "Appendix: is this realistic? Today I have the 2D game, with its run cycle, lunge rig, cave lights, particles, "
     "hurt tint and thirty-eight passing test runs, plus my Assignment 3 props and the concept portraits.", (0.3, 0.8)),
    ('A02', 'Appendix', 'Appendix · Started, not finished', 'still', 'constructed',
     "Started but not finished: this GDD and brief, and the story scenes, whose portraits exist but whose dialogue "
     "box and triggers don't. Nothing of the 3D cave is started yet.", (0.3, 0.6)),
    ('A03', 'Appendix', 'Appendix · Not started (will exist)', 'still', 'constructed',
     "Not started: the 3D levels and camera, the look, the story in the game, the heal spell, the great wolf, the "
     "hazards, the rest point, title and end screens, the Windows export and its test report.", (0.3, 0.6)),
    ('A04', 'Appendix', 'Appendix · Can one person finish it?', 'still', 'constructed',
     "Can one person finish it? Yes, at the must and should size with two levels. If I fall behind, I'll cut the "
     "third level first, then the could items, then the story scenes, and keep the must column whole.", (0.3, 0.6)),
    ('A05', 'Appendix', 'Appendix · Where every asset comes from', 'still', 'mixed',
     "Every asset's source: the sprites, run sheet and portraits from Gemini; the lunge rig and the 3D props, mine; "
     "the music from Lyria and the effects from Stable Audio Open; the shaders and particles, my own. "
     "Nothing bought, and no third-party game assets.", (0.3, 1.2)),
    ('OUT', 'outro', 'Outro', 'still', 'constructed', '', (0.0, 0.0)),
]
OUTRO_S = 4.0
# The footage beats need at least this much time on screen; the shortfall becomes held-frame time, never retiming.
MIN_S = {'Q07B': 6.0, 'Q07C': 7.0, 'Q07D': 5.0}

# The voice reads narration_text; these spoken forms keep Kokoro from guessing at tokens (the toolkit's normaliser only
# maps symbols). PLAN keeps the written script, which FACTCHECK.md quotes and the screen shows.
SAY = [('HD-2D', 'H-D two-D'), ('2D', 'two-D'), ('3D', 'three-D'), ('RTX 5060', 'R-T-X fifty-sixty'),
       ('0.02 and 0.10 milliseconds', 'zero point zero two and zero point one zero milliseconds'),
       ('0.08-second', 'zero point zero eight second'), ('Godot 4.7.2', 'Godot four point seven point two'),
       ('1080p', 'ten-eighty p'), ('60 fps', 'sixty frames per second'), ('the exe', 'the E-X-E'),
       ('version 2.0', 'version two point oh'), ('GDD', 'G-D-D')]


def spoken(text):
    for a, b in SAY:
        text = text.replace(a, b)
    return text


def plan():
    return {p[0]: p for p in PLAN}


def write():
    path = REEL / 'beat_sheet.json'
    old = {b['beat_id']: b for b in load_json(path)['beats']} if path.exists() else {}
    beats = []
    for bid, part, heading, kind, label, text, (lead, tail) in PLAN:
        b = {'beat_id': bid, 'part': part, 'heading': heading, 'narration_text': spoken(text), 'script_text': text,
             'engine': 'kokoro', 'voice': 'am_onyx', 'label': label, 'pad_s': [lead, tail],
             'shot': {'type': 'STILL' if kind == 'still' else 'VIDEO',
                      'source': 'capture' if kind in ('capture', 'audio') else 'own',
                      'classification': 'SHOW', 'visual_intent': heading,
                      'show': [{'at': 'beat', 'event': heading}],
                      'motion': 'hold' if kind == 'still' else 'video'},
             'visual_kind': kind}
        if bid == 'P01':
            b['qc'] = {'contrast_regions': [{'label': 'the game in brief text', 'box': [0.05, 0.75, 0.95, 0.93]}],
                       'contrast_reason': 'A real captured frame and a portrait fill most of the card; the brief '
                                          'text below them is checked in its own region.'}
        if bid == 'OUT':
            b.update({'act': 'outro', 'audio_policy': 'silence', 'estimated_duration_s': OUTRO_S,
                      'actual_duration_s': OUTRO_S})
        else:
            b['audio_file'] = f'mp3/beat-{bid}.mp3'
            prev = old.get(bid, {})
            if prev.get('narration_text') == spoken(text) and prev.get('actual_duration_s'):
                b['actual_duration_s'] = prev['actual_duration_s']
                for k in ('voice_s', 'padded', 'audio_mix'):
                    if k in prev:
                        b[k] = prev[k]
        beats.append(b)
    sheet = {'metadata': {
        'slug': SLUG, 'title': TITLE, 'author': AUTHOR, 'persona': 'Liam (Kokoro am_onyx) speaking as the author',
        'engine': 'kokoro', 'voice': 'am_onyx', 'voice_kokoro': 'am_onyx', 'fps': FPS, 'width': W, 'height': H,
        'aspect_ratio': '16:9', 'fit': 'crop', 'caption_policy': 'No captions (not requested); no burned captions',
        'skill': 'godot-waikthrough', 'modifier': 'walker (capture contract only; see BUILD-PROMPT.md)',
        'game_revision': REV_A7, 'gdd': 'GDD.md version 2.0, 2026-11-21',
        'structure': 'title (GDD metadata) · game in brief · GDD 1-16 · questions 1, 2, 3, 4, 5, 7 (6 is GDD 15) · '
                     'appendix · outro',
        'capture_source': 'capture/run-01.mp4 and capture/run-02.mp4: the real main scene at 840b501, played by '
                          'capture/driver.gd and capture/driver_fail.gd (scripted input), Movie Maker, windowed, '
                          '640x360 at 60 fps, archived x6 nearest neighbour; capture/a5-run-01.mp4: the Assignment 5 '
                          "game at 2b68e0a; the Assignment 6 film's capture run-01.mp4 at 3c37fe0, reused unchanged "
                          '(SHA-256 checked); one render of the Assignment 3 prop scene at 840b501; the Assignment 2 '
                          'music and sound files read at 840b501',
        'authorization': 'Author requested the CSYE 7270 Assignment 8 pitch film (pitch/prompt-1-pitch.txt) and its '
                         'rebuild from the GDD (pitch/prompt-2-gdd.txt). Local 4K master for the author to review; no '
                         'upload or publication; records committed, media kept out of git.',
        'human_review_approved': False}, 'beats': beats}
    save_json(path, sheet)
    print('beat_sheet.json:', len(beats), 'beats')


def pad():
    """Add each beat's lead/tail silence (and any held-frame room a footage beat needs) to its measured mp3."""
    path = REEL / 'beat_sheet.json'
    sheet = load_json(path)
    for b in sheet['beats']:
        if b.get('audio_policy') == 'silence' or b.get('padded') or b['visual_kind'] == 'audio':
            continue
        mp3 = REEL / b['audio_file']
        voice = float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', mp3])
                      .stdout.decode().strip())
        lead, tail = b['pad_s']
        want = max(voice + lead + tail, MIN_S.get(b['beat_id'], 0.0))
        tail = want - voice - lead
        tmp = mp3.with_suffix('.tmp.mp3')
        run(['ffmpeg', '-v', 'error', '-y', '-i', mp3, '-af', f'adelay={int(lead * 1000)}:all=1,apad=pad_dur={tail:.3f}',
             '-ar', '24000', '-ac', '1', '-c:a', 'libmp3lame', '-b:a', '192k', tmp])
        tmp.replace(mp3)
        dur = float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', mp3])
                    .stdout.decode().strip())
        b['voice_s'] = round(voice, 3)
        b['actual_duration_s'] = round(dur, 2)
        b['padded'] = [lead, round(tail, 3)]
        print(f"{b['beat_id']}: voice {voice:.2f}s -> {dur:.2f}s (lead {lead}, tail {tail:.2f})")
    save_json(path, sheet)


if __name__ == '__main__':
    pad() if '--pad' in sys.argv else write()
