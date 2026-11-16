from pathlib import Path
import json,shutil,hashlib,subprocess,datetime
W=Path(__file__).resolve().parent
R=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-building-2d-particle-effects-in-godot/redo-2026-10-23')
report=R/'evidence/final-qc/validation.json';v=json.loads(report.read_text());assert v['full_decode']=='passed' and v['audio']['clipped_samples']==0
assert 'BLOCKER: 0  ·  MAJOR: 0' in (R/'_qc/REPORT.md').read_text()
check=subprocess.run(['python3','/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/scripts/bookend_check.py',str(R)],capture_output=True,text=True,check=True)
(R/'evidence/final-qc/bookend-check.txt').write_text(check.stdout)
v['visual_review']='Assistant inspected 111 samples across all 37 beats plus native burst-onset/curve/gradient retake samples and final owner-repair onset samples. Native construction, Inspector values, source input/cleanup code, ordinary input results, hidden-owner fault/repair, coordinate-space comparison, and opening/closing checked.'
v['qc_summary']='1920×1080 H.264/AAC; full decode passed; Gate V 74 samples, zero major or blocker defects; bookend check passed; 111 final visual samples plus burst onset frames inspected; narration levels and local ASR checked, zero clipping; eight real-renderer input/lifecycle tests passed. Human listening and teaching review pending.'
v['remaining_issues']=['Review rough includes pipeline beat labels.','Human listening and pedagogical approval pending; speech recognition is an automated check.','Native editor actions are scripted and labeled; synchronized viewport/Inspector crops preserve the original timing.','The focused code crop omits ends of unrelated lines while preserving the input, instantiate, position, and cleanup lines under discussion.','Fixed-frame native 4K evidence is not a performance benchmark.']
report.write_text(json.dumps(v,indent=2)+'\n')
(R/'QC.md').write_text(f'''# Narrated rough-cut QC

Video: `{Path(v['video']).name}`
Runtime: {v['duration_s']:.3f} seconds (8:19.333). Resolution: 1920×1080. Video H.264, audio AAC.

{v['qc_summary']}

37 complete narrated beats. The main lesson uses genuine macOS window-only Godot captures. The selected burst retake B09–B15 repeats native one-shot restarts so onset remains visible during explanation; both the first take and selected retake remain preserved. Framing and source timecodes are in captures/framing.json. The failed Inspector-selection pilot is retained separately.

Narration: local Kokoro am_onyx, speed 0.94. Peak {v['audio']['peak_dbfs']:.2f} dBFS; zero clipped samples. Full-film local ASR similarity {v['asr_word_similarity']:.2%}. The larger cached model checked nine flagged source tracks and five excerpts from the actual assembled soundtrack. One ambiguous visibility sentence was rewritten and regenerated, then the complete file was checked again. Definitions, explosiveness, the owner/visibility distinction, Liam signoff, and the title/handle are present. Numeric formatting and homophones are not script changes. B20 uses a measured 0.9-second lead; the other demonstrations use 1.2 seconds. The approximately two-second silent intervals are the intended show-before-explain lead plus narration tails.

Eight checks passed on the final real-renderer project, including ordinary Space/arrow inputs, event position, finished cleanup, hidden-owner failure and repair, and six bounded triggers. The first implementation redundantly called restart before enabling a fresh one-shot; that suppressed its finished signal. The final code enables the fresh instance once. Failed checks and the official engine source diagnosis are retained. This is a local implementation repair, not a claimed engine defect.

111 final visual samples and targeted burst-onset frames inspected. The native curve graph and gradient, code-to-input behavior, repeated cleanup, local/world trail comparison and CPU conversion remain visible. The code crop preserves the relevant lines but omits the ends of unrelated long lines. Ninety native 3840×2160 rendered frames and editable final/starter projects are included. Offline frames establish visual evidence, not performance.

Human listening, pacing and teaching approval remain pending. This is a complete narrated review rough, not an approved master.

SHA-256: `{v['sha256']}`
''')
with (R/'BUILD-LOG.md').open('a') as f:f.write('\n'+datetime.datetime.now(datetime.timezone.utc).isoformat()+' Complete 1080p Film 2 passed decode, gates, sampled visual review and local narration analysis. Human review remains pending. See QC.md.\n')
for n in ['make_film2.py','managed_capture.py','capture_film.py','frame_film2.py','qc_film.py','audio_flags_film2.py','review_film2_final_audio.py','finalize_film2.py','pad_narration.py']:
 shutil.copy2(W/n,R/'evidence/production-sources'/n)
shutil.copy2(R/'beat_sheet.json',R/'authored-sheet-snapshot.json')
(R/'make_sheet.py').write_text("from pathlib import Path\nimport json\nroot=Path(__file__).resolve().parent\nsheet=json.loads((root/'authored-sheet-snapshot.json').read_text())\ntarget=root/'beat_sheet.regenerated.json'\ntarget.write_text(json.dumps(sheet,indent=2)+'\\n')\nprint(target)\n")
rows=[]
for folder in [R/'teaching-project',R/'teaching-starter',R/'evidence/native-4k-2d',R/'evidence/production-sources']:
 for p in sorted(folder.rglob('*')):
  if p.is_file():rows.append(dict(path=str(p.relative_to(R)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
for p in [R/'captures/native-editor-take-01.mov',R/'capture-retake-bursts/captures/native-editor-take-01.mov']:
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(8*1024*1024),b''):h.update(chunk)
 rows.append(dict(path=str(p.relative_to(R)),bytes=p.stat().st_size,sha256=h.hexdigest()))
(R/'evidence/source-manifest.json').write_text(json.dumps(dict(created=datetime.datetime.now(datetime.timezone.utc).isoformat(),files=rows),indent=2)+'\n')
print(v['video']);print(v['duration_s'],v['sha256'])
