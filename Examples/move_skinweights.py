# -*- coding: utf-8 -*-
"""
@FileName    :   jointChildCreater.py
@DateTime    :   2023/02/27 16:07:43
@Author  :   Tian Chao
@Contact :   tianchao0533@163.com
"""

import pymel.core as pm


def move_skin_weights(jnt: str, other_jnt: str) -> None:
    """
    两个骨骼之间互换蒙皮权重
    Args:
            jnt: 移动权重的骨骼
            other_jnt: 被移动权重的骨骼

    Returns:None

    """
    pm.select(cl=True)  # 取消所有选择
    skin_cluster = pm.listConnections(jnt, type="skinCluster")[0]  # 获取蒙皮节点
    pm.skinCluster(skin_cluster, edit=True, selectInfluenceVerts=jnt)  # 选择父骨骼蒙皮影响的点
    pm.skinPercent(
        skin_cluster, transformMoveWeights=[jnt, other_jnt]
    )  # 传递父骨骼的蒙皮权重到子骨骼


move_skin_weights("pelvis", "pelvis_c")
move_skin_weights("spine_01", "spine_01_c")
move_skin_weights("spine_02", "spine_02_c")
move_skin_weights("spine_03", "spine_03_c")
move_skin_weights("neck_01", "neck_01_c")

move_skin_weights("clavicle_l", "clavicle_child_l")
move_skin_weights("upperarm_l", "upperarm_child_l")
move_skin_weights("lowerarm_l", "lowerarm_child_l")
move_skin_weights("thigh_l", "thigh_child_l")
move_skin_weights("calf_l", "calf_child_l")

move_skin_weights("clavicle_r", "clavicle_child_r")
move_skin_weights("upperarm_r", "upperarm_child_r")
move_skin_weights("lowerarm_r", "lowerarm_child_r")
move_skin_weights("thigh_r", "thigh_child_r")
move_skin_weights("calf_r", "calf_child_r")
