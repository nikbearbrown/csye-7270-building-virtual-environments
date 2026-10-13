"""Lecture mechanism scenes. Real screenshots are identified; diagrams are conceptual.
Self-contained for Gate A, literal Scene subclasses for run.sh discovery.
"""
from manim import *
from pathlib import Path
import json
import re
import numpy as np
R=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shading-language')
STAGE='#F2F0E9';INK='#3D3929';TERRA='#D97757';DIM='#8B8F96';GHOST='#D9D4C7'
config.background_color=STAGE
config.frame_width=14.222222
config.frame_height=8
try: DATA=json.loads((R/'beat_sheet.json').read_text()); TARGET={b['beat_id']:b.get('actual_duration_s',b['estimated_duration_s']) for b in DATA['beats']}
except Exception: TARGET={}
def tx(s,size=36,color=INK): return Text(s,font='EB Garamond',font_size=size,color=color)
def mono(s,size=32,color=INK):return Text(s,font='Menlo',font_size=size,color=color)
def bid(scene):return type(scene).__name__.split('_')[0]
def dur(scene):return float(TARGET.get(bid(scene),12))
def elapsed(scene):
 t=getattr(getattr(scene,'renderer',None),'time',0)
 return float(t) if isinstance(t,(int,float)) else 0.0
CUES={
 'B01':{.25:'Rasterization',.65:'The fragment function'},
 'B07':{.25:'Writing ALPHA',.68:'That alone'},
 'B09':{.29:'The drawn square shifts'},
 'B11':{.18:'quarter turn',.64:'half turn'},
 'B14':{.2:'Each fragment',.63:'Other pixels'},
 'B17':{.3:'or as red',.66:'underlying four values'},
 'B19':{.23:'Put one and two',.63:'Multiplying by'},
 'B30':{.22:'Between them',.63:'Halfway across'},
 'B33':{.22:'then three quarters',.36:'then one tenth',.64:'captured outputs'},
 'B35':{.15:'one',.28:'two',.65:'stop at three'},
 'B44':{.22:'alter one input',.64:'compare the result'}}
try: WORDS=json.loads((R/'mp3/words.json').read_text()).get('beats',{})
except Exception: WORDS={}
def cue(scene,f):
 target=dur(scene)*f
 phrase=CUES.get(bid(scene),{}).get(f)
 words=WORDS.get(bid(scene),[])
 if phrase and words:
  norm=lambda x:re.sub(r'[^a-z0-9]','',x.lower())
  wanted=[norm(x) for x in phrase.split()]
  stream=[norm(x['text']) for x in words]
  for i in range(len(stream)-len(wanted)+1):
   if stream[i:i+len(wanted)]==wanted:
    target=words[i]['startFrame']/24;break
 gap=target-elapsed(scene)
 if gap>0.01:scene.wait(gap)
def done(scene):
 gap=dur(scene)-0.05-elapsed(scene)
 if gap>0.01:scene.wait(gap)
def heading(scene,title,subtitle='Conceptual diagram'):
 scene.add(tx(title,44).move_to([0,3.05,0]))
 scene.add(tx(subtitle,30).move_to([0,-2.85,0]))
 scene.add(tx('@NikBearBrown',24).move_to([5.0,-3.15,0]))
def grid(w=6,h=4,cell=.65):
 return VGroup(*[Square(side_length=cell,stroke_color=GHOST,stroke_width=2,fill_color=STAGE,fill_opacity=1).move_to([(x-(w-1)/2)*cell,((h-1)/2-y)*cell,0]) for y in range(h) for x in range(w)])
def picture(name,width=5.9):
 return ImageMobject(str(R/'captures'/f'{name}.png')).set_width(width)

