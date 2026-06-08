#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import os

def is_chapter_title(line):
    """判断一行是否为章节标题（以'第X章'开头）"""
    return bool(re.match(r'^\s*第[0-9]+章', line.strip()))

def format_novel(text):
    lines = text.splitlines()
    n = len(lines)

    # 标记每行是否为空行
    is_blank = [re.match(r'^\s*$', line) is not None for line in lines]

    # 标记需要保留的空行索引
    keep_blank = [False] * n

    i = 0
    while i < n:
        if is_blank[i]:
            start = i
            while i < n and is_blank[i]:
                i += 1
            end = i - 1

            # 检查空行块前后是否为标题行
            prev_is_title = (start > 0 and is_chapter_title(lines[start - 1]))
            next_is_title = (end + 1 < n and is_chapter_title(lines[end + 1]))

            if prev_is_title or next_is_title:
                # 保留这个空行块中的所有空行
                for j in range(start, end + 1):
                    keep_blank[j] = True
        else:
            i += 1

    # 构建输出：保留所有非空行 + 被标记为保留的空行
    output = []
    for idx, line in enumerate(lines):
        if not is_blank[idx]:
            output.append(line)
        else:
            if keep_blank[idx]:
                output.append('')   # 保留空行

    # 删除开头和结尾的多余空行（这些空行不可能前后有标题）
    while output and output[0] == '':
        output.pop(0)
    while output and output[-1] == '':
        output.pop()

    return '\n'.join(output)

def process_file(input_path, output_path=None, backup=True):
    try:
        encodings = ['utf-8', 'gbk', 'gb2312']
        content = None
        for enc in encodings:
            try:
                with open(input_path, 'r', encoding=enc) as f:
                    content = f.read()
                print(f"成功使用 {enc} 编码读取文件")
                break
            except UnicodeDecodeError:
                continue

        if content is None:
            raise ValueError("无法识别文件编码，请确认文件为文本格式")

        formatted = format_novel(content)

        if output_path is None:
            if backup:
                backup_path = input_path + '.bak'
                # 避免覆盖已有备份
                if os.path.exists(backup_path):
                    base, ext = os.path.splitext(backup_path)
                    counter = 1
                    while os.path.exists(f"{base}_{counter}{ext}"):
                        counter += 1
                    backup_path = f"{base}_{counter}{ext}"
                os.rename(input_path, backup_path)
                print(f"原文件已备份为: {backup_path}")
            output_path = input_path

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted)

        print(f"格式化完成！标题前后的空行已保留，其余空行已删除。文件保存为: {output_path}")

    except Exception as e:
        print(f"处理失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python smart_format_novel.py <输入文件> [输出文件]")
        print("示例: python smart_format_novel.py 小说.txt")
        print("      python smart_format_novel.py 小说.txt 小说_格式化.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(input_file):
        print(f"错误: 文件 '{input_file}' 不存在")
        sys.exit(1)

    process_file(input_file, output_file, backup=True)