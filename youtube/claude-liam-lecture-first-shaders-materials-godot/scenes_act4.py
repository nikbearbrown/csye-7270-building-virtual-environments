"""ACT IV · The Shader From Code  (B25-B34, ten Manim beats; the Remotion runner-ups are recorded in lanes/act4.json and evidence/act4/auditions/)

HONESTY (Films = things actually done).
- The shader on screen is the INSTRUCTOR EXAMPLE's signal.gdshader (an A. I. wrote it under Professor Bear's direction): every code line below is a
  verbatim literal of evidence/example/sources/signal.gdshader, garden.gd, test-signal-driver.gd or a line of a real log in evidence/runs/;
  evidence/act4/verify_lines.py diffs every A4_SRC_* literal against its source file. Tabs are shown as four spaces and the indentation is kept
  (the first kit's code_block dropped indentation because Manim's Text bounding box ignores leading spaces; a4_Code places every row by character cell and recolours
  glyph by glyph, which code_block cannot do, so it is kept even after the kit fix).
- Nothing is called hand-written, student work or a Claude Code session. B25 shows the INSTRUCTION ("write it by hand") with scribble lines on a page
  labelled "your shader"; the only example text there is the specification's colour line (CHANGE-BRIEF-a5.md line 5), tagged as the example's.
- B29 shows the assignment's own prompt text, labelled "documented, not run". B31-B34 logs are from the re-run for this film (evidence/runs/, 16 Oct).
- Pad pictures are the example's own native captures (Compatibility, 14 Oct) or scripted-input lab frames (captures/lab/), never styled as anything else.

Cast for the act: the same 11 lines of signal.gdshader (B26-B28), the pad (B28, B30, B34), three frame-rate rulers (B32), the E key (B31).
Pacing: until() cues are the character share of the narration x the estimate (no audio exists yet); fixed sequences end by ~75-85% of the estimate.
"""

A4_ADV = {20: 0.15, 24: 0.2, 28: 0.25, 32: 0.25}     # Menlo advance per character (measured: evidence/act4/measure_menlo.py)

# ── verbatim source literals (diffed against the frozen sources by evidence/act4/verify_lines.py) ─────────────────────
A4_SRC_SIGNAL = [                                    # evidence/example/sources/signal.gdshader lines 1-11
    "shader_type spatial;",
    "render_mode unshaded;",
    "uniform float activation : hint_range(0.0, 1.0) = 0.0;",
    "uniform vec4 quiet_color : source_color = vec4(0.40, 0.16, 0.09, 1.0);",
    "uniform vec4 active_color : source_color = vec4(0.12, 0.72, 0.52, 1.0);",
    "uniform float stripe_count : hint_range(1.0, 16.0, 1.0) = 8.0;",
    "void fragment() {",
    "\tfloat stripe = step(0.5, fract(UV.x * stripe_count));",
    "\tvec3 base = quiet_color.rgb * mix(0.65, 1.0, stripe);",
    "\tALBEDO = mix(base, active_color.rgb, activation);",
    "}",
]
A4_SRC_BRIEF_COLOUR = "ALBEDO = mix(base, active_color.rgb, activation)"     # CHANGE-BRIEF-a5.md line 5 (the specification's colour line, no semicolon)
# the assignment's own driver prompt (assignment-05.md, Step 2): consecutive words of the prompt, whitespace-normalised (verify_lines.py checks each)
A4_SRC_PROMPT = ["do not edit any .gdshader file.", "First propose the smallest plan that meets the spec:", "Do not edit yet.",
                 "through the real game loop and real input,", "the new one at 30, 60 and 144.", "what it cannot prove in a headless run,"]
# real log lines of the re-run (evidence/runs/, 16 Oct 2026): (file, line number, the line); verify_lines.py diffs each against the file
A4_SRC_LOG_B31 = [("R2-driver-60fps.log", n, t) for n, t in (
    (3, "PASS scaled duration 1.0"), (4, "PASS retrigger ignored 1.0"), (5, "PASS end uniform one 1.0"),
    (7, "PASS scaled duration 0.5"), (8, "PASS retrigger ignored 0.5"), (9, "PASS end uniform one 0.5"),
    (11, "PASS pause freezes charge"), (12, "PASS reset clears uniform"), (13, "PASS interruption has no late gate"),
    (14, "PASS every sampled uniform matches game state"))]
A4_SRC_CMD_B33 = "./scripts/run-test.sh test-material-contract.gd 60"            # journal-commands-exit-codes-elapsed.tsv, row M1-parse (exit=1)
A4_SRC_LOG_B33 = [("R4-M1-parse-60fps.log", n, t) for n, t in (
    (7, "SHADER ERROR: Expected a ';' after 'shader_type spatial'."), (15, "UNIFORM_TYPES {}"),
    (16, "FAIL declared activation is float"), (17, "FAIL declared quiet_color is vec4"),
    (18, "FAIL declared active_color is vec4"), (19, "FAIL declared stripe_count is float"),
    (78, "RESULT 53 checks / 4 failures / baseline"))]
A4_SRC_LOG_B34 = [("R4-M2-undeclared-probe.log", 4, "READBACK activation = 0.7"), ("R4-M2-undeclared-probe.log", 5, "READBACK renamed_activation = <null>"),
                  ("R4-M2-rename-driver-60fps.log", 16, "RESULT 10 checks / 0 failures; sample count 409"),
                  ("R4-M2-rename-contract-60fps.log", 4, "FAIL declared activation is float"),
                  ("R4-M2-rename-contract-60fps.log", 66, "RESULT 53 checks / 1 failures / baseline")]
A4_SRC_GARDEN_4 = ["const CHARGE_SECONDS := 0.6"]                                # garden.gd line 4
A4_SRC_GARDEN_227 = [                                                          # garden.gd lines 227-231
    "\tif charging:",
    "\t\tcharge = minf(CHARGE_SECONDS, charge + delta)",
    "\t\tif charge >= CHARGE_SECONDS - 0.00001:",
    "\t\t\tcharging = false",
    "\t\t\tgate_open = true",
]
A4_SRC_GARDEN_253 = ['\tpad_material.set_shader_parameter("activation", charge / CHARGE_SECONDS)']   # garden.gd line 253


