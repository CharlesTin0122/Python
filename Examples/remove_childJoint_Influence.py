# -*- coding: utf-8 -*-
'''
@FileName    :   removeInfluenceWeights,py
@DateTime    :   2023/03/31 10:15:56
@Author  :   Tian Chao 
@Contact :   tianchao0533@163.com
'''


def remove_childJoint_Influence(mesh, rootJoint, parentJoint):
    """
    将面部子骨骼权重赋予面部根骨骼后，移除面部子骨骼权重

    Args:
        mesh (meshtransform): 要处理的模型
        rootJoint (joint): 要处理蒙皮骨骼链的根骨骼
        parentJoint (joint): 要处理蒙皮骨骼链的父骨骼

    Returns:
        list: 要处理蒙皮骨骼链
    """
    meshVtx = pm.ls('{}.vtx[*]'.format(mesh), fl=True)  # 获取物体所有顶点
    skClu = pm.listHistory(mesh, type='skinCluster')[0]  # 获取SkinCluster
    # 锁定所有骨骼权重
    joints = pm.ls(rootJoint, dag=True, type="joint")
    for jnt in joints:
        pm.setAttr('{}.liw'.format(jnt), 1)
    # 解锁所有面部骨骼权重
    faceJnt = pm.ls(parentJoint, dag=True, type="joint")
    for jnt in faceJnt:
        pm.setAttr('{}.liw'.format(jnt), 0)
    # 物体所有顶点权重赋予面部根骨骼
    for vtx in meshVtx:
        pm.skinPercent(skClu, vtx, transformValue=(parentJoint, 1))
    # 移除面部子骨骼蒙皮
    for jnt in faceJnt[1:]:
        pm.skinCluster(skClu, e=1, removeInfluence=jnt)
    # 移除微小权重
    pm.skinPercent(skClu, mesh, pruneWeights=0.1)
    # 返回骨骼链
    return faceJnt


remove_childJoint_Influence('SK_Human_Male_001', 'root', 'face')

import pymel.core as pm

'''
此脚本用于：将面部子骨骼权重赋予面部根骨骼后，移除面部子骨骼权重
'''
mesh = pm.selected()[0]  # 获取所选物体
meshVtx = pm.ls('{}.vtx[*]'.format(mesh), fl=True)  # 获取物体所有顶点
skClu = pm.listHistory(mesh, type='skinCluster')[0]  # 获取SkinCluster
# 锁定所有骨骼权重
joints = pm.ls('root', dag=True, type="joint")
for jnt in joints:
    pm.setAttr('{}.liw'.format(jnt), 1)
# 解锁所有面部骨骼权重
faceJnt = pm.ls('parentJoint', dag=True, type="joint")
for jnt in faceJnt:
    pm.setAttr('{}.liw'.format(jnt), 0)
# 物体所有顶点权重赋予面部根骨骼
for vtx in meshVtx:
    pm.skinPercent(skClu, vtx, tv=('parentJoint', 1))
# 移除面部子骨骼蒙皮
for jnt in faceJnt[1:]:
    pm.skinCluster(skClu, e=1, ri=jnt)
# 移除微小权重
pm.skinPercent(skClu, mesh, pruneWeights=0.1)