class B01_Pipeline(Scene):
 def construct(self):
  heading(self,'Geometry → Fragments','Conceptual pipeline · canvas_item')
  quad=Square(side_length=3.2,color=INK).move_to([-3.6,0,0])
  corners=VGroup(*[Dot([-3.6+x,y,0],radius=.12,color=TERRA) for x,y in [(-1.6,-1.6),(-1.6,1.6),(1.6,1.6),(1.6,-1.6)]])
  diagonal=Line([-5.2,-1.6,0],[-2,1.6,0],color=DIM)
  cells=grid(5,5,.6).move_to([3.5,0,0])
  self.add(tx('vertex()',36).move_to([-3.6,2.25,0]),quad,diagonal,corners)
  self.play(quad.animate.shift(RIGHT*.35),diagonal.animate.shift(RIGHT*.35),corners.animate.shift(RIGHT*.35),run_time=1)
  cue(self,.25)
  arrow=Arrow([-1.4,0,0],[.4,0,0],color=INK,buff=.1)
  self.play(Create(arrow),FadeIn(cells),run_time=.7)
  self.add(tx('fragment()',36).move_to([3.5,2.25,0]))
  cue(self,.65)
  self.play(*[c.animate.set_fill(TERRA,opacity=.65) for c in cells],run_time=1)
  done(self)

class B07_SpatialComparison(Scene):
 def construct(self):
  heading(self,'Opaque → Transparent','Actual Godot output · same cube, camera and lighting')
  left=picture('spatial').move_to([-3.25,0,0]);right=picture('alpha').move_to([3.25,0,0])
  self.add(left,tx('ALBEDO',36).move_to([-3.25,2.2,0]))
  cue(self,.25)
  self.play(FadeIn(right),run_time=.6)
  self.add(tx('ALPHA = 0.3',36).move_to([3.25,2.2,0]))
  cue(self,.68)
  ring=SurroundingRectangle(right,color=TERRA,buff=.08,stroke_width=5)
  self.play(Create(ring),run_time=.5)
  done(self)

class B09_Displacement(Scene):
 def construct(self):
  heading(self,'Rendered Geometry ≠ Collision','Conceptual overlay · displacement enlarged for visibility')
  collider=Square(side_length=2.9,stroke_color=INK,stroke_width=6).move_to([-2,0,0])
  drawn=Square(side_length=2.75,stroke_width=0,fill_color=DIM,fill_opacity=1).move_to([-2,0,0])
  self.add(drawn,collider,tx('Collision',36).move_to([-2,-2.2,0]))
  cue(self,.29)
  self.play(drawn.animate.shift(RIGHT*4.5).set_fill(TERRA),run_time=1.2)
  self.play(Create(Arrow([-1.0,2.0,0],[2.5,2.0,0],color=INK)),run_time=.4)
  self.add(tx('Rendered',36).move_to([2.5,-2.2,0]))
  done(self)

class B11_TimeInput(Scene):
 def construct(self):
  heading(self,'Time Is an Input','Conceptual clock · sin(TIME) in the executed wave.gdshader')
  dial=Circle(radius=1.45,color=INK).move_to([-4,0,0])
  pointer=Line([-4,0,0],[-2.55,0,0],color=TERRA,stroke_width=8)
  quad=Square(side_length=1.5,fill_color=DIM,fill_opacity=1,stroke_width=0).move_to([2,0,0])
  track=Line([.5,-1.3,0],[5.4,-1.3,0],color=INK)
  self.add(dial,pointer,quad,track,tx('Clock',36).move_to([-4,2.2,0]),tx('Offset',36).move_to([3,2.2,0]))
  cue(self,.18)
  self.play(Rotate(pointer,angle=PI/2,about_point=[-4,0,0]),quad.animate.shift(RIGHT*2),run_time=.9)
  cue(self,.64)
  self.play(Rotate(pointer,angle=PI/2,about_point=[-4,0,0]),quad.animate.shift(LEFT*2),run_time=.9)
  self.play(Create(Line([2,-1.7,0],[2,-.85,0],color=INK,stroke_width=6)),run_time=.4)
  done(self)

