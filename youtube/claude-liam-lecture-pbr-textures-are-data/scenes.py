"""scenes.py — PBR Textures Are Data, Not Pictures (CSYE 7270). Manim body beats B02, B03, B05, B06, B08, B09.

Claude stage: cream #F2F0E9, ink #3D3929, terracotta #D97757 as the one accent.
Images are the REAL code-made texture files in _pbr-evidence/textures (tools/make_textures.py).
Texel values in C2 are read from tiles_roughness.png, rows 126-130, columns 268-272.
Decode numbers: sRGB EOTF of 128/255 = 0.2158; unpacked normal (-0.568, -0.568, 1.0) is 38.8 degrees off +Z.
"""
from manim import *
import numpy as np
from PIL import Image

STAGE, INK, ACC, DIM, GHOST, CARD = "#F2F0E9", "#3D3929", "#D97757", "#8B8F96", "#D9D4C7", "#FFFEFB"
SOFT = "#6E6A57"
config.background_color = STAGE
FONT = "EB Garamond"
TEX = "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_pbr-evidence/textures"


def T(s, size=40, color=INK, **kw):
    return Text(s, font=FONT, font_size=size, color=color, **kw)


# Pacing helpers, attached to Scene so every beat class can subclass Scene directly (run.sh finds
# scenes by the pattern `class B##_Name(Scene)`). DUR on each class = the beat's measured narration.
def _go(self, *anims, rt=0.6):
    self.play(*anims, run_time=rt)
    self._t = getattr(self, "_t", 0.0) + rt


def _at(self, t):
    now = getattr(self, "_t", 0.0)
    if t - now > 0.02:
        self.wait(t - now)
        self._t = t


def _end(self):
    _at(self, self.DUR)


Scene.go, Scene.at, Scene.end = _go, _at, _end


def crisp(m):
    """Nearest-neighbour sampling so texels stay square (skipped where the QC stub has no resampling table)."""
    table = globals().get("RESAMPLING_ALGORITHMS")
    if table and hasattr(m, "set_resampling_algorithm"):
        m.set_resampling_algorithm(table["nearest"])
    return m


def img(name, h):
    return crisp(ImageMobject(f"{TEX}/{name}")).scale_to_fit_height(h)


def framed(m):
    return SurroundingRectangle(m, buff=0, color=INK, stroke_width=3)


MAPS = [("tiles_albedo.png", "base colour"), ("tiles_normal.png", "normal"), ("tiles_roughness.png", "roughness"),
        ("tiles_metallic.png", "metallic"), ("tiles_ao.png", "occlusion")]


class B02_FiveMaps(Scene):
    DUR = 11.69

    def construct(self):
        ims = [img(f, 2.22) for f, _ in MAPS]
        xs = np.linspace(-4.95, 4.95, 5)
        groups = []
        for m, x, (_, n) in zip(ims, xs, MAPS):
            m.move_to([x, 0.5, 0])
            fr = framed(m)
            lab = T(n, 36).next_to(fr, DOWN, buff=0.3)
            groups.append((m, fr, lab))
        self.go(*[FadeIn(g[0]) for g in groups], *[Create(g[1]) for g in groups], *[FadeIn(g[2]) for g in groups], rt=0.9)

        ring = SurroundingRectangle(groups[0][1], color=ACC, stroke_width=7, buff=0.12)
        eyes = T("for your eyes", 34).next_to(ring, UP, buff=0.25)
        self.at(1.75)
        self.go(Create(ring), FadeIn(eyes), rt=0.6)

        tags = VGroup()
        for g in groups[1:]:
            tag = RoundedRectangle(width=1.3, height=0.62, corner_radius=0.1, fill_color=INK, fill_opacity=1, stroke_width=0)
            tag.next_to(g[1], UP, buff=0.3)
            tags.add(VGroup(tag, T("data", 34, STAGE).move_to(tag)))
        self.at(4.55)
        self.go(LaggedStart(*[FadeIn(t, shift=DOWN * 0.15) for t in tags], lag_ratio=0.2), rt=0.9)

        # a grid of numbers: rule the roughness image into cells
        m, fr, _ = groups[2]
        cells = VGroup()
        for k in range(1, 8):
            cells.add(Line(fr.get_left() + RIGHT * k * fr.width / 8, fr.get_left() + RIGHT * k * fr.width / 8 + UP * 0, color=INK, stroke_width=2)
                      .put_start_and_end_on(fr.get_corner(DL) + RIGHT * k * fr.width / 8, fr.get_corner(UL) + RIGHT * k * fr.width / 8))
            cells.add(Line(fr.get_corner(DL) + UP * k * fr.height / 8, fr.get_corner(DR) + UP * k * fr.height / 8, color=INK, stroke_width=2))
        grid_lab = T("a grid of numbers", 38).next_to(groups[2][2], DOWN, buff=0.35)
        self.at(9.9)
        self.go(LaggedStart(*[Create(c) for c in cells], lag_ratio=0.05), FadeIn(grid_lab), rt=0.8)
        self.end()


