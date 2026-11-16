"""ACT I · The Shape of a File  (B03, B04, B07, B08, B09: the Manim beats of this act)

Cast for the act: the shader file as monospace lines placed on an explicit character grid (A1_CW per character, so Pango can never fuse or drop a
space), the real Lab renders shown as themselves (lab_window of pantry/*.png), and drawn marks (ring, check, cross, bracket, arrow) for the claims.
Every code line is a line of a real file in lab-shaders/ (04-globals, 02-spacing-*, 03-comment-*, 41-err-case); nothing is mocked.
"""

A1P = "pantry/"


def a1_cw(size=32):
    """Advance of one Menlo character at this size, measured once with Manim 0.20.1 (font scaling is not linear in size: 32 -> 0.25, 40 -> 0.35).
    Constants, not a runtime measurement: Gate A's stub Text has no real widths."""
    return {32: 0.25, 36: 0.30, 40: 0.35}.get(size, 0.25 * size / 32)


def a1_mono(s, xl, y, size=32, color=INK, t2c=None):
    """One code line, LEFT edge on the character grid: leading spaces become columns, so indentation and spaces are exact."""
    ind = len(s) - len(s.lstrip(" "))
    t = Text(s.lstrip(" "), font=MONO, color=color, font_size=size, t2c=t2c or {})
    t.move_to([xl + ind * a1_cw(size) + t.width / 2, y, 0])
    return t


def a1_x(xl, col, size=32):
    """Scene x of the left edge of column `col` (0-based) of a line whose left edge is xl."""
    return xl + col * a1_cw(size)


def a1_t(s, x, y, size=32, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a1_check(x, y, s=0.26, color=TEAL, sw=9):
    return VMobject(stroke_color=color, stroke_width=sw).set_points_as_corners(
        [np.array([x - s, y, 0]), np.array([x - s * 0.3, y - s * 0.75, 0]), np.array([x + s, y + s * 0.8, 0])])


def a1_cross(x, y, s=0.26, color=INK, sw=8):
    return VGroup(Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=sw),
                  Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=sw))


def a1_equals(x, y, w=0.7, gap=0.2):
    return VGroup(Line([x - w / 2, y + gap / 2, 0], [x + w / 2, y + gap / 2, 0], color=INK, stroke_width=7),
                  Line([x - w / 2, y - gap / 2, 0], [x + w / 2, y - gap / 2, 0], color=INK, stroke_width=7))


def a1_glyphs(lines):
    """All the glyph pieces (non-space characters, in reading order) of a list of code-line Texts."""
    return VGroup(*[g for ln in lines for g in ln.submobjects])


# ═════════════════════════════ B03 · the header ═════════════════════════════
def a1_ubar(mob, pad=0.08):
    """terracotta underline bar over a grey backing (a bar, never text): the emphasis mark that does not read as accent text"""
    w = mob.width + 2 * pad
    return VGroup(Rectangle(width=w, height=0.2, stroke_width=0).set_fill(DIM, opacity=0.55).move_to(mob.get_bottom() + DOWN * 0.18),
                  Rectangle(width=w, height=0.12, stroke_width=0).set_fill(TERRA, opacity=1).move_to(mob.get_bottom() + DOWN * 0.18))


