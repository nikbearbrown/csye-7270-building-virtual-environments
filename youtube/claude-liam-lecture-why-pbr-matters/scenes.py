"""scenes.py — Why PBR Matters (CSYE 7270). Manim body beats B05, B06.

Claude stage: cream #F2F0E9, ink #3D3929, terracotta #D97757 as the one accent.
B05 plots REAL measurements: luma along the row through the highlight of three Godot 4.7.2 renders
(_pbr-evidence/evidence/profiles.json, every 4th pixel of 601). B06 numbers are the saved gold material.
"""
from manim import *

STAGE, INK, ACC, DIM, GHOST, CARD = "#F2F0E9", "#3D3929", "#D97757", "#8B8F96", "#D9D4C7", "#FFFEFB"
SOFT = "#6E6A57"
config.background_color = STAGE
FONT = "EB Garamond"
LOGOS = "/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/icons/logos"

PROFILES = {0.2: [0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.008, 0.008, 0.008, 0.008, 0.008, 0.008, 0.008, 0.012, 0.012, 0.016, 0.016, 0.02, 0.024, 0.031, 0.039, 0.047, 0.059, 0.075, 0.094, 0.118, 0.149, 0.188, 0.239, 0.31, 0.4, 0.522, 0.667, 0.808, 0.878, 0.835, 0.71, 0.561, 0.427, 0.333, 0.255, 0.2, 0.157, 0.125, 0.102, 0.078, 0.063, 0.051, 0.039, 0.031, 0.024, 0.02, 0.016, 0.016, 0.012, 0.012, 0.012, 0.008, 0.008, 0.008, 0.008, 0.008, 0.008, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004], 0.4: [0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.008, 0.008, 0.008, 0.008, 0.008, 0.008, 0.008, 0.008, 0.008, 0.008, 0.008, 0.008, 0.012, 0.012, 0.012, 0.012, 0.012, 0.012, 0.016, 0.016, 0.016, 0.02, 0.02, 0.02, 0.024, 0.027, 0.027, 0.031, 0.035, 0.039, 0.043, 0.047, 0.051, 0.059, 0.063, 0.071, 0.075, 0.082, 0.09, 0.098, 0.106, 0.118, 0.125, 0.141, 0.149, 0.161, 0.173, 0.184, 0.196, 0.204, 0.216, 0.227, 0.231, 0.239, 0.243, 0.239, 0.239, 0.235, 0.231, 0.224, 0.216, 0.204, 0.192, 0.18, 0.169, 0.157, 0.145, 0.133, 0.125, 0.114, 0.106, 0.098, 0.09, 0.082, 0.075, 0.067, 0.063, 0.055, 0.051, 0.043, 0.039, 0.035, 0.035, 0.031, 0.027, 0.024, 0.024, 0.02, 0.02, 0.02, 0.016, 0.016, 0.016, 0.012, 0.012, 0.012, 0.012, 0.012, 0.012, 0.008, 0.008, 0.008, 0.008, 0.008, 0.008, 0.008, 0.008, 0.008, 0.008, 0.008, 0.008, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004], 0.7: [0.004, 0.012, 0.012, 0.012, 0.012, 0.012, 0.012, 0.012, 0.012, 0.012, 0.012, 0.012, 0.012, 0.012, 0.012, 0.016, 0.016, 0.016, 0.016, 0.016, 0.016, 0.016, 0.016, 0.016, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.024, 0.024, 0.024, 0.024, 0.024, 0.027, 0.027, 0.027, 0.027, 0.027, 0.031, 0.031, 0.031, 0.031, 0.035, 0.035, 0.035, 0.035, 0.039, 0.039, 0.039, 0.043, 0.043, 0.039, 0.047, 0.047, 0.047, 0.047, 0.051, 0.051, 0.051, 0.051, 0.055, 0.055, 0.055, 0.055, 0.055, 0.059, 0.059, 0.059, 0.059, 0.059, 0.059, 0.059, 0.067, 0.063, 0.063, 0.063, 0.063, 0.063, 0.063, 0.063, 0.063, 0.063, 0.059, 0.059, 0.059, 0.059, 0.059, 0.059, 0.059, 0.055, 0.055, 0.055, 0.055, 0.055, 0.051, 0.051, 0.051, 0.051, 0.047, 0.047, 0.047, 0.043, 0.039, 0.043, 0.043, 0.039, 0.039, 0.039, 0.035, 0.035, 0.035, 0.035, 0.031, 0.031, 0.031, 0.031, 0.027, 0.027, 0.027, 0.027, 0.024, 0.024, 0.024, 0.024, 0.024, 0.024, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.016, 0.016, 0.016, 0.016, 0.016, 0.016, 0.016, 0.016, 0.016, 0.012, 0.012, 0.012, 0.012, 0.012, 0.012]}


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