BLOCK = [[0.90, 0.90, 0.90, 0.28, 0.29],
         [0.90, 0.90, 0.90, 0.28, 0.29],
         [0.90, 0.90, 0.90, 0.36, 0.39],
         [0.90, 0.90, 0.90, 0.31, 0.28],
         [0.90, 0.90, 0.90, 0.33, 0.28]]


class B03_RoughNumbers(Scene):
    DUR = 11.03

    def construct(self):
        m = img("tiles_roughness.png", 5.0).move_to(LEFT * 3.55 + DOWN * 0.1)
        fr = framed(m)
        title = T("roughness map", 38).next_to(fr, UP, buff=0.25)
        self.go(FadeIn(m), Create(fr), FadeIn(title), rt=0.6)
        # the sampled block: columns 268-272, rows 126-130 of 1024
        px = fr.width / 1024
        corner = fr.get_corner(UL) + RIGHT * 268 * px + DOWN * 126 * px
        mark = Square(0.36, color=INK, stroke_width=6).move_to(corner + RIGHT * 2.5 * px + DOWN * 2.5 * px)
        self.at(0.6)
        self.go(Create(mark), rt=0.5)

        cells = VGroup()
        for r in range(5):
            for c in range(5):
                v = BLOCK[r][c]
                g = int(round(v * 255))
                sq = Square(0.95, fill_color=rgb_to_color((g / 255, g / 255, g / 255)), fill_opacity=1, stroke_color=INK, stroke_width=2)
                cells.add(sq)
        cells.arrange_in_grid(5, 5, buff=0).move_to(RIGHT * 2.6 + UP * 0.25)
        lines = VGroup(Line(mark.get_corner(UR), cells.get_corner(UL), color=INK, stroke_width=2),
                       Line(mark.get_corner(DR), cells.get_corner(DL), color=INK, stroke_width=2))
        self.at(1.35)
        self.go(Create(lines), TransformFromCopy(mark, cells), rt=0.9)

        def nums(cols, t):
            labs = VGroup()
            for r in range(5):
                for c in cols:
                    v = BLOCK[r][c]
                    labs.add(T(f"{v:.2f}", 36, INK if v > 0.5 else STAGE).move_to(cells[r * 5 + c]))
            self.at(t)
            self.go(LaggedStart(*[FadeIn(l) for l in labs], lag_ratio=0.05), rt=0.7)

        nums([3, 4], 2.62)
        tile_tag = T("tile", 36).next_to(VGroup(cells[3], cells[4]), UP, buff=0.25)
        self.go(FadeIn(tile_tag), rt=0.3)
        nums([0, 1, 2], 4.92)
        grout_tag = T("grout", 36).next_to(VGroup(cells[0], cells[2]), UP, buff=0.25)
        self.go(FadeIn(grout_tag), rt=0.3)

        bar = VGroup(*[Rectangle(width=0.22, height=0.42, fill_color=rgb_to_color((k / 15, k / 15, k / 15)), fill_opacity=1, stroke_width=0) for k in range(16)]).arrange(RIGHT, buff=0)
        bar.next_to(cells, DOWN, buff=0.4)
        left = T("0 smooth", 34).next_to(bar, LEFT, buff=0.25)
        right = T("rough 1", 34).next_to(bar, RIGHT, buff=0.25)
        self.at(6.55)
        self.go(GrowFromEdge(bar, LEFT), FadeIn(left), FadeIn(right), rt=0.8)
        self.end()


