#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import zhconv

def remove_ad_flexible(content, ad_text):
    """
    从 content 中删除广告文本，忽略广告文本内部的任何空白字符（包括换行）。
    广告文本中的每个字符之间允许出现 \s*。
    """
    # 将广告文本转换为正则模式：每个字符间允许任意空白
    pattern = r'\s*'.join(re.escape(ch) for ch in ad_text)
    # 使用多行模式，让 '.' 也能匹配换行符（实际上 \s 已包含换行，但为了稳妥）
    regex = re.compile(pattern, re.DOTALL)
    # 替换为空
    return regex.sub('', content)

def clean_novel_file(input_path, output_path=None, backup=True):
    """
    清理小说 TXT 文件：
    1. 删除指定的广告段落（支持跨行匹配）
    2. 删除全等号分隔行（如 ==========）
    3. 全文繁体转简体（使用 zhconv）
    """
    # 需要删除的广告文本（原始形式，不关心其中的换行）
    ads_to_remove = [
        "关于登录用户跨设备保存书架的问题,已经修正了, 如果还是无法保存, 请先记住书架的内容, 清除浏览器的Cookie, 再重新登陆并加入书架!",
        "本站采用Cookie技术来保存您的“阅读记录”和“书架”, 所以清除浏览器Cookie数据、重装浏览器 之类的操作会让您的阅读进度消失哦,建议可以偶尔截图保存书架, 以防找不到正在阅读的小说!",
        "搜书名找不到, 可以试试搜作者哦, 也许只是改名了!"
    ]

    # 读取原文件
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 删除广告（跨行灵活匹配）
    for ad in ads_to_remove:
        content = remove_ad_flexible(content, ad)
        # 可选：再尝试一次精确匹配（以防正则未匹配到）
        content = content.replace(ad, '')

    # 2. 删除全等号分隔行（单独成行的等号串）
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        if re.fullmatch(r'=+', line.strip()):
            continue
        cleaned_lines.append(line)
    content = '\n'.join(cleaned_lines)

    # 3. 繁体转简体
    content = zhconv.convert(content, 'zh-cn')

    # 清理多余空行（保留最多两个换行，维持章节分隔）
    content = re.sub(r'\n{3,}', '\n\n', content)

    # 确定输出路径
    if output_path is None:
        if backup:
            backup_path = input_path + '.bak'
            os.rename(input_path, backup_path)
            print(f"原文件已备份为: {backup_path}")
        output_path = input_path

    # 写入清理后的内容
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"清理完成！文件保存为: {output_path}")

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("用法: python clean_novel.py <小说文件路径> [输出文件路径]")
        print("示例: python clean_novel.py 小说.txt")
        print("      python clean_novel.py 小说.txt 小说_clean.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(input_file):
        print(f"错误: 文件 '{input_file}' 不存在")
        sys.exit(1)

    clean_novel_file(input_file, output_file, backup=True)
