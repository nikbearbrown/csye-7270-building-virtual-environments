#!/usr/bin/env python3
"""Apply the instructor's Fall 2026 corrections without rebuilding the DOCX.

Run with the bundled document runtime. Writes a separate candidate and audit;
never overwrites the input. Original styles, fonts, numbering and boilerplate
are retained. This is a course-specific migration, not an AI1 toolkit file.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

from lxml import etree as E

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PKG = 'http://schemas.openxmlformats.org/package/2006/relationships'
NS = {'w': W, 'r': R}
POLICY = 'https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz'


def q(name):
    return '{%s}%s' % (W, name)


def text(el):
    return ''.join(el.xpath('.//w:t/text()', namespaces=NS))


def setting(parent, name, value='1'):
    el = parent.find(q(name))
    if el is None:
        el = E.SubElement(parent, q(name))
    el.set(q('val'), value)
    return el


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('source', type=Path)
    ap.add_argument('candidate', type=Path)
    ap.add_argument('--audit', required=True, type=Path)
    args = ap.parse_args()
    assert args.source.resolve() != args.candidate.resolve(), 'Use a separate candidate'
    source_bytes = args.source.read_bytes()
    with ZipFile(args.source) as z:
        parts = {i.filename: z.read(i.filename) for i in z.infolist()}
        infos = z.infolist()
    root = E.fromstring(parts['word/document.xml'])
    body = root.find('w:body', NS)
    original = list(body)
    frozen = [E.tostring(p) for p in original]
    assert len(original) == 259, 'Unexpected syllabus version; review before editing'
    assert text(original[24]).endswith('Students choose Unity or Unreal; Walker supports both.')
    assert text(original[175]) == 'Collaboration Policy'
    rels = E.fromstring(parts['word/_rels/document.xml.rels'])
    changes = []
    body_rpr = copy.deepcopy(original[23].find('w:r/w:rPr', NS))

    def run(content, kind='plain', template=None):
        r = E.Element(q('r'))
        rp = copy.deepcopy(template if template is not None else body_rpr)
        if kind in ('bold', 'italic'):
            setting(rp, 'b' if kind == 'bold' else 'i')
            setting(rp, 'bCs' if kind == 'bold' else 'iCs')
        r.append(rp)
        t = E.SubElement(r, q('t'))
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        t.text = content
        return r

    def fill(p, content, template=None):
        for child in list(p):
            if child.tag != q('pPr'):
                p.remove(child)
        chunks = [content] if isinstance(content, str) else content
        for item in chunks:
            if isinstance(item, tuple):
                kind, words = item
            else:
                kind, words = 'plain', item
            p.append(run(words, kind, template))
        return p

    def replace(i, content, preserve_run_style=False):
        p = original[i]
        before = text(p)
        rp = p.find('w:r/w:rPr', NS) if preserve_run_style else None
        fill(p, content, rp)
        changes.append({'original_block': i, 'before': before, 'after': text(p)})

    def substitute(i, old, new):
        p = original[i]
        before = text(p)
        for t in p.iter(q('t')):
            if old in (t.text or ''):
                t.text = t.text.replace(old, new)
                changes.append({'original_block': i, 'before': before, 'after': text(p)})
                return
        raise AssertionError(f'No single-run match at {i}: {old}')

    def paragraph(content, template=23):
        p = copy.deepcopy(original[template])
        p.attrib.clear()
        rp = p.find('w:r/w:rPr', NS) if template != 23 else None
        return fill(p, content, rp)

    def add_after(i, paragraphs):
        at = body.index(original[i]) + 1
        for p in paragraphs:
            body.insert(at, p)
            at += 1
            changes.append({'added_after_original_block': i, 'text': text(p)})

    def link_paragraph(label, url, prefix=''):
        p = paragraph(prefix)
        rid = 'rIdSyllabus' + str(len(rels) + 1)
        E.SubElement(rels, '{%s}Relationship' % PKG, {
            'Id': rid, 'Type': R + '/hyperlink', 'Target': url, 'TargetMode': 'External'})
        h = E.SubElement(p, q('hyperlink'), {'{%s}id' % R: rid})
        r = run(label)
        rp = r.find(q('rPr'))
        setting(rp, 'color', '0000FF')
        setting(rp, 'u', 'single')
        h.append(r)
        return p

    # Term, learning model and the first three modules.
    replace(2, 'Course Syllabus — Fall 2026', True)
    substitute(24, 'Students choose Unity or Unreal; Walker supports both.',
               'All students use Walker with Godot and GDScript.')
    replace(27, "Claude Code helps write and revise GDScript; you remain responsible for understanding and verifying it. Your job is to audit whether the output is plausible, decide what the problem actually is before the agent sees it, sequence the work, supply game-specific meaning, and hold the session toward one coherent goal. Walker calls these the Five Supervisory Capacities — PA, PF, TO, IJ, EI — and you will use this vocabulary throughout the semester, including in submissions:")
    replace(46, 'Recognize the "dangerous middle" — changes requiring human inspection, such as Godot resource paths, UIDs, scene references, exported properties, and behavior that can only be judged by playing the build')
    replace(47, 'Run the Walker production cycle: Game brief → Build → Playtest → Inspect → Revise → Export. State acceptance criteria, review changes, and do not treat a successful build as proof of good gameplay.')
    replace(49, 'There will be a 100-point assignment every 10 days, creating small games, tools, 3D simulations, or virtual environments. There will be a group project and an individual project. Canvas will publish the assignment deadlines and project milestones.')
    replace(50, 'The course begins with the walker-jumpman starter: change its main character and extend its playable level. Week 2 develops prompted game art; Week 3 connects Blender MCP to an asset workflow for Godot. Later work retains rendering, collision, physics, shaders, particles, animation, audio, game AI, profiling, analytics, procedural content, and appropriate networking, mobile, and XR applications — all through Walker and Godot.')
    add_after(50, [paragraph([('bold', 'Predict → Build It → Use It → Ship It → Verify. '), 'Predict the behavior before prompting; build a focused change; use it in the running game; ship a reproducible version and explainer; verify the claims with evidence. The AI can generate code and assets. The human sets the intent, playtests, judges results, and accepts or rejects the work.'])])
    replace(53, 'Each course module maps one-to-one to a chapter in the companion book. Modules and chapters will be released incrementally, one or two per week; assignment deadlines follow a separate 10-day cadence. The sequence below is the Fall 2026 teaching plan. Every assignment includes a Brutalist Godot explainer; selected films will be viewed and discussed in class.')

    schedule = [
        ['Wk.', 'Engine/Concept Focus', 'Walker / CLI Practice', 'Capacity', 'Notes'],
        ['1', 'Walker + Godot starter', 'Inspect walker-jumpman. Change its main character; extend and playtest the level.', 'PF / PA', 'Brief, baseline, revision, gameplay explainer.'],
        ['2', 'Prompting game art', 'Create and compare art with available Gemini, ChatGPT, Midjourney, or similar tools. Import into Godot.', 'TO / IJ', 'Record prompts, provenance, and readability checks.'],
        ['3', 'Blender MCP → Godot', 'Prompt Blender through the community MCP integration. Inspect geometry, scale, materials, and export.', 'TO / PA', 'Verify the imported asset in the game.'],
        ['4', 'Scenes, collision & physics', 'Trace inputs, nodes, signals, movement, and collisions. Test one focused change at a time.', 'PF / PA', '2D/3D mechanics and scene ownership.'],
        ['5', 'GDD & virtual worlds', 'Refine the brief into a GDD. Build a small 3D interaction with measurable acceptance criteria.', 'PF / IJ', 'Scope mobile, network, and XR applications.'],
        ['6', 'Shader foundations', 'Write project context in CLAUDE.md. Specify a visible effect and its boundaries before coding.', 'PF', 'Explain the shader mechanism in Godot.'],
        ['7', 'Materials & textures', 'Prompt or source textures, then inspect material settings, lighting, and asset attribution.', 'TO', 'Judge the material in the running scene.'],
        ['8', 'Shader verification', 'Review a plausible but incorrect shader change. Compare controlled inputs and observed output.', 'PA', 'Show evidence, not just a successful compile.'],
        ['9', 'Particle effects', 'Build Godot particle effects; tune timing, emission, motion, and performance.', 'TO', 'Separate visual intent from measured cost.'],
        ['10', 'Animation foundations', 'Establish behavior checks before changing animation tracks, timing, or transitions.', 'EI', 'Brutalist game-development explainer.'],
        ['11', 'Animation & interaction', 'Connect animation states to player actions. Use motion references and test blends and edge cases.', 'IJ', 'Check feel and readability through play.'],
        ['12', 'Audio & triggers', 'Import licensed or generated audio. Trace trigger logic, levels, and restart behavior.', 'PA', 'Disclose sources; verify actual playback.'],
        ['13', 'Profiling & optimization', 'Measure frame cost and analytics. Compare a baseline with one justified optimization.', 'EI', 'Include relevant mobile/XR constraints.'],
        ['14', 'Game AI & systems', 'Sequence navigation, behavior-tree, and procedural-content tasks with explicit handoffs.', 'TO', 'Test state, failure, and scoped networking.'],
        ['15', 'Final projects', 'Review the full brief-to-export cycle. Reproduce the build and defend its design and evidence.', 'All five', 'Final Brutalist films and class discussion.'],
    ]
    table = original[54]
    before_table = text(table)
    for ri, (row, words) in enumerate(zip(table.findall('w:tr', NS), schedule)):
        rp = row.find(q('trPr'))
        setting(rp, 'cantSplit')
        setting(rp, 'tblHeader', '1' if ri == 0 else '0')
        for cell, value in zip(row.findall('w:tc', NS), words):
            p = cell.find(q('p'))
            for el in list(cell):
                if el.tag != q('tcPr') and el is not p:
                    cell.remove(el)
            fill(p, [('bold', value)] if ri == 0 else value)
            pp = p.find(q('pPr'))
            # Retain type, widths, cell margins and row spacing; avoid stretched
            # words in narrow cells and repeat the header on continued pages.
            setting(pp, 'jc', 'left')
    changes.append({'original_block': 54, 'before': before_table, 'after': text(table)})

    replace(57, 'Required engine: the regular Godot Engine with GDScript. The starter does not require the .NET edition, C#, Unity, Unreal, or Houdini.')
    body.replace(original[58], link_paragraph('Download Godot Engine', 'https://godotengine.org/download/', 'Godot: '))
    body.replace(original[59], link_paragraph('walker-jumpman starter project', 'https://github.com/nikbearbrown/walker-jumpman', 'Course starter: '))
    replace(60, 'Install the course-specified Godot version and matching export templates when needed. Open the starter’s godot/project.godot. Learn both the editor and the command-line build/test workflow; do not substitute legacy engine-specific instructions.')
    body.replace(original[61], link_paragraph('Brutalist video toolkit', 'https://github.com/nikbearbrown/brutalist.art', 'Required for assignment explainers: '))
    body.replace(original[62], link_paragraph('Blender downloads', 'https://www.blender.org/download/', 'Blender is required from Week 3: '))
    add_after(60, [link_paragraph('Blender MCP (community project)', 'https://github.com/ahujasid/blender-mcp', 'Week 3 integration: ')])
    replace(63, 'Walker supplies the game brief, GDD, and agent-guided build/playtest/revision workflow. Use the Godot course materials; older Unity/Unreal documentation is not the setup for this course. Walker prompting assistants for game art are planned additions, not prerequisites that already exist.')
    add_after(63, [link_paragraph('Walker project', 'https://github.com/nikbearbrown/walker')])
    replace(64, 'Claude Code is required; setup and access checks are covered in Week 1. Exercises assume a working Claude Code account through the course’s NEU access arrangements. Check access early and contact the instructor if it is unavailable. Separate API credits are not a prerequisite for the starter work.')
    add_after(64, [link_paragraph('Northeastern Claude access', 'https://claude.northeastern.edu/', 'NEU’s Claude site describes institutional access and sign-in: '), paragraph('Game-art tools may include Gemini, ChatGPT, Midjourney, or available alternatives. Use tools you can access, document asset provenance and terms, and do not assume a paid subscription is required to meet the learning objective.')])
    replace(68, 'The course strongly emphasizes developing and communicating practical skills in virtual environments, Godot game development, and AI-assisted production.')
    replace(81, 'Learning outcomes are developed through practice and demonstrated in graded assignments and term projects:')
    replace(82, 'Ungraded practice exercises and quizzes, called Assessments')
    replace(83, '100-point assignments every 10 days, including implementation and a required Brutalist Godot explainer')
    replace(89, 'A point system is used for grading. Each assignment is worth 100 points and is due every 10 days. Canvas provides exact deadlines and project milestones. The assignment rubric is 60 / 10 / 10 / 20, as follows:')

    # Concise rubric with the original syllabus's body and emphasis formatting.
    add_after(89, [
        paragraph([('bold', 'Implementation and substantive explanation — 60 points. '), 'Complete the assigned work and explain it through the required Brutalist Godot film. Correctness, demonstrated mechanisms, reproducible evidence, and stated limitations carry the credit. The assignment specifies the detailed criteria within these 60 points.']),
        paragraph([('bold', 'Frictional (honest learning log) — 10 points. '), 'In FRICTIONAL.md, record your prediction, attempts, obstacles, changes, results, and next test. Include a concrete instance of struggle or revision and what you learned. An honest record of effort is not a timesheet, commit-count contest, or performance of suffering.']),
        paragraph([('bold', 'GitHub version posting matching Canvas — 10 points. '), 'Post the source and documentation, identify the submitted commit hash, and link the same version and accessible rendered film in Canvas. Explain your changes from the starter and distinguish human contributions from AI contributions.']),
        paragraph([('bold', 'Relative Quartile — 20 points. '), 'The instructor and TAs review the full comparison group before assigning these points. Meeting the stated criterion-based requirements can earn 80 points; it does not guarantee the remaining 20. See Quality Expectations and Grading below.']),
        paragraph('Total: 100 points. The required explainer is part of the 60-point implementation/explanation category, not a fifth points category. The final course letter-grade policy below is separate from the assignment-level Relative Quartile.'),
    ])
    substitute(108, 'LastName_FirstName_Assignment_#.zip', 'LastName_FirstName_CSYE7270_Assignment_#.zip')
    replace(111, 'Assignments MUST estimate the share of code written by the student versus AI or other external sources, and identify the actual contributions in SOURCES.md.')
    replace(112, 'Assignments MUST identify licenses and sources for code, art, audio, and film assets in the README or SOURCES.md; notebooks, when submitted, must also specify their license.')
    add_after(113, [
        paragraph([('bold', 'Film as code. '), 'GitHub holds game source, film source, beat sheets, scripts/prompts, README.md, SOURCES.md, FRICTIONAL.md, and reproducible build/test instructions. MP3/MP4 and files over 25 MB belong in Drive or designated media storage, linked from GitHub. Exclude secrets and unnecessary private chats.']),
        paragraph('Canvas must include the required submission files, the GitHub repository/folder URL, the final commit hash, and an accessible link to the matching rendered film. A beat sheet alone does not satisfy the video requirement. No public YouTube upload or additional vertical version is required unless an assignment explicitly requests it.'),
        paragraph('Use meaningful commits at learning milestones: prediction or plan; focused change; test result; revision. State what changed, why, what you observed, and what remains unverified. Keep detailed attempts in FRICTIONAL.md and human/AI attribution in SOURCES.md; do not invent activity or claim tests you did not run.'),
        paragraph('Required Brutalist Godot Explainers', template=124),
        paragraph('Every assignment must include a rendered explainer using the appropriate Brutalist Godot skill. The assignment determines coverage; three available skills do not mean three films are required for every submission.'),
        paragraph([('bold', 'godot-walkthrough '), '(alias of godot-waikthrough): show the implemented game through real gameplay, controls, feature outcomes, and failure/recovery.']),
        paragraph([('bold', 'godot-gamedev: '), 'walk through the actual code, scenes, resources, assets/art, and tests. Show an input → state → output trace.']),
        paragraph([('bold', 'godot-gdd: '), 'explain the design document using game evidence; distinguish proposed, built, tested, and human-reviewed features.']),
        paragraph('Ask Claude Code to read and follow the installed skill; these are agent-driven workflows, not a standalone Walker shell command. The optional walker modifier adds the prompt opening, built-result summary, Verdict, Your Turn, and regular outro. Use it when the assignment requests it or it clarifies the process.'),
        paragraph('A sufficient film explains the concept correctly; shows the mechanism with motion, a worked example, or real output; uses reproducible numbers and labels constructed or reconstructed views; and names something the evidence does not establish. Watch and verify the rendered film. Use the skill’s native 4K landscape workflow and regular outro. If a Short is requested, it must be a separate native 9:16 cut under 3:00.'),
    ])
    replace(115, 'Due Dates: Assignments are due every 10 days, at 11:59 PM on the date posted in Canvas.')
    replace(117, 'Late submissions incur a 10% deduction per day, rounded up.')
    replace(125, [('bold', 'Use of AI in Assignments. '), 'Claude Code is part of the Walker/Godot workflow, and Brutalist is required for assignment explainers. AI may help with the game, GDD, script, beat sheet, code, and build. You remain responsible for the submission and must document its contributions in SOURCES.md. Other AI tools may be used subject to the same requirements.'])
    add_after(125, [link_paragraph('AI Policy for Professor Bear’s Courses | Using AI Responsibly in Class', POLICY, 'Required viewing: ')])
    replace(131, 'Students must be able to explain any part of the submitted game, GDD, code, assets, beat sheet, video, and build, including AI-generated content')
    replace(133, 'Inability to explain your submission reduces points under the relevant criteria. Misrepresenting what was run or verified is an academic integrity matter under the course AI policy')
    replace(139, 'Include the following labor-separation disclosure in SOURCES.md, alongside attribution to the walker-jumpman starter, third-party assets, and your substantive changes:')
    replace(141, 'Stage reached: [Game brief / Build / Playtest / Inspect / Revise / Export]')
    replace(142, 'AI did: [tools used; code, assets, text, or tests generated; what you delegated]')
    replace(143, 'Human did: [intent, direct contributions, playtesting, inspection, revisions, and acceptance/rejection decisions]')
    replace(145, 'Specific instance: [a concrete moment this capacity mattered; for example,')
    replace(146, '  "Claude Code changed the character appearance, but the collision shape')
    replace(147, '  no longer matched. I reproduced the mismatch in Godot, directed a fix,')
    replace(148, '  and replayed the collision test — that is Plausibility Auditing."]')
    replace(149, 'This disclosure belongs to the existing rubric, not an additional points category. SOURCES.md identifies contributions; FRICTIONAL.md records the honest learning process and evidence, including unresolved failures.')
    replace(165, 'Every 100-point assignment includes a Relative Quartile component worth 20 points (20%). The instructor and TAs assign it after reviewing the full comparison group, with emphasis on:')
    replace(166, 'Specificity, originality, and substantive improvement beyond the starter or an unexamined AI response')
    replace(167, 'Demonstrated understanding and evidence that you actually ran, tested, or clearly labeled a simulation of the workflow')
    replace(168, 'Meaningful customization and honesty about what is and is not verified')
    replace(169, 'Usability, relevant application, and professional communication')
    replace(170, 'Relative Quartile Score Breakdown (20 points)', True)
    replace(171, [('italic', 'Bottom 25% (5 points):'), ' Work in the lowest quarter of the comparison group, with limited specificity, substantive improvement, demonstrated understanding, or verification evidence.'])
    replace(172, [('italic', '26th–50th percentile (10 points):'), ' Work in the next quarter, with clear implementation, relevant customization, and a defensible explanation, but less complete evidence or refinement than higher-ranked submissions.'])
    replace(173, [('italic', '51st–75th percentile (15 points):'), ' Work in the next quarter, with strong implementation, reproducible tests, meaningful improvements, clear limitations, and effective communication.'])
    replace(174, [('italic', 'Top 25% (20 points):'), ' Work in the highest quarter, distinguished by substantive improvement, depth of understanding, convincing evidence, honest verification, usability, and professional communication.'])
    add_after(174, [paragraph('Production polish counts only as professional communication. It does not substitute for a correct explanation: a plain film that teaches precisely can outrank a beautiful one that does not. AI assistance does not remove the requirement to understand and defend your work.')])

    # Pagination repair only: keep headings with their following paragraphs.
    # This does not change boilerplate wording, fonts, spacing, or style IDs.
    for p in body.findall('w:p', NS):
        pp = p.find(q('pPr'))
        if pp is None:
            continue
        sty = pp.find(q('pStyle'))
        if sty is not None and sty.get(q('val'), '').startswith('Heading'):
            setting(pp, 'keepNext')
    for i in [89, 99, 102, 116, 130, 134, 138, 140, 145, 146, 147, 151, 155, 159, 170, 177]:
        setting(original[i].find(q('pPr')), 'keepNext')
    for row in original[100].findall('w:tr', NS)[:-1]:
        for p in row.findall('.//w:p', NS):
            setting(p.find(q('pPr')), 'keepNext')

    # Compare complete protected XML after ignoring keepNext pagination flags.
    # No boilerplate paraphrasing or typography changes are allowed.
    preserved = list(range(3,23)) + list(range(93,105)) + list(range(175,259))
    for i in preserved:
        before = E.fromstring(frozen[i])
        after = copy.deepcopy(original[i])
        for p in [before, after]:
            for el in p.xpath('.//w:pPr/w:keepNext', namespaces=NS):
                el.getparent().remove(el)
        assert E.tostring(before, method='c14n', exclusive=True) == E.tostring(after, method='c14n', exclusive=True), f'Protected block changed: {i}'
    all_text = text(root)
    for required in ['Fall 2026', '100-point assignment every 10 days', 'Frictional', '60 points', 'Relative Quartile', 'godot-gdd', 'godot-gamedev', 'godot-walkthrough', 'FRICTIONAL.md', 'SOURCES.md', 'Blender MCP', 'Predict → Build It → Use It → Ship It → Verify']:
        assert required in all_text, f'Missing: {required}'
    assert '5% deduction' not in all_text
    assert 'Unreal Reels' not in all_text
    assert 'DontDestroyOnLoad' not in all_text
    assert 'weekly assignments' not in all_text
    assert all_text.count('Late submissions incur a 10% deduction per day, rounded up.') == 2
    assert 60 + 10 + 10 + 20 == 100
    parts['word/document.xml'] = E.tostring(root, encoding='UTF-8', xml_declaration=True, standalone=True)
    parts['word/_rels/document.xml.rels'] = E.tostring(rels, encoding='UTF-8', xml_declaration=True, standalone=True)
    args.candidate.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(args.candidate, 'w') as z:
        for info in infos:
            z.writestr(info, parts[info.filename])
    with ZipFile(args.source) as old, ZipFile(args.candidate) as new:
        changed_parts = [k for k in old.namelist() if old.read(k) != new.read(k)]
    assert changed_parts == ['word/document.xml', 'word/_rels/document.xml.rels']
    audit = {
        'source': str(args.source.resolve()), 'candidate': str(args.candidate.resolve()),
        'source_sha256': hashlib.sha256(source_bytes).hexdigest(),
        'candidate_sha256': hashlib.sha256(args.candidate.read_bytes()).hexdigest(),
        'changed_zip_parts': changed_parts,
        'institutional_and_collaboration_blocks_unchanged_except_keepNext': list(range(175,259)),
        'final_letter_grade_blocks_unchanged_except_keepNext': list(range(93,105)),
        'pagination_only_keepNext_changes': [i for i in preserved if E.tostring(original[i]) != frozen[i]],
        'unchanged_styles_fonts_numbering_theme_and_sections': True,
        'schedule_rows': len(schedule), 'policy_url': POLICY,
        'render_review': 'PENDING', 'human_approval': False, 'changes': changes,
    }
    args.audit.parent.mkdir(parents=True, exist_ok=True)
    args.audit.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k:v for k,v in audit.items() if k != 'changes'}, indent=2))


if __name__ == '__main__':
    main()
