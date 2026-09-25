"""Resume only this film: fixed result excerpts, scene renders, then review cut."""
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ART=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art')
commands=[
 [sys.executable,ROOT/'scripts/build.py','footage','--only','B14','B18','B20','--force'],
 [sys.executable,ROOT/'scripts/build.py','render'],
 [sys.executable,ROOT/'scripts/qc.py','contacts'],
 [sys.executable,ART/'runtime/scripts/compile.py',ROOT,'--review','--height','1080','--fps','30'],
]
for i,cmd in enumerate(commands):
    print('STAGE',i+1,' '.join(map(str,cmd)),flush=True)
    subprocess.run(list(map(str,cmd)),check=True,cwd=ROOT)
print('REVIEW READY. Inspect contacts and scenes before final export.',flush=True)
