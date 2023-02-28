# -*- coding: utf-8 -*-
'''
@FileName    :   quadruped_Auto_Rig.py
@DateTime    :   2023/02/15 14:07:21
@Author  :   Tian Chao 
@Contact :   tianchao0533@163.com
'''

'''Quadruped Auto Rig'''
import sys
sys.path.append(r'G:\Code\Python\quadrupedRigging')
from ctrl_creater import *
import pymel.core as pm

'''-----------------------------------------------Placement locs----------------------------------------------- '''
def placementLoc(name,tx,ty,tz,colorId=0):
	loc = pm.spaceLocator(n=name)
	loc.translate.set((tx,ty,tz))
	loc.overrideEnabled.set(1)
	loc.overrideColor.set(colorId)
	loc.getShape().localScale.set(10,10,10)
	return loc
	
### hindLegsLocs

hindToe = placementLoc('L_hindToe_Loc',15,0,-70,15)
hindAnkle = placementLoc('L_hindAnkle_Loc',15,25,-78,15)
hindknee = placementLoc('L_hindKnee_Loc',15,63,-76,15)
hindUpperKnee = placementLoc('L_hindUpperKnee_Loc',15,90,-55,15)
hindFemur = placementLoc('L_hindFemure_Loc',15,116,-62,15)
hindPelvis = placementLoc('L_hindPelvis_Loc',0,145,-48,17)

hindLocGrp = pm.group(
								hindToe,
								hindAnkle,
								hindknee,
								hindUpperKnee,
								hindFemur,
								hindPelvis,
								n='hindPlacement_GRP',
								w=True
								)
hindLocGrp.zeroTransformPivots()

### frontLegsLocs

frontToe = placementLoc('L_frontToe_Loc',15,0,77,15)
frontAnkle = placementLoc('L_frontAnkle_Loc',15,22,67,15)
frontknee = placementLoc('L_frontKnee_Loc',15,53,68,15)
frontUpperKnee = placementLoc('L_frontUpperKnee_Loc',15,96,63,15)
frontFemur = placementLoc('L_frontFemure_Loc',15,126,72,15)
frontPelvis = placementLoc('L_frontPelvis_Loc',0,145,60,17)

frontLocGrp = pm.group(
								frontToe,
								frontAnkle,
								frontknee,
								frontUpperKnee,
								frontFemur,
								frontPelvis,
								n='frontPlacement_GRP',
								w=True
								)
frontLocGrp.zeroTransformPivots()

### neckLocs

neckRoot = placementLoc('neckRoot_Loc',0,150,78,17)
neckEnd = placementLoc('neckEnd_Loc',0,186,126,17)

neckLocGrp = pm.group(
					neckRoot,
					neckEnd,
					n='neckPlacement_GRP',
					w=True
					)
neckLocGrp.zeroTransformPivots()

### tailLocs

tailRoot = placementLoc('tailRoot_Loc',0,145,-83,17)
tailEnd = placementLoc('tailEnd_Loc',0,145,-158,17)

tailLocGrp = pm.group(
								tailRoot,
								tailEnd,
								n='tailPlacement_GRP',
								w=True
								)
tailLocGrp.zeroTransformPivots()

### Finalize Placement Loc Module
mainLocGrp = pm.group(
                     hindLocGrp,
                     frontLocGrp,
                     neckLocGrp,
                     tailLocGrp,
                     n='mainPlacementLoc_GRP'
                     )
mainLocGrp.zeroTransformPivots()

'''--------------------------------------------Creat Joint---------------------------------------------'''

def placementJoint(jointName,targetObj):
	pm.select(cl=True)
	tempJoint = pm.joint(n=jointName)
	ConNod = pm.pointConstraint(targetObj,tempJoint,weight=1,offset=(0,0,0))
	pm.delete(ConNod)
	pm.select(cl=True)
	return tempJoint

L_hindToeJnt = placementJoint('L_hindToe_JNT',hindToe)
L_hindAnkleJnt = placementJoint('L_hindAnkle_JNT',hindAnkle)
L_hindkneeJnt = placementJoint('L_hindknee_JNT',hindknee)
L_hindUpperKneeJnt = placementJoint('L_hindUpperKnee_JNT',hindUpperKnee)
L_hindFemurJnt = placementJoint('L_hindFemur_JNT',hindFemur)


