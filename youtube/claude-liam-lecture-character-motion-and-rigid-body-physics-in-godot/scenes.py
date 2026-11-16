"""Self-contained lecture scenes. Conceptual diagrams are labeled; measured plots use lab data."""

from manim import *

from pathlib import Path

import json,re

import numpy as np

R=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-character-motion-and-rigid-body-physics-in-godot')

STAGE='#F2F0E9';INK='#3D3929';TERRA='#D97757';DIM='#8B8F96';PALE='#D9D4C7'

STAGE='#F2F0E9';INK='#3D3929';TERRA='#D97757';DIM='#8B8F96';PALE='#D9D4C7'

STAGE='#F2F0E9';INK='#3D3929';TERRA='#D97757';DIM='#8B8F96';PALE='#D9D4C7'

STAGE='#F2F0E9';INK='#3D3929';TERRA='#D97757';DIM='#8B8F96';PALE='#D9D4C7'

STAGE='#F2F0E9';INK='#3D3929';TERRA='#D97757';DIM='#8B8F96';PALE='#D9D4C7'

config.background_color=STAGE

config.frame_width=14.222222

config.frame_height=8

try: SHEET=json.loads((R/'beat_sheet.json').read_text());TARGET={b['beat_id']:b.get('actual_duration_s',b['estimated_duration_s']) for b in SHEET['beats']}
except Exception: TARGET={}

try: WORDS=json.loads((R/'mp3/words.json').read_text()).get('beats',{})
except Exception: WORDS={}

CUES={'B01':{.25:'Collision defines',.65:'A movement policy'},'B04':{.35:'when its parent moves'},'B07':{.25:'collected signal',.65:'score update'},'B10':{.25:'conveyor velocity',.65:'A platform'},'B14':{.25:'A rectangle',.65:'a capsule'},'B15':{.25:'The player scans',.65:'The coin scans'},'B20':{.25:'gravity is',.65:'Initial upward speed'},'B23':{.25:'Coyote time',.65:'Jump buffering'},'B27':{.25:'measured apex',.65:'Plot the measured samples'},'B30':{.25:'comparing origins',.65:'side and corner'},'B37':{.25:'sixty ticks',.65:'render-frame motion'},'B40':{.25:'intermediate poses',.65:'without simulating'},'B43':{.25:'An offset boundary',.65:'A wrong tile'},'B45':{.25:'ten percent',.65:'inside the band'},'B47':{.25:'Convex shapes',.65:'a few convex pieces'},'B48':{.25:'kinematic body',.65:'annotation'},'B50':{.25:'new object',.65:'debris deliberately'}}

def text(s,size=36,color=INK):return Text(s,font='EB Garamond',font_size=size,color=color)

def mono(s,size=28):return Text(s,font='Menlo',font_size=size,color=INK)

def bid(sc):return type(sc).__name__.split('_')[0]

def duration(sc):return float(TARGET.get(bid(sc),16))

def elapsed(sc):return float(sc.renderer.time)

def cue(sc,f):
 target=duration(sc)*f;phrase=CUES.get(bid(sc),{}).get(f)
 if phrase and WORDS.get(bid(sc)):
  words=WORDS[bid(sc)];norm=lambda s:re.sub(r'[^a-z0-9]','',s.lower());needle=[norm(x) for x in phrase.split()];stream=[norm(x['text']) for x in words]
  for i in range(len(stream)-len(needle)+1):
   if stream[i:i+len(needle)]==needle:target=words[i]['startFrame']/24;break
 if target>elapsed(sc):sc.wait(target-elapsed(sc))

def finish(sc):
 if duration(sc)-elapsed(sc)>.05:sc.wait(duration(sc)-elapsed(sc)-.05)

def head(sc,title,source='Conceptual diagram · not captured gameplay'):
 sc.add(text(title,44).move_to([0,3.05,0]),text(source,27).move_to([0,-2.85,0]),text('@NikBearBrown',23).move_to([5.2,-3.15,0]))

