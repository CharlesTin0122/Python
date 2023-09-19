# -*- coding: utf-8 -*-
'''
@FileName      : jointChildCreater.py
@DateTime      : 2023/09/19 16:43:18
@Author        : Tian Chao
@Contact       : tianchao0533@163.com
@Software      : Maya 2023.3
@PythonVersion : python 3.9.7
@Description   :
'''
import pymel.core as pm


def child_jnt_creater(jnt, child_jntname):
    """给骨骼创建子骨骼，并传递权重给子骨骼

    Args:
            jnt (str): 骨骼名称
            child_jntname (str): 子骨骼名称
    """
    pm.select(cl=True)  # 取消所有选择
    child_jnt = pm.duplicate(jnt, name=child_jntname, parentOnly=True)[
        0
    ]  # 复制骨骼为子骨骼并重命名
    pm.parent(child_jnt, jnt)  # 设置子骨骼父子关系
    skin_clusters = pm.listConnections(jnt, type="skinCluster")  # 获取蒙皮节点
    # 列表去重
    skin_list = list(set(skin_clusters))
    for skin in skin_list:
        pm.skinCluster(
            skin, edit=True, addInfluence=str(child_jnt), weight=0
        )  # 将子骨骼添加到蒙皮节点
        pm.skinCluster(skin, edit=True, selectInfluenceVerts=jnt)  # 选择父骨骼蒙皮影响的点
        pm.skinPercent(
            skin, transformMoveWeights=[jnt, child_jnt]
        )  # 传递父骨骼的蒙皮权重到子骨骼


if __name__ == "__main__":
    child_jnt_creater("pelvis", "pelvis_c")
    child_jnt_creater("spine_01", "spine_01_c")
    child_jnt_creater("spine_02", "spine_02_c")
    child_jnt_creater("spine_03", "spine_03_c")
    child_jnt_creater("neck_01", "neck_01_c")

    child_jnt_creater("clavicle_l", "clavicle_child_l")
    child_jnt_creater("upperarm_l", "upperarm_child_l")
    child_jnt_creater("lowerarm_l", "lowerarm_child_l")
    child_jnt_creater("thigh_l", "thigh_child_l")
    child_jnt_creater("calf_l", "calf_child_l")

    child_jnt_creater("clavicle_r", "clavicle_child_r")
    child_jnt_creater("upperarm_r", "upperarm_child_r")
    child_jnt_creater("lowerarm_r", "lowerarm_child_r")
    child_jnt_creater("thigh_r", "thigh_child_r")
    child_jnt_creater("calf_r", "calf_child_r")