# ═════════════════════════ helpers (all act-prefixed) ═════════════════════════
def a4_lab(s, x, y, size=34, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a4_mono(s, x, y, size=32, color=INK):
    return M(s, size, color).move_to([x, y, 0])


def a4_etag(x=3.4, y=2.95):
    return example_tag(x, y)


def a4_stag(text, x, y):
    return status_tag(text, x, y)


def a4_cell(s, left, y, size=20, color=INK, col=0):
    """Monospace text whose first character sits in cell `col` of a row whose cell-left is `left` (no leading or trailing spaces in s).
    Menlo's advance is exactly 0.15 / 0.20 / 0.25 units at size 20 / 24 / 28-32, so the row's ink centre is left + (col + len/2) * advance.
    (Text.width and get_left() are never used for placing: the bounding box ignores leading spaces.)"""
    t = M(s, size, color)
    t.move_to([left + (col + len(s) / 2.0) * A4_ADV[size], y, 0])
    return t


class a4_Code(VGroup):
    """Real code, one monospace row per line, OUTLINE-only frame, REAL line numbers (first=), indentation kept (tab = 4 spaces).
    `show` = the row indexes drawn now (default all); the others are built later with num_mob(i) / txt_mob(i) (same geometry)."""

    def __init__(self, lines, first=1, x=0.0, y=0.0, size=20, pitch=None, pad=0.25, numbers=True, min_cols=0, color=INK, frame=True, show=None):
        VGroup.__init__(self)
        adv = A4_ADV[size]
        lines = [ln.replace("\t", "    ").rstrip() for ln in lines]
        pitch = pitch or (size / 32 * 0.46)
        ndig = max(len(str(first + i)) for i in range(len(lines)))
        nw = (ndig * adv + 0.3) if numbers else 0.0
        cols = max(max(len(l) for l in lines), min_cols)
        W = nw + cols * adv + 2 * pad
        H = len(lines) * pitch + 2 * pad
        self.adv, self.pitch, self.W, self.H, self.cx, self.cy, self.size_, self.first, self.lines_ = adv, pitch, W, H, x, y, size, first, lines
        self.pad_, self.ndig, self.numbers_, self.color_, self.cols = pad, ndig, numbers, color, cols
        self.left0 = x - W / 2 + pad + nw                 # cell-left of column 0
        self.frame = RoundedRectangle(width=W, height=H, corner_radius=0.14, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
        self.rows = VGroup()
        for i in (range(len(lines)) if show is None else show):
            self.rows.add(VGroup(*([self.num_mob(i)] if numbers else []), self.txt_mob(i)))
        if frame:
            self.add(self.frame)
        self.add(self.rows)

    def y_of(self, n):
        return self.cy + self.H / 2 - self.pad_ - self.pitch * (n - self.first + 0.5)

    def x_of(self, col):
        return self.left0 + col * self.adv

    def num_mob(self, i):
        s = str(self.first + i)
        n = M(s, self.size_, DIM)
        n.move_to([self.cx - self.W / 2 + self.pad_ + self.ndig * self.adv - len(s) * self.adv / 2.0, self.y_of(self.first + i), 0])
        return n

    def txt_mob(self, i):
        ln = self.lines_[i]
        body = ln.strip()
        k = len(ln) - len(ln.lstrip(" "))
        return a4_cell(body, self.left0, self.y_of(self.first + i), self.size_, self.color_, col=k) if body else VGroup()

    def seg(self, n, text, col, color=None):
        """A piece of REAL line n starting at column col (monospace: exact placement), for per-piece colouring."""
        return a4_cell(text, self.left0, self.y_of(n), self.size_, color or self.color_, col=col)

    def ring_cols(self, n, c0, c1, pad=0.07, h=0.26, color=TERRA):
        """Ring (grey backing + terracotta) round columns c0..c1 (inclusive) of REAL line n."""
        w = (c1 - c0 + 1) * self.adv
        ph = Rectangle(width=w, height=h, stroke_width=0, fill_opacity=0).move_to([self.x_of(c0) + w / 2, self.y_of(n), 0])
        return ring(ph, color=color, pad=pad, sw=6)

    def ring_row(self, n, color=TERRA, full=False, grey=False):
        """Ring (grey backing + terracotta) round the text of REAL line n (from its indentation to its last character), clear of the glyphs.
        grey=True: a grey ring plus one terracotta dot just beyond its right end. GATE T reads a SHORT terracotta ring (width < 15 x height) as accent text,
        so a ring round a short line is grey with a terracotta dot (a dot is never read as text)."""
        ln = self.lines_[n - self.first]
        k = 0 if full else len(ln) - len(ln.lstrip(" "))
        w = (self.cols if full else len(ln.strip())) * self.adv
        ph = Rectangle(width=w, height=0.27, stroke_width=0, fill_opacity=0).move_to([self.x_of(k) + w / 2, self.y_of(n), 0])
        if grey:
            r_ = ring(ph, color=DIM, pad=0.09, sw=6, backing=False)
            dot = Dot([self.x_of(k) + w + 0.3, self.y_of(n), 0], radius=0.09, color=TERRA)
            return VGroup(r_, dot)
        return ring(ph, color=color, pad=0.09, sw=6)


def a4_glyphs(txt, body, c0, c1):
    """The glyph sub-mobjects of Text `txt` (whose string is `body`, no leading/trailing spaces) for characters c0..c1-1.
    Manim's Text has one sub-mobject per NON-space character, so spans can be recoloured with exact positions."""
    start = len(body[:c0].replace(" ", ""))
    n = len(body[c0:c1].replace(" ", ""))
    return [txt[i] for i in range(start, start + n)]


def a4_paint(glyphs, color):
    """Animations that recolour each glyph in place (one .animate per glyph: a VGroup(*glyphs) would be added to the scene as a second owner of the glyphs)."""
    return [m.animate.set_color(color) for m in glyphs]


def a4_uniform_parts(line):
    """Split a REAL `uniform <type> <name> : <hint> = <default>;` line into (role, text, column) pieces (monospace columns)."""
    import re
    m = re.match(r"^uniform (\w+) (\w+) : (.+?) = (.+);$", line)
    t, n, h, d = m.group(1), m.group(2), m.group(3), m.group(4)
    c_t = 8
    c_n = c_t + len(t) + 1
    c_h = c_n + len(n) + 3
    c_d = c_h + len(h) + 3
    return [("kw", "uniform", 0), ("type", t, c_t), ("name", n, c_n), ("pun", ":", c_n + len(n) + 1), ("hint", h, c_h), ("pun", "=", c_h + len(h) + 1),
            ("default", d + ";", c_d)]


def a4_gap(x, y, color=DIM):
    """The marker for lines left out between two excerpts: three small dots."""
    return VGroup(*[Dot([x + dx, y, 0], radius=0.045, color=color) for dx in (-0.18, 0.0, 0.18)])


def a4_no(x, y, r=0.3, sw=7):
    """A prohibition mark (ink ring + bar), drawn BESIDE or over a picture, never over type."""
    d = r * 0.7071
    return VGroup(Circle(radius=r, stroke_color=INK, stroke_width=sw).move_to([x, y, 0]), Line([x - d, y + d, 0], [x + d, y - d, 0], color=INK, stroke_width=sw))


def a4_calendar(x, y, s=0.32, color=INK):
    """A drawn calendar page (outline, a header bar, two binder rings, one terracotta dot): the mark for 'dated'. No numerals."""
    body = RoundedRectangle(width=2 * s, height=1.7 * s, corner_radius=0.06, stroke_color=color, stroke_width=4, fill_opacity=0).move_to([x, y - 0.1 * s, 0])
    bar = Line([x - s, y + 0.45 * s, 0], [x + s, y + 0.45 * s, 0], color=color, stroke_width=4)
    rings = VGroup(*[Line([x + dx * s, y + 0.75 * s, 0], [x + dx * s, y + 1.05 * s, 0], color=color, stroke_width=5) for dx in (-0.55, 0.55)])
    dot = Dot([x + 0.3 * s, y - 0.35 * s, 0], radius=0.07, color=TERRA)
    return VGroup(body, bar, rings, dot)


# ── the writing kit (show-tell iso_kit, copied with the a4_ prefix: the kit file is pasted, never imported) ─────────────
def a4_quill(x, y, s=1.0, angle=0.0, color=INK, fill=BOX_TOP):
    """A drawn quill with its NIB at (x, y); the feather points up-right. `g.nib` is the nib point."""
    o = np.array([x, y, 0.0])

    def P(u, v):
        return o + np.array([u * s, v * s, 0.0])
    body = VMobject(fill_color=fill, fill_opacity=1, stroke_color=color, stroke_width=4)
    body.set_points_smoothly([P(0.00, 0.00), P(0.12, 0.62), P(0.55, 1.02), P(1.00, 1.10), P(0.95, 0.68), P(0.62, 0.22), P(0.00, 0.00)])
    shaft = Line(P(0.02, 0.02), P(0.98, 1.06), color=color, stroke_width=3)
    barb = Line(P(0.46, 0.50), P(0.40, 0.72), color=color, stroke_width=2.5)
    g = VGroup(body, shaft, barb)
    if angle:
        g.rotate(angle, about_point=o)
    g.nib = o.copy()
    return g


def a4_paper(x, y, w=2.4, h=3.0, fill=PAGE_TOP):
    """A flat 2-D sheet: white page, ink outline, kraft drop shadow."""
    shadow = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.12, y - 0.12, 0])
    sheet = Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    return VGroup(shadow, sheet)


