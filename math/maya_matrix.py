# -*- coding: utf-8 -*-
# @FileName :  maya_matrix.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/6/25 17:17
# @Software : PyCharm
# Description:
import math
import pymel.core as pm
import pymel.core.datatypes as dt
import pymel.core.nodetypes as nt
# 手动设置矩阵
a = dt.Matrix([
	[3.1324578069247884, 0.29919305978615185, 0.7407371045155786, 0.0],
	[-0.19225011009577528, 3.191677834104045, -0.4761642108048981, 0.0],
	[-0.7754017282663777, 0.41734395102731425, 3.1104784267917376, 0.0],
	[-27.532081130166546, -302.4986190328789, 85.98686530544654, 1.0]
])

b = dt.Matrix(
	3.1324578069247884, 0.29919305978615185, 0.7407371045155786, 0.0,
	-0.19225011009577528, 3.191677834104045, -0.4761642108048981, 0.0,
	-0.7754017282663777, 0.41734395102731425, 3.1104784267917376, 0.0,
	-27.532081130166546, -302.4986190328789, 85.98686530544654, 1.0
)
# 获取对象矩阵
obj = nt.Transform("locator3")
cube = nt.Transform("pCube1")
obj_matrix = obj.getMatrix()
cube_matrix = cube.getMatrix()
# 设置对象矩阵
cube.setMatrix(obj_matrix)
# 矩阵相乘
multiply_mat = obj_matrix * cube_matrix
# 逆矩阵
inverse_matrix = obj_matrix.inverse()
# 将矩阵转化为变换矩阵
transformation_matrix = dt.TransformationMatrix(cube_matrix)
# 变换空间
Transform_space = dt.Space.kTransform
World_space = dt.Space.kWorld
# 获取变换矩阵元素
translation = transformation_matrix.getTranslation(Transform_space)  # 获取变换矩阵位移
scale = transformation_matrix.getScale(Transform_space)  # 获取变换矩阵缩放
rotation = [math.degrees(x) for x in transformation_matrix.getRotation()]  # 获取变换矩阵旋转，将弧度转化为度
shear = transformation_matrix.getShear(Transform_space)  # 获取变换矩阵斜切
# 设置变换矩阵元素
transformation_matrix.setTranslation(dt.Vector(1, 1, 1), Transform_space)  # 设置变换矩阵位移
# 设置变换矩阵旋转
transformation_matrix.setRotation(dt.Vector(30, 30, 30))
transformation_matrix.setScale(dt.Vector(1, 1, 1), Transform_space)  # 设置变换矩阵缩放
transformation_matrix.setShear(dt.Vector(1, 1, 1), Transform_space)  # 设置变换矩阵斜切
# 添加到变换矩阵元素
transformation_matrix.addTranslation(dt.Vector(2, 2, 2), Transform_space)  # 添加变换矩阵位移
# 添加变换矩阵旋转
rotation_order = dt.TransformationMatrix.RotationOrder.XYZ  # 设置旋转顺序为XYZ
# 添加变换矩阵旋转，参数1：旋转向量，参数2：旋转次序，参数3：空间。
transformation_matrix.addRotation(dt.Vector(30, 30, 30), rotation_order, Transform_space)
# 通过四元数添加旋转
transformation_matrix.rotateBy(dt.Quaternion(0, 0, 0, 1), Transform_space)
transformation_matrix.addScale(dt.Vector(1, 1, 1), Transform_space)  # 添加变换矩阵缩放
transformation_matrix.addShear(dt.Vector(1, 1, 1), Transform_space)  # 添加变换矩阵斜切

# 变换矩阵转化为矩阵
matrix_a = transformation_matrix.asMatrix()
cube.setMatrix(matrix_a)
