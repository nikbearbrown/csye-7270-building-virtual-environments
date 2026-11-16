"""ACT III · Give the Agent Rules  (B19, B23, B24 Manim; B20, B21, B22 are Remotion CCPlainShell, see lanes/act3.json)

Cast of the act: the REAL wrapper script (evidence/runs/scripts/run-test.sh, verbatim from the assignment; B19), the example's own CLAUDE.md
(evidence/example/sources/CLAUDE.md; B23), the assignment's own claude -p flag line (documented, not run; B24) and the commit chain.
Every line of code on screen is copied from those files (checked by evidence/act3/verify_lines.py); nothing is typed from memory.
SOFT WRAP: the wrapper's line 6 is 101 characters and its line 8 is 66; no type size at or above the floor shows 101 characters on this frame.
So a long line is shown as an editor shows it: broken at a space into indented continuation rows (a hook in the gutter, no line number), no character
added, none dropped; joined with single spaces the rows are the real line (verify_lines.py checks it). The flag line in B24 is broken after a comma, so its rows join with no space.
"""

A3_CW = {20: 0.15, 24: 0.20}      # Menlo, units per character (kit code_block, measured on this Mac)


def a3_lab(s, x, y, size=34, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a3_code(spec, x=0.0, y=0.0, size=24, pad=0.3, indent=0.4, numbers=True, lh=None):
    """Real code in Menlo with an outline frame (like kit code_block) that also soft-wraps: spec = [(label, text), ...] where label is the REAL line
    number (str) or None for a continuation row. Returns a VGroup with .frame .rows (VGroup(num-or-hook, text) per row) .W .H .lh and .row_y(i), .text_left(i)."""
    cw = A3_CW[size]
    lh = lh or size / 32 * 0.46
    labs = [l for l, _ in spec if l]
    nw = (max(len(l) for l in labs) * cw + 0.25) if numbers else 0.0
    texts = [M(t, size) for _, t in spec]
    tw = max(len(t) * cw + (indent if l is None else 0.0) for l, t in spec)       # widths from character counts: the Gate A stub's Text.width is wrong
    W = tw + nw + 2 * pad
    H = len(spec) * lh + 2 * pad
    frame = RoundedRectangle(width=W, height=H, corner_radius=0.14, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
    left = x - W / 2 + pad
    rows = VGroup()
    for i, ((lab, _), t) in enumerate(zip(spec, texts)):
        yy = y + H / 2 - pad - lh * (i + 0.5)
        tl = left + nw + (indent if lab is None else 0.0)
        t.move_to([tl + len(spec[i][1]) * cw / 2, yy, 0])
        if lab is not None:
            n = M(lab, size, DIM).move_to([left + (len(lab) * cw) / 2, yy, 0]) if (numbers and lab) else VGroup()
        else:
            gx = left + 0.12
            n = VGroup(Line([gx, yy + 0.09, 0], [gx, yy - 0.03, 0], color=DIM, stroke_width=3),
                       Line([gx, yy - 0.03, 0], [gx + 0.22, yy - 0.03, 0], color=DIM, stroke_width=3))
        rows.add(VGroup(n, t))
    g = VGroup(frame, rows)
    g.frame, g.rows, g.W, g.H, g.lh, g.x_, g.y_ = frame, rows, W, H, lh, x, y
    g.row_y = lambda i: y + H / 2 - pad - lh * (i + 0.5)
    return g


def a3_bracket(g, i0, i1, off=0.25, color=INK, w=5):
    """A right-margin bracket '[' mirrored: spans rows i0..i1 of block g. Never touches text (sits 0.25 outside the frame)."""
    xb = g.x_ + g.W / 2 + off
    ya = g.row_y(i0) + g.lh * 0.42
    yb = g.row_y(i1) - g.lh * 0.42
    return VGroup(Line([xb, ya, 0], [xb, yb, 0], color=color, stroke_width=w),
                  Line([xb - 0.13, ya, 0], [xb, ya, 0], color=color, stroke_width=w),
                  Line([xb - 0.13, yb, 0], [xb, yb, 0], color=color, stroke_width=w))


# ── B19 · the wrapper script: four jobs ──────────────────────────────────────────────────────────────────────────────────
A3_WRAP = [("1", "#!/usr/bin/env bash"),
           ("2", "# scripts/run-test.sh <test-file.gd> <fps>"),
           ("3", "set -o pipefail"),
           ("4", "mkdir -p logs"),
           ("5", 'log="logs/$(basename "$1" .gd)_${2}fps.log"'),
           ("6", "timeout 120 godot --headless --path godot"),
           (None, '--script "res://tests/$1" --fixed-fps "$2"'),
           (None, '2>&1 | tee "$log"'),
           ("7", "status=$?"),
           ("8", 'if grep -qE "SHADER ERROR|SCRIPT ERROR" "$log";'),
           (None, "then status=1; fi"),
           ("9", "exit $status")]


class B19_Wrapper(Scene):
    def construct(self):
        title = T("Give  the  Agent  Rules", 40).move_to([-3.75, 2.95, 0])
        tag = status_tag("from the assignment", 4.1, 3.0)
        blk = a3_code(A3_WRAP, x=-0.55, y=-0.1)
        self.add(title, tag, blk.frame)
        until(self, "commit one wrapper script", lead=0.5)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in blk.rows], lag_ratio=0.12), run_time=1.6)
        jobs = [("1", "timeout", [[5]], "a timeout", 0.55),
                ("2", "frame rate", [[6]], "pins the frame rate", 0.7),
                ("3", "log", [[4], [7]], "keeps a log", 0.55),
                ("4", "fails on errors", [[9, 10]], "fails on any shader error", 0.7)]
        # legend, left to right along the bottom
        nw_ = {"1": 0.154, "2": 0.207, "3": 0.184, "4": 0.219}                     # measured EB Garamond 34 widths (real Manim)
        lw_ = {"timeout": 1.428, "frame rate": 1.811, "log": 0.549, "fails on errors": 2.426}
        widths = [nw_[n] + 0.35 + lw_[l] for n, l, _, _, _ in jobs]
        gap = 0.8
        x0 = -(sum(widths) + gap * 3) / 2
        for (num, lab, spans, cue, lead), w in zip(jobs, widths):
            until(self, cue, lead=lead)
            brs, nums = [], []
            for sp in spans:
                br = a3_bracket(blk, sp[0], sp[-1])
                xb = blk.x_ + blk.W / 2 + 0.25
                yc = (blk.row_y(sp[0]) + blk.row_y(sp[-1])) / 2
                nm = T(num, 32).move_to([xb + 0.42, yc, 0])
                brs.append(br); nums.append(nm)
            ln = T(num, 34).move_to([x0 + nw_[num] / 2, -3.05, 0])
            ll = T(lab, 34).move_to([x0 + nw_[num] + 0.35 + lw_[lab] / 2, -3.05, 0])
            dot = Dot([x0 - 0.3, -3.05, 0], radius=0.1, color=TERRA)
            self.play(*[Create(b) for b in brs], *[FadeIn(n) for n in nums], FadeIn(ln), FadeIn(ll), FadeIn(dot, scale=0.5), run_time=0.45)
            x0 += w + gap
        done(self)


