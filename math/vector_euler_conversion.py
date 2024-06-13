# -*- coding: utf-8 -*-
"""
@FileName      : vector_euler_conversion.py
@DateTime      : 2024/06/12 20:44:24
@Author        : Tian Chao
@Contact       : tianchao0533@163.com
@Software      : Maya 2024.2
@PythonVersion : python 3.10.8
@librarys      : pymel 1.4.0
@Description   :
"""

import math
import pymel.core.datatypes as dt


def unit_vector_to_euler_angles(unit_vector, reference_vector=(1, 0, 0)):
    """单位向量到欧拉角的转化
    1. 计算旋转轴和旋转角度
        1.旋转轴:用单位向量 u 和参考向量 ref (通常是一个全局轴，如(1,0,0))之间的叉积来计算旋转轴 rotation_axis
        2.旋转角度:用单位向量 u 和参考向量之间的点积和大小来计算旋转角度。
    2.将旋转轴和角度转化为欧拉角
        1.利用旋转轴和角度，可以构造旋转矩阵或四元数，然后从旋转矩阵或四元数中提取欧拉角。
    Args:
        unit_vector (tuple): 要转化为欧拉角的单位向量.
        reference_vector (tuple, optional): 参考向量即全局轴，默认为 (1, 0, 0).

    Returns:
        tuple: 欧拉角,单位为度
    """
    # 将输入向量和参考向量转换为MVector
    u = dt.Vector(unit_vector)
    ref = dt.Vector(reference_vector)

    # 计算旋转轴:两向量叉乘得到与两向量组成平面垂直的向量，即为旋转轴
    rotation_axis = ref ^ u

    # 如果旋转轴长度为零，说明向量是平行的，不需要旋转
    if rotation_axis.length() == 0:
        return (0, 0, 0)

    # 将旋转轴归一化
    rotation_axis.normalize()

    # 计算旋转角度：angle函数用于获得两向量夹角
    angle = ref.angle(u)

    # 创建旋转四元数，参数1为旋转角度，参数2为旋转轴
    quaternion = dt.Quaternion(angle, rotation_axis)

    # 将四元数转换为欧拉旋转
    euler_rotation = quaternion.asEulerRotation()

    # 将欧拉旋转转换为向量
    vector_rotation = euler_rotation.asVector()
    # 弧度转换为度
    euler_angles = [math.degrees(x) for x in vector_rotation]
    # 返回欧拉角
    return euler_angles


def euler_angles_to_unit_vector(euler_angles, reference_vector=(1, 0, 0)):
    """从欧拉角到单位向量的转化:将欧拉角转换为旋转矩阵，然后应用旋转矩阵到单位向量
    1.计算旋转矩阵:使用欧拉角(x,y,z)按照指定顺序(如Z-Y-X)计算旋转矩阵R
    2. 应用旋转矩阵到单位向量:将单位向量u用旋转矩阵R变换 u~ = Ru
    """
    # 创建欧拉旋转对象
    euler_rotation = dt.EulerRotation(
        math.radians(euler_angles[0]),
        math.radians(euler_angles[1]),
        math.radians(euler_angles[2]),
    )

    # 转换为旋转矩阵
    rotation_matrix = euler_rotation.asMatrix()

    # 将参考向量转换为Vector
    ref = dt.Vector(reference_vector)

    # 应用旋转矩阵到参考向量
    rotated_vector = ref * rotation_matrix

    return rotated_vector


# 示例使用欧拉角 (30, 45, 60)
euler_angles = (30, 45, 60)

unit_vector = euler_angles_to_unit_vector(euler_angles)
