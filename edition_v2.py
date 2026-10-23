"""The complete V2 reader. Source text is immutable; annotations are browser overlays."""
from pathlib import Path
from html import escape as E
import json,re,shutil,hashlib
VERSION='2.0.0'; EDITION='heidelberg-52-20261023-v2-GTstudy'
REPO='https://github.com/07-Je-GT-Love-Personal-20260918/heidelberg-52-GTstudy'
PATHS={'book':'M4 5h6a3 3 0 0 1 3 3v13a4 4 0 0 0-4-2H4z M22 5h-6a3 3 0 0 0-3 3v13a4 4 0 0 1 4-2h5z','spark':'m13 2 3 8 8 3-8 3-3 8-3-8-8-3 8-3z','map':'m3 6 6-3 8 3 6-3v17l-6 3-8-3-6 3z M9 3v17 M17 6v17','clock':'M13 7v6l4 3 M23 13a10 10 0 1 1-20 0 10 10 0 0 1 20 0','link':'m10 16 6-6 M8 18l-2 2a4 4 0 0 1-5-5l5-5a4 4 0 0 1 5 0 M18 8l2-2a4 4 0 0 0-5-5l-5 5a4 4 0 0 0 0 5','layers':'m13 2 11 6-11 6L2 8z M2 13l11 6 11-6 M2 18l11 6 11-6','pen':'m4 18-1 6 6-1L23 9l-5-5z M15 7l5 5','search':'M19 19l6 6 M21 11a10 10 0 1 1-20 0 10 10 0 0 1 20 0','moon':'M22 16A10 10 0 0 1 10 3a10 10 0 1 0 12 13','sun':'M13 1v3 M13 22v3 M1 13h3 M22 13h3 M4 4l2 2 M20 20l2 2 M4 22l2-2 M20 6l2-2 M18 13a5 5 0 1 1-10 0 5 5 0 0 1 10 0','menu':'M3 6h20 M3 13h20 M3 20h20','arrow':'M4 13h18 M15 6l7 7-7 7','heart':'M13 23 3 13C-4 4 7-3 13 6c6-9 17-2 10 7z','shield':'m13 2 10 4v7c0 6-10 11-10 11S3 19 3 13V6z M8 13l3 3 7-7','key':'M16 9a6 6 0 1 1-12 0 6 6 0 0 1 12 0 M14 14l10 10 M19 19l3-3','cross':'M13 2v23 M4 9h18','leaf':'M4 22C0 3 11 2 24 2c0 14-4 24-20 20z M4 22 19 7','brain':'M13 23V4c-5-6-12 2-7 7-8 5-1 16 7 9 M13 4c5-6 12 2 7 7 8 5 1 16-7 9 M7 11l6 4 M20 11l-7 4','volume':'M3 9h5l7-6v20l-7-6H3z M19 8c4 3 4 7 0 10 M22 4c7 5 7 13 0 18','check':'m4 13 6 6L23 5','question':'M9 8c0-6 10-6 10 0 0 4-6 3-6 8 M13 21v1 M25 13A12 12 0 1 1 1 13a12 12 0 0 1 24 0','compare':'M13 3v21 M3 8h20 M3 8l-3 8h6z M23 8l-3 8h6z','flag':'M5 25V3c8-5 11 6 19 0v13c-8 6-11-5-19 0','quote':'M3 17c0-8 0-11 8-12v6H6v6h5v7H3z M16 17c0-8 0-11 8-12v6h-5v6h5v7h-8z'}
def icon(name,cls=''):
 return f'<svg class="ico {cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'
def symbols():return '<svg class="icon-defs" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"><defs>'+''.join(f'<symbol id="i-{k}" viewBox="-1 -1 29 29"><path d="{v}"/></symbol>'for k,v in PATHS.items())+'</defs></svg>'
def markable(html,key):
 count=[0]
 def sub(m):
  count[0]+=1
  return f'<{m[1]}{m[2] or ""} data-mark-key="{E(key)}:{count[0]}">{m[3]}</{m[1]}>'
 return re.sub(r'<(p|h[1-6])(\s[^>]*)?>(.*?)</\1>',sub,html,flags=re.S)
def para(t,key='',cls=''):
 return f'<p'+(f' data-mark-key="{E(key)}"'if key else '')+(f' class="{cls}"'if cls else '')+'>'+E(t)+'</p>'
