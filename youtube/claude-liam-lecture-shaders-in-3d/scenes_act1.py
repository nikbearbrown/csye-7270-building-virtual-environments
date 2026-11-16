"""ACT I · Same Shape, New Names  (B02 B03 B04 B05 B09, all Manim; the kit is pasted above this file by assemble_scenes.py)

Cast for the act: the skeleton code card (lab-shaders/03-skeleton-3d.gdshader, typed in here so scenes.py stands alone), the teal flat square and its
four terracotta corner dots, the teal cube (the same teal, 0.37 0.64 0.57), the pixel grid of outline cells. Code is typed word by word at exact monospace
columns (Menlo is 0.2496 wide per character at size 32) so Pango can never fuse a space; every token sits on one shared baseline.
"""

A1_CW = 0.24962           # width of one Menlo character at size 32 (measured)
A1_LH = 0.40              # line pitch of the act's code cards
A1_TEAL_D = "#4A8A79"; A1_TEAL_L = "#86BFAE"


def a1_toks(line, left, ybase, size=32):
    """The words of one code line, each a VGroup of glyphs, on the baseline ybase; word k starts at its exact column. Returns a list of VGroups."""
    out = []
    col = 0
    for w in line.replace("\t", "  ").split(" "):
        if w:
            t = Text("H" + w + "H", font=MONO, color=INK, font_size=size)
            if len(t.submobjects) >= len(w) + 2:
                h0 = t.submobjects[0]
                t.shift([left + (col - 0.5) * A1_CW - h0.get_center()[0], ybase - h0.get_bottom()[1], 0])
                out.append(VGroup(*t.submobjects[1:-1]))
            else:                                    # (static-check stub without glyph children)
                out.append(M(w, size).move_to([left + (col + len(w) / 2.0) * A1_CW, ybase + 0.16, 0]))
        col += len(w) + 1
    return out


def a1_card(lines, xc, yc, ncols=None, lh=0.46, blank=0.22, pad_l=0.6, pad_r=0.35):
    """A white code card with the lines typed as word tokens (blank lines are thinner). Returns VGroup(frame, *tokens) with .frame, .tok (list per line of
    token VGroups), .left, .base (baselines), .cy (line centres), .W, .H."""
    ncols = ncols or max(len(l.replace("\t", "  ")) for l in lines)
    pitch = [lh if ln.strip() else blank for ln in lines]
    W = ncols * A1_CW + pad_l + pad_r
    H = sum(pitch) + 0.3
    frame = RoundedRectangle(width=W, height=H, corner_radius=0.14, stroke_color=DIM, stroke_width=4).set_fill(PALEBOX, opacity=1).move_to([xc, yc, 0])
    left = xc - W / 2 + pad_l
    y = yc + H / 2 - 0.15
    toks, bases, cys = [], [], []
    for i, ln in enumerate(lines):
        cy = y - pitch[i] / 2
        y -= pitch[i]
        cys.append(cy); bases.append(cy - 0.16)
        toks.append(a1_toks(ln, left, cy - 0.16))
    g = VGroup(frame, *[t for row in toks for t in row])
    g.frame = frame; g.tok = toks; g.left = left; g.base = bases; g.cy = cys; g.W = W; g.H = H
    return g


def a1_cap(s, x, y):
    return T(s, 32).move_to([x, y, 0])


def a1_bracket(x, y0, y1, color=INK):
    """A right-hand square bracket from y0 (top) down to y1, opening towards the code."""
    return VGroup(Line([x - 0.14, y0, 0], [x, y0, 0], color=color, stroke_width=6), Line([x, y0, 0], [x, y1, 0], color=color, stroke_width=6),
                  Line([x, y1, 0], [x - 0.14, y1, 0], color=color, stroke_width=6))


