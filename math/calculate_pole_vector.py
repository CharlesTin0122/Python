# -*- coding: utf-8 -*-
"""
@FileName    :   calculate_pole_vector.py
@DateTime    :   2023/06/26 14:10:01
@Author  :   Tian Chao
@Contact :   tianchao0533@163.com
"""

import pymel.core as pm

"""
An Autodesk Maya PyMEL script that calculates a pole vector position
based on 3 input PyNode objects. example: leg, knee, ankle bones.
Chris Lesage chris@rigmarolestudio.com
https://gist.github.com/chris-lesage/0fcc9a344f2096cf6c82a353cb735b3e
"""


def calculate_pole_vector(p1, p2, p3, poleDistance=1):
    """
        This function takes 3 PyMEL PyNodes as inputs.
    Creates a pole vector position at a "nice" distance away from a triangle of positions.
    Normalizes the bone lengths relative to the knee to calculate straight ahead
    without shifting up and down if the bone lengths are different.
    Returns a pymel.core.datatypes.Vector

    Args:
        p1 (pm.PyNode): joint
        p2 (pm.PyNode): joint
        p3 (pm.PyNode): joint
        poleDistance (int, optional): pole Vector Distance, Defaults to 1.

    Returns:
        pm.datatypes.Vector: position of pole Vector.
    """
    vec1 = p1.getTranslation(space="world")  # "hips"
    vec2 = p2.getTranslation(space="world")  # "knee"
    vec3 = p3.getTranslation(space="world")  # "ankle"

    # 1. 根据两个骨骼长度的平均值计算“合适距离”。
    legLength = (vec2 - vec1).length()  # 大腿长度
    kneeLength = (vec3 - vec2).length()  # 小腿长度
    distance = (legLength + kneeLength) * 0.5 * poleDistance  # 极向量约束控制器距离膝关节合适的距离

    # 2. 将大腿和小腿的长度相对于膝盖进行归一化
    # 这将确极向量控制器直接指向膝盖，避免了如果两根骨骼长度不同而产生的上下移动。
    """
    在给定的代码中，`vec1norm`是通过以下步骤计算得到的：

    1. `vec1 - vec2`：这表示从关节2（膝盖）指向关节1（髋关节）的向量。它表示大腿的方向和长度。
    2. `.normal()`：这是对向量进行归一化的操作，即将向量的长度缩放为1，但保持其方向不变。这样做是为了获得一个单位向量，用于后续的计算。
    3. `* distance`：将归一化后的向量乘以距离值`distance`。这样做是为了将大腿的长度调整为指定的距离，以便在极向量计算中使用。
    4. `+ vec2`：将调整后的向量与关节2（膝盖）的位置相加，以获得极向量的位置。这样极向量的起点将与关节2（膝盖）的位置重合，方向与大腿方向一致。

    因此，`vec1norm`代表了一个从关节2（膝盖）起始、方向与大腿方向一致、长度为指定距离的向量。
    在极向量计算中，它用于确保极向量的起点与关节2（膝盖）位置重合，并且指向正确的方向。
    """
    vec1norm = ((vec1 - vec2).normal() * distance) + vec2
    vec3norm = ((vec3 - vec2).normal() * distance) + vec2

    # 3. 给定三个点，计算极向量的位置
    """
    在给定的代码中，`mid`是通过以下步骤计算得到的：

    1. `vec2 - vec1norm`：这表示从归一化后的关节1位置（`vec1norm`）指向关节2位置（膝盖）的向量。它表示极向量起点到关节2（膝盖）的方向和长度。
    2. `vec3norm - vec1norm`：这表示从归一化后的关节1位置（`vec1norm`）指向归一化后的关节3位置（小腿）的向量。
        它表示关节1到关节3之间的方向向量。
    3. `.projectionOnto(vec3norm - vec1norm)`：这是对第一步得到的向量进行投影操作，将其投影到第二步得到的方向向量上。
        投影操作得到的结果是一个与第二步方向向量相同或相反的向量，表示杆矢量起点到投影点的方向和长度。
    4. `vec1norm + (vec2 - vec1norm).projectionOnto(vec3norm - vec1norm)`：
        这将归一化后的关节1位置（`vec1norm`）与第三步计算得到的投影向量相加，得到杆矢量的中间点位置。

    因此，`mid`表示杆矢量在关节1（髋关节）到关节3（小腿）方向上的投影点，即杆矢量起点到投影点的中间位置。
        它用于计算杆矢量的位置，确保杆矢量在正确的方向上，并且与骨骼的走向保持一致。
    """
    mid = vec1norm + (vec2 - vec1norm).projectionOnto(vec3norm - vec1norm)

    # 4. 将极向量向膝盖前方移动指定的“合适距离”。
    midPointer = vec2 - mid
    poleVector = (midPointer.normal() * distance) + vec2

    return poleVector


if __name__ == "__main__":
    poleControl = pm.PyNode('poleVector_ctrl')
    p1 = pm.PyNode('leg_bone')
    p2 = pm.PyNode('knee_bone')
    p3 = pm.PyNode('ankle_bone')

    polePosition = calculate_pole_vector(p1, p2, p3, poleDistance=1)
    poleControl.setTranslation(polePosition, space='world')
