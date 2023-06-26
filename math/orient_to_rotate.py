# -*- coding: utf-8 -*-
# @FileName :  orient_to_rotate.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/6/26 10:30
# @Software : PyCharm
# Description:
import math
import pymel.core.datatypes as dt
import pymel.core.nodetypes as nt

jnt = nt.Joint("elbow")
parent_jnt = jnt.getParent()

arm_matrix = parent_jnt.getMatrix(worldSpace=True)
elbow_matrix = jnt.getMatrix(worldSpace=True)
elbow_local_matrix = jnt.getMatrix(objectSpace=True)
# 对象的世界矩阵乘以它的父对象逆矩阵等于它的局部矩阵
elbow_local_matrix1 = elbow_matrix * arm_matrix.inverse()
# 获得肘关节局部矩阵的变换矩阵
elbow_local_trans_matrix = dt.TransformationMatrix(elbow_local_matrix)
elbow_rotation = [math.degrees(x) for x in elbow_local_trans_matrix.getRotation()]

jnt.jointOrient.set(0, 0, 0)
jnt.setRotation(elbow_rotation)
