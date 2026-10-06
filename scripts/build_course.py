#!/usr/bin/env python3
"""Build the CSYE 7270 Canvas course from the Markdown/JSON sources.

Two outputs, both generated, both local-only (see .gitignore):

  canvas/paste/*.html          one Canvas-safe HTML fragment per page and assignment,
                               for pasting into Canvas's HTML editor by hand
  canvas/package/*.imscc       an importable Canvas cartridge: modules, pages, assignments,
                               ungraded practice quizzes, syllabus, late policy

Usage (from the course root):
  python3 scripts/build_course.py                 # build everything (fails on a missing source)
  python3 scripts/build_course.py --partial       # skip sources that do not exist yet (for testing)
  python3 scripts/build_course.py --state published
  python3 scripts/build_course.py --check         # build, then run the integrity check only

Needs: Python 3, pandoc. Nothing from the old Spring 2026 export is copied: no media, no
Unity/Unreal assignments, no quizzes, no enrollment data.

The cartridge was modeled on the old export's XML, but it has NOT been import-tested in a live
Canvas; see canvas/README.md.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import zipfile
from xml.sax.saxutils import escape

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPO = "https://github.com/nikbearbrown/csye-7270-building-virtual-environments"
COURSE_TITLE = "CSYE 7270 Virtual Environments and Real-Time 3D - Fall 2026 (Godot, Walker, Claude Code)"
COURSE_CODE = "CSYE7270.FALL2026.GODOT"
BUILD_DATE = "2026-10-06"
SYLLABUS_DOCX = "CSYE_7270_Virtual_Environments_and_Real-Time_3D.docx"
OUT_PASTE = os.path.join(ROOT, "canvas", "paste")
OUT_PKG = os.path.join(ROOT, "canvas", "package")
IMSCC_NAME = "csye7270-fall-2026-godot-walker.imscc"

# --------------------------------------------------------------------------------------
# The course structure. Edit here to move things around.
# --------------------------------------------------------------------------------------

# (number, folder, title, week)
MODULES = [
    (0, "00-start-here", "Start Here", None),
    (1, "01-walker-and-godot", "Walker and Godot", 1),
    (2, "02-prompting-game-art", "Prompting Game Art", 2),
    (3, "03-blender-mcp-to-godot", "Blender MCP to Godot", 3),
    (4, "04-scenes-collision-and-physics", "Scenes, Collision and Physics", 4),
    (5, "05-the-gdd-and-virtual-worlds", "The GDD and Virtual Worlds", 5),
    (6, "06-shader-foundations", "Shader Foundations", 6),
    (7, "07-materials-and-textures", "Materials and Textures", 7),
    (8, "08-shader-verification", "Shader Verification", 8),
    (9, "09-particle-effects", "Particle Effects", 9),
    (10, "10-animation-foundations", "Animation Foundations", 10),
    (11, "11-animation-and-interaction", "Animation and Interaction", 11),
    (12, "12-audio-and-triggers", "Audio and Triggers", 12),
    (13, "13-profiling-and-optimization", "Profiling and Optimization", 13),
    (14, "14-game-ai-and-systems", "Game AI and Systems", 14),
    (15, "15-final-projects-brief-to-export", "Final Projects: From Brief to Export", 15),
]

# Extra lecture pages beyond lesson.md, per module folder, in order.
EXTRA_PAGES = {
    "14-game-ai-and-systems": ["labs.md"],
}

# Module 0's pages, in order, before the toolchain lesson. (source path, kind)
START_HERE_PAGES = [
    "modules/00-start-here/course-map.md",
    "prerequisites/ai-policy.md",
    "prerequisites/assessment-policy.md",
    "assignments/rubrics/100-point-assignment.md",
    "prerequisites/brutalist-godot-explainers.md",
]

# assignment number -> (source file, module number whose "Assignment" header carries it).
# Rule: an assignment appears in the FIRST module it covers, so students see the target while they learn.
ASSIGNMENTS = {
    1: ("assignments/01-extend-walker-jumpman.md", 1),
    2: ("assignments/02-generate-art-sound-music-for-your-game.md", 2),
    3: ("assignments/03-blender-prop-into-godot.md", 3),
    4: ("assignments/04-specify-and-build-a-3d-interaction.md", 5),
    5: ("assignments/05-shader-and-material.md", 6),
    6: ("assignments/06-audit-a-shader-change.md", 8),
    7: ("assignments/07-particle-effects.md", 9),
    8: ("assignments/08-animation-and-state.md", 10),
    9: ("assignments/09-audio-and-a-performance-budget.md", 12),
    10: ("assignments/10-final-project.md", 14),
}

# An assignment that covers two modules is listed again in the second one, so a student sees it
# in every module whose material it uses. (Canvas allows one assignment in several modules.)
ALSO_LISTED_IN = {3: 4, 5: 7, 8: 11, 9: 13, 10: 15}

# --------------------------------------------------------------------------------------

STATE = "unpublished"
PARTIAL = False
warnings = []
link_log = []  # (source, url) pairs rewritten to the course repo


def warn(msg):
    warnings.append(msg)
    print("WARN " + msg)


def gid(key):
    return "g" + hashlib.md5(key.encode("utf-8")).hexdigest()


def slugify(s):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.lower()).strip("-")
    return s[:80]


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def exists(path):
    return os.path.exists(os.path.join(ROOT, path))


# ----------------------------- Markdown -> Canvas-safe HTML -----------------------------

def rewrite_links(md, src):
    """Rewrite relative links to GitHub URLs, outside fenced code."""
    base = os.path.dirname(src)
    parts = re.split(r"(^```.*?^```[ \t]*$)", md, flags=re.S | re.M)
    for i in range(0, len(parts), 2):
        def fix(m):
            text, url = m.group(1), m.group(2)
            if url.startswith(("https://", "#")):
                return m.group(0)
            if "://" in url or url.startswith("mailto:"):
                raise SystemExit(f"non-https link in {src}: {url}")
            frag = ""
            if "#" in url:
                url, frag = url.split("#", 1)
                frag = "#" + frag
            target = os.path.normpath(os.path.join(base, url))
            if target.startswith(".."):
                raise SystemExit(f"link leaves the course repo in {src}: {url}")
            kind = "tree" if os.path.isdir(os.path.join(ROOT, target)) else "blob"
            new = f"{REPO}/{kind}/main/{target}{frag}"
            link_log.append((src, new))
            return f"[{text}]({new})"
        parts[i] = re.sub(r"(?<!\!)\[([^\]]*)\]\(([^)\s]+)\)", fix, parts[i])
    return "".join(parts)


def split_title(md):
    """Return (title, body_without_first_h1)."""
    lines = md.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("# "):
            return line[2:].strip(), "\n".join(lines[:i] + lines[i + 1:]).lstrip("\n")
    raise SystemExit("no H1 title found")


TABLE = '<table style="border-collapse: collapse; width: 100%; margin: 1em 0;">'


def style_html(html):
    html = html.replace("<table>", TABLE)
    html = re.sub(
        r"<th\b([^>]*)>",
        lambda m: "<th" + re.sub(r' style="[^"]*"', "", m.group(1))
        + ' style="border: 1px solid #999; padding: 0.6em; text-align: left; vertical-align: top;" scope="col">',
        html,
    )
    html = re.sub(
        r"<td\b([^>]*)>",
        lambda m: "<td" + re.sub(r' style="[^"]*"', "", m.group(1))
        + ' style="border: 1px solid #999; padding: 0.6em; text-align: left; vertical-align: top;">',
        html,
    )
    html = re.sub(
        r"<pre\b([^>]*)>",
        r'<pre\1 style="white-space: pre-wrap; overflow-wrap: anywhere; background-color: #f4f4f4; padding: 1em;">',
        html,
    )
    return html


def md_to_html(md, src):
    md = rewrite_links(md, src)
    html = subprocess.run(
        ["pandoc", "--from=gfm", "--to=html5", "--wrap=none", "--no-highlight"],
        input=md, capture_output=True, text=True, check=True,
    ).stdout
    html = style_html(html)
    if re.search(r"href=\"(?!https://|#)", html):
        raise SystemExit(f"non-https link survived in {src}")
    if re.search(r"<(?:script|iframe|img|object|embed)\b", html):
        raise SystemExit(f"disallowed element in {src}")
    return '<div style="line-height: 1.6; overflow-wrap: anywhere;">\n' + html + "</div>\n"


# ----------------------------------- Quiz -> QTI ----------------------------------------

def inline_html(text):
    out = escape(text)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    return out


def plain(text):
    return text.replace("`", "")


def qti_item(qid, i, q):
    """One multiple-choice item in Canvas's non-CC QTI dialect (feedback shown always)."""
    ans_ids = [str(1000 + i * 10 + j) for j in range(len(q["choices"]))]
    correct = ans_ids[q["answer"]]
    item_id = gid(f"{qid}:q{i}")
    labels = "\n".join(
        f'              <response_label ident="{aid}">\n                <material>\n'
        f'                  <mattext texttype="text/plain">{escape(plain(c))}</mattext>\n'
        f"                </material>\n              </response_label>"
        for aid, c in zip(ans_ids, q["choices"])
    )
    return f"""      <item ident="{item_id}" title="Question {i}">
        <itemmetadata>
          <qtimetadata>
            <qtimetadatafield>
              <fieldlabel>question_type</fieldlabel>
              <fieldentry>multiple_choice_question</fieldentry>
            </qtimetadatafield>
            <qtimetadatafield>
              <fieldlabel>points_possible</fieldlabel>
              <fieldentry>1.0</fieldentry>
            </qtimetadatafield>
            <qtimetadatafield>
              <fieldlabel>original_answer_ids</fieldlabel>
              <fieldentry>{",".join(ans_ids)}</fieldentry>
            </qtimetadatafield>
            <qtimetadatafield>
              <fieldlabel>assessment_question_identifierref</fieldlabel>
              <fieldentry>{gid(f"{qid}:aq{i}")}</fieldentry>
            </qtimetadatafield>
          </qtimetadata>
        </itemmetadata>
        <presentation>
          <material>
            <mattext texttype="text/html">{escape("<div><p>" + inline_html(q["prompt"]) + "</p></div>")}</mattext>
          </material>
          <response_lid ident="response1" rcardinality="Single">
            <render_choice>
{labels}
            </render_choice>
          </response_lid>
        </presentation>
        <resprocessing>
          <outcomes>
            <decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>
          </outcomes>
          <respcondition continue="Yes">
            <conditionvar>
              <other/>
            </conditionvar>
            <displayfeedback feedbacktype="Response" linkrefid="general_fb"/>
          </respcondition>
          <respcondition continue="No">
            <conditionvar>
              <varequal respident="response1">{correct}</varequal>
            </conditionvar>
            <setvar action="Set" varname="SCORE">100</setvar>
          </respcondition>
        </resprocessing>
        <itemfeedback ident="general_fb">
          <flow_mat>
            <material>
              <mattext texttype="text/html">{escape("<p>" + inline_html(q["feedback"]) + "</p>")}</mattext>
            </material>
          </flow_mat>
        </itemfeedback>
      </item>"""