def a1_cube(x, y, s=1.0, faces=True):
    """An isometric cube in the series teal with faint triangle edges. s is the half-width of the hexagon."""
    cx, cy = x, y
    dx, dy = s, s * 0.5
    top = Polygon([cx, cy + s, 0], [cx + dx, cy + dy, 0], [cx, cy, 0], [cx - dx, cy + dy, 0], fill_color=A1_TEAL_L, fill_opacity=1, stroke_color=INK, stroke_width=3)
    left = Polygon([cx - dx, cy + dy, 0], [cx, cy, 0], [cx, cy - s, 0], [cx - dx, cy - dy, 0], fill_color=TEAL, fill_opacity=1, stroke_color=INK, stroke_width=3)
    right = Polygon([cx + dx, cy + dy, 0], [cx, cy, 0], [cx, cy - s, 0], [cx + dx, cy - dy, 0], fill_color=A1_TEAL_D, fill_opacity=1, stroke_color=INK, stroke_width=3)
    g = VGroup(top, left, right)
    if faces:
        g.add(Line([cx, cy + s, 0], [cx, cy, 0], color=GHOST, stroke_width=2), Line([cx - dx, cy + dy, 0], [cx, cy - s, 0], color=GHOST, stroke_width=2),
              Line([cx + dx, cy + dy, 0], [cx, cy - s, 0], color=GHOST, stroke_width=2))
    return g


def a1_lamp(x, y, color=INK):
    """A drawn bulb with rays pointing down. Returns VGroup with .bulb and .rays."""
    bulb = Circle(radius=0.2, stroke_color=color, stroke_width=4).move_to([x, y, 0])
    base = Line([x - 0.1, y - 0.28, 0], [x + 0.1, y - 0.28, 0], color=color, stroke_width=5)
    rays = VGroup(*[Line([x + 0.34 * np.cos(a), y + 0.34 * np.sin(a), 0], [x + 0.5 * np.cos(a), y + 0.5 * np.sin(a), 0], color=GOLD, stroke_width=4)
                    for a in np.radians([180, 225, 270, 315, 360])])
    g = VGroup(bulb, base, rays)
    g.bulb = bulb; g.rays = rays
    return g


# ═════════════════════════════════════════ B02 ═════════════════════════════════════════
class B02_Anatomy(Scene):
    """The skeleton file: a program counter steps down it, then three brackets say its shape: a first line, up to three functions, dials."""

    def construct(self):
        src = ["shader_type spatial;", "", "uniform float amount;", "", "void vertex() {", "}", "", "void fragment() {", "}", "", "void light() {", "}"]
        # the file has 12 lines; line 3 is the uniform (the dial), lines 5 to 12 the three functions
        card = a1_card(src, -2.5, -0.72, ncols=20, lh=0.5, blank=0.2)
        c1 = a1_cap("shader: a small program the graphics card", 0, 2.95)
        c2 = a1_cap("runs to decide how something is drawn", 0, 2.45)
        self.add(card, c1, c2)
        dot = Dot([card.frame.get_left()[0] + 0.3, card.cy[0], 0], radius=0.11, color=TERRA).set_stroke(DIM, width=3)
        self.play(FadeIn(dot), run_time=0.4)
        for ln in (2, 4, 7, 10):                       # zero-based: uniform, vertex, fragment, light
            self.play(dot.animate.move_to([dot.get_center()[0], card.cy[ln], 0]), run_time=0.32)
            self.wait(0.22)
        self.play(FadeOut(dot), run_time=0.3)
        bx = card.frame.get_right()[0] + 0.45
        lx = bx + 0.3
        until(self, "a first line")
        b1 = a1_bracket(bx, card.cy[0] + 0.17, card.cy[0] - 0.17)
        l1 = T("type", 32).move_to([lx + 0.4, card.cy[0], 0])
        self.play(Create(b1), FadeIn(l1), run_time=0.7)
        until(self, "up to three functions")
        b2 = a1_bracket(bx, card.cy[4] + 0.2, card.cy[11] - 0.2)
        l2 = T("functions", 32).move_to([lx + 0.75, (card.cy[4] + card.cy[11]) / 2, 0])
        self.play(Create(b2), FadeIn(l2), run_time=0.8)
        until(self, "dials")
        b3 = a1_bracket(bx, card.cy[2] + 0.17, card.cy[2] - 0.17)
        l3 = T("dials", 32).move_to([lx + 0.5, card.cy[2], 0])
        dc = np.array([bx + 2.2, card.cy[2], 0])
        dial = Circle(radius=0.38, stroke_color=INK, stroke_width=5).move_to(dc)
        tick = VGroup(Line(dc, dc + np.array([0, 0.3, 0]), color=INK, stroke_width=5), Dot(dc + np.array([0, 0.3, 0]), radius=0.1, color=TERRA).set_stroke(DIM, width=3))
        hub = Dot(dc, radius=0.06, color=INK)
        self.play(Create(b3), FadeIn(l3), Create(dial), Create(tick), FadeIn(hub), run_time=0.5)
        self.play(Rotate(tick, angle=-TAU * 0.75, about_point=dc), run_time=0.8)
        done(self)


