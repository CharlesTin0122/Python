# -*- coding: utf-8 -*-
'''
@FileName    :   quadruped_Auto_Rig.py
@DateTime    :   2023/02/15 14:07:21
@Author  :   Tian Chao 
@Contact :   tianchao0533@163.com
'''

'''Quadruped Auto Rig'''

import pymel.core as pm

'''Placement locs '''

def placementLoc(name,tx,ty,tz,colorInd):
	loc = pm.spaceLocator(n=name)
	loc.translate.set((tx,ty,tz))
	loc.overrideEnabled.set(1)
	loc.overrideColor.set(colorInd)
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
frontknee = placementLoc('L_frontKnee_Loc',15,53,66,15)
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

### Creat Joint

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

#create IK joint

def ikJointCreater(jnt,oldStr,newStr):
	tempName = jnt[0].replace(oldStr,newStr)
	IKJnt = pm.duplicate(jnt,n='{}'.format(tempName))
	pm.select(IKJnt[0],r=True,hi=True)
	childjntList = pm.selected()
	for jnt in childjntList[1:]:
		newName=jnt.split('|')[-1].replace(oldStr,newStr)
		jnt.rename(newName)
		IKJnt.append(jnt)
	return IKJnt
	
L_hindLeg_IKJntList = ikJointCreater(L_hindFemurJnt,'_JNT','_IK_JNT')
L_frontLeg_IKJntList = ikJointCreater(L_frontFemurJnt,'_JNT','_IK_JNT')
R_frontLeg_IKJntList = ikJointCreater(R_hindFemurJnt,'_JNT','_IK_JNT')
R_hindLeg_IKJntList = ikJointCreater(R_frontFemurJnt,'_JNT','_IK_JNT')
