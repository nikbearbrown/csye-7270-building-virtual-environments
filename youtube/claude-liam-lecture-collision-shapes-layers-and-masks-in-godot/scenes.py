"""Self-contained lecture scenes. Conceptual diagrams are labeled; measured plots use lab data."""

from manim import *

from pathlib import Path

import json,re

import numpy as np

R=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-collision-shapes-layers-and-masks-in-godot')

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

class B10_Platforms(Scene):
 def construct(self):
  head(self,'Surface Velocity / Moving Geometry')
  left=Rectangle(width=4,height=.5,color=INK).move_to([-3.5,-1,0]);right=left.copy().move_to([3.2,-1,0]);self.add(left,right,text('Static conveyor',36).move_to([-3.5,1.8,0]),text('Animatable',36).move_to([3.2,1.8,0]))
  cue(self,.25);a=arrow([-5,-.2,0],[-2,-.2,0]);self.play(Create(a),run_time=.7)
  cue(self,.65);self.play(right.animate.shift(UP*1.5),run_time=1.2);finish(self)

class B14_Shapes(Scene):
 def construct(self):
  head(self,'Appearance / Collision Boundary')
  art=RoundedRectangle(width=2.2,height=3.0,corner_radius=.45,fill_color=PALE,fill_opacity=1,stroke_width=0).move_to([-3,0,0]);rect=Rectangle(width=2.2,height=3,color=TERRA,stroke_width=6).move_to(art)
  self.add(art,text('Artwork',34).move_to([-3,-2.1,0]))
  cue(self,.25);self.play(Create(rect),run_time=.6)
  cap=RoundedRectangle(width=2.2,height=3,corner_radius=1.09,color=TERRA,stroke_width=6).move_to([3,0,0])
  cue(self,.65);self.play(FadeIn(art.copy().move_to([3,0,0])),Create(cap),run_time=.7);self.add(text('Rectangle',34).move_to([-3,2.2,0]),text('Capsule',34).move_to([3,2.2,0]));finish(self)

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

class B15_Matrix(Scene):
 def construct(self):matrix(self)

class B43_Diagnostics(Scene):
 def construct(self):
  head(self,'Symptom → Hypothesis → Test')
  pairs=[('Missed coin','Mask / monitoring'),('Offset shape','Scale / ownership'),('Wrong tile','Contact / coordinates'),('Slope flicker','Order / snap')]
  for i,(a,b) in enumerate(pairs):
   if i==1:cue(self,.25)
   if i==2:cue(self,.65)
   y=1.6-i*1.05;l=text(a,36).move_to([-3.4,y,0]);r=text(b,36).move_to([3,y,0]);self.play(FadeIn(l),Create(arrow([-1,y,0],[.4,y,0])),FadeIn(r),run_time=.45)
  finish(self)

class B47_Geometry(Scene):
 def construct(self):
  head(self,'Convex Hull / Compound Shapes','Conceptual cross-section of a 3D collider')
  points=[[-1.7,-1,0],[1.7,-1,0],[1.7,1,0],[.6,1,0],[.6,0,0],[-.6,0,0],[-.6,1,0],[-1.7,1,0]]
  outline=Polygon(*points,color=INK).shift(LEFT*3.5);self.add(outline,text('Concave outline',34).move_to([-3.5,2,0]))
  cue(self,.25);hull=Rectangle(width=3.4,height=2,color=TERRA,fill_opacity=.25,fill_color=TERRA).move_to([-3.5,0,0]);self.play(Create(hull),run_time=.7)
  cue(self,.65);parts=VGroup(Rectangle(width=3.4,height=1).move_to([3.5,-.5,0]),Rectangle(width=1.1,height=1).move_to([2.35,.5,0]),Rectangle(width=1.1,height=1).move_to([4.65,.5,0])).set_color(TERRA);self.play(Create(parts),run_time=.8);self.add(text('Compound convex',34).move_to([3.5,2,0]));finish(self)

class B48_Migration(Scene):
 def construct(self):
  head(self,'Check the API Generation','Reference comparison · old forms are intentionally not executable here')
  pairs=[('KinematicBody2D','CharacterBody2D'),('scene.instance()','scene.instantiate()'),('yield(...)','await signal'),('export var','@export var')]
  self.add(text('Godot 3',36).move_to([-3.4,2,0]),text('Godot 4',36).move_to([3.4,2,0]))
  for i,(old,new) in enumerate(pairs):
   if i==1:cue(self,.25)
   if i==2:cue(self,.65)
   y=1.1-i*.95;self.add(mono(old,28).move_to([-3.4,y,0]));self.play(FadeIn(mono(new,28).move_to([3.4,y,0])),Create(arrow([-.8,y,0],[.8,y,0])),run_time=.5)
  finish(self)

class B50_MatrixReview(Scene):
 def construct(self):matrix(self,review=True)


CUES.update({'BT01':{.25:'Both use collision geometry',.65:'The same rectangle'},'BT08':{.25:'Moving an object',.65:'Prefer enter and exit'},'BT10':{.25:'enter and exit',.65:'a timer applies damage'},'BP01':{.25:'An impulse',.65:'doubling mass'}})

