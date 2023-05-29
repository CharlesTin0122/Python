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
    return '{}'.format(integer).rjust(padding_integer, '0')


# re.sub查询替换'#'为填充的整型
def enum_string(string, integer):
    if len(re.split('#*', string)) != 2:
        raise ValueError('not found any # with {}'.format(string))

    index = string.count('#')
    # re.sub(要替换的字符，替换的字符，要修改的字符串)
    return re.sub('#' * index, pad_integer(integer, index), string)


# 文件名按规定的格式递增
def getUniqueName(name, new_name):
    unique_name = name
    all_objs = pm.ls(long=True)  # 获取所有物体长名称
    # 用分割'|'和':'获取文件短名称
    obj_name = [obj.split('|')[-1].split(':')[-1] for obj in all_objs]
    # 遍历重命名
    if unique_name in obj_name:
        count = 1
        unique_name = enum_string(new_name, count)
        while unique_name in obj_name:
            count += 1
            unique_name = enum_string(new_name, count)
    return unique_name


if __name__ == '__main__':
    getUniqueName('test_05_loc', 'test_##_loc')
