# -*- coding: utf-8 -*-
"""
@FileName : switched_parent_matrix copy.py
@DateTime : 2023/07/18 17:01:18
@Author   : Tian Chao
@Contact  : tianchao0533@163.com
"""

import pymel.core as pm


def switched_parent_matrix(trans=None, rot=None, scale=None, switch_control=None):
    """创建一个可切换的矩阵约束，连接多个父对象。
    输入参数：trans（指定平移通道，接受字符串 'ALL'、'X'、'Y'、'Z'，为None时跳过平移连接），
    rot（指定旋转通道，接受字符串 'ALL'、'X'、'Y'、'Z'，为None时跳过旋转连接),
    scale（指定缩放通道，接受字符串 'ALL'、'X'、'Y'、'Z'，为None时跳过缩放连接）
    switch_control（用于控制切换的控制器，为None时创建一个默认的switchControl）。
    为了让该函数正常工作，子对象需要有一个父节点，
    如果子对象没有被父对象直接控制，则会自动创建一个父节点并连接。"""

    parents = pm.selected()
    child = parents.pop(-1)
    const_name = "{0}_switchedParentConstraint".format(child)
    channel_input_list = [trans, rot, scale]
    channel_list = [
        ["Translate", "translate"],
        ["Rotate", "rotate"],
        ["Scale", "scale"],
    ]

    enum_inputs = parents[0]
    for i in range(1, len(parents)):
        enum_inputs = enum_inputs + ":" + parents[i]

    poc = child.listRelatives(p=True, pa=True) or []
    if not poc:
        poc = pm.group(em=True, n="{0}_offsetGRP".format(child))
        mat = child.getMatrix(worldSpace=True)
        poc.setMatrix(mat, worldSpace=True)
        child.setParent(poc)

    # 创建默认switchControl
    if switch_control is None:
        switch_control = pm.circle(name="switch_control")[0]

    if not switch_control.hasAttr("parent_switch"):
        switch_control.addAttr("parent_switch", at="enum", k=True, enumName=enum_inputs)

    store_attr = "{0}.parent_switch".format(switch_control)

    mult_matrix = pm.createNode(
        "multMatrix", name="{0}_{1}_multM".format(const_name, parents[0])
    )
    choice_o_matrix = pm.createNode(
        "choice", name="{0}_offsetMat_choice".format(const_name)
    )
    choice_p_matrix = pm.createNode(
        "choice", name="{0}_parentMat_choice".format(const_name)
    )

    decomp_matrix = pm.createNode(
        "decomposeMatrix", name="{0}_{1}_decompM".format(const_name, parents[0])
    )

    # 连接choice节点后的节点网络
    mult_matrix.matrixSum >> decomp_matrix.inputMatrix
    choice_o_matrix.output >> mult_matrix.matrixIn[0]
    choice_p_matrix.output >> mult_matrix.matrixIn[1]
    poc.worldInverseMatrix[0] >> mult_matrix.matrixIn[2]
    store_attr >> choice_o_matrix.selector
    store_attr >> choice_p_matrix.selector

    # 获取子对象的worldMatrix
    child_mat = child.worldMatrix[0].get(asMatrix=True)

    for p in range(0, len(parents)):
        # 获取父对象的worldInverseMatrix并计算到子对象的偏移
        parent_mat = parents[p].worldInverseMatrix[0].get(asMatrix=True)

        offset_mat = child_mat * parent_mat

        # 建立连接父对象到其他节点的网络
        offset_mat >> choice_o_matrix.input[p]
        parents[p].worldMatrix[0] >> choice_p_matrix.input[p]

        # 连接约束通道
        for i, channel in enumerate(channel_list):
            if channel_input_list[i] and channel_input_list[i] != "ALL":
                if channel[0] in channel_input_list[i]:
                    attr = getattr(child, channel[1])
                    pm.connectAttr(
                        "{0}.output{1}".format(decomp_matrix, i),
                        "{0}.{1}".format(attr, channel[0]),
                    )

    return const_name