def qti_document(qid, data, cc):
    items = "\n".join(qti_item(qid, i, q) for i, q in enumerate(data["questions"], 1))
    schema = (
        "http://www.imsglobal.org/profile/cc/ccv1p1/ccv1p1_qtiasiv1p2p1_v1p0.xsd"
        if cc else "http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd"
    )
    cc_meta = """      <qtimetadatafield>
        <fieldlabel>cc_profile</fieldlabel>
        <fieldentry>cc.exam.v0p1</fieldentry>
      </qtimetadatafield>
      <qtimetadatafield>
        <fieldlabel>qmd_assessmenttype</fieldlabel>
        <fieldentry>Examination</fieldentry>
      </qtimetadatafield>
      <qtimetadatafield>
        <fieldlabel>qmd_scoretype</fieldlabel>
        <fieldentry>Percentage</fieldentry>
      </qtimetadatafield>
""" if cc else ""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 {schema}">
  <assessment ident="{qid}" title="{escape(data["title"])}">
    <qtimetadata>
{cc_meta}      <qtimetadatafield>
        <fieldlabel>cc_maxattempts</fieldlabel>
        <fieldentry>unlimited</fieldentry>
      </qtimetadatafield>
    </qtimetadata>
    <section ident="root_section">
{items}
    </section>
  </assessment>