def part(n):return ('intro','总纲','安慰')if n==1 else ('misery','第一部','罪苦')if n<5 else ('grace','第二部','拯救')if n<32 else ('thanks','第三部','感恩')
def chip(text,kind=''):return f'<span class="chip {kind}">{text}</span>'
def original(doc,s,i):
 key=f'original:{doc}:{i}'
 return f'<article class="source-unit" id="source-{doc}-{i}"><div class="original-text">{markable(s["html"],key)}</div><div class="source-foot"><a href="{E(s["source"])}" target="_blank" rel="noopener">{icon("link")} CCI原文</a><span>指定中文译文 · 已逐字核验</span></div></article>'
def upgrade(R,O,data,lessons,maphtml,places):
 docs={d['key']:d for d in data['documents']};deep={}
 for f in ['deep-1-26.json','deep-27-52.json']:
  if (R/'content'/f).exists():
   items=json.loads((R/'content'/f).read_text(encoding='utf-8'))
   if isinstance(items,dict):items=items.get('lessons',list(items.values()))
   for item in items:deep[int(item['day'])]=item
 common_nav=[('index.html#whole','book','整本圣经'),('index.html#covenant','link','圣约主线'),('history.html','map','历史与地图'),('index.html#lessons','layers','52主日'),('forms.html','compare','三信条对比'),('library.html','book','六份原典'),('memory.html','brain','记忆工坊')]
 course_nav=''.join(f'<a href="index.html#day-{l["n"]}" class="day-link {part(int(l["n"]))[0]}" data-nav-day="{l["n"]}"><span>{int(l["n"]):02d}</span><b>{E(l["title"])}</b></a>'for l in lessons)
 header=f'''<a class="skip" href="#main">跳到正文</a>{symbols()}<div id="reading-line"></div><header class="topbar"><button id="toc-toggle" class="icon-button" aria-label="显示或隐藏目录" aria-controls="toc" aria-expanded="true">{icon('menu')}</button><a href="index.html" class="brand"><span class="brand-icon">{icon('book')}</span><span>海德堡 <b>52</b><small>GTstudy · 欧陆改革宗</small></span></a><nav class="top-nav"><a href="index.html#lessons">逐课深读</a><a href="forms.html">三项信条</a><a href="memory.html">记忆工坊</a></nav><div class="header-tools"><button id="search-open" aria-label="全文搜索">{icon('search')}<span>搜索</span><kbd>/</kbd></button><button id="notes-open" aria-label="打开标记与笔记">{icon('pen')}<span>我的标记</span><b id="mark-count">0</b></button><button id="theme" class="icon-button" aria-label="切换夜间阅读">{icon('moon')}</button><details class="settings"><summary aria-label="阅读设置">Aa</summary><div class="settings-panel"><b>阅读设置</b><div class="font-controls"><button id="font-down">A−</button><span id="font-value">21</span><button id="font-up">A＋</button></div><p>配色</p><div class="palette-options">{''.join(f'<button data-palette="{k}" title="{name}" aria-label="{name}"><i style="background:{col}"></i></button>'for k,name,col in [('cloud','云海蓝','#5479ca'),('jade','竹影青','#268677'),('violet','紫藤暮色','#8c63bb'),('amber','晨光琥珀','#b57b2d'),('rose','蔷薇暖调','#b75c7a')])}</div><button id="motion">动效：开</button><button id="marks-toggle">个人标记：显示</button></div></details></div></header>'''
 aside=f'''<aside id="toc"><div class="toc-head"><span>CONTENTS</span><strong>阅读地图</strong><input id="nav-search" type="search" aria-label="过滤目录" placeholder="筛选主日、主题…"></div><nav class="global-nav">{''.join(f'<a href="{u}">{icon(i)}{n}</a>'for u,i,n in common_nav)}</nav><div class="toc-course-title"><b>52 主日</b><a href="index.html#lessons">全景</a></div><nav class="course-nav">{course_nav}</nav><div class="toc-footer"><span>颜色记忆</span><div><i class="dot intro"></i>总纲 <i class="dot misery"></i>罪苦 <i class="dot grace"></i>拯救 <i class="dot thanks"></i>感恩</div><a href="index.html#sources">来源 · 版本 · 校验</a></div></aside>'''
 dialogs=(R/'v2-dialogs.html').read_text(encoding='utf-8')
 def page(title,body,pageid='index',clean=False):
  if pageid!='index':body=re.sub(r'href="#(day-\d+)"',r'href="index.html#\1"',body)
  return f'''<!doctype html><html lang="zh-Hans"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><meta name="description" content="海德堡52主日、129问完整深读。经文论证、圣约主线、三项信条比较、地图与个人重点标记。"><title>{E(title)} · 海德堡52 · GTstudy</title><link rel="icon" href="favicon.svg"><link rel="stylesheet" href="reader.css"><script src="reader-init.js"></script><script src="reader.js" defer></script><script src="annotations.js" defer></script></head><body data-page="{pageid}" class="{'clean-mode'if clean else ''}">{header}<div class="reading-shell">{aside}<main id="main">{body}</main></div><footer class="site-footer"><div>{icon('book')} 海德堡 52 · GTstudy</div><p>2026.10.23 · v2.0.0 · 生死属于基督，生活出于感恩。</p><a href="{REPO}">源码与版本</a> · <a href="index.html#sources">来源说明</a> · <a href="#main">返回顶部 ↑</a></footer>{dialogs}<div id="toast" role="status" hidden></div></body></html>'''
 def section(id,title,body,eyebrow='',cls=''):
  return f'<section id="{id}" class="reading-section {cls}"><div class="section-title"><div class="eyebrow">{eyebrow}</div><h2>{title}</h2></div>{body}</section>'
 fragments={}
 overview=(R/'content/overview.html').read_text(encoding='utf-8')
 for frag in re.split(r'(?=<section id=")',overview):
  m=re.match(r'<section id="([^"]+)"',frag)
  if m:fragments[m[1]]=frag
 # Restore the immutable map built by the original edition, with exact geography.
 history=fragments['history']+fragments['geography'].replace('{{MAP}}',maphtml).replace('{{PLACE_BUTTONS}}',''.join(f'<button data-place="{i}">{i+1} {E(p[0])}</button>'for i,p in enumerate(places)))
 history=markable(history,'overview:history')
 # First-person teaching scene and an explicit causal diagram precede the course.
 lens=(R/'content/v2-overview.html').read_text(encoding='utf-8')
 blocks=[2,9,74,44]; labels=['总纲','罪苦','拯救','感恩']; kinds=['intro','misery','grace','thanks']
 donut='<svg viewBox="0 0 240 240" class="donut" role="img" aria-label="129问分布：总纲2、罪苦9、拯救74、感恩44"><circle cx="120" cy="120" r="89" class="donut-track" fill="none" stroke-width="24"/>'
 offset=0
 for v,k in zip(blocks,kinds):
  circumference=559.2035;length=v/129*circumference
  donut+=f'<circle cx="120" cy="120" r="89" class="donut-segment {k}" fill="none" stroke-width="24" stroke-dasharray="{length:.3f} {circumference-length:.3f}" stroke-dashoffset="{-offset:.3f}" transform="rotate(-90 120 120)"/>';offset+=length
 donut+='<text x="120" y="119" class="donut-total" text-anchor="middle">129</text><text x="120" y="146" class="donut-caption" text-anchor="middle">问答 · 一条福音主线</text></svg>'
 bars=''.join(f'<a class="day-bar {part(int(l["n"]))[0]}" href="#day-{l["n"]}" style="--bar:{len([s for s in docs["heidelberg"]["sections"]if s["lord_day"]==int(l["n"])])/5*100}%" title="主日{l["n"]} · {E(l["title"])}"><span>{len([s for s in docs["heidelberg"]["sections"]if s["lord_day"]==int(l["n"])])}</span><i></i><small>{l["n"]}</small></a>'for l in lessons)
 structure=section('structure','全书的重心：从罪苦进入丰盛的恩典',f'<div class="structure-grid"><div class="donut-card">{donut}<ul class="chart-legend">'+''.join(f'<li><i class="dot {k}"></i><b>{lab}</b><span>{v} 问</span><small>{v/129*100:.1f}%</small></li>'for v,lab,k in zip(blocks,labels,kinds))+'</ul></div><div class="structure-copy"><p class="key-statement" data-mark-key="overview:structure:1">安慰是总论题；罪苦揭露需要，拯救展开基督，感恩显出救恩的果子。</p><div class="triad"><a class="misery" href="#day-2">'+icon('shield')+'<b>罪苦</b><span>主日2–4 · 问3–11</span><small>律法如镜，照见我的真实处境。</small></a><a class="grace" href="#day-5">'+icon('cross')+'<b>拯救</b><span>主日5–31 · 问12–85</span><small>基督成就，圣灵使我分享。</small></a><a class="thanks" href="#day-32">'+icon('leaf')+'<b>感恩</b><span>主日32–52 · 问86–129</span><small>先蒙恩，后以爱与祷告回应。</small></a></div><p class="caption">图表按129问实际计数；主日1的2问为总纲。比例仅说明篇幅，不等同各教义的重要程度。</p></div></div><div class="bar-card"><h3>52个主日，各有多长？</h3><div class="day-bars">'+bars+'</div><p class="caption">每柱代表该主日问答数，点按直接进入课程。手机可横向浏览本图。</p></div>','01 / THE ARCHITECTURE')
 hero=f'''<section class="hero-v2"><div class="hero-orbit orbit-one"></div><div class="hero-orbit orbit-two"></div><div class="hero-copy"><div class="hero-chips">{chip('1563 · Heidelberg','intro')}{chip('欧陆改革宗','grace')}{chip('2026.10.23 · V2','thanks')}</div><div class="eyebrow">THE HEIDELBERG CATECHISM</div><h1>读懂<span>唯一的安慰。</span><small>海德堡要理问答 · 52主日深读</small></h1><p class="hero-lead">把整本圣经的故事，读成可以记住的信仰骨架；<br>再进入每一问的经文、逻辑与生活。</p><div class="hero-actions"><a class="button primary" href="#day-1">{icon('book')} 开始第一主日 {icon('arrow')}</a><a class="button soft" href="#whole">先看圣经与圣约</a></div><div class="hero-facts"><span><b>52</b> 主日</span><span><b>129</b> 问答</span><span><b>6</b> 认信文本</span><span><b>232</b> 原文单元核验</span></div></div><div class="hero-insight"><span class="mini-label">一本书，回答三件事</span><div class="hero-path"><a href="#day-2" class="misery">{icon('shield')}<span><small>认识处境</small><b>我的罪苦有多深？</b></span><i>01</i></a><a href="#day-5" class="grace">{icon('cross')}<span><small>认识救主</small><b>基督怎样拯救我？</b></span><i>02</i></a><a href="#day-32" class="thanks">{icon('leaf')}<span><small>回应恩典</small><b>我怎样感恩而活？</b></span><i>03</i></a></div><p>不是三条得救道路，而是同一恩典的<br><b>需要、成就与果子。</b></p></div></section>'''
 forms=(R/'content/v2-forms.html').read_text(encoding='utf-8');forms=markable(forms,'overview:forms')
 memory=(R/'content/v2-memory.html').read_text(encoding='utf-8');memory=markable(memory,'overview:memory')
 readers='<div class="reader-links">'+''.join(f'<a href="reader-{k}.html">{icon("book")}<b>{E(docs[k]["title"])}</b><span>干净版 · 背诵 · 打印 {icon("arrow")}</span></a>'for k in ['apostles','nicene','athanasian'])+'</div>'
 memory=memory.replace('{{READERS}}',readers)
 memory=memory.replace('<div class="flashcard-studio">',(R/'content/v2-mindmap.html').read_text(encoding='utf-8')+'<div class="flashcard-studio">')
 sources=section('sources','文本有来处，解释有边界',f'''<p data-mark-key="overview:sources:1">六份正式中文文本均取自CCI《敬拜手册》的指定网页。2026年10月23日独立联网复核155个来源页，232个正文单元全部匹配；只忽略排版空白，字词、标点、段号与脚注均保留。这里的“原文”指指定中文译文。</p><div class="source-metrics"><span>{icon('check')} 155 / 155 来源页</span><span>{icon('check')} 232 / 232 正文单元</span><a href="source-audit.json">查看核验记录 ↗</a></div><div class="source-columns"><div><h3>正式文本</h3><p><a href="https://ccifellowship.org/books/book-of-praise">CCI《敬拜手册》</a> · <a href="library.html">本站六份全文</a>。译文版权归原权利人。个人标记仅改变浏览器显示，不改写正式文本。附带PDF只读参考，不公开上传。</p></div><div><h3>逐课扩展</h3><p>每课给出实际核实的CCI《I Belong》对应入口，并以<a href="https://canrc.org/heidelberg-catechism">CanRC</a>及相关正式信条互证。<a href="cci-expansion.json">栏目研究范围</a>记录实际访问；不把有限研究说成通读CCI全站。</p></div><div><h3>教义取向</h3><p>以三项联合信条共同教导为主轴。<a href="https://www.urcna.org/">URCNA</a>、<a href="https://heritagereformed.com/">HRC</a>、<a href="https://www.prca.org/">PRCA</a>在若干圣约用语上有差异，须定义术语再比较；不把某一支派全部主张强作共识。</p></div><div><h3>继续研究</h3><p><a href="https://www.ccreformed.org/">恩约教会</a> · <a href="https://www.reformedbeginner.net/">改革宗初学者</a> · <a href="https://opc.org/">OPC</a> · <a href="https://www.wts.edu/">WTS</a> · <a href="https://canadianreformedseminary.ca/">CRTS</a>。作为进阶资源入口，不冒称已综合其全部课程与文章。</p></div></div><p class="caption">历史图使用Natural Earth公版现代底图，坐标近似，不代表古代疆界。原创解读与正式原文分别标识；经文索引供回到上下文细读。</p><p><a href="{REPO}">已有仓库 · 历史与版本 ↗</a> · <a href="{REPO}/releases">恢复包 ↗</a></p>''','09 / SOURCES & VERIFICATION')
 chapters=[];search=[];flash=[];original_map={}
 for l in lessons:
  n=int(l['n']);kind,partname,label=part(n);d=deep.get(n)
  if not d:d={'thesis':l['memory'],'exegesis':l['argument'],'chain':[l['setting'],l['covenant'],l['application']],'distinction':{'left':'救恩的根基','right':'恩典的回应','boundary':l['covenant']},'difficult':{'q':l['review'],'a':l['argument']},'scene':{'title':l['title'],'body':l['setting'],'ref':l['bible']},'links':['https://canrc.org/heidelberg-catechism'],'memory':l['memory']}
  ss=[(i,s)for i,s in enumerate(docs['heidelberg']['sections'],1)if s['lord_day']==n]
  originals=''.join(original('heidelberg',s,i)for i,s in ss)
  for i,s in ss:original_map[f'original:heidelberg:{i}']=f'day-{n}'
  chain='<ol class="causal-chain">'+''.join(f'<li><span>{i}</span>{para(t,f"day:{n}:chain:{i}")}</li>'for i,t in enumerate(d['chain'],1))+'</ol>'
  chain='<div class="logic-controls"><span>全部理由已展开；点按依次跟随。</span><button data-logic-step>逐步推演 →</button></div>'+chain
  concept=f'<div class="concept-contrast"><span>{E(d["distinction"]["left"])}</span><b>≠</b><span>{E(d["distinction"]["right"])}</span></div>'+para(d['distinction']['boundary'],f'day:{n}:distinction')
  idx=26 if n in [26,27]else n
  cci='26-27'if n in [26,27]else '28-29-30'if n in[28,29,30]else '36-37'if n in[36,37]else str(n)
  links=list(dict.fromkeys(['https://ccifellowship.org/books/i-belong/'+cci]+d.get('links',[])))
  chapter=f'''<section class="lesson reading-section {kind}" id="day-{n}" data-day="{n}"><div class="lesson-heading"><div><div class="eyebrow">{partname} / {label} · 问{E(l['q'])}</div><h2><span class="day-number">{n:02d}</span>{E(l['title'])}</h2></div><a href="day-{n:02d}.html" class="reading-link">独立阅读 {icon('arrow')}</a></div><div class="thesis"><span>{icon('spark')} 本课命题</span>{para(d['thesis'],f'day:{n}:thesis')}</div><div class="lesson-context"><span>{icon('book')} 经文起点</span><p>{E(l['bible'])}</p><span>{icon('map')} 历史与处境</span>{para(l['setting'],f'day:{n}:setting')}</div><div class="source-box"><div class="box-heading">{icon('quote')} 指定原文 <small>CCI · 正文保持不变</small></div>{originals}</div><div class="lesson-subheading"><span>01</span><h3>经文怎样把答案推出来</h3></div>{para(d['exegesis'],f'day:{n}:exegesis')}<div class="lesson-subheading"><span>02</span><h3>抓住因果，不只背结论</h3></div>{chain}<div class="deep-grid"><article class="boundary-card"><div class="box-heading">{icon('compare')} 必须分清</div>{concept}</article><article class="difficulty-card"><div class="box-heading">{icon('question')} 关键难题</div><h4>{E(d['difficult']['q'])}</h4>{para(d['difficult']['a'],f'day:{n}:difficulty')}</article></div><div class="lesson-subheading"><span>03</span><h3>放回整本圣经与圣约主线</h3></div>{para(l['covenant'],f'day:{n}:covenant')}<article class="scene-card"><div class="scene-icon">{icon('map')}</div><div><div class="eyebrow">真实圣经场景 · 按经文概述</div><h4>{E(d['scene']['title'])}</h4>{para(d['scene']['body'],f'day:{n}:scene')}<span class="verse-chip">{E(d['scene']['ref'])}</span></div></article><div class="cross-reference"><b>信条互证</b><span>{E(l['refs'])}</span><a href="library.html#belgic">比利时全文</a><a href="library.html#dort">多特全文</a></div><div class="lesson-subheading"><span>04</span><h3>把恩典落实到今天</h3></div>{para(l['application'],f'day:{n}:application','application-text')}<div class="recall-card"><div>{icon('brain')} 记忆锚点</div>{para(d['memory'],f'day:{n}:memory')}<span>闭卷回想</span><h4>{E(l['review'])}</h4><button data-recall="{n}">显示回忆线索</button><p data-recall-answer="{n}" hidden>{E(d['thesis'])}</p></div><div class="lesson-end"><label><input type="checkbox" class="complete" data-complete="{n}"> 已学习并闭卷回想</label><button data-note-for="{n}">{icon('pen')} 写本课笔记</button><a href="{links[0]}" target="_blank" rel="noopener">CCI本课扩展 ↗</a></div><div class="lesson-note" id="lesson-note-{n}" hidden><label for="note-{n}">主日{n} · 我的笔记</label><textarea id="note-{n}" data-note="{n}" rows="4" placeholder="一个因果关系、一处疑问、一个行动…"></textarea><span>自动保存到此浏览器，可在“我的标记”中一起导出。</span></div><div class="course-sources">本课研究入口：{''.join(f'<a href="{E(u)}" target="_blank" rel="noopener">{i+1} ↗</a>'for i,u in enumerate(links))}</div></section>'''
  chapter=chapter.replace('</div><div class="lesson-context">',f'<button class="quick-mark" data-mark-whole="day:{n}:thesis">{icon("pen")} 标记本课命题</button></div><div class="lesson-context">',1)
  chapters.append(chapter)
  prev=f'<a href="day-{n-1:02d}.html">← 主日{n-1}</a>'if n>1 else '<a href="index.html">← 全书总览</a>'
  nxt=f'<a href="day-{n+1:02d}.html">主日{n+1} →</a>'if n<52 else '<a href="memory.html">进入记忆工坊 →</a>'
  (O/f'day-{n:02d}.html').write_text(page(f'主日{n} · {l["title"]}',f'<nav class="breadcrumbs"><a href="index.html#day-{n}">全书</a><span>/</span>主日{n:02d}</nav>'+chapter+f'<nav class="chapter-pagination">{prev}{nxt}</nav>',f'day-{n:02d}'),encoding='utf-8')
  search.append({'title':f'主日{n} · {l["title"]}','url':f'day-{n:02d}.html','body':' '.join([l['bible'],l['argument'],l['covenant'],d['thesis'],d['exegesis'],d['difficult']['a']]+[s['text']for _,s in ss])})
  flash.append({'day':n,'part':kind,'title':l['title'],'q':l['review'],'answer':d['thesis'],'memory':d['memory'],'chain':d['chain']})
 course_grid='<div class="course-grid">'+''.join(f'<a class="course-tile {part(int(l["n"]))[0]}" href="#day-{l["n"]}"><span>{int(l["n"]):02d}</span><b>{E(l["title"])}</b><small>问{E(l["q"])} {icon("arrow")}</small></a>'for l in lessons)+'</div>'
 catalogue=section('lessons','52主日，全程展开',f'<p class="section-lead">先抓命题，再读原文；跟随经文推论，辨清关键边界，最后闭卷回想。</p><div class="color-key"><span class="intro">总纲 1</span><span class="misery">罪苦 2–4</span><span class="grace">拯救 5–31</span><span class="thanks">感恩 32–52</span></div>{course_grid}','07 / THE COMPLETE COURSE')
 # Keep all actual text in HTML; offscreen layout is deferred by CSS, never by removing content.
 full=hero+structure+markable(lens,'overview:core')+section('history-preview','一段救赎历史，一部认信史',f'<div class="two-cards"><a href="history.html"><b>{icon("clock")} 时间线与真实背景</b><p>创造与应许 → 道成肉身 → 十架复活 → 教会与新创造；再看1563年的教导处境。</p></a><a href="history.html#geography"><b>{icon("map")} 地图与文化区域</b><p>从犹太地、希腊语东地中海到拉丁西方与普法尔茨。让时间、地点与问题相连。</p></a></div>','04 / HISTORY & GEOGRAPHY')+forms+memory+catalogue+''.join(chapters)+sources
 (O/'index.html').write_text(page('读懂唯一的安慰',full),encoding='utf-8')
 (O/'overview.html').write_text(page('圣经与圣约主线',structure+markable(lens,'overview:core'),'overview'),'utf-8')
 (O/'history.html').write_text(page('时间线、故事与地理',history,'history'),'utf-8')
 (O/'forms.html').write_text(page('三项联合信条 · 深度比较',forms+sources,'forms'),'utf-8')
 (O/'memory.html').write_text(page('记忆工坊 · 闭卷回想',memory,'memory'),'utf-8')
 library=[]
 for k,doc in docs.items():
  library.append(f'<section class="reading-section source-document" id="{k}"><div class="eyebrow">指定中文原文 · CCI</div><h1>{E(doc["title"])}</h1><p><a href="{E(doc["source"])}">原站目录 ↗</a> · <a href="source-audit.json">逐字核验记录</a></p>')
  for i,s in enumerate(doc['sections'],1):library.append(f'<div id="{k}-{i}" class="source-container">{original(k,s,i)}</div>')
  library.append('</section>')
  if k in ['apostles','nicene','athanasian']:
   clean=f'<article class="clean-reader"><div class="eyebrow">CREDO · 指定中文译文</div><h1>{E(doc["title"])}</h1><div class="clean-controls"><a href="memory.html">← 背诵工坊</a><button data-print>打印干净版</button></div>{original(k,doc["sections"][0],1)}<p class="caption">仅调整排版，不改正文。默认隐藏个人标记；可在阅读设置中显示。来源：CCI《敬拜手册》。</p></article>'
   (O/f'reader-{k}.html').write_text(page(doc['title'],clean,f'reader-{k}',True),encoding='utf-8')
 (O/'library.html').write_text(page('六份认信原典全文','<nav class="library-nav">'+''.join(f'<a href="#{k}">{E(d["title"])}</a>'for k,d in docs.items())+'</nav>'+''.join(library),'library'),encoding='utf-8')
 for f in ['reader.css','reader.js','annotations.js','reader-init.js']:shutil.copyfile(R/f,O/f)
 shutil.copyfile(R/'qa/v2-source-audit.json',O/'source-audit.json')
 if (R/'qa/v2-cci-expansion.json').exists():shutil.copyfile(R/'qa/v2-cci-expansion.json',O/'cci-expansion.json')
 else:(O/'cci-expansion.json').write_text(json.dumps({'scope':'CCI I Belong 52主日对应章节；六份认信正文；不声称全站穷尽。'},ensure_ascii=False),'utf-8')
 (O/'flashcards.json').write_text(json.dumps(flash,ensure_ascii=False),'utf-8')
 (O/'search-index.json').write_text(json.dumps(search,ensure_ascii=False),'utf-8')
 (O/'creeds.json').write_text(json.dumps({k:markable(docs[k]['sections'][0]['html'],f'original:{k}:1')for k in ['apostles','nicene','athanasian']},ensure_ascii=False),'utf-8')
 (R/'qa/v2-build-report.json').write_text(json.dumps({'edition':EDITION,'pages':len(list(O.glob('*.html'))),'lessons':52,'questions':129,'deep_lessons':len(deep),'deep_analysis_characters':sum(len(json.dumps(d,ensure_ascii=False))for d in deep.values()),'source_units':232,'rendering':'All text in static HTML; CSS content-visibility for offscreen sections; no wheel/touch interception.'},ensure_ascii=False,indent=2),'utf-8')
 print(f'V2: {len(deep)}/52 deep lessons, 232 immutable original units, {len(list(O.glob("*.html")))} pages.')
