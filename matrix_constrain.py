# -*- coding: utf-8 -*-
# @FileName :  matrix_constrain.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/6/13 10:26
# @Software : PyCharm
# Description:
import pymel.core as pm
import pymel.core.nodetypes as nt


def matrix_offset_constrain(parent_obj: nt.Transform, child_obj: nt.Transform):
    """
    矩阵偏移父子约束
    Args:
        parent_obj(nt.Transform): 约束父对象
        child_obj(nt.Transform): 约束子对象

    Returns:None

    """
    assert (isinstance(parent_obj, nt.Transform))
    assert (isinstance(child_obj, nt.Transform))
    pick_matrix_node = pm.createNode("pickMatrix")

    pm.connectAttr(parent_obj.worldMatrix[0], pick_matrix_node.inputMatrix)
    pm.connectAttr(pick_matrix_node.outputMatrix, child_obj.offsetParentMatrix)
    # parent_obj.worldMatrix[0] >> child_obj.offsetParentMatrix
    pm.setAttr(pick_matrix_node.useTranslate, 1)
    pm.setAttr(pick_matrix_node.useRotate, 1)
    pm.setAttr(pick_matrix_node.useScale, 1)


if __name__ == '__main__':
    parent_obj1, child_obj1 = pm.selected()
    matrix_offset_constrain(parent_obj1, child_obj1)
