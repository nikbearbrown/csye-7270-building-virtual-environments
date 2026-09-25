import React from 'react';
import {registerRoot, Composition, AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, Img, staticFile, delayRender, continueRender} from 'remotion';
import {ClaudeComposerAsk} from '/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist-art/runtime/remotion/src/scenes/ClaudeComposerAsk';
import {BrutalistHesitantWriter} from '/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist-art/runtime/remotion/src/scenes/BrutalistHesitantWriter';
import {ClaudeVerdictArtifact} from '/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist-art/runtime/remotion/src/scenes/ClaudeVerdictArtifact';
import {ClaudeTitleOutro} from '/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist-art/runtime/remotion/src/scenes/ClaudeTitleOutro';

const fontGate = delayRender('Load local course fonts');
Promise.all([['EB Garamond','EBGaramond-Regular.ttf'],['Inter','Inter-Regular.ttf'],['PT Mono','PTMono-Regular.ttf']].map(async ([family,file])=>{
 const font = new FontFace(family, `url(${staticFile(file)})`); await font.load(); document.fonts.add(font);
})).then(()=>continueRender(fontGate));
const INK='#3D3929', BG='#FAF9F5', ACC='#D97757', EDGE='#CEC9BE';
const serif='"EB Garamond", Georgia, serif';
const sans='Inter, sans-serif';
type P={heading:string;mode?:string;labels?:string[];note?:string;image?:string;label?:string;durationFrames?:number;nodeSize?:number};
const appear=(f:number,start:number)=>interpolate(f,[start,start+15],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
const Shell:React.FC<{p:P;children:React.ReactNode}>=({p,children})=>{
 const f=useCurrentFrame();return <AbsoluteFill style={{background:BG,color:INK,fontFamily:serif}}>
 <div style={{position:'absolute',left:140,top:75,fontSize:72,opacity:appear(f,0)}}>{p.heading}</div>
 <div style={{position:'absolute',left:140,top:182,width:1640,height:3,background:EDGE}}/>
 {children}
 <div style={{position:'absolute',left:140,bottom:68,fontSize:50,fontFamily:serif}}>{p.note}</div>
 </AbsoluteFill>;
};
const Node:React.FC<{x:number;y:number;w?:number;label:string;active?:boolean;opacity?:number;size?:number}>=({x,y,w=340,label,active=false,opacity=1,size=54})=><div style={{position:'absolute',left:x,top:y,width:w,height:size>54?178:134,display:'flex',alignItems:'center',justifyContent:'center',border:`3px solid ${active?ACC:EDGE}`,background:active?'#F3E9E2':BG,fontSize:size,lineHeight:1.1,textAlign:'center',padding:'0 18px',boxSizing:'border-box',opacity}}>{label}</div>;
export const CourseScene:React.FC<P>=(p)=>{
 const f=useCurrentFrame();const {durationInFrames:d}=useVideoConfig();const labels=p.labels||[];
 const active=Math.min(labels.length-1,Math.floor(f/Math.max(1,d*.7/labels.length)));
 const show=(i:number)=>appear(f,24+i*38);
 const row = (labels.length===3?285:145);
 return <Shell p={p}>
 {p.mode==='tree'?<>
  <svg width="1920" height="1080" style={{position:'absolute'}}><g stroke={EDGE} strokeWidth="5" fill="none"><path d="M 960 350 V 435 M 960 555 V 635 M 430 635 H 1490 M 430 635 V 715 M 960 635 V 715 M 1490 635 V 715"/></g></svg>
  <Node x={790} y={240} label={labels[0]} active={active===0}/><Node x={790} y={435} label={labels[1]} opacity={show(1)}/>{labels.slice(2).map((s,i)=><Node key={s} x={260+i*530} y={715} label={s} active={active===i+2} opacity={show(i+2)}/>)}
 </>:p.mode==='files'||p.mode==='spec'||p.mode==='ledger'?<>
  {labels.map((s,i)=><div key={s} style={{position:'absolute',left:190,top:270+i*178,opacity:show(i),width:1540,height:130,borderBottom:`3px solid ${EDGE}`,display:'flex',alignItems:'center',gap:44}}><span style={{width:18,height:90,background:i===active?ACC:EDGE}}/><span style={{fontSize:56,fontFamily:p.mode==='files'?'"PT Mono", monospace':serif}}>{s}</span></div>)}
 </>:p.mode==='scope'?<>
  <div style={{position:'absolute',left:300,top:290,width:1320,height:190,border:`5px solid ${ACC}`,display:'flex',alignItems:'center',justifyContent:'center',fontSize:74}}>{labels[0]}</div>
  {labels.slice(1).map((s,i)=><div key={s} style={{position:'absolute',left:350+i*700,top:650,fontSize:52,opacity:show(i+1)}}>{s}<svg width="520" height="70" style={{position:'absolute',left:-30,top:0}}><path d="M 0 35 H 480" stroke={INK} strokeWidth="3"/></svg></div>)}
 </>:p.mode==='level'?<>
  <svg width="1920" height="1080" style={{position:'absolute'}}>
   <path d="M 180 760 H 580 V 830 H 180 Z" fill={INK}/><path d="M 780 675 H 1060 V 750 H 780 Z" fill={ACC} opacity={show(1)}/><path d="M 1270 590 H 1690 V 670 H 1270 Z" fill={ACC} opacity={show(2)}/>
   <path d="M 420 740 Q 620 400 880 660 M 920 650 Q 1150 330 1380 580" fill="none" stroke={INK} strokeWidth="5" strokeDasharray="14 14" opacity={show(1)}/><path d="M 1610 410 V 590 H 1620 V 410 Z M 1620 420 L 1690 450 L 1620 480 Z" fill={INK} opacity={show(2)}/>
  </svg><div style={{position:'absolute',left:200,top:825,fontSize:50}}>{labels[0]}</div><div style={{position:'absolute',left:810,top:805,fontSize:50,opacity:show(1)}}>{labels[1]}</div><div style={{position:'absolute',left:1450,top:300,fontSize:50,opacity:show(2)}}>{labels[2]}</div>
 </>:p.mode==='cadence'?<>
  <div style={{position:'absolute',left:180,top:275,fontSize:60}}>{labels[0]}</div><div style={{position:'absolute',right:190,top:275,fontSize:52}}>{labels[1]}</div>
  <svg width="1920" height="1080" style={{position:'absolute'}}>{[0,1,2,3,4,5,6].map((i)=><rect key={i} x={190+i*220} y={405} width={150} height={80} fill={i<=active+2?ACC:EDGE}/>)}<path d="M 190 730 H 1730" stroke={INK} strokeWidth="5"/>{[0,1,2,3].map(i=><circle key={i} cx={190+i*510} cy={730} r={18} fill={INK}/>)}</svg>
  <div style={{position:'absolute',left:190,top:800,fontSize:62}}>{labels[2]}</div>
 </>:p.mode==='art'?<>
  <svg width="1920" height="1080" style={{position:'absolute'}}>{[0,1,2].map((i)=><g key={i} opacity={show(i)} transform={`translate(${350+i*600} 530)`}><rect x={-210} y={-240} width={420} height={470} rx={8} fill={i===2?'#DADCCB':'#F0ECE4'}/><path d={i===0?'M -50 70 V -60 H 55 V 70 M -50 -60 L -80 -130 L -10 -95 L 60 -130 L 55 -60':i===1?'M -80 80 L -100 -40 L -35 -125 L 30 -105 L 95 -30 L 65 80 Z':'M -55 85 V -40 L -90 -80 L -35 -125 H 40 L 95 -75 L 50 -35 V 85 Z'} fill={i===2?INK:ACC}/><circle cx={-12} cy={-55} r={8} fill={BG}/><circle cx={22} cy={-55} r={8} fill={BG}/></g>)}</svg>
  <div style={{position:'absolute',left:200,top:810,fontSize:50}}>Constructed silhouette study</div><div style={{position:'absolute',right:240,top:810,fontSize:50}}>Test in context</div>
 </>:<>
  <svg width="1920" height="1080" style={{position:'absolute'}}><path d={`M ${row+140} 555 H ${row+(labels.length-1)*420+140}`} stroke={EDGE} strokeWidth="5"/></svg>
  {labels.map((s,i)=><React.Fragment key={s}><Node size={p.nodeSize} x={row+i*420} y={p.nodeSize&&p.nodeSize>54?473:495} w={340} label={s} active={i===active} opacity={show(i)}/><div style={{position:'absolute',left:row+i*420,top:360,width:340,textAlign:'center',fontSize:76,opacity:show(i)}}>{String(i+1).padStart(2,'0')}</div></React.Fragment>)}
 </>}
 </Shell>;
};
export const CourseEvidence:React.FC<P>=(p)=>{
 const f=useCurrentFrame();return <Shell p={p}>
 <div style={{position:'absolute',left:320,top:215,width:1280,height:720,opacity:appear(f,0),border:`3px solid ${EDGE}`,boxSizing:'content-box'}}><Img src={staticFile(p.image!)} style={{width:'100%',height:'100%',objectFit:'contain'}}/></div>
 </Shell>;
};
const defaults={heading:'Course evidence',labels:['Intent','Build','Inspect'],note:'CSYE 7270',durationFrames:240};
const entries:any[]=[['CourseScene',CourseScene],['CourseEvidence',CourseEvidence],['ClaudeComposerAsk',ClaudeComposerAsk],['BrutalistHesitantWriter',BrutalistHesitantWriter],['ClaudeVerdictArtifact',ClaudeVerdictArtifact],['ClaudeTitleOutro',ClaudeTitleOutro]];
const Root:React.FC=()=> <>{entries.map(([id,component])=><Composition key={id} id={id} component={component} width={1920} height={1080} fps={24} durationInFrames={240} defaultProps={defaults} calculateMetadata={({props})=>({durationInFrames:props.durationFrames||240})}/>)}</>;
registerRoot(Root);
