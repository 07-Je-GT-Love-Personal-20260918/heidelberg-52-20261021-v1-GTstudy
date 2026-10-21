from pathlib import Path
import requests,json,datetime,concurrent.futures,hashlib
R=Path(__file__).parent
bases={'githubPages':'https://07-je-gt-love-personal-20260918.github.io/heidelberg-52-20261021-v1-GTstudy/','surge':'https://heidelberg-52-20261021-v1-gtstudy.surge.sh/','vercel':'https://heidelberg-52-20261021-v1-gtstudy.vercel.app/'}
files=['index.html','day-01.html','day-27.html','day-52.html','reader-apostles.html','reader-nicene.html','reader-athanasian.html','library.html','style.css','app.js','fulltexts.json','source-audit.json','places.json','creeds.json','lessons.json','journey.svg']
def verify(arg):
 k,b,f=arg
 try:
  r=requests.get(b+f,timeout=30);r.raise_for_status();r.encoding='utf-8'
  match=r.text.replace('\r\n','\n')==(R/'dist'/f).read_text(encoding='utf-8').replace('\r\n','\n')
  return {'platform':k,'file':f,'url':b+f,'status':r.status_code,'matches_local':match,'sha256':hashlib.sha256(r.content).hexdigest()}
 except Exception as e:return {'platform':k,'file':f,'url':b+f,'error':type(e).__name__}
with concurrent.futures.ThreadPoolExecutor(max_workers=8)as ex:rows=list(ex.map(verify,[(k,b,f)for k,b in bases.items()for f in files]))
for i,r in enumerate(rows):
 if 'error'in r:rows[i]=verify((r['platform'],bases[r['platform']],r['file']))
out={'edition':'heidelberg-52-20261021-v1-GTstudy','version':'1.0.0','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'repository':'https://github.com/07-Je-GT-Love-Personal-20260918/heidelberg-52-20261021-v1-GTstudy','urls':bases,'results':rows,'summary':{k:{'checked':len(files),'ok':sum(r.get('status')==200 for r in rows if r['platform']==k),'matches_local':sum(r.get('matches_local',False)for r in rows if r['platform']==k)}for k in bases},'limits':['CCI live recheck:227 of232 sections verified; three pages with five sections unavailable due TLS/timeout.','Vercel direct deployment succeeds; GitHub automatic project connection unavailable.']}
(R/'deployment.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out['summary']))
