# -*- coding: utf-8 -*-
# Python 3.9 +
import os
import re


def batch_rename(replace_str: str, find_str: str, path: str) -> list:
    """
    批量修改替换文件名
    Args:
        replace_str: 要替换的字符串
        find_str: 原始字符串
        path: 要重命名的文件所在路径

    Returns:重命名后的名称列表

    """
    all_renamed_path = []  # 创建变量用来储存要返回的重命名后名称列表
    # 遍历整个路径，找到所有文件路径
    for root, dirs, files in os.walk(path):
        for filename in files:
            file_path = os.path.join(root, filename)
            # 正则表达式文件名重命名，注意这里的参数是：1.要替换的字符换，2.原始字符串，3.要修改的文件名
            renamed_filename = re.sub(replace_str, find_str, filename)
            renamed_path = os.path.join(root, renamed_filename)  # 将文件名重新组合成完整路径
            all_renamed_path.append(renamed_path)  # 将所完整路径添加到变量，用于返回
            # 重命名
            try:
                os.rename(file_path, renamed_path)
                print(f"Renamed: {file_path} -> {renamed_path}")
            except OSError as e:
                print(f"Error renaming {file_path}: {e}")
    return all_renamed_path


if __name__ == "__main__":
    replace_str1 = "_Sword_"
    find_str1 = "_bow_"
    path1 = r"D:\Work_MobilGame\outsourcing\Submissions\modify"

    batch_rename(replace_str1, find_str1, path1)