L_frontToeJnt = placementJoint('L_frontToe_JNT',frontToe)
L_frontAnkleJnt = placementJoint('L_frontAnkle_JNT',frontAnkle)
L_frontkneeJnt = placementJoint('L_frontknee_JNT',frontknee)
L_frontUpperKneeJnt = placementJoint('L_frontUpperKnee_JNT',frontUpperKnee)
L_frontFemurJnt = placementJoint('L_frontFemur_JNT',frontFemur)


hindPelvisJnt = placementJoint('hindPelvis_JNT',hindPelvis)
frontPelvisJnt = placementJoint('frontPelvis_JNT',frontPelvis)
neckRootJnt = placementJoint('neckRoot_JNT',neckRoot)
neckEndJnt = placementJoint('neckEnd_JNT',neckEnd)
tailRootJnt = placementJoint('tailRoot_JNT',tailRoot)
tailEndJnt = placementJoint('tailEnd_JNT',tailEnd)

### Mirror Joint
R_hindToeJnt = pm.duplicate('L_hindToe_JNT',n='R_hindToe_JNT')[0]
R_hindToeJnt.tx.set(R_hindToeJnt.tx.get()*-1)
R_hindAnkleJnt = pm.duplicate('L_hindAnkle_JNT',n='R_hindAnkle_JNT')[0]
R_hindAnkleJnt.tx.set(R_hindAnkleJnt.tx.get()*-1)
R_hindkneeJnt = pm.duplicate('L_hindknee_JNT',n='R_hindknee_JNT')[0]
R_hindkneeJnt.tx.set(R_hindkneeJnt.tx.get()*-1)
R_hindUpperKneeJnt = pm.duplicate('L_hindUpperKnee_JNT',n='R_hindUpperKnee_JNT')[0]
R_hindUpperKneeJnt.tx.set(R_hindUpperKneeJnt.tx.get()*-1)
R_hindFemurJnt = pm.duplicate('L_hindFemur_JNT',n='R_hindFemur_JNT')[0]
R_hindFemurJnt.tx.set(R_hindFemurJnt.tx.get()*-1)


R_frontToeJnt = pm.duplicate('L_frontToe_JNT',n='R_frontToe_JNT')[0]
R_frontToeJnt.tx.set(R_frontToeJnt.tx.get()*-1)
R_frontAnkleJnt = pm.duplicate('L_frontAnkle_JNT',n='R_frontAnkle_JNT')[0]
R_frontAnkleJnt.tx.set(R_frontAnkleJnt.tx.get()*-1)
R_frontkneeJnt = pm.duplicate('L_frontknee_JNT',n='R_frontknee_JNT')[0]
R_frontkneeJnt.tx.set(R_frontkneeJnt.tx.get()*-1)
R_frontUpperKneeJnt = pm.duplicate('L_frontUpperKnee_JNT',n='R_frontUpperKnee_JNT')[0]
R_frontUpperKneeJnt.tx.set(R_frontUpperKneeJnt.tx.get()*-1)
R_frontFemurJnt = pm.duplicate('L_frontFemur_JNT',n='R_frontFemur_JNT')[0]
R_frontFemurJnt.tx.set(R_frontFemurJnt.tx.get()*-1)


###Parent Joint
def parentJoint(jointList):
	for i in range(len(jointList)-1):
		pm.parent(jointList[i],jointList[i+1])

L_frontLeg_jontList = [L_frontToeJnt,L_frontAnkleJnt,L_frontkneeJnt,
					L_frontUpperKneeJnt,L_frontFemurJnt,frontPelvisJnt]
L_hindLeg_jontList = [L_hindToeJnt,L_hindAnkleJnt,L_hindkneeJnt,
						L_hindUpperKneeJnt,L_hindFemurJnt,hindPelvisJnt]
R_frontLeg_jontList = [R_frontToeJnt,R_frontAnkleJnt,R_frontkneeJnt,
						R_frontUpperKneeJnt,R_frontFemurJnt,frontPelvisJnt]
R_hindLeg_jontList = [R_hindToeJnt,R_hindAnkleJnt,R_hindkneeJnt,
						R_hindUpperKneeJnt,R_hindFemurJnt,hindPelvisJnt]

parentJoint(L_frontLeg_jontList)
parentJoint(L_hindLeg_jontList)
parentJoint(R_frontLeg_jontList)
parentJoint(R_hindLeg_jontList)

