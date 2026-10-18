"""SEIS v005 shoulders/back: enclosing on-model pauldrons and posterior armor wells.
Shoulders revised to the authoritative supplied video frames 000360/000240/000480. Front is -Y.
"""
from math import sin, cos, pi, exp, sqrt


def build_shoulders_back(U):
    oldbone = getattr(U, 'BONE', 'chest')
    U.BONE = 'chest'

    def p3(points, s):
        return [(s*x,y,z) for x,y,z in points]

    def cast_edges(ob):
        # Small genuine machined radii on closed castings, not on decorative curves.
        dims=[abs(float(d)) for d in ob.dimensions if abs(float(d))>1e-6]
        width=min(.0012,min(dims)*.1) if dims else .0012
        be=ob.modifiers.new('Cast_Machined_Edge_Radius','BEVEL')
        be.width=width; be.segments=3; be.limit_method='ANGLE'; be.angle_limit=.60
        be.use_clamp_overlap=True
        return ob

    def closed_curve(points, subdivisions=8):
        out=[]; count=len(points)
        for i in range(count):
            a,b,c,d=points[(i-1)%count],points[i],points[(i+1)%count],points[(i+2)%count]
            for j in range(subdivisions):
                t=j/subdivisions
                out.append(tuple(.5*((2*b[k])+(-a[k]+c[k])*t+(2*a[k]-5*b[k]+4*c[k]-d[k])*t*t+(-a[k]+3*b[k]-3*c[k]+d[k])*t*t*t) for k in range(2)))
        return out

    def ring_frame(name, outer, inner, surface, s, material='armor', depth=.010, bone='chest'):
        """A cast annulus with an actual open cavity and thick beveled perimeter."""
        # Both contours have matching landmarks; closed strips remain manifold.
        oo=closed_curve(outer); ii=closed_curve(inner); n=len(oo)
        nr=8; verts=[]; wear=[]
        for back in (False,True):
            for k in range(nr+1):
                t=k/nr
                for j in range(n):
                    x=oo[j][0]*(1-t)+ii[j][0]*t
                    z=oo[j][1]*(1-t)+ii[j][1]*t
                    y=surface(x,z)+(.0038*sin(pi*t) if not back else -depth)
                    verts.append((s*x,y,z))
                    wear.append(.70*exp(-min(t,1-t)*20) if not back else .1)
        faces=[]; layer=(nr+1)*n
        for side in range(2):
            off=side*layer
            for k in range(nr):
                for j in range(n):
                    a=off+k*n+j;b=off+k*n+(j+1)%n;c=off+(k+1)*n+(j+1)%n;d=off+(k+1)*n+j
                    faces.append((a,b,c,d) if side==0 else (d,c,b,a))
        for k in (0,nr):
            for j in range(n):
                a=k*n+j;b=k*n+(j+1)%n
                faces.append((a,a+layer,b+layer,b) if k==0 else (b,b+layer,a+layer,a))
        ob=cast_edges(U.mesh(name,verts,faces,material,wear,bone=bone))
        # Visible lip is a substantial casting; the fine inset bead catches light.
        pts=[(s*x,surface(x,z)+.0008,z) for x,z in ii]
        U.line(name+'_Cavity_Lip',pts+[pts[0]],.00125,'edge')
        return ob

    def cup_point(s,u,phi,inflate=0,wall=0):
        # Ellipsoidal shell about the arm's lateral axis. A filled convex cup,
        # not an annular rail in the front plane. The lower skirt is shortened
        # slightly to flow into the upper-arm housing as seen in the video.
        rx=.160+inflate-wall; ry=.155+inflate-wall; rz=.165+inflate-wall
        si=sin(u); cp=cos(phi)
        # Oblique axis: the cap lies rear/outboard and the cup opens forward
        # and inward. A lateral-X opening produced beach-ball silhouettes.
        dx=rx*cos(u)+.005*si*si*(.5+.5*cp)
        dy=ry*si*sin(phi)
        ca=.8660254038; sa=.5
        x=.363+ca*dx-sa*dy+.020*max(0,-cp)**2*si*si
        y=-.014+sa*dx+ca*dy
        z=1.717+rz*si*(cp if cp>=0 else .88*cp)
        return (s*x,y,z)

    def pauldron_panel(name,s,u0,u1,inflate,bone):
        nu=24; np=112; verts=[]; faces=[]; wear=[]
        for inside in (False,True):
            for j in range(nu+1):
                t=j/nu; u=u0+(u1-u0)*t
                for i in range(np):
                    phi=2*pi*i/np
                    verts.append(cup_point(s,u,phi,inflate,.016 if inside else 0))
                    wear.append(.48*exp(-min(t,1-t)*35) if not inside else .07)
        layer=(nu+1)*np
        for inside in range(2):
            off=inside*layer
            for j in range(nu):
                for i in range(np):
                    a=off+j*np+i; b=off+j*np+(i+1)%np
                    c=b+np; d=a+np
                    faces.append((a,b,c,d) if not inside else (d,c,b,a))
        for j in (0,nu):
            for i in range(np):
                a=j*np+i; b=j*np+(i+1)%np
                faces.append((a,a+layer,b+layer,b) if j==0 else (b,b+layer,a+layer,a))
        cast_edges(U.mesh(name,verts,faces,'armor',wear,bone=bone))
        # Each fitted panel has one small rolled metal lip; the painted surface
        # between lips is now 5-7 cm wide and curves continuously through depth.
        pts=[cup_point(s,u1-.006,2*pi*i/112,inflate+.001) for i in range(113)]
        U.line(name+'_Rolled_Champagne_Lip',pts,.0015,'edge')
        if u0<.05:
            # Closed cap at the lateral pole; a tiny fan avoids UV-lathe degeneracy.
            q=[cup_point(s,u0,2*pi*i/np,inflate) for i in range(np)]
            qi=[cup_point(s,u0,2*pi*i/np,inflate,.016) for i in range(np)]
            pole=cup_point(s,0,0,inflate)
            innerpole=cup_point(s,0,0,inflate,.016)
            capv=[pole]+q+[innerpole]+qi; off=np+1
            capf=[]
            for i in range(np):
                a=1+i;b=1+(i+1)%np
                capf.extend(((0,a,b),(off,off+b,off+a),(a,off+a,off+b,b)))
            U.mesh(name+'_Outer_Pole',capv,capf,'armor',[0]*len(capv),bone=bone)

    for s,label in ((1,'L'),(-1,'R')):
        bone='upper_arm_l' if s==1 else 'upper_arm_r'
        U.BONE=bone
        # A deeply enclosed bearing is only glimpsed beneath the inner skirt.
        U.ellipsoid('Shoulder_'+label+'_Buried_Core',(s*.366,.035,1.697),(.084,.080,.106),'dark')
        U.cylinder('Shoulder_'+label+'_Axle',(s*.372,.024,1.708),.053,.115,'rubber',axis=(s,0,0),bone=bone)
        # Three substantial compound-curved shells make one enclosed pauldron.
        # The profile remains full in side and three-quarter views, unlike the
        # old C bands whose front projection looked like ornamental hoops.
        for k,(a,b,inflate) in enumerate(((.022,.920,0),(.943,1.280,.003),(1.303,1.610,.006))):
            pauldron_panel('Shoulder_'+label+'_Pauldron_Cup_'+str(k+1),s,a,b,inflate,bone)
        # Rounded collar root nested under the cup. No square attachment tabs.
        root=p3([(.283,-.025,1.823),(.318,-.060,1.844),(.356,-.070,1.845),(.393,-.063,1.824),(.415,-.040,1.790)],s)
        U.sweep('Shoulder_'+label+'_Collar_Root_Casting',root,.027,.019,'armor',normal=(0,0,1),steps=8,profile=20,power=3.3,bone=bone)

    U.BONE='chest'
    # An enclosed upper back volume, never a bare ball floating behind the chest.
    U.loft('Back_Deep_Chassis',[(0,.019,1.205,.151,.107),(0,.016,1.35,.159,.125),(0,.012,1.52,.210,.140),(0,.012,1.68,.290,.153),(0,.017,1.80,.276,.125),(0,.018,1.855,.140,.093)],mat='dark',start=pi*.38,end=pi*1.62,segments=64,steps=5,thickness=.010,bone='chest')

    # One broad raised collar panel wraps continuously around the back of the
    # neck and fans toward both shoulder roots. It replaces the detached rails.
    nu=96; nv=18; verts=[]; faces=[]; wear=[]
    def collar_point(th,t,under=False):
        rx=.108+(.326-.108)*t
        ry=.079+(.165-.079)*t
        # Curved front ends return into the neck/shoulder rather than terminating
        # as squared-off radial wings.
        angle=th/1.93*(1.72+.20*sin(pi*t))
        x=rx*sin(angle); y=.009+ry*cos(angle)
        z=1.896-.070*t+.032*max(0,cos(angle))*(1-.3*t)
        z+=.008*sin(pi*t)
        return (x,y,z-(.014 if under else 0))
    for under in (False,True):
        for j in range(nv+1):
            t=j/nv
            for i in range(nu+1):
                u=i/nu; th=-1.93+3.86*u
                verts.append(collar_point(th,t,under))
                wear.append(.35*exp(-min(t,1-t,u,1-u)*35) if not under else .05)
    layer=(nu+1)*(nv+1)
    for side in range(2):
        off=side*layer
        for j in range(nv):
            for i in range(nu):
                a=off+j*(nu+1)+i;b=a+1;c=b+nu+1;d=a+nu+1
                faces.append((a,b,c,d) if not side else (d,c,b,a))
    for j in (0,nv):
        for i in range(nu):
            a=j*(nu+1)+i;b=a+1
            faces.append((a,a+layer,b+layer,b) if j==0 else (b,b+layer,a+layer,a))
    for i in (0,nu):
        for j in range(nv):
            a=j*(nu+1)+i;b=a+nu+1
            faces.append((b,b+layer,a+layer,a) if i==0 else (a,a+layer,b+layer,b))
    cast_edges(U.mesh('Back_Continuous_Raised_Collar',verts,faces,'armor',wear,bone='chest'))
    for n,t in enumerate((.025,.975)):
        pts=[collar_point(-1.93+3.86*i/96,t) for i in range(97)]
        U.line('Back_Continuous_Collar_Fitted_Edge_'+str(n),pts,.0015,'edge')

    # Thick continuous rear casting connects both scapulae and the shoulder sockets.
    # Fitted surface panels below sit in this volume rather than floating in space.
    U.loft('Back_Upper_Integrated_Cast_Enclosure',[(0,.014,1.590,.226,.147),(0,.014,1.650,.278,.185),(0,.014,1.735,.300,.214),(0,.014,1.810,.267,.185),(0,.014,1.865,.153,.113)],mat='armor',start=pi*.43,end=pi*1.57,segments=64,steps=6,thickness=.022,bone='chest')

    def scapular_y(x,z):
        # Convex rear vault following the upper cast enclosure's fore/aft volume.
        ry=.177+.038*exp(-((z-1.740)/.091)**2)
        return .020+ry*sqrt(max(.04,1-(abs(x)/.315)**2))+.009

    def scapular_grid(name,s,field,thickness=.036,lift=.016):
        # Closed regular quad grid. There is no polygon fan, concave outline
        # triangulation or shared-radial centre that can fold into black gashes.
        nx=28; nz=24; verts=[]; faces=[]; wear=[]
        for rear in (False,True):
            for j in range(nz+1):
                v=j/nz
                for i in range(nx+1):
                    u=i/nx; x,z=field(u,v)
                    y=scapular_y(x,z)+lift-(thickness if rear else 0)
                    verts.append((s*x,y,z))
                    wear.append(.35*exp(-min(u,1-u,v,1-v)*28) if not rear else .05)
        layer=(nx+1)*(nz+1)
        for rear in range(2):
            off=rear*layer
            for j in range(nz):
                for i in range(nx):
                    a=off+j*(nx+1)+i;b=a+1;c=b+nx+1;d=a+nx+1
                    faces.append((a,b,c,d) if not rear else (d,c,b,a))
        for j in (0,nz):
            for i in range(nx):
                a=j*(nx+1)+i;b=a+1
                faces.append((a,a+layer,b+layer,b) if j==0 else (b,b+layer,a+layer,a))
        for i in (0,nx):
            for j in range(nz):
                a=j*(nx+1)+i;b=a+nx+1
                faces.append((b,b+layer,a+layer,a) if i==0 else (a,a+layer,b+layer,b))
        return cast_edges(U.mesh(name,verts,faces,'armor',wear,bone='chest'))

    def quadrilateral(bl,br,tr,tl):
        def field(u,v):
            return tuple((1-u)*(1-v)*bl[k]+u*(1-v)*br[k]+u*v*tr[k]+(1-u)*v*tl[k] for k in range(2))
        return field

    for s,label in ((1,'L'),(-1,'R')):
        # Rear collar is a structured faceted span from the neck to the shoulder.
        # Three convex quadrilateral panels fit the common back vault with
        # uniform narrow seams. Straight fitted limits replace pointed lobes.
        panels=(
            ('Medial',((.040,1.674),(.125,1.687),(.119,1.817),(.038,1.805))),
            ('Central',((.130,1.687),(.221,1.672),(.226,1.789),(.124,1.817))),
            ('Outer',((.227,1.671),(.282,1.679),(.293,1.744),(.232,1.787))),
        )
        for part,corners in panels:
            scapular_grid('Back_'+label+'_Scapula_'+part+'_Casting',s,quadrilateral(*corners))
        # One regular curved strip returns below the panels. Its top and bottom
        # are smooth cubic functions with positive separation everywhere.
        def lower_field(u,v):
            x=.050+.203*u
            top=(1-u)**3*1.684+3*(1-u)**2*u*1.701+3*(1-u)*u*u*1.695+u**3*1.673
            bottom=(1-u)**3*1.638+3*(1-u)**2*u*1.651+3*(1-u)*u*u*1.653+u**3*1.623
            return x,bottom+(top-bottom)*v
        scapular_grid('Back_'+label+'_Scapular_Lower_Return',s,lower_field,.052,.025)
        # Lateral connector folds towards the arm's rear shell and closes the gap.
        connector=p3([(.249,.141,1.779),(.288,.133,1.775),(.319,.104,1.757),(.344,.062,1.739)],s)
        U.sweep('Back_'+label+'_Scapula_Shoulder_Connector',connector,.029,.022,'armor',normal=(0,0,1),steps=8,profile=16,power=4,bone='chest')
        # Recessed long paraspinal red well, asymmetrically tapered like reference.
        outer=[(.062,1.657),(.126,1.664),(.197,1.595),(.195,1.440),(.163,1.226),(.145,1.139),(.087,1.143),(.050,1.251),(.046,1.455)]
        inner=[(.076,1.622),(.121,1.630),(.166,1.573),(.166,1.435),(.139,1.241),(.126,1.176),(.100,1.180),(.077,1.270),(.072,1.451)]
        def well_surface(x,z):
            return .139+.034*sin(pi*max(0,min(1,(z-1.14)/.52)))-.12*(x-.12)**2
        ring_frame('Back_'+label+'_Paraspinal_Cavity_Frame',outer,inner,well_surface,s,'armor',.014)
        # Dark perimeter underneath the frame reads as depth, red only inside it.
        U.patch('Back_'+label+'_Paraspinal_Deep_Gasket',[(s*x,z) for x,z in inner],lambda x,z:well_surface(abs(x),z)-.014,mat='rubber',thickness=.012,bevel=.001,smooth=4,bone='chest')
        redpoly=[(.084,1.606),(.120,1.613),(.155,1.565),(.153,1.436),(.130,1.245),(.120,1.191),(.107,1.197),(.088,1.277),(.082,1.452)]
        U.patch('Back_'+label+'_Recessed_Red_Tendon',[(s*x,z) for x,z in redpoly],lambda x,z:well_surface(abs(x),z)-.007+.006*sin(pi*(abs(x)-.08)/.08),mat='red',thickness=.008,bevel=.001,smooth=5,bone='chest')
        # Parallel internal ridge is built into the red insert, not an exterior hose.
        U.line('Back_'+label+'_Tendon_Inset_Ridge',p3([(.113,.165,1.592),(.126,.165,1.48),(.118,.158,1.34),(.116,.147,1.217)],s),.0013,'red')
        # Outer longitudinal rail defines the latissimus silhouette and its vent.
        rail=[(.248,1.646),(.272,1.612),(.254,1.496),(.215,1.348),(.188,1.203),(.172,1.197),(.185,1.357),(.214,1.512)]
        U.patch('Back_'+label+'_Outer_Latissimus_Rail',[(s*x,z) for x,z in rail],lambda x,z:.101+.042*(z-1.20)/.45,mat='armor',thickness=.013,bevel=.0015,smooth=3,bone='chest')
        # A compact cooling grille is recessed under the scapula in its cavity.
        for j in range(5):
            z=1.574-j*.020
            U.box('Back_'+label+'_Recessed_Cooling_Fin_'+str(j),(s*(.223-j*.003),.132-j*.001,z),(.027,.008,.005),'dark',bevel=.001)
        # A few functional screw sockets, deliberately not rows of decorative dots.
        for k,(x,y,z) in enumerate(((.265,.172,1.739),(.086,.176,1.755),(.157,.145,1.224))):
            U.cylinder('Back_'+label+'_Fastener_Recess_'+str(k),(s*x,y-.001,z),.0052,.0035,'rubber',axis=(0,1,0),bone='chest',bevel=.0005)
            U.bolt('Back_'+label+'_Fastener_'+str(k),(s*x,y+.001,z),axis=(0,1,0),r=.0026)
        # Chunky lower socket connects the well frame into the sacrum.
        lowercap=[(.073,1.195),(.150,1.198),(.173,1.145),(.166,1.090),(.129,1.062),(.080,1.097)]
        U.patch('Back_'+label+'_Sacral_Socket',[(s*x,z) for x,z in lowercap],lambda x,z:.137-.04*(1.20-z),mat='armor',thickness=.013,bevel=.002,smooth=3,bone='chest')

    # Protected articulated spinal cassette, broad at the top and narrow below.
    spine_outline=[(-.040,1.783),(.040,1.783),(.047,1.658),(.039,1.436),(.035,1.198),(.023,1.143),(-.023,1.143),(-.035,1.198),(-.039,1.436),(-.047,1.658)]
    U.patch('Back_Central_Spine_Gasket',spine_outline,lambda x,z:.158,mat='rubber',thickness=.014,bevel=.0015,smooth=3,bone='chest')
    for i in range(11):
        z=1.742-i*.049
        w=.032 if i<4 else .027
        # These taper with the spine while the near-square overlapping scales keep
        # a mechanical structure rather than a stack of puffy oval beads.
        poly=[(-w,z+.022),(w,z+.022),(w+.002,z-.008),(w-.005,z-.023),(-w+.005,z-.023),(-w-.002,z-.008)]
        U.patch('Back_Spine_Overlapping_Scale_'+str(i),poly,lambda x,z:.172+.008*(1-abs(x)/.04),mat='armor',thickness=.008,bevel=.0012,smooth=2,bone='chest')
        U.line('Back_Spine_Scale_Bottom_Lip_'+str(i),[(-w+.004,.177,z-.021),(0,.181,z-.023),(w-.004,.177,z-.021)],.0011,'edge')
    # Neck-collar service port is framed into the top bridge, visible from behind.
    U.cylinder('Back_Nape_Port_Base',(0,.126,1.850),.026,.018,'armor',axis=(0,1,.3),bone='chest')
    U.cylinder('Back_Nape_Port_Recess',(0,.137,1.853),.019,.006,'rubber',axis=(0,1,.3),bone='chest')
    U.torus('Back_Nape_Port_Lip',(0,.142,1.855),.020,.002,'silver',axis=(0,1,.3))
    U.cylinder('Back_Nape_Port_Cap',(0,.142,1.855),.013,.002,'dark',axis=(0,1,.3),bone='chest')
    U.BONE=oldbone