class B05_Profiles(Scene):
    DUR = 13.01

    def construct(self):
        rule = T("A surface never sends out more light than it receives.", 42).to_edge(UP, buff=0.7)
        cite = T("Energy conservation, as stated in LearnOpenGL, PBR Theory", 34, SOFT).next_to(rule, DOWN, buff=0.18)
        self.go(FadeIn(rule), rt=0.6)
        self.at(3.1)
        self.go(FadeIn(cite), rt=0.5)

        ax = Axes(x_range=[0, 600, 100], y_range=[0, 1, 0.25], x_length=10.5, y_length=3.6,
                  axis_config={"color": INK, "stroke_width": 3, "include_ticks": False}, tips=False).shift(DOWN * 0.1)
        ylab = T("brightness", 36).next_to(ax.c2p(0, 1), RIGHT, buff=0.2)
        xlab = T("pixels across the highlight", 34).next_to(ax.x_axis, DOWN, buff=0.18)
        src = T("measured on Godot 4.7.2 renders · sun only", 32, SOFT).next_to(xlab, DOWN, buff=0.1)
        self.at(5.85)
        self.go(Create(ax), FadeIn(ylab), FadeIn(xlab), FadeIn(src), rt=0.8)

        xs = [4 * i for i in range(151)]
        curves, labels = VGroup(), VGroup()
        widths = {0.2: 7, 0.4: 5, 0.7: 4}
        for r, t in [(0.2, 6.9), (0.4, 8.0), (0.7, 9.0)]:
            pts = [ax.c2p(x, y) for x, y in zip(xs, PROFILES[r])]
            c = VMobject(color=INK, stroke_width=widths[r]).set_points_smoothly(pts)
            peak_i = max(range(151), key=lambda i: PROFILES[r][i])
            spot = {0.2: (330, 0.86), 0.4: (420, 0.27), 0.7: (500, 0.11)}[r]
            lab = T(f"roughness {r}", 34).move_to(ax.c2p(*spot), aligned_edge=LEFT)
            self.at(t)
            self.go(Create(c), FadeIn(lab), rt=0.8)
            curves.add(c)
            labels.add(lab)

        # spreads wider: a bracket across the half-maximum width of the roughest highlight (280 px measured)
        y_half = 0.067 / 2
        span = Line(ax.c2p(160, y_half), ax.c2p(440, y_half), color=INK, stroke_width=4)
        ends = VGroup(Line(UP * 0.12, DOWN * 0.12, color=INK, stroke_width=4).move_to(span.get_start()),
                      Line(UP * 0.12, DOWN * 0.12, color=INK, stroke_width=4).move_to(span.get_end()))
        self.at(10.4)
        self.go(GrowFromCenter(span), FadeIn(ends), rt=0.6)

        # peak drops: one marker rides from peak to peak
        tops = []
        for r in (0.2, 0.4, 0.7):
            i = max(range(151), key=lambda k: PROFILES[r][k])
            tops.append(ax.c2p(xs[i], PROFILES[r][i]))
        dot = Dot(tops[0], radius=0.13, color=ACC)
        self.at(11.4)
        self.go(FadeIn(dot), rt=0.2)
        self.go(dot.animate.move_to(tops[1]), rt=0.45)
        self.go(dot.animate.move_to(tops[2]), rt=0.45)
        self.end()