def a4_scribble(x, y, w, amp=0.07, color=INK, sw=4):
    """One wavy handwriting line from (x, y) rightwards for w units (reads as script, never as type)."""
    n = max(3, int(round(w * 3)))
    pts = []
    for i in range(n * 4 + 1):
        t = i / (n * 4)
        pts.append([x + w * t, y + amp * np.sin(t * n * 2 * np.pi) * (0.6 + 0.4 * np.cos(t * 5.3)), 0])
    m = VMobject(stroke_color=color, stroke_width=sw)
    m.set_points_smoothly(pts)
    return m


def a4_write_lines(self, q, lines, speed=7.0, hop=0.2, dip=0.05):
    """The quill q WRITES each scribble line: the nib hops to the line's start, then the line draws while the nib rides its tip."""
    for ln in lines:
        start = np.array(ln.get_start(), dtype=float)
        self.play(q.animate.shift(start - q.nib), run_time=hop, rate_func=smooth)
        q.nib = start.copy()
        off = np.array(q.get_center(), dtype=float) - q.nib

        def ride(m, a, ln=ln, off=off):
            m.move_to(np.array(ln.point_from_proportion(min(1.0, a)), dtype=float) + off)
        try:
            length = float(ln.get_arc_length())
        except Exception:
            length = 2.0
        rt = max(0.35, length / speed)
        self.play(Create(ln), UpdateFromAlphaFunc(q, ride), run_time=rt, rate_func=linear)
        q.nib = np.array(ln.get_end(), dtype=float)
        q.shift([0, dip, 0]); q.nib = q.nib + np.array([0, dip, 0])


# ═════════════════════════ B25 · write it by hand from the specification; TIME is global ═════════════════════════
class B25_WriteFromSpec(Scene):
    def construct(self):
        title = T("The  Shader  From  Code", 40).move_to([-3.4, 2.95, 0])
        self.add(title)
        cx = -1.4                                                                     # centre of the specification card and the page
        spec = a4_Code([A4_SRC_BRIEF_COLOUR], x=cx, y=1.3, size=20, numbers=False, pad=0.22)
        spec_l = a4_lab("specification", 4.7, 1.3, 34)
        page = a4_paper(cx, -0.85, w=7.5, h=1.9)
        page_l = a4_lab("your shader", 4.7, -0.85, 34)
        # three scribble lines on the page (script, not type); the third is as long as the colour line above it
        sx = cx - 3.2
        lines = [a4_scribble(sx, -0.38, 6.3), a4_scribble(sx, -0.85, 5.4), a4_scribble(sx, -1.32, 6.4)]
        quill = a4_quill(sx, -0.38, 0.8, 0.0)
        quill.shift(np.array([-0.2, 0.55, 0.0])); quill.nib = quill.nib + np.array([-0.2, 0.55, 0.0])

        until(self, "Write it by hand", lead=0.45)
        etag = a4_etag()
        self.play(FadeIn(spec, shift=DOWN * 0.15), FadeIn(spec_l), FadeIn(etag), run_time=0.45)
        self.play(FadeIn(page), FadeIn(page_l), FadeIn(quill), run_time=0.4)
        a4_write_lines(self, quill, lines[:2], speed=7.5)
        until(self, "colour line exactly", lead=0.55)
        arr = arrow([-3.4, 0.95, 0], [-3.4, 0.2, 0], color=INK, w=6, tip=0.2)
        ex_l = a4_lab("exactly", -2.4, 0.58, 32)
        self.play(GrowArrow(arr), FadeIn(ex_l), run_time=0.35)
        a4_write_lines(self, quill, lines[2:], speed=7.5)
        until(self, "revise the specification", lead=0.6)
        back = CurvedArrow(np.array([-5.5, -0.7, 0.0]), np.array([-5.5, 1.05, 0.0]), angle=-PI / 2.2, color=INK, stroke_width=6, tip_length=0.2)
        self.play(Create(back), run_time=0.5)
        until(self, "dated", lead=0.75)
        cal = a4_calendar(3.55, 0.3, s=0.34)
        cal_l = a4_lab("dated", 4.75, 0.3, 34)
        self.play(FadeIn(cal), FadeIn(cal_l), run_time=0.4)
        # reimport -> no shader error -> commit alone
        c1 = chip("reimport", -4.8, -2.45, size=34)
        a1 = arrow([-3.5, -2.45, 0], [-2.6, -2.45, 0], w=6, tip=0.18)
        c2 = chip("no shader error", -0.82, -2.45, size=34)
        tk = tick_mark(1.2, -2.45, s=0.22, color=INK, w=8)
        a2 = arrow([1.7, -2.45, 0], [2.55, -2.45, 0], w=6, tip=0.18)
        c3 = chip("commit alone", 4.2, -2.45, size=34)
        cdot = Dot([6.05, -2.45, 0], radius=0.11, color=TERRA)
        until(self, "Reimport", lead=0.4)
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.35)
        until(self, "no shader error", lead=0.4)
        self.play(GrowArrow(a1), FadeIn(c2, shift=UP * 0.15), run_time=0.35)
        self.play(Create(tk), run_time=0.25)
        until(self, "commit it alone", lead=0.4)
        self.play(GrowArrow(a2), FadeIn(c3, shift=UP * 0.15), FadeIn(cdot, scale=0.5), run_time=0.35)
        # the second picture: TIME is global
        until(self, "The built-in time", lead=0.7)
        gone = [etag, spec, spec_l, page, page_l, quill, arr, ex_l, back, cal, cal_l, lines[0], lines[1], lines[2]]
        self.play(*[FadeOut(m) for m in gone], run_time=0.25)
        ty = 0.85
        track = Line([-5.2, ty, 0], [5.2, ty, 0], color=DIM, stroke_width=5)
        start_l = a4_lab("engine start", -4.5, ty - 0.7, 32)
        t_l = a4_mono("TIME", -5.2, ty + 0.8, 32)
        t_dot = Dot([-5.2, ty, 0], radius=0.16, color=INK)
        ev_dot = Dot([0.6, ty, 0], radius=0.16, color=TERRA)
        ev_l = a4_lab("your event", 0.6, ty - 0.7, 32)
        self.play(Create(track), FadeIn(start_l), FadeIn(t_l), FadeIn(t_dot), FadeIn(ev_dot, scale=0.5), FadeIn(ev_l), run_time=0.35)
        self.play(t_dot.animate.move_to([5.2, ty, 0]), t_l.animate.move_to([5.2, ty + 0.8, 0]), run_time=1.0, rate_func=linear)
        until(self, "never time since", lead=0.5)
        since = Line([0.6, ty - 1.55, 0], [4.9, ty - 1.55, 0], color=GHOST, stroke_width=7)
        since_l = a4_lab("since event", -0.95, ty - 1.55, 32)
        no = cross_mark(2.75, ty - 1.55, s=0.28, color=INK, w=8)
        self.play(Create(since), FadeIn(since_l), Create(no), run_time=0.3)
        done(self)


