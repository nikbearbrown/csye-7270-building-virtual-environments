#!/usr/bin/env python3
"""Author the three PBR lecture packages (CSYE 7270). Writes beat sheets and paperwork; no audio, no render.

Run: python3 prepare_pbr_films.py            (all three)
     python3 prepare_pbr_films.py <slug>     (one)
Re-running keeps audio_file / actual_duration_s / render_duration_s for beats whose narration is unchanged.
"""
from pathlib import Path
import json, sys

HERE = Path(__file__).resolve().parent
BOOK = HERE.parents[1]
YT = BOOK / 'youtube'
TOOLKIT = BOOK.parent / 'brutalist.art'
CH7 = BOOK / 'chapters/07-materials-and-textures.md'
CH3 = BOOK / 'chapters/03-blender-mcp-to-godot.md'
DECK = BOOK / 'glossary/decks/12 Materials and textures.html'
PLAYLIST = 'CSYE 7270 Building Virtual Environments'
SPOKEN_PLAYLIST = 'C S Y E seventy-two seventy, Building Virtual Environments.'
CAPTION = 'Godot 4.7.2 · recorded render'

FILMS = [
 {
  'slug': 'what-is-pbr',
  'title': 'What Is PBR?',
  'objective': 'What physically based rendering means, and the five measurements a Godot material is made of.',
  'card_sub': 'The five measurements a Godot material is made of.',
  'greeting': 'Kia ora',
  'idea_text': 'A material is\na picture of a surface',
  'wrong': 'a picture of a surface', 'right': 'a set of measurements',
  'idea_narration': 'Kia ora. This is Liam, in for Bear. Most people picture a material as an image wrapped around a model. In physically based rendering, a material is a set of measurements, and the light does the painting.',
  'terms': [('Mesh', 'The shape: a surface made of triangles'), ('Material', 'What tells Godot how a surface meets light'), ('Texture', 'An image a material can read')],
  'terms_narration': 'Three terms. Mesh: the shape, a surface made of triangles. Material: what tells Godot how that surface meets light. Texture: an image a material can read.',
  'beats': [
   ('Five Measurements', 'manim', 'B01_FiveMeasurements', 'P B R stands for physically based rendering. Instead of painting how a surface looks, you measure what it is. Godot\'s Standard Material 3D holds five measurements: base colour, metallic, roughness, normal and ambient occlusion.',
    'Five labelled measurement slots fill one by one beside a sphere; the word PBR expands to its three words', 'Each slot lands on its spoken name'),
   ('Five Measurements', 'cap', 'albedo', 'Base colour, which Godot calls albedo, is the colour the surface reflects. Watch it change from grey to terracotta to teal. The highlight and the shadow stay where they are, because they come from the light, not from the colour.',
    'Real Godot sphere whose albedo changes while the light stays fixed', 'Hue changes; highlight and shadow do not move'),
   ('Five Measurements', 'cap', 'metallic', 'Metallic says whether the surface behaves like a metal. At zero, the highlight is white and sits on top of the colour. At one, the colour moves into the reflection itself, and the sphere starts to mirror the sky and the floor.',
    'Real Godot brass sphere, metallic 0 to 1, readout of the value', 'White highlight becomes a tinted reflection of the sky and floor'),
   ('Five Measurements', 'cap', 'roughness', 'Roughness says how blurred the reflections are. Godot\'s documentation puts it plainly: zero is a perfect mirror, and one blurs the reflection completely. As roughness rises, the highlight spreads out and grows dimmer.',
    'Real Godot sphere, roughness 0.05 to 1.00, readout of the value', 'The highlight widens and dims as the number rises'),
   ('Five Measurements', 'cap', 'grid', 'Put two of them together and you get the classic chart. Roughness rises from left to right, and metallic from top to bottom. Every sphere has the same base colour. Only two numbers change, and each sphere looks like a different material.',
    'Real Godot 5 by 5 sphere chart, one albedo, slow light sweep', 'Highlights slide across 25 spheres that differ only in two numbers'),
   ('Five Measurements', 'cap', 'normal', 'The normal is the direction the surface faces, at a detail smaller than the mesh. A normal map changes it pixel by pixel. Tiles appear and catch the moving light, but the outline stays perfectly round. The light changes. The geometry does not.',
    'Real Godot sphere: flat normal map, then a tile normal map, under a moving light', 'Tiles appear inside an unchanged round silhouette'),
   ('Five Measurements', 'cap', 'ao', 'Ambient occlusion is how much of the surrounding light reaches a crevice. By default, Godot applies it to ambient light, not to direct light. Lit by the sky alone, the grooves darken when it switches on. Add the sun, and the sunlight ignores the map.',
    'Real Godot sphere: AO off, AO on under sky light only, then sun added', 'Grooves darken only in the sky-lit phase'),
   ('The Light Does the Painting', 'manim', 'B08_LightPaints', 'None of these five is a colour on the screen yet. For every pixel, in every frame, the renderer combines them with a light and a camera. Only then is there a colour to show.',
    'Measurements, a light and a camera converge on one pixel, which takes its colour last', 'The pixel stays empty until light and camera arrive'),
   ('The Light Does the Painting', 'cap', 'lights', 'So a material is always judged under some light. Here are three materials, plastic, gold and rubber, under a noon sun, a sunset and a dim blue room. The lighting changes. The materials never do.',
    'Real Godot plastic, gold and rubber spheres under three lighting presets', 'Lighting changes; labels show the materials stay the same'),
   ('The Light Does the Painting', 'manim', 'B10_ColourOrData', 'One more consequence. Only the base colour is a colour. Metallic, roughness, normal and occlusion are numbers that happen to be stored in image files, so they must be read as numbers.',
    'The five slots again: base colour stays a colour swatch, the other four flip into grids of numbers', 'Four slots turn from pictures into numbers'),
  ],
  'recap': ['A PBR material is measurements, not a picture.', 'Base colour, metallic, roughness, normal, occlusion.', 'A light and a camera turn them into colour.', 'So judge a material under stated lighting.'],
  'exercise': 'In Godot, add a sphere with a Standard Material 3D and a directional light. Predict what the highlight does as roughness goes from zero to one, then set metallic to one and repeat. Rotate the light.',
  'checks': ['The highlight spreads and dims as roughness rises.', 'The base colour never changed while the light moved.'],
  'segment': 'Predict Then Test',
 },
 {
  'slug': 'why-pbr-matters',
  'title': 'Why PBR Matters',
  'objective': 'Why describing a surface as measurements beats painting the light in, and what that buys a game.',
  'card_sub': 'Why measurements beat painting the light in.',
  'greeting': 'Jambo',
  'idea_text': 'PBR just means\nmore realistic graphics',
  'wrong': 'more realistic graphics', 'right': 'materials that hold up under any light',
  'idea_narration': 'Jambo. This is Liam, in for Bear. P B R is often sold as more realistic graphics. The bigger payoff is practical: materials that hold up under any light.',
  'terms': [('PBR', 'Physically based rendering: materials as measurements'), ('Albedo', 'Base colour, with no light painted in'), ('Roughness', 'How blurred the reflections are'), ('Metallic', 'Whether the surface behaves like a metal')],
  'terms_narration': 'Four terms. P B R: physically based rendering, where materials are measurements. Albedo: base colour, with no light painted in. Roughness: how blurred the reflections are. Metallic: whether the surface behaves like a metal.',
  'beats': [
   ('Painting the Light', 'cap', 'painted_static', 'The older shortcut is to paint the light into the texture. On the left, the highlight and the shadow are part of the image. On the right, a P B R material is lit by the scene. Lit from the upper left, the two look much alike.',
    'Real Godot: an unshaded sphere with lighting painted into its texture beside a PBR sphere', 'Two similar spheres; labels say which is painted'),
   ('Painting the Light', 'cap', 'painted_orbit', 'Now move the light. The P B R highlight follows it around the sphere. The painted highlight stays exactly where the painter put it, and the painted shadow ends up facing the sun.',
    'Real Godot: the light orbits; only the PBR highlight moves', 'The PBR highlight travels; the painted one is frozen'),
   ('Painting the Light', 'cap', 'painted_daynight', 'Change the time of day and the gap gets worse. The P B R sphere turns orange at sunset and dims at night. The painted sphere ignores the light entirely, so it glows the same in every scene.',
    'Real Godot: noon, sunset, dim room; the painted sphere never changes', 'PBR sphere tracks the light; painted sphere stays constant'),
   ('One Description, Any Light', 'cap', 'three', 'With P B R you describe a surface once. Plastic, gold and rubber keep reading as plastic, gold and rubber at noon, at sunset and in a dim room, because the light does the painting, not the texture.',
    'Real Godot: three materials under three lighting presets', 'Lighting changes; each material stays recognisable'),
   ('One Description, Any Light', 'manim', 'B05_Profiles', 'P B R models also follow a rule from physics: a surface never sends out more light than it receives. These are brightness measurements taken across Godot renders. As roughness rises, the highlight spreads wider and its peak drops.',
    'Measured brightness profiles across the highlight at roughness 0.2, 0.4 and 0.7, drawn in order', 'Each curve is wider and lower than the last'),
   ('Numbers Travel', 'manim', 'B06_Travel', 'Measurements also travel between tools. A material made in Blender leaves through the G L T F format as base colour, metallic and roughness, and arrives in Godot as a Standard Material 3D. Nobody repaints it.',
    'Blender logo, a glTF file carrying three numbers, Godot logo; the numbers ride across intact', 'The same three numbers arrive unchanged'),
   ('Numbers Travel', 'shell', 'gold.tres', 'And because they are numbers, you can check them. Saved as a text file, a Godot material is a short list of values that a person, a test or an agent can read.',
    'Real terminal output: cat of the gold material saved by Godot', 'The material file prints as plain values'),
   ('Numbers Travel', 'cap', 'metal_sky', 'One warning. P B R does not rescue bad lighting. With nothing to reflect, a polished metal looks like black plastic. Give it a sky and it reads as metal again. Judge every material under the light it will really be seen in.',
    'Real Godot metal sphere: black surroundings, then a sky', 'Black plastic look becomes metal when the sky appears'),
  ],
  'recap': ['Painted light breaks when the light moves.', 'PBR materials hold up under any light.', 'Rougher means a wider, dimmer highlight.', 'Measurements travel between tools and can be checked.'],
  'exercise': 'In Godot, make two spheres: one unshaded with a highlight painted into its texture, and one with a Standard Material 3D. Predict what happens to each as you rotate a directional light all the way round. Then remove the sky and look at a metal sphere.',
  'checks': ['Only the PBR highlight follows the light.', 'The metal needs something to reflect.'],
  'segment': 'Predict Then Test',
 },
 {
  'slug': 'pbr-textures-are-data',
  'title': 'PBR Textures Are Data, Not Pictures',
  'objective': 'Which PBR maps hold colour and which hold numbers, what a normal map stores, and why reading data as colour breaks the lighting.',
  'card_sub': 'Which maps hold colour, which hold numbers.',
  'greeting': 'Aloha',
  'idea_text': 'A roughness map\nis a picture',
  'wrong': 'a picture', 'right': 'a table of numbers',
  'idea_narration': 'Aloha. This is Liam, in for Bear. Texture maps look like pictures, so it is natural to treat them all as pictures. Only one of them is. The rest are tables of numbers.',
  'terms': [('Texel', 'One pixel of a texture'), ('Channel', 'The red, green, blue or alpha part'), ('sRGB', 'A colour encoding spaced for human eyes')],
  'terms_narration': 'Three terms. Texel: one pixel of a texture. Channel: the red, green, blue or alpha part of a texel. S R G B: a colour encoding whose steps are spaced for human eyes.',
  'beats': [
   ('One Colour, Four Data Maps', 'cap', 'stack', 'A P B R material usually arrives as a set of texture maps, one per measurement. Watch this sphere gain them one at a time: base colour, normal, roughness, metallic and ambient occlusion.',
    'Real Godot sphere gaining five maps in order, each named as it lands', 'The surface builds up map by map'),
   ('One Colour, Four Data Maps', 'manim', 'B02_FiveMaps', 'Lay the maps side by side. Only the base colour map is a colour meant for your eyes. The other four are data. They look like grey or blue pictures only because an image file is a handy way to store a grid of numbers.',
    'The five real texture files in a row; base colour ringed, the other four tagged data', 'Four of five maps are re-labelled as data'),
   ('One Colour, Four Data Maps', 'manim', 'B03_RoughNumbers', 'Zoom into the roughness map and read the texels. The tiles hold values near point three. The grout holds point nine. White means rough, and black means smooth. Those numbers are the whole point of the map.',
    'Zoom from the real roughness map into a block of texels that become their actual values', 'Grey squares turn into the numbers they store'),
   ('One Colour, Four Data Maps', 'cap', 'roughmap', 'Plug that grid into the roughness slot and the shine follows it. As the light sweeps across, the smooth tiles flash and the rough grout stays matte. One image, many roughness values.',
    'Real Godot tiled plane with the roughness map, light sweeping', 'Tiles flash while the grout stays matte'),
   ('Normals', 'manim', 'B05_Normal', 'A normal is the direction a surface faces: an arrow standing straight out of it. Lighting depends on the angle between that arrow and the light. Tilt the arrow away from the light, and the surface gets darker.',
    'A surface with its normal arrow and a light ray; tilting the arrow dims the patch as the angle grows', 'Brightness falls as the angle opens'),
   ('Normals', 'manim', 'B06_NormalTexel', 'A normal map stores one arrow per texel. Red is X, green is Y, and blue is Z. A flat texel is one twenty-eight, one twenty-eight, two fifty-five: an arrow pointing straight out. That is why normal maps look pale blue.',
    'One texel\'s three channels map onto the X, Y and Z of an arrow; the flat texel gives a straight-out arrow and a pale blue swatch', 'Three numbers become one arrow'),
   ('Normals', 'cap', 'normal', 'In Godot, the normal map tilts the light texel by texel. Tiles appear and catch the moving light, yet the outline of the sphere stays perfectly round, because the geometry never moved.',
    'Real Godot sphere: flat normal map, then a tile normal map, under a moving light', 'Tiles appear inside an unchanged round silhouette'),
   ('Packed and Decoded', 'manim', 'B08_Pack', 'Because these maps are just numbers, files often pack three into one. A Poly Haven A R M file keeps ambient occlusion in red, roughness in green and metallic in blue. Godot\'s O R M Material 3D reads that same order.',
    'Three greyscale maps slide into the red, green and blue channels of one packed image', 'Three files become one'),
   ('Packed and Decoded', 'manim', 'B09_Decode', 'Here colour and data part ways. Colour values are stored in S R G B and decoded before lighting. Decode a flat normal that way, and one twenty-eight over two fifty-five, about point five, becomes about point two two. The arrow tilts thirty-nine degrees.',
    'The decode curve maps 0.502 to 0.216; the straight-out arrow tips over by 38.8 degrees', 'One wrong decode tilts the arrow'),
   ('Packed and Decoded', 'cap', 'decode', 'Here is that mistake in Godot. Both spheres use the same flat normal map, lit straight on. The left reads it as data and is lit evenly. The right reads it as colour, and its lighting slides off to one side.',
    'Real Godot: the same flat normal map read as data and as colour, side by side', 'The right sphere is lit off-centre'),
  ],
  'recap': ['Only the base colour map is a colour.', 'Roughness, metallic, AO and normal maps hold numbers.', 'A normal map stores one arrow per texel.', 'Read data as colour and the lighting breaks.'],
  'exercise': 'In Godot, open a Standard Material 3D and load a texture into each slot. For every map, predict whether it holds colour or data. Then open a normal map texture and read one texel near a flat area.',
  'checks': ['Only the base colour map should be treated as colour.', 'A flat normal texel reads close to 128, 128, 255.'],
  'segment': 'Colour or Data',
 },
]