# ═════════════════════════════════════════ B03 ═════════════════════════════════════════
class B03_TwoTypes(Scene):
    """The first line names the type: canvas_item is replaced by spatial and the flat square becomes a cube."""

    def construct(self):
        left = -2.5
        ybase = 1.45
        w_type = a1_toks("shader_type", left, ybase)[0]
        w_a = a1_toks("            canvas_item;", left, ybase)[0]
        w_b = a1_toks("            spatial;", left, ybase)[0]
        cap = a1_cap("shader type: the first line; says what the shader is for", 0, 2.75)
        sq = Square(side_length=2.1, stroke_color=INK, stroke_width=5, fill_color=TEAL, fill_opacity=1).move_to([0, -0.7, 0])
        lab2 = T("2D", 32).move_to([0, -2.45, 0])
        self.add(cap, w_type, w_a, sq, lab2)
        until(self, "Canvas item means two-D")
        self.play(Indicate(w_a, scale_factor=1.06, color=INK), run_time=0.7)
        until(self, "three-D, where the shader", lead=0.0)
        w_b.shift([0, 0.5, 0]).set_opacity(0)
        cube = a1_cube(0, -0.7, 1.15)
        lab3 = T("3D", 32).move_to([0, -2.45, 0])
        self.play(w_a.animate.shift([0, -0.5, 0]).set_opacity(0), w_b.animate.shift([0, -0.5, 0]).set_opacity(1), ReplacementTransform(sq, cube),
                  ReplacementTransform(lab2, lab3), run_time=1.1)
        until(self, "the points and triangles")
        mesh = T("mesh", 32).move_to([3.4, -0.7, 0])
        arr = arrow([2.75, -0.7, 0], [1.55, -0.7, 0])
        self.play(FadeIn(mesh), GrowArrow(arr), run_time=0.7)
        done(self)


# ═════════════════════════════════════════ B04 ═════════════════════════════════════════
class B04_ThreeFunctions(Scene):
    """Counts as motion: four corner dots flash 1 to 4, the covered cells tint one by one, two lamps brighten the cells in turn."""

    def construct(self):
        cy = 0.2
        quad = vertex_quad(3.0, 2.2, -4.0, cy)
        grid = pixel_grid(12, 8, 0.4, 3.3, cy)
        foot = vertex_quad(2.4, 1.6, 3.3, cy)
        foot_out = Rectangle(width=2.4, height=1.6, stroke_color=INK, stroke_width=5).move_to([3.3, cy, 0])
        cap1 = a1_cap("vertex: a corner point of a shape", 0, -2.55)
        cap2 = a1_cap("pixel: one dot of the picture on screen", 0, -3.05)
        qbody = quad.body.set_fill(TEAL, opacity=0.9)
        self.add(qbody, grid, foot_out, cap1, cap2)
        until(self, "Vertex runs")
        vlab = M("vertex()", 32).move_to([-4.0, -1.85, 0])
        nums = [("1", [-5.95, cy + 1.45]), ("2", [-2.05, cy + 1.45]), ("3", [-2.05, cy - 1.45]), ("4", [-5.95, cy - 1.45])]
        self.play(FadeIn(vlab), run_time=0.4)
        for d, (s, p) in zip(quad.corners, nums):
            n = T(s, 32).move_to([p[0], p[1], 0])
            self.play(FadeIn(d, scale=0.4), FadeIn(n), run_time=0.45)
            self.play(Indicate(d, scale_factor=1.7, color=TERRA), run_time=0.4)
        until(self, "pixel the mesh covers", lead=0.9)
        flab = M("fragment()", 32).move_to([2.2, -1.85, 0])
        covered = fill_in(grid, foot, TEAL)
        self.play(FadeIn(flab), run_time=0.3)
        self.play(LaggedStart(*covered, lag_ratio=0.1), run_time=1.9)
        until(self, "Light runs")
        l1 = a1_lamp(2.3, 2.75)
        l2 = a1_lamp(4.3, 2.75)
        lt = M("light()", 32).move_to([4.9, -1.85, 0])
        cells = [s for row in grid.cells for s in row if min(p[0] for p in foot.pts) <= s.get_center()[0] <= max(p[0] for p in foot.pts)
                 and min(p[1] for p in foot.pts) <= s.get_center()[1] <= max(p[1] for p in foot.pts)]
        self.play(FadeIn(l1), FadeIn(lt), run_time=0.4)
        self.play(*[c.animate.set_fill("#A9D8CB", 1) for c in cells], Indicate(l1.rays, color=GOLD), run_time=0.7)
        until(self, "for every light")
        self.play(FadeIn(l2), run_time=0.3)
        self.play(*[c.animate.set_fill("#D2EDE4", 1) for c in cells], Indicate(l2.rays, color=GOLD), run_time=0.7)
        done(self)


