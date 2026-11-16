from pathlib import Path
import json,hashlib,datetime,subprocess
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
root=Path(__file__).resolve().parent
slugs=['csye-7270-twenty-multiple-answer-questions','csye-7270-exam-generator-walkthrough']
playlist='PLCQVxqDm8fsw'; channel='UCg0cw2ouRhQ8dr114yGp0mA'
receipt=root/'exam-intro-private-upload-receipts.jsonl'
rows=[]
for slug in slugs:
 p=root/slug;src=p/'exports/landscape'/f'{slug}.mp4';assert src.exists(),src
 assert 'Overall: PASS' in (p/'TYPECHECK.md').read_text()
 assert 'BLOCKER: 0' in (p/'_qc/REPORT.md').read_text()
 meta=json.loads((p/'beat_sheet.json').read_text())['metadata']; rows.append((p,src,meta,hashlib.sha256(src.read_bytes()).hexdigest()))
c=Credentials.from_authorized_user_file('/Users/bear/Documents/CoWork/bear-textbooks/books/youtube/credentials/nikbearbrown/youtube_token.json')
if not c.valid:c.refresh(Request())
y=build('youtube','v3',credentials=c,cache_discovery=False)
ch=y.channels().list(part='id,snippet,contentDetails',mine=True).execute()['items'];assert len(ch)==1 and ch[0]['id']==channel
pl=y.playlists().list(part='snippet,status',id=playlist).execute()['items'][0];assert pl['snippet']['channelId']==channel and pl['status']['privacyStatus']=='private'
print('VERIFIED CHANNEL/PLAYLIST',ch[0]['snippet']['title'],pl['snippet']['title'],flush=True)
live={};token=None
while True:
 z=y.playlistItems().list(part='snippet',playlistId=ch[0]['contentDetails']['relatedPlaylists']['uploads'],maxResults=50,pageToken=token).execute()
 for a in z['items']:live.setdefault(a['snippet']['title'],[]).append(a['snippet']['resourceId']['videoId'])
 token=z.get('nextPageToken')
 if not token:break
prior={}
if receipt.exists():
 for l in receipt.read_text().splitlines():
  a=json.loads(l);prior[a['sha256']]=a
for position,(p,src,meta,sha) in enumerate(rows):
 title=meta['title']; old=prior.get(sha)
 if old: vid=old['video_id']
 else:
  assert not live.get(title),f'Live title already exists, inspect before duplicate upload: {title}'
  desc=f"{title}\n\nPrivate review draft for CSYE 7270 midterm preparation. Based on the current local draft exam coach and course knowledge sheet. The real exam and its answer key are not included. The coach has not been tested in a live Claude Project or custom GPT and is not yet published.\n\nCurrent scope clarification: knowing what PBR is and why it matters is included. Detailed PBR techniques and experience with a PBR-based No-Bake system are not required.\n\nPublic course book:\nhttps://github.com/nikbearbrown/csye-7270-building-virtual-environments\n\nThe draft coach source files are local and under review; no public prompt link is available yet.\n\nNarration: Liam, a synthetic voice, in for Bear. Native 4K review master."
  body={'snippet':{'title':title,'description':desc,'categoryId':'27','defaultLanguage':'en','defaultAudioLanguage':'en'},'status':{'privacyStatus':'private','selfDeclaredMadeForKids':False,'containsSyntheticMedia':True}}
  req=y.videos().insert(part='snippet,status',notifySubscribers=False,body=body,media_body=MediaFileUpload(str(src),chunksize=8*1024*1024,resumable=True,mimetype='video/mp4'))
  result=None
  while result is None:_,result=req.next_chunk(num_retries=0)
  vid=result['id'];entry={'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':sha,'video_id':vid,'title':title,'playlist_id':playlist,'position':position,'source':str(src)}
  with receipt.open('a') as f:f.write(json.dumps(entry)+'\n')
  print('UPLOADED',vid,title,flush=True)
 existing=y.playlistItems().list(part='snippet',playlistId=playlist,videoId=vid,maxResults=50).execute()['items']
 if not existing:
  y.playlistItems().insert(part='snippet',body={'snippet':{'playlistId':playlist,'position':position,'resourceId':{'kind':'youtube#video','videoId':vid}}}).execute()
 else:
  assert len(existing)==1
  if existing[0]['snippet']['position']!=position:
   y.playlistItems().update(part='snippet',body={'id':existing[0]['id'],'snippet':{'playlistId':playlist,'position':position,'resourceId':{'kind':'youtube#video','videoId':vid}}}).execute()
 check=y.videos().list(part='snippet,status,processingDetails',id=vid).execute()['items'][0]
 assert check['snippet']['channelId']==channel and check['status']['privacyStatus']=='private' and not check['status'].get('publishAt')
 (p/'YOUTUBE-VERIFICATION.json').write_text(json.dumps(check,indent=2)+'\n'); print('VERIFIED PRIVATE',vid,check.get('processingDetails',{}),flush=True)
order=y.playlistItems().list(part='snippet',playlistId=playlist,maxResults=50).execute()['items'];
assert [a['snippet']['title'] for a in order[:2]]==[a[2]['title'] for a in rows]
(root/'exam-intro-playlist-order.json').write_text(json.dumps(order,indent=2)+'\n')
print('VERIFIED FIRST TWO',[(a['snippet']['position'],a['snippet']['title']) for a in order[:2]],flush=True)
