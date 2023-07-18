# -*- coding: utf-8 -*-
"""
@FileName : meshAnim2JntAnim.py
@DateTime : 2023/07/14 16:59:11
@Author   : Tian Chao
@Contact  : tianchao0533@163.com
"""

import pymel.core as pm


def meshanim2jntanim():
    """
    模型变形动画转骨骼动画：
    选中要操作的模型
    设置好要转换动画的时间栏
    执行此函数即可

    Raises:
        RuntimeError: 模型选择错误
        TypeError: 模型类型错误

    Returns:
        list: 骨骼列表
    """
    pm.currentUnit(time="ntsc")  # 设置环境为30fps
    time_start = pm.playbackOptions(q=True, min=True)  # 获取初始帧
    time_end = pm.playbackOptions(q=True, max=True)  # 获取末尾帧
    pm.currentTime(time_start)  # 设置当前帧为起始帧

    sel_obj = pm.selected()  # 获取选择物体
    if len(sel_obj) != 1:
        raise RuntimeError("请仅选择一个模型作为操作对象")
    sel_mesh = sel_obj[0]
    sel_shape = sel_mesh.getShape()  # 获取该物体形节点
    if not isinstance(sel_shape, pm.nodetypes.Mesh):
        raise TypeError("所选物体不是有效的模型")
    mesh_vtxs = sel_shape.vtx  # 获取所有顶点
    pm.select(clear=True)

    mesh_RotatePivot = sel_mesh.getRotatePivot()
    root_jnt = pm.joint(name="root", radius=0.1, position=mesh_RotatePivot)  # 创建根骨骼

    # 定义列表变量用于接收骨骼列表
    jnt_list = []
    # 给每个顶点位置创建一个骨骼，并设置根骨骼为父骨骼
    for i, vtx in enumerate(mesh_vtxs):
        vtx_pos = vtx.getPosition()
        jnt_pnt = pm.joint(name=f"jnt_{i}", position=vtx_pos, radius=0.1, ch=False)
        pm.select(root_jnt, replace=True)
        jnt_list.append(jnt_pnt)
    # 时间栏的每一帧将骨骼移动到对应顶点移动到的位置，并给骨骼设置动画
    for frame in range(int(time_start), int(time_end) + 1):
        pm.currentTime(frame)
        for i, vtx in enumerate(mesh_vtxs):
            vtx_pos = vtx.getPosition()
            pm.joint(jnt_list[i], edit=True, position=vtx_pos)
        pm.setKeyframe(jnt_list)

    return jnt_list


if __name__ == "__main__":
    jnt_anim = meshanim2jntanim()