class B14_Independent(Scene):
 def construct(self):
  heading(self,'One Rule, Different Inputs','Conceptual invocations · no promised execution order')
  cells=grid(9,5,.72)
  self.add(cells)
  arrow=Arrow([-3.9,1.9,0],[3.9,1.9,0],color=DIM,buff=0)
  self.add(arrow,tx('A remembered sequence?',32).move_to([0,2.3,0]))
  cue(self,.2)
  self.play(FadeOut(arrow),run_time=.5)
  self.play(*[cells[i].animate.set_fill(INK,opacity=.65) for i in [0,8,22,36,44]],run_time=.65)
  cue(self,.63)
  self.play(*[c.animate.set_fill(TERRA if i==22 else DIM,opacity=.8) for i,c in enumerate(cells)],run_time=.8)
  done(self)

class B17_VectorCells(Scene):
 def construct(self):
  heading(self,'Same Components, Different Names','Values from swizzle.gdshader')
  xs=[-4.5,-1.5,1.5,4.5]
  cells=VGroup(*[Square(side_length=2.25,stroke_color=DIM,fill_color='#FAF9F5',fill_opacity=1).move_to([x,0,0]) for x in xs])
  values=VGroup(*[mono(v,42).move_to([x,0,0]) for x,v in zip(xs,['0.2','0.6','0.9','1.0'])])
  labels=VGroup(*[tx(v,42).move_to([x,1.8,0]) for x,v in zip(xs,['x','y','z','w'])])
  self.add(cells,values,labels)
  cue(self,.3)
  colorlabels=VGroup(*[tx(v,42).move_to([x,1.8,0]) for x,v in zip(xs,['r','g','b','a'])])
  self.play(Transform(labels,colorlabels),run_time=.7)
  cue(self,.66)
  self.play(Create(SurroundingRectangle(cells[0],color=TERRA,buff=.12,stroke_width=6)),run_time=.45)
  done(self)

class B19_MatrixColumns(Scene):
 def construct(self):
  heading(self,'The Constructor Takes Columns','Constructed example · verified by matrix.gdshader pixels')
  col1=MathTex(r'\begin{bmatrix}1\\2\end{bmatrix}',color=INK,font_size=56).move_to([-4,0,0])
  col2=MathTex(r'\begin{bmatrix}3\\4\end{bmatrix}',color=INK,font_size=56).move_to([-1.5,0,0])
  matrix=MathTex(r'\begin{bmatrix}1&3\\2&4\end{bmatrix}',color=INK,font_size=56).move_to([3,0,0])
  self.add(col1,col2,tx('column 0',32).move_to([-4,2,0]),tx('column 1',32).move_to([-1.5,2,0]))
  cue(self,.23)
  self.play(TransformFromCopy(VGroup(col1,col2),matrix),run_time=.9)
  self.play(Create(Rectangle(width=.5,height=1.3,stroke_color=DIM).move_to([2.7,0,0])),run_time=.3)
  cue(self,.63)
  result=MathTex(r'\begin{bmatrix}1&3\\2&4\end{bmatrix}\begin{bmatrix}1\\0\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix}',color=INK,font_size=42).move_to([0,-2.1,0])
  self.play(Write(result),run_time=.9)
  self.play(Create(Rectangle(width=.65,height=1.5,stroke_color=TERRA).move_to([2.7,0,0])),run_time=.4)
  done(self)

class B30_Interpolation(Scene):
 def construct(self):
  heading(self,'Between the Vertices','Flat rectangle example · varying horizontal = UV.x')
  left=Dot([-5,0,0],radius=.16,color=INK);right=Dot([5,0,0],radius=.16,color=INK)
  self.add(left,right,tx('0',40).move_to([-5,1.5,0]),tx('1',40).move_to([5,1.5,0]))
  strips=VGroup(*[Rectangle(width=.25,height=2,stroke_width=0,fill_color=interpolate_color(BLACK,WHITE,i/39),fill_opacity=1).move_to([-4.875+i*.25,0,0]) for i in range(40)])
  cue(self,.22)
  self.play(FadeIn(strips),run_time=.9)
  cue(self,.63)
  marker=Line([0,-1.4,0],[0,1.4,0],color=TERRA,stroke_width=6)
  self.play(Create(marker),run_time=.5)
  self.add(tx('0.5',40).move_to([0,2,0]))
  done(self)