SPARSE = {
    ('pbr-textures-are-data', 'B02'): 'Five real texture maps in one row already span the safe width (measured 55%, just under the line); larger squares would push the row past the edge.',
    ('what-is-pbr', 'B10'): 'Five square map tiles in one row already span the safe width; their height is set by the square, so the row cannot fill more of the frame without shrinking the numbers.',
}


def base(bid, act, narration, lane='bookend', gate='SHOW'):
    return {'beat_id': bid, 'act': act, 'lane': lane, 'proof_gate': gate, 'narration_text': narration,
            'estimated_duration_s': round(len(narration.split()) / 2.4, 2), 'voice': 'am_onyx', 'engine': 'kokoro'}


def rem(bid, act, narration, pattern, props, events, lane='bookend'):
    b = base(bid, act, narration, lane)
    b['shot'] = {'type': 'REMOTION', 'source': 'own', 'visual_intent': events[-1]['event'], 'show': events,
                 'motion_claim': events[-1]['event'], 'remotion': {'pattern': pattern, 'props': props}}
    return b


def build(d):
    slug = 'claude-liam-lecture-' + d['slug']
    reel = YT / slug
    reel.mkdir(exist_ok=True)
    title = d['title']
    B = []
    b = base('BOPEN', 'Opening', f"{SPOKEN_PLAYLIST} {title} {d['objective']}", gate='CARD')
    b['shot'] = {'type': 'GRAPHIC', 'source': 'own', 'template': 'lecture-title-slide-16x9', 'narration_contract': 'playlist-title-summary-v1',
                 'motion': 'hold', 'visual_intent': 'Professor Bear portrait, title, narrator credit and learning payoff',
                 'show': [{'at': 0, 'event': 'Complete portrait and title card visible immediately'}]}
    B.append(b)
    b = rem('BIDEA', 'Opening', d['idea_narration'], 'BrutalistHesitantWriter',
            {'text': d['idea_text'], 'triggerWords': d['wrong'], 'replacementWords': d['right'], 'fontSize': 72, 'charMs': 24,
             'seed': slug, 'banner': ''},
            [{'at': 0, 'event': 'Type the common misconception'}, {'at': 0.55, 'event': 'Correct it to: ' + d['right']}])
    b['lead_silence_s'] = 0.8
    b['qc'] = {'sparse_by_design': True, 'sparse_reason': 'The typed correction is the opening visual.'}
    B.append(b)
    B.append(rem('BDEFS', 'Opening', d['terms_narration'], 'ClaudeDefinitions',
                 {'title': 'Terms In This Lecture', 'terms': [{'term': k, 'meaning': v} for k, v in d['terms']]},
                 [{'at': i / len(d['terms']), 'event': 'Reveal ' + k} for i, (k, _) in enumerate(d['terms'])]))
    rows = []
    seen_acts = set()
    for j, (act, kind, ref, narration, intent, claim) in enumerate(d['beats']):
        bid = f'B{j + 1:02d}'
        first = act not in seen_acts
        seen_acts.add(act)
        heading = act if first else ''
        if kind == 'cap':
            props = {'title': heading or capture_title(ref), 'layout': 'video', 'code': '', 'codeFile': '', 'cues': [],
                     'video': f'pbr-captures/{d["slug"]}-{bid}-{ref}.mp4', 'videoLabel': 'Godot output', 'videoAspect': 16 / 9,
                     'caption': CAPTION}
            b = rem(bid, act, narration, 'ShaderLab', props, [{'at': 0, 'event': intent}, {'at': 0.3, 'event': claim}], lane='remotion')
            b['qc'] = {'contrast_regions': [{'label': 'beat title', 'box': [0.06, 0.04, 0.85, 0.12]}], 'contrast_reason': 'Real Godot render keeps its own look (SHOW-THE-THING); judge contrast on the heading.'}
            b['evidence'] = {'capture_id': ref, 'capture_tool': str(HERE / 'tools/capture.gd'), 'project': str(HERE),
                             'frames_log': str(HERE / 'evidence/capture-log.txt')}
            lane, runner = 'ShaderLab (real Godot render)', 'Manim diagram of the same idea'
        elif kind == 'shell':
            out = (HERE / 'evidence/materials' / ref).read_text().rstrip('\n').split('\n')
            props = {'title': 'zsh — _pbr-evidence/evidence', 'lines': [f'$ cat materials/{ref}'] + out, 'fontSize': 44,
                     'startCue': 12, 'lineGap': 10}
            b = rem(bid, act, narration, 'CCPlainShell', props, [{'at': 0, 'event': intent}, {'at': 0.3, 'event': claim}], lane='remotion')
            b['evidence'] = {'command': f'cat {HERE}/evidence/materials/{ref}', 'written_by': str(HERE / 'tools/save_materials.gd')}
            lane, runner = 'CCPlainShell (real command output)', 'ShaderLab still of the Godot inspector'
        else:
            b = base(bid, act, narration, lane='body')
            b['shot'] = {'type': 'GRAPHIC', 'source': 'own', 'visual_intent': intent, 'motion_claim': claim,
                         'show': [{'at': 0, 'event': 'Establish'}, {'at': 0.3, 'event': claim}, {'at': 0.85, 'event': 'Hold the result'}],
                         'manim': {'class': ref}}
            lane, runner = 'Manim lesson', 'ShaderLab still of a Godot render'
        if heading:
            b['act_title'] = heading
        waive = SPARSE.get((d['slug'], bid))
        if waive:
            b.setdefault('qc', {}).update({'sparse_by_design': True, 'sparse_reason': waive})
        B.append(b)
        rows.append((bid, act, intent, lane, runner, kind, ref))
    recap = 'Let’s recap with Claude. ' + ' '.join(d['recap']) + ' Liam, in for Bear.'
    b = rem('BVDT', 'Closing', recap, 'ClaudeVerdictArtifact',
            {'artifactTitle': title, 'artifactHeading': 'What We Established', 'artifactLines': d['recap'], 'lectureLayout': True},
            [{'at': 0, 'event': 'Recap'}, {'at': 0.5, 'event': 'Show remaining recap lines'}])
    b['lead_silence_s'] = 0.5
    B.append(b)
    prompt = d['exercise'] + ' Check two things: ' + ' '.join(d['checks'])
    B.append(rem('BHTF', 'Closing', prompt, 'ClaudeComposerAsk',
                 {'greeting': 'Your turn.', 'largeText': True, 'topic': 'GODOT · YOUR TURN', 'segment': d['segment'], 'command': prompt,
                  'runningText': 'Try this in Godot', 'output': d['checks'], 'folderLabel': '@NikBearBrown'},
                 [{'at': 0, 'event': 'The exercise prompt types'}, {'at': 0.8, 'event': 'Reveal the two checks'}]))
    b = rem('BOUT', 'Closing', title + ' At Nik Bear Brown.', 'ClaudeTitleOutro',
            {'title': title, 'slug': slug, 'lectureLayout': True, 'handle': '@NikBearBrown'},
            [{'at': 0, 'event': 'Exact title, @NikBearBrown and seeded mascot'}])
    b['kind'] = 'outro_voice'
    b['tail_silence_s'] = 1.0
    b['qc'] = {'sparse_by_design': True, 'sparse_reason': 'Locked outro card.'}
    B.append(b)
    sheet = {'metadata': {'slug': slug, 'title': title, 'playlist': PLAYLIST, 'series_title': PLAYLIST,
                          'lecture_opening_description': d['card_sub'], 'skill': 'lecture', 'style_preset': 'lecture',
                          'channel': 'claude-liam', 'persona': 'Liam (in for Bear)', 'voice_kokoro': 'am_onyx', 'voice': 'am_onyx',
                          'engine': 'kokoro', 'palette': 'claude', 'register': 'Teardown', 'clock': 'narration', 'fps': 24,
                          'aspect_ratio': '16:9', 'width': 3840, 'height': 2160, 'course': 'CSYE 7270 Building Virtual Environments',
                          'source_doc': str(CH7), 'caption_policy': 'none',
                          'tags': ['Godot', 'PBR', 'materials', 'game development', 'CSYE 7270'],
                          'status': 'authored; audio and film rendering pending'}, 'beats': B}
    old = reel / 'beat_sheet.json'
    if old.exists():
        prev = {x['beat_id']: x for x in json.loads(old.read_text())['beats']}
        for x in B:
            p = prev.get(x['beat_id'], {})
            if p.get('narration_text') == x['narration_text']:
                for k in ('audio_file', 'actual_duration_s', 'render_duration_s'):
                    if k in p:
                        x[k] = p[k]
                if 'remotion' in x.get('shot', {}) and 'remotion' in p.get('shot', {}):
                    dur = p['shot']['remotion']['props'].get('durationSeconds')
                    if dur:
                        x['shot']['remotion']['props']['durationSeconds'] = dur
    old.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + '\n')
    paperwork(d, reel, B, rows)
    return reel, B