class B03_Header(Scene):
    def construct(self):
        xl = -3.75
        line1 = a1_mono("shader_type canvas_item;", xl, 2.85, 40)
        # tiles: row 1 (the two big types), row 2 (three more)
        def tile(txt, x, y, w):
            b = box(x, y, w, 0.72, INK, 4)
            return VGroup(b, M(txt, 32).move_to([x, y, 0]))
        t_canvas = tile("canvas_item", -2.55, 1.5, 3.3)
        t_spatial = tile("spatial", 2.3, 1.5, 2.5)
        cap_c = a1_t("2D + interface", -2.55, 0.75)
        cap_s = a1_t("3D", 2.3, 0.85)
        t_part = tile("particles", -2.5, -0.35, 2.7)
        t_sky = tile("sky", 0.05, -0.35, 1.5)
        t_fog = tile("fog", 2.0, -0.35, 1.5)
        bx0, bx1, by = -3.85, 2.75, -0.95
        bracket = VGroup(Line([bx0, by, 0], [bx1, by, 0], color=DIM, stroke_width=5), Line([bx0, by, 0], [bx0, by + 0.15, 0], color=DIM, stroke_width=5),
                         Line([bx1, by, 0], [bx1, by + 0.15, 0], color=DIM, stroke_width=5))
        cap_more = a1_t("more", (bx0 + bx1) / 2, by - 0.4)
        lx0, lx1, ly = a1_x(xl, 12, 40) - 0.05, a1_x(xl, 23, 40) - 0.15, 2.38
        ring_line = VGroup(Line([lx0, ly, 0], [lx1, ly, 0], color=DIM, stroke_width=6), Line([lx0, ly, 0], [lx0, ly + 0.14, 0], color=DIM, stroke_width=6),
                           Line([lx1, ly, 0], [lx1, ly + 0.14, 0], color=DIM, stroke_width=6),
                           Dot([(lx0 + lx1) / 2, ly - 0.2, 0], radius=0.11, color=TERRA).set_stroke(DIM, width=3))
        ring_tile = a1_ubar(t_canvas[0], pad=0.1)
        # the optional second line
        rx = -6.0
        line2 = a1_mono("render_mode blend_add;", rx, -2.3, 32, DIM)
        opt = VGroup(box(1.1, -2.3, 2.1, 0.62, DIM, 3), a1_t("optional", 1.1, -2.3))
        sq_a = Square(side_length=1.0, stroke_color=INK, stroke_width=5).move_to([4.0, -2.3, 0])
        sq_b = Square(side_length=1.0, stroke_color=INK, stroke_width=5).move_to([4.55, -2.3 - 0.0, 0]).shift(UP * 0.05)
        overlap = Rectangle(width=0.45, height=0.95, stroke_width=0).set_fill("#CFE3DC", opacity=1).move_to([4.275, -2.275, 0])
        cap_blend = a1_t("blend", 4.28, -3.05)

        until(self, "The header starts", lead=0.0)
        self.play(AddTextLetterByLetter(line1, time_per_char=0.05), run_time=1.3)
        until(self, "Canvas item means", lead=0.9)
        self.play(LaggedStart(Create(t_canvas), Create(t_spatial), Create(t_part), Create(t_sky), Create(t_fog), lag_ratio=0.3), run_time=1.4)
        until(self, "Canvas item means", lead=0.0)
        self.play(FadeIn(ring_line), FadeIn(ring_tile), FadeIn(cap_c), run_time=0.5)
        until(self, "Spatial means", lead=0.1)
        self.play(FadeIn(cap_s), FadeIn(bracket), FadeIn(cap_more), run_time=0.4)
        until(self, "An optional second line", lead=0.0)
        self.play(FadeIn(line2, shift=RIGHT * 0.6), FadeIn(opt, shift=RIGHT * 0.3), run_time=0.6)
        until(self, "such as how a pixel blends", lead=0.1)
        self.play(Create(sq_a), Create(sq_b), run_time=0.5)
        self.play(FadeIn(overlap), FadeIn(cap_blend), run_time=0.4)
        done(self)


# ═════════════════════════════ B04 · globals ═════════════════════════════
class B04_Globals(Scene):
    def construct(self):
        xl = -5.3
        band = box(0.0, 0.8, 12.2, 5.0, DIM, 4)
        lab = a1_t("globals", -4.9, 2.95, 32)
        rows = [
            ("uniform float level = 0.8;", ["a value your game sets from outside;", "every pixel sees the same one"], 2.3),
            ("const vec3 TEAL = vec3(0.37, 0.64, 0.57);", ["a named value that never changes"], 0.8),
            ("varying vec2 corner_uv;", ["a value set at each corner, blended across", "the shape for fragment() to read"], -0.3),
        ]
        groups = []
        for decl, caps, y in rows:
            dot = Dot([-5.75, y, 0], radius=0.12, color=TERRA).set_stroke(DIM, width=3)
            d = a1_mono(decl, xl, y)
            cs = VGroup(*[a1_t(c, xl + 0.0, y - 0.5 - 0.42 * i).align_to([xl, 0, 0], LEFT) for i, c in enumerate(caps)])
            groups.append(VGroup(dot, d, cs))
        fbar = box(0.0, -2.9, 12.2, 0.62, INK, 4)
        flab = a1_t("functions", -4.9, -2.9, 32)
        down = arrow([-2.3, -1.75, 0], [-2.3, -2.55, 0], INK, 7)
        rd = a1_t("readable below", 0.1, -2.15)

        self.play(Create(band), FadeIn(lab), Create(fbar), FadeIn(flab), run_time=0.7)
        until(self, "A uniform is", lead=0.1)
        self.play(FadeIn(groups[0], shift=RIGHT * 0.3), run_time=0.5)
        until(self, "A const never", lead=0.1)
        self.play(FadeIn(groups[1], shift=RIGHT * 0.3), run_time=0.5)
        until(self, "A varying hands", lead=0.1)
        self.play(FadeIn(groups[2], shift=RIGHT * 0.3), run_time=0.5)
        until(self, "Declare each one", lead=0.1)
        self.play(GrowArrow(down), FadeIn(rd), run_time=0.6)
        done(self)


