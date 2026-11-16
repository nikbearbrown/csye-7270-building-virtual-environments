"""scenes.py — What Is PBR? (CSYE 7270). Manim body beats B01, B08, B10.

Claude stage: cream #F2F0E9, ink #3D3929, terracotta #D97757 as the one accent, dim #8B8F96.
Each scene is paced to its beat's measured narration (word times in word_times.json).
"""
from manim import *
import numpy as np

STAGE, INK, ACC, DIM, GHOST, CARD = "#F2F0E9", "#3D3929", "#D97757", "#8B8F96", "#D9D4C7", "#FFFEFB"
SOFT = "#6E6A57"   # muted TEXT (dim is for shapes only: it fails text contrast on cream)
SHADE = "#A9573D"
config.background_color = STAGE
FONT = "EB Garamond"


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


def ball(r=1.6):
    """A drawn sphere: terracotta disc, a crescent of shade, one small highlight."""
    dark = Circle(radius=r, fill_color=SHADE, fill_opacity=1, stroke_width=0)
    lit = Circle(radius=0.8 * r, fill_color=ACC, fill_opacity=1, stroke_width=0).shift(UL * 0.14 * r)
    rim = Circle(radius=r, stroke_color=INK, stroke_width=4)
    hi = Ellipse(width=0.38 * r, height=0.26 * r, fill_color=CARD, fill_opacity=0.95, stroke_width=0).shift(UL * 0.42 * r)
    return VGroup(dark, lit, rim, hi)


def bar(value, w=1.5):
    track = Line(LEFT * w / 2, RIGHT * w / 2, color=INK, stroke_width=5)
    knob = Dot(track.point_from_proportion(value), radius=0.11, color=INK)
    return VGroup(track, knob)


SLOTS = ["base colour", "metallic", "roughness", "normal", "ambient occlusion"]


def slot_icon(i):
    if i == 0:
        return Square(0.5, fill_color=ACC, fill_opacity=1, stroke_color=INK, stroke_width=3)
    if i == 1:
        return bar(0.0)
    if i == 2:
        return bar(0.5)
    if i == 3:
        return Arrow(DOWN * 0.3, UP * 0.35, buff=0, color=INK, stroke_width=6, max_tip_length_to_length_ratio=0.35)
    g = VGroup(*[Square(0.25, fill_color=c, fill_opacity=1, stroke_width=0) for c in ["#5E5A50", "#B9B3A6", "#B9B3A6", "#FFFFFF"]])
    g.arrange_in_grid(2, 2, buff=0)
    return VGroup(g, SurroundingRectangle(g, buff=0, color=INK, stroke_width=3))


class B01_FiveMeasurements(Scene):
    DUR = 13.14

    def construct(self):
        big = T("PBR", 132)
        self.go(FadeIn(big), rt=0.5)
        full = T("Physically Based Rendering", 56).to_edge(UP, buff=0.7)
        self.at(1.2)
        self.go(ReplacementTransform(big, full), rt=0.9)

        sph = ball().move_to(LEFT * 3.9 + UP * 0.15)
        self.at(2.7)
        self.go(GrowFromCenter(sph), rt=0.7)
        painted = T("paint how it looks", 40, SOFT).next_to(sph, DOWN, buff=0.45)
        self.go(FadeIn(painted), rt=0.4)
        no = VGroup(Line(UL * 0.16, DR * 0.16, color=INK, stroke_width=6), Line(UR * 0.16, DL * 0.16, color=INK, stroke_width=6))
        no.next_to(painted, LEFT, buff=0.25)
        measured = T("measure what it is", 40).next_to(painted, DOWN, buff=0.25)
        self.at(4.3)
        self.go(Create(no), FadeIn(measured), rt=0.6)

        card = RoundedRectangle(width=6.6, height=5.7, corner_radius=0.18, fill_color=CARD, fill_opacity=1,
                                stroke_color=INK, stroke_width=3).move_to(RIGHT * 3.1 + DOWN * 0.55)
        head = T("StandardMaterial3D", 40).move_to(card.get_top() + DOWN * 0.5)
        rule = Line(card.get_left() + RIGHT * 0.3, card.get_right() + LEFT * 0.3, color=GHOST, stroke_width=3).next_to(head, DOWN, buff=0.2)
        rows = VGroup()
        for i, name in enumerate(SLOTS):
            y = 0.65 - i * 0.9          # card spans y -3.4..2.3, x -0.2..6.4
            lab = T(name, 38, SOFT).move_to([0.25, y, 0], aligned_edge=LEFT)
            hole = DashedVMobject(Square(0.55, color=DIM, stroke_width=3), num_dashes=12).move_to([5.2, y, 0])
            rows.add(VGroup(lab, hole))
        self.at(6.0)
        self.go(FadeIn(card), FadeIn(head), Create(rule), *[FadeIn(r) for r in rows], rt=0.9)

        ring = None
        for i, t in enumerate([9.12, 9.84, 10.5, 11.2, 11.66]):
            self.at(t)
            lab, hole = rows[i]
            icon = slot_icon(i).move_to(hole)
            box = SurroundingRectangle(rows[i], color=ACC, stroke_width=5, buff=0.12)
            anims = [lab.animate.set_color(INK), ReplacementTransform(hole, icon)]
            anims.append(Create(box) if ring is None else ReplacementTransform(ring, box))
            self.go(*anims, rt=0.4)
            ring = box
        self.at(12.3)
        self.go(FadeOut(ring), rt=0.5)
        self.end()