# ═════════════════════════ B26 · lines 1-6: the type, unshaded, four uniforms (type, hint, default) ═════════════════════════
class B26_FirstLines(Scene):
    def construct(self):
        g = a4_Code(A4_SRC_SIGNAL[:6], first=1, x=0.0, y=0.8, size=20, pitch=0.5, show=[0, 1])
        self.add(g)
        etag = a4_etag(3.3, -3.05)
        # rows 3-6: one Text per row; its glyphs are recoloured by span (type / name / hint / default) so each kind can be lit alone
        rows = {n: g.txt_mob(n - 1) for n in (3, 4, 5, 6)}
        nums = {n: g.num_mob(n - 1) for n in (3, 4, 5, 6)}
        spans = {n: {} for n in rows}
        for n in rows:
            body = A4_SRC_SIGNAL[n - 1]
            for role, txt, col in a4_uniform_parts(body):
                spans[n].setdefault(role, []).extend(a4_glyphs(rows[n], body, col, col + len(txt)))
        c_type = chip("shader type", -2.0, -1.95, size=34)
        c_mode = chip("render mode", 2.0, -1.95, size=34)
        until(self, "first lines choose", lead=0.35)
        self.play(g.rows[1][1].animate.set_color(DIM), FadeIn(c_type, shift=UP * 0.1), FadeIn(etag), run_time=0.4)
        until(self, "unshaded rendering", lead=0.55)
        self.play(g.rows[0][1].animate.set_color(DIM), g.rows[1][1].animate.set_color(INK), FadeIn(c_mode, shift=UP * 0.1), run_time=0.4)
        until(self, "Then four uniforms", lead=0.5)
        self.play(FadeOut(c_type), FadeOut(c_mode), g.rows[0][1].animate.set_color(INK), run_time=0.25)
        self.play(LaggedStart(*[FadeIn(VGroup(nums[n], rows[n]), shift=UP * 0.1) for n in (3, 4, 5, 6)], lag_ratio=0.18), run_time=0.7)
        # each kind of piece lit in turn: all four types, all four hints, all four defaults, then the names
        lg = {"type": chip("type", -3.0, -1.95, size=34), "hint": chip("hint", 0.0, -1.95, size=34), "default": chip("default", 3.0, -1.95, size=34)}

        def light(roles_by_row):
            """roles_by_row: {row n: roles lit}; rows 1-2 and every other glyph go DIM."""
            lit, dim = [], list(g.rows[0][1]) + list(g.rows[1][1])
            for n in rows:
                for role, gl in spans[n].items():
                    (lit if role in roles_by_row.get(n, ()) else dim).extend(gl)
            return a4_paint(lit, INK) + a4_paint(dim, DIM)
        allrows = lambda role: {n: (role,) for n in rows}
        until(self, "a type", lead=0.4)
        self.play(*light(allrows("type")), FadeIn(lg["type"], shift=UP * 0.1), run_time=0.35)
        until(self, "a hint", lead=0.3)
        self.play(*light(allrows("hint")), FadeIn(lg["hint"], shift=UP * 0.1), run_time=0.3)
        until(self, "a default", lead=0.3)
        self.play(*light(allrows("default")), FadeIn(lg["default"], shift=UP * 0.1), run_time=0.3)
        until(self, "activation", lead=0.35)
        self.play(*light({3: ("name",)}), FadeOut(lg["type"]), FadeOut(lg["hint"]), FadeOut(lg["default"]), run_time=0.35)
        until(self, "two colours", lead=0.3)
        self.play(*light({3: ("name",), 4: ("name",), 5: ("name",)}), run_time=0.3)
        until(self, "a stripe count", lead=0.6)
        self.play(*light({n: ("name",) for n in rows}), run_time=0.3)
        done(self)


