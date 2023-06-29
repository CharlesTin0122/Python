# -*- coding: utf-8 -*-
# @FileName :  poleVector_position.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/6/25 12:06
# @Software : PyCharm
# Description:利用向量来计算极向量约束控制器的位置
import pymel.core as pm


def get_pole_vector_position(jnt1, jnt2, jnt3, pv_ctrl, ctrl_length_scale=1.0):
    """
    利用向量来计算极向量约束控制器的位置
    Args:
        jnt1 (nt.Joint): 第一节骨骼名称
        jnt2 (nt.Joint): 第二节骨骼名称
        jnt3 (nt.Joint): 第三节骨骼名称
        pv_ctrl (nt.Transform): 极向量控制器名称
        ctrl_length_scale (float): 极向量控制器和骨骼距离的缩放值

    Returns: Vector

    """
    # 获取参数，并转换为Pymel对象
    jnt1_vec = jnt1.getTranslation(ws=True)
    jnt2_vec = jnt2.getTranslation(ws=True)
    jnt3_vec = jnt3.getTranslation(ws=True)
    # 获取胯骨指向脚的向量
    leg_foot_vec = jnt3_vec - jnt1_vec
    # 获取胯骨指向膝盖的向量的向量
    leg_knee_vec = jnt2_vec - jnt1_vec
    # 将胯膝向量向腿脚向量投影，获得该投影位置
    knee_projection_vec = leg_knee_vec.projectionOnto(leg_foot_vec)
    # 将投影向量移动到腿上，之前向量起点为原点
    mid_position = jnt1_vec + knee_projection_vec
    # 获得投影点指向膝盖点的向量，再乘以一个缩放系数，得到极向量，再讲极向量移动到膝盖点
    ctrl_position = jnt2_vec + (jnt2_vec - mid_position) * ctrl_length_scale
    # 设置控制器位置
    pv_ctrl.setTranslation(ctrl_position)
    return ctrl_position


if __name__ == '__main__':
    """依次选择三个骨骼对象和一个控制器对象，然后执行脚本，
    控制器就被摆放在正确的位置上,通过ctrl_length_scale数值来调整控制器和骨骼距离。
    """
    jnt_1, jnt_2, jnt_3, ctrl_pv = pm.selected()
    get_pole_vector_position(jnt_1, jnt_2, jnt_3, ctrl_pv, 1.5)
