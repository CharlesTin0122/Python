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


def bake_selected_joints(bakeBlendshapes=False):
    startFrame = pm.playbackOptions(minTime=True, q=True)
    endFrame = pm.playbackOptions(maxTime=True, q=True)

    attrsToBake = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
    everyJoint = pm.selected(type="joint")
    everyBakeAttr = []
    for eachNode in everyJoint:
        for eachAttr in attrsToBake:
            everyBakeAttr.append(eachNode.attr(eachAttr))

        # Then include every custom attribute too:
        for eachCustomAttr in eachNode.listAttr(userDefined=True):
            everyBakeAttr.append(eachCustomAttr)

    if bakeBlendshapes:
        # Include baking all blendshapes
        targetBlendshapes = pm.selected(type="blendShape")
        for eachBlendshape in targetBlendshapes:
            for eachTarget in eachBlendshape.w:
                if eachTarget.isLocked():
                    continue
                everyBakeAttr.append(eachTarget)

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

    # Run an euler filter to help prevent flipping.
    everyRotation = [jnt.r for jnt in everyJoint]
    pm.filterCurve(everyRotation, filter="euler")


bake_selected_joints(bakeBlendshapes=True)