def capture_title(ref):
    return {'albedo': 'Base Colour (Albedo)', 'metallic': 'Metallic', 'roughness': 'Roughness', 'grid': 'Two Numbers, 25 Materials',
            'normal': 'Normal', 'ao': 'Ambient Occlusion', 'lights': 'Same Materials, Three Lights', 'painted_orbit': 'Move the Light',
            'painted_daynight': 'Change the Time of Day', 'three': 'Same Materials, Three Lights', 'metal_sky': 'Metal Needs a World',
            'roughmap': 'A Roughness Map at Work', 'stack': 'Five Maps', 'decode': 'Data Read as Colour', 'painted_static': 'Painted vs Measured'}[ref]


FACTS = {
 'what-is-pbr': [
  ('B01', 'Godot StandardMaterial3D holds base colour, metallic, roughness, normal, AO (metallic–roughness model, as glTF 2.0)', 'Correct', f'{CH7} "A PBR material is a set of measurements"; https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html'),
  ('B02', 'Albedo is the base colour; highlight and shadow come from the light', 'Correct; shown in the render', 'Godot docs: "Albedo is the base color for the material, on which all the other settings operate"; capture albedo'),
  ('B03', 'Metallic 0: white highlight over the colour; metallic 1: colour moves into the reflection', 'Correct; shown in the render', 'capture metallic (frames 0 vs end); Godot docs Metallic section'),
  ('B04', 'Roughness 0 = perfect mirror, 1 = completely blurred reflection', 'Correct (paraphrase of the docs)', 'Godot docs: "A value of 0 makes it a perfect mirror while a value of 1 completely blurs the reflection"'),
  ('B05', 'Chart: roughness left to right, metallic top to bottom, one albedo', 'Correct; capture parameters', 'tools/capture.gd case "grid"'),
  ('B06', 'Normal map changes lighting, not geometry; silhouette stays round', 'Correct', 'Godot docs Normal map: "This does not modify geometry, only the incident angle for light."; capture normal'),
  ('B07', 'AO affects ambient light, not direct light, by default', 'Correct', 'Godot docs AO: "it does not affect direct light by default"; chapter: ao_light_affect defaults to 0.0'),
  ('B08', 'The renderer combines the measurements with light and camera per pixel', 'Correct (conceptual)', f'{CH7}: "A light and a camera then turn those quantities into a colour."'),
  ('B09', 'Material judged under stated lighting; materials unchanged across presets', 'Correct; capture keeps materials fixed', f'{CH7} consequences list; capture lights'),
  ('B10', 'Only base colour is a colour; the rest are data in image files', 'Correct', f'{CH7}: "Only the base colour is a colour. The rest are data that happen to be stored in an image file."'),
 ],
 'why-pbr-matters': [
  ('B01', 'Painting light into a texture was an older shortcut', 'Correct (general practice); demonstrated with a code-painted texture', 'tools/make_textures.py painted_sphere.png; unshaded material in capture.gd'),
  ('B02', 'Only the PBR highlight follows a moving light', 'Correct; shown in the render', 'capture painted_orbit'),
  ('B03', 'Painted sphere ignores time-of-day lighting', 'Correct; unshaded material ignores lights', 'capture painted_daynight; Godot SHADING_MODE_UNSHADED'),
  ('B04', 'PBR materials look correct regardless of lighting conditions', 'Correct; attributed source', 'https://learnopengl.com/PBR/Theory: "these materials will look correct regardless of lighting conditions"; capture three'),
  ('B05', 'Energy conservation: outgoing light never exceeds incoming; rougher = wider, dimmer highlight', 'Correct; measured in Godot', 'https://learnopengl.com/PBR/Theory: "outgoing light energy should never exceed the incoming light energy"; evidence/profiles.json'),
  ('B06', 'Blender material crosses glTF as metallic-roughness and arrives as StandardMaterial3D', 'Correct; tested in the course worked example', f'{CH3} line 93'),
  ('B07', 'A Godot material saved as text is a list of values', 'Correct; real output', 'evidence/materials/gold.tres written by tools/save_materials.gd'),
  ('B08', 'With nothing to reflect, a metal looks like dark plastic', 'Correct; shown in the render', f'{CH7}: "A rough metal looks like plastic without something to reflect."; capture metal_sky'),
 ],
 'pbr-textures-are-data': [
  ('B01', 'A PBR material is a set of maps, one per measurement', 'Correct', f'{CH7}; capture stack'),
  ('B02', 'Only the base colour map is a colour', 'Correct', f'{CH7}: "Only the base colour is a colour."'),
  ('B03', 'Tiles hold about 0.3 roughness, grout 0.9', 'Correct; read from the file', 'textures/tiles_roughness.png via textures.json'),
  ('B04', 'Roughness map makes the shine vary across the surface', 'Correct; shown in the render', 'capture roughmap'),
  ('B05', 'Lighting depends on the angle between normal and light', 'Correct (Lambert N·L)', f'{CH7} N·L worked example'),
  ('B06', 'Normal map RGB = XYZ; flat texel (128,128,255); normal maps pale blue', 'Correct', f'glTF 2.0 normal texture rule quoted in {CH7}; chapter flat texel (128,128,255)'),
  ('B07', 'Normal map changes lighting, not geometry', 'Correct', 'Godot docs: "This does not modify geometry, only the incident angle for light."'),
  ('B08', 'Poly Haven ARM: R=AO, G=roughness, B=metallic; ORMMaterial3D reads the same order', 'Correct', f'{CH7} ORM channel order (material.cpp at 4.7.2)'),
  ('B09', '128/255 = 0.502 decodes to 0.216; flat normal tilts 38.8°', 'Correct; recomputed', f'{CH7} "Colour versus data"; evidence/decode-check.txt'),
  ('B10', 'Same flat normal map read as colour lights the sphere off-centre', 'Correct; shown in the render', 'capture decode (two ShaderMaterials differing only in hint_normal vs source_color)'),
 ],
}