class B05_Normal(Scene):
    DUR = 11.2

    def construct(self):
        ground = Line(LEFT * 6 + DOWN * 2.2, RIGHT * 1.5 + DOWN * 2.2, color=INK, stroke_width=6)
        tilt = ValueTracker(0.0)
        P = np.array([-2.2, -2.2, 0])
        L = np.array([-0.55, 0.835, 0])  # direction TO the light, 33.4 degrees from straight up

        def patch():
            a = tilt.get_value()
            seg = Line(P + np.array([-1.3, 0, 0]), P + np.array([1.3, 0, 0]), color=INK, stroke_width=12)
            return seg.rotate(a, about_point=P)

        def normal():
            a = tilt.get_value()
            n = np.array([-np.sin(a), np.cos(a), 0])
            return Arrow(P, P + 2.6 * n, buff=0, color=INK, stroke_width=8, max_tip_length_to_length_ratio=0.12)

        def shade():
            a = tilt.get_value()
            n = np.array([-np.sin(a), np.cos(a), 0])
            d = max(0.0, float(np.dot(n, L)))
            g = 0.12 + 0.86 * d
            return Square(2.2, fill_color=rgb_to_color((g * 0.85, g * 0.47, g * 0.34)), fill_opacity=1, stroke_color=INK, stroke_width=3).move_to(RIGHT * 4.2 + UP * 0.2)

        pt = always_redraw(patch)
        self.go(Create(ground), FadeIn(pt), rt=0.6)
        nv = always_redraw(normal)
        n_lab = always_redraw(lambda: T("normal", 38).next_to(P + 2.6 * np.array([-np.sin(tilt.get_value()), np.cos(tilt.get_value()), 0]), UP + RIGHT, buff=0.3))
        self.at(2.5)
        first = normal()
        self.go(GrowArrow(first), FadeIn(n_lab), rt=0.6)
        self.remove(first)
        self.add(nv)

        sun = VGroup(Circle(radius=0.32, fill_color=INK, fill_opacity=1, stroke_width=0),
                     *[Line(ORIGIN, RIGHT * 0.22, color=INK, stroke_width=5).shift(RIGHT * 0.45).rotate(a, about_point=ORIGIN) for a in np.linspace(0, TAU, 9)[:-1]])
        sun.move_to(P + 4.4 * L)
        ray = Arrow(sun.get_center() - 0.6 * L, P + 0.2 * L, buff=0, color=INK, stroke_width=5)
        # the angle as a filled pale-terracotta wedge, not a thin terracotta arc (GATE T reads thin accent lines as text)
        arc = always_redraw(lambda: AnnularSector(inner_radius=0, outer_radius=1.1, start_angle=PI / 2 + tilt.get_value(),
                                                  angle=(np.arctan2(L[1], L[0])) - (PI / 2 + tilt.get_value()), arc_center=P,
                                                  fill_color=ACC, fill_opacity=0.35, stroke_width=0))
        theta = MathTex(r"\theta", color=INK, font_size=60).move_to(P + 1.55 * np.array([-0.32, 0.95, 0]))
        sw = always_redraw(shade)
        sw_lab = T("how bright the patch is", 34).next_to(RIGHT * 4.2 + DOWN * 0.9, DOWN, buff=0.2)
        self.at(4.6)
        self.go(FadeIn(sun), GrowArrow(ray), rt=0.6)
        self.go(Create(arc), FadeIn(theta), FadeIn(sw), FadeIn(sw_lab), rt=0.6)
        self.add(arc, sw)
        self.at(7.7)
        self.go(tilt.animate.set_value(-0.95), FadeOut(theta), rt=2.2)
        self.end()


