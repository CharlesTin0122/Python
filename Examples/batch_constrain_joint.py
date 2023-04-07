# -*- coding: utf-8 -*-
# @Time    : 2023/4/3 13:32
# @Author  : TianChao
# @File    : test001.py
# @Email: tianchao0533@gamil.com
# @Software: PyCharm

import pymel.core as pm

jntlist1 = pm.ls(sl=True, dag=True, type="joint")  # 列出骨骼链的所有骨骼，注意参数dag
jntlist2 = pm.ls(sl=True, dag=True, type="joint")  # 列出骨骼链的所有骨骼，注意参数dag

# 遍历选定的所有骨骼
for jnt in jntlist1:
    closest_joint = None  # 创建最近骨骼变量
    closest_distance = float("inf")  # 创建最近距离变量为正无穷
    pos1 = jnt.getTranslation(space='world')  # 获取骨骼位置坐标

    # 遍历场景查找最近的骨骼
    for other_joint in jntlist2:
        if other_joint == jnt:  # 如果该骨骼已存在玉所选择骨骼
            continue  # 则跳过
        elif not other_joint.visibility.get():
            continue
        pos2 = other_joint.getTranslation(space='world')  # 获取其他骨骼位置
        distance = (pos1 - pos2).length()  # 获取选择骨骼和其他骨骼之间的距离
        """通过遍历所有其他骨骼和选择骨骼之间的距离，得到离选择骨骼最近的其他骨骼的距离"""
        if distance < closest_distance:  # 如果该距离小于最近骨骼距离即正无穷
            closest_joint = other_joint  # 那么最近骨骼就是该骨骼
            closest_distance = distance  # 最近距离就是该距离

    # 父子约束到最近的骨骼
    if closest_joint:  # 如果最近骨骼存在
        pm.parentConstraint(jnt, closest_joint, maintainOffset=True)  # 执行父子约束