def paperwork(d, reel, B, rows):
    title = d['title']
    (reel / 'NARRATION.md').write_text('# ' + title + '\n\n' + '\n\n'.join('## ' + b['beat_id'] + '\n\n' + b['narration_text'] for b in B) + '\n')
    acts = {}
    for bid, act, *_ in rows:
        acts.setdefault(act, []).append(bid)
    (reel / 'ACTS.md').write_text(
        f'# {title}\n\nLearning objective: {d["objective"]}\n\nThis is a topic film inside the CSYE 7270 course playlist, built with the lecture skill in the same topic-film form as the Godot shader films (Bear asked for "films on PBR and why PBR is important", 2026-11-13; PBR is OFF the exam, this is class material).\n\n'
        f'Source: {CH7}, section "A PBR material is a set of measurements, not a picture" and the sections it leans on; deck {DECK} slides 3 and 4.\n\n'
        'Opening: narrated portrait/title card, the corrected misconception, prerequisite terms.\n\n'
        + '\n'.join(f'Act — {a}: {", ".join(v)}' for a, v in acts.items())
        + '\n\nClosing: four-line recap, Your Turn exercise with two checks, exact-title outro.\n\n'
        'Cast: the same terracotta sphere family, the same tile texture set and the same three lighting presets (noon, sunset, dim blue room) across all three PBR films; all renders come from one Godot rig, '
        f'{HERE}.\n\nCoverage note: these are topic films, not a whole-chapter lecture. LEFT OUT on purpose: texture import settings, decals, global illumination techniques, attribution, the ship audit; none is needed to say what PBR is or why it matters. No Godot shading-language code is shown (not examined in the course).\n')
    (reel / 'SHOTLIST.md').write_text(
        '# Shot decisions\n\nLibrary checked: ShaderLab (layout "video"), CCPlainShell, BrutalistHesitantWriter, ClaudeDefinitions, ClaudeVerdictArtifact, ClaudeComposerAsk and ClaudeTitleOutro are registered. '
        'Every material beat shows a real Godot 4.7.2 render made for this film (SHOW-THE-THING: Godot shown as itself); concept beats that have no picture in the engine are Manim.\n\n'
        '| Beat | About | Lane picked | Runner-up | Why this one wins |\n|---|---|---|---|---|\n'
        + '\n'.join(f'| {bid} | {intent} | {lane} | {runner} | ' + ('The claim is how a real material looks; only a real render proves it.' if kind == 'cap' else 'The file text is the evidence; a picture of it would add nothing.' if kind == 'shell' else 'The idea is a mechanism or a set of numbers with no on-screen object in Godot; a transform shows it moving.') + ' |'
                    for bid, act, intent, lane, runner, kind, ref in rows) + '\n')
    (reel / 'FACTCHECK.md').write_text(
        f'# Fact check — {title}\n\n| # | Beat | Claim | Verdict | Source | Fix |\n|---|---|---|---|---|---|\n'
        + '\n'.join(f'| {i + 1} | {bid} | {c} | {v} | {s} | none |' for i, (bid, c, v, s) in enumerate(FACTS[d['slug']]))
        + '\n\nNothing datable (no prices, versions beyond Godot 4.7.2 on the capture label, or dates) is spoken. Sources checked 2026-11-13.\n')
    (reel / 'SOURCES.md').write_text(
        f'# Sources\n\n- Chapter: {CH7}\n- Chapter 3 (Blender to Godot over glTF): {CH3}\n- Deck: {DECK}, slides 3 and 4\n'
        '- Godot Standard Material 3D docs: https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html (checked 2026-11-13)\n'
        '- LearnOpenGL, PBR Theory: https://learnopengl.com/PBR/Theory (checked 2026-11-13)\n'
        f'- Evidence rig (Godot 4.7.2 project, capture script, code-made textures, logs): {HERE}\n\n'
        'All textures are code-authored by tools/make_textures.py; no downloaded or AI-generated images. No paid services.\n')
    (reel / 'PROMPTS.md').write_text('# Generation prompts\n\nNo generation prompts. Free local Kokoro narration, Manim, Remotion and real Godot renders.\n')
    kinds = [r[5] for r in rows]
    (reel / 'CHECKS-REPORT.md').write_text(
        f'# Authoring checks\n\n{len(rows)} body SHOW beats; 0 HOLD; 0 PUNT.\n\nLane histogram (information, not a quota): '
        f'{kinds.count("cap")} real Godot renders (ShaderLab), {kinds.count("manim")} Manim, {kinds.count("shell")} real shell output; 6 bookends.\n\n'
        'Teaching arc: misconception corrected (BIDEA) → prerequisites (BDEFS) → mechanism shown on real renders → limit or consequence → recap → scaffolded task with two checks.\n')
    log = reel / 'BUILD-LOG.md'
    if not log.exists():
        log.write_text(f'# Build log — {title}\n\n2026-11-13: authored by the PBR films session from {CH7} and the deck; Bear approved the three-film set ("Build all three"). '
                       f'Playlist set to the existing course playlist "{PLAYLIST}" instead of the "Materials and PBR in Godot" series name floated in the plan, so no new series is invented. '
                       f'Estimated runtime {sum(b["estimated_duration_s"] for b in B):.0f} s before audio.\n')
    (reel / 'make_sheet.py').write_text(
        f"#!/usr/bin/env python3\nimport subprocess, sys\nsubprocess.run([sys.executable, {str(HERE / 'prepare_pbr_films.py')!r}, {d['slug']!r}], check=True)\n")


if __name__ == '__main__':
    want = sys.argv[1:]
    for d in FILMS:
        if want and d['slug'] not in want:
            continue
        reel, B = build(d)
        print(reel.name, len(B), 'beats', round(sum(b['estimated_duration_s'] for b in B)), 's est')