</questestinterop>
"""


def quiz_meta(qid, data):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<quiz identifier="{qid}" xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <title>{escape(data["title"])}</title>
  <description>{escape("<p>" + inline_html(data["description"]) + "</p>")}</description>
  <shuffle_answers>true</shuffle_answers>
  <scoring_policy>keep_highest</scoring_policy>
  <hide_results></hide_results>
  <quiz_type>practice_quiz</quiz_type>
  <points_possible>{float(len(data["questions"])):.1f}</points_possible>
  <require_lockdown_browser>false</require_lockdown_browser>
  <require_lockdown_browser_for_results>false</require_lockdown_browser_for_results>
  <require_lockdown_browser_monitor>false</require_lockdown_browser_monitor>
  <lockdown_browser_monitor_data></lockdown_browser_monitor_data>
  <show_correct_answers>true</show_correct_answers>
  <anonymous_submissions>false</anonymous_submissions>
  <could_be_locked>false</could_be_locked>
  <disable_timer_autosubmission>false</disable_timer_autosubmission>
  <allowed_attempts>-1</allowed_attempts>
  <one_question_at_a_time>false</one_question_at_a_time>
  <cant_go_back>false</cant_go_back>
  <available>{"true" if STATE == "published" else "false"}</available>
  <one_time_results>false</one_time_results>
  <show_correct_answers_last_attempt>false</show_correct_answers_last_attempt>
  <only_visible_to_overrides>false</only_visible_to_overrides>
  <module_locked>false</module_locked>
  <assignment_overrides>
  </assignment_overrides>
</quiz>
"""


