"""SEIS v005: volumetric articulated limbs, authored from supplied robot references.
Front -Y; metres; L=+X. No external assets and no scene lifecycle operations.
"""
import math
from math import sin, cos, pi, copysign
from mathutils import Vector


def build_limbs(U):
    """Build closed armor castings, recessed red enamel, mechanical joints and hands."""
    def lerp(a,b,t): return a+(b-a)*t
    def curve(keys,t):
        """C1 cubic Hermite interpolation with time-aware central derivatives.

        Each component is interpolated in the independent station parameter t.
        In contrast to applying one smoothstep fraction to every component of a
        segment, the adjacent-station derivatives create genuine curved spatial
        paths and continuously varying casting radii.
        """
        if t <= keys[0][0]: return keys[0][1]
        if t >= keys[-1][0]: return keys[-1][1]
        def tangent(i):
            if i == 0:
                return (keys[1][1]-keys[0][1])/(keys[1][0]-keys[0][0])
            if i == len(keys)-1:
                return (keys[-1][1]-keys[-2][1])/(keys[-1][0]-keys[-2][0])
            dt0=keys[i][0]-keys[i-1][0];dt1=keys[i+1][0]-keys[i][0]
            v0=(keys[i][1]-keys[i-1][1])/dt0
            v1=(keys[i+1][1]-keys[i][1])/dt1
            return (v0*dt1+v1*dt0)/(dt0+dt1)
        for j in range(len(keys)-1):
            if t <= keys[j+1][0]:
                a,b=keys[j],keys[j+1];dt=b[0]-a[0];q=(t-a[0])/dt
                q2=q*q;q3=q2*q
                return ((2*q3-3*q2+1)*a[1]+(q3-2*q2+q)*dt*tangent(j)
                        +(-2*q3+3*q2)*b[1]+(q3-q2)*dt*tangent(j+1))
        return keys[-1][1]
    def P(s,p): return (s*p[0],p[1],p[2])
    def path(s,ps): return [P(s,p) for p in ps]
    def line(name,ps,r=.0012,mat='dark'): return U.line(name,ps,r,mat)
    def frame_shell(name, point, rows=48,cols=64, mat='armor', thickness=.005, edgewear=True, handedness=1):
        """Watertight shell over an analytic rectangular surface; perimeter has wall thickness."""
        vs=[]; fs=[]; wear=[]
        for inner in (0,1):
            for j in range(rows+1):
                t=j/rows
                for k in range(cols+1):
                    a=k/cols
                    p=Vector(point(t,a))
                    # Surface normal from local derivatives; inner layer is inset.
                    d1=Vector(point(min(1,t+.0002),a))-Vector(point(max(0,t-.0002),a))
                    d2=Vector(point(t,min(1,a+.0002)))-Vector(point(t,max(0,a-.0002)))
                    n=d2.cross(d1).normalized()*handedness
                    # Most casting surfaces point away from limb axis. Direction handled by point ordering.
                    p += n * (-thickness if inner else 0)
                    vs.append(tuple(p))
                    w=max(max(0,1-min(t,1-t)*22),max(0,1-min(a,1-a)*30))
                    wear.append(w*.9 if edgewear and not inner else .08)
        count=(rows+1)*(cols+1)
        for inner in (0,1):
            off=inner*count
            for j in range(rows):
                for k in range(cols):
                    a=off+j*(cols+1)+k; face=(a,a+1,a+cols+2,a+cols+1)
                    fs.append(face if not inner else tuple(reversed(face)))
        for j in (0,rows):
            for k in range(cols):
                a=j*(cols+1)+k; b=a+1; fs.append((a,b,b+count,a+count))
        for k in (0,cols):
            for j in range(rows):
                a=j*(cols+1)+k;b=a+cols+1;fs.append((a,b,b+count,a+count))
        return U.mesh(name,vs,fs,mat,wear)
    def housing(name,s,stations,opening,phi=0,inset=.010,red=True,seams=True,window_shape=None,inset_mat='red',window_range=(.11,.91)):
        """Closed wraparound casting with a genuine front window and inset enamel.
        stations: (t, local center X, center Y, Z, halfwidth, halfdepth).
        The red component occupies a separate lower surface inside the opening.
        """
        coords=[[ (v[0],v[k]) for v in stations] for k in range(1,6)]
        def val(t):
            values=[curve(k,t) for k in coords]
            values[3]=max(.004,values[3]);values[4]=max(.004,values[4])
            return values
        def surf(t,angle,offset=0):
            x,y,z,rx,ry=val(t)
            # Slight superellipse gives cast planes, unlike a cylindrical tube or pill.
            sx=sin(angle);cy=cos(angle)
            xx=copysign(abs(sx)**.84,sx); yy=copysign(abs(cy)**.84,cy)
            return (s*(x+(rx+offset)*xx), y-(ry+offset)*yy, z)
        def window(t):
            if window_shape is not None: return window_shape(t)
            al=curve(opening,t); return (phi-al,phi+al)
        def back(t,u):
            a,b=window(t);theta=b+u*(2*pi+a-b)
            return surf(t,theta)
        frame_shell(name+'_Cast_Housing',back,64,72,'armor',.006,handedness=s)
        # Internal liner follows the housing completely, visible only within narrow seams and wells.
        rows=[]
        for t,x,y,z,rx,ry in stations: rows.append((s*x,y,z,rx-.020,ry-.020))
        U.loft(name+'_Inner_Liner',rows,'dark',segments=48,steps=4,thickness=.003)
        # Inset window stops before the end of the shell; matching cap plates close ends.
        t0,t1=window_range
        def inset_surface(t,u):
            tt=lerp(t0,t1,t);a,b=window(tt);mid=(a+b)*.5;a=lerp(mid,a,.93);b=lerp(mid,b,.93)
            return surf(tt,lerp(a,b,u),-inset)
        if red: frame_shell(name+'_Recessed_Enamel',inset_surface,44,32,inset_mat,.003,False,handedness=s)
        # The front window is bordered by a dark deep gasket, then a cast stepped chamfer.
        for sign,tag in [(-1,'Medial'),(1,'Lateral')]:
            def border(t,u,sign=sign):
                tt=lerp(.095,.935,t);a,b=window(tt)
                ang=(a if sign<0 else b)+sign*lerp(-.025,.060,u)
                off=lerp(-.004,.0008,u)
                return surf(tt,ang,off)
            frame_shell(name+'_Window_Chamfer_'+tag,border,48,5,'armor',.002,handedness=s)
            ps=[]
            for j in range(37):
                tt=lerp(.12,.915,j/36);a,b=window(tt);mid=(a+b)*.5;ang=lerp(mid,a if sign<0 else b,.94);ps.append(surf(tt,ang,-.006))
            line(name+'_Window_Gasket_'+tag,ps,.0016,'rubber')
            ps=[]
            for j in range(37):
                tt=lerp(.12,.915,j/36);a,b=window(tt);ps.append(surf(tt,(a if sign<0 else b)+sign*.043,.0010))
            line(name+'_Milled_Lip_'+tag,ps,.00065,'edge')
        # Short front closure at either extremity; no dangling leaf tips.
        for lo,hi,tag in [(0,.125,'Cuff'),(.90,1,'Crown')]:
            def cap(t,u,lo=lo,hi=hi):
                tt=lerp(lo,hi,t);a,b=window(tt)
                return surf(tt,lerp(a-.01,b+.01,u),.0007)
            frame_shell(name+'_Closed_'+tag,cap,12,22,'armor',.005,handedness=s)
        if seams:
            # Long manufacturing seams delineate a broad outer/back shell and side service covers.
            for a,tag in [(phi+1.22,'Outer'),(phi-1.25,'Inner'),(phi+2.70,'Rear')]:
                ps=[surf(lerp(.10,.92,j/42),a+.035*sin(pi*j/42),.0010) for j in range(43)]
                line(name+'_Panel_Seam_'+tag,ps,.00105,'rubber')
                if tag!='Rear':
                    ps=[surf(lerp(.18,.86,j/36),a+.035*sin(pi*j/36)+.025,.0016) for j in range(37)]
                    line(name+'_Panel_Steel_Edge_'+tag,ps,.00040,'silver')
            for t,tag in [(.22,'Lower'),(.73,'Upper')]:
                ps=[surf(t+.020*sin(pi*j/30),phi+.92+j/30*1.42,.0012) for j in range(31)]
                line(name+'_Service_Panel_Crosscut_'+tag,ps,.0012,'rubber')
        return surf
    def joint(name,s,loc,r=.045,axis=(1,0,0)):
        """Dark recessed bearing cup with actual surround, no target graphic circles."""
        loc=Vector(loc); ax=Vector(axis).normalized()
        U.cylinder(name+'_Recess',loc,r,.025,'rubber',axis,vertices=56,bevel=.001)
        U.cylinder(name+'_Bearing_Wall',loc+ax*.007,r*.80,.012,'dark',axis,vertices=56,bevel=.0012)
        U.torus(name+'_Machined_Liner',loc+ax*.014,r*.74,.0021,'silver',axis)
        U.cylinder(name+'_Axle_Recess',loc+ax*.014,r*.50,.004,'rubber',axis,vertices=48,bevel=.0006)
        U.cylinder(name+'_Axle',loc+ax*.0155,r*.28,.003,'dark',axis,vertices=12,bevel=.0003)
        basis=ax.cross(Vector((0,0,1))).normalized()
        if basis.length<.1: basis=Vector((1,0,0))
        other=ax.cross(basis)
        for j in range(4):
            a=pi*.25+j*pi/2; pp=loc+ax*.014+(basis*cos(a)+other*sin(a))*r*.92
            U.bolt(name+'_Recessed_Cap_Screw_%02d'%j,pp,axis,r=.0016)
    def oriented_box(name,a,b,width,depth,mat='armor',bevel=.0015):
        a=Vector(a);b=Vector(b);v=b-a
        o=U.box(name,(a+b)*.5,(width,depth,v.length),mat,bevel=bevel)
        o.rotation_mode='QUATERNION';o.rotation_quaternion=v.to_track_quat('Z','Y')
        return o


    def phalanx_plate(name,a,b,width,depth,mat='silver'):
        a=Vector(a);b=Vector(b);delta=b-a
        o=U.ellipsoid(name,(a+b)*.5,(width*.5,depth*.5,delta.length*.57),mat,seg=32,rings=20)
        o.rotation_mode='QUATERNION';o.rotation_quaternion=delta.to_track_quat('Z','Y')
        return o

    for s,side,suf in [(1,'L','l'),(-1,'R','r')]:
        shoulder=(s*.373,0,1.77);elbow=(s*.425,0,1.35);wrist=(s*.443,-.008,1.01)
        hip=(s*.165,0,1.045);knee=(s*.19,-.006,.585);ankle=(s*.20,0,.145)
        upper='upper_arm_'+suf; fore='forearm_'+suf; hand='hand_'+suf
        thigh='thigh_'+suf; shin='shin_'+suf; foot='foot_'+suf
        U.BONE=upper
        # Humeral armature under continuous casings. Shoulder machinery is substantially buried.
        U.ellipsoid('Humeral_Rotator_'+side,P(s,(.373,0,1.735)),(.060,.060,.060),'dark')
        U.cylinder('Humeral_Load_Shaft_'+side,P(s,(.402,0,1.557)),.034,.32,'silver',axis=(s*.12,0,-1),bevel=.001)
        arm=housing('Upper_Arm_'+side,s,[
            (0,.422,0,1.390,.046,.049),(.16,.419,0,1.425,.056,.058),
            (.35,.410,.004,1.490,.064,.065),(.66,.397,.008,1.585,.071,.069),
            (.86,.383,.007,1.655,.073,.069),(1,.376,.002,1.701,.062,.058)],
            [(0,.025),(.34,.025),(.46,.12),(.60,.29),(.75,.31),(.86,.20),(.94,.025),(1,.025)],phi=-.03,inset=.012,window_range=(.40,.92))
        # Shoulder-side wrap lip covers the top of the humerus rather than exposing a toy ball.
        U.loft('Humerus_Upper_Sleeve_'+side,[(s*.381,.005,1.650,.078,.074),(s*.376,.002,1.686,.080,.075),(s*.374,0,1.715,.067,.062)],'armor',start=.60,end=2*pi-.60,segments=56,steps=5,thickness=.006)
        for j in range(3):
            tt=.45+j*.14
            ps=[arm(tt+.012*sin(pi*k/18),2.25+k/18*.72,.001) for k in range(19)]
            line('Upper_Arm_Rear_Vent_'+side+str(j),ps,.0022,'dark')
        # Distal yoke has two cheeks sheltering the actual elbow hinge.
        for off,tag in [(-.050,'Medial'),(.050,'Lateral')]:
            U.ellipsoid('Elbow_Yoke_'+side+tag,P(s,(.425+off,-.003,1.374)),(.019,.052,.065),'armor')
        U.BONE=fore
        U.ellipsoid('Elbow_Internal_Gimbal_'+side,elbow,(.045,.048,.046),'rubber')
        joint('Elbow_Bearing_'+side,s,P(s,(.478,0,1.35)),.040,(s,0,0))
        # A front socket rim is shielded beneath the end of the humeral shell.
        U.torus('Elbow_Front_Cup_Lip_'+side,P(s,(.425,-.048,1.355)),.031,.0038,'armor',(0,-1,0))
        U.cylinder('Elbow_Front_Cup_'+side,P(s,(.425,-.047,1.355)),.027,.004,'dark',(0,-1,0),vertices=48)
        f=housing('Forearm_'+side,s,[
            (0,.443,-.008,1.050,.035,.034),(.12,.443,-.007,1.081,.043,.041),
            (.30,.442,-.004,1.135,.051,.047),(.56,.438,0,1.215,.064,.056),
            (.76,.431,.001,1.270,.068,.061),(.91,.428,0,1.307,.059,.054),
            (1,.426,0,1.327,.047,.048)],
            [(0,.045),(.12,.14),(.30,.38),(.53,.66),(.72,.67),(.88,.37),(1,.045)],phi=0,inset=.010,
            window_shape=lambda t:(-.80-curve([(0,.025),(.12,.06),(.30,.22),(.54,.29),(.77,.25),(.91,.12),(1,.025)],t),-.80+curve([(0,.025),(.12,.05),(.34,.15),(.61,.22),(.82,.22),(.94,.10),(1,.025)],t)))
        # Standing reference: forward forearm is an overlapping cast-metal gauntlet;
        # the red soft well is on its medial face and only opens fully on wrist rotation.
        def gauntlet_front(t,u):
            tt=lerp(.065,.965,t);a=-.28+.14*sin(pi*t);b=1.33+.12*sin(pi*t)
            return f(tt,lerp(a,b,u),.005+.003*sin(pi*u))
        frame_shell('Forearm_Primary_Front_Casting_'+side,gauntlet_front,52,36,'armor',.006,handedness=s)
        def gauntlet_side(t,u):
            tt=lerp(.23,.88,t);a=1.16+.10*sin(pi*t);b=2.12-.15*sin(pi*t)
            return f(tt,lerp(a,b,u),.003+.002*sin(pi*u))
        frame_shell('Forearm_Lateral_Flared_Overplate_'+side,gauntlet_side,38,20,'armor',.003,handedness=s)
        # Broad anterior rail and a diagonal separation terminate in the wrist cuff.
        for angle,tag in [(.12,'Medial'),(.65,'Lateral')]:
            ps=[f(lerp(.13,.91,k/42),angle+.055*sin(pi*k/42),.010) for k in range(43)]
            line('Gauntlet_Long_Cast_Seam_'+side+tag,ps,.0011,'rubber')
        ps=[f(.52+.065*sin(pi*k/28),-.12+k/28*1.55,.010) for k in range(29)]
        line('Gauntlet_Oblique_Panel_Split_'+side,ps,.0013,'rubber')
        for t in (.34,.79):
            U.bolt('Gauntlet_Front_Countersink_'+side+str(t),f(t,.46,.011),(s*.3,-.9,0),r=.0020)
        def gauntlet_silver(t,u):
            tt=lerp(.10,.92,t);a=.90+.04*sin(pi*t);b=1.06+.04*sin(pi*t)
            return f(tt,lerp(a,b,u),.006)
        frame_shell('Forearm_Silver_Transition_'+side,gauntlet_silver,42,7,'silver',.002,False,handedness=s)
        # Side actuator running through an honest notch at the forearm's dorsal edge.
        for off in (-.020,.020):
            ps=path(s,[(.429+off,.061,1.280),(.437+off,.060,1.197),(.443+off,.033,1.070)])
            line('Forearm_Dorsal_Tendon_'+side+str(off),ps,.0032,'silver')
        for j in range(3):
            ps=[f(.58+j*.07,1.8+k/20*.76,.001) for k in range(21)]
            line('Forearm_Service_Louvre_'+side+str(j),ps,.0018,'dark')
        for t,ang,tag in [(.74,1.10,'Upper'),(.23,1.22,'Lower')]:
            pos=f(t,ang,.0015); U.bolt('Forearm_Service_Bolt_'+side+tag,pos,(s*.8,-.5,0),r=.0023)
        # Layered cuff surrounds wrist; no oversized exposed universal joint.
        U.loft('Wrist_Cast_Cuff_'+side,[(s*.443,-.008,1.028,.038,.035),(s*.443,-.008,1.046,.039,.036),(s*.443,-.008,1.063,.036,.034)],'armor',segments=48,steps=4,thickness=.004)
        U.cylinder('Wrist_Bearing_'+side,wrist,.030,.030,'dark',(0,0,1),vertices=48,bevel=.001)
        U.torus('Wrist_Machined_Collar_'+side,P(s,(.443,-.008,1.022)),.0305,.0022,'silver',(0,0,1))
        for j in range(7):
            U.torus('Wrist_Flexible_Seal_'+side+str(j),P(s,(.443,-.008,1.000+j*.0035)),.028,.00095,'rubber',(0,0,1))
        # Full palm volume, projected carpal flanges, four fingers and truly opposed thumb.
        U.BONE=hand
        U.loft('Palm_Structure_'+side,[(s*.443,-.008,.905,.042,.021),(s*.443,-.010,.925,.055,.029),(s*.443,-.009,.963,.057,.032),(s*.443,-.008,.992,.043,.026),(s*.443,-.008,1.007,.028,.024)],'dark',segments=56,steps=5,thickness=.006)
        outline=[(.390,.944),(.393,.972),(.410,.991),(.438,.998),(.474,.984),(.493,.958),(.492,.923),(.474,.911),(.414,.912),(.394,.926)]
        U.patch('Hand_Dorsal_Casting_'+side,[(s*x,z) for x,z in outline],lambda x,z: -.052+4.0*(abs(x)-.444)**2+4.0*(z-.953)**2,'silver',thickness=.005,bevel=.0015,smooth=2)
        # Primary seated reference: petrol dorsal plate with a restrained metal
        # border. The workshop lights make other frames read fully silver.
        inner_outline=[(.444+(x-.444)*.89,.953+(z-.953)*.87) for x,z in outline]
        U.patch('Hand_Petrol_Dorsal_Inset_'+side,[(s*x,z) for x,z in inner_outline],lambda x,z: -.054+4.0*(abs(x)-.444)**2+4.0*(z-.953)**2,'armor',thickness=.0025,bevel=.0010,smooth=2)
        # Inset metacarpal tracks are not stuck-on long rods.
        for j in range(4):
            x=.405+j*.025
            ps=path(s,[(x,-.053,.960),(x+.001,-.052,.942),(x+.002,-.048,.920)])
            line('Metacarpal_Recess_'+side+str(j),ps,.00125,'dark')
            for z in (.938,.960):
                U.bolt('Metacarpal_Fastener_'+side+str(j)+str(z),P(s,(x,-.054+4.0*(x-.444)**2+4.0*(z-.953)**2,z)),(0,-1,0),r=.00125)
        # Finger rigid links have curved petrol dorsal plates, compliant pads and metal hinge pins.
        for finger in range(4):
            x=.402+finger*.027; length=[.112,.124,.118,.099][finger]
            curl=[.045,.058,.065,.073][finger]
            pts=[P(s,(x,-.010,.901)),P(s,(x+.001,-.025,.901-length*.39)),P(s,(x+.004,-.025-curl*.55,.901-length*.65)),P(s,(x+.005,-.025-curl,.901-length*.73))]
            U.BONE=hand
            U.ellipsoid('Hand_Metacarpal_Knuckle_'+side+str(finger),P(s,(x,-.025,.910)),(.014,.017,.015),'dark',seg=28,rings=18)
            parent=hand
            for seg in range(3):
                bone=f'finger_{finger+1}_{seg+1}_{suf}'; U.BONES[bone]=(pts[seg],pts[seg+1],parent);parent=bone;U.BONE=bone
                a,b=Vector(pts[seg]),Vector(pts[seg+1]);rad=.0125 if finger<3 else .0115
                U.cylinder(f'Finger_{side}_{finger}_{seg}_Hinge',a,rad,rad*2.0,'dark',(s,0,0),vertices=32,bevel=.0007)
                U.cylinder(f'Finger_{side}_{finger}_{seg}_Recess_Pin',a+Vector((s*rad,0,0)),rad*.44,.0015,'silver',(s,0,0),vertices=20,bevel=.0002)
                oriented_box(f'Finger_{side}_{finger}_{seg}_Chassis',a.lerp(b,.10),a.lerp(b,.94),rad*1.70,rad*1.65,'dark',.0043)
                aa=a.lerp(b,.17)+Vector((0,-.006,0));bb=a.lerp(b,.89)+Vector((0,-.006,0))
                phalanx_plate(f'Finger_{side}_{finger}_{seg}_Dorsal_Plate',aa,bb,rad*1.80,.013,'armor')
                aa=a.lerp(b,.20)+Vector((0,.007,0));bb=a.lerp(b,.89)+Vector((0,.007,0))
                oriented_box(f'Finger_{side}_{finger}_{seg}_Grip_Pad',aa,bb,rad*1.42,.008,'rubber',.0028)
                for cut in (.37,.65):
                    mid=a.lerp(b,cut)+Vector((0,.011,0))
                    U.box(f'Finger_{side}_{finger}_{seg}_Grip_Groove_{cut}',mid,(rad*1.35,.001,.0014),'dark',bevel=.0002)
        pts=path(s,[(.390,-.004,.968),(.369,-.010,.950),(.358,-.029,.924),(.368,-.050,.907)])
        parent=hand
        for seg in range(3):
            bone=f'thumb_{seg+1}_{suf}';U.BONES[bone]=(pts[seg],pts[seg+1],parent);parent=bone;U.BONE=bone
            a,b=Vector(pts[seg]),Vector(pts[seg+1]);rad=.015
            U.ellipsoid(f'Thumb_{side}_{seg}_Ball',a,(rad,rad,rad),'dark',seg=32,rings=20)
            oriented_box(f'Thumb_{side}_{seg}_Casting',a.lerp(b,.12),a.lerp(b,.91),.025,.025,'armor',.004)
            U.cylinder(f'Thumb_{side}_{seg}_Pin',a+Vector((s*.014,0,0)),.006,.002,'silver',(s,0,0),vertices=24,bevel=.0003)
            oriented_box(f'Thumb_{side}_{seg}_Pad',a.lerp(b,.22)+Vector((0,.012,0)),a.lerp(b,.88)+Vector((0,.012,0)),.019,.006,'rubber',.0015)

        # LOWER LIMBS: broad cast envelopes, deliberate taper, integrated joints.
        U.BONE=thigh
        U.ellipsoid('Hip_Bearing_Core_'+side,hip,(.083,.080,.080),'dark')
        joint('Hip_Outer_Socket_'+side,s,P(s,(.236,.002,1.045)),.063,(s,0,0))
        U.cylinder('Femoral_Internal_Spar_'+side,P(s,(.178,.002,.825)),.040,.350,'dark',(s*.07,0,-1),vertices=48,bevel=.0015)
        th=housing('Thigh_'+side,s,[
            (0,.188,-.003,.635,.073,.074),(.13,.187,-.001,.682,.089,.086),
            (.36,.180,.003,.775,.111,.093),(.66,.172,.007,.890,.116,.098),
            (.86,.166,.006,.962,.112,.095),(1,.165,.004,1.004,.094,.084)],
            [(0,.06),(.13,.12),(.32,.42),(.55,.53),(.75,.46),(.90,.28),(1,.06)],phi=-.82,inset=.012,
            window_shape=lambda t:(-.82-curve([(0,.04),(.15,.12),(.35,.36),(.61,.51),(.82,.41),(1,.04)],t),-.82+curve([(0,.04),(.15,.13),(.40,.50),(.68,.38),(.85,.17),(1,.04)],t)))
        # Continuous outer thigh plate wraps around the lateral bulk. Broad flat casting and tight seam.
        def thigh_outer(t,u):
            tt=lerp(.11,.94,t);a=-.08+.14*sin(pi*t);b=1.82-.10*sin(pi*t)
            return th(tt,lerp(a,b,u),.006+.002*sin(pi*u))
        frame_shell('Thigh_Outer_Overlapping_Casting_'+side,thigh_outer,54,36,'armor',.006,handedness=s)
        # Narrow tapered lateral service channel sunk between two long plate lips.
        def thigh_channel(t,u):
            tt=lerp(.20,.88,t);a=.57+.025*sin(pi*t);b=a+.12
            return th(tt,lerp(a,b,u),.0066)
        frame_shell('Thigh_Lateral_Service_Recess_'+side,thigh_channel,38,5,'dark',.002,False,handedness=s)
        for edge in (.55,.72):
            ps=[th(lerp(.20,.88,k/40),edge,.009) for k in range(41)]
            line('Thigh_Service_Channel_Edge_'+side+str(edge),ps,.0012,'armor')
        for t in (.36,.69):
            ps=[th(t+.025*cos(pi*k/24),-.05+k/24*.61,.0085) for k in range(25)]
            line('Thigh_Overplate_Diagonal_Join_'+side+str(t),ps,.0014,'rubber')
        # Long outer cast rib is part of the housing, with a recessed inset access strip.
        for j,ang in enumerate((.82,1.12)):
            ps=[th(lerp(.12,.90,k/45),ang,.0020) for k in range(46)]
            line('Femoral_Shell_Longitudinal_Recess_'+side+str(j),ps,.0016,'rubber')
        for j in range(4):
            t=.22+j*.16
            ps=[th(t+.020*sin(pi*k/22),.82+k/22*.40,.0022) for k in range(23)]
            line('Thigh_Outer_Access_Join_'+side+str(j),ps,.0011,'dark')
        for t in (.25,.76):
            pos=th(t,.99,.002);U.bolt('Thigh_Recessed_Fastener_'+side+str(t),pos,(s*.85,-.4,0),r=.0022)
        # Distal armor wraps the sides of knee and leaves flexion clearance at the rear.
        # On-model knee transition: smooth thigh cup over a domed knee, no exposed
        # horseshoe frame. The thigh remains separate for FK bending clearance.
        U.loft('Femur_Distal_Knee_Cup_'+side,[(s*.189,-.002,.612,.074,.066),(s*.188,0,.641,.085,.076),(s*.186,.001,.674,.091,.082)],'armor',start=-1.65,end=1.65,segments=60,steps=5,thickness=.006)
        U.BONE=shin
        U.ellipsoid('Knee_Hinge_Core_'+side,knee,(.058,.062,.058),'rubber')
        joint('Knee_Outer_Cup_'+side,s,P(s,(.248,-.006,.585)),.049,(s,0,0))
        joint('Knee_Inner_Cup_'+side,s,P(s,(.132,-.006,.585)),.038,(-s,0,0))
        # Broad domed petrol knee cover seen in the seated on-model frame.
        U.ellipsoid('Knee_Domed_Armor_Cap_'+side,P(s,(.190,-.052,.602)),(.075,.052,.086),'armor',seg=64,rings=40)
        for angle,tag in [(-1,'Medial'),(1,'Lateral')]:
            ps=[]
            for j in range(23):
                a=.12+j/22*2.54
                ps.append(P(s,(.190+angle*.071*sin(a),-.059-.027*sin(a),.602+.080*cos(a))))
            line('Knee_Cap_Subtle_Inlay_'+side+tag,ps,.0011,'silver')
        sh=housing('Shin_'+side,s,[
            (0,.200,.001,.152,.048,.047),(.14,.200,.004,.214,.057,.057),
            (.34,.198,.012,.310,.075,.076),(.60,.196,.016,.417,.090,.087),
            (.81,.192,.006,.492,.089,.080),(.94,.191,0,.538,.078,.068),
            (1,.190,-.001,.552,.065,.061)],
            [(0,.045),(.14,.13),(.33,.32),(.56,.51),(.76,.55),(.91,.29),(1,.045)],phi=-.035,inset=.004,inset_mat='armor',
            window_shape=lambda t:(curve([(0,-.03),(.18,-.20),(.36,-.37),(.64,-.57),(.82,-.43),(1,-.04)],t),curve([(0,.04),(.22,.12),(.48,.35),(.68,.51),(.86,.37),(1,.04)],t)))
        # Authoritative on-model design: a long dark central blade flanked by
        # broad convex crimson side panels. Panel geometry is a smooth inset
        # within slightly raised petrol lips, not added as painted diamonds.
        def shin_blade(t,u):
            tt=lerp(.015,.97,t);width=.29+.10*(1-t)
            return sh(tt,lerp(-width,width,u),.006+.003*sin(pi*u))
        frame_shell('Shin_Long_Central_Blade_'+side,shin_blade,60,24,'armor',.005,handedness=s)
        for panel_side,tag in [(-1,'Medial'),(1,'Lateral')]:
            def red_side(t,u,panel_side=panel_side):
                tt=lerp(.37,.925,t);width=.035+.50*sin(pi*t)**.72
                angle=panel_side*(.86+lerp(-width,width,u))
                return sh(tt,angle,.0035)
            frame_shell('Shin_Broad_Crimson_Side_Panel_'+side+tag,red_side,46,28,'red',.003,False,handedness=s*panel_side)
            for edge,edge_tag in [(-1,'Front'),(1,'Back')]:
                def lip(t,u,panel_side=panel_side,edge=edge):
                    tt=lerp(.37,.925,t);width=.035+.50*sin(pi*t)**.72
                    angle=panel_side*(.86+edge*(width+lerp(.005,.055,u)))
                    return sh(tt,angle,.007)
                frame_shell('Shin_Red_Well_Lip_'+side+tag+edge_tag,lip,44,5,'armor',.003,handedness=s*panel_side*edge)
                ps=[]
                for j in range(39):
                    t=j/38;tt=lerp(.37,.925,t);width=.035+.50*sin(pi*t)**.72
                    ps.append(sh(tt,panel_side*(.86+edge*(width+.012)),.008))
                line('Shin_Red_Well_Join_'+side+tag+edge_tag,ps,.0010,'dark')
            # Narrow continuation of crimson down the lower leg, visible beside
            # the central blade and disappearing into the armored boot collar.
            def lower_stripe(t,u,panel_side=panel_side):
                tt=lerp(.01,.43,t);angle=panel_side*(.70+lerp(-.045,.045,u))
                return sh(tt,angle,.0025)
            frame_shell('Shin_Lower_Crimson_Inlay_'+side+tag,lower_stripe,30,5,'red',.002,False,handedness=s*panel_side)
        for sign in (-1,1):
            ps=[sh(lerp(.06,.94,k/44),sign*(.31+.07*(1-k/44)),.010) for k in range(45)]
            line('Shin_Blade_Edge_'+side+str(sign),ps,.00085,'silver')
        # Rear calf access recess and longitudinal split with fasteners on cast landings.
        for j in range(4):
            t=.35+j*.105
            ps=[sh(t,pi-.38+k/26*.76,.0010) for k in range(27)]
            line('Calf_Rear_Flex_Louvre_'+side+str(j),ps,.0022,'dark')
        for t in (.25,.73):
            U.bolt('Shin_Lateral_Cap_Screw_'+side+str(t),sh(t,1.16,.0015),(s*.85,-.25,0),r=.0022)
        # Achilles telescoping unit is sheltered in a rear casting, mechanically plausible.
        line('Achilles_Piston_Rod_'+side,path(s,[(.200,.056,.171),(.199,.082,.261),(.196,.087,.344)]),.008,'silver')
        line('Achilles_Piston_Body_'+side,path(s,[(.199,.083,.250),(.196,.089,.350)]),.014,'dark')
        for j in range(9):
            z=.181+j*.0063;U.torus('Achilles_Gaiter_'+side+str(j),P(s,(.200,.061+(z-.181)*.24,z)),.012,.0018,'rubber')
        U.loft('Ankle_Cast_Collar_'+side,[(s*.20,.002,.154,.051,.049),(s*.20,.003,.181,.055,.052),(s*.20,.004,.206,.052,.051)],'armor',start=.65,end=2*pi-.65,segments=48,steps=4,thickness=.006)
        U.BONE=foot
        U.ellipsoid('Ankle_Rocker_Core_'+side,ankle,(.045,.047,.045),'dark')
        joint('Ankle_Outer_Recess_'+side,s,P(s,(.247,0,.145)),.034,(s,0,0))
        # Closed load-bearing foot enclosure with broad instep and real sole. No floating sandal pieces.
        U.loft('Foot_Closed_Casting_'+side,[
            (s*.20,-.058,.027,.073,.143),(s*.20,-.058,.047,.080,.146),
            (s*.20,-.051,.078,.080,.139),(s*.20,-.036,.113,.071,.109),
            (s*.20,-.010,.151,.055,.071),(s*.20,.000,.184,.047,.050)],'armor',segments=72,steps=5,thickness=.006)
        U.loft('Foot_Tread_Sole_'+side,[(s*.20,-.058,.014,.070,.139),(s*.20,-.058,.021,.076,.145),(s*.20,-.058,.034,.076,.145)],'rubber',segments=64,steps=4,thickness=.005)
        # The on-model feet are continuous armored boots, with no separated toes.
        # A subtle transverse break separates the toe box from the instep shell.
        line('Boot_Toe_Box_Panel_Break_'+side,path(s,[(.133,-.151,.067),(.163,-.165,.083),(.20,-.170,.086),(.237,-.165,.083),(.267,-.151,.067)]),.0011,'dark')
        # Front shell seams: three interlocking panels around instep/ankle relief.
        for j,off in enumerate((-.038,.038)):
            ps=path(s,[(.20+off*.55,-.015,.166),(.20+off*.8,-.059,.132),(.20+off,-.112,.103),(.20+off,-.153,.079)])
            line('Foot_Instep_Panel_Seam_'+side+str(j),ps,.0012,'rubber')
        for k in range(5):
            y=-.13+k*.044
            U.box('Sole_Tread_Block_'+side+str(k),P(s,(.20,y,.012)),(.125,.018,.006),'rubber',bevel=.001)
        for off in (-.057,.057):
            U.bolt('Foot_Sole_Fastener_'+side+str(off),P(s,(.20+off,.020,.062)),(s*(1 if off>0 else -1),0,0),r=.0018)
    U.BONE='chest'
