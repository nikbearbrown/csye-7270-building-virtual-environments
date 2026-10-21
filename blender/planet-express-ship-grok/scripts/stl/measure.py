import numpy as np, glob, json
A='/home/box/agent-data/agents/b69b3394-2ce6-4d73-a2a8-a63bdefca41d/attachments/'
def load(k):
    f=glob.glob(A+k+'*.stl')[0]; d=open(f,'rb').read(); n=int.from_bytes(d[80:84],'little')
    a=np.frombuffer(d[84:],dtype=np.dtype([('n','<3f4'),('v','<9f4'),('a','<u2')]),count=n)
    return a['v'].reshape(-1,3).astype(float)
n=load('c7d391ae'); r=load('b060907f')
N=np.c_[n[:,2]+13.3, n[:,0], n[:,1]+39.45]
R=np.c_[-(r[:,2]+13.8), -r[:,0], r[:,1]-49.45]
V=np.r_[N,R]
np.save('hull_ship_mm.npy',V)
print('X range',V[:,0].min(),V[:,0].max())
rows=[]
for X in np.arange(-88,89,4.0):
    s=V[np.abs(V[:,0]-X)<1.0]
    if len(s)<20: continue
    hw=np.abs(s[:,1]).max(); top=s[:,2].max(); bot=s[:,2].min()
    # z of widest: mean z of points with |y|>0.97 hw
    zl=float(np.median(s[np.abs(s[:,1])>0.97*hw][:,2]))
    # superellipse probe: half-width at z midway lip-top
    zm=zl+0.5*(top-zl); b=s[np.abs(s[:,2]-zm)<0.8]; wm=np.abs(b[:,1]).max() if len(b) else 0
    zb=zl-0.5*(zl-bot); b2=s[np.abs(s[:,2]-zb)<0.8]; wb=np.abs(b2[:,1]).max() if len(b2) else 0
    rows.append([X,hw,zl,top,bot,wm/hw,wb/hw])
    print('X%6.1f hw%5.1f lip%5.1f top%5.1f bot%6.1f  up%.2f lo%.2f'%tuple(rows[-1]))
json.dump(rows,open('hull_profile_mm.json','w'))