# ═════════════════════════════════════════ B05 ═════════════════════════════════════════
def a1_ubar(mob, pad=0.08):
    """terracotta underline bar over a grey backing (a bar, never text): the emphasis mark that does not read as accent text"""
    w = mob.width + 2 * pad
    return VGroup(Rectangle(width=w, height=0.2, stroke_width=0).set_fill(DIM, opacity=0.55).move_to(mob.get_bottom() + DOWN * 0.18),
                  Rectangle(width=w, height=0.12, stroke_width=0).set_fill(TERRA, opacity=1).move_to(mob.get_bottom() + DOWN * 0.18))


class B05_CodeMorph(Scene):
    """The 2D file and the 3D file, line for line: COLOR becomes ALBEDO, vec4 becomes vec3, the alpha number goes."""

    def construct(self):
        cw = A1_CW
        top_src = ["shader_type canvas_item;", "", "void fragment() {", "  COLOR = vec4(0.37, 0.64, 0.57, 1.0);", "}"]
        bot_src = ["shader_type spatial;", "", "void fragment() {", "  COLOR = vec4(0.37, 0.64, 0.57, 1.0);", "}"]
        top = a1_card(top_src, 0.0, 1.85, ncols=38, lh=0.5, blank=0.24, pad_r=0.6)
        bot = a1_card(bot_src, 0.0, -0.95, ncols=38, lh=0.5, blank=0.24, pad_r=0.6)
        self.add(top, bot)
        xin = bot.frame.get_right()[0] - 1.4            # empty space inside the card, right of the short lines

        def under(txt, x):
            lab = T(txt, 32).move_to([x, -2.65, 0])
            return VGroup(lab, Line([x, -2.42, 0], [x, -2.2, 0], color=DIM, stroke_width=4))
        # the first lines already differ (canvas_item above, spatial below): label 'type'
        ltype = T("type", 32).move_to([xin, bot.cy[0], 0])
        self.play(FadeIn(ltype), run_time=0.4)
        color, eq, v4, n2, n3, n4 = bot.tok[3]           # COLOR, =, vec4(0.37,, 0.64,, 0.57,, 1.0);
        until(self, "the output")
        albedo = a1_toks("  ALBEDO", bot.left, bot.base[3])[0]
        r1 = a1_ubar(color, pad=0.06)
        lout = under("output", color.get_center()[0] + 0.1)
        self.play(Create(r1), FadeIn(lout), run_time=0.4)
        rest = [eq, v4, n2, n3, n4]
        self.play(ReplacementTransform(color, albedo), r1.animate.become(a1_ubar(albedo)), *[m.animate.shift([cw, 0, 0]) for m in rest], run_time=0.8)
        self.play(FadeOut(r1), run_time=0.3)
        until(self, "four numbers")
        nums = VGroup(v4, n2, n3, n4)
        r2 = a1_ubar(nums, pad=0.05)
        lfour = under("four numbers", nums.get_center()[0])
        self.play(FadeOut(lout), run_time=0.2)
        self.play(Create(r2), FadeIn(lfour), run_time=0.5)
        until(self, "and alpha")
        cap = a1_cap("alpha: how visible a pixel is: 0 invisible, 1 solid", 0, -3.15)
        r3 = a1_ubar(n4, pad=0.05)
        self.play(Transform(r2, r3), FadeOut(lfour), run_time=0.5)
        self.play(FadeIn(cap), run_time=0.4)
        until(self, "three numbers")
        v3 = a1_toks("vec3(0.37,", bot.left + 11 * cw, bot.base[3])[0]
        end57 = a1_toks("0.57);", bot.left + 28 * cw, bot.base[3])[0]
        l3 = under("three numbers", (v4.get_left()[0] + n3.get_right()[0]) / 2)
        self.play(FadeOut(r2), ReplacementTransform(v4, v3), ReplacementTransform(n3, end57), FadeOut(n4), FadeIn(l3), run_time=0.8)
        until(self, "Alpha becomes")
        chip = VGroup(box(0, 0, 1.7, 0.48, color=INK, sw=3, radius=0.24), T("ALPHA", 32)).move_to([xin - 0.1, bot.cy[2] + 0.1, 0])
        self.play(FadeIn(chip, shift=LEFT * 0.3), run_time=0.5)
        done(self)


