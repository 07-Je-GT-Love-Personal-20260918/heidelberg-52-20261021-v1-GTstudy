from pathlib import Path
from html import escape as E
import json,shutil,re,hashlib
R=Path(__file__).parent; O=R/'dist';O.mkdir(exist_ok=True)
data=json.loads((R/'content/fulltexts.json').read_text(encoding='utf-8'))
docs={d['key']:d for d in data['documents']}
lessons=[dict(zip(['n','title','q','bible','setting','argument','covenant','refs','application','memory','review'],line.split('|'))) for line in (R/'content/lessons.txt').read_text(encoding='utf-8').splitlines() if line]
assert len(lessons)==52
for i,l in enumerate(lessons,1):assert int(l['n'])==i and all(l.values())
for d in docs.values():
 for s in d['sections']:assert hashlib.sha256(s['text'].encode()).hexdigest()==s['sha256']
places=[['耶路撒冷',31.78,35.23,'希伯来—亚兰语犹太文化与希腊语、罗马治理交织。圣殿、逾越节、受难复活与五旬节的历史中心；主日15–21。'],['拿撒勒',32.70,35.30,'加利利犹太城镇，耶稣成长的环境；不可把现代城景当作一世纪完整复原。主日14。'],['尼西亚',40.43,29.72,'今土耳其伊兹尼克。325年会议聚集于罗马帝国东部，争论子与父的关系；希腊语同质措辞回应亚流争议。'],['君士坦丁堡',41.01,28.98,'今伊斯坦布尔。381年会议与尼西亚信仰的进一步确认相连；须区分历史会议、文本流传与后来的西方添加。'],['罗马',41.90,12.50,'拉丁西方受洗宣认发展中的重要中心，古罗马信条是理解使徒信经形成的重要见证。不能把逐步发展缩为单日创作。'],['海德堡',49.41,8.71,'内卡河畔，神圣罗马帝国普法尔茨选帝侯领地。1563年教会、大学、学校的教导需要促成要理；受教者不只是大学学者。'],['低地国家／多特',51.81,4.67,'今荷兰多德雷赫特。荷语传播、改革宗教会秩序与抗辩派争论相连；1618–1619国际性会议形成多特信经。'],['日内瓦',46.20,6.14,'法语改革宗的翻译、讲道与诗篇歌唱网络，对欧洲传播具有重要影响；不能因此把海德堡写作地点改成日内瓦。']]
def xy(lon,lat):return (lon+15)*14,(60-lat)*17
geo=json.loads((R/'content/countries.json').read_text(encoding='utf-8'))
paths=[]
for f in geo['features']:
 g=f['geometry']; polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
 for poly in polys:
  if not any(-18<x<43 and 25<y<61 for x,y,*_ in poly[0]):continue
  path=' '.join(('M' if j==0 else 'L')+f'{xy(pt[0],pt[1])[0]:.1f},{xy(pt[0],pt[1])[1]:.1f}' for j,pt in enumerate(poly[0]))+' Z'
  paths.append(f'<path d="{path}"/>')
markers=[]
for i,(name,lat,lon,desc) in enumerate(places):
 x,y=xy(lon,lat)
 if i==1:x+=20;y-=9
 if i==3:x-=23;y-=12
 markers.append(f'<g class="map-pin" data-place="{i}" tabindex="0" role="button" aria-label="{E(name)}"><circle cx="{x}" cy="{y}" r="13"/><text x="{x}" y="{y+5}" text-anchor="middle">{i+1}</text><title>{E(name)}</title></g>')
maphtml='<figure class="map"><svg viewBox="0 0 810 590" role="img" aria-label="欧洲与东地中海教学地图"><defs><clipPath id="map-clip"><rect width="810" height="590" rx="20"/></clipPath></defs><g clip-path="url(#map-clip)"><rect class="sea" width="810" height="590"/><g class="land">'+''.join(paths)+'</g><text x="400" y="450" class="sea-label">地 中 海</text>'+''.join(markers)+'</g></svg><figcaption>底图：Natural Earth 1:110m 公版地理数据；编号对应下方地点。为避免遮挡，邻近标记略有偏移。</figcaption></figure>'
head='''<!doctype html><html lang="zh-Hans"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><meta name="description" content="海德堡要理问答52主日与129问完整深读，欧陆改革宗、圣经神学与圣约神学，地图时间线与三经背诵。"><title>{title} · GTstudy</title><link rel="icon" href="favicon.svg"><link rel="stylesheet" href="style.css"><script src="init.js"></script><script src="app.js" defer></script></head><body><a class="skip" href="#main">跳到正文</a><div class="read-progress" id="read-progress"></div><header><a class="brand" href="index.html">✦ GTstudy <span>海德堡 · 52 主日</span></a><div class="tools"><button id="toc-toggle" aria-expanded="true" aria-controls="toc">☰ 目录</button><button id="theme" aria-label="切换夜间阅读">◐ 夜读</button><button id="font-down" aria-label="缩小字体">A−</button><button id="font-up" aria-label="放大字体">A＋</button><button id="motion">◈ 动效</button></div></header>'''
foot='''<footer><p>HEIDELBERG · 52 LORD’S DAYS · CONTINENTAL REFORMED</p><p>2026-10-21 · v1.0.0 · GTstudy<br>从属于基督的安慰，走向感恩与祷告。</p><a href="index.html#sources">来源与版本</a> · <a href="#main">返回顶部 ↑</a></footer><div id="toast" role="status"></div></body></html>'''
def shell(title,body,nav=''):
 return head.replace('{title}',E(title))+'<div class="page-layout"><aside id="toc"><h2>学习导航</h2><input id="nav-search" type="search" placeholder="查找目录标题…" aria-label="查找目录标题"><nav>'+nav+'</nav><a href="library.html">↗ 六份原典</a><p class="caption">纸页白 · 松针绿 · 琥珀金<br>全文平铺，可用浏览器查找</p></aside><main id="main">'+body+'</main></div>'+foot