class B06_NormalTexel(Scene):
    DUR = 12.86

    def construct(self):
        texel = Square(2.4, fill_color="#8080FF", fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(LEFT * 3.7 + UP * 1.1)
        t_lab = T("one texel", 38).next_to(texel, UP, buff=0.25)
        chans = VGroup()
        for name in ["R", "G", "B"]:
            box = Rectangle(width=1.3, height=0.8, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=3)
            chans.add(VGroup(box, T(name, 40).move_to(box)))
        chans.arrange(RIGHT, buff=0.2).next_to(texel, DOWN, buff=0.6)
        self.go(FadeIn(texel), FadeIn(t_lab), FadeIn(chans), rt=0.7)

        O = RIGHT * 3.0 + DOWN * 0.6
        ax_x = Arrow(O, O + RIGHT * 2.6, buff=0, color=INK, stroke_width=5)
        ax_y = Arrow(O, O + UP * 2.6, buff=0, color=INK, stroke_width=5)
        ax_z = Arrow(O, O + np.array([-1.6, -1.25, 0]), buff=0, color=INK, stroke_width=5)
        lx = T("X", 40).next_to(ax_x.get_end(), RIGHT, buff=0.15)
        ly = T("Y", 40).next_to(ax_y.get_end(), UP, buff=0.15)
        lz = T("Z, out of the surface", 36).next_to(ax_z.get_end(), DOWN, buff=0.15)
        self.at(1.0)
        self.go(GrowArrow(ax_x), GrowArrow(ax_y), GrowArrow(ax_z), FadeIn(lx), FadeIn(ly), FadeIn(lz), rt=0.8)

        ring = None
        for i, (t, target) in enumerate([(2.5, VGroup(ax_x, lx)), (3.3, VGroup(ax_y, ly)), (4.06, VGroup(ax_z, lz))]):
            link = VGroup(SurroundingRectangle(chans[i], color=ACC, stroke_width=6, buff=0.08),
                          SurroundingRectangle(target, color=ACC, stroke_width=6, buff=0.1))
            self.at(t)
            self.go(Create(link) if ring is None else ReplacementTransform(ring, link), rt=0.4)
            ring = link

        vals = VGroup(*[T(v, 40) for v in ["128", "128", "255"]])
        for v, c in zip(vals, chans):
            v.next_to(c, DOWN, buff=0.25)
        self.at(5.2)
        self.go(FadeOut(ring), rt=0.3)
        self.at(5.9)
        self.go(LaggedStart(*[FadeIn(v) for v in vals], lag_ratio=0.45), rt=1.8)
        maps = MathTex(r"\tfrac{2c}{255}-1:\ (128,128,255)\ \to\ (0,\,0,\,1)", color=INK, font_size=48).next_to(chans, DOWN, buff=1.15).shift(RIGHT * 1.4)
        out = Arrow(O, O + np.array([-1.6, -1.25, 0]), buff=0, color=ACC, stroke_width=12, max_tip_length_to_length_ratio=0.18)
        self.at(8.5)
        self.go(Write(maps), GrowArrow(out), rt=1.0)
        pale = SurroundingRectangle(texel, color=ACC, stroke_width=7, buff=0.12)
        self.at(10.5)
        self.go(Create(pale), rt=0.6)
        self.end()


def chan(name, k):
    a = np.asarray(Image.open(f"{TEX}/{name}").convert("L").resize((256, 256), Image.NEAREST))
    rgb = np.zeros((256, 256, 3), np.uint8)
    rgb[..., k] = a
    return rgb


class B08_Pack(Scene):
    DUR = 13.59

    def construct(self):
        srcs = [("tiles_ao.png", "ambient occlusion", 0), ("tiles_roughness.png", "roughness", 1), ("tiles_metallic.png", "metallic", 2)]
        greys, labs, tinted = [], [], []
        for i, (f, n, k) in enumerate(srcs):
            g = img(f, 1.9).move_to([-3.9, 2.3 - i * 2.35, 0])
            lab = T(n, 36).next_to(g, RIGHT, buff=0.3)
            tint = crisp(ImageMobject(chan(f, k))).scale_to_fit_height(1.9).move_to(g)
            greys.append(g); labs.append(lab); tinted.append(tint)
        frames = [framed(g) for g in greys]
        self.go(*[FadeIn(g) for g in greys], *[Create(f) for f in frames], *[FadeIn(l) for l in labs], rt=0.8)

        packed = img("tiles_arm.png", 4.0).move_to(RIGHT * 3.4 + UP * 0.6)
        pf = framed(packed)
        p_lab = T("one packed ARM file", 38).next_to(pf, DOWN, buff=0.3)
        self.at(1.85)
        self.go(Create(pf), FadeIn(p_lab), rt=0.6)

        letters = ["red", "green", "blue"]
        for i, t in enumerate([5.5, 7.2, 8.2]):
            tag = T(letters[i], 36).next_to(frames[i], LEFT, buff=0.25)
            self.at(t)
            self.go(FadeOut(greys[i]), FadeIn(tinted[i]), FadeIn(tag), rt=0.4)
            moving = tinted[i].copy()
            self.add(moving)
            self.go(moving.animate.move_to(packed).scale_to_fit_height(4.0).set_opacity(0.0), rt=0.5)
            self.remove(moving)
        self.go(FadeIn(packed), rt=0.4)

        orm = RoundedRectangle(width=5.8, height=0.9, corner_radius=0.12, fill_color=CARD, fill_opacity=1, stroke_color=ACC, stroke_width=5)
        orm_t = T("ORMMaterial3D: R, G, B", 36).move_to(orm)
        g_orm = VGroup(orm, orm_t).next_to(p_lab, DOWN, buff=0.3)
        self.at(9.8)
        self.go(FadeIn(g_orm, shift=DOWN * 0.15), rt=0.6)
        self.end()


def srgb_decode(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


class B09_Decode(Scene):
    DUR = 14.76

    def construct(self):
        ax = Axes(x_range=[0, 1, 0.5], y_range=[0, 1, 0.5], x_length=5.2, y_length=5.2, tips=False,
                  axis_config={"color": INK, "stroke_width": 3, "include_ticks": False}).move_to(LEFT * 2.2 + DOWN * 0.2)
        xl = T("stored value", 34).next_to(ax.x_axis, DOWN, buff=0.25)
        yl = T("value used", 34).next_to(ax.c2p(0, 1), RIGHT, buff=0.15)
        self.go(Create(ax), FadeIn(xl), FadeIn(yl), rt=0.7)
        straight = ax.plot(lambda x: x, color=DIM, stroke_width=4)
        s_lab = T("read as data", 32, SOFT).move_to(ax.c2p(0.3, 0.62))
        self.at(0.75)
        self.go(Create(straight), FadeIn(s_lab), rt=0.6)
        curve = ax.plot(srgb_decode, color=INK, stroke_width=6)
        c_lab = T("sRGB decode", 34).move_to(ax.c2p(0.86, 0.2))
        self.at(2.05)
        self.go(Create(curve), FadeIn(c_lab), rt=1.0)

        O = RIGHT * 4.3 + DOWN * 1.6
        base = Line(O + LEFT * 1.8, O + RIGHT * 1.8, color=INK, stroke_width=8)
        good = Arrow(O, O + UP * 3.2, buff=0, color=DIM, stroke_width=8)
        good_l = T("should be", 32, SOFT).next_to(good.get_end(), UP, buff=0.12)
        cap = T("side view, simplified", 32, SOFT).next_to(base, DOWN, buff=0.3)
        self.at(6.3)
        self.go(Create(base), GrowArrow(good), FadeIn(good_l), FadeIn(cap), rt=0.6)

        x0 = 128 / 255
        y0 = srgb_decode(x0)
        dot = Dot(ax.c2p(x0, 0), radius=0.12, color=ACC)
        x_val = MathTex(r"\tfrac{128}{255}\approx 0.502", color=INK, font_size=44).next_to(ax.c2p(x0, 0), DOWN, buff=0.2)
        self.at(7.65)
        self.go(FadeIn(dot), FadeOut(xl), Write(x_val), rt=0.8)
        up = DashedLine(ax.c2p(x0, 0), ax.c2p(x0, y0), color=INK, stroke_width=3)
        across = DashedLine(ax.c2p(x0, y0), ax.c2p(0, y0), color=INK, stroke_width=3)
        y_val = MathTex(r"0.216", color=INK, font_size=44).next_to(ax.c2p(0, y0), LEFT, buff=0.2)
        self.at(10.45)
        self.go(Create(up), dot.animate.move_to(ax.c2p(x0, y0)), rt=0.5)
        self.go(Create(across), dot.animate.move_to(ax.c2p(0, y0)), Write(y_val), rt=0.5)

        ang = np.deg2rad(38.8)
        bad = Arrow(O, O + 3.2 * np.array([-np.sin(ang), np.cos(ang), 0]), buff=0, color=ACC, stroke_width=10)
        arc = Arc(radius=1.4, start_angle=PI / 2, angle=ang, arc_center=O, color=INK, stroke_width=5)
        deg = MathTex(r"38.8^\circ", color=INK, font_size=48).move_to(O + 1.95 * np.array([-np.sin(ang / 2), np.cos(ang / 2), 0]) + LEFT * 1.25)
        self.at(12.3)
        self.go(GrowArrow(bad), Create(arc), Write(deg), rt=0.9)
        self.end()
