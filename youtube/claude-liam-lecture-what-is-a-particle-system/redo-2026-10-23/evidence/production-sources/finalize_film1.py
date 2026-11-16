from pathlib import Path
import json,shutil,hashlib,subprocess,datetime
W=Path(__file__).resolve().parent
R=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-what-is-a-particle-system/redo-2026-10-23')
report=R/'evidence/final-qc/validation.json';v=json.loads(report.read_text());assert v['full_decode']=='passed' and v['audio']['clipped_samples']==0
assert 'BLOCKER: 0  ·  MAJOR: 0' in (R/'_qc/REPORT.md').read_text()
check=subprocess.run(['python3','/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/scripts/bookend_check.py',str(R)],capture_output=True,text=True,check=True)
(R/'evidence/final-qc/bookend-check.txt').write_text(check.stdout)
v['visual_review']='Assistant inspected 102 samples across all 34 beats, including opening/closing and every act; native construction, property changes, vector motion, cleanup fault/repair, burst onset/expiry and final code/result checked. Two discovered capture defects repaired and final affected samples reinspected.'
v['qc_summary']='1920×1080 H.264/AAC; full decode passed; Gate V 68 samples, zero major defects; bookend check passed; 102 visual samples inspected; narration level/ASR checked, zero clipping. Human listening and teaching review pending.'
v['remaining_issues']=['Rough review includes pipeline beat labels.','Human listening and pedagogical approval pending; automated speech recognition is not a human review.','Native actions are scripted through an EditorPlugin and labeled. Original-speed recordings and retake edits are documented.','Fixed-frame 4K evidence is not a performance benchmark.']
report.write_text(json.dumps(v,indent=2)+'\n')
(R/'QC.md').write_text(f'''# Narrated rough-cut QC

Video: `{Path(v['video']).name}`
Runtime: {v['duration_s']:.3f} seconds (7:21.625). Resolution: 1920×1080. Video H.264, audio AAC.

{v['qc_summary']}

The first complete-file inspection found B24 becoming black after the editor window disappeared and B21's continuous pre-roll obscuring the one-shot. Both were repaired with genuine native footage. The defective candidate and evidence remain in `preserved-candidates/` and `evidence/pre-repair-qc/`. Final B21 now shows three complete burst trials with preprocess zero; B24 returns from native code to the native moving experiment. Gate settings were not weakened.

Narration: local Kokoro am_onyx, speed 0.94. Peak {v['audio']['peak_dbfs']:.2f} dBFS; zero clipped samples. Full-film local ASR word similarity {v['asr_word_similarity']:.2%}; number formatting and name homophones account for many differences. The larger local model independently recognized the flagged instructions and numbers in eleven source tracks. It correctly recognized Liam and Godot; Nik/Nick is an acoustic homophone, not a changed script credit. Silent intervals around two seconds are the intended show-before-explain lead plus narration tails; no unexplained long silence was found.

Visual review: 102 samples across 34 beats, plus native action/retake frames at critical moments. Main demonstrations are original-speed Godot footage; the source webpage is a labeled attribution hold. Every beat is filled. Six lifecycle/state checks passed separately. Raw editor captures, action receipts, source versions, rendering scripts and 90 native 4K frames are preserved.

Human listening, pacing and teaching review remain pending. This is a complete narrated review rough, not a final approved master. No real-time performance or human playtesting claim is made.

SHA-256: `{v['sha256']}`
''')
with (R/'BUILD-LOG.md').open('a') as f:f.write('\n'+datetime.datetime.now(datetime.timezone.utc).isoformat()+' Final native repair and complete-file checks passed. See QC.md and evidence/final-qc/validation.json. Human approval remains pending.\n')
with (R/'teaching-project/README.md').open('a') as f:f.write('\nOne-shot comparison: change the continuous fountain’s preprocess from 2 seconds to 0 before setting one_shot true and explosiveness 1. Otherwise the pre-roll advances its short burst before you see the onset. The repaired native take records zero pre-roll and three complete trials. `blank_tool.tscn` is the explicit empty starter shown receiving the original script.\n')
for name in ['capture_tool_creation.py','finish_construction_insert.py','capture_builtin_burst.py','repair_final_segments.py','qc_film.py','audio_flags.py','finalize_film1.py']:
 shutil.copy2(W/name,R/'evidence/production-sources'/name)
shutil.copy2(R/'beat_sheet.json',R/'authored-sheet-snapshot.json')
manifest=R/'evidence/source-manifest.json'
if not (R/'evidence/source-manifest-initial.json').exists():shutil.copy2(manifest,R/'evidence/source-manifest-initial.json')
rows=[]
for folder in [R/'teaching-project',R/'evidence/native-4k-foundations',R/'evidence/production-sources']:
 for p in sorted(folder.rglob('*')):
  if p.is_file():rows.append(dict(path=str(p.relative_to(R)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
manifest.write_text(json.dumps(dict(created=datetime.datetime.now(datetime.timezone.utc).isoformat(),files=rows),indent=2)+'\n')
print(v['video']);print(v['duration_s'],v['sha256'])