def box(label,at,w=2.5,h=1.0):
 r=RoundedRectangle(width=w,height=h,corner_radius=.1,stroke_color=INK,fill_color=STAGE,fill_opacity=1).move_to(at)
 t=text(label,32).move_to(at)
 if t.width>w-.25:t.scale_to_fit_width(w-.25)
 return VGroup(r,t)

def arrow(a,b):return Arrow(a,b,buff=.15,color=TERRA,stroke_width=5)

def actor(at):return Rectangle(width=.5,height=.8,stroke_color=TERRA,fill_color=TERRA,fill_opacity=.8).move_to(at)

class B01_Responsibilities(Scene):
 def construct(self):
  head(self,'Organization · Boundary · Motion')
  root=box('Level',[-3,1.6,0]);child=box('Player',[-3,-.2,0]);edge=Line([-3,1.1,0],[-3,.3,0],color=INK)
  self.add(root,child,edge)
  body=actor([1.2,0,0]);self.play(FadeIn(body),run_time=.5)
  cue(self,.25);outline=Rectangle(width=.72,height=1.02,color=INK).move_to(body);zone=Rectangle(width=1.4,height=2.8,color=DIM).move_to([4.3,0,0])
  self.play(Create(outline),Create(zone),run_time=.7);self.add(text('Sensor',32).move_to([4.3,2,0]))
  cue(self,.65);self.play(body.animate.shift(RIGHT*3.1),outline.animate.shift(RIGHT*3.1),run_time=1.2);self.play(zone.animate.set_stroke(TERRA,width=7),run_time=.5);finish(self)

class B10_Platforms(Scene):
 def construct(self):
  head(self,'Surface Velocity / Moving Geometry')
  left=Rectangle(width=4,height=.5,color=INK).move_to([-3.5,-1,0]);right=left.copy().move_to([3.2,-1,0]);self.add(left,right,text('Static conveyor',36).move_to([-3.5,1.8,0]),text('Animatable',36).move_to([3.2,1.8,0]))
  cue(self,.25);a=arrow([-5,-.2,0],[-2,-.2,0]);self.play(Create(a),run_time=.7)
  cue(self,.65);self.play(right.animate.shift(UP*1.5),run_time=1.2);finish(self)

NAMES=['World','One way','Player','Enemy','Pickup','Hazard','Debris']

def matrix(sc,review=False):
 head(sc,'Who Scans Whom?','Constructed collision policy · rows scan columns')
 x0=-3.0;y0=1.25;s=.68;rows=['Player','Coin','Enemy','Hazard','Debris'];hits=[[0,1],[2],[0,1,3],[2,3],[0]]
 cells=[]
 for j,n in enumerate(NAMES):sc.add(text(n,27).rotate(PI/4).move_to([x0+j*s,y0+1,0]))
 for i,n in enumerate(rows):
  sc.add(text(n,30).move_to([x0-1.3,y0-i*s,0]));row=[]
  for j in range(7):
   c=Square(side_length=s,stroke_color=DIM,stroke_width=2).move_to([x0+j*s,y0-i*s,0]);sc.add(c);row.append(c)
  cells.append(row)
 for i,row in enumerate(hits):
  if review and i==4:cue(sc,.25)
  elif i==1:cue(sc,.25)
  elif i==3:cue(sc,.65)
  sc.play(*[FadeIn(Dot(cells[i][j].get_center(),radius=.14,color=TERRA)) for j in row],run_time=.35)
 if review:
  cue(sc,.65);selfmark=Cross(cells[4][2],stroke_color=INK,stroke_width=6);sc.play(Create(selfmark),run_time=.5)
 finish(sc)

