from pathlib import Path
import json,hashlib,re,concurrent.futures,datetime
import requests
from bs4 import BeautifulSoup
R=Path(__file__).parent
data=json.loads((R/'content/fulltexts.json').read_text(encoding='utf-8'))
data['meta'].pop('permission',None)
data['meta']['usage']='指定中文译本；源于用户提供PDF所对应的CCI网页。版权归原权利人；本项目不宣称译文采用开源许可。'
(R/'content/fulltexts.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
sections=[s for d in data['documents'] for s in d['sections']]
def norm(t):return re.sub(r'\s+','',t)
def check(url):
 try:
  r=requests.get(url,timeout=35);r.raise_for_status()
  soup=BeautifulSoup(r.content,'html.parser')
  text=norm(soup.get_text())
  items=[s for s in sections if s['source']==url]
  return {'url':url,'status':r.status_code,'sections':len(items),'matches':[{'title':s['title'],'exact_nonwhitespace':norm(s['text']) in text,'sha256':hashlib.sha256(s['text'].encode()).hexdigest()} for s in items]}
 except Exception as e:return {'url':url,'error':type(e).__name__}
urls=sorted(set(s['source'] for s in sections))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:results=list(ex.map(check,urls))
for i,r in enumerate(results):
 if 'error' in r:results[i]=check(r['url'])
report={'checked':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Live requests; cached text must appear contiguously in page after removing Unicode whitespace; words and punctuation unchanged. Hashes over cached UTF-8 text.','results':results}
report['summary']={'urls':len(urls),'sections':len(sections),'matched':sum(m['exact_nonwhitespace'] for r in results for m in r.get('matches',[])),'errors':sum('error'in r for r in results)}
(R/'qa/source-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report['summary']))
