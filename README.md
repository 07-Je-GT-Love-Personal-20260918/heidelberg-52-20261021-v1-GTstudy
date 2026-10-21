# 海德堡要理问答 · 52主日 · GTstudy

版本标识：**heidelberg-52-20261021-v1-GTstudy**；2026-10-21，v1.0.0。

52个主日、129问完整原文与原创解读；从整本圣经的救赎历史到圣约、信经、伦理与祷告。每课包括历史文化情境、经文索引、论证、圣约联系、应用、记忆句、回忆题及本地笔记。57个静态HTML页面，含三份信经干净版与六份原典库。

## 部署

| 平台 | 地址 | 状态 |
| --- | --- | --- |
| GitHub Pages | https://07-je-gt-love-personal-20260918.github.io/heidelberg-52-20261021-v1-GTstudy/ | 部署中，以deployment.json核验为准 |
| Surge | https://heidelberg-52-20261021-v1-gtstudy.surge.sh/ | 部署中，以deployment.json核验为准 |
| Vercel | 尚无确认的公开地址 | 待登录和部署成功后填写，不将计划域名冒充上线地址 |

仓库：https://github.com/07-Je-GT-Love-Personal-20260918/heidelberg-52-20261021-v1-GTstudy

## 来源与范围

六份正式中文文本来自CCI《敬拜手册》相应网页，与用户提供的2015版PDF对应。`content/fulltexts.json`保存232单元、来源与摘要。现代译文版权归原权利人，不宣称为公版或采用源码许可；不采用旧项目中未经本轮确认的许可声明。原创解读与原文明确分开。

`qa/source-audit.json`记录本轮155个去重来源的联网核验。比较仅忽略Unicode空白，保留词语、标点、段号和脚注。文本hash在每次构建时检查。网站不声称已通读或综合CCI全站，也不声称各欧陆教会在每一项圣约解释上都完全相同。

PDF只读参考，不将其文件、任何访问令牌、账号密码、会话数据放入仓库。Natural Earth底图为公版；地图采用近似现代坐标，不表示古代疆界。插图和图标为原创SVG。

## 开发与恢复

Python 3.10及以上：

```sh
python build.py
python -m http.server 4182 -d dist
```

构建无第三方依赖。重新联网核验需先安装`requirements.txt`再运行`python audit.py`。网页数据与源码均版本管理；发布标签`v1.0.0-20261021`用于恢复。建议从标签建立新分支：

```sh
git switch -c restore-v1 v1.0.0-20261021
```

推送main触发Pages自动发布。Surge与Vercel需相应平台认证；账号凭据不进入源码，Vercel配置在`vercel.json`。新版本修改日期、版本、发布域名、README与deployment.json，保留旧标签。

## 使用

首页全部平铺；目录可隐藏，手机目录为抽屉。支持夜读、18–30px字号、减少动效、地图键盘操作、分幕故事、信经背诵遮罩和设备朗读。学习进度与笔记仅保存在当前浏览器当前域名，跨设备/跨站点需导出再导入。无后端采集。

## 版本记录

- v1.0.0 · 2026-10-21：首次完整52主日学习站；六份认信原典；地图、双时间线、故事、三经比较、干净阅读与记忆模块。
