# -*- coding: utf-8 -*-
# @FileName :  switched_parent_matrix.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/6/13 11:39
# @Software : PyCharm
# Description:
import maya.cmds as mc
from maya.api.OpenMaya import MMatrix


def switchedParentMatrix(trans=None, rot=None, scale=None, switchControl=None):
    """creates a switchable constraint betweenmultiple parent objects using matrixs nodes.
    Takes inputs:trans (specifies translation Channel, takes strings 'ALL', 'X','Y','Z', input None skips translation),
    rot (specifies rotation Channel, takes strings 'ALL', 'X','Y','Z', input None skips rotation),
    scale (specifies scale Channel, takes strings 'ALL', 'X','Y','Z', input None skips scale),
    control(control used to control switching, string)
    (input None will create a default switchControl with an attr that controls the switch)
    For this function to work child needs a parent node,
     this node will be created automatically if the child is parented under root"""

    parents = mc.ls(sl=True)
    child = parents.pop(-1)
    constName = "{0}_switchedParentConstraint".format(child)
    channelInputList = [trans, rot, scale]
    channelList = [['Translate', 'translate'], ['Rotate', 'rotate'], ['Scale', 'scale']]

    EnumInputs = parents[0]
    for i in range(1, len(parents)):
        EnumInputs = EnumInputs + ":" + parents[i]

    poc = mc.listRelatives(child, p=True, pa=True) or []
    if not poc:
        poc = mc.group(n="{0}_offsetGRP".format(child), em=True)
        mat = mc.xform(child, q=True, m=True, ws=True)
        mc.xform(poc, m=mat, ws=True)
        mc.parent(child, poc)

    # create default switchControll

    if switchControl is None:
        switchControl = mc.circle(name='switch_control')[0]

    if not mc.attributeQuery('parent_switch', n=switchControl, ex=True):
        mc.addAttr(switchControl, ln='parent_switch', at='enum', k=True, enumName=EnumInputs)

    storeAttr = '{0}.parent_switch'.format(switchControl)

    multMatrix = mc.createNode('multMatrix', name='{0}_{1}_multM'.format(constName, parents[0]))
    choiceOMatrix = mc.createNode('choice', name='{0}_offsetMat_choice'.format(constName))
    choicePMatrix = mc.createNode('choice', name='{0}_partentMat_choice'.format(constName))

    decompMatrix = mc.createNode('decomposeMatrix', name='{0}_{1}_decompM'.format(constName, parents[0]))

    # connecting back node network after choice nodes
    mc.connectAttr('{0}.matrixSum'.format(multMatrix), '{0}.inputMatrix'.format(decompMatrix))
    mc.connectAttr('{0}.output'.format(choiceOMatrix), '{0}.matrixIn[0]'.format(multMatrix))
    mc.connectAttr('{0}.output'.format(choicePMatrix), '{0}.matrixIn[1]'.format(multMatrix))
    mc.connectAttr('{0}.worldInverseMatrix[0]'.format(poc), '{0}.matrixIn[2]'.format(multMatrix))
    mc.connectAttr(storeAttr, '{0}.selector'.format(choiceOMatrix))
    mc.connectAttr(storeAttr, '{0}.selector'.format(choicePMatrix))

    # finding childs worldMatrix
    childMat = MMatrix(mc.getAttr('{0}.worldMatrix[0]'.format(child)))

    for p in range(0, len(parents)):
        # finding parent worldInverseMatrix and calculating offset to child
        parentMat = MMatrix(mc.getAttr('{0}.worldInverseMatrix[0]'.format(parents[p])))

        offsetMat = childMat * parentMat

        # building network to connect parent to other nodes
        mc.addAttr(switchControl, ln='{0}x{1}_offsetMatrix'.format(parents[p], child), at='matrix', h=True)
        mc.setAttr('{0}.{1}x{2}_offsetMatrix'.format(switchControl, parents[p], child), offsetMat, type='matrix')

        mc.connectAttr('{0}.{1}x{2}_offsetMatrix'.format(switchControl, parents[p], child),
                       '{0}.input[{1}]'.format(choiceOMatrix, p))
        mc.connectAttr('{0}.worldMatrix[0]'.format(parents[p]), '{0}.input[{1}]'.format(choicePMatrix, p))

    # determine which channels are connected
    for c in range(0, len(channelInputList)):
        if channelInputList[c] is None:
            pass
        elif channelInputList[c] == 'ALL':
            mc.connectAttr('{0}.output{1}'.format(decompMatrix, channelList[c][0]),
                           '{0}.{1}'.format(child, channelList[c][1]))
        elif channelInputList[c] == 'X' or 'Y' or 'Z':
            mc.connectAttr('{0}.output{1}{2}'.format(decompMatrix, channelList[c][0], channelInputList[c]),
                           '{0}.{1}{2}'.format(child, channelList[c][1], channelInputList[c]))
        else:
            _logger.Error('trans, rot or scale set to invalid value, takes only strings ALL, X, Y, Z and None')


switchedParentMatrix(trans="ALL", rot="ALL", scale=None, switchControl=None)