def logo(name, h=1.6):
    return SVGMobject(f"{LOGOS}/{name}/{name}-01.svg").scale_to_fit_height(h)


class B06_Travel(Scene):
    DUR = 12.93

    def construct(self):
        blender = logo("blender").move_to(LEFT * 5.0 + UP * 1.6)
        godot = logo("godot").move_to(RIGHT * 5.0 + UP * 1.6)
        b_lab = T("Blender", 38).next_to(blender, DOWN, buff=0.25)
        g_lab = T("Godot", 38).next_to(godot, DOWN, buff=0.25)
        slab = RoundedRectangle(width=1.7, height=2.1, corner_radius=0.12, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(UP * 1.6)
        fold = Polygon(slab.get_corner(UR) + LEFT * 0.45, slab.get_corner(UR), slab.get_corner(UR) + DOWN * 0.45, color=INK, stroke_width=3, fill_color=GHOST, fill_opacity=1)
        f_lab = T("glTF", 40).move_to(slab)
        file = VGroup(slab, fold, f_lab)
        a1 = Arrow(blender.get_right(), slab.get_left(), buff=0.3, color=INK, stroke_width=4)
        a2 = Arrow(slab.get_right(), godot.get_left(), buff=0.3, color=INK, stroke_width=4)
        self.go(FadeIn(blender), FadeIn(b_lab), FadeIn(godot), FadeIn(g_lab), rt=0.7)

        rows = [("base colour", "1.00, 0.78, 0.34"), ("metallic", "1.0"), ("roughness", "0.2")]
        card = VGroup()
        box = RoundedRectangle(width=6.8, height=2.7, corner_radius=0.15, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=3).set_z_index(-2)
        head = T("material", 36, SOFT)
        lines = VGroup(*[VGroup(T(k, 36), T(v, 36)).arrange(RIGHT, buff=0.5) for k, v in rows])
        for ln in lines:
            ln[1].align_to(box, RIGHT).shift(LEFT * 0.35)
        body = VGroup(head, *lines).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        card = VGroup(box, body.move_to(box))
        for ln in lines:
            ln[1].move_to([box.get_right()[0] - 0.35 - ln[1].width / 2, ln[1].get_center()[1], 0])
        card.move_to(LEFT * 2.9 + DOWN * 1.9)
        self.at(2.4)
        self.go(FadeIn(card, shift=UP * 0.2), rt=0.6)

        self.at(3.55)
        self.go(FadeIn(file), GrowArrow(a1), card.animate.move_to(DOWN * 1.9), rt=0.9)

        ring = None
        for i, t in enumerate([5.76, 6.6, 7.16]):
            # a pale terracotta backing plate, not a thin terracotta ring (GATE T reads thin accent lines as text)
            box_i = SurroundingRectangle(lines[i], buff=0.1, stroke_width=0, fill_color=ACC, fill_opacity=0.25).set_z_index(-1)
            self.at(t)
            self.go(Create(box_i) if ring is None else ReplacementTransform(ring, box_i), rt=0.35)
            ring = box_i

        self.at(7.9)
        new_head = T("StandardMaterial3D", 36, SOFT).move_to(head, aligned_edge=LEFT)
        self.go(GrowArrow(a2), FadeOut(ring), card.animate.move_to(RIGHT * 2.9 + DOWN * 1.9), rt=1.0)
        self.at(9.3)
        new_head.move_to(head, aligned_edge=LEFT)
        self.go(Transform(head, new_head), rt=0.6)

        tick = VMobject(color=INK, stroke_width=8).set_points_as_corners([LEFT * 0.35 + UP * 0.02, LEFT * 0.08 + DOWN * 0.28, RIGHT * 0.42 + UP * 0.38])
        tick.next_to(card, LEFT, buff=0.4)
        same = T("same numbers", 38).next_to(tick, LEFT, buff=0.3)
        self.at(11.3)
        self.go(Create(tick), FadeIn(same), rt=0.6)
        self.end()