# ═════════════════════════ B27 · lines 7-9: U V picks the stripe (fract, step, 0.65) ═════════════════════════
class B27_StripeMaths(Scene):
    def construct(self):
        g = a4_Code(A4_SRC_SIGNAL[6:9], first=7, x=-1.4, y=2.2, size=20, pitch=0.4)
        self.add(g)
        XL, PW, Y0, PH = -5.1, 8.6, -0.3, 1.4
        px = lambda u: XL + u * PW
        py = lambda v: Y0 + v * PH
        pts = []
        for k in range(8):                                           # fract(UV.x * 8): eight teeth; the real stripe_count default is 8.0 (signal.gdshader line 6)
            pts += [[px(k / 8), py(0), 0], [px((k + 1) / 8), py(1), 0], [px((k + 1) / 8), py(0), 0]]
        saw = VMobject(stroke_color=INK, stroke_width=6)
        saw.set_points_as_corners(np.array(pts, dtype=float))
        axes = VGroup(Line([px(0), Y0, 0], [px(1), Y0, 0], color=INK, stroke_width=5), Line([px(0), Y0, 0], [px(0), py(1) + 0.15, 0], color=INK, stroke_width=5))
        lab_x = a4_mono("UV.x", 4.75, Y0, 28)
        lab_0, lab_1 = a4_lab("0", px(0), Y0 - 0.45, 32), a4_lab("1", px(1), Y0 - 0.45, 32)
        lab_f = a4_mono("fract", 4.75, py(0.92), 28)
        thr = DashedLine([px(0), py(0.5), 0], [px(1) + 0.25, py(0.5), 0], color=DIM, stroke_width=5, dash_length=0.18)
        lab_h = a4_lab("0.5", 4.35, py(0.5), 34)
        # the two real sample pixels (UV.x 0.15625 and 0.21875): both in the second tooth, one under the cut, one over it
        u1, u2 = 0.15625, 0.21875
        d1 = Dot([px(u1), py((8 * u1) % 1.0), 0], radius=0.1, color=TERRA)
        d2 = Dot([px(u2), py((8 * u2) % 1.0), 0], radius=0.1, color=TERRA)
        strip = framed(img("pantry/a4_pad_strip.png", w=PW, x=px(0.5), y=-1.78), color=DIM, pad=0.07)
        g1 = DashedLine([px(u1), py((8 * u1) % 1.0) - 0.13, 0], [px(u1), -1.5, 0], color=DIM, stroke_width=4, dash_length=0.14)
        g2 = DashedLine([px(u2), py((8 * u2) % 1.0) - 0.13, 0], [px(u2), -1.5, 0], color=DIM, stroke_width=4, dash_length=0.14)
        etag = a4_etag(-3.4, -3.05)
        stag = a4_stag("example, 14 Oct · Compatibility", 3.3, -3.05)

        until(self, "U V picks", lead=0.45)
        r8 = g.ring_row(8)
        self.play(Create(r8), FadeIn(etag), run_time=0.4)
        until(self, "the fractional part", lead=0.5)
        self.play(Create(axes), FadeIn(lab_x), FadeIn(lab_0), FadeIn(lab_1), run_time=0.4)
        self.play(Create(saw), FadeIn(lab_f), run_time=1.5, rate_func=linear)
        until(self, "cut at one half", lead=0.75)
        self.play(Create(thr), FadeIn(lab_h), run_time=0.4)
        self.play(FadeIn(d1, scale=0.4), FadeIn(d2, scale=0.4), run_time=0.3)
        # after the midpoint: the real strip lands under the maths, the guides drop to it
        until(self, "A dark stripe", lead=0.3)
        self.play(FadeIn(strip), FadeIn(stag), Create(g1), Create(g2), run_time=0.5)
        # the colours: quiet x 0.65 = dark, quiet x 1 = light
        self.play(FadeOut(VGroup(saw, axes, lab_x, lab_0, lab_1, lab_f, thr, lab_h, d1, d2, g1, g2)), g.rows[1].animate.set_opacity(0.45),
                  FadeOut(r8), Create(g.ring_row(9)), run_time=0.4)
        quiet = swatch((102, 41, 23), -4.8, 0.15, w=1.0, h=0.8)
        quiet_l = a4_lab("quiet", -4.8, -0.55, 34)
        until(self, "sixty-five percent", lead=1.7)
        self.play(FadeIn(quiet, scale=0.6), FadeIn(quiet_l), run_time=0.35)
        until(self, "sixty-five percent", lead=0.55)
        a_d = arrow([-4.1, 0.4, 0], [-1.3, 0.7, 0], w=6, tip=0.2)
        x_d = a4_lab("× 0.65", -2.7, 1.1, 34)
        dark = swatch((66, 27, 15), -0.55, 0.7, w=1.0, h=0.7)
        dark_l = a4_lab("dark stripe", 2.0, 0.7, 34)
        self.play(GrowArrow(a_d), FadeIn(x_d), FadeIn(dark, scale=0.6), FadeIn(dark_l), run_time=0.45)
        until(self, "a light stripe", lead=0.4)
        a_l = arrow([-4.1, -0.1, 0], [-1.3, -0.4, 0], w=6, tip=0.2)
        x_l = a4_lab("× 1", -2.7, -0.95, 34)
        light = swatch((102, 41, 23), -0.55, -0.4, w=1.0, h=0.7)
        light_l = a4_lab("light stripe", 2.0, -0.4, 34)
        self.play(GrowArrow(a_l), FadeIn(x_l), FadeIn(light, scale=0.6), FadeIn(light_l), run_time=0.45)
        done(self)


# ═════════════════════════ B28 · line 10: mix by activation (0, 0.5, 1) with the pad's own captures ═════════════════════════
class B28_MixByActivation(Scene):
    def construct(self):
        g = a4_Code([A4_SRC_SIGNAL[9]], first=10, x=0.0, y=2.45, size=24, pitch=0.5, pad=0.25)
        self.add(g)
        TX0, TX1, TY = -3.9, 3.9, 0.95
        vx = lambda v: TX0 + v * (TX1 - TX0)
        track = Line([-4.5, TY, 0], [4.5, TY, 0], color=DIM, stroke_width=6)
        stops = VGroup(*[Dot([vx(v), TY, 0], radius=0.09, color=DIM) for v in (0.0, 0.5, 1.0)])
        tl = [a4_lab("0", vx(0.0), TY - 0.5, 36), a4_lab("0.5", vx(0.5), TY - 0.5, 36), a4_lab("1", vx(1.0), TY - 0.5, 36)]
        left = VGroup(swatch((66, 27, 15), -5.45, TY, w=0.4, h=0.5), swatch((102, 41, 23), -5.0, TY, w=0.4, h=0.5))
        left_l = a4_lab("stripes", -5.2, TY - 0.6, 32)
        right = swatch((31, 184, 133), 5.1, TY, w=0.8, h=0.6)
        right_l = a4_lab("green", 5.1, TY - 0.6, 32)
        knob = Dot([vx(0.0), TY, 0], radius=0.2, color=INK)
        kl = a4_mono("activation", vx(0.0), TY + 0.62, 28)
        kg = VGroup(knob, kl)
        pics = []
        for v, x in (("0.0", -3.9), ("0.5", 0.0), ("1.0", 3.9)):
            pics.append(framed(img(f"pantry/a4_padc_{v}.png", w=3.5, x=x, y=-1.5), color=DIM, pad=0.07))
        etag = a4_etag(-3.4, -3.05)
        stag = a4_stag("example, 14 Oct · Compatibility", 3.3, -3.05)

        self.play(Create(g.ring_row(10)), FadeIn(etag), run_time=0.4)
        until(self, "mix the stripe colour", lead=0.5)
        self.play(Create(track), FadeIn(left), FadeIn(left_l), FadeIn(stops), run_time=0.5)
        until(self, "toward the active colour", lead=0.5)
        self.play(FadeIn(right, scale=0.6), FadeIn(right_l), *[FadeIn(t) for t in tl], run_time=0.4)
        until(self, "by activation", lead=0.55)
        self.play(FadeIn(kg, shift=DOWN * 0.15), run_time=0.35)
        until(self, "At zero", lead=0.3)
        self.play(FadeIn(pics[0]), FadeIn(stag), run_time=0.4)
        until(self, "At half", lead=0.45)
        self.play(kg.animate.shift(RIGHT * (vx(0.5) - vx(0.0))), run_time=0.45)
        self.play(FadeIn(pics[1]), run_time=0.35)
        until(self, "At one", lead=0.45)
        self.play(kg.animate.shift(RIGHT * (vx(1.0) - vx(0.5))), run_time=0.45)
        self.play(FadeIn(pics[2]), run_time=0.35)
        done(self)


