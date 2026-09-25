"""Course-owned mechanism animations. Source-sized facts and constructed diagrams
are labelled in the beat sheet. No simulated engine viewport or invented result.
"""
from manim import *
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SHEET = json.loads((ROOT / 'beat_sheet.json').read_text())
BG, INK, ACC, EDGE = '#FAF9F5', '#3D3929', '#D97757', '#CEC9BE'
config.background_color = BG
config.frame_width = 16
config.frame_height = 9

class CourseMechanism(Scene):
    bid = ''
    def label(self, text, size=48):
        return Text(text, font='EB Garamond', font_size=size, color=INK, disable_ligatures=False)
    def box(self, text, pos, width=3.0):
        label = self.label(text)
        if label.width > width - .25 and ' ' in text:
            label = self.label(text.replace(' ', '\n', 1),44)
        if label.width > width - .25:
            raise ValueError(f'Text too wide at readable size: {text}')
        border = RoundedRectangle(width=width,height=max(1.05,label.height+.35),corner_radius=.06,color=EDGE,stroke_width=3)
        return VGroup(border,label).move_to(pos)
    def construct(self):
        b = next(x for x in SHEET['beats'] if x['beat_id']==self.bid)
        p=b['shot']['manim']; mode=p['mode']; names=p['labels']
        self.camera.background_color=BG
        title=self.label(b['heading'],58).to_edge(UP,buff=.65)
        footer=self.label(p['footer'],37).to_edge(DOWN,buff=.65)
        if title.width>13.7 or footer.width>13.7: raise ValueError('Text exceeds safe width')
        self.play(FadeIn(title),Create(Line([-6.8,2.85,0],[6.8,2.85,0],color=EDGE)),run_time=.65)
        if mode in ('roles','sequence','pipeline','learning','revise'):
            n=len(names); spacing=3.3 if n==4 else 2.75; width=2.85 if n==4 else 2.48
            boxes=[self.box(s,[(i-(n-1)/2)*spacing,.05,0],width) for i,s in enumerate(names)]
            for i,box in enumerate(boxes):
                self.play(FadeIn(box,shift=UP*.15),run_time=.55)
                if i: self.play(GrowArrow(Arrow(boxes[i-1].get_right(),box.get_left(),buff=.10,color=INK,stroke_width=4)),run_time=.45)
            for box in boxes: self.play(box[0].animate.set_stroke(ACC,5),run_time=.4)
            self.play(FadeIn(footer),run_time=.5)
        elif mode in ('loop','capacities'):
            n=len(names); radius=2.1 if n==6 else 2.0
            nodes=[]
            for i,s in enumerate(names):
                a=PI/2-i*TAU/n; pos=np.array([radius*1.9*np.cos(a),radius*np.sin(a)-.25,0])
                node=self.box(s,pos,2.55 if n==6 else 1.7); nodes.append(node)
                self.play(FadeIn(node),run_time=.45)
            if n==6:
                for i,node in enumerate(nodes):
                    nxt=nodes[(i+1)%n]
                    direction=nxt.get_center()-node.get_center()
                    direction=direction/np.linalg.norm(direction)
                    start=node.get_boundary_point(direction)+direction*.08
                    end=nxt.get_boundary_point(-direction)-direction*.08
                    self.play(GrowArrow(Arrow(start,end,buff=0,color=INK,stroke_width=3)),run_time=.3)
            else:
                center=self.label('Supervision',48).move_to([0,-.3,0]); self.play(FadeIn(center),run_time=.5)
                for node in nodes: self.play(node[0].animate.set_stroke(ACC,5),run_time=.3)
            self.play(FadeIn(footer),run_time=.5)
        elif mode in ('compare','boundary'):
            left=self.box(names[0],[-3.4,.3,0],5.5); right=self.box(names[1],[3.4,.3,0],5.5)
            self.play(FadeIn(left),run_time=.7)
            self.play(FadeIn(right),run_time=.7)
            self.play(Create(Line([0,-1.9,0],[0,1.9,0],color=ACC,stroke_width=5)),run_time=.7)
            sub1=self.label('Observed checks',40).move_to([-3.4,-1.1,0]); sub2=self.label('Human judgment',40).move_to([3.4,-1.1,0])
            self.play(FadeIn(sub1),FadeIn(sub2),run_time=.6)
            self.play(FadeIn(footer),run_time=.5)
        elif mode=='collision':
            shape=Polygon([-1.9,-1.2,0],[-1.9,1.5,0],[-2.3,2,0],[-1.3,1.75,0],[1.2,1.75,0],[2.3,2,0],[1.9,1.5,0],[1.9,-1.2,0],color=EDGE,fill_color=EDGE,fill_opacity=.45,stroke_width=3).shift(LEFT*1.6+DOWN*.2)
            self.play(DrawBorderThenFill(shape),run_time=1.2)
            collider=Rectangle(width=1.8,height=2.8,color=ACC,stroke_width=7).move_to([-1.6,.15,0]); self.play(Create(collider),run_time=1)
            dim=self.label(names[0],55).move_to([-1.6,-2.0,0]); art=self.label(names[1],44).move_to([3.6,1,0]); contract=self.label(names[2],44).move_to([3.6,-.65,0])
            self.play(FadeIn(dim),FadeIn(art),run_time=.6)
            self.play(FadeIn(contract),GrowArrow(Arrow([1.2,-.65,0],[-.5,-.65,0],buff=.1,color=INK)),run_time=.7)
            self.play(FadeIn(footer),run_time=.5)
        elif mode=='dependencies':
            center=self.box(names[0],[-3.8,0,0],3.4);self.play(FadeIn(center),run_time=.6)
            for i,s in enumerate(names[1:]):
                child=self.box(s,[3.2,1.8-i*1.8,0],3.4)
                self.play(FadeIn(child),GrowArrow(Arrow(center.get_right(),child.get_left(),buff=.1,color=INK)),run_time=.7)
            self.play(center[0].animate.set_stroke(ACC,5),FadeIn(footer),run_time=.6)
        elif mode=='timeline':
            line=Line([-6.1,-.5,0],[6.1,-.5,0],color=INK,stroke_width=4);self.play(Create(line),run_time=.8)
            for i,s in enumerate(names):
                x=-5.5+i*3.65;dot=Dot([x,-.5,0],radius=.11,color=ACC);label=self.label(s,46).move_to([x,.55,0])
                self.play(FadeIn(label),GrowFromCenter(dot),run_time=.65)
            self.play(FadeIn(footer),run_time=.5)
        else: raise ValueError(mode)
        remaining=float(b['actual_duration_s'])-self.renderer.time
        if remaining<0: raise ValueError(f'{self.bid}: animation exceeds audio clock')
        self.wait(remaining)

class B02_Roles(CourseMechanism): bid='B02'
class B05_Loop(CourseMechanism): bid='B05'
class B07_Capacities(CourseMechanism): bid='B07'
class B09_Sequence(CourseMechanism): bid='B09'
class B11_Interpretation(CourseMechanism): bid='B11'
class B15_Collision(CourseMechanism): bid='B15'
class B18_Dependencies(CourseMechanism): bid='B18'
class B20_Revision(CourseMechanism): bid='B20'
class B22_Pipeline(CourseMechanism): bid='B22'
class B24_Time(CourseMechanism): bid='B24'
class B28_Learning(CourseMechanism): bid='B28'
class B31_Boundary(CourseMechanism): bid='B31'
