#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re


def clean_novel_file(input_path, output_path=None, backup=True):
    """
    清理小说 TXT 文件：
    1. 删除指定的广告段落
    2. 将全文中的“於”替换为“于”

    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径（若为 None，则覆盖原文件）
        backup: 是否备份原文件（仅在覆盖时有效）
    """
    # 需要删除的广告文本（精确匹配整段）
    ads_to_remove = [
        "关於登录用户跨设备保存书架的问题, 已经修正了, 如果还是无法保存, 请先记住书架的内容, 清除浏览器的Cookie, 再重新登陆并加入书架!",
        "本站采用Cookie技术来保存您的「阅读记录」和「书架」, 所以清除浏览器Cookie数据丶重装浏览器 之类的操作会让您的阅读进度消失哦, 建议可以偶尔截图保存书架, 以防找不到正在阅读的小说!",
        "=================================================="
    ]

    # 读取原文件
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 删除广告（直接替换为空字符串）
    for ad in ads_to_remove:
        content = content.replace(ad, '')

    # 将繁体“於”替换为简体“于”
    content = content.replace('於', '于')

    # 可选：删除广告后可能留下多余的空行，可以进一步清理
    # 例如将连续多个换行替换为最多两个换行（保持章节分隔）
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