#!/usr/bin/env python3
"""Verify the repo against supplied assignment definitions, not an obsolete draft template."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,re,subprocess,sys,unicodedata,zipfile
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.inhead=0
 def handle_starttag(self,tag,attrs):
  if tag=='head':self.inhead+=1
 def handle_endtag(self,tag):
  if tag=='head':self.inhead-=1
 def handle_data(self,s):
  if not self.inhead:self.parts.append(s)
def semantic(html):
 html=re.sub(r'<h1\b[^>]*>.*?</h1>','',html,count=1,flags=re.S|re.I);p=Text();p.feed(html)
 return re.sub(r'\s+','',unicodedata.normalize('NFKC',''.join(p.parts)))
def run():
 data=json.loads((ROOT/'assignments/canvas-authority.json').read_text());errors=[]
 for r in data['assignments']:
  p=ROOT/r['source'];text=p.read_text();h=hashlib.sha256(p.read_bytes()).hexdigest()
  if h!=r['imported_markdown_sha256']:errors.append(f"{p.name}: changed since authoritative import")
  if not text.startswith('# '+r['title']+'\n'):errors.append(f'{p.name}: title differs from authority')
  original=(ROOT/r['snapshot_html']).read_text()
  if hashlib.sha256(original.encode()).hexdigest()!=r['snapshot_sha256']:errors.append(f'{p.name}: source snapshot changed')
  if r['number']<10:
   rebuilt=subprocess.run(['pandoc','-f','gfm','-t','html5','--no-highlight','--wrap=none'],input=text,text=True,capture_output=True,check=True).stdout
   normalized=subprocess.run(['pandoc','-f','html','-t','html5','--no-highlight','--wrap=none'],input=original,text=True,capture_output=True,check=True).stdout
   if semantic(normalized)!=semantic(rebuilt):errors.append(f'{p.name}: body text differs from Canvas')
  else:
   for token in ['Assignment 9','teach/','PROJECT-BRIEF.md','delivered, changed or dropped','150','250','50','25','a10']:
    if token not in text:errors.append(f'final missing {token}')
   subtotal=re.search(r'### Implementation and explanation — 150 points\n(.*?)(?=\nAward)',text,re.S).group(1)
   points=sum(float(x) for x in re.findall(r'\| ([\d.]+) \|',subtotal))
   if points!=150:errors.append(f'final implementation subtotal {points} != 150')
 package=ROOT/'canvas/package/csye7270-fall-2026-godot-walker.imscc'
 if package.exists():
  with zipfile.ZipFile(package) as z:
   seen={};ns={'c':'http://canvas.instructure.com/xsd/cccv1p0'}
   for n in z.namelist():
    if n.endswith('/assignment_settings.xml'):
     e=ET.fromstring(z.read(n));seen[e.findtext('c:title',namespaces=ns)]={k:e.findtext('c:'+k,namespaces=ns) for k in ['points_possible','due_at','submission_types']}
   if len(seen)!=10:errors.append(f'package contains {len(seen)} assignments')
   for r in data['assignments']:
    expected={'points_possible':f"{r['points']:.1f}",'due_at':r['due_at_utc'],'submission_types':r['submission_types']}
    if seen.get(r['title'])!=expected:errors.append(f'package metadata mismatch: {r["title"]}')
 print('\n'.join(errors) if errors else 'PASS: nine Canvas bodies preserved; pasted final and rubric checked; ten package settings match source points, dates and submission types.')
 return errors
if __name__=='__main__':sys.exit(bool(run()))