# ═════════════════════════════ B07 · three spellings ═════════════════════════════
class B07_ThreeSpellings(Scene):
    def construct(self):
        xl = -6.0
        lh = 0.55
        top, bot = 3.3, -0.45
        cy = (top + bot) / 2
        card = box(0.0, cy, 12.5, top - bot, DIM, 4, fill=PALEBOX, radius=0.14)
        neat = ["shader_type canvas_item;", "", "void fragment() {", "  COLOR = vec4(0.4 + 0.6 * UV, 0.7, 1.0);", "}"]
        squeezed = ["shader_type canvas_item;", "void fragment(){COLOR=vec4(0.4+0.6*UV,0.7,1.0);}"]
        spread = ["shader_type canvas_item;", "", "void fragment() {", "  COLOR = vec4(", "    0.4 + 0.6 * UV,", "    0.7, 1.0);", "}"]

        def build(lines):
            hs = [(lh * 0.5 if not s else lh) for s in lines]
            tot = sum(hs)
            y = cy + tot / 2
            out = []
            for s, h in zip(lines, hs):
                if s:
                    out.append(a1_mono(s, xl, y - h / 2))
                y -= h
            return out
        A, B, C = build(neat), build(squeezed), build(spread)
        gA, gB, gC = a1_glyphs(A), a1_glyphs(B), a1_glyphs(C)
        assert len(gA) == len(gB) == len(gC), (len(gA), len(gB), len(gC))
        names = VGroup()
        pic = lab_window(A1P + "spacing.png", 2.5, -2.6, -1.75, "")
        cap = a1_t("Godot 4.7.2 · Forward+", -2.6, -2.9)
        eq = a1_equals(0.55, -1.75)
        same = a1_t("same picture", 2.6, -1.75)
        tag = a1_t("neat", 5.4, 2.95, 32, DIM)

        self.play(Create(card), run_time=0.4)
        self.add(gA)
        self.play(FadeIn(gA), FadeIn(pic), FadeIn(cap), run_time=0.7)
        until(self, "squeezed onto one line", lead=0.55)
        self.play(Transform(gA, gB), run_time=1.0)
        until(self, "spread over many", lead=0.55)
        self.play(Transform(gA, gC), run_time=1.0)
        until(self, "Godot draws the same", lead=0.2)
        self.play(FadeIn(eq), FadeIn(same), run_time=0.5)
        done(self)


