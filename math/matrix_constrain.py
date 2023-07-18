# -*- coding: utf-8 -*-
# @FileName :  matrix_constrain.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/6/13 10:26
# @Software : PyCharm
# Description:
import pymel.core as pm
import pymel.core.nodetypes as nt
import pymel.core.datatypes as dt


def offset_parent_matrix():
    """
    矩阵偏移父子约束
    利用transform节点的offsetParentMatrix接口来实现父子约束
    被约束对象可变换

    Returns:None
    """
    from_obj, to_obj = pm.selected()  # 获取约束父对象和子对象
    # 创建空组作为父对象的子物体，并且变换和子对象相同，得到两个对象的相对偏移
    offset_grp = pm.group(em=True)
    pm.parent(offset_grp, from_obj)
    pm.matchTransform(offset_grp, to_obj)
    # 父对象的世界矩阵 -- 子对象的偏移父子矩阵
    from_obj.worldMatrix >> to_obj.offsetParentMatrix
    # 偏移空组的变换 -- 子对象的变换（使子对象保持偏移）
    offset_grp.translate >> to_obj.translate
    offset_grp.rotate >> to_obj.rotate
    offset_grp.scale >> to_obj.scale

    pm.delete(offset_grp)

    return None


def matrix_constrain():
    """
    矩阵父子约束
    利用矩阵乘法节点实现矩阵父子约束
    被约束对象不可变换

    Returns:None
    """
    cstr_obj, cstred_obj = pm.selected()  # 获取约束父对象和子对象
    # 创建空组作为父对象的子物体，并且变换和子对象相同，得到两个对象的相对偏移
    offset_grp = pm.group(em=True)
    pm.parent(offset_grp, cstr_obj)
    pm.matchTransform(offset_grp, cstred_obj)
    # 创建组合矩阵节点作为偏移缓存节点，创建矩阵相乘节点，创建分解矩阵节点
    offset_matrix_node = pm.createNode("composeMatrix", name="Offset_Matrix_Cache")
    mult_matrix_node = pm.createNode("multMatrix")
    decompose_matrix_node = pm.createNode("decomposeMatrix")
    # 偏移空组连接偏移缓存节点
    offset_grp.translate >> offset_matrix_node.inputTranslate
    offset_grp.rotate >> offset_matrix_node.inputRotate
    offset_grp.scale >> offset_matrix_node.inputScale
    # 连接矩阵相乘节点，三项分别是：偏移矩阵，父对象世界矩阵，子对象的父对象逆矩阵
    offset_matrix_node.outputMatrix >> mult_matrix_node.matrixIn[0]
    cstr_obj.worldMatrix[0] >> mult_matrix_node.matrixIn[1]
    cstred_obj.parentInverseMatrix[0] >> mult_matrix_node.matrixIn[2]
    # 矩阵相乘后的矩阵和连接到分解矩阵，分解为位移 旋转和缩放
    mult_matrix_node.matrixSum >> decompose_matrix_node.inputMatrix
    # 分解矩阵节点变换输出连接子对象的变换输入
    decompose_matrix_node.outputTranslate >> cstred_obj.translate
    decompose_matrix_node.outputRotate >> cstred_obj.rotate
    decompose_matrix_node.outputScale >> cstred_obj.scale
    # 断开偏移空组和偏移缓存节点，偏移数据已经存入偏移缓存节点，偏移空组不再需要
    offset_grp.translate // offset_matrix_node.inputTranslate
    offset_grp.rotate // offset_matrix_node.inputRotate
    offset_grp.scale // offset_matrix_node.inputScale
    # 删除偏移空组
    pm.delete(offset_grp)
    return None


def get_transform_matrix(source_obj: nt.Transform, target_obj: nt.Transform):
    """获取一个对象到另一个对象的变换矩阵

    Args:
        source_obj (pm.nodetypes.Joint): 源对象
        target_obj (pm.nodetypes.Joint): 目标对象

    Returns:
        dt.Matrix: 变换矩阵
    """
    # 获取源骨骼的世界坐标矩阵
    source_matrix = source_obj.getMatrix(worldSpace=True)

    # 获取目标骨骼的世界坐标矩阵
    target_matrix = target_obj.getMatrix(worldSpace=True)

    # 将源骨骼的世界坐标矩阵转换为逆矩阵
    source_inverse_matrix = source_matrix.inverse()

    # 计算源骨骼到目标骨骼的变换矩阵
    transform_matrix: dt.Matrix = target_matrix * source_inverse_matrix

    return transform_matrix
