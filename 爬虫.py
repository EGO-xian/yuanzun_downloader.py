import requests
from bs4 import BeautifulSoup
import time
import os
import re

# ==================== 用户配置 ====================
# 请将下面的网址替换为你想要下载的小说目录页 URL
BOOK_URL = 'https://www.yuanzunxs88.com/go/1521/'   # 示例：《穿越炮灰反派？我化身病娇萝莉》
# =================================================

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.yuanzunxs88.com/',
}
TIMEOUT = 10
DELAY = 1   # 章节间延时（秒），避免请求过快
PARAGRAPH_INDENT = '　　'

def get_soup(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.encoding = 'gbk'
        if r.status_code != 200:
            print(f"请求失败：{url}，状态码 {r.status_code}")
            return None
        return BeautifulSoup(r.text, 'html.parser')
    except Exception as e:
        print(f"请求异常：{url}，错误：{e}")
        return None

def get_book_title(soup, url):
    """从目录页提取小说书名"""
    # 尝试多种常见位置
    # 1. <div class="book"> 下的 <h1>
    book_div = soup.select_one('div.book h1')
    if book_div:
        return book_div.get_text(strip=True)
    # 2. <div class="info"> 下的 <h1>
    info_h1 = soup.select_one('div.info h1')
    if info_h1:
        return info_h1.get_text(strip=True)
    # 3. 从 <title> 中提取（通常格式：书名_笔趣阁）
    title_tag = soup.find('title')
    if title_tag:
        title_text = title_tag.get_text(strip=True)
        # 去除 "_笔趣阁" 等后缀
        title_text = re.sub(r'_[^_]+$', '', title_text)
        if title_text:
            return title_text
    # 4. 从面包屑导航中提取
    breadcrumb = soup.select_one('.breadcrumb')
    if breadcrumb:
        # 最后一个 <a> 或文本
        last = breadcrumb.find_all('a')[-1] if breadcrumb.find_all('a') else None
        if last:
            return last.get_text(strip=True)
    return "未知书名"

def clean_title(title):
    match = re.search(r'(第[0-9]+章[^\n]*)', title)
    return match.group(1).strip() if match else None

def get_chapter_list(soup, base_url):
    """提取章节列表，base_url 为目录页 URL，用于补全链接"""
    chapters = []
    # 查找所有 class 以 d 开头的 div（如 d1, d2, ..., dXXX）
    for div in soup.find_all('div', class_=re.compile(r'^d\d+$')):
        a_tag = div.find('a')
        if a_tag:
            raw_title = a_tag.get_text(strip=True)
            link = a_tag.get('href')
            if not raw_title or not link:
                continue
            clean = clean_title(raw_title)
            if not clean:
                match = re.search(r'第[0-9]+章[^\n]*', raw_title)
                if match:
                    clean = match.group(0).strip()
            if not clean:
                continue
            # 补全链接
            if not link.startswith('http'):
                if link.startswith('/'):
                    link = 'https://www.yuanzunxs88.com' + link
                else:
                    base_dir = '/'.join(base_url.split('/')[:-1]) + '/'
                    link = base_dir + link
            chapters.append((clean, link))
    # 如果上面没找到，回退到查找所有 .html 的 a 标签
    if not chapters:
        for a in soup.find_all('a', href=re.compile(r'\.html')):
            raw_title = a.get_text(strip=True)
            link = a['href']
            clean = clean_title(raw_title)
            if not clean:
                match = re.search(r'第[0-9]+章[^\n]*', raw_title)
                if match:
                    clean = match.group(0).strip()
            if not clean:
                continue
            if not link.startswith('http'):
                if link.startswith('/'):
                    link = 'https://www.yuanzunxs88.com' + link
                else:
                    base_dir = '/'.join(base_url.split('/')[:-1]) + '/'
                    link = base_dir + link
            chapters.append((clean, link))
    # 按章节数字排序
    def extract_chapter_num(title):
        match = re.search(r'第([0-9]+)章', title)
        return int(match.group(1)) if match else 0
    chapters.sort(key=lambda x: extract_chapter_num(x[0]))
    # 去重
    seen = set()
    unique = []
    for title, link in chapters:
        if link not in seen:
            seen.add(link)
            unique.append((title, link))
    print(f"共提取到 {len(unique)} 个真实章节")
    return unique

def extract_chapter_id(url):
    match = re.search(r'/(\d+)(?:_\d+)?\.html', url)
    return match.group(1) if match else None

def is_same_chapter(url1, url2):
    id1 = extract_chapter_id(url1)
    id2 = extract_chapter_id(url2)
    return id1 is not None and id1 == id2

def clean_text(raw_text, chapter_title):
    """清洗文本：删除广告、导航、特殊标记等"""
    raw_text = re.sub(r'-->>', '', raw_text)
    raw_text = re.sub(r'<<--', '', raw_text)
    lines = raw_text.split('\n')
    cleaned_lines = []
    seen_titles = set()
    title_clean = chapter_title.strip()
    block_keywords = [
        '本章未完', '点击下一页', '上一页', '下一页', '上一章', '下一章',
        '章节目录', '温馨提示', '按 回车[Enter]键', '返回书目', '加入书签',
        '推荐阅读', '所有内容均来自互联网', '笔趣阁只为原作者', '欢迎各位书友支持',
        '收藏', '首页', '都市', '穿越炮灰反派', '投票推荐', '留言反馈',
        '(1/2)', '(2/2)', '书库', '排行', '都市小说', '积分规则',
        '夜无疆', '欢迎进入梦魇直播间', '我不做妾', '星路仙踪', '洄天',
        '没你就不行', '人设崩塌后反派连夜跑了', '有港来信', '男二忍辱负重', '异度旅社'
    ]
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line in ('。', '.'):
            continue
        if re.fullmatch(r'[=\-*_]+', line):
            continue
        if any(kw in line for kw in block_keywords):
            continue
        if re.fullmatch(r'[\d\s/\\\-_=*]+', line):
            continue
        if line == title_clean:
            continue
        if re.match(r'^第\d+章\s+.+', line):
            if line in seen_titles:
                continue
            seen_titles.add(line)
        cleaned_lines.append(PARAGRAPH_INDENT + line)
    return '\n'.join(cleaned_lines)

def get_chapter_content(soup, current_url, chapter_title):
    """递归获取完整章节（含分页）"""
    content_div = None
    content_selectors = [
        'div#content', 'div#chaptercontent', 'div.read-content',
        'div.article-content', 'div.content', 'div#nr', 'div#nr1'
    ]
    for sel in content_selectors:
        content_div = soup.select_one(sel)
        if content_div:
            break
    if not content_div:
        raw_text = soup.body.get_text(separator='\n', strip=True) if soup.body else ''
        return clean_text(raw_text, chapter_title)
    for script in content_div(['script', 'style']):
        script.decompose()
    current_text = content_div.get_text(separator='\n', strip=True)
    # 查找“下一页”链接
    next_link = None
    for a in soup.find_all('a', href=True):
        text = a.get_text(strip=True)
        if '下一页' in text or '下一章' in text:
            next_link = a['href']
            break
    if next_link:
        if not next_link.startswith('http'):
            if next_link.startswith('/'):
                next_url = 'https://www.yuanzunxs88.com' + next_link
            else:
                base = '/'.join(current_url.split('/')[:-1]) + '/'
                next_url = base + next_link
        else:
            next_url = next_link
        if is_same_chapter(current_url, next_url):
            print(f"  检测到同一章节的分页，获取：{next_url}")
            time.sleep(DELAY)
            next_soup = get_soup(next_url)
            if next_soup:
                next_text = get_chapter_content(next_soup, next_url, chapter_title)
                current_text = current_text + '\n' + next_text
    return clean_text(current_text, chapter_title)

def download_novel(book_url):
    print("1. 获取目录页...")
    soup = get_soup(book_url)
    if not soup:
        print("获取目录失败，请检查网址")
        return
    print("2. 提取书名...")
    book_title = get_book_title(soup, book_url)
    print(f"书名：{book_title}")
    print("3. 提取章节列表...")
    chapters = get_chapter_list(soup, book_url)
    if not chapters:
        print("未提取到任何章节，请检查网页结构")
        return
    # 创建输出目录：脚本所在目录下的 downloads 文件夹
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'downloads')
    os.makedirs(output_dir, exist_ok=True)
    # 文件名使用书名，替换非法字符
    safe_title = re.sub(r'[\\/*?:"<>|]', '', book_title)
    output_path = os.path.join(output_dir, f'{safe_title}.txt')
    print(f"开始下载，共 {len(chapters)} 章，保存到 {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        for idx, (title, link) in enumerate(chapters, 1):
            print(f"[{idx}/{len(chapters)}] 正在下载：{title}")
            soup_page = get_soup(link)
            if not soup_page:
                print(f"  跳过：{link}")
                continue
            content = get_chapter_content(soup_page, link, title)
            if not content:
                print(f"  内容为空，跳过")
                continue
            f.write(f"\n\n{title}\n\n")
            f.write(content)
            f.write("\n\n" + "="*50 + "\n\n")
            time.sleep(DELAY)
    print(f"下载完成！文件保存在：{output_path}")

if __name__ == '__main__':
    download_novel(BOOK_URL)