#set last joint
lastjoint = [L_frontToeJnt,L_hindToeJnt,R_frontToeJnt,R_hindToeJnt]
for jnt in lastjoint:
	dupJnt=pm.duplicate(jnt,n='{}_last'.format(jnt))
	pm.parent(dupJnt[0],jnt)
	dupJnt[0].tz.set(1)
	dupJnt[0].v.set(0)

#set joint orient
topJoint = [L_frontFemurJnt,L_hindFemurJnt,R_frontFemurJnt,R_hindFemurJnt]
for jnt in topJoint:
	pm.joint(jnt,zso=1, ch=1, e=1, oj='xyz', secondaryAxisOrient='yup')

#create Rename Function

def renameChildJoint(jnt,oldStr,newStr):
	pm.select(jnt,r=True,hi=True)
	childjntList = pm.selected()[1:]
	for jnt in childjntList:
		newName=jnt.split('|')[-1].replace(oldStr,newStr)
		jnt.rename(newName)
	return childjntList

#create IK,FK Joint
L_hindLeg_FkJntList = pm.duplicate(L_hindFemurJnt,n='L_hindFemur_FK_JNT')
L_hindLeg_FkJntChild = renameChildJoint(L_hindLeg_FkJntList[0],'_JNT','_FK_JNT')
for obj in L_hindLeg_FkJntChild:
	L_hindLeg_FkJntList.append(obj)

L_frontLeg_FkJntList = pm.duplicate(L_frontFemurJnt,n='L_frontFemur_FK_JNT')
L_frontLeg_FkJntChild = renameChildJoint(L_frontLeg_FkJntList[0],'_JNT','_FK_JNT')
for obj in L_frontLeg_FkJntChild:
	L_frontLeg_FkJntList.append(obj)

R_frontLeg_FkJntList = pm.duplicate(R_frontFemurJnt,n='R_frontFemur_FK_JNT')
R_frontLeg_FkJntChild = renameChildJoint(R_frontLeg_FkJntList[0],'_JNT','_FK_JNT')
for obj in R_frontLeg_FkJntChild:
	R_frontLeg_FkJntList.append(obj)

R_hindLeg_FkJntList = pm.duplicate(R_hindFemurJnt,n='R_hindFemur_FK_JNT')
R_hindLeg_FkJntChild = renameChildJoint(R_hindLeg_FkJntList[0],'_JNT','_FK_JNT')
for obj in R_hindLeg_FkJntChild:
	R_hindLeg_FkJntList.append(obj)

L_hindLeg_IkJntList = pm.duplicate(L_hindFemurJnt,n='L_hindFemur_IK_JNT')
L_hindLeg_IkJntChild = renameChildJoint(L_hindLeg_IkJntList[0],'_JNT','_IK_JNT')
for obj in L_hindLeg_IkJntChild:
	L_hindLeg_IkJntList.append(obj)

L_frontLeg_IkJntList = pm.duplicate(L_frontFemurJnt,n='L_frontFemur_IK_JNT')
L_frontLeg_IkJntChild = renameChildJoint(L_frontLeg_IkJntList[0],'_JNT','_IK_JNT')
for obj in L_frontLeg_IkJntChild:
	L_frontLeg_IkJntList.append(obj)

R_frontLeg_IkJntList = pm.duplicate(R_frontFemurJnt,n='R_frontFemur_IK_JNT')
R_frontLeg_IkJntChild = renameChildJoint(R_frontLeg_IkJntList[0],'_JNT','_IK_JNT')
for obj in R_frontLeg_IkJntChild:
	R_frontLeg_IkJntList.append(obj)

R_hindLeg_IkJntList = pm.duplicate(R_hindFemurJnt,n='R_hindFemur_IK_JNT')
R_hindLeg_IkJntChild = renameChildJoint(R_hindLeg_IkJntList[0],'_JNT','_IK_JNT')
for obj in R_hindLeg_IkJntChild:
	R_hindLeg_IkJntList.append(obj)

def pointMatch(obj1,obj2):
	nod = pm.pointConstraint(obj2,obj1)
	pm.delete(nod)
	pm.select(cl=1)
	
def parentMatch(obj1,obj2):
	nod = pm.parentConstraint(obj2,obj1)
	pm.delete(nod)
	pm.select(cl=1)

