# yuanzun_downloader.py:

这是一个专为 https://www.yuanzunxs88.com 网站设计的 Python 爬虫脚本，支持下载该网站上任意一本小说的完整内容，自动合并分页、过滤广告、去除导航并添加段落缩进，最终生成干净的 TXT 文件。

## 功能特点

- ✅ 自动提取书名，使用书名作为输出文件名
- ✅ 智能识别章节列表（支持该网站特有的 `d1`~`dXXX` 嵌套结构）
- ✅ 自动合并分页（如 `xxx.html` 和 `xxx_2.html`）
- ✅ 过滤广告、导航、推荐等无关内容
- ✅ 去除重复章节标题、特殊标记（`-->`、`<<`）
- ✅ 每段首行添加两个全角空格缩进，符合中文阅读习惯
- ✅ 可配置下载延迟，降低被封风险
- ✅ 下载失败自动跳过，不影响后续章节

## 环境要求

- Python 3.6 及以上版本
- 依赖库：`requests`, `beautifulsoup4`

## 安装与使用

### 1. 安装依赖

打开命令行（终端），执行：

```bash
pip install requests beautifulsoup4
```
2. 下载脚本
将上面的完整脚本代码保存为 yuanzunxs_downloader.py。

3. 修改目标小说网址
用文本编辑器（如记事本、VS Code）打开脚本，找到文件开头的 BOOK_URL 变量，将其值修改为你想要下载的小说的目录页网址。

示例：

# 原示例（《穿越炮灰反派？我化身病娇萝莉》）
```bash
BOOK_URL = 'https://www.yuanzunxs88.com/go/1521/'
```

# 修改为你想下载的小说目录页，例如：
```bash
BOOK_URL = 'https://www.yuanzunxs88.com/go/12345/'
```
如何找到目录页？

打开 https://www.yuanzunxs88.com，搜索或点击任意小说，进入其介绍页，点击“阅读”或“章节目录”，浏览器地址栏中的 URL 即为目录页 URL。

4. 运行脚本
在脚本所在目录打开命令行，执行：

```bash
python yuanzunxs_downloader.py
```
5. 查看下载结果
下载完成后，会在脚本所在目录下自动创建 downloads 文件夹，小说 TXT 文件保存在其中，文件名即为小说书名。

自定义配置
你可以修改脚本顶部的以下参数（位于 BOOK_URL 下方）：
```bash

变量	                      说明	                  默认值
DELAY	                章节间请求延时（秒）	            1
TIMEOUT	                请求超时时间（秒）	            10
PARAGRAPH_INDENT	    段落缩进字符串	          '　　'（两个全角空格）

```
常见问题
Q: 运行时提示 ModuleNotFoundError: No module named 'requests'
A: 未安装依赖，执行 pip install requests beautifulsoup4 即可。

Q: 下载的章节顺序错乱或不全
A: 脚本会自动按章节目录中的数字排序，如果依然错乱，请检查目录页是否包含了所有章节链接。

Q: 正文中仍有残留广告或多余文字
A: 脚本内置了广告关键词过滤列表。如果遇到新广告，可以在 clean_text 函数的 block_keywords 列表中添加相应关键词。

Q: 网站打不开或请求失败
A: 该网站可能屏蔽了非中国大陆 IP，可以尝试使用代理或 VPN。另外，适当增加 DELAY 值可以降低请求频率。

注意事项
本脚本仅供个人学习、备份使用，请勿将下载内容传播或用于商业用途，尊重原作者版权。

请勿频繁请求，建议保持 DELAY >= 1，避免给服务器造成压力。

若网站改版导致失效，欢迎根据实际 HTML 调整选择器或过滤规则。


# clean_novel.py：

用于清理笔趣阁下载的小说文件：

删除指定的广告文本

删除全等号分隔行（=====...）

将繁体转换为简体

使用方法
```bash
python clean_novel.py <输入文件> [输出文件]

不指定输出文件：直接覆盖原文件（自动生成 .bak 备份）

指定输出文件：生成新文件，原文件不变
```

示例
```bash
# 直接清理原文件
python clean_novel.py 小说.txt

# 输出到新文件
python clean_novel.py 小说.txt 小说_clean.txt
```

## 环境要求

- Python 3.6 及以上版本
- 依赖库：`zhconv`

### 1. 安装依赖

打开命令行（终端），执行：

```bash
pip install requests beautifulsoup4
```

## 自定义
如需添加/修改广告文本，编辑脚本中的 ads_to_remove 列表即可。


# smart_format_novel.py ：

## 使用说明

运行（覆盖原文件，自动备份）：

```bash
python smart_format_novel.py "《穿越炮灰反派？我化身病娇萝莉》.txt"
```

如需保留原文件，指定输出文件：

```bash
python smart_format_novel.py 小说.txt 小说_格式化.txt
```
效果示例
处理前：

```text
第1章 开头



第一段正文


第二段正文



第2章 后续


正文段落
处理后：
```
```text
第1章 开头



第一段正文
第二段正文


第2章 后续


正文段落

```
标题后的两个空行被保留。

正文段落之间的空行被删除（第一段和第二段之间只有一个换行，没有多余空行）。

标题之间的空行（第2章前面的两个空行）因为其后一行是标题，也被保留。

正文末尾的换行（如果有）会被保留，因为后面是标题。

### 如果章节标题格式不同（如“第一章”而非“第1章”），请修改 is_chapter_title 中的正则表达式为 r'^\s*第[零一二三四五六七八九十百千万0-9]+章'。
