# -*- coding: utf-8 -*-
'''
@FileName    :   jointChildCreater.py
@DateTime    :   2023/02/27 16:07:43
@Author  :   Tian Chao 
@Contact :   tianchao0533@163.com
'''

import pymel.core as pm

def childJntCreater(jnt,childJntname):
	"""给骨骼创建子骨骼，并传递权重给子骨骼

	Args:
		jnt (str): 骨骼名称
		childJntname (str): 子骨骼名称
	"""
	pm.select(cl=True) #取消所有选择
	childJnt = pm.duplicate(jnt,name=childJntname,parentOnly=True)[0] #复制骨骼为子骨骼并重命名
	pm.parent(childJnt,jnt) #设置子骨骼父子关系
	skin_cluster = pm.listConnections(jnt, type='skinCluster')[0] #获取蒙皮节点
	pm.skinCluster(skin_cluster, edit=True, addInfluence=childJnt, weight=0) #将子骨骼添加到蒙皮节点
	pm.skinCluster(skin_cluster, edit=True, selectInfluenceVerts=jnt) #选择父骨骼蒙皮影响的点
	pm.skinPercent(skin_cluster, transformMoveWeights=[jnt, childJnt]) #传递父骨骼的蒙皮权重到子骨骼

childJntCreater('pelvis','pelvis_c')
childJntCreater('spine_01','spine_01_c')
childJntCreater('spine_02','spine_02_c')
childJntCreater('spine_03','spine_03_c')
childJntCreater('neck_01','neck_01_c')

childJntCreater('clavicle_l','clavicle_child_l')
childJntCreater('upperarm_l','upperarm_child_l')
childJntCreater('lowerarm_l','lowerarm_child_l')
childJntCreater('thigh_l','thigh_child_l')
childJntCreater('calf_l','calf_child_l')

childJntCreater('clavicle_r','clavicle_child_r')
childJntCreater('upperarm_r','upperarm_child_r')
childJntCreater('lowerarm_r','lowerarm_child_r')
childJntCreater('thigh_r','thigh_child_r')
childJntCreater('calf_r','calf_child_r')