class B20_JumpMath(Scene):
 def construct(self):
  head(self,'Choose Height and Apex Time','Constructed continuous model · upward height is positive')
  h=MathTex(r'h=72\,\mathrm{px}',color=INK,font_size=46).move_to([-3.5,1.6,0]);t=MathTex(r't_a=0.38\,\mathrm{s}',color=INK,font_size=46).move_to([3.5,1.6,0]);self.add(h,t)
  curve=VMobject(color=TERRA,stroke_width=5).set_points_smoothly([np.array([3.6+1.8*u,-1.5+3*(2*u-u*u),0]) for u in np.linspace(0,1,20)]);self.play(Create(curve),run_time=.7)
  cue(self,.25);g=MathTex(r'g=\frac{2h}{t_a^2}\approx997.23\,\mathrm{px/s^2}',color=INK,font_size=40).move_to([-2,.1,0]);self.play(Write(g),run_time=1)
  cue(self,.65);v=MathTex(r'v_{y,0}=-g\,t_a\approx-378.95\,\mathrm{px/s}',color=TERRA,font_size=40).move_to([-2,-1.5,0]);self.play(Write(v),FadeIn(Dot([5.4,1.5,0],radius=.13,color=INK)),run_time=1);finish(self)

class B23_Timers(Scene):
 def construct(self):
  head(self,'Two Different Grace Windows','Constructed timeline · values are design choices')
  left=Line([-5,1,0],[5,1,0],color=INK);right=Line([-5,-1,0],[5,-1,0],color=INK);self.add(left,right,text('Leave ledge',32).move_to([-3,2,0]),text('Land',32).move_to([3,-2,0]))
  cue(self,.25);w1=Rectangle(width=2,height=.5,fill_color=TERRA,fill_opacity=.6,stroke_width=0).move_to([-2,1,0]);self.play(FadeIn(w1),run_time=.5);self.add(text('Coyote: 0.08 s',32).move_to([1,2,0]))
  cue(self,.65);w2=Rectangle(width=2.5,height=.5,fill_color=TERRA,fill_opacity=.6,stroke_width=0).move_to([1.75,-1,0]);self.play(FadeIn(w2),run_time=.5);self.add(text('Buffer: 0.10 s',32).move_to([-1.5,-2,0]));dot=Dot([1,-1,0],color=INK,radius=.13);self.play(FadeIn(dot),run_time=.3);self.play(w1.animate.set_opacity(.4),w2.animate.set_opacity(.4),run_time=.4);finish(self)

class B27_JumpMeasured(Scene):
 def construct(self):
  data=json.loads((R/'evidence/physics-results.json').read_text());rows=data['trajectory']
  head(self,'Design Target / Engine Samples','Actual Godot lab · fixed-step controller · 60 ticks/s')
  ax=Axes(x_range=[0,1.2,.2],y_range=[0,90,30],x_length=10,y_length=4,axis_config={'color':INK,'include_numbers':True,'font_size':25}).move_to([.2,-.2,0]);self.add(ax,text('Time (s)',30).move_to([0,-2.65,0]),text('Height (px)',30).move_to([-5,2.4,0]))
  line=DashedLine(ax.c2p(0,72),ax.c2p(1.15,72),color=DIM);self.add(line)
  cue(self,.25);graph=VMobject(color=TERRA,stroke_width=5).set_points_as_corners([ax.c2p(r['time'],r['height']) for r in rows]);self.play(Create(graph),run_time=1.2)
  cue(self,.65);peak=max(rows,key=lambda x:x['height']);p=Dot(ax.c2p(peak['time'],peak['height']),color=INK);self.play(FadeIn(p),run_time=.3);self.add(text(f"Apex: {peak['height']:.2f} px",32).move_to([2.8,2.25,0]));finish(self)