# ═════════════════════════════════════════ B09 ═════════════════════════════════════════
def a1_file_icon(x, y, h=0.9):
    w = h * 0.78
    c = h * 0.28
    page = Polygon([x - w / 2, y + h / 2, 0], [x + w / 2 - c, y + h / 2, 0], [x + w / 2, y + h / 2 - c, 0], [x + w / 2, y - h / 2, 0], [x - w / 2, y - h / 2, 0],
                   stroke_color=INK, stroke_width=4, fill_color=PALEBOX, fill_opacity=1)
    fold = VGroup(Line([x + w / 2 - c, y + h / 2, 0], [x + w / 2 - c, y + h / 2 - c, 0], color=INK, stroke_width=4),
                  Line([x + w / 2 - c, y + h / 2 - c, 0], [x + w / 2, y + h / 2 - c, 0], color=INK, stroke_width=4))
    return VGroup(page, fold)


class B09_AttachChain(Scene):
    """Three boxes link left to right: mesh instance, ShaderMaterial, shader. The slot tab lands on the first link; a dot travels back to the node."""

    def construct(self):
        xs = [-4.5, 0.0, 4.5]
        bw, bh = 3.3, 2.5
        b1 = box(xs[0], 0.2, bw, bh); b2 = box(xs[1], 0.2, bw, bh); b3 = box(xs[2], 0.2, bw, bh)
        cube = a1_cube(xs[0], 0.55, 0.55)
        t1 = T("mesh instance", 32).move_to([xs[0], -0.55, 0])
        t2 = T("ShaderMaterial", 32).move_to([xs[1], 0.2, 0])
        fic = a1_file_icon(xs[2], 0.65, 0.85)
        t3 = T("shader", 32).move_to([xs[2], -0.05, 0])
        t3b = M(".gdshader", 32).move_to([xs[2], -0.6, 0])
        g1 = VGroup(b1, cube, t1); g2 = VGroup(b2, t2); g3 = VGroup(b3, fic, t3, t3b)
        cap1 = a1_cap("mesh instance: the node that draws a mesh", 0, -2.35)
        cap2 = a1_cap("ShaderMaterial: a material that holds your shader and its settings", 0, -2.9)
        self.play(FadeIn(g1, shift=RIGHT * 0.4), FadeIn(cap1), run_time=0.5)
        until(self, "a shader material")
        lk1 = arrow([xs[0] + bw / 2 + 0.05, 0.2, 0], [xs[1] - bw / 2 - 0.05, 0.2, 0])
        self.play(FadeIn(g2, shift=RIGHT * 0.5), GrowArrow(lk1), FadeIn(cap2), run_time=0.6)
        until(self, "material override")
        tab = VGroup(pill(0, 0, 3.5, 0.62), T("material override", 32)).move_to([(xs[0] + xs[1]) / 2, 2.2, 0])
        stem = Line([(xs[0] + xs[1]) / 2, 1.88, 0], [(xs[0] + xs[1]) / 2, 0.25, 0], color=DIM, stroke_width=5)
        self.play(Create(stem), FadeIn(tab, shift=DOWN * 0.3), run_time=0.5)
        until(self, "The material holds")
        lk2 = arrow([xs[1] + bw / 2 + 0.05, 0.2, 0], [xs[2] - bw / 2 - 0.05, 0.2, 0])
        self.play(FadeIn(g3, shift=RIGHT * 0.5), GrowArrow(lk2), run_time=0.5)
        dot = Dot([xs[2], -1.65, 0], radius=0.15, color=TERRA).set_stroke(DIM, width=3)
        path = Line([xs[2], -1.65, 0], [xs[0], -1.65, 0], color=DIM, stroke_width=4)
        self.add(path)
        self.play(FadeIn(dot), run_time=0.15)
        self.play(MoveAlongPath(dot, path), run_time=0.9)
        self.play(Create(ring(b1)), run_time=0.35)
        done(self)
