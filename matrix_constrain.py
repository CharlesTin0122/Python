# -*- coding: utf-8 -*-
# @FileName :  matrix_constrain.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/6/13 10:26
# @Software : PyCharm
# Description:
import pymel.core as pm


def offset_parent_matrix():
    """
    矩阵偏移父子约束
    被约束对象可变换
    Returns:None
    """
    from_obj, to_obj = pm.selected()

    offset_grp = pm.group(em=True)
    pm.parent(offset_grp, from_obj)
    pm.matchTransform(offset_grp, to_obj)

    from_obj.worldMatrix >> to_obj.offsetParentMatrix

    offset_grp.translate >> to_obj.translate
    offset_grp.rotate >> to_obj.rotate
    offset_grp.scale >> to_obj.scale

    pm.delete(offset_grp)

    return None