class B37_Ticks(Scene):
 def construct(self):
  head(self,'Physics Ticks / Rendered Frames')
  self.add(text('Physics',36).move_to([-5.4,1.1,0]),text('Render',36).move_to([-5.4,-1.1,0]))
  cue(self,.25);top=VGroup(*[Line([-3.5+i*1.5,.7,0],[-3.5+i*1.5,1.5,0],color=INK) for i in range(6)]);self.play(Create(top),run_time=.8)
  self.add(MathTex(r'\Delta t=\frac{1}{60}\,\mathrm{s}',font_size=42,color=INK).move_to([0,2.3,0]))
  cue(self,.65);bottom=VGroup(*[Line([-3.5+i*.625,-1.5,0],[-3.5+i*.625,-.7,0],color=TERRA) for i in range(13)]);self.play(Create(bottom),run_time=.9);self.add(text('Illustration: 144 Hz display',30).move_to([0,-2.2,0]));finish(self)

class B40_Interpolation(Scene):
 def construct(self):
  head(self,'Presentation Between States')
  a=actor([-4,0,0]).set_fill(DIM,.5);b=actor([4,0,0]).set_fill(DIM,.5);self.add(a,b,text('Previous tick',34).move_to([-4,1.6,0]),text('Current tick',34).move_to([4,1.6,0]))
  cue(self,.25);visible=actor([-4,0,0]);self.add(visible);self.play(visible.animate.shift(RIGHT*8),run_time=2,rate_func=linear)
  cue(self,.65);self.add(MathTex(r'x_r=(1-\alpha)x_{n-1}+\alpha x_n',font_size=44,color=INK).move_to([0,-1.8,0]));finish(self)

class B45_Tolerance(Scene):
 def construct(self):
  result=json.loads((R/'evidence/physics-results.json').read_text());peak=result['measurements']['jump_height']
  head(self,'A Measurement Has a Contract','Lab rubric · target 72 px · tolerance ±10%')
  ax=NumberLine(x_range=[60,84,4],length=10,include_numbers=True,font_size=30,color=INK).move_to([0,-.5,0]);self.add(ax)
  cue(self,.25);band=Rectangle(width=(79.2-64.8)/24*10,height=1.2,fill_color=TERRA,fill_opacity=.25,stroke_width=0).move_to(np.array([0,.1,0]));self.play(FadeIn(band),run_time=.6);self.add(MathTex(r'72\pm7.2\,\mathrm{px}',font_size=46,color=INK).move_to([0,2,0]))
  cue(self,.65);dot=Dot(np.array([(peak-72)/24*10,.1,0]),radius=.15,color=TERRA);self.play(FadeIn(dot),run_time=.5);self.add(text(f'{peak:.2f} px',36).next_to(dot,UP));finish(self)


CUES.update({'BT01':{.25:'Both use collision geometry',.65:'The same rectangle'},'BT08':{.25:'Moving an object',.65:'Prefer enter and exit'},'BT10':{.25:'enter and exit',.65:'a timer applies damage'},'BP01':{.25:'An impulse',.65:'doubling mass'}})


class BP01_ForceImpulse(Scene):
 def construct(self):
  head(self,'Force Over Time / One Impulse','Ideal model · neglects damping and other forces')
  self.add(Line([-5,1.4,0],[0,1.4,0],color=INK),text('Time',30).move_to([-2.5,.95,0]),text('Force',30).move_to([-5,1.9,0]))
  force=Rectangle(width=3,height=.8,color=TERRA,fill_color=TERRA,fill_opacity=.2).move_to([-2.5,1.8,0]);self.play(Create(force),run_time=.6)
  cue(self,.25);self.play(Create(Arrow([2.5,1.3,0],[2.5,2.3,0],buff=0,color=TERRA)),run_time=.6);self.add(text('Impulse',32).move_to([4.2,1.8,0]))
  cue(self,.65);self.add(MathTex(r'\Delta v=J/m',font_size=44,color=INK).move_to([0,.2,0]),box('Mass m',[-4,-1,0]),box('Mass 2m',[-4,-2,0]))
  self.play(Create(arrow([-2.5,-1,0],[3.5,-1,0])),Create(arrow([-2.5,-2,0],[.5,-2,0])),run_time=.8);self.add(text('Same impulse',30).move_to([3.5,-2,0]));finish(self)