# ------------------------------------ Canvas files --------------------------------------

def wiki_html(title, ident, body):
    return f"""<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>{escape(title)}</title>
<meta name="identifier" content="{ident}"/>
<meta name="editing_roles" content="teachers"/>
<meta name="workflow_state" content="{"active" if STATE == "published" else "unpublished"}"/>
<meta name="editor_type" content="rce"/>
</head>
<body>
{body}</body>
</html>
"""


def assignment_xml(ident, title, group_id, position, points=100.0):
    wf = "published" if STATE == "published" else "unpublished"
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<assignment identifier="{ident}" xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <title>{escape(title)}</title>
  <time_zone_edited>Eastern Time (US &amp; Canada)</time_zone_edited>
  <due_at/>
  <lock_at/>
  <unlock_at/>
  <module_locked>false</module_locked>
  <assignment_group_identifierref>{group_id}</assignment_group_identifierref>
  <workflow_state>{wf}</workflow_state>
  <assignment_overrides>
  </assignment_overrides>
  <allowed_extensions></allowed_extensions>
  <has_group_category>false</has_group_category>
  <points_possible>{points:.1f}</points_possible>
  <grading_type>points</grading_type>
  <all_day>false</all_day>
  <submission_types>online_upload,online_text_entry</submission_types>
  <position>{position}</position>
  <turnitin_enabled>false</turnitin_enabled>
  <vericite_enabled>false</vericite_enabled>
  <peer_review_count>0</peer_review_count>
  <peer_reviews>false</peer_reviews>
  <automatic_peer_reviews>false</automatic_peer_reviews>
  <anonymous_peer_reviews>false</anonymous_peer_reviews>
  <grade_group_students_individually>false</grade_group_students_individually>
  <freeze_on_copy>false</freeze_on_copy>
  <omit_from_final_grade>false</omit_from_final_grade>
  <hide_in_gradebook>false</hide_in_gradebook>
  <intra_group_peer_reviews>false</intra_group_peer_reviews>
  <only_visible_to_overrides>false</only_visible_to_overrides>
  <post_to_sis>false</post_to_sis>
  <moderated_grading>false</moderated_grading>
  <grader_count>0</grader_count>
  <grader_comments_visible_to_graders>true</grader_comments_visible_to_graders>
  <anonymous_grading>false</anonymous_grading>
  <graders_anonymous_to_graders>false</graders_anonymous_to_graders>
  <grader_names_visible_to_final_grader>true</grader_names_visible_to_final_grader>
  <anonymous_instructor_annotations>false</anonymous_instructor_annotations>
  <lockdown_browser_settings>{{"require_lockdown_browser":false}}</lockdown_browser_settings>
  <post_policy>
    <post_manually>false</post_manually>
  </post_policy>
</assignment>
"""


NS = ('xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
      'xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd"')


def course_settings_xml(course_id):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<course identifier="{course_id}" {NS}>
  <title>{escape(COURSE_TITLE)}</title>
  <course_code>{COURSE_CODE}</course_code>
  <start_at/>
  <conclude_at/>
  <allow_student_wiki_edits>false</allow_student_wiki_edits>
  <syllabus_course_summary>true</syllabus_course_summary>
  <lock_all_announcements>false</lock_all_announcements>
  <allow_student_organized_groups>true</allow_student_organized_groups>
  <default_view>modules</default_view>
  <usage_rights_required>false</usage_rights_required>
  <homeroom_course>false</homeroom_course>
  <conditional_release>false</conditional_release>
  <grading_standard_enabled>false</grading_standard_enabled>
  <restrict_student_future_view>false</restrict_student_future_view>
  <restrict_student_past_view>false</restrict_student_past_view>
  <default_post_policy>
    <post_manually>false</post_manually>
  </default_post_policy>
  <enable_course_paces>false</enable_course_paces>
</course>
"""