overview=(R/'content/overview.html').read_text(encoding='utf-8').replace('{{MAP}}',maphtml).replace('{{PLACE_BUTTONS}}',''.join(f'<button data-place="{i}">{i+1} {E(p[0])}</button>' for i,p in enumerate(places)))
nav=''.join(f'<a href="#{a}">{b}</a>' for a,b in [('whole','01 整本圣经'),('covenant','02 圣约主轴'),('history','03 双时间线与故事'),('geography','04 地图与文化'),('compare','05 三经深度比较'),('memory','06 记忆与背诵'),('lessons','07 52主日逐课深读'),('sources','08 来源与核验')])
hero='''<section class="hero"><div class="hero-copy"><div class="eyebrow">THE HEIDELBERG CATECHISM · AN ANNOTATED JOURNEY</div><p class="edition">2026.10.21 / V1 · 欧陆改革宗学习书</p><h1>生死之间，<br>有一个<span>永恒的归属。</span></h1><p class="hero-sub">海德堡要理问答 · 52 个主日完整深读</p><p>沿着整本圣经的故事，从创造走到新创造。<br>看见信经背后的历史，让教义成为可以理解、记住和活出的安慰。</p><div class="hero-links"><a class="primary button" href="#day-1">从第一主日开始 ↗</a><a class="button" href="#whole">先看全书主线 ↓</a></div><div class="stats"><span><b>52</b> 主日</span><span><b>129</b> 问答</span><span><b>6</b> 认信原典</span><span><b>1</b> 救赎主线</span></div></div><figure class="hero-art"><img src="journey.svg" alt="从创造、应许、十架与复活到新创造的原创救恩历史路径图"><figcaption>应许在历史中展开，安慰在基督里扎根。</figcaption></figure></section>'''
def refs_html(refs):
 return E(refs)+' · <a href="library.html#belgic">比利时全文</a> · <a href="library.html#dort">多特全文</a>'
chapters=['<section id="lessons"><span class="eyebrow">07 · THE COMPLETE 52 LORD’S DAYS</span><h2>每一个主日，沿同一福音继续走</h2><p>以下129问正式正文全部展开。绿色边框标识指定原文；其他段落为原创教学解读。每课先读圣经上下文，再读原文与解析，不以记忆句代替完整内容。</p><div class="day-grid">'+''.join(f'<a href="#day-{l["n"]}" title="{E(l["title"])}">{l["n"]}</a>' for l in lessons)+'</div></section>']
counts=[]
for l in lessons:
 n=int(l['n']); ss=[s for s in docs['heidelberg']['sections'] if s['lord_day']==n]
 group='序言 · 唯一安慰' if n==1 else '第一部 · 罪与苦' if n<=4 else '第二部 · 拯救' if n<=31 else '第三部 · 感恩'
 nav+=f'<a class="day-link" href="#day-{n}"><span>{n:02d}</span> {E(l["title"])}</a>'
 original=''.join(f'<article class="original-text" data-q="{s["title"].split("．")[0].split(".")[0]}">{s["html"]}<p class="source-line"><a href="{E(s["source"])}">CCI此问正文 ↗</a> · 指定中文译文 · SHA-256 {s["sha256"][:12]}…</p></article>' for s in ss)
 # In Bible-text layout, preserve each source HTML fragment and its footnote numbering.
 parts=[f'<section class="lesson" id="day-{n}"><div class="lesson-label"><span>{E(group)}</span><span>LORD’S DAY {n:02d}</span></div><h2><span class="day-num">{n:02d}</span> {E(l["title"])}</h2><p class="lesson-meta">问答 {E(l["q"])} · <a href="day-{n:02d}.html">本课独立阅读 ↗</a></p>',f'<div class="bible"><b>📖 先读经文上下文</b><p>{E(l["bible"])}</p></div>',f'<h3>① 回到真实情境</h3><p>{E(l["setting"])}</p>',f'<div class="source-box"><div class="eyebrow">CCI 指定中文原文 · 全部展开</div>{original}</div>',f'<h3>② 本质与论证：为什么这样回答</h3><p>{E(l["argument"])}</p>',f'<h3>③ 放回圣经与圣约主线</h3><p>{E(l["covenant"])}</p><p class="cross-ref"><b>信条互证 · 条号索引，非逐字引用</b><br>{refs_html(l["refs"])}</p>',f'<div class="application"><h3>④ 今天如何回应</h3><p>{E(l["application"])}</p></div><div class="recall"><span>✦ 一句话记住 · 原创概括</span><p>{E(l["memory"])}</p><b>合上内容，试着回答：</b><p>{E(l["review"])}</p></div>',f'<div class="lesson-tools"><label><input type="checkbox" class="complete" data-day="{n}"> 本课已读并回忆</label><a href="https://ccifellowship.org/books/i-belong">CCI逐主日扩展目录 ↗</a></div><label class="note-label" for="note-{n}">我的课堂笔记</label><textarea id="note-{n}" data-note="{n}" placeholder="一个因果关系、一处疑问、一个行动…" rows="3"></textarea><p class="caption">笔记只存于此浏览器，可在记忆模块导出。</p></section>']
 chapter=''.join(parts);chapters.append(chapter);counts.append(len(ss))
 (O/f'day-{n:02d}.html').write_text(shell(f'主日{n} · {l["title"]}',f'<p><a href="index.html#day-{n}">← 返回完整课程</a></p>'+chapter+f'<div class="reader-nav">'+(f'<a href="day-{n-1:02d}.html">← 上一主日</a>'if n>1 else '')+(f'<a href="day-{n+1:02d}.html">下一主日 →</a>'if n<52 else '')+'</div>', '<a href="index.html">完整学习网站</a>'+''.join(f'<a href="day-{j:02d}.html">主日 {j:02d}</a>' for j in range(1,53))),encoding='utf-8')
