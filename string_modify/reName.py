# -*- coding: utf-8 -*-
"""
@FileName    :   reName.py
@DateTime    :   2023/02/13 11:26:32
@Author  :   Tian Chao
@Contact :   tianchao0533@163.com
"""

import re
import pymel.core as pm


# rjust用0填充文件名整型缺失
def pad_integer(integer, padding_integer):
    # 将一个整数 integer 转换为字符串，并在其左侧填充指定数量的零，使其达到 padding_integer 指定的总长度。
    return "{}".format(integer).rjust(padding_integer, "0")


# re.sub查询替换'#'为填充的整型
def enum_string(string, integer):

    '''
    1. re.split 是 Python 正则表达式模块 re 中的一个函数，用于根据指定的模式拆分字符串
    2. "#*" 表示零个或多个连续的 # 字符。这会在每个 # 字符的地方拆分字符串。
    3. 例如，对于输入字符串 "file_###", 拆分结果将是 ["file_", ""]，因为 #* 会匹配字符串中的所有 # 字符。
    4. 如果输入字符串中没有 # 字符，例如 "file_name"，拆分结果是 ["file_name"]，其长度为 1。
    5. 如果输入字符串中有多个连续的 # 分隔不同部分，例如 "file_###_part"，拆分结果是 ["file_", "_part"]，其长度为 2。
    6. 只有当拆分结果的长度正好为 2 时，才意味着字符串中有且只有一个部分包含 # 字符（例如 "file_###"）。
    '''
    if len(re.split("#*", string)) != 2:
        raise ValueError("not found any # with {}".format(string))
    index = string.count("#") # 字符串中'#'的个数
    # re.sub(要替换的字符，替换的字符，要修改的字符串)
    return re.sub("#" * index, pad_integer(integer, index), string)


# 文件名按规定的格式递增
def getUniqueName(name, new_name):
    unique_name = name
    all_objs = pm.ls(long=True)  # 获取所有物体长名称
    # 用分割'|'和':'获取文件短名称
    obj_name = [obj.split("|")[-1].split(":")[-1] for obj in all_objs]
    # 遍历重命名
    if unique_name in obj_name:
        count = 1
        unique_name = enum_string(new_name, count)
        while unique_name in obj_name:
            count += 1
            unique_name = enum_string(new_name, count)
    return unique_name


if __name__ == "__main__":
    getUniqueName("test_05_loc", "test_##_loc")