def assignment_groups_xml(gid_assign):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<assignmentGroups {NS}>
  <assignmentGroup identifier="{gid_assign}">
    <title>Assignments</title>
    <position>1</position>
    <group_weight>0.0</group_weight>
  </assignmentGroup>
</assignmentGroups>
"""


def late_policy_xml():
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<late_policy identifier="{gid("late-policy")}" {NS}>
  <missing_submission_deduction_enabled>false</missing_submission_deduction_enabled>
  <missing_submission_deduction>100.0</missing_submission_deduction>
  <late_submission_deduction_enabled>true</late_submission_deduction_enabled>
  <late_submission_deduction>10.0</late_submission_deduction>
  <late_submission_interval>day</late_submission_interval>
  <late_submission_minimum_percent_enabled>false</late_submission_minimum_percent_enabled>
  <late_submission_minimum_percent>0.0</late_submission_minimum_percent>
</late_policy>
"""


def syllabus_html():
    html = subprocess.run(
        ["pandoc", "--from=docx", "--to=html5", "--wrap=none", os.path.join(ROOT, SYLLABUS_DOCX)],
        capture_output=True, text=True, check=True,
    ).stdout
    html = re.sub(r"<img\b[^>]*>", "", html)
    # The revised DOCX marks changed text with highlighting; students should not see it.
    html = re.sub(r"</?mark>", "", html)

    # pandoc can treat the first body rows as header rows; keep only the first row in <thead>.
    def fix_thead(m):
        rows = re.findall(r"<tr\b.*?</tr>", m.group(1), flags=re.S)
        if len(rows) <= 1:
            return m.group(0)
        rest = "".join(re.sub(r"<th\b([^>]*)>", r"<td\1>", r).replace("</th>", "</td>") for r in rows[1:])
        return "<thead>" + rows[0] + "</thead><tbody>" + rest

    html = re.sub(r"<thead>(.*?)</thead>\s*<tbody>", lambda m: fix_thead(m), html, flags=re.S)
    html = style_html(html)
    return f'<div style="line-height: 1.6; overflow-wrap: anywhere;">\n{html}</div>\n'


def module_item_xml(ident, ctype, title, ref, position, state):
    ref_xml = f"\n        <identifierref>{ref}</identifierref>" if ref else ""
    return f"""      <item identifier="{ident}">
        <content_type>{ctype}</content_type>
        <workflow_state>{state}</workflow_state>
        <title>{escape(title)}</title>{ref_xml}
        <position>{position}</position>
        <new_tab>false</new_tab>
        <indent>0</indent>
        <link_settings_json>null</link_settings_json>
      </item>"""


# --------------------------------------- Build ------------------------------------------

