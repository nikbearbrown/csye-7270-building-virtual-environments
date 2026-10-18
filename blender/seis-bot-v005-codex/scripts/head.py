"""SEIS Bot v005: fitted continuous mask and fluted helmet.
Primary reference: generated_video_frame_000360/000120/000240-topaz-upscale-4x.
Authoritative on-model front, raised throat, and side frames supersede prior stills.
All proportions in metres; front is -Y. No enlarged separate facial pads.
"""
import math
from math import sin,cos,pi,sqrt
from mathutils import Vector
import bpy
import bmesh


def build_head(U):
    def apply(o, typ, name, **kw):
        m=o.modifiers.new(name,typ)
        for k,v in kw.items(): setattr(m,k,v)
        bpy.context.view_layer.objects.active=o
        try: bpy.ops.object.modifier_apply(modifier=m.name)
        except RuntimeError: pass
        return o

    def closed_skin(name,verts,faces,mat,thickness=.0025,bevel=.0006,bone=None):
        o=U.mesh(name,verts,faces,mat,bone=bone)
        # Merge the two mask halves into one genuine skin along the centre line.
        bm=bmesh.new(); bm.from_mesh(o.data)
        bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=0.000001)
        bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
        if thickness: apply(o,'SOLIDIFY','Skin_thickness',thickness=thickness,offset=-1,use_rim=True)
        if bevel: apply(o,'BEVEL','Manufactured_edges',width=bevel,segments=3,limit_method='ANGLE',angle_limit=.6)
        return o

    def interp(z,rows):
        # Monotone cubic Hermite interpolation shares a derivative at each row.
        # The earlier per-interval smoothstep forced slope to zero at every row,
        # creating the unwanted horizontal corrugations in a reflective mask.
        if z <= rows[0][0]: return rows[0][1]
        if z >= rows[-1][0]: return rows[-1][1]
        xx=[q[0] for q in rows]; yy=[q[1] for q in rows]
        hh=[b-a for a,b in zip(xx,xx[1:])]
        sec=[(b-a)/h for a,b,h in zip(yy,yy[1:],hh)]
        d=[sec[0]]
        for i in range(1,len(rows)-1):
            if sec[i-1]*sec[i] <= 0: d.append(0.)
            else:
                w1=2*hh[i]+hh[i-1];w2=hh[i]+2*hh[i-1]
                d.append((w1+w2)/(w1/sec[i-1]+w2/sec[i]))
        d.append(sec[-1])
        for i in range(len(rows)-1):
            if xx[i] <= z <= xx[i+1]:
                t=(z-xx[i])/hh[i]
                return ((2*t**3-3*t**2+1)*yy[i]+(t**3-2*t**2+t)*hh[i]*d[i]
                        +(-2*t**3+3*t**2)*yy[i+1]+(t**3-t**2)*hh[i]*d[i+1])

    def smooth_min(a,b,k=.003):
        h=max(k-abs(a-b),0)/k
        return min(a,b)-h*h*k*.25

    # One connected silver skin, shaped by broad machined planes across the nose
    # and muzzle. Eyelid apertures are actual holes through this shell.
    def face_y(x,z):
        # Deliberate planar nose/muzzle with long continuous cheek chamfers.
        # The central forty millimetres remain flat across the centre seam.
        prof=interp(z,[(1.923,-.096),(1.940,-.125),(1.960,-.141),
                      (1.990,-.142),(2.022,-.134),(2.045,-.119),
                      (2.070,-.108),(2.095,-.092),(2.15,-.046),(2.18,-.013),(2.20,.005)])
        plane=prof+max(0,abs(x)-.024)*.80
        # One continuous field over the ENTIRE front cap. The previous z>2.07
        # switch moved the temple surface forward by about 8 mm at one row,
        # producing the visible rectangular forehead wings and shell overlap.
        # Blend to the skull everywhere; lower nose planes are already farther
        # forward and remain unchanged by this smooth minimum.
        skull=.012-.108*sqrt(max(.0005,1-(x/.128)**2-((z-2.033)/.164)**2))-.0020
        return smooth_min(plane,skull,.0035)

    U.BONE='head'
    U.ellipsoid('Helmet_structural_shell',(0,.012,2.033),(.128,.108,.164),'armor',seg=96,rings=64)
    # The rear shell and vented occipital closure share the same curved head.
    U.ellipsoid('Occipital_rear_insert',(0,.063,2.024),(.108,.064,.128),'dark',seg=48,rings=32)

    eye_c=(.051,2.023)
    def eye_edge(a,scale=1):
        dx=.0305*cos(a)*scale
        dz=.0153*math.copysign(abs(sin(a))**1.15,sin(a))*scale+.22*dx
        return eye_c[0]+dx,eye_c[1]+dz

    # A structured rectangular topology mapped into a tapered outline, with
    # boolean eye apertures. This replaces the ray-based annuli: those developed
    # severe long-quad shading wrinkles around the central nose and chin.
    def face_width(z):
        return interp(z,[(1.923,.016),(1.940,.030),(1.960,.050),
                         (1.980,.065),(2.000,.081),(2.030,.097),
                         (2.060,.095),(2.085,.087),(2.110,.080),(2.140,.075),(2.160,.067),(2.180,.047),(2.196,.008)])
    verts=[];faces=[];nu=80;nv=100
    for side in range(2):
        for j in range(nv+1):
            z=1.923+(2.196-1.923)*j/nv;w=face_width(z)
            for i in range(nu+1):
                x=w*(-1+2*i/nu)
                verts.append((x,face_y(x,z)+side*.004,z))
    N=(nu+1)*(nv+1)
    for j in range(nv):
        for i in range(nu):
            a=j*(nu+1)+i;b=a+1;c=b+nu+1;d=a+nu+1
            faces.extend([(a,b,c,d),(N+d,N+c,N+b,N+a)])
    boundary=list(range(nu+1))+[j*(nu+1)+nu for j in range(1,nv+1)]+[nv*(nu+1)+i for i in range(nu-1,-1,-1)]+[j*(nu+1) for j in range(nv-1,0,-1)]
    for i,a in enumerate(boundary):
        b=boundary[(i+1)%len(boundary)];faces.append((a,N+a,N+b,b))
    mask=U.mesh('Continuous_silver_face_mask',verts,faces,'silver')
    for ss in [-1,1]:
        cv=[];cf=[];n=96
        for yy in [-.30,.12]:
            for j in range(n):
                x,z=eye_edge(2*pi*j/n)
                cv.append((ss*x,yy,z))
        cf.extend([tuple(reversed(range(n))),tuple(range(n,2*n))])
        for j in range(n):cf.append((j,(j+1)%n,(j+1)%n+n,j+n))
        cutter=U.mesh('TEMP_EYE_CUTTER_'+str(ss),cv,cf,'dark')
        m=mask.modifiers.new('Precision_eye_aperture','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=cutter
        bpy.context.view_layer.objects.active=mask
        bpy.ops.object.modifier_apply(modifier=m.name)
        U.PARTS.pop(cutter.name,None);bpy.data.objects.remove(cutter,do_unlink=True)
    # Only aperture and silhouette edges are bevelled; quad interior stays planar.
    apply(mask,'BEVEL','Eye_and_silhouette_radii',width=.00045,segments=3,limit_method='ANGLE',angle_limit=.50)

    # Authoritative video eyes are filled luminous red lenses, not human irises.
    for key,base,emission,strength in [
        ('seis_eye_glow','eye',(.080,.0001,.0004,1),.10),
        ('seis_eye_hotspot','white',(1.0,.80,.73,1),2.3),
        ('seis_eye_inner','eye',(1.0,.001,.006,1),3.5)]:
        material=U.M[base].copy();material.name='MAT_'+key
        bs=material.node_tree.nodes.get('Principled BSDF')
        for socket in ['Base Color','Roughness','Normal']:
            for link in list(bs.inputs[socket].links):material.node_tree.links.remove(link)
        bs.inputs['Base Color'].default_value=emission
        bs.inputs['Emission Color'].default_value=emission;bs.inputs['Emission Strength'].default_value=strength
        bs.inputs['Metallic'].default_value=.12;bs.inputs['Roughness'].default_value=.26 if base=='eye' else .17
        U.M[key]=material
    # Red lenses are inset into the enlarged almond openings in the solid mask.
    for s in [-1,1]:
        sn='L' if s>0 else 'R'
        boundary=[]
        for j in range(96):
            x,z=eye_edge(2*pi*j/96,1.08)
            boundary.append((s*x,face_y(x,z)+.004,z))
        centre=(s*eye_c[0],face_y(*eye_c)+.006,eye_c[1])
        ev=[centre]+boundary
        ef=[(0,1+j,1+(j+1)%96) if s>0 else (0,1+(j+1)%96,1+j) for j in range(96)]
        closed_skin('Eye_'+sn+'_dark_recess',ev,ef,'glass',.001,0)
        # Bronze and black eyelid lips follow exactly the aperture; tiny edging.
        lip=[];inner=[]
        for j in range(97):
            x,z=eye_edge(2*pi*j/96,1.015);lip.append((s*x,face_y(x,z)-.0007,z))
            x,z=eye_edge(2*pi*j/96,.965);inner.append((s*x,face_y(x,z)+.0014,z))
        U.line('Eye_'+sn+'_socket_lip',lip,.00115,'bronze')
        U.line('Eye_'+sn+'_inner_rubber_seal',inner,.0011,'rubber')
        # A shallow fitted lens follows the mask surface behind the aperture.
        # A free ellipsoid crossed the sloping cheek plane and looked like an
        # external pink bulb; every lens vertex is now recessed in the opening.
        cx=s*.051;cz=2.023;lv=[];lf=[];nr=14;na=64
        lv.append((cx,face_y(abs(cx),cz)+.0024,cz))
        for ring in range(1,nr+1):
            rr=ring/nr
            for j in range(na):
                aa=2*pi*j/na;dx=.024*rr*cos(aa)
                xp=.051+dx;zz=cz+.0115*rr*sin(aa)+.22*dx
                yy=face_y(xp,zz)+.0030-.0006*(1-rr*rr)
                lv.append((s*xp,yy,zz))
        for j in range(na):
            lf.append((0,1+j,1+(j+1)%na) if s>0 else (0,1+(j+1)%na,1+j))
        for ring in range(nr-1):
            for j in range(na):
                a=1+ring*na+j;b=1+ring*na+(j+1)%na
                lf.append((a,b,b+na,a+na) if s>0 else (a+na,b+na,b,a))
        closed_skin('Eye_'+sn+'_filled_red_lens',lv,lf,'seis_eye_glow',.001,0)
        hx=s*.049;hz=cz+.0024;hy=face_y(abs(hx),hz)+.0021
        U.ellipsoid('Eye_'+sn+'_red_optical_core',(hx,hy+.0006,hz),(.0060,.0011,.0044),'seis_eye_inner',seg=32,rings=24)
        U.ellipsoid('Eye_'+sn+'_bright_core',(hx,hy,hz),(.0018,.0007,.0015),'seis_eye_hotspot',seg=24,rings=16)
        # Fine engraved routes turn across the silver plate rather than puffing it.
        routes=[[(.023,2.009),(.027,1.992),(.031,1.974),(.037,1.955)],
                [(.083,2.011),(.077,1.994),(.066,1.977)]]
        for i,route in enumerate(routes):
            pts=[]
            for (x0,z0),(x1,z1) in zip(route,route[1:]):
                for sample in range(13):
                    t=sample/12;x=x0+(x1-x0)*t;z=z0+(z1-z0)*t
                    if pts and sample==0:continue
                    x=min(x,face_width(z)-.0035)
                    pts.append((s*x,face_y(x,z)+.00006,z))
            U.line('Mask_'+sn+'_panel_boundary_%02d'%i,pts,.00028,'bronze')

        # Three short parallel service cuts on the lower cheek. Each sample is
        # projected individually onto the real face; the 0.38 mm dark core sits
        # partly inside the skin, reading as a fine engraved panel boundary.
        for cut in range(3):
            z0=1.971-cut*.008
            pts=[]
            for sample in range(29):
                t=sample/28
                x=.031+.012*t
                z=z0-.0015*t
                x=min(x,face_width(z)-.0035)
                pts.append((s*x,face_y(x,z)+.00010,z))
            U.line('Mask_'+sn+'_micro_panel_cut_%d'%cut,pts,.00038,'dark')

    # Longitudinal helmet ribbons: actual curved plate bands continue over crown.
    # Spherical surface strips use projected angle/latitude, not flattened decals.
    def crown_surface(phi,theta,out=0):
        # Matched exactly to the skull radii: these are fitted plates, not rails.
        extra=.0009
        x=(.128+extra)*sin(theta)
        a=cos(theta)
        z=2.033+(.164+extra)*cos(phi)*a
        y=.012+(.108+extra)*sin(phi)*a
        if phi < 0 and 1.923<z<2.196:
            # One continuous frontal silver cap now extends over the crown.
            # All silver ribbon points on that cap share its actual surface,
            # avoiding the previous horizontal forehead flap and intersections.
            margin=face_width(z)-abs(x)
            blend=max(0,min(1,margin/.006))
            if blend>0:
                fy=face_y(x,z)-.0011
                y=y*(1-blend)+smooth_min(y,fy,.0015)*blend
        return x,y,z
    for s in [-1,1]:
        sn='L' if s>0 else 'R'
        for i,(lo,hi,mat) in enumerate([(.10,.46,'silver'),(.50,.73,'silver')]):
            v=[];f=[];nu=64;nv=9
            for j in range(nu+1):
                phi=-1.48+(3.22*j/nu)
                # Elegant converging crests at forehead, widening behind crown.
                widthscale=.78+.22*sin(pi*(j/nu))
                drift=.10*sin(phi+.65)
                for k in range(nv+1):
                    theta=s*((lo+(hi-lo)*k/nv)*widthscale+drift)
                    v.append(crown_surface(phi,theta,.0035+i*.0002))
            for j in range(nu):
                for k in range(nv):
                    a=j*(nv+1)+k;f.append((a,a+1,a+nv+2,a+nv+1) if s>0 else (a+nv+1,a+nv+2,a+1,a))
            closed_skin('Helmet_'+sn+'_crown_track_%d'%i,v,f,mat,.0022,.00065)
            for edge in [lo,hi]:
                pp=[]
                for j in range(nu+1):
                    phi=-1.48+3.22*j/nu;widthscale=.78+.22*sin(pi*j/nu);drift=.10*sin(phi+.65)
                    pp.append(crown_surface(phi,s*(edge*widthscale+drift),.0044+i*.0002))
                U.line('Helmet_'+sn+'_track_%d_edge_%03d'%(i,int(edge*1000)),pp,.00065,'bronze')
        # Transverse panel divisions flow across the fitted crown plates near
        # the brow. They follow the identical parametric surface at every point,
        # including the forehead blend, avoiding floating straight chord lines.
        for track,(lo,hi) in enumerate([(.10,.46),(.50,.73)]):
            for cut,phi in enumerate([-1.36,-1.23,-1.10]):
                u=(phi+1.48)/3.22
                widthscale=.78+.22*sin(pi*u)
                drift=.10*sin(phi+.65)
                pts=[]
                for sample in range(33):
                    t=sample/32
                    theta=s*((lo+.012+(hi-lo-.024)*t)*widthscale+drift)
                    x,y,z=crown_surface(phi,theta)
                    # Embed the line slightly into the plate surface.
                    normal=Vector((x/(.128**2),(y-.012)/(.108**2),(z-2.033)/(.164**2))).normalized()
                    pp=Vector((x,y,z))-normal*.00008
                    pts.append(tuple(pp))
                U.line('Helmet_'+sn+'_crown_plate_division_%d_%d'%(track,cut),pts,.00036,'dark')

        # Swept cheek/jaw shields echo the distinctive wraparound reference form.
        jaw=[(s*.116,.032,2.107),(s*.133,.010,2.068),(s*.138,-.024,2.021),
             (s*.126,-.050,1.984),(s*.103,-.076,1.949),(s*.074,-.080,1.925),
             (s*.045,-.074,1.913),(s*.029,-.068,1.916)]
        U.sweep('Helmet_'+sn+'_swept_jaw_shield',jaw,.0105,.006,'armor',normal=(0,-1,0),steps=10,profile=18,power=4)
        U.line('Helmet_'+sn+'_jaw_exposed_edge',[(x,y-.006,z) for x,y,z in jaw],.00095,'edge')
        inner=[(s*.111,-.038,2.026),(s*.115,-.065,1.995),(s*.100,-.080,1.965),
               (s*.075,-.090,1.940),(s*.046,-.084,1.925)]
        U.sweep('Helmet_'+sn+'_inner_jaw_frame',inner,.0055,.004,'armor',normal=(0,-1,0),steps=9,profile=14,power=4)
        U.line('Helmet_'+sn+'_inner_jaw_seal',[(x,y+.004,z) for x,y,z in inner],.0012,'rubber')
        # Integrated ear mechanism, surrounded by shell rather than free discs.
        ear=(s*.126,.008,2.017);axis=(s,0,0)
        U.cylinder('Helmet_'+sn+'_ear_bearing',ear,.036,.012,'dark',axis=axis,vertices=64,bevel=.001)
        U.torus('Helmet_'+sn+'_ear_gasket',(s*.134,.008,2.017),.029,.0024,'rubber',axis)
        U.cylinder('Helmet_'+sn+'_ear_hub',(s*.136,.008,2.017),.022,.006,'armor',axis=axis,vertices=56,bevel=.0006)
        U.torus('Helmet_'+sn+'_ear_ring',(s*.140,.008,2.017),.020,.0011,'edge',axis)
        U.cylinder('Helmet_'+sn+'_ear_axle',(s*.141,.008,2.017),.010,.002,'dark',axis=axis,vertices=40,bevel=.0005)
        U.bolt('Helmet_'+sn+'_ear_service_fastener',(s*.143,.008,2.017),axis=axis,r=.0023)
        # Cheek turbine is recessed obliquely into the face/jaw intersection.
        axis=Vector((s*.87,-.49,0)).normalized();center=Vector((s*.104,-.071,1.970))
        U.cylinder('Helmet_'+sn+'_cheek_rotor_bed',tuple(center),.026,.004,'dark',axis=tuple(axis),vertices=64,bevel=.0004)
        center+=axis*.0028
        U.torus('Helmet_'+sn+'_cheek_outer_lip',tuple(center),.024,.0010,'armor',tuple(axis))
        U.torus('Helmet_'+sn+'_cheek_inner_lip',tuple(center+axis*.0008),.019,.0008,'rubber',tuple(axis))
        av=axis;uu=Vector((0,0,1));vv=av.cross(uu).normalized()
        for i in range(12):
            a=2*pi*i/12; da=.11
            pts=[]
            for r,t,d in [(.008,a,.001),(.021,a+.12,.000),(.021,a+.12+da,.000),(.008,a+da,.001)]:
                pts.append(tuple(center+uu*(r*cos(t))+vv*(r*sin(t))+av*d))
            closed_skin('Helmet_'+sn+'_cheek_vane_%02d'%i,pts,[(0,1,2,3)],'dark',.001,0)
        U.cylinder('Helmet_'+sn+'_cheek_axle',tuple(center+av*.0014),.0085,.002,'dark',axis=tuple(av),vertices=40,bevel=.0005)
        U.torus('Helmet_'+sn+'_cheek_axle_lip',tuple(center+av*.0025),.007,.0007,'silver',tuple(av))
        for i in range(3):
            a=2*pi*i/3
            pos=center+uu*(.013*cos(a))+vv*(.013*sin(a))+av*.002
            U.bolt('Helmet_'+sn+'_rotor_fastener_%d'%i,tuple(pos),axis=tuple(av),r=.0017)

    # Central dark forehead keel joins the forehead to the long upper crown.
    def forehead_y(x,z):
        shell=.012-.109*sqrt(max(.025,1-(x/.129)**2-((z-2.033)/.165)**2))-.0006
        return smooth_min(shell-.0015,face_y(x,z)-.0025,.003)
    fv=[];ff=[];nu=32;nv=96
    for j in range(nv+1):
        z=2.110+(2.196-2.110)*j/nv
        w=interp(z,[(2.110,.008),(2.126,.015),(2.152,.029),(2.176,.038),(2.189,.029),(2.196,.016)])
        for i in range(nu+1):
            x=w*(-1+2*i/nu);fv.append((x,forehead_y(x,z),z))
    for j in range(nv):
        for i in range(nu):
            a=j*(nu+1)+i;ff.append((a,a+1,a+nu+2,a+nu+1))
    forehead=closed_skin('Helmet_central_petrol_forehead',fv,ff,'armor',.0025,.0004)
    for i in range(3):
        z=2.067+i*.013
        pp=[(x,face_y(x,z)+.00008,z) for x in [-.014,-.007,0,.007,.014]]
        U.line('Helmet_forehead_register_%d'%i,pp,.00040,'dark')
    jaw_bridge=[(-.043,-.086,1.929),(-.029,-.095,1.909),(0,-.100,1.901),(.029,-.095,1.909),(.043,-.086,1.929)]
    U.sweep('Helmet_integrated_lower_jaw_closure',jaw_bridge,.009,.006,'armor',normal=(0,-1,0),steps=10,profile=20,power=4)
    U.line('Helmet_lower_jaw_precise_lip',[(x,y-.006,z) for x,y,z in jaw_bridge],.0008,'silver')
    # Distinct chin plate, closely fitted below the shared face skin.
    # Close the lower-mask/jaw transition with a fitted solid chin shield.
    cv=[];cf=[];nu=32;nv=30
    for j in range(nv+1):
        z=1.883+.046*j/nv
        w=interp(z,[(1.883,.012),(1.897,.023),(1.915,.032),(1.929,.028)])
        cy=interp(z,[(1.883,-.071),(1.900,-.093),(1.915,-.103),(1.929,-.100)])
        for i in range(nu+1):
            x=w*(-1+2*i/nu);cv.append((x,cy+.12*abs(x),z))
    for j in range(nv):
        for i in range(nu):
            a=j*(nu+1)+i;cf.append((a,a+1,a+nu+2,a+nu+1))
    closed_skin('Helmet_lower_chin_plate',cv,cf,'armor',.004,.0006)
    # Back plates contain shallow vents and seams following the helmet curve.
    for s in [-1,1]:
        for j in range(5):
            z=1.990+j*.017
            pp=[]
            for i in range(12):
                x=s*(.018+.060*i/11)
                y=.012+.111*sqrt(max(.05,1-(x/.132)**2-((z-2.035)/.166)**2))+.002
                pp.append((x,y,z))
            U.line('Helmet_rear_%s_vent_%d'%('L' if s>0 else 'R',j),pp,.0016,'rubber')
    # Cervical section: broad protected neck with overlapping plate courses.
    U.BONE='neck'
    U.ellipsoid('Cervical_inner_frame',(0,.012,1.842),(.067,.060,.092),'dark',seg=48,rings=32)
    U.sweep('Cervical_exposed_red_throat',[(0,-.033,1.804,.70),(0,-.034,1.837,.88),(0,-.034,1.873,1.0),(0,-.024,1.912,.84)],.033,.012,'red',normal=(0,-1,0),steps=10,profile=24,power=4)
    for j,z in enumerate([1.817,1.841]):
        U.sweep('Cervical_front_silver_chevron_%d'%j,[(-.025,-.060,z+.009),(0,-.064,z),(.025,-.060,z+.009)],.0055,.003,'silver',normal=(0,-1,0),steps=8,profile=16,power=4)
    U.cylinder('Cervical_rotary_base',(0,.007,1.795),.076,.015,'dark',axis=(0,0,1),vertices=64,bevel=.001)
    for j in range(4):
        za=1.797+j*.027;zb=za+.024;rx=.082-j*.0036;ry=.072-j*.0020
        for k,(a,b) in enumerate([(-1.58,-.55),(.55,1.58),(1.65,3.10),(-3.10,-1.65)]):
            rows=[(0,.014,za,rx,ry),(0,.014,za+.009,rx+.002,ry+.001),(0,.014,zb,rx-.002,ry-.001)]
            U.loft('Cervical_course_%d_segment_%d'%(j,k),rows,'silver' if k<2 else 'armor',start=a,end=b,segments=16,steps=4,thickness=.003)
            pp=[]
            for n in range(25):
                theta=a+(b-a)*n/24
                pp.append(((rx+.0003)*sin(theta),.014-(ry+.0003)*cos(theta),za+.001))
            U.line('Cervical_course_%d_edge_%d'%(j,k),pp,.0009,'edge')
    for s in [-1,1]:
        sn='L' if s>0 else 'R'
        # Red elastomer flexors sit behind the neck guard at the side.
        p=[(s*.051,.022,1.794),(s*.054,.018,1.827),(s*.057,.016,1.866),(s*.060,.019,1.903)]
        U.sweep('Cervical_'+sn+'_recessed_flexor',p,.011,.010,'red',normal=(s,0,0),steps=8,profile=14,power=3)
        U.cylinder('Cervical_'+sn+'_rotation_pin',(s*.071,.005,1.883),.012,.006,'dark',axis=(s,0,0),vertices=40,bevel=.0005)
    U.BONE='head'

    # Final reference comparison supports the native width. The previous 0.93
    # X compression made the head too small against the rebuilt shoulder shells.
