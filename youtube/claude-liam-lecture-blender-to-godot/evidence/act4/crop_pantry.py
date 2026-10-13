# a4_post.png / a4_post_hull.png = the SAME crop box of the real Blender renders (same camera), so the hull overlays the post exactly.
from PIL import Image
import os
here=os.path.dirname(os.path.abspath(__file__)); pantry=os.path.join(here,'..','..','pantry')
box=(967-10,250-10,1348+10,1128+10)
for src,dst in [('post_visual','a4_post'),('post_collider_only','a4_post_hull')]:
    Image.open(os.path.join(pantry,src+'.png')).crop(box).save(os.path.join(pantry,dst+'.png'))