assert sum(counts)==129
# Keep the sources section at the end, after the full course.
before,sources=overview.split('<section id="sources">',1)
(O/'index.html').write_text(shell('海德堡52主日 · 生死属于基督',hero+before+''.join(chapters)+'<section id="sources">'+sources,nav),encoding='utf-8')
lib=[];libnav=''
for k,d in docs.items():
 libnav+=f'<a href="#{k}">{E(d["title"])}</a>'
 lib.append(f'<section id="{k}"><div class="eyebrow">指定中文正文</div><h1>{E(d["title"])}</h1><p><a href="{E(d["source"])}">CCI原站目录 ↗</a></p>')
 for i,s in enumerate(d['sections'],1):lib.append(f'<article class="source-box" id="{k}-{i}"><h2>{E(s["title"])}</h2><div class="original-text">{s["html"]}</div><p class="source-line"><a href="{E(s["source"])}">原站此节 ↗</a></p></article>')
 lib.append('</section>')
 if k in ['apostles','nicene','athanasian']:
  body=f'<section class="clean"><span class="eyebrow">CREDO · 干净阅读与背诵</span><h1>{E(d["title"])}</h1><p class="clean-tools"><a href="index.html#compare">← 回到三经比较</a> <button onclick="window.print()">打印干净版</button></p><div class="original-text">{d["sections"][0]["html"]}</div><p class="source-line">指定中文译文：<a href="{E(d["source"])}">CCI《敬拜手册》</a>。仅调整布局，保留原字词、标点、段号与脚注。核验见<a href="source-audit.json">报告</a>。</p></section>'
  (O/f'reader-{k}.html').write_text(shell(d['title'],body,'<a href="index.html#memory">记忆工坊</a><a href="reader-apostles.html">使徒信经</a><a href="reader-nicene.html">尼西亚信经</a><a href="reader-athanasian.html">亚他那修信经</a>'),encoding='utf-8')
(O/'library.html').write_text(shell('六份认信原典','<p class="insight">本页完整平铺六份指定文本。原文指CCI中文译文，不是古代语言原典；译文版权归原权利人。</p>'+''.join(lib),libnav),encoding='utf-8')
for f in ['style.css','app.js','init.js','journey.svg','favicon.svg'] :shutil.copyfile(R/f,O/f)
shutil.copyfile(R/'content/fulltexts.json',O/'fulltexts.json')
if (R/'qa/source-audit.json').exists():shutil.copyfile(R/'qa/source-audit.json',O/'source-audit.json')
(O/'places.json').write_text(json.dumps(places,ensure_ascii=False),encoding='utf-8')
(O/'creeds.json').write_text(json.dumps({k:docs[k]['sections'][0]['html'] for k in ['apostles','nicene','athanasian']},ensure_ascii=False),encoding='utf-8')
(O/'lessons.json').write_text(json.dumps(lessons,ensure_ascii=False),encoding='utf-8')
(O/'.nojekyll').write_text('')
(R/'qa/build-report.json').write_text(json.dumps({'lessons':52,'questions':sum(counts),'documents':6,'source_units':sum(len(d['sections']) for d in docs.values()),'html_pages':len(list(O.glob('*.html'))),'original_analysis_characters':sum(len(''.join(l.values())) for l in lessons)},ensure_ascii=False,indent=2),encoding='utf-8')
print('Built 57 HTML pages; 52 lessons; 129 questions; 232 source units.')