# ═════════════════════════ B29 · direct the driver and its test, plan first (the assignment's own prompt, documented, not run) ═════════════════════════
class B29_DriverPrompt(Scene):
    def construct(self):
        CX, CY, CW, CH = -1.6, 0.1, 9.0, 4.7
        card = RoundedRectangle(width=CW, height=CH, corner_radius=0.2, fill_color="#FFFFFF", fill_opacity=1, stroke_color=DIM, stroke_width=3).move_to([CX, CY, 0])
        card_l = a4_lab("the assignment's prompt", -3.9, 2.95, 34)
        to_arr = arrow([-1.45, 2.95, 0], [-0.6, 2.95, 0], w=6, tip=0.2)
        cc = chip("Claude Code", 1.1, 2.95, size=34)       # text chip: the Claude Code logo is a wide terracotta blob that GATE T reads as accent text (reported to the lead)
        tag = a4_stag("documented, not run", CX, -2.85)
        LX = CX - CW / 2 + 0.9                       # text left edge
        F = A4_SRC_PROMPT
        rows_y = [1.8, 0.95, 0.5, -0.3, -1.1, -1.85]
        rows = [a4_cell(F[i], LX, rows_y[i], 20) for i in range(6)]
        DX = CX - CW / 2 + 0.4
        dot = Dot([DX, rows_y[0], 0], radius=0.1, color=TERRA)
        IX = 4.75
        # one drawing per rule, in the prompt's own order: shader file with a prohibition, a plan page, the E key, three frame rates, the eye
        page1 = a4_paper(IX - 0.1, 1.8, w=0.62, h=0.72)
        l1 = VGroup(*[a4_scribble(IX - 0.34, 1.8 + dy, 0.48, amp=0.035, sw=3) for dy in (0.17, 0.0, -0.17)])
        no1 = a4_no(IX + 0.5, 1.6, r=0.27)
        page2 = a4_paper(IX - 0.1, 0.85, w=0.62, h=0.72)
        l2 = VGroup(*[a4_scribble(IX - 0.34, 0.85 + dy, 0.48, amp=0.035, sw=3) for dy in (0.17, 0.0, -0.17)])
        key = chip("E", IX, -0.3, w=0.95, size=40)
        rates = chip("30 · 60 · 144", IX - 0.1, -1.1, size=32)
        eye = eye_icon(IX, -1.85, s=0.55)

        self.play(FadeIn(card), FadeIn(card_l), GrowArrow(to_arr), FadeIn(cc, shift=DOWN * 0.1), FadeIn(tag), run_time=0.5)
        until(self, "forbids editing", lead=0.5)
        self.play(FadeIn(rows[0], shift=RIGHT * 0.1), FadeIn(dot, scale=0.5), FadeIn(VGroup(page1, l1)), Create(no1), run_time=0.45)
        until(self, "the smallest plan", lead=0.7)
        self.play(dot.animate.move_to([DX, rows_y[1], 0]), FadeIn(rows[1], shift=RIGHT * 0.1), FadeIn(VGroup(page2, l2)), run_time=0.4)
        until(self, "before any edit", lead=0.3)
        self.play(FadeIn(rows[2], shift=RIGHT * 0.1), run_time=0.3)
        until(self, "real input", lead=0.45)
        self.play(dot.animate.move_to([DX, rows_y[3], 0]), FadeIn(rows[3], shift=RIGHT * 0.1), FadeIn(key, shift=DOWN * 0.1), run_time=0.4)
        until(self, "three frame rates", lead=0.4)
        self.play(dot.animate.move_to([DX, rows_y[4], 0]), FadeIn(rows[4], shift=RIGHT * 0.1), FadeIn(rates, shift=DOWN * 0.1), run_time=0.4)
        until(self, "cannot prove", lead=0.85)
        self.play(dot.animate.move_to([DX, rows_y[5], 0]), FadeIn(rows[5], shift=RIGHT * 0.1), FadeIn(eye), run_time=0.4)
        done(self)


# ═════════════════════════ B30 · the driver is one line (garden.gd 4, 227-231, 253) ═════════════════════════
class B30_DriverLine(Scene):
    def construct(self):
        C = a4_Code(A4_SRC_GARDEN_4, first=4, x=-3.6, y=2.3, size=20, pitch=0.4, pad=0.25)
        A = a4_Code(A4_SRC_GARDEN_227, first=227, x=-1.5, y=0.35, size=20, pitch=0.4, pad=0.25)
        B = a4_Code(A4_SRC_GARDEN_253, first=253, x=0.0, y=-1.75, size=20, pitch=0.4, pad=0.25)
        gap = a4_gap(-5.4, -1.1)
        gd = a4_mono("garden.gd", 4.6, 2.3, 28)
        phys = a4_lab("physics tick", 4.7, 0.35, 34)
        etag = a4_etag(3.3, -3.05)
        line253 = A4_SRC_GARDEN_253[0].replace("\t", "    ")
        body = line253.strip()
        bt = B.rows[0][1]                                # the row text that is actually on screen (its glyphs are recoloured in place)
        i_act = body.index('"activation"')
        i_chg = body.index("charge / CHARGE_SECONDS")
        g_act = a4_glyphs(bt, body, i_act, i_act + len('"activation"'))
        g_chg = a4_glyphs(bt, body, i_chg, i_chg + len("charge / CHARGE_SECONDS"))
        g_rest = [m for m in bt if m not in g_act and m not in g_chg]
        rB = B.ring_row(253)
        until(self, "the driver is one line", lead=0.5)
        self.play(FadeIn(B, shift=UP * 0.1), FadeIn(gd), FadeIn(etag), run_time=0.45)
        self.play(Create(rB), run_time=0.3)
        until(self, "Each physics tick", lead=0.55)
        self.play(FadeIn(A, shift=UP * 0.1), FadeIn(gap), FadeIn(phys), run_time=0.45)
        until(self, "the game sets activation", lead=0.45)
        self.play(*a4_paint(g_rest, DIM), *a4_paint(g_chg, DIM), run_time=0.3)
        until(self, "charge divided", lead=0.35)
        self.play(*a4_paint(g_chg, INK), *a4_paint(g_act, DIM), run_time=0.3)
        until(self, "point six", lead=0.25)
        self.play(FadeIn(C, shift=DOWN * 0.1), run_time=0.4)
        # the second picture: the game owns the state, the shader only observes (three REAL lab frames; activation = charge / 0.6 from states.jsonl)
        fr = [framed(img(f"pantry/a4_labpadT_{f}.png", w=2.6, x=x, y=1.15), color=DIM, pad=0.06) for f, x in ((300, -3.8), (597, -0.6), (603, 2.6))]
        vals = [a4_lab(t, x, -0.15, 40) for t, x in (("0", -3.8), ("0.278", -0.6), ("0.611", 2.6))]
        up = arrow([-0.6, -1.2, 0], [-0.6, -0.6, 0], w=6, tip=0.2)
        stag = a4_stag("scripted input · earlier take, 14 Oct", -3.2, -3.05)
        eye = eye_icon(5.4, 1.5, s=0.55)
        eye_l = a4_lab("observes", 5.4, 0.75, 34)
        until(self, "The game owns", lead=0.6)
        self.play(*[FadeOut(m) for m in (A, C, gap, phys, gd)], rB.animate.set_opacity(0.0), *a4_paint(list(bt), INK), run_time=0.25)
        self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.1) for f in fr], lag_ratio=0.25), FadeIn(stag), run_time=0.6)
        self.play(*[FadeIn(v) for v in vals], GrowArrow(up), run_time=0.35)
        until(self, "only observes", lead=0.55)
        self.play(FadeIn(eye, scale=0.6), FadeIn(eye_l), run_time=0.35)
        done(self)


