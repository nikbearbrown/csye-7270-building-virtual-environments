"""Put each original question into fall-2026-exam/practice-exam-NN-KEY.md, copied from practice-exam-NN.md, and write the
"Covered in:" source lines (from exam_sources.py). Idempotent: marked blocks are stripped and rebuilt on every run, so the key's
question text cannot drift from the exam file. Checks that every cited chapter heading exists and holds its keywords.
Run: python3 -I scripts/build_combined.py"""
import re,sys
import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from exam_sources import S,NC
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
D=ROOT+'fall-2026-exam/'
base=ROOT+'chapters/'
cache={}
def sections(f):
    if f in cache: return cache[f]
    lines=open(ROOT+(f if f.startswith('modules/') else 'chapters/'+f)).read().split('\n'); idx=[]
    fence=False
    for i,l in enumerate(lines):
        if l.startswith('```'): fence=not fence
        m=None if fence else re.match(r'^(#{1,6}) (.*)',l)
        if m: idx.append((i,len(m.group(1)),m.group(2).strip()))
    cache[f]=(lines,idx); return cache[f]
def section_text(f,h):
    lines,idx=sections(f); hits=[k for k,(i,lv,t) in enumerate(idx) if t==h]
    if len(hits)!=1: return None,len(hits)
    k=hits[0]; i,lv,_=idx[k]; end=len(lines)
    for j,l2,_t in idx[k+1:]:
        if l2<=lv: end=j;break
    return '\n'.join(lines[i:end]),1

def check_sources(nns=('01','02')):
    bad=0
    for key,srcs in S.items():
        if key[0] not in nns: continue
        for f,h,kws in srcs:
            t,n=section_text(f,h)
            if t is None: print('HEADING NOT FOUND (or not unique)',key,f,h); bad+=1; continue
            for k in kws:
                if not re.search(k,t,re.I): print('KEYWORD MISSING',key,f,h,'|',k); bad+=1
    if bad: sys.exit('source check failed: %d problems'%bad)
    print('source check OK:',sum(len(v) for v in S.values()),'citations in',len(S),'entries')
def line_for(key):
    parts=[]
    for f,h,_ in S[key]:
        pf=f if f.startswith('modules/') else 'chapters/'+f
        parts.append(f'[{pf}](../{pf}), section "{h}"')
    s='**Covered in:** '+'; '.join(parts)+'.'
    if key in NC: s+=f' **Not covered in the course text:** {NC[key]}.'
    return s
def add_sources(nn):
    t=open(D+f'practice-exam-{nn}-KEY.md').read()
    t=re.sub(r'\n\*\*Covered in:\*\*[^\n]*\n','\n',t)          # idempotent
    t=re.sub(r'\n*<!-- q-begin -->.*?<!-- q-end -->\n*','\n\n',t,flags=re.S)
    ex=open(D+f'practice-exam-{nn}.md').read(); _,ec,_,em=split_exam(ex)
    out=[];n=0;cnt=[0,0]
    lines=t.split('\n');i=0;case=0
    while i<len(lines):
        l=lines[i];out.append(l)
        m=re.match(r'^## Case (\d+): ',l)
        if m:
            out.append(lines[i+1]);i+=1                     # *Chapter ...* line
            c=int(m.group(1)); out+=['',line_for((nn,'case',c))]
            qb=ec[c-1].split('\n',2)[2].strip('\n')
            out+=['','<!-- q-begin -->','#### The question, as printed in the exam','',qb,'','#### Answer key','<!-- q-end -->','']
            cnt[0]+=1
        m=re.match(r'^\*\*(\d+)\.\*\* \(`MA-',l)
        if m:
            q=int(m.group(1)); out.pop()
            out+=['<!-- q-begin -->','#### The question, as printed in the exam','',em[q-1],'','#### Answer key','<!-- q-end -->','',l,'',line_for((nn,'ma',q))]; cnt[1]+=1
        i+=1
    t2='\n'.join(out)
    t2=re.sub(r'\n{3,}','\n\n',t2)
    open(D+f'practice-exam-{nn}-KEY.md','w').write(t2)
    return cnt
def split_key(t):
    head,rest=t.split('\n# Part A: Cases\n',1)
    a,b=rest.split('\n# Part B: Multiple-answer questions\n',1)
    cases=re.split(r'\n(?=## Case \d+: )',a.strip('\n'))
    cases=[c.rstrip('\n-').rstrip() for c in cases]
    bi=re.split(r'\n(?=\*\*\d+\.\*\* \(`MA-)',b)
    return head,cases,bi[0],[x.strip('\n') for x in bi[1:]]
def split_exam(t):
    head,rest=t.split('\n# Part A: Cases (70 points)\n',1)
    a,b=rest.split('\n# Part B: Multiple-answer questions (30 points)\n',1)
    cases=re.split(r'\n(?=## Case \d+\n)',a.strip('\n'))
    cases=[c.rstrip('\n-').rstrip() for c in cases]
    bi=re.split(r'\n(?=\*\*\d+\.\*\* )',b)
    return head,cases,bi[0],[x.strip('\n') for x in bi[1:]]
def verify(nn):
    ex=open(D+f'practice-exam-{nn}.md').read(); ky=open(D+f'practice-exam-{nn}-KEY.md').read()
    _,ec,_,em=split_exam(ex)
    for c in ec: assert c.split('\n',2)[2].strip('\n') in ky,'case text drifted'
    for e in em: assert e in ky,'MA text drifted'
    assert ky.count('**Covered in:**')==13 and ky.count('<!-- q-begin -->')==13
    assert 'Covered in' not in ex,'sources leaked into the exam-only file'
    print(nn,'key shows all 13 questions verbatim from the exam file, 13 sources')
if __name__=='__main__':
    nns=sys.argv[1:] or ['01','02']
    check_sources(nns)
    for nn in nns:
        print(nn,'sourced (cases, MA):',add_sources(nn)); verify(nn)
