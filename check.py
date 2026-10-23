from pathlib import Path
from urllib.parse import urlsplit,unquote
from bs4 import BeautifulSoup
import json,re
R=Path(__file__).parent;D=R/'dist';errors=[]
soups={p.name:BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')for p in D.glob('*.html')}
anchors={name:{e['id']for e in soup.select('[id]')}for name,soup in soups.items()}
for name,s in soups.items():
 ids=[e['id']for e in s.select('[id]')]
 if len(ids)!=len(set(ids)):errors.append([name,'duplicate ids'])
 for e in s.select('a[href],img[src],script[src],link[href]'):
  u=urlsplit(e.get('href',e.get('src','')))
  if u.scheme or u.netloc:continue
  target=unquote(u.path)or name
  if not(D/target).exists():errors.append([name,'missing file',target])
  elif u.fragment and target in soups and unquote(u.fragment) not in anchors[target]:errors.append([name,'missing anchor',target,u.fragment])
 # Credentials must never appear in source/public artifacts.
for p in R.rglob('*'):
 if not p.is_file()or any(x in p.parts for x in ['.git','.vercel','__pycache__']):continue
 if p.suffix not in ['.html','.js','.json','.md','.txt','.yml','.py','.css']:continue
 t=p.read_text(encoding='utf-8')
 if re.search(r'github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{25,}',t):errors.append([str(p.relative_to(R)),'credential pattern'])
assert len(soups['index.html'].select('.lesson'))==52
assert len(soups['index.html'].select('.lesson .source-unit'))==129
source_data=json.loads((R/'content/fulltexts.json').read_text(encoding='utf-8'))
source_checked=0
for doc in source_data['documents']:
 for i,section in enumerate(doc['sections'],1):
  el=soups['library.html'].select_one(f'#source-{doc["key"]}-{i} .original-text')
  norm=lambda t:re.sub(r'\s+','',t)
  if el is None or norm(el.get_text())!=norm(section['text']):errors.append(['library.html','source text differs',doc['key'],i])
  source_checked+=1
report={'pages':len(soups),'local_links_checked':sum(len(s.select('a[href]'))for s in soups.values()),'source_units_checked':source_checked,'errors':errors,'note':'Browser responsive and interaction tests are recorded separately.'}
(R/'qa/static-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=True));assert not errors