# ═════════════════════════ B31 · what the test does: ten checks (the real names from the re-run's log) ═════════════════════════
class B31_TenChecks(Scene):
    def construct(self):
        names = [t[len("PASS "):] for _, _, t in A4_SRC_LOG_B31]
        RX, RY0, RP = -2.35, 2.45, 0.45
        rows = [a4_cell(nm, RX, RY0 - RP * i, 24) for i, nm in enumerate(names)]
        ticks = [tick_mark(RX - 0.5, RY0 - RP * i, s=0.14, color=INK, w=6) for i in range(10)]
        key = chip("E", -5.0, 1.85, w=1.1, size=48)
        key_l = a4_lab("key event", -5.0, 1.05, 32)
        ten = T("10", 130).move_to([-5.0, -0.35, 0])
        ten_l = a4_lab("checks", -5.0, -1.2, 36)
        stag = a4_stag("re-run for this film", -3.2, -3.05)
        etag = a4_etag(3.4, -3.05)

        def press():
            return [key.animate.shift(DOWN * 0.1)]

        until(self, "sends real key events", lead=0.35)
        self.play(FadeIn(key, shift=DOWN * 0.1), FadeIn(key_l), FadeIn(stag), FadeIn(etag), run_time=0.3)
        until(self, "times the charge", lead=0.35)
        self.play(*press(), run_time=0.1)
        self.play(key.animate.shift(UP * 0.1), run_time=0.1)
        self.play(LaggedStart(*[FadeIn(VGroup(rows[i], ticks[i]), shift=RIGHT * 0.1) for i in range(3)], lag_ratio=0.3), run_time=0.7)
        until(self, "presses again mid-charge", lead=0.35)
        self.play(*press(), run_time=0.1)
        self.play(key.animate.shift(UP * 0.1), run_time=0.1)
        self.play(LaggedStart(*[FadeIn(VGroup(rows[i], ticks[i]), shift=RIGHT * 0.1) for i in range(3, 6)], lag_ratio=0.3), run_time=0.7)
        until(self, "pauses", lead=-0.05)
        self.play(FadeIn(VGroup(rows[6], ticks[6]), shift=RIGHT * 0.1), run_time=0.3)
        until(self, "resets", lead=0.15)
        self.play(FadeIn(VGroup(rows[7], ticks[7]), shift=RIGHT * 0.1), run_time=0.3)
        self.play(FadeIn(VGroup(rows[8], ticks[8]), shift=RIGHT * 0.1), run_time=0.3)
        until(self, "compares the uniform", lead=0.2)
        self.play(FadeIn(VGroup(rows[9], ticks[9]), shift=RIGHT * 0.1), run_time=0.3)
        until(self, "Ten checks", lead=0.9)
        self.play(FadeIn(ten, scale=0.7), FadeIn(ten_l), run_time=0.4)
        done(self)


# ═════════════════════════ B32 · 30 / 60 / 144 frames per second: 0.6 game seconds each time; headless draws nothing ═════════════════════════
A4_RATES = [(30, 16), (60, 34), (144, 83)]    # (fps, render_samples while charging): R2-driver-<fps>fps.log, the DURATION line, scale 1.0