class B33_Fallthrough(Scene):
 def construct(self):
  heading(self,'Accepted Code, Different Meaning','Actual Godot render · mode = 1 in both cases')
  left=picture('switch',5.5).move_to([-3.3,-.55,0]);right=picture('fallthrough',5.5).move_to([3.3,-.55,0])
  self.add(left,tx('With breaks',34).move_to([-3.3,1.6,0]))
  labels=VGroup(*[mono(x,36).move_to([p,2.25,0]) for p,x in zip([-1.8,1,3.8],['0.25','0.75','0.10'])])
  self.add(labels)
  marker=SurroundingRectangle(labels[0],color=TERRA,buff=.12)
  self.play(Create(marker),run_time=.35)
  cue(self,.22)
  self.play(Transform(marker,SurroundingRectangle(labels[1],color=TERRA,buff=.12)),run_time=.45)
  cue(self,.36)
  self.play(Transform(marker,SurroundingRectangle(labels[2],color=TERRA,buff=.12)),run_time=.45)
  cue(self,.64)
  self.play(FadeIn(right),run_time=.6)
  self.add(tx('Fallthrough',34).move_to([3.3,1.6,0]))
  done(self)

class B35_LoopTrace(Scene):
 def construct(self):
  heading(self,'Prove Progress, Then Stop','Bounded trace of loop.gdshader · no infinite loop executed')
  xs=[-4,-1,2]
  boxes=VGroup(*[Square(side_length=2,stroke_color=DIM).move_to([x,0,0]) for x in xs])
  vals=VGroup(*[mono(v,38).move_to([x,0,0]) for x,v in zip(xs,['0.2','0.3','0.5'])])
  ids=VGroup(*[tx(str(i),36).move_to([x,1.65,0]) for i,x in enumerate(xs)])
  marker=SurroundingRectangle(boxes[0],color=TERRA,buff=.08)
  self.add(boxes,vals,ids,marker)
  cue(self,.15)
  self.play(Transform(marker,SurroundingRectangle(boxes[1],color=TERRA,buff=.08)),run_time=.4)
  cue(self,.28)
  self.play(Transform(marker,SurroundingRectangle(boxes[2],color=TERRA,buff=.08)),run_time=.4)
  cue(self,.65)
  stop=tx('3 · stop',40).move_to([5,0,0])
  self.play(FadeIn(stop),Transform(marker,SurroundingRectangle(stop,color=TERRA,buff=.15)),run_time=.5)
  done(self)

class B44_Experiment(Scene):
 def construct(self):
  heading(self,'Predict → Change → Compare','Controlled experiment · same surface and input contract')
  original=Square(side_length=2.3,fill_color=DIM,fill_opacity=1,stroke_width=0).move_to([-3.5,0,0])
  prediction=Square(side_length=2.3,stroke_color=INK,stroke_width=5).move_to([3.5,0,0])
  self.add(original,prediction,tx('Base',36).move_to([-3.5,2,0]),tx('Prediction',36).move_to([3.5,2,0]))
  cue(self,.22)
  self.play(prediction.animate.set_fill(TERRA,opacity=.65),run_time=.6)
  cue(self,.64)
  self.play(original.animate.set_fill(TERRA,opacity=.65),run_time=.6)
  comparison=Line([-1.8,-1.9,0],[1.8,-1.9,0],color=INK,stroke_width=4)
  self.play(Create(comparison),run_time=.4)
  self.add(tx('Compare',36).move_to([0,-2.2,0]))
  done(self)