class B08_LightPaints(Scene):
    DUR = 9.54

    def construct(self):
        chips = VGroup()
        for name in SLOTS:
            lab = T(name, 40)
            box = RoundedRectangle(width=4.2, height=0.86, corner_radius=0.12, fill_color=CARD, fill_opacity=1, stroke_width=0)  # no ink border: a border plus the arrows reads as one text blob to GATE T
            chips.add(VGroup(box, lab.move_to(box)))
        chips.arrange(DOWN, buff=0.3).move_to(LEFT * 4.15)
        pix = Square(2.5, color=DIM, stroke_width=5).move_to(RIGHT * 4.75)
        pix_dash = pix  # a plain outline: dashes read as stray type to the type-size check
        pix_lab = T("one pixel", 42).next_to(pix, DOWN, buff=0.35)
        self.go(FadeIn(chips), Create(pix_dash), FadeIn(pix_lab), rt=0.8)
        q = T("?", 96, SOFT).move_to(pix)
        self.at(1.0)
        self.go(FadeIn(q), rt=0.4)

        rend = Circle(radius=1.15, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(RIGHT * 0.6)
        rend_lab = T("renderer", 38).move_to(rend)
        self.at(2.6)
        self.go(GrowFromCenter(rend), FadeIn(rend_lab), rt=0.6)
        ins = VGroup(*[Arrow(c.get_right(), rend.get_left(), buff=0.3, color=INK, stroke_width=4, max_tip_length_to_length_ratio=0.08) for c in chips])
        self.at(4.4)
        self.go(LaggedStart(*[GrowArrow(a) for a in ins], lag_ratio=0.15), rt=1.0)

        sun_core = Circle(radius=0.38, fill_color=INK, fill_opacity=1, stroke_width=0)
        rays = VGroup(*[Line(ORIGIN, RIGHT * 0.26, color=INK, stroke_width=5).shift(RIGHT * 0.52).rotate(a, about_point=ORIGIN) for a in np.linspace(0, TAU, 9)[:-1]])
        sun = VGroup(sun_core, rays).scale(1.15).move_to(RIGHT * 0.6 + UP * 2.75)
        sun_lab = T("light", 40).next_to(sun, RIGHT, buff=0.3)
        sun_arrow = Arrow(sun.get_bottom(), rend.get_top(), buff=0.12, color=INK, stroke_width=4)
        self.at(5.7)
        self.go(FadeIn(sun), FadeIn(sun_lab), GrowArrow(sun_arrow), rt=0.5)

        body = RoundedRectangle(width=1.1, height=0.75, corner_radius=0.1, fill_color=INK, fill_opacity=1, stroke_width=0)
        lens = Triangle(fill_color=INK, fill_opacity=1, stroke_width=0).scale(0.32).rotate(-PI / 2).next_to(body, RIGHT, buff=0)
        cam = VGroup(body, lens).scale(1.15).move_to(RIGHT * 0.6 + DOWN * 2.75)
        cam_lab = T("camera", 40).next_to(cam, RIGHT, buff=0.3)
        cam_arrow = Arrow(cam.get_top(), rend.get_bottom(), buff=0.12, color=INK, stroke_width=4)
        self.at(6.25)
        self.go(FadeIn(cam), FadeIn(cam_lab), GrowArrow(cam_arrow), rt=0.5)

        out = Arrow(rend.get_right(), pix.get_left(), buff=0.12, color=ACC, stroke_width=6)
        filled = Square(2.5, fill_color="#C66F50", fill_opacity=1, stroke_color=ACC, stroke_width=6).move_to(pix)
        self.at(7.1)
        self.go(GrowArrow(out), rt=0.5)
        self.go(FadeOut(q), ReplacementTransform(pix_dash, filled), rt=0.7)
        self.end()


DATA = {
    "metallic": ["0", "0", "1", "0"],
    "roughness": [".28", ".90", ".29", ".36"],
    "normal": ["128", "128", "255"],
    "occlusion": ["1.0", ".29", ".34", "1.0"],
}


class B10_ColourOrData(Scene):
    DUR = 10.07

    def construct(self):
        names = ["base colour", "metallic", "roughness", "normal", "occlusion"]
        tiles = VGroup()
        for i, n in enumerate(names):
            frame = Square(2.3, stroke_color=INK, stroke_width=3)
            if i == 0:
                cells = VGroup(*[Square(0.766, fill_color=(ACC if (k + k // 3) % 2 else "#EDE3CC"), fill_opacity=1, stroke_width=0) for k in range(9)]).arrange_in_grid(3, 3, buff=0)
            elif i == 1:
                cells = VGroup(*[Square(0.766, fill_color=("#FFFFFF" if k == 4 else "#111111"), fill_opacity=1, stroke_width=0) for k in range(9)]).arrange_in_grid(3, 3, buff=0)
            elif i == 2:
                cells = VGroup(*[Square(0.766, fill_color=["#4D4D4D", "#E6E6E6", "#555555"][k % 3], fill_opacity=1, stroke_width=0) for k in range(9)]).arrange_in_grid(3, 3, buff=0)
            elif i == 3:
                cells = VGroup(*[Square(0.766, fill_color=["#8080FF", "#7A9AF0", "#8080FF"][k % 3], fill_opacity=1, stroke_width=0) for k in range(9)]).arrange_in_grid(3, 3, buff=0)
            else:
                cells = VGroup(*[Square(0.766, fill_color=("#FFFFFF" if k == 4 else "#8A857A"), fill_opacity=1, stroke_width=0) for k in range(9)]).arrange_in_grid(3, 3, buff=0)
            lab = T(n, 40).next_to(frame, DOWN, buff=0.3)
            tiles.add(VGroup(cells.move_to(frame), frame, lab))
        tiles.arrange(RIGHT, buff=0.26).move_to(UP * 0.1)
        self.go(LaggedStart(*[FadeIn(t) for t in tiles], lag_ratio=0.12), rt=0.9)

        ring = SurroundingRectangle(tiles[0][1], color=ACC, stroke_width=7, buff=0.12)
        tag = T("a colour", 38).next_to(tiles[0], UP, buff=0.35)
        self.at(1.5)
        self.go(Create(ring), FadeIn(tag), rt=0.6)

        for i, (key, t) in enumerate(zip(["metallic", "roughness", "normal", "occlusion"], [3.48, 3.76, 4.38, 4.9])):
            tile = tiles[i + 1]
            vals = DATA[key]
            nums = VGroup(*[T(v, 46) for v in vals]).arrange(DOWN, buff=0.12).move_to(tile[1])
            if len(vals) == 4:
                nums = VGroup(*[T(v, 46) for v in vals]).arrange_in_grid(2, 2, buff=(0.35, 0.3)).move_to(tile[1])
            self.at(t)
            self.go(ReplacementTransform(tile[0], nums), rt=0.45)
        data_rule = Line(tiles[1].get_corner(UL) + UP * 0.25, tiles[4].get_corner(UR) + UP * 0.25, color=INK, stroke_width=4)
        data_tag = T("numbers stored in image files", 38).next_to(data_rule, UP, buff=0.2)
        self.at(6.6)
        self.go(Create(data_rule), FadeIn(data_tag), rt=0.6)
        self.end()
