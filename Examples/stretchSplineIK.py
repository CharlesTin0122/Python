# -*- coding: utf-8 -*-
'''
@FileName    :   stretchSplineIK.py
@DateTime    :   2023/03/27 09:48:20
@Author  :   Tian Chao 
@Contact :   tianchao0533@163.com
'''

import pymel.core as pm

jntChain = []# 骨骼链列表
clusterList = []# 曲线簇列表
IKCurve = None #曲线
ctrl_list = [] #控制器列表

def creatJoint(jntCount,jntLength):
	"""创建骨骼链工具

	Args:
		jntCount (int): 要创建的骨骼数量
		jntLength (float): 要创建的每节骨骼长度

	Returns:
		list: 骨骼列表
	"""
	global jntChain # 全局变量
	#遍历骨骼数量创建骨骼
	for i in range(jntCount):
		jnt = pm.joint(name='jnt_{}'.format(i+1),
					   position=((i+1)*jntLength,0,0))
		jntChain.append(jnt)
	return  jntChain # 返回骨骼链
	
def insertJointTool(rootJoint,jointCount,jointName):
	"""两节骨骼之间插入一定数量骨骼

	Args:
		rootJoint (str): 需要插入骨骼的根骨骼
		jointCount (int):要插入的骨骼数量
		jointName (str): 骨骼名称

	Returns:
		list: 骨骼链列表
	"""
	rootJointPos = rootJoint.getTranslation(space='world') #获取首根骨骼的位置
	endJointPos = rootJoint.getChildren()[0].getTranslation(space='world')#获取末端骨骼的位置
	difVal = endJointPos - rootJointPos #获取首尾骨骼位置的差值
	segmentVal = difVal / (jointCount+1)#获取每段新骨骼的差值
	pm.select(rootJoint) #选择首根骨骼
	for i in range(jointCount):
		targetJoint = pm.selected()[0] #获取所选骨骼为目标骨骼
		targetJointPos = targetJoint.getTranslation(space='world') #获取目标骨骼位置
		newJoint = pm.insertJoint(targetJoint)#在目标骨骼上插入新骨骼
		pm.joint(newJoint,component=True,edit=True,p=(targetJointPos+segmentVal))#调整新骨骼位置
	pm.select(rootJoint,hi=True)
	jntChainList = pm.selected()
	for j in range(len(jntChainList)):
		jntChainList[j].rename('{}_{}_JNT'.format(jointName,j+1)) #骨骼链重命名
	pm.joint(jntChainList[-1],zso=1, ch=1, e=1, oj='none')#调整骨骼方向
	pm.select(cl=True)#取消选择
	return jntChainList#返回骨骼链列表

def creatSplineIK(jntChain,numSpans):
	"""创建线性IK工具

	Args:
		jntChain (list): 骨骼列表
		numSpans (int): 线性IK曲线段数

	Returns:
		list: SplineIK列表
	"""
	global clusterList,ctrl_list,IKCurve # 全局变量
	#创建线性IK
	jntsplineIK = pm.ikHandle(sol='ikSplineSolver',name='tail_spline_IK',
							  ns=numSpans,sj=jntChain[0],ee=jntChain[-1])
	IKCurve = jntsplineIK[2] # 获取曲线变量
	IKCurve.rename('splineIK_curve') # 曲线重命名
	splineIKCVList = pm.ls('{}.cv[*]'.format(jntsplineIK[2]),fl=True) # 获取曲线cv点列表
	#遍历cv点创建簇
	for i in range(len(splineIKCVList)):
		cvcluster = pm.cluster(splineIKCVList[i],n='cv_cluster{}'.format(i+1))[1]
		clusterList.append(cvcluster)
	#遍历簇创建控制器
	for i in range(len(clusterList)):
		ctrl_spik = pm.circle(n='ctrl_{}'.format(i+1),nr=(1,0,0),r=2)
		ctrl_grp = pm.group(ctrl_spik,n='grp_ctrl_{}'.format(i+1))
		constrain = pm.parentConstraint(clusterList[i],ctrl_grp)
		pm.delete(constrain)
		pm.parentConstraint(ctrl_spik,clusterList[i])
		ctrl_list.append(ctrl_spik[0])
	return clusterList,IKCurve,ctrl_list

def stretchSplineIKIKJnt(jntChain,splineIKCurve):
	"""创建可拉伸线性IK

	Args:
		jntChain (list): 要创建拉伸的骨骼链
		splineIKCurve (str): 要创建拉伸的splineIK曲线
	"""
	cvShape = splineIKCurve.getShape() # 获取曲线的形节点
	cvInfo = pm.createNode('curveInfo',n='{}_info'.format(splineIKCurve)) # 创建curveInfo节点
	cvShape.worldSpace[0] >> cvInfo.inputCurve # 链接曲线的worldSpace[0]到cvInfo.inputCurve，获取曲线长度
	cvInfoMD = pm.createNode('multiplyDivide',n='{}_md'.format(splineIKCurve)) # 创建乘除节点
	cvInfo.arcLength >> cvInfoMD.input1X # 链接曲线长度arcLength到乘除节点input1X 
	cvInfoMD.input2X.set(cvInfo.arcLength.get()) # 设置乘除节点的input2X值为曲线长度，
	cvInfoMD.operation.set(2) # 设置乘除节点的类型为除法
	stretch_jntChain = jntChain[1:] #获取骨骼链列表，去除第一节骨骼，第一节骨骼无需缩放
	#遍历骨骼列表，创建乘除节点，链接节点
	for jnt in stretch_jntChain:
		mudNode = pm.createNode('multiplyDivide',n='{}_md'.format(jnt)) # 创建乘除节点
		mudNode.input2X.set(jnt.tx.get()) #设置乘除节点的input2X值为此节骨骼长度
		cvInfoMD.outputX >> mudNode.input1X # 链接曲线缩放结果到乘除节点输入口
		mudNode.outputX >> jnt.tx #链接乘除节点输出口到骨骼位移X


creatJoint(11,5)
creatSplineIK(jntChain,5)
stretchSplineIKIKJnt(jntChain,IKCurve)