class Builder:
    def __init__(self):
        self.files = {}      # zip path -> bytes/str
        self.resources = []  # (xml string)
        self.modules = []    # dicts: ident,title,items[(ident,ctype,title,ref)]
        self.org_items = []  # manifest org xml per module
        self.paste = {}      # filename -> html
        self.titles_used = set()
        self.assign_group = gid("group:assignments")
        self.pos = 0
        self.counts = {"pages": 0, "assignments": 0, "quizzes": 0}
        self.assignment_cache = {}

    # -- items --
    def page(self, src, forced_title=None):
        if not exists(src):
            if PARTIAL:
                warn(f"missing source skipped: {src}")
                return None
            raise SystemExit(f"missing source: {src}")
        title, body_md = split_title(read(src))
        title = forced_title or title
        ident = gid("page:" + src)
        slug = slugify(title)
        base, n = slug, 2
        while slug in self.titles_used:
            slug = f"{base}-{n}"
            n += 1
        self.titles_used.add(slug)
        body = md_to_html(body_md, src)
        href = f"wiki_content/{slug}.html"
        self.files[href] = wiki_html(title, ident, body)
        self.resources.append(
            f'    <resource identifier="{ident}" type="webcontent" href="{href}">\n'
            f'      <file href="{href}"/>\n    </resource>')
        self.paste[f"page-{slug}.html"] = body
        self.counts["pages"] += 1
        return ("WikiPage", title, ident)

    def assignment(self, num, src):
        if num in self.assignment_cache:
            return self.assignment_cache[num]
        if not exists(src):
            if PARTIAL:
                warn(f"missing source skipped: {src}")
                return None
            raise SystemExit(f"missing source: {src}")
        title, body_md = split_title(read(src))
        ident = gid("assignment:" + src)
        slug = slugify(title)
        body = md_to_html(body_md, src)
        d = ident
        html_href = f"{d}/{slug}.html"
        set_href = f"{d}/assignment_settings.xml"
        self.files[html_href] = (
            '<html>\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n'
            f"<title>Assignment: {escape(title)}</title>\n</head>\n<body>\n{body}</body>\n</html>\n")
        self.files[set_href] = assignment_xml(ident, title, self.assign_group, num)
        self.resources.append(
            f'    <resource identifier="{ident}" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="{html_href}">\n'
            f'      <file href="{html_href}"/>\n      <file href="{set_href}"/>\n    </resource>')
        self.paste[f"assignment-{slug}.html"] = body
        self.counts["assignments"] += 1
        self.assignment_cache[num] = ("Assignment", title, ident)
        return self.assignment_cache[num]

    def quiz(self, src):
        if not exists(src):
            if PARTIAL:
                warn(f"missing source skipped: {src}")
                return None
            raise SystemExit(f"missing source: {src}")
        data = json.loads(read(src))
        qid = gid("quiz:" + src)
        meta_id = gid("quizmeta:" + src)
        self.files[f"{qid}/assessment_meta.xml"] = quiz_meta(qid, data)
        self.files[f"{qid}/assessment_qti.xml"] = qti_document(qid, data, cc=True)
        self.files[f"non_cc_assessments/{qid}.xml.qti"] = qti_document(qid, data, cc=False)
        self.resources.append(
            f'    <resource identifier="{qid}" type="imsqti_xmlv1p2/imscc_xmlv1p1/assessment">\n'
            f'      <file href="{qid}/assessment_qti.xml"/>\n'
            f'      <dependency identifierref="{meta_id}"/>\n    </resource>')
        self.resources.append(
            f'    <resource identifier="{meta_id}" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="{qid}/assessment_meta.xml">\n'
            f'      <file href="{qid}/assessment_meta.xml"/>\n'
            f'      <file href="non_cc_assessments/{qid}.xml.qti"/>\n    </resource>')
        self.counts["quizzes"] += 1
        return ("Quizzes::Quiz", data["title"], qid)

    # -- modules --
    def build(self):
        for num, folder, title, week in MODULES:
            d = f"modules/{folder}"
            items = []

            def add(kind_title, entry):
                if entry:
                    items.append(entry)

            items.append(("ContextModuleSubHeader", "Lecture", None))
            if num == 0:
                for src in START_HERE_PAGES:
                    add("", self.page(src))
            add("", self.page(f"{d}/lesson.md"))
            for extra in EXTRA_PAGES.get(folder, []):
                add("", self.page(f"{d}/{extra}"))
            q = self.quiz(f"{d}/assessment.json")
            if q:
                items.append(("ContextModuleSubHeader", "Practice (ungraded)", None))
                items.append(q)
            for anum, (asrc, amod) in sorted(ASSIGNMENTS.items()):
                if amod == num:
                    a = self.assignment(anum, asrc)
                    if a:
                        items.append(("ContextModuleSubHeader", "Assignment", None))
                        items.append(a)
            for anum, amod in sorted(ALSO_LISTED_IN.items()):
                if amod == num:
                    a = self.assignment(anum, ASSIGNMENTS[anum][0])
                    if a:
                        items.append(("ContextModuleSubHeader", f"Assignment (opened in Module {ASSIGNMENTS[anum][1]})", None))
                        items.append(a)
            lk = self.page(f"{d}/links.md")
            if lk:
                items.append(("ContextModuleSubHeader", "Links", None))
                items.append(lk)
            mtitle = f"Module {num} — {title}" + (f" (Week {week})" if week else "")
            self.modules.append({"ident": gid(f"module:{num}"), "title": mtitle, "items": items, "pos": num + 1})
        self.write_course_level()

    def write_course_level(self):
        course_id = gid("course:" + COURSE_CODE)
        self.files["course_settings/course_settings.xml"] = course_settings_xml(course_id)
        self.files["course_settings/assignment_groups.xml"] = assignment_groups_xml(self.assign_group)
        self.files["course_settings/late_policy.xml"] = late_policy_xml()
        self.files["course_settings/canvas_export.txt"] = (
            "CSYE 7270 Fall 2026 (Godot, Walker, Claude Code). Generated by scripts/build_course.py.\n")
        self.files["course_settings/syllabus.html"] = syllabus_html()
        self.files["course_settings/files_meta.xml"] = f'<?xml version="1.0" encoding="UTF-8"?>\n<fileMeta {NS}>\n</fileMeta>\n'
        self.files["course_settings/media_tracks.xml"] = f'<?xml version="1.0" encoding="UTF-8"?>\n<media_tracks {NS}>\n</media_tracks>\n'
        self.files["course_settings/events.xml"] = f'<?xml version="1.0" encoding="UTF-8"?>\n<events {NS}>\n</events>\n'
        self.files["course_settings/rubrics.xml"] = f'<?xml version="1.0" encoding="UTF-8"?>\n<rubrics {NS}>\n</rubrics>\n'
        self.resources.insert(
            0,
            f'    <resource identifier="{course_id}_syllabus" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="course_settings/syllabus.html" intendeduse="syllabus">\n'
            '      <file href="course_settings/syllabus.html"/>\n    </resource>')

        # module_meta.xml + manifest organization
        mm, org = [], []
        state = "active" if STATE == "published" else "unpublished"
        item_state = "active" if STATE == "published" else "unpublished"
        for m in self.modules:
            mi, oi = [], []
            for pos, (ctype, title, ref) in enumerate(m["items"], 1):
                iid = gid(f"item:{m['ident']}:{pos}:{title}")
                st = "active" if ctype == "ContextModuleSubHeader" else item_state
                mi.append(module_item_xml(iid, ctype, title, ref, pos, st))
                ref_attr = f' identifierref="{ref}"' if ref else ""
                oi.append(f'          <item identifier="{iid}"{ref_attr}>\n            <title>{escape(title)}</title>\n          </item>')
            mm.append(
                f'  <module identifier="{m["ident"]}">\n    <title>{escape(m["title"])}</title>\n'
                f'    <workflow_state>{state}</workflow_state>\n    <position>{m["pos"]}</position>\n'
                '    <require_sequential_progress>false</require_sequential_progress>\n    <locked>false</locked>\n'
                '    <items>\n' + "\n".join(mi) + "\n    </items>\n  </module>")
            org.append(
                f'        <item identifier="{m["ident"]}">\n          <title>{escape(m["title"])}</title>\n'
                + "\n".join(oi) + "\n        </item>")
        self.files["course_settings/module_meta.xml"] = (
            f'<?xml version="1.0" encoding="UTF-8"?>\n<modules {NS}>\n' + "\n".join(mm) + "\n</modules>\n")
        self.files["imsmanifest.xml"] = self.manifest(course_id, org)

    def manifest(self, course_id, org):
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="{gid("manifest:" + COURSE_CODE)}" xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1" xmlns:lom="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource" xmlns:lomimscc="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/manifest" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1 http://www.imsglobal.org/profile/cc/ccv1p1/ccv1p1_imscp_v1p2_v1p0.xsd http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource http://www.imsglobal.org/profile/cc/ccv1p1/LOM/ccv1p1_lomresource_v1p0.xsd http://ltsc.ieee.org/xsd/imsccv1p1/LOM/manifest http://www.imsglobal.org/profile/cc/ccv1p1/LOM/ccv1p1_lommanifest_v1p0.xsd">
  <metadata>
    <schema>IMS Common Cartridge</schema>
    <schemaversion>1.1.0</schemaversion>
    <lomimscc:lom>
      <lomimscc:general>
        <lomimscc:title>
          <lomimscc:string>{escape(COURSE_TITLE)}</lomimscc:string>
        </lomimscc:title>
      </lomimscc:general>
      <lomimscc:lifeCycle>
        <lomimscc:contribute>
          <lomimscc:date>
            <lomimscc:dateTime>{BUILD_DATE}</lomimscc:dateTime>
          </lomimscc:date>
        </lomimscc:contribute>
      </lomimscc:lifeCycle>
      <lomimscc:rights>
        <lomimscc:copyrightAndOtherRestrictions>
          <lomimscc:value>yes</lomimscc:value>
        </lomimscc:copyrightAndOtherRestrictions>
        <lomimscc:description>
          <lomimscc:string>Private (Copyrighted) - http://en.wikipedia.org/wiki/Copyright</lomimscc:string>
        </lomimscc:description>
      </lomimscc:rights>
    </lomimscc:lom>
  </metadata>
  <organizations>
    <organization identifier="org_1" structure="rooted-hierarchy">
      <item identifier="LearningModules">
{chr(10).join(org)}
      </item>
    </organization>
  </organizations>
  <resources>
{chr(10).join(self.resources)}
  </resources>
