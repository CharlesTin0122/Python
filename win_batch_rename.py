# -*- coding: utf-8 -*-
# Python 3.9 +
import os
import re


def batch_rename(find_str: str, replace_str: str, path: str) -> list:
    """
    批量修改替换文件名
    Args:
        find_str: 要查找的字符串
        replace_str: 要替换的字符串
        path: 要重命名的文件所在路径

    Returns:
        重命名后的名称列表
    """
    all_renamed_path = []  # 储存重命名后的路径列表

    for root, dirs, files in os.walk(path):
        for filename in files:
            file_path = os.path.join(root, filename)
            # 正确的 re.sub 参数顺序
            renamed_filename = re.sub(find_str, replace_str, filename)

            if renamed_filename != filename:  # 确保有文件名变化
                renamed_path = os.path.join(root, renamed_filename)
                all_renamed_path.append(renamed_path)  # 添加到返回列表

                try:
                    os.rename(file_path, renamed_path)  # 重命名文件
                    print(f"Renamed: {file_path} -> {renamed_path}")
                except OSError as e:
                    print(f"Error renaming {file_path}: {e}")

    return all_renamed_path


if __name__ == "__main__":
    find_str = "_Male_"
    replace_str = "_M_"
    path = r"D:\Work\Animation\cloth\import"

    batch_rename(find_str, replace_str, path)
