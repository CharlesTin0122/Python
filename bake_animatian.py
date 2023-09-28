# -*- coding: utf-8 -*-
"""
@FileName    :   bake_animatian.py
@DateTime    :   2023/06/14 12:09:50
@Author  :   Tian Chao
@Contact :   tianchao0533@163.com
"""

import pymel.core as pm

# bake_selected_joints.py

# A simple helper script to bake selected joints.
# This automatically chooses all the attributes, so the animator
# Doesn't have to manually choose settings each time.

# TODO: It would be nice to have a little GUI so the animator can choose settings, like range.


def bake_selected_joints(everyJoint: list, bakeBlendshapes: bool = False):
    """为所选骨骼烘焙关键帧

    Args:
        bakeBlendshapes (bool, optional): 是否烘焙融合变形. Defaults to False.
    """
    # 设定起止帧
    startFrame = pm.playbackOptions(minTime=True, q=True)
    endFrame = pm.playbackOptions(maxTime=True, q=True)
    # 设定需要烘焙的动画属性。分别为位移，旋转，缩放
    attrsToBake = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
    # 设定需要烘焙的骨骼和骨骼属性
    if not everyJoint:
        everyJoint = pm.selected(type="joint")
    everyBakeAttr = []
    # 要需要烘焙的每根骨骼的每个属性放入everyBakeAttr变量
    for eachJoint in everyJoint:
        for eachAttr in attrsToBake:
            everyBakeAttr.append(eachJoint.attr(eachAttr))

        # 也包括自定义属性
        for eachCustomAttr in eachJoint.listAttr(userDefined=True):
            everyBakeAttr.append(eachCustomAttr)
    # 如果烘焙融合变形
    if bakeBlendshapes:
        # Include baking all blendshapes
        targetBlendshapes = pm.selected(type="blendShape")
        for eachBlendshape in targetBlendshapes:
            for eachTarget in eachBlendshape.w:
                if eachTarget.isLocked():
                    continue
                everyBakeAttr.append(eachTarget)
    # 烘焙关键帧
    pm.bakeResults(
        everyBakeAttr,
        simulation=True,
        shape=False,
        sampleBy=1,
        sparseAnimCurveBake=False,
        bakeOnOverrideLayer=False,
        removeBakedAnimFromLayer=True,
        # resolveWithoutLayer=cmds.ls(type='animLayer'),
        t=(startFrame, endFrame),
    )

    # 执行欧拉过滤器以防止动画曲线翻转
    everyRotation = [jnt.r for jnt in everyJoint]
    pm.filterCurve(everyRotation, filter="euler")


if __name__ == "__main__":
    jnt_list = pm.selected(type="joint")
    bake_selected_joints(jnt_list)