class B32_ThreeRates(Scene):
    def construct(self):
        RX0, RX1 = -3.9, 2.9
        ys = [1.5, 0.1, -1.3]
        rulers, bars, labs, ends, verdicts, smp, dots = VGroup(), [], [], [], [], [], []
        for (fps, n), y in zip(A4_RATES, ys):
            base = Line([RX0, y, 0], [RX1, y, 0], color=DIM, stroke_width=5)
            ticks = VGroup(*[Line([RX0 + (RX1 - RX0) * i / (n - 1), y - 0.17, 0], [RX0 + (RX1 - RX0) * i / (n - 1), y + 0.17, 0], color=DIM, stroke_width=2.5)
                             for i in range(n)])
            rulers.add(VGroup(base, ticks))
            bar = Rectangle(width=RX1 - RX0, height=0.36, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([(RX0 + RX1) / 2, y, 0])
            bar.set_z_index(-1)
            bars.append(bar)
            labs.append(a4_lab(f"{fps} fps", -5.15, y, 36))
            ends.append(a4_lab("0.6 s", RX1, y + 0.5, 34))
            smp.append(a4_lab(f"{n} samples", -3.0, y - 0.5, 32, DIM))
            verdicts.append(VGroup(a4_lab("10 checks", 4.85, y + 0.2, 32), a4_lab("0 failures", 4.85, y - 0.22, 32)))
            dots.append(Dot([RX1, y, 0], radius=0.13, color=TERRA))
        stag = a4_stag("re-run for this film", -3.2, -3.05)
        etag = a4_etag(3.4, -3.05)

        until(self, "At thirty", lead=-0.05)
        self.play(LaggedStart(*[FadeIn(VGroup(labs[i], rulers[i], smp[i])) for i in range(3)], lag_ratio=0.2), FadeIn(stag), FadeIn(etag), run_time=1.0)
        until(self, "point six game seconds", lead=0.8)
        self.play(*[GrowFromEdge(b, LEFT) for b in bars], run_time=1.1, rate_func=linear)
        self.play(*[FadeIn(e) for e in ends], *[FadeIn(d, scale=0.4) for d in dots], run_time=0.3)
        until(self, "no failures", lead=0.55)
        self.play(*[FadeIn(v, shift=LEFT * 0.1) for v in verdicts], run_time=0.4)
        # the second picture: headless draws nothing, so it cannot say what colour the pad is
        until(self, "All headless", lead=0.35)
        self.play(*[FadeOut(m) for m in (rulers, *bars, *labs, *ends, *smp, *verdicts, *dots, stag)], run_time=0.3)
        empty = Rectangle(width=3.8, height=2.4, stroke_color=DIM, stroke_width=5, fill_opacity=0).move_to([-3.0, 0.8, 0])
        term = terminal_icon(-3.0, 0.8, s=0.6)
        nothing = a4_lab("nothing drawn", -3.0, -0.8, 36)
        self.play(Create(empty), FadeIn(term), FadeIn(nothing), run_time=0.45)
        q = T("?", 90).move_to([-0.2, 0.8, 0])
        pad = framed(img("pantry/a4_labpadT_300.png", w=3.1, x=3.0, y=0.8), color=DIM, pad=0.06)
        pad_l = a4_lab("the pad", 3.0, -0.95, 36)
        stag2 = a4_stag("scripted input · earlier take, 14 Oct", -3.2, -3.05)
        until(self, "what colour the pad is", lead=1.0)
        self.play(FadeIn(q), FadeIn(pad), FadeIn(pad_l), FadeIn(stag2), run_time=0.45)
        done(self)


# ═════════════════════════ B33 · mutation 1: delete a semicolon (re-run, evidence/runs/R4-M1-parse-60fps.log) ═════════════════════════
class B33_DeleteSemicolon(Scene):
    def construct(self):
        f = a4_Code(A4_SRC_SIGNAL[:1], first=1, x=-3.4, y=2.55, size=24, pitch=0.45, pad=0.25, min_cols=24)
        f_l = a4_mono("signal.gdshader", 2.9, 2.55, 28)
        semi = f.rows[0][1][-1]                                   # the last glyph of line 1: the semicolon
        L = [A4_SRC_CMD_B33] + [t for _, _, t in A4_SRC_LOG_B33[:6]] + ["..."] + [A4_SRC_LOG_B33[6][2]]
        L[0] = "$ " + L[0]
        g = a4_Code(L, first=1, x=0.0, y=-0.35, size=24, pitch=0.4, pad=0.25, numbers=False, show=[])
        rows = [g.txt_mob(i) for i in range(len(L))]
        # rows: 0 command, 1 SHADER ERROR, 2 UNIFORM_TYPES {}, 3-6 FAIL x4, 7 ..., 8 RESULT
        gap_dot = Dot([f.x_of(19) + 0.1, f.y_of(1) - 0.02, 0], radius=0.09, color=TERRA)
        ex = chip("exit 1", 4.3, g.y_of(1 + 8), mono=True, size=34)
        stag = a4_stag("re-run for this film", -3.2, -3.05)
        etag = a4_etag(3.4, -3.05)
        self.add(f)
        self.play(FadeIn(f_l), FadeIn(stag), FadeIn(etag), run_time=0.3)
        until(self, "delete a semicolon", lead=0.55)
        self.play(FadeOut(semi), FadeIn(gap_dot, scale=0.4), run_time=0.35)
        until(self, "fails to parse", lead=0.9)
        self.play(FadeIn(g.frame), run_time=0.2)
        self.play(FadeIn(rows[0], shift=RIGHT * 0.1), run_time=0.25)
        self.play(FadeIn(rows[1], shift=RIGHT * 0.1), run_time=0.25)
        until(self, "empty uniform list", lead=0.45)
        r2 = g.ring_row(1 + 2, grey=True)
        self.play(FadeIn(rows[2], shift=RIGHT * 0.1), Create(r2), run_time=0.35)
        self.play(LaggedStart(*[FadeIn(rows[i], shift=RIGHT * 0.1) for i in (3, 4, 5, 6)], lag_ratio=0.2), run_time=0.6)
        self.play(FadeIn(rows[7]), FadeIn(rows[8], shift=RIGHT * 0.1), run_time=0.3)
        until(self, "must exit one", lead=0.35)
        self.play(FadeIn(ex, shift=LEFT * 0.1), run_time=0.3)
        until(self, "Restore the file", lead=0.4)
        self.play(FadeOut(gap_dot), FadeIn(semi), run_time=0.35)
        done(self)


# ═════════════════════════ B34 · mutation 2: rename the driven uniform; the driver test still passes ═════════════════════════
class B34_RenameUniform(Scene):
    def construct(self):
        PY = 2.45                                                         # the pipe row
        pipe = Line([-5.8, PY, 0], [-2.0, PY, 0], color=DIM, stroke_width=14)
        send_l = a4_mono('"activation"', -4.4, PY + 0.6, 28)            # the string the game sends (garden.gd line 253)
        game_l = a4_lab("game", -4.4, PY - 0.62, 34)
        tipdot = Dot([-5.8, PY, 0], radius=0.14, color=TERRA)
        sock = Circle(radius=0.42, stroke_color=INK, stroke_width=7, fill_opacity=0).move_to([-1.55, PY, 0])
        sock_l = a4_mono("activation", -1.0, PY + 0.6, 28)
        sock_l2 = a4_mono("renamed_activation", 1.2, PY + 0.6, 28)
        shader_l = a4_lab("shader", -1.55, PY - 0.72, 34)
        shader_l2 = a4_lab("shader", 0.95, PY - 0.72, 34)
        no = cross_mark(-0.74, PY, s=0.26, color=INK, w=8)
        to_pad = DashedLine([1.55, PY, 0], [3.8, PY, 0], color=DIM, stroke_width=5, dash_length=0.2)
        pad = framed(img("pantry/a4_labpadT_300.png", w=1.8, x=4.9, y=PY), color=DIM, pad=0.05)
        # three real log cards, one width, one left edge
        CX = -2.25
        probe = a4_Code([A4_SRC_LOG_B34[0][2], A4_SRC_LOG_B34[1][2]], x=CX, y=0.75, size=20, pitch=0.4, numbers=False, min_cols=47)
        drv = a4_Code([A4_SRC_LOG_B34[2][2]], x=CX, y=-0.62, size=20, pitch=0.4, numbers=False, min_cols=47)
        con = a4_Code([A4_SRC_LOG_B34[3][2], A4_SRC_LOG_B34[4][2]], x=CX, y=-2.0, size=20, pitch=0.4, numbers=False, min_cols=47)
        probe_l, drv_l, con_l = a4_lab("probe", 5.0, 0.75, 34), a4_lab("driver", 5.0, -0.62, 34), a4_lab("contract", 5.0, -2.0, 34)
        ex0 = chip("exit 0", 2.85, -0.62, mono=True, size=34)
        ex1 = chip("exit 1", 2.85, -2.0, mono=True, size=34)
        stag = a4_stag("re-run for this film", -3.2, -3.05)
        etag = a4_etag(3.4, -3.05)
        pad_tag = a4_stag("scripted input", 4.9, PY - 1.12)

        self.play(Create(pipe), FadeIn(send_l), FadeIn(game_l), FadeIn(sock), FadeIn(sock_l), FadeIn(shader_l), FadeIn(stag), FadeIn(etag), run_time=0.5)
        until(self, "driven uniform", lead=0.45)
        self.play(FadeIn(tipdot, scale=0.5), run_time=0.15)
        self.play(tipdot.animate.move_to([-2.0, PY, 0]), run_time=0.5, rate_func=linear)
        until(self, "shader only", lead=0.5)
        self.play(sock.animate.shift(RIGHT * 2.5), FadeOut(sock_l), FadeOut(shader_l), FadeIn(sock_l2), FadeIn(shader_l2), run_time=0.5)
        self.play(Create(no), run_time=0.2)
        until(self, "Setting an undeclared", lead=0.35)
        self.play(FadeIn(VGroup(probe, probe_l), shift=UP * 0.1), run_time=0.4)
        until(self, "driver test still passed", lead=0.35)
        self.play(FadeIn(VGroup(drv, drv_l, ex0), shift=UP * 0.1), run_time=0.4)
        until(self, "pad would never change colour", lead=0.5)
        self.play(Create(to_pad), FadeIn(pad), FadeIn(pad_tag), run_time=0.4)
        until(self, "Only the uniform list", lead=0.45)
        self.play(FadeIn(VGroup(con, con_l, ex1), shift=UP * 0.1), run_time=0.4)
        self.play(Create(con.ring_row(1, grey=True)), run_time=0.3)
        done(self)