# ═════════════════════════════ B08 · comment out ═════════════════════════════
class B08_CommentOut(Scene):
    def construct(self):
        xl = -6.05
        lh = 0.45
        top = 2.6
        src_on = ["shader_type canvas_item;", "", "/* A note for people,", "   over two lines. */", "void fragment() {",
                  "  vec3 c = vec3(UV, 0.5);", "  c = 0.4 + 0.6 * c; // soften", "  COLOR = vec4(c, 1.0);", "}"]
        card = box(-1.7, top - 0.15 - len(src_on) * lh / 2, 9.0, len(src_on) * lh + 0.3, DIM, 4, fill=PALEBOX, radius=0.14)
        lines = []
        for i, s in enumerate(src_on):
            y = top - 0.15 - lh * (i + 0.5)
            if not s:
                continue
            if i in (2, 3):
                lines.append(a1_mono(s, xl, y, color=DIM))
            elif i == 6:
                lines.append(a1_mono(s, xl, y, t2c={"// soften": DIM}))
            else:
                lines.append(a1_mono(s, xl, y))
        y6 = top - 0.15 - lh * 6.5
        off6 = a1_mono("  // c = 0.4 + 0.6 * c; // soften", xl, y6, color=DIM)
        idx6 = [k for k, s in enumerate([s for s in src_on if s]) if s.startswith("  c = 0.4")][0]
        on6 = lines[idx6]
        xr = 4.7
        on_pic = lab_window(A1P + "comment-on.png", 2.9, xr, 1.45, "Godot 4.7.2")
        off_im = ImageMobject(A1P + "comment-off.png").set_width(2.9).move_to([xr, 1.45, 0])
        # captions with drawn brackets
        bkx = a1_x(xl, 23.5)
        by_top, by_bot = top - 0.15 - lh * 2.5 + 0.18, top - 0.15 - lh * 3.5 - 0.18
        blk = VGroup(Line([bkx, by_top, 0], [bkx, by_bot, 0], color=DIM, stroke_width=5),
                     Line([bkx, by_top, 0], [bkx - 0.14, by_top, 0], color=DIM, stroke_width=5),
                     Line([bkx, by_bot, 0], [bkx - 0.14, by_bot, 0], color=DIM, stroke_width=5))
        blk_cap = a1_t("block comment", bkx + 1.4, (by_top + by_bot) / 2)
        lin_cap = a1_t("line comment", 4.7, y6)
        lin = arrow([3.45, y6, 0], [a1_x(xl, 30) + 0.12, y6, 0], DIM, 5, 0.2)

        self.play(Create(card), run_time=0.4)
        self.play(FadeIn(VGroup(*lines)), FadeIn(on_pic), run_time=0.6)
        until(self, "Two slashes comment out", lead=0.15)
        self.play(GrowArrow(lin), FadeIn(lin_cap), run_time=0.5)
        until(self, "Slash star starts", lead=0.15)
        self.play(Create(blk), FadeIn(blk_cap), run_time=0.5)
        until(self, "Godot skips both", lead=0.3)
        self.play(Transform(on6, off6), FadeOut(lin), FadeOut(lin_cap), FadeIn(off_im), run_time=1.0)
        done(self)


# ═════════════════════════════ B09 · names must match ═════════════════════════════
class B09_NamesMustMatch(Scene):
    def construct(self):
        cap1 = a1_t("GLSL: the OpenGL Shading Language.", 0, 3.0)
        cap2 = a1_t("Godot's is close to GLSL ES 3.0.", 0, 2.5)
        pl = box(-3.2, -0.55, 5.8, 4.2, DIM, 4)
        pr = box(3.2, -0.55, 5.8, 4.2, DIM, 4)

        def tagbox(txt, x, y, w):
            return VGroup(box(x, y, w, 0.78, INK, 4), M(txt, 32).move_to([x, y, 0]))
        lv = tagbox("level", -4.0, 0.7, 2.2)
        LV = tagbox("Level", -4.0, -0.6, 2.2)
        ok = a1_check(-2.2, 0.7)
        bad = a1_cross(-2.2, -0.6)
        cl = LV[1][0]
        ul = Line([cl.get_left()[0], -1.12, 0], [cl.get_right()[0], -1.12, 0], color=DIM, stroke_width=6)
        ringL = VGroup(ul, Dot([cl.get_center()[0], -1.32, 0], radius=0.12, color=TERRA).set_stroke(DIM, width=3))
        capL = a1_t("capitals count", -3.0, -1.9)
        gl = tagbox("gl_FragColor", 2.2, 0.7, 3.5)
        badg = a1_cross(4.4, 0.7)
        co = tagbox("COLOR", 2.2, -0.9, 2.2)
        okc = a1_check(4.0, -0.9)
        arr = arrow([2.2, 0.25, 0], [2.2, -0.45, 0], INK, 6)
        capc = a1_t("Godot's name for the output", 3.2, -1.8)

        self.play(FadeIn(cap1), FadeIn(cap2), Create(pl), Create(pr), run_time=0.6)
        self.play(FadeIn(lv), FadeIn(LV), run_time=0.4)
        until(self, "Names must match", lead=0.1)
        self.play(Create(ok), run_time=0.3)
        until(self, "a capital L makes", lead=0.1)
        self.play(Create(bad), FadeIn(ringL), FadeIn(capL), run_time=0.5)
        until(self, "The other language's", lead=0.2)
        self.play(FadeIn(gl), run_time=0.3)
        self.play(Create(badg), run_time=0.3)
        until(self, "Godot calls it", lead=0.2)
        self.play(GrowArrow(arr), FadeIn(co), run_time=0.5)
        self.play(Create(okc), FadeIn(capc), run_time=0.4)
        done(self)