</manifest>
"""

    # -- output --
    def write(self):
        os.makedirs(OUT_PASTE, exist_ok=True)
        os.makedirs(OUT_PKG, exist_ok=True)
        for old in os.listdir(OUT_PASTE):
            if old.endswith(".html"):
                os.remove(os.path.join(OUT_PASTE, old))
        for name, html in sorted(self.paste.items()):
            with open(os.path.join(OUT_PASTE, name), "w", encoding="utf-8") as f:
                f.write(html)
        path = os.path.join(OUT_PKG, IMSCC_NAME)
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("imsmanifest.xml", self.files["imsmanifest.xml"])
            for name in sorted(self.files):
                if name != "imsmanifest.xml":
                    z.writestr(name, self.files[name])
        return path


# --------------------------------------- Check ------------------------------------------

def integrity_check(path):
    import xml.etree.ElementTree as ET
    problems = []
    z = zipfile.ZipFile(path)
    names = set(z.namelist())
    for n in names:
        if n.endswith((".xml", ".qti")):
            try:
                ET.fromstring(z.read(n))
            except ET.ParseError as e:
                problems.append(f"not well-formed: {n}: {e}")
    man = ET.fromstring(z.read("imsmanifest.xml"))
    ns = {"m": "http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1"}
    res = {}
    for r in man.findall(".//m:resource", ns):
        rid = r.get("identifier")
        if rid in res:
            problems.append(f"duplicate resource id {rid}")
        res[rid] = r
        for f in r.findall("m:file", ns):
            if f.get("href") not in names:
                problems.append(f"resource {rid} lists missing file {f.get('href')}")
        for d in r.findall("m:dependency", ns):
            if d.get("identifierref") not in res and d.get("identifierref") not in {x.get("identifier") for x in man.findall('.//m:resource', ns)}:
                problems.append(f"resource {rid} depends on unknown {d.get('identifierref')}")
    org_ids = set()
    for it in man.findall(".//m:organization//m:item", ns):
        iid = it.get("identifier")
        if iid in org_ids:
            problems.append(f"duplicate item id {iid}")
        org_ids.add(iid)
        ref = it.get("identifierref")
        if ref and ref not in res:
            problems.append(f"organization item {iid} refers to unknown resource {ref}")
    cn = {"c": "http://canvas.instructure.com/xsd/cccv1p0"}
    mm = ET.fromstring(z.read("course_settings/module_meta.xml"))
    for it in mm.findall(".//c:item", cn):
        ref = it.findtext("c:identifierref", namespaces=cn)
        ct = it.findtext("c:content_type", namespaces=cn)
        if ct != "ContextModuleSubHeader" and (not ref or ref not in res):
            problems.append(f"module item '{it.findtext('c:title', namespaces=cn)}' has bad ref {ref}")
    for n in names:
        if n.endswith("assignment_settings.xml"):
            a = ET.fromstring(z.read(n))
            if a.findtext("c:points_possible", namespaces=cn) != "100.0":
                problems.append(f"{n}: points_possible is not 100.0")
    return problems


def main():
    global STATE, PARTIAL
    ap = argparse.ArgumentParser()
    ap.add_argument("--partial", action="store_true", help="skip sources that do not exist yet")
    ap.add_argument("--state", choices=["published", "unpublished"], default="unpublished")
    ap.add_argument("--check", action="store_true", help="only report integrity problems")
    args = ap.parse_args()
    STATE, PARTIAL = args.state, args.partial
    b = Builder()
    b.build()
    path = b.write()
    problems = integrity_check(path)
    size = os.path.getsize(path)
    print(f"\nBuilt {os.path.relpath(path, ROOT)} ({size/1024:.0f} KB): "
          f"{len(MODULES)} modules, {b.counts['pages']} pages, {b.counts['assignments']} assignments, "
          f"{b.counts['quizzes']} quizzes; state={STATE}")
    print(f"Paste fragments: {len(b.paste)} in {os.path.relpath(OUT_PASTE, ROOT)}")
    repo_links = sorted({u for _, u in link_log})
    print(f"Links rewritten to the course repo: {len(repo_links)} unique (resolve only after the repo is pushed)")
    if problems:
        print("\nINTEGRITY PROBLEMS:")
        for p in problems:
            print("  " + p)
        sys.exit(1)
    print("Integrity check: OK (well-formed XML, every reference resolves)")
    with open(os.path.join(OUT_PKG, "repo-links.txt"), "w") as f:
        f.write("\n".join(repo_links) + "\n")


if __name__ == "__main__":
    main()
