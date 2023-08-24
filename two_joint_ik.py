# -*- coding: utf-8 -*-
'''
@FileName      : two_joint_ik.py
@DateTime      : 2023/08/15 14:51:44
@Author        : Tian Chao
@Contact       : tianchao0533@163.com
@Software      : Maya 2023.3
@PythonVersion : python 3.9.7
'''
import numpy as np
import math


def two_joint_ik(a, b, c, t, eps, a_gr, b_gr, a_lr, b_lr):
    """
    计算两个关节系统的反向运动学（IK）。

    参数:
        a (numpy.ndarray): 关节A的坐标.
        b (numpy.ndarray): 关节B的坐标.
        c (numpy.ndarray): 关节C的坐标C.
        t (numpy.ndarray): 目标坐标.
        eps (float): 用于剪切的 epsilon 值.
        a_gr (float): 关节A的旋转角度.
        b_gr (float): 关节B的旋转角度.
        a_lr (float): 关节A的局部旋转角度.
        b_lr (float): 关节B的局部旋转角度.

    返回:
        None
    """
    # 计算关节 A 和关节 B 之间的长度
    lab = np.linalg.norm(b - a)
    lcb = np.linalg.norm(b - c)

    # 计算目标坐标在线段 AB 上的投影长度
    lat = np.clip(np.linalg.norm(t - a), eps, lab + lcb - eps)

    # 计算关节 A、B 和 C 形成的三角形的初始角度
    ac_ab_0 = np.arccos(np.clip(np.dot((c - a) / np.linalg.norm(c - a), (b - a) / np.linalg.norm(b - a)), -1, 1))
    ba_bc_0 = np.arccos(np.clip(np.dot((a - b) / np.linalg.norm(a - b), (c - b) / np.linalg.norm(c - b)), -1, 1))
    ac_at_0 = np.arccos(np.clip(np.dot((c - a) / np.linalg.norm(c - a), (t - a) / np.linalg.norm(t - a)), -1, 1))

    # 计算更新后的角度
    ac_ab_1 = np.arccos(np.clip((lcb*lcb-lab*lab-lat*lat) / (-2*lab*lat), -1, 1))
    ba_bc_1 = np.arccos(np.clip((lat*lat-lab*lab-lcb*lcb) / (-2*lab*lcb), -1, 1))

    # 计算旋转轴
    axis0 = np.cross(c - a, b - a)
    axis1 = np.cross(c - a, t - a)

    # 计算旋转矩阵
    r0 = np.array([math.cos(ac_ab_1 - ac_ab_0), *axis0]) * np.array([math.sin(ac_ab_1 - ac_ab_0), *axis0])
    r1 = np.array([math.cos(ba_bc_1 - ba_bc_0), *axis0]) * np.array([math.sin(ba_bc_1 - ba_bc_0), *axis0])
    r2 = np.array([math.cos(ac_at_0), *axis1]) * np.array([math.sin(ac_at_0), *axis1])

    # 更新关节 A 和 B 的局部旋转角度
    a_lr = np.quaternion(*a_lr) * np.quaternion(*r0) * np.quaternion(*r2)
    b_lr = np.quaternion(*b_lr) * np.quaternion(*r1)
