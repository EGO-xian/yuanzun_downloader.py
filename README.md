# novel-spider
专为 yuanzunxs88.com 站点定制的 Python 爬虫，支持自动合并分页、去除广告、过滤导航、添加段落缩进，最终生成干净的 TXT 文件。

功能特点
✅ 智能章节提取：自动识别真实章节列表（过滤“书库”、“排行”等无关链接）

✅ 分页合并：识别章节分页（如 xxx.html 和 xxx_2.html）并自动拼接完整内容

✅ 广告/导航过滤：删除“本章未完”、“上一页”、“下一章”、“加入书签”等干扰行

✅ 重复标题去重：合并分页时自动移除多余的章节标题

✅ 文本清洗：删除 -->、<< 等特殊标记，去除单独的分页句号及分隔线

✅ 中文段落缩进：每段前自动添加两个全角空格（　　），符合阅读习惯

✅ 请求延迟：可配置下载间隔，降低被封风险

✅ 错误容忍：单章失败不影响整体下载，自动跳过并继续

依赖环境
Python 3.6+

第三方库：requests, beautifulsoup4

安装与使用
1. 安装依赖
bash
pip install requests beautifulsoup4
2. 下载脚本
将代码保存为 novel_downloader.py。

3. 修改配置（可选）
脚本顶部可自定义以下参数：

python
START_URL = 'https://www.yuanzunxs88.com/go/1521/'   # 小说目录页
OUTPUT_DIR = r'E:\下载器\下载文件'                   # 保存目录
OUTPUT_FILE = '小说.txt'                            # 输出文件名
DELAY = 1                                           # 章节间延时（秒）
4. 运行
bash
python novel_downloader.py
输出示例
下载完成后会在指定目录生成 TXT 文件，内容格式如下：

text
第1章 反派？但我是病娇

　　清晨的阳光透过窗帘，池小橙睁开眼睛...
　　（正文内容，每段首行缩进两个全角空格）

==================================================



第2章 喜欢你喜欢你喜欢你喜欢你

　　“你……你为什么要救我？”

  
　　...
注意事项
本脚本仅用于个人学习与备份，请勿传播下载内容，尊重版权。

网站可能存在反爬机制，如频繁被封请适当增加 DELAY 值。

若网站改版导致失效，请根据实际 HTML 调整 content_selectors 或 block_keywords。

常见问题
Q：运行时提示 ModuleNotFoundError
A：未安装依赖，执行 pip install requests beautifulsoup4。

Q：下载的章节不全或顺序错乱
A：脚本已按章节数字排序，如果仍然错乱，请检查目录页是否包含所有章节。

Q：正文中仍有残留广告
A：在 clean_text 函数的 block_keywords 列表中添加对应的关键词即可。

许可
本脚本仅供学习交流使用，请勿用于商业或非法用途。