'''-----------------------------------------------------Create IK------------------------------------------------------------'''
###create L hind IK###

L_hindLegIk = pm.ikHandle(name='L_hindLeg_IK',sj=L_hindLeg_IkJntList[0],ee=L_hindLeg_IkJntList[-3],solver='ikRPsolver')
L_hindIkCtrl = ctrlCreater('L_hindLeg_IK_Ctrl',ik_CurInfo,6)
L_hindIkCtrl_Grp = pm.group(L_hindIkCtrl,n='L_hindLeg_IK_Ctrl_GRP')
pointMatch(L_hindIkCtrl_Grp,L_hindLeg_IkJntList[-2])
pm.parent(L_hindLegIk[0],L_hindIkCtrl)
pm.aimConstraint(L_hindIkCtrl,L_hindLeg_IkJntList[0],n='l_femur_aim_towards_footCtrl',mo=True,wu=[0,0,0])
L_hindLegToeIk = pm.ikHandle(n='L_hindLegToe_IK',sol='ikRPsolver',sj=L_hindLeg_IkJntList[-3],ee=L_hindLeg_IkJntList[-2])
pm.parent(L_hindLegToeIk[0],L_hindIkCtrl)
#create L hind IK PoleVector
L_hindIkPoleCtrl = ctrlCreater('L_hind_Ik_Pole_Ctrl',pole_CurInfo,6)
L_hindIkPoleCtrlGrp = pm.group(L_hindIkPoleCtrl,n='L_hind_Ik_Pole_Ctrl_GRP')
pointMatch(L_hindIkPoleCtrlGrp,L_hindLeg_IkJntList[2])
L_hindIkPoleCtrlGrp.tz.set(L_hindIkPoleCtrlGrp.tz.get()*2)
pm.poleVectorConstraint(L_hindIkPoleCtrl,L_hindLegIk[0])
L_hindLegIk[0].twist.set(180)

###creare R hind IK###

R_hindLegIk = pm.ikHandle(name='R_hindLeg_IK',sj=R_hindLeg_IkJntList[0],ee=R_hindLeg_IkJntList[-3],solver='ikRPsolver')
R_hindIkCtrl = ctrlCreater('R_hindLeg_IK_Ctrl',ik_CurInfo,13)
R_hindIkCtrR_Grp = pm.group(R_hindIkCtrl,n='R_hindLeg_IK_Ctrl_GRP')
pointMatch(R_hindIkCtrR_Grp,R_hindLeg_IkJntList[-2])
pm.parent(R_hindLegIk[0],R_hindIkCtrl)
pm.aimConstraint(R_hindIkCtrl,R_hindLeg_IkJntList[0],n='R_femur_aim_towards_footCtrl',mo=True,wu=[0,0,0])
R_hindLegToeIk = pm.ikHandle(n='R_hindLegToe_IK',sol='ikRPsolver',sj=R_hindLeg_IkJntList[-3],ee=R_hindLeg_IkJntList[-2])
pm.parent(R_hindLegToeIk[0],R_hindIkCtrl)

#create R hind IK PoleVector
R_hindIkPoleCtrl = ctrlCreater('R_hind_Ik_Pole_Ctrl',pole_CurInfo,13)
R_hindIkPoleCtrlGrp = pm.group(R_hindIkPoleCtrl,n='R_hind_Ik_Pole_Ctrl_GRP')
pointMatch(R_hindIkPoleCtrlGrp,R_hindLeg_IkJntList[2])
R_hindIkPoleCtrlGrp.tz.set(R_hindIkPoleCtrlGrp.tz.get()*2)
pm.poleVectorConstraint(R_hindIkPoleCtrl,R_hindLegIk[0])
R_hindLegIk[0].twist.set(180)

###creare L front IK###

L_frontLegIk = pm.ikHandle(name='L_frontLeg_IK',sj=L_frontLeg_IkJntList[0],ee=L_frontLeg_IkJntList[-3],solver='ikRPsolver')
L_frontIkCtrl = ctrlCreater('L_frontLeg_IK_Ctrl',ik_CurInfo,6)
L_frontIkCtrl_Grp = pm.group(L_frontIkCtrl,n='L_frontLeg_IK_Ctrl_GRP')
pointMatch(L_frontIkCtrl_Grp,L_frontLeg_IkJntList[-2])
pm.parent(L_frontLegIk[0],L_frontIkCtrl)
L_frontLegToeIk = pm.ikHandle(n='L_frontLegToe_IK',sol='ikRPsolver',sj=L_frontLeg_IkJntList[-3],ee=L_frontLeg_IkJntList[-2])
pm.parent(L_frontLegToeIk[0],L_frontIkCtrl)

