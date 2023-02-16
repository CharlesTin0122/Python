# -*- coding: utf-8 -*-
'''
@FileName    :   reName.py
@DateTime    :   2023/02/13 11:26:32
@Author  :   Tian Chao 
@Contact :   tianchao0533@163.com
'''

import pymel.core as pm
import re

#rjust用0填充文件名整型缺失
def pad_integer(integer,padding_integer):
    return '{}'.format(integer).rjust(padding_integer,'0')

#re.sub查询替换'#'为填充的整型
def enum_string(string,integer):
    if len(re.split('#*',string)) !=2:
        raise ValueError('not found any # with {}'.format(string))

    index = string.count('#')
#re.sub(要替换的字符，替换的字符，要修改的字符串)
    return re.sub('#'*index,pad_integer(integer,index),string)
#文件名按规定的格式递增
def getUniqueName(name,newName):
    uniqueName = name
    allObjs = pm.ls(long=True) #获取所有物体长名称
#用分割'|'和':'获取文件短名称
    objName = [obj.split('|')[-1].split(':')[-1] for obj in allObjs]
#遍历重命名
    if uniqueName in objName:
        count = 1
        uniqueName = enum_string(newName,count)
        while uniqueName in objName:
            count += 1
            uniqueName = enum_string(newName,count)
    return uniqueName

# getUniqueName('test_05_loc','test_##_loc')
