# -*- coding: utf-8 -*-
# @FileName :  poleVector_position.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/6/25 12:06
# @Software : PyCharm
# Description:利用向量来计算极向量约束控制器的位置
import pymel.core.nodetypes as nt


def get_pole_vector_position(jnt1_name, jnt2_name, jnt3_name, pole_vector_ctrl):
    """
    利用向量来计算极向量约束控制器的位置
    Args:
        jnt1_name (str): 第一节骨骼名称
        jnt2_name (str): 第二节骨骼名称
        jnt3_name (str): 第三节骨骼名称
        pole_vector_ctrl (str): 极向量控制器名称

    Returns:None

    """
    pv = nt.Transform(pole_vector_ctrl)

    hip_jnt = nt.Joint(jnt1_name)
    hip_pose = hip_jnt.getTranslation(ws=True)
    knee_jnt = nt.Joint(jnt2_name)
    knee_pose = knee_jnt.getTranslation(ws=True)
    foot_jnt = nt.Joint(jnt3_name)
    foot_pose = foot_jnt.getTranslation(ws=True)

    hip_to_foot = foot_pose - hip_pose  # 通过脚部向量和胯部向量之差得到脚胯之间的向量
    hip_to_foot_scaled = hip_to_foot / 2  # 向量差除以二，得到脚胯之间向量的中点，此时向量起点为原点
    mid_point = hip_pose + hip_to_foot_scaled  # 通过向量和，将脚胯之间向量的一半移动到脚胯之间
    mid_point_to_knee = knee_pose - mid_point  # 通过膝盖向量和脚胯之间向量的一半只差，得到脚胯之间向量的一半到膝盖的向量
    mid_point_to_knee_scaled = mid_point_to_knee * 2  # 放大该向量为原来的两倍
    mid_point_to_knee_point = mid_point + mid_point_to_knee_scaled  # 将缩放后的向量移动到正确的位置

    pv.setTranslation(mid_point_to_knee_point)


if __name__ == '__main__':
    get_pole_vector_position("hip", "knee", "ankle", "pv")
