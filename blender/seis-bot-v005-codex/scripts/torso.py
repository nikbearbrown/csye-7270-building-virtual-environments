"""Reference-led thorax: broad cast frames, recessed segmented enamel, rib cage.
The primary shape reference is the supplied on-model workshop video, frames 000360 and 000240.
"""
from math import sin,cos,pi,sqrt,exp
from mathutils import Vector

def build_torso(U):
    U.BONE='chest'
    def mirrored(poly,s):return [(s*x,z) for x,z in poly]
    def surf(x,z):return -.188+.67*x*x-.025*exp(-((z-1.68)/.115)**2)
    def framed(name, outline, surface, mat='edge', inner=.84, width=.005):
        bd=U.smooth_path(outline,6,True);c=sum(bd,Vector((0,0)))/len(bd);n=len(bd)
        verts=[];faces=[];wear=[]
        # Broad metal surface, an edge radius, then an actual return into the well.
        for r,off,w in [(1,.004,.45),(.985,0,.95),(.96,-width,.5),((1+inner)/2,-width,0),(inner+.016,-width,.35),(inner,0,.8),(inner,.010,.15)]:
            for b in bd:
                x,z=c.lerp(b,r);verts.append((x,surface(x,z)+off,z));wear.append(w)
        for j in range(6):
            for i in range(n):
                a=j*n+i;b=j*n+(i+1)%n;faces.append((a,b,b+n,a+n))
        o=U.mesh(name,verts,faces,mat,wear)
        m=o.modifiers.new('Cast_Metal_Thickness','SOLIDIFY');m.thickness=.006
        return [(p.x,p.y) for p in [c.lerp(b,inner-.018) for b in bd]]
    def clipz(poly,low,high):
        out=poly
        for cut,keepup in ((low,True),(high,False)):
            new=[]
            for i,b in enumerate(out):
                a=out[i-1];ina=a[1]>=cut if keepup else a[1]<=cut;inb=b[1]>=cut if keepup else b[1]<=cut
                if ina!=inb:
                    t=(cut-a[1])/(b[1]-a[1]);new.append((a[0]+t*(b[0]-a[0]),cut))
                if inb:new.append(b)
            out=new
        return out
    # Load-bearing core is concealed by the casings, not an exposed rubber oval.
    U.loft('Thorax_Inner_Chassis',[(0,.018,1.40,.122,.095),(0,.014,1.50,.19,.118),(0,.01,1.66,.29,.135),(0,.008,1.77,.26,.116)],'dark')
    U.loft('Thoracic_Upper_Closure',[(0,.012,1.762,.270,.124),(0,.015,1.788,.222,.110),(0,.015,1.811,.150,.090),(0,.014,1.827,.083,.070)],'armor',start=-pi/2,end=pi/2,segments=64,steps=5,thickness=.009)
    def upper_surf(x,z):
        rows=[(1.762,.270,.124),(1.788,.222,.110),(1.811,.150,.090),(1.827,.083,.070)]
        for (a,ra,da),(b,rb,db) in zip(rows,rows[1:]):
            if a<=z<=b:
                t=(z-a)/(b-a);r=ra+(rb-ra)*t;d=da+(db-da)*t
                return .014-d*sqrt(max(.04,1-(x/r)**2))-.003
        return -.10
    for s,side in ((-1,'R'),(1,'L')):
        pp=mirrored([(.075,1.787),(.083,1.803),(.104,1.802),(.151,1.786),(.140,1.779),(.080,1.780)],s)
        U.patch('Recessed_Trapezius_Field_'+side,pp,lambda x,z:upper_surf(x,z)-.002,'red',.003,.0005,3)
        for j in range(3):
            x=.094+j*.014
            z=1.797-j*.004
            pts=[(s*x,upper_surf(x,z)-.003, z),(s*(x+.010),upper_surf(x+.010,z-.011)-.003,z-.011)]
            U.line('Trapezius_Flexion_Seam_'+side+str(j),pts,.0011,'dark')
    U.loft('Abdomen_Core',[(0,.008,1.13,.132,.092),(0,.012,1.25,.139,.10),(0,.015,1.40,.137,.105)],'rubber')
    # Petrol pectoral plates flank a narrow centered six and metallic sternum.
    chestpoly=[(.025,1.772),(.078,1.793),(.194,1.795),(.304,1.795),(.345,1.765),(.329,1.725),(.251,1.69),(.190,1.64),(.144,1.574),(.105,1.477),(.074,1.414),(.034,1.412),(.031,1.56)]
    for s,side in ((-1,'R'),(1,'L')):
        outline=mirrored(chestpoly,s)
        # Actual recessed stepped well and upper enamel plate.
        U.patch('Pectoral_Deep_Gasket_'+side,outline,lambda x,z:surf(x,z)+.012,'rubber',.010,.001,4)
        inner=framed('Pectoral_Cast_Surround_'+side,outline,surf,inner=.86,width=.006)
        for j,(lo,hi) in enumerate([(1.55,1.83),(1.504,1.547),(1.461,1.501),(1.41,1.458)]):
            poly=clipz(inner,lo,hi)
            if len(poly)>2:U.patch('Recessed_Enamel_Pectoral_'+side+str(j),poly,lambda x,z:surf(x,z)+.004,'armor',.006,.001,0)
        # Horizontal articulated plating across clavicles, swept along front curve.
        for j in range(5):
            x0=.202+j*.022
            curve=[(s*x0,surf(x0,1.790)+.002,1.790),(s*(x0+.012),surf(x0+.012,1.771)+.002,1.771),(s*(x0+.025),surf(x0+.025,1.746)+.002,1.746)]
            U.line('Clavicle_Articulation_Seam_'+side+str(j),curve,.0012,'dark')
        # Sculpted crimson understructure is visible through each costal opening.
        U.loft('Costal_Red_Understructure_'+side,[(s*.220,.004,1.455,.025,.051),(s*.250,.004,1.525,.036,.058),(s*.272,.004,1.615,.036,.062),(s*.285,.004,1.695,.024,.052)],'red',segments=48,steps=8)
        # Three broad costal laminae wrap around the side of the chest. Their
        # normals follow the body circumference, avoiding twisted tubular ribs.
        for j in range(3):
            path=[(s*(.075+j*.006),-.177,1.645-j*.040),
                  (s*(.128+j*.012),-.167,1.553-j*.037),
                  (s*(.216+j*.015),-.123,1.493-j*.034),
                  (s*(.285+j*.010),-.038,1.521-j*.030),
                  (s*(.296+j*.007),.060,1.598-j*.025),
                  (s*(.264+j*.006),.136,1.695-j*.022)]
            centers=U.smooth_path(path,16);vs=[];fs=[];n=len(centers);cols=9
            for layer in [0,1]:
                for k,c in enumerate(centers):
                    tangent=(centers[min(k+1,n-1)]-centers[max(k-1,0)]).normalized()
                    outward=Vector((c.x*1.15,c.y*2.4,0)).normalized()
                    across=tangent.cross(outward).normalized()
                    normal=across.cross(tangent).normalized()
                    if normal.dot(outward)<0:normal=-normal
                    taper=.72+.28*sin(pi*k/(n-1))
                    for i in range(cols):
                        u=-1+2*i/(cols-1)
                        v=c+across*(u*.024*taper)+normal*(.004*(1-u*u)-layer*.009)
                        vs.append(tuple(v))
            layer_size=n*cols
            for layer in [0,1]:
                for k in range(n-1):
                    for i in range(cols-1):
                        a=layer*layer_size+k*cols+i
                        f=(a,a+1,a+cols+1,a+cols);fs.append(f if layer==0 else tuple(reversed(f)))
            for k in range(n-1):
                for i in [0,cols-1]:
                    a=k*cols+i;b=(k+1)*cols+i;fs.append((a,b,b+layer_size,a+layer_size))
            for k in [0,n-1]:
                for i in range(cols-1):
                    a=k*cols+i;fs.append((a,a+layer_size,a+1+layer_size,a+1))
            ob=U.mesh('Thoracic_Rib_Cast_'+side+str(j),vs,fs,'armor')
            bevel=ob.modifiers.new('Rounded_Costal_Edges','BEVEL');bevel.width=.0015;bevel.segments=3;bevel.limit_method='ANGLE';bevel.angle_limit=.4
            # Real metal edge is a narrow fitted fillet on the lamina itself.
            edge=[vs[k*cols] for k in range(n)]
            U.line('Thoracic_Rib_Edge_'+side+str(j),edge,.0010,'edge')
        # Short oblique structural rails with seam breaks, not long external red tubes.
        rail=[(.126,1.47),(.174,1.48),(.159,1.37),(.151,1.27),(.147,1.16),(.100,1.15),(.107,1.29)]
        for j,(lo,hi) in enumerate([(1.35,1.50),(1.25,1.347),(1.15,1.247)]):
            poly=clipz(mirrored(rail,s),lo,hi)
            U.patch('Oblique_Cast_Rail_'+side+str(j),poly,lambda x,z:-.113+.30*x*x,'armor',.018,.0015,2)
        # Red flexor blocks reside behind the metal ribs and segmented center spine.
        for j in range(4):
            z=1.18+j*.057
            U.box('Inset_Abdominal_Flexor_'+side+str(j),(s*.064,-.094,z),(.041,.037,.051),'red',.007)
            U.box('Flexor_Side_Stop_'+side+str(j),(s*.087,-.093,z),(.007,.025,.047),'dark',.002)
        # Deep lateral channel exposes guarded linkages at flank.
        for k in range(2):
            U.line('Flank_Recessed_Pipe_'+side+str(k),[(s*(.142+k*.016),.035,1.16),(s*(.15+k*.017),.053,1.30),(s*(.185+k*.02),.07,1.48)],.0045,'bronze' if k else 'rubber')
        U.sweep('Waist_Outer_Pilaster_'+side,[(s*.175,.044,1.14,.6),(s*.184,.057,1.29,.85),(s*.202,.060,1.45,1),(s*.236,.048,1.51,.5)],.022,.024,'armor',normal=(s,0,0),power=5)
        U.bolt('Pectoral_Latch_'+side,(s*.312,surf(.312,1.75)-.008,1.75),r=.0035)
        # Visible engineering inside the protected rib cavities: telescoping
        # thrust rods and their end eyes, with a short nested weather seal.
        a=Vector((s*.291,-.022,1.665));b=Vector((s*.223,.010,1.481));axis=(b-a).normalized()
        U.cylinder('Costal_Actuator_Sleeve_'+side,a.lerp(b,.22),.018,(b-a).length*.46,'dark',tuple(axis),vertices=48)
        U.cylinder('Costal_Actuator_Piston_'+side,a.lerp(b,.66),.008,(b-a).length*.55,'silver',tuple(axis),vertices=40)
        for k in range(6):U.torus('Costal_Actuator_Seal_'+side+str(k),a.lerp(b,.41)+axis*(k*.003),.011,.0018,'rubber',tuple(axis))
        for j,p in enumerate((a,b)):
            U.cylinder('Costal_Clevis_'+side+str(j),p,.018,.026,'armor',(s,0,0),vertices=40)
            U.cylinder('Costal_Clevis_Pin_'+side+str(j),p+Vector((s*.014,0,0)),.007,.003,'silver',(s,0,0),vertices=24)
    # Center casting includes a Y-shaped collar and fitted sternum segments.
    # Explicit connected quad rows avoid the concave fan pinching of v004.
    yy=[];ff=[];wear=[]
    for row in [list(zip([-.085,-.050,-.025,0,.025,.050,.085],[1.787,1.792,1.790,1.786,1.790,1.792,1.787])),
                list(zip([-.055,-.035,-.018,0,.018,.035,.055],[1.779]*7)),
                list(zip([-.032,-.023,-.012,0,.012,.023,.032],[1.746]*7))]:
        for i,(x,z) in enumerate(row):yy.append((x,surf(x,z)-.004,z));wear.append(.7 if i in (0,6) else .08)
    for j in range(2):
        for i in range(6):a=j*7+i;ff.append((a,a+1,a+8,a+7))
    ob=U.mesh('Central_Clavicular_Yoke',yy,ff,'silver',wear)
    m=ob.modifiers.new('Cast_Wall','SOLIDIFY');m.thickness=.011
    m=ob.modifiers.new('Cast_Fillet','BEVEL');m.width=.0015;m.segments=3;m.limit_method='ANGLE'
    for j,(z,w,h) in enumerate([(1.735,.030,.020),(1.573,.030,.049),(1.517,.027,.048),(1.465,.023,.044),(1.422,.024,.029)]):
        U.patch('Sternal_Casting_'+str(j),[(-w,z+h/2),(w,z+h/2),(w*.87,z-h/2),(-w*.87,z-h/2)],lambda x,z:surf(x,z)-.007,'edge',.009,.0012,2)
        U.patch('Sternal_Enamel_Inlay_'+str(j),[(-w*.74,z+h*.34),(w*.74,z+h*.34),(w*.64,z-h*.34),(-w*.64,z-h*.34)],lambda x,z:surf(x,z)-.010,'armor',.002,.0007,2)
    for j,(z,w,h) in enumerate([(1.363,.048,.078),(1.292,.046,.057),(1.229,.041,.056),(1.172,.035,.044)]):
        U.patch('Abdominal_Vertebra_Plate_'+str(j),[(-w,z+h/2),(w,z+h/2),(w*.84,z-h/2),(-w*.84,z-h/2)],lambda x,z:-.125+.3*x*x+.11*(z-1.32)**2,'edge',.010,.0015,2)
        U.patch('Abdominal_Vertebra_Inlay_'+str(j),[(-w*.72,z+h*.34),(w*.72,z+h*.34),(w*.62,z-h*.34),(-w*.62,z-h*.34)],lambda x,z:-.128+.3*x*x+.11*(z-1.32)**2,'armor',.002,.0008,2)
    # The authoritative front frame carries the six on the narrow midline badge.
    badge=[(-.032,1.719),(.032,1.719),(.034,1.696),(.032,1.609),(.022,1.598),(-.022,1.598),(-.032,1.609),(-.034,1.696)]
    U.patch('Sternal_Badge_Silver_Rim',badge,lambda x,z:surf(x,z)-.008,'silver',.006,.0012,4)
    U.patch('Sternal_Badge_Dark_Inset',[(x*.87,1.660+(z-1.660)*.94) for x,z in badge],lambda x,z:surf(x,z)-.010,'dark',.003,.0008,4)
    for side in [-1,1]:
        U.patch('Sternal_Badge_Red_Recess_'+str(side),[(side*.037,1.705),(side*.049,1.701),(side*.048,1.624),(side*.037,1.619)],lambda x,z:surf(x,z)+.001,'red',.004,.001,3)
    number=U.text_mesh('Chest_Six_Lato','6',(0,surf(0,1.664)-.013,1.664),.116,'white')
    number['badge_anchor']=[0,1.664]

    # Pelvic shell is integrated with thigh ball sockets and sculpted iliac crests.
    U.BONE='pelvis'
    U.loft('Pelvic_Central_Casing',[(0,0,.987,.11,.090),(0,.012,1.051,.183,.110),(0,.010,1.127,.175,.105)],'dark')
    for s,side in ((-1,'R'),(1,'L')):
        U.sweep('Iliac_Upper_Cast_'+side,[(s*.028,-.104,1.102,.9),(s*.098,-.107,1.151,1),(s*.187,-.025,1.188,1.2),(s*.216,.060,1.145,.9),(s*.144,.126,1.082,.5)],.030,.018,'edge',normal=(0,0,1),steps=12,power=5,profile=24)
        U.sweep('Iliac_Lower_Return_'+side,[(s*.058,-.092,1.036,.6),(s*.108,-.106,1.096,1),(s*.198,-.022,1.136,1),(s*.211,.06,1.10,.7)],.022,.014,'armor',normal=(0,0,1),steps=12,power=5)
        U.patch('Hip_Socket_Front_Rim_'+side,mirrored([(.055,1.091),(.102,1.112),(.179,1.068),(.18,1.019),(.142,1.032),(.103,1.043),(.066,.985)],s),lambda x,z:-.112+.4*x*x,'armor',.011,.002,3)
        # Deep recessed locking flange, mostly sheltered by the iliac casing.
        U.cylinder('Pelvis_Socket_Inner_'+side,(s*.157,-.058,1.053),.064,.017,'rubber',(0,-1,0))
        U.torus('Pelvis_Socket_Return_'+side,(s*.157,-.070,1.053),.054,.005,'dark',(0,-1,0))
        for k in range(5):
            a=pi*.2+k/4*pi*.9
            U.bolt('Hip_Lock_'+side+str(k),(s*.157+.044*cos(a),-.076,1.053+.044*sin(a)),r=.0028)
    U.patch('Pelvic_Keystone',[(-.073,1.13),(0,1.104),(.073,1.13),(.051,1.045),(.025,.946),(-.025,.946),(-.051,1.045)],lambda x,z:-.130+.9*x*x+.35*(z-1.08)**2,'armor',.017,.002,3)
    U.patch('Pelvic_Center_Inlay',[(-.035,1.11),(0,1.09),(.035,1.11),(.024,1.055),(.012,.974),(-.012,.974),(-.024,1.055)],lambda x,z:-.131+.9*x*x+.35*(z-1.08)**2,'dark',.005,.001,2)