L_frontLegRoCtrl = ctrlCreater('L_front_Leg_Rotete_Ctrl',fk_CurInfo,6)
L_frontLegRoCtrlGrp = pm.group(L_frontLegRoCtrl,n='L_front_Leg_Rotete_Ctrl_GRP')
pointMatch(L_frontLegRoCtrlGrp,L_frontLeg_IkJntList[0])

#create L front IK PoleVector
L_frontIkPoleCtrl = ctrlCreater('L_front_Ik_Pole_Ctrl',pole_CurInfo,6)
L_frontIkPoleCtrlGrp = pm.group(L_frontIkPoleCtrl,n='L_front_Ik_Pole_Ctrl_GRP')
pointMatch(L_frontIkPoleCtrlGrp,L_frontLeg_IkJntList[2])
L_frontIkPoleCtrlGrp.tz.set(0)
pm.poleVectorConstraint(L_frontIkPoleCtrl,L_frontLegIk[0])


###creare R front IK###

R_frontLegIk = pm.ikHandle(name='R_frontLeg_IK',sj=R_frontLeg_IkJntList[0],ee=R_frontLeg_IkJntList[-3],solver='ikRPsolver')
R_frontIkCtrl = ctrlCreater('R_frontLeg_IK_Ctrl',ik_CurInfo,13)
R_frontIkCtrR_Grp = pm.group(R_frontIkCtrl,n='R_frontLeg_IK_Ctrl_GRP')
pointMatch(R_frontIkCtrR_Grp,R_frontLeg_IkJntList[-2])
pm.parent(R_frontLegIk[0],R_frontIkCtrl)
R_frontLegToeIk = pm.ikHandle(n='R_frontLegToe_IK',sol='ikRPsolver',sj=R_frontLeg_IkJntList[-3],ee=R_frontLeg_IkJntList[-2])
pm.parent(R_frontLegToeIk[0],R_frontIkCtrl)

R_frontLegRoCtrl = ctrlCreater('R_front_Leg_Rotete_Ctrl',fk_CurInfo,6)
R_frontLegRoCtrlGrp = pm.group(R_frontLegRoCtrl,n='R_front_Leg_Rotete_Ctrl_GRP')
pointMatch(R_frontLegRoCtrlGrp,R_frontLeg_IkJntList[0])

#create R front IK PoleVector
R_frontIkPoleCtrl = ctrlCreater('R_front_Ik_Pole_Ctrl',pole_CurInfo,13)
R_frontIkPoleCtrlGrp = pm.group(R_frontIkPoleCtrl,n='R_front_Ik_Pole_Ctrl_GRP')
pointMatch(R_frontIkPoleCtrlGrp,R_frontLeg_IkJntList[2])
R_frontIkPoleCtrlGrp.tz.set(0)
pm.poleVectorConstraint(R_frontIkPoleCtrl,R_frontLegIk[0])

#Group IK Items
poleVectorGrp = pm.group(L_frontIkPoleCtrlGrp,R_frontIkPoleCtrlGrp,L_hindIkPoleCtrlGrp,R_hindIkPoleCtrlGrp,n='pole_Vector_GRP')
IkCtrlGrp = pm.group(poleVectorGrp,
					L_hindIkCtrl_Grp,R_hindIkCtrR_Grp,L_frontIkCtrl_Grp,R_frontIkCtrR_Grp,
					L_frontLegRoCtrlGrp,R_frontLegRoCtrlGrp,n='IK_Ctrl_Grp')
IkCtrlGrp.zeroTransformPivots()

#crtl scale founction
'''
def scaleCurShap(cvName,scaleVal=1.1):
	cvList = pm.ls('{}.cv[*]'.format(cvName))
	pm.scale(cvList,scaleVal,scaleVal,scaleVal,objectCenterPivot=True,relative=True)

selList = pm.selected()
for obj in selList:
	scaleCurShap(obj,1.25)
'''