# ── B23 · step one: the agent drafts the project context file (the example's REAL CLAUDE.md, 65 lines) ───────────────────
# Lines shown are real lines 1-5 and 22 of evidence/example/sources/CLAUDE.md (a gap row marks the lines left out). Line 10 of that file says
# "Assignments 1-9", so the prose block (lines 7-13) is left out on purpose. Size 20: line 22 is 67 characters.
A3_CLAUDEMD = [("1", "@AGENTS.md"),
               ("2", "@CHANGE-BRIEF.md"),
               ("3", "@assignments/05-shaders-materials/CHANGE-BRIEF.md"),
               ("4", " "),
               ("5", "# Signal Garden context"),
               ("", "\u2026"),
               ("22", "The quiet/active colors and eight stripes are in `signal.gdshader`.")]


class B23_ContextFile(Scene):
    def construct(self):
        blk = a3_code(A3_CLAUDEMD, x=0.0, y=0.75, size=20, lh=0.4)
        fname = M("CLAUDE.md", 28).move_to([-4.95, 2.95, 0])
        tag = example_tag(x=3.05, y=3.0)
        self.add(fname, blk.frame)
        until(self, "drafts the project context file", lead=0.9)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in blk.rows], lag_ratio=0.1), FadeIn(tag), run_time=1.3)
        # a fact with a file reference: ring the whole of real line 22 (it names signal.gdshader)
        until(self, "each with a file reference", lead=0.6)
        r22 = RoundedRectangle(width=blk.W - 0.3, height=blk.lh - 0.1, corner_radius=0.1, stroke_color=TERRA, stroke_width=6, fill_opacity=0).move_to([blk.x_, blk.row_y(6), 0])
        fr = T("file reference", 34).move_to([4.3, blk.row_y(6) - 0.95, 0])
        self.play(Create(r22), FadeIn(fr), run_time=0.5)
        # under 120 lines: a 120-wide bar, 65 filled
        until(self, "under a hundred twenty lines", lead=0.55)
        bx0, by, bw = -3.6, -2.3, 8.0
        outline = RoundedRectangle(width=bw, height=0.36, corner_radius=0.1, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([bx0 + bw / 2, by, 0])
        fill = Rectangle(width=bw * 65 / 120, height=0.28, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([bx0 + bw * 65 / 240, by, 0])
        n65 = T("65", 48).move_to([bx0 + bw * 65 / 120, by - 0.65, 0])
        n120 = T("120", 48).move_to([bx0 + bw, by - 0.65, 0])
        ln = T("lines", 34).move_to([-4.85, by, 0])
        tip = Dot([bx0 + bw * 65 / 120, by + 0.3, 0], radius=0.1, color=TERRA)
        self.play(Create(outline), FadeIn(ln), run_time=0.35)
        self.play(GrowFromEdge(fill, LEFT), FadeIn(n65), FadeIn(tip, scale=0.5), FadeIn(n120), run_time=0.6)
        # importing the brief, not pasting it
        until(self, "importing your change brief", lead=0.5)
        imp = T("imports your brief", 34).move_to([-1.9, 2.95, 0])
        yr = (blk.row_y(1) + blk.row_y(2)) / 2
        rr = VGroup(*[RoundedRectangle(width=blk.W - 0.3, height=blk.lh - 0.1, corner_radius=0.1, stroke_color=TERRA, stroke_width=6, fill_opacity=0).move_to([blk.x_, blk.row_y(i), 0])
                      for i in (1, 2)])
        arr = Arrow([-1.9, 2.7, 0], [-1.9, yr + blk.lh + 0.05, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2, max_tip_length_to_length_ratio=0.5)
        self.play(FadeIn(imp), run_time=0.3)
        self.play(GrowArrow(arr), *[Create(r) for r in rr], run_time=0.5)
        done(self)


# ── B24 · commit the draft unedited, then your review, separately; scope the session ─────────────────────────────────────
# The commit chain is a DRAWING of the assignment's order (agent draft, then your review); it is not the example's git history. The flag line is the
# assignment's own claude -p text (the --allowedTools flag only), shown as documented, not run, soft-wrapped after a comma (no character added).
A3_FLAG = [("\u2026", '--allowedTools "Read,Write,Glob,Grep,Bash(git status:*),'),
           (None, 'Bash(git diff:*),Bash(git log:*),Bash(ls:*)"')]


class B24_CommitAndScope(Scene):
    def construct(self):
        n1, n2 = np.array([-3.6, 1.0, 0.0]), np.array([-0.7, 1.0, 0.0])
        agent = logo_chip("claude", n1[0], 2.4, h=1.1)      # the Claude mark (LOGO LAW: claude-01); the claude-code mascot logo is a wide terracotta blob that GATE T reads as accent text
        me = professor_bear("1x1", 1.15, seed="B24", x=n2[0], y=2.4, shape="circle")
        node1 = Circle(radius=0.2, stroke_color=INK, stroke_width=5, fill_color=CARD, fill_opacity=1).move_to(n1)
        node2 = Circle(radius=0.2, stroke_color=INK, stroke_width=5, fill_color=CARD, fill_opacity=1).move_to(n2)
        link = Line(n1 + RIGHT * 0.2, n2 + LEFT * 0.2, color=INK, stroke_width=5)
        l_draft = T("draft", 34).move_to([n1[0], 0.4, 0])
        l_uned = T("unedited", 34).move_to([n1[0], -0.05, 0])
        l_rev = T("review", 34).move_to([n2[0], 0.4, 0])
        until(self, "Commit the draft", lead=0.3)
        self.play(FadeIn(agent, shift=DOWN * 0.2), GrowFromCenter(node1), FadeIn(l_draft), run_time=0.45)
        until(self, "unedited", lead=0.2)
        self.play(FadeIn(l_uned), run_time=0.3)
        until(self, "then your review", lead=0.15)
        self.play(Create(link), GrowFromCenter(node2), FadeIn(me), FadeIn(l_rev), run_time=0.55)
        # what the recorded draft got wrong (the assignment's own recorded run)
        until(self, "cited wrong lines", lead=0.7)
        tag = status_tag("recorded in the assignment", 3.45, 2.95)
        c1 = cross_mark(2.0, 1.75, 0.17)
        w1 = T("wrong lines", 34).move_to([3.47, 1.75, 0])
        self.play(FadeIn(tag), Create(c1), FadeIn(w1), run_time=0.4)
        until(self, "a headless test would settle the look", lead=0.9)
        c2 = cross_mark(2.0, 0.85, 0.17)
        w2 = T("headless settles look", 34).move_to([4.26, 0.85, 0])
        self.play(Create(c2), FadeIn(w2), run_time=0.4)
        # scope the session: the assignment's allowed-tools list, git read-only
        until(self, "Scope the session too", lead=0.2)
        flag = a3_code(A3_FLAG, x=-0.2, y=-1.45, size=24)
        dots2 = M("…", 24, DIM).move_to([-0.2 - flag.W / 2 + 0.3 + 0.45 + 0.4 + 44 * 0.2 + 0.35, flag.row_y(1), 0])   # after the real line's last character
        st = status_tag("documented, not run", 4.1, -0.3)
        self.play(Create(flag.frame), FadeIn(flag.rows), FadeIn(dots2), FadeIn(st), run_time=0.5)
        until(self, "an agent allowed all of git", lead=0.2)
        gchip = chip("git:*", -3.4, -2.75, mono=True, size=34)
        gx = cross_mark(-1.85, -2.75, 0.2)
        gl = T("not allowed", 34).move_to([-0.35, -2.75, 0])
        self.play(FadeIn(gchip), Create(gx), FadeIn(gl), run_time=0.5)
        done(self)
