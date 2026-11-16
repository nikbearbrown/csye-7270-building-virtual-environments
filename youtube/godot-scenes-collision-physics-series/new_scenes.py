# These definitions are appended to each film's self-contained helper module.
CUES.update({'BT01':{.25:'Both use collision geometry',.65:'The same rectangle'},'BT08':{.25:'Moving an object',.65:'Prefer enter and exit'},'BT10':{.25:'enter and exit',.65:'a timer applies damage'},'BP01':{.25:'An impulse',.65:'doubling mass'}})

class BT01_BlockOrDetect(Scene):
 def construct(self):
  head(self,'Solid Boundary / Overlap Sensor')
  wall=Rectangle(width=1.2,height=1.2,color=INK,fill_color=INK,fill_opacity=.85).move_to([0,1,0])
  zone=Rectangle(width=1.2,height=1.2,color=TERRA,fill_color=TERRA,fill_opacity=.15).move_to([0,-1.1,0])
  p=actor([-4,1,0]);q=actor([-4,-1.1,0]);self.add(wall,zone,p,q,text('Body',34).move_to([3.4,1,0]),text('Area',34).move_to([3.4,-1.1,0]))
  cue(self,.25);self.play(Create(arrow([-4,2,0],[-.8,2,0])),Create(arrow([-4,-2.1,0],[2,-2.1,0])),run_time=.6)
  cue(self,.65);self.play(p.animate.move_to([-.87,1,0]),q.animate.move_to([0,-1.1,0]),run_time=1)
  event=Dot([0,-1.1,0],radius=.14,color=INK);self.play(FadeIn(event),run_time=.2);self.play(q.animate.move_to([2,-1.1,0]),run_time=.7)
  self.add(text('Stopped',30).move_to([-3,1,0]),text('Entry detected',30).move_to([-3,-1.1,0]));finish(self)

class BT08_OverlapClock(Scene):
 def construct(self):
  head(self,'Movement / Physics Update / Observation','Conceptual sequence · update delay is not to scale')
  region=Rectangle(width=1.5,height=1.8,color=TERRA).move_to([0,.6,0]);p=actor([-4,.6,0]);readout=box('Cached count: 0',[3.6,.6,0],3.8)
  self.add(region,p,readout,Line([-5,-1.5,0],[5,-1.5,0],color=DIM))
  cue(self,.25);self.play(p.animate.move_to([0,.6,0]),run_time=.8);self.play(FadeIn(Dot([-2,-1.5,0],radius=.15,color=TERRA)),run_time=.3);self.add(text('Move',30).move_to([-2,-2.1,0]))
  cue(self,.65);tick=Line([1,-1.9,0],[1,-1.1,0],color=INK,stroke_width=5);self.play(Create(tick),run_time=.4);self.add(text('Physics update',30).move_to([2,-2.1,0]));self.play(Transform(readout[1],text('Observed count: 1',30).move_to([3.6,.6,0])),run_time=.5);finish(self)

class BT10_Occupancy(Scene):
 def construct(self):
  head(self,'Enter Is an Event. Staying Is State.','Constructed damage policy · not an executed damage-zone test')
  self.add(Line([-5,0,0],[5,0,0],color=INK),text('Enter',34).move_to([-4,1.5,0]),text('Exit',34).move_to([4,1.5,0]))
  cue(self,.25);band=Rectangle(width=8,height=.5,color=TERRA,fill_color=TERRA,fill_opacity=.25).move_to([0,0,0]);self.play(FadeIn(band),FadeIn(Dot([-4,0,0],radius=.16,color=INK)),run_time=.6)
  cue(self,.65)
  for x in [-2,0,2]:self.play(Create(Line([x,-.7,0],[x,.7,0],color=TERRA,stroke_width=5)),run_time=.25)
  self.play(FadeIn(Dot([4,0,0],radius=.16,color=INK)),run_time=.3);self.add(text('Timer pulses while occupied',34).move_to([0,-1.6,0]),text('Policy chooses interval and first hit',30).move_to([0,-2.2,0]));finish(self)

class BP01_ForceImpulse(Scene):
 def construct(self):
  head(self,'Force Over Time / One Impulse','Ideal model · neglects damping and other forces')
  self.add(Line([-5,1.4,0],[0,1.4,0],color=INK),text('Time',30).move_to([-2.5,.95,0]),text('Force',30).move_to([-5,1.9,0]))
  force=Rectangle(width=3,height=.8,color=TERRA,fill_color=TERRA,fill_opacity=.2).move_to([-2.5,1.8,0]);self.play(Create(force),run_time=.6)
  cue(self,.25);self.play(Create(Arrow([2.5,1.3,0],[2.5,2.3,0],buff=0,color=TERRA)),run_time=.6);self.add(text('Impulse',32).move_to([4.2,1.8,0]))
  cue(self,.65);self.add(MathTex(r'\Delta v=J/m',font_size=44,color=INK).move_to([0,.2,0]),box('Mass m',[-4,-1,0]),box('Mass 2m',[-4,-2,0]))
  self.play(Create(arrow([-2.5,-1,0],[3.5,-1,0])),Create(arrow([-2.5,-2,0],[.5,-2,0])),run_time=.8);self.add(text('Same impulse',30).move_to([3.5,-2,0]));finish(self)
