# -*- coding: utf-8 -*-
# @Time    : 2023/4/3 13:32
# @Author  : TianChao
# @File    : test001.py
# @Email: tianchao0533@gamil.com
# @Software: PyCharm

import pymel.core as pm


def batch_closestjoint_constrain(jntlist1: list, jntlist2: list):
    """用于在另一个骨骼列表中找到最接近选择骨骼并创建父子约束。
    Args:
        jntlist1:约束父对象骨骼链列表
        jntlist2:约束子对象骨骼链列表
    Returns:None
    """
    # 遍历选定的所有骨骼
    for jnt in jntlist1:
        closest_joint = None  # 创建最近骨骼变量
        closest_distance = float("inf")  # 创建最近距离变量为正无穷
        pos1 = jnt.getTranslation(space='world')  # 获取骨骼位置坐标

        # 遍历场景查找最近的骨骼
        for other_joint in jntlist2:
            if other_joint == jnt:  # 如果该骨骼已存在所选择骨骼
                continue  # 则跳过
            elif not other_joint.visibility.get():  # 如果该骨骼显示为隐藏
                continue  # 则跳过
            pos2 = other_joint.getTranslation(space='world')  # 获取其他骨骼位置
            distance = (pos1 - pos2).length()  # 获取选择骨骼和其他骨骼之间的距离,注意.length求两点之间的距离
            """通过遍历所有其他骨骼和选择骨骼之间的距离，得到离选择骨骼最近的其他骨骼的距离"""
            if distance < closest_distance:  # 如果该距离小于最近骨骼距离即正无穷
                closest_joint = other_joint  # 那么最近骨骼就是该骨骼
                closest_distance = distance  # 最近距离就是该距离

        # 如果最近骨骼存在,同时骨骼没有被约束,父子约束到最近的骨骼
        if closest_joint and not pm.listConnections(closest_joint, type='parentConstraint'):
            pm.parentConstraint(jnt, closest_joint, maintainOffset=True)  # 执行约束


list1 = pm.ls(sl=True)  # 列出约束父对象骨骼链的所有骨骼
list2 = pm.ls(sl=True)  # 列出约束子对象骨骼链的所有骨骼
batch_closestjoint_constrain(list1, list2)
