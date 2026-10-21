from PIL import Image,ImageOps,ImageDraw,ImageFont
from pathlib import Path
ROOT=Path('/Users/bear/Downloads/enterprise-build')
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',26)
small=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',21)
def panel(path,size,bg=(246,245,241),crop=None):
    im=Image.open(path).convert('RGB')
    if crop:im=im.crop(crop)
    im=ImageOps.contain(im,size,Image.Resampling.LANCZOS)
    out=Image.new('RGB',size,bg);out.paste(im,((size[0]-im.width)//2,(size[1]-im.height)//2));return out
specs=[('side','Side profile','constitution-side-supplied.jpg',None, 'NCC-1700 class plan; model carries Enterprise NCC-1701 markings.'),('front','Forward elevation','constitution-elevations.jpg',(14,3,214,124),'Left drawing only; low-resolution source. Scale and lighting are approximate.'),('top','Dorsal plan','constitution-general-plan.jpg',(10,139,442,328),'Top-view region of supplied poster; no perspective distortion in the render.')]
for key,title,ref,crop,note in specs:
    out=Image.new('RGB',(2000,850),(246,245,241));d=ImageDraw.Draw(out)
    d.text((30,20),title+' / reference comparison',font=font,fill='#111c25')
    d.text((30,66),'REFERENCE • supplied drawing',font=small,fill='#374755')
    d.text((1030,66),'MODEL • actual Blender render',font=small,fill='#374755')
    out.paste(panel(ROOT/'references'/ref,(940,640),crop=crop),(30,110))
    out.paste(panel(ROOT/'renders'/f'{key}.png',(940,640),bg=(16,23,30)),(1030,110))
    d.text((30,780),note,font=small,fill='#374755')
    d.text((30,814),'Reconstruction by Codex • Human review: Professor Bear — pending',font=small,fill='#374755')
    out.save(ROOT/'compare'/f'{key}-comparison.jpg',quality=92)
# Small web copies preserve full-resolution renders separately.
web=ROOT/'renders'/'web';web.mkdir(exist_ok=True)
for p in (ROOT/'renders').glob('*.png'):
    im=Image.open(p).convert('RGB');im.thumbnail((1200,1000),Image.Resampling.LANCZOS);im.save(web/(p.stem+'.jpg'),quality=87)
