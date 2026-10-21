from pathlib import Path
R=Path(__file__).parent
p=R/'content/overview.html';t=p.read_text(encoding='utf-8')
a='译文版权归原权利人。本站不宣称译文为公版，也没有把旧项目文件中未经本轮核实的“已获许可”声明当作事实。原创解读、图表与译文应分别识别。圣经位置引用用于检索，原创释义不是圣经逐字引文。'
b='译文版权归原权利人，不宣称为公版。原创解读、图表与译文分别标识。圣经位置引用用于检索，原创释义不是圣经逐字引文。本轮联网核验152页、227单元通过；另3页涉及5单元因连接错误暂未完成在线复核，仍保留既有CCI来源文本与完整性校验，详见报告。'
if a in t:p.write_text(t.replace(a,b),encoding='utf-8')
