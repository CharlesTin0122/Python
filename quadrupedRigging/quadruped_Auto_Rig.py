# -*- coding: utf-8 -*-
"""
@FileName    :   quadruped_Auto_Rig.py
@DateTime    :   2023/02/15 14:07:21
@Author  :   Tian Chao
@Contact :   tianchao0533@163.com
"""

"""Quadruped Auto Rig"""
import sys

sys.path.append(r"I:\Code\Python\quadrupedRigging")
from ctrl_creater import *
import pymel.core as pm

"""-----------------------------------------------Placement locs----------------------------------------------- """


def placementLoc(name, tx, ty, tz, colorId=0):
    loc = pm.spaceLocator(n=name)
    loc.translate.set((tx, ty, tz))
    loc.overrideEnabled.set(1)
    loc.overrideColor.set(colorId)
    loc.getShape().localScale.set(10, 10, 10)
    return loc


### hindLegsLocs

hindToe = placementLoc("L_hindToe_Loc", 15, 0, -70, 15)
hindAnkle = placementLoc("L_hindAnkle_Loc", 15, 25, -78, 15)
hindknee = placementLoc("L_hindKnee_Loc", 15, 63, -76, 15)
hindUpperKnee = placementLoc("L_hindUpperKnee_Loc", 15, 90, -55, 15)
hindFemur = placementLoc("L_hindFemure_Loc", 15, 116, -62, 15)
hindPelvis = placementLoc("L_hindPelvis_Loc", 0, 145, -48, 17)

hindLocGrp = pm.group(
    hindToe,
    hindAnkle,
    hindknee,
    hindUpperKnee,
    hindFemur,
    hindPelvis,
    n="hindPlacement_GRP",
    w=True,
)
hindLocGrp.zeroTransformPivots()

### frontLegsLocs

frontToe = placementLoc("L_frontToe_Loc", 15, 0, 77, 15)
frontAnkle = placementLoc("L_frontAnkle_Loc", 15, 22, 67, 15)
frontknee = placementLoc("L_frontKnee_Loc", 15, 53, 68, 15)
frontUpperKnee = placementLoc("L_frontUpperKnee_Loc", 15, 96, 63, 15)
frontFemur = placementLoc("L_frontFemure_Loc", 15, 126, 72, 15)
frontPelvis = placementLoc("L_frontPelvis_Loc", 0, 145, 60, 17)

frontLocGrp = pm.group(
    frontToe,
    frontAnkle,
    frontknee,
    frontUpperKnee,
    frontFemur,
    frontPelvis,
    n="frontPlacement_GRP",
    w=True,
)
frontLocGrp.zeroTransformPivots()

### neckLocs

neckRoot = placementLoc("neckRoot_Loc", 0, 150, 78, 17)
neckEnd = placementLoc("neckEnd_Loc", 0, 186, 126, 17)

neckLocGrp = pm.group(neckRoot, neckEnd, n="neckPlacement_GRP", w=True)
neckLocGrp.zeroTransformPivots()

### tailLocs

tailRoot = placementLoc("tailRoot_Loc", 0, 145, -83, 17)
tailEnd = placementLoc("tailEnd_Loc", 0, 145, -158, 17)

tailLocGrp = pm.group(tailRoot, tailEnd, n="tailPlacement_GRP", w=True)
tailLocGrp.zeroTransformPivots()

### Finalize Placement Loc Module
mainLocGrp = pm.group(
    hindLocGrp, frontLocGrp, neckLocGrp, tailLocGrp, n="mainPlacementLoc_GRP"
)
mainLocGrp.zeroTransformPivots()

"""--------------------------------------------Creat Joint---------------------------------------------"""


def placementJoint(jointName, targetObj):
    pm.select(cl=True)
    tempJoint = pm.joint(n=jointName)
    ConNod = pm.pointConstraint(targetObj, tempJoint, weight=1, offset=(0, 0, 0))
    pm.delete(ConNod)
    pm.select(cl=True)
    return tempJoint


L_hindToeJnt = placementJoint("L_hindToe_JNT", hindToe)
L_hindAnkleJnt = placementJoint("L_hindAnkle_JNT", hindAnkle)
L_hindkneeJnt = placementJoint("L_hindknee_JNT", hindknee)
L_hindUpperKneeJnt = placementJoint("L_hindUpperKnee_JNT", hindUpperKnee)
L_hindFemurJnt = placementJoint("L_hindFemur_JNT", hindFemur)


L_frontToeJnt = placementJoint("L_frontToe_JNT", frontToe)
L_frontAnkleJnt = placementJoint("L_frontAnkle_JNT", frontAnkle)
L_frontkneeJnt = placementJoint("L_frontknee_JNT", frontknee)
L_frontUpperKneeJnt = placementJoint("L_frontUpperKnee_JNT", frontUpperKnee)
L_frontFemurJnt = placementJoint("L_frontFemur_JNT", frontFemur)


hindPelvisJnt = placementJoint("hindPelvis_JNT", hindPelvis)
frontPelvisJnt = placementJoint("frontPelvis_JNT", frontPelvis)
neckRootJnt = placementJoint("neckRoot_JNT", neckRoot)
neckEndJnt = placementJoint("neckEnd_JNT", neckEnd)
tailRootJnt = placementJoint("tailRoot_JNT", tailRoot)
tailEndJnt = placementJoint("tailEnd_JNT", tailEnd)

### Mirror Joint
R_hindToeJnt = pm.duplicate("L_hindToe_JNT", n="R_hindToe_JNT")[0]
R_hindToeJnt.tx.set(R_hindToeJnt.tx.get() * -1)
R_hindAnkleJnt = pm.duplicate("L_hindAnkle_JNT", n="R_hindAnkle_JNT")[0]
R_hindAnkleJnt.tx.set(R_hindAnkleJnt.tx.get() * -1)
R_hindkneeJnt = pm.duplicate("L_hindknee_JNT", n="R_hindknee_JNT")[0]
R_hindkneeJnt.tx.set(R_hindkneeJnt.tx.get() * -1)
R_hindUpperKneeJnt = pm.duplicate("L_hindUpperKnee_JNT", n="R_hindUpperKnee_JNT")[0]
R_hindUpperKneeJnt.tx.set(R_hindUpperKneeJnt.tx.get() * -1)
R_hindFemurJnt = pm.duplicate("L_hindFemur_JNT", n="R_hindFemur_JNT")[0]
R_hindFemurJnt.tx.set(R_hindFemurJnt.tx.get() * -1)


R_frontToeJnt = pm.duplicate("L_frontToe_JNT", n="R_frontToe_JNT")[0]
R_frontToeJnt.tx.set(R_frontToeJnt.tx.get() * -1)
R_frontAnkleJnt = pm.duplicate("L_frontAnkle_JNT", n="R_frontAnkle_JNT")[0]
R_frontAnkleJnt.tx.set(R_frontAnkleJnt.tx.get() * -1)
R_frontkneeJnt = pm.duplicate("L_frontknee_JNT", n="R_frontknee_JNT")[0]
R_frontkneeJnt.tx.set(R_frontkneeJnt.tx.get() * -1)
R_frontUpperKneeJnt = pm.duplicate("L_frontUpperKnee_JNT", n="R_frontUpperKnee_JNT")[0]
R_frontUpperKneeJnt.tx.set(R_frontUpperKneeJnt.tx.get() * -1)
R_frontFemurJnt = pm.duplicate("L_frontFemur_JNT", n="R_frontFemur_JNT")[0]
R_frontFemurJnt.tx.set(R_frontFemurJnt.tx.get() * -1)


###Parent Joint
def parentJoint(jointList):
    for i in range(len(jointList) - 1):
        pm.parent(jointList[i], jointList[i + 1])


L_frontLeg_jontList = [
    L_frontToeJnt,
    L_frontAnkleJnt,
    L_frontkneeJnt,
    L_frontUpperKneeJnt,
    L_frontFemurJnt,
    frontPelvisJnt,
]
L_hindLeg_jontList = [
    L_hindToeJnt,
    L_hindAnkleJnt,
    L_hindkneeJnt,
    L_hindUpperKneeJnt,
    L_hindFemurJnt,
    hindPelvisJnt,
]
R_frontLeg_jontList = [
    R_frontToeJnt,
    R_frontAnkleJnt,
    R_frontkneeJnt,
    R_frontUpperKneeJnt,
    R_frontFemurJnt,
    frontPelvisJnt,
]
R_hindLeg_jontList = [
    R_hindToeJnt,
    R_hindAnkleJnt,
    R_hindkneeJnt,
    R_hindUpperKneeJnt,
    R_hindFemurJnt,
    hindPelvisJnt,
]
tail_jointList = [tailEndJnt, tailRootJnt, hindPelvisJnt]
neckSpine_jointList = [neckEndJnt, neckRootJnt, frontPelvisJnt, hindPelvisJnt]
parentJoint(L_frontLeg_jontList)
parentJoint(L_hindLeg_jontList)
parentJoint(R_frontLeg_jontList)
parentJoint(R_hindLeg_jontList)
parentJoint(tail_jointList)
parentJoint(neckSpine_jointList)

# set last joint
lastjoint = [L_frontToeJnt, L_hindToeJnt, R_frontToeJnt, R_hindToeJnt]
endjnt = []
for jnt in lastjoint:
    dupJnt = pm.duplicate(jnt, n="{}_last".format(jnt))
    pm.parent(dupJnt[0], jnt)
    dupJnt[0].tz.set(1)
    dupJnt[0].v.set(0)
    endjnt.append(dupJnt)

L_frontLeg_JntList = [
    L_frontFemurJnt,
    L_frontUpperKneeJnt,
    L_frontkneeJnt,
    L_frontAnkleJnt,
    L_frontToeJnt,
    endjnt[0],
]
L_hindLeg_JntList = [
    L_hindFemurJnt,
    L_hindUpperKneeJnt,
    L_hindkneeJnt,
    L_hindAnkleJnt,
    L_hindToeJnt,
    endjnt[1],
]
R_frontLeg_JntList = [
    R_frontFemurJnt,
    R_frontUpperKneeJnt,
    R_frontkneeJnt,
    R_frontAnkleJnt,
    R_frontToeJnt,
    endjnt[2],
]
R_hindLeg_JntList = [
    R_hindFemurJnt,
    R_hindUpperKneeJnt,
    R_hindkneeJnt,
    R_hindAnkleJnt,
    R_hindToeJnt,
    endjnt[3],
]

# set joint orient
topJoint = [
    L_frontFemurJnt,
    L_hindFemurJnt,
    R_frontFemurJnt,
    R_hindFemurJnt,
    neckRootJnt,
    tailRootJnt,
]
for jnt in topJoint:
    pm.joint(jnt, zso=1, ch=1, e=1, oj="xyz", secondaryAxisOrient="zup")

# create Rename Function


def renameChildJoint(jnt, oldStr, newStr):
    pm.select(jnt, r=True, hi=True)
    childjntList = pm.selected()[1:]
    for jnt in childjntList:
        newName = jnt.split("|")[-1].replace(oldStr, newStr)
        jnt.rename(newName)
    return childjntList


# create IK,FK Joint
L_hindLeg_FkJntList = pm.duplicate(L_hindFemurJnt, n="L_hindFemur_FK_JNT")
L_hindLeg_FkJntChild = renameChildJoint(L_hindLeg_FkJntList[0], "_JNT", "_FK_JNT")
for obj in L_hindLeg_FkJntChild:
    L_hindLeg_FkJntList.append(obj)

L_frontLeg_FkJntList = pm.duplicate(L_frontFemurJnt, n="L_frontFemur_FK_JNT")
L_frontLeg_FkJntChild = renameChildJoint(L_frontLeg_FkJntList[0], "_JNT", "_FK_JNT")
for obj in L_frontLeg_FkJntChild:
    L_frontLeg_FkJntList.append(obj)

R_frontLeg_FkJntList = pm.duplicate(R_frontFemurJnt, n="R_frontFemur_FK_JNT")
R_frontLeg_FkJntChild = renameChildJoint(R_frontLeg_FkJntList[0], "_JNT", "_FK_JNT")
for obj in R_frontLeg_FkJntChild:
    R_frontLeg_FkJntList.append(obj)

R_hindLeg_FkJntList = pm.duplicate(R_hindFemurJnt, n="R_hindFemur_FK_JNT")
R_hindLeg_FkJntChild = renameChildJoint(R_hindLeg_FkJntList[0], "_JNT", "_FK_JNT")
for obj in R_hindLeg_FkJntChild:
    R_hindLeg_FkJntList.append(obj)

L_hindLeg_IkJntList = pm.duplicate(L_hindFemurJnt, n="L_hindFemur_IK_JNT")
L_hindLeg_IkJntChild = renameChildJoint(L_hindLeg_IkJntList[0], "_JNT", "_IK_JNT")
for obj in L_hindLeg_IkJntChild:
    L_hindLeg_IkJntList.append(obj)

L_frontLeg_IkJntList = pm.duplicate(L_frontFemurJnt, n="L_frontFemur_IK_JNT")
L_frontLeg_IkJntChild = renameChildJoint(L_frontLeg_IkJntList[0], "_JNT", "_IK_JNT")
for obj in L_frontLeg_IkJntChild:
    L_frontLeg_IkJntList.append(obj)

R_frontLeg_IkJntList = pm.duplicate(R_frontFemurJnt, n="R_frontFemur_IK_JNT")
R_frontLeg_IkJntChild = renameChildJoint(R_frontLeg_IkJntList[0], "_JNT", "_IK_JNT")
for obj in R_frontLeg_IkJntChild:
    R_frontLeg_IkJntList.append(obj)

R_hindLeg_IkJntList = pm.duplicate(R_hindFemurJnt, n="R_hindFemur_IK_JNT")
R_hindLeg_IkJntChild = renameChildJoint(R_hindLeg_IkJntList[0], "_JNT", "_IK_JNT")
for obj in R_hindLeg_IkJntChild:
    R_hindLeg_IkJntList.append(obj)


def pointMatch(obj1, obj2):
    nod = pm.pointConstraint(obj2, obj1)
    pm.delete(nod)
    pm.select(cl=1)


def orientMatch(obj1, obj2):
    nod = pm.orientConstraint(obj2, obj1)
    pm.delete(nod)
    pm.select(cl=1)


def parentMatch(obj1, obj2):
    nod = pm.parentConstraint(obj2, obj1)
    pm.delete(nod)
    pm.select(cl=1)


"""-----------------------------------------------------Create IK------------------------------------------------------------"""
###create L hind IK###

L_hindLegIk = pm.ikHandle(
    name="L_hindLeg_IK",
    sj=L_hindLeg_IkJntList[0],
    ee=L_hindLeg_IkJntList[-3],
    solver="ikRPsolver",
)
L_hindIkCtrl = ctrlCreater("L_hindLeg_IK_Ctrl", ik_CurInfo, 6)
L_hindIkCtrl_Grp = pm.group(L_hindIkCtrl, n="L_hindLeg_IK_Ctrl_GRP")
pointMatch(L_hindIkCtrl_Grp, L_hindLeg_IkJntList[-2])
pm.parent(L_hindLegIk[0], L_hindIkCtrl)
pm.aimConstraint(
    L_hindIkCtrl,
    L_hindLeg_IkJntList[0],
    n="l_femur_aim_towards_footCtrl",
    mo=True,
    wu=[0, 0, 0],
)
L_hindLegToeIk = pm.ikHandle(
    n="L_hindLegToe_IK",
    sol="ikRPsolver",
    sj=L_hindLeg_IkJntList[-3],
    ee=L_hindLeg_IkJntList[-2],
)
pm.parent(L_hindLegToeIk[0], L_hindIkCtrl)
# create L hind IK PoleVector
L_hindIkPoleCtrl = ctrlCreater("L_hind_Ik_Pole_Ctrl", pole_CurInfo, 6)
L_hindIkPoleCtrlGrp = pm.group(L_hindIkPoleCtrl, n="L_hind_Ik_Pole_Ctrl_GRP")
pointMatch(L_hindIkPoleCtrlGrp, L_hindLeg_IkJntList[2])
L_hindIkPoleCtrlGrp.tz.set(L_hindIkPoleCtrlGrp.tz.get() * 2)
pm.poleVectorConstraint(L_hindIkPoleCtrl, L_hindLegIk[0])
L_hindLegIk[0].twist.set(180)

###creare R hind IK###

R_hindLegIk = pm.ikHandle(
    name="R_hindLeg_IK",
    sj=R_hindLeg_IkJntList[0],
    ee=R_hindLeg_IkJntList[-3],
    solver="ikRPsolver",
)
R_hindIkCtrl = ctrlCreater("R_hindLeg_IK_Ctrl", ik_CurInfo, 13)
R_hindIkCtrR_Grp = pm.group(R_hindIkCtrl, n="R_hindLeg_IK_Ctrl_GRP")
pointMatch(R_hindIkCtrR_Grp, R_hindLeg_IkJntList[-2])
pm.parent(R_hindLegIk[0], R_hindIkCtrl)
pm.aimConstraint(
    R_hindIkCtrl,
    R_hindLeg_IkJntList[0],
    n="R_femur_aim_towards_footCtrl",
    mo=True,
    wu=[0, 0, 0],
)
R_hindLegToeIk = pm.ikHandle(
    n="R_hindLegToe_IK",
    sol="ikRPsolver",
    sj=R_hindLeg_IkJntList[-3],
    ee=R_hindLeg_IkJntList[-2],
)
pm.parent(R_hindLegToeIk[0], R_hindIkCtrl)

# create R hind IK PoleVector
R_hindIkPoleCtrl = ctrlCreater("R_hind_Ik_Pole_Ctrl", pole_CurInfo, 13)
R_hindIkPoleCtrlGrp = pm.group(R_hindIkPoleCtrl, n="R_hind_Ik_Pole_Ctrl_GRP")
pointMatch(R_hindIkPoleCtrlGrp, R_hindLeg_IkJntList[2])
R_hindIkPoleCtrlGrp.tz.set(R_hindIkPoleCtrlGrp.tz.get() * 2)
pm.poleVectorConstraint(R_hindIkPoleCtrl, R_hindLegIk[0])
R_hindLegIk[0].twist.set(180)

###creare L front IK###

L_frontLegIk = pm.ikHandle(
    name="L_frontLeg_IK",
    sj=L_frontLeg_IkJntList[0],
    ee=L_frontLeg_IkJntList[-3],
    solver="ikRPsolver",
)
L_frontIkCtrl = ctrlCreater("L_frontLeg_IK_Ctrl", ik_CurInfo, 6)
L_frontIkCtrl_Grp = pm.group(L_frontIkCtrl, n="L_frontLeg_IK_Ctrl_GRP")
pointMatch(L_frontIkCtrl_Grp, L_frontLeg_IkJntList[-2])
pm.parent(L_frontLegIk[0], L_frontIkCtrl)
L_frontLegToeIk = pm.ikHandle(
    n="L_frontLegToe_IK",
    sol="ikRPsolver",
    sj=L_frontLeg_IkJntList[-3],
    ee=L_frontLeg_IkJntList[-2],
)
pm.parent(L_frontLegToeIk[0], L_frontIkCtrl)

L_frontLegRoCtrl = ctrlCreater("L_front_Leg_Rotete_Ctrl", fk_CurInfo, 6)
L_frontLegRoCtrlGrp = pm.group(L_frontLegRoCtrl, n="L_front_Leg_Rotete_Ctrl_GRP")
pointMatch(L_frontLegRoCtrlGrp, L_frontLeg_IkJntList[0])

# create L front IK PoleVector
L_frontIkPoleCtrl = ctrlCreater("L_front_Ik_Pole_Ctrl", pole_CurInfo, 6)
L_frontIkPoleCtrlGrp = pm.group(L_frontIkPoleCtrl, n="L_front_Ik_Pole_Ctrl_GRP")
pointMatch(L_frontIkPoleCtrlGrp, L_frontLeg_IkJntList[2])
L_frontIkPoleCtrlGrp.tz.set(0)
pm.poleVectorConstraint(L_frontIkPoleCtrl, L_frontLegIk[0])


###creare R front IK###

R_frontLegIk = pm.ikHandle(
    name="R_frontLeg_IK",
    sj=R_frontLeg_IkJntList[0],
    ee=R_frontLeg_IkJntList[-3],
    solver="ikRPsolver",
)
R_frontIkCtrl = ctrlCreater("R_frontLeg_IK_Ctrl", ik_CurInfo, 13)
R_frontIkCtrR_Grp = pm.group(R_frontIkCtrl, n="R_frontLeg_IK_Ctrl_GRP")
pointMatch(R_frontIkCtrR_Grp, R_frontLeg_IkJntList[-2])
pm.parent(R_frontLegIk[0], R_frontIkCtrl)
R_frontLegToeIk = pm.ikHandle(
    n="R_frontLegToe_IK",
    sol="ikRPsolver",
    sj=R_frontLeg_IkJntList[-3],
    ee=R_frontLeg_IkJntList[-2],
)
pm.parent(R_frontLegToeIk[0], R_frontIkCtrl)

R_frontLegRoCtrl = ctrlCreater("R_front_Leg_Rotete_Ctrl", fk_CurInfo, 6)
R_frontLegRoCtrlGrp = pm.group(R_frontLegRoCtrl, n="R_front_Leg_Rotete_Ctrl_GRP")
pointMatch(R_frontLegRoCtrlGrp, R_frontLeg_IkJntList[0])

# create R front IK PoleVector
R_frontIkPoleCtrl = ctrlCreater("R_front_Ik_Pole_Ctrl", pole_CurInfo, 13)
R_frontIkPoleCtrlGrp = pm.group(R_frontIkPoleCtrl, n="R_front_Ik_Pole_Ctrl_GRP")
pointMatch(R_frontIkPoleCtrlGrp, R_frontLeg_IkJntList[2])
R_frontIkPoleCtrlGrp.tz.set(0)
pm.poleVectorConstraint(R_frontIkPoleCtrl, R_frontLegIk[0])

# Group IK Items

L_hindIkVis_Grp = pm.group(
    L_hindIkCtrl_Grp, L_hindIkPoleCtrlGrp, n="L_hind_leg_Ik_Vis_GRP"
)
L_frontIkVis_Grp = pm.group(
    L_frontIkCtrl_Grp,
    L_frontLegRoCtrlGrp,
    L_frontIkPoleCtrlGrp,
    n="L_front_leg_Ik_Vis_GRP",
)
R_hindIkVis_Grp = pm.group(
    R_hindIkCtrR_Grp, R_hindIkPoleCtrlGrp, n="R_hind_leg_Ik_Vis_GRP"
)
R_frontIkVis_Grp = pm.group(
    R_frontIkCtrR_Grp,
    R_frontLegRoCtrlGrp,
    R_frontIkPoleCtrlGrp,
    n="R_front_leg_Ik_Vis_GRP",
)
IkCtrlGrp = pm.group(
    L_hindIkVis_Grp,
    L_frontIkVis_Grp,
    R_hindIkVis_Grp,
    R_frontIkVis_Grp,
    n="IK_Ctrl_GRP",
)
IkCtrlGrp.zeroTransformPivots()

# crtl scale founction
"""
def scaleCurShap(cvName,scaleVal=1.1):
	cvList = pm.ls('{}.cv[*]'.format(cvName))
	pm.scale(cvList,scaleVal,scaleVal,scaleVal,objectCenterPivot=True,relative=True)

selList = pm.selected()
for obj in selList:
	scaleCurShap(obj,1.25)
"""
"""-----------------------------------------------------Create FK Ctrl------------------------------------------------------------"""


def fkCtrlCreater(jntList, colorId):
    CTRL_list = []
    GRP_list = []
    for i in range(len(jntList) - 1):
        tempCtrl = ctrlCreater(jntList[i].replace("_JNT", "_Ctrl"), fk_CurInfo, colorId)
        tempGrp = pm.group(tempCtrl, n="{}_GRP".format(tempCtrl))
        parentMatch(tempGrp, jntList[i])
        pm.parentConstraint(tempCtrl, jntList[i], weight=1)
        CTRL_list.append(tempCtrl)
        GRP_list.append(tempGrp)
    for i in range(len(GRP_list) - 1):
        pm.parent(GRP_list[i + 1], CTRL_list[i])
    return CTRL_list, GRP_list


L_hindLeg_FkList = fkCtrlCreater(L_hindLeg_FkJntList, 6)
L_frontLeg_FkList = fkCtrlCreater(L_frontLeg_FkJntList, 6)
R_hindLeg_FkList = fkCtrlCreater(R_hindLeg_FkJntList, 13)
R_frontLeg_FkList = fkCtrlCreater(R_frontLeg_FkJntList, 13)
leg_fk_Grp = pm.group(
    L_hindLeg_FkList[1][0],
    L_frontLeg_FkList[1][0],
    R_hindLeg_FkList[1][0],
    R_frontLeg_FkList[1][0],
    n="FK_Ctrl_GRP",
)
leg_fk_Grp.zeroTransformPivots()

"""--------------------------------------------------------IK FK Switch-----------------------------------------------------"""
# L_hind_leg_Switch
L_hindSwitchCtrl = ctrlCreater("L_hind_switch_Ctrl", switch_CurInfo, 6)
pm.rotate(pm.ls("{}.cv[*]".format(L_hindSwitchCtrl))[0], (0, -90, 0), ocp=True, os=True)
pm.move(pm.ls("{}.cv[*]".format(L_hindSwitchCtrl))[0], (0, 0, -32), os=True, r=True)
L_hindSwitchGrp = pm.group(L_hindSwitchCtrl, n="{}_GRP".format(L_hindSwitchCtrl))
L_hindSwitchGrp.zeroTransformPivots()
pointMatch(L_hindSwitchGrp, L_hindAnkleJnt)
pm.parentConstraint(L_hindAnkleJnt, L_hindSwitchGrp, mo=True)
L_hindSwitchCtrl_att = L_hindSwitchCtrl.listAnimatable()
for att in L_hindSwitchCtrl_att[:-1]:
    pm.setAttr(att, lock=True, channelBox=False, keyable=False)
pm.addAttr(L_hindSwitchCtrl, longName="IK_FK", at="float", k=True, min=0, max=1)

# L_front_leg_Switch
L_frontSwitchCtrl = ctrlCreater("L_front_switch_Ctrl", switch_CurInfo, 6)
pm.rotate(
    pm.ls("{}.cv[*]".format(L_frontSwitchCtrl))[0], (0, -90, 0), ocp=True, os=True
)
pm.move(pm.ls("{}.cv[*]".format(L_frontSwitchCtrl))[0], (0, 0, -32), os=True, r=True)
L_frontSwitchGrp = pm.group(L_frontSwitchCtrl, n="{}_GRP".format(L_frontSwitchCtrl))
L_frontSwitchGrp.zeroTransformPivots()
pointMatch(L_frontSwitchGrp, L_frontAnkleJnt)
pm.parentConstraint(L_frontAnkleJnt, L_frontSwitchGrp, mo=True)
L_frontSwitchCtrl_att = L_frontSwitchCtrl.listAnimatable()
for att in L_frontSwitchCtrl_att[:-1]:
    pm.setAttr(att, lock=True, channelBox=False, keyable=False)
pm.addAttr(L_frontSwitchCtrl, longName="IK_FK", at="float", k=True, min=0, max=1)

# R_hind_leg_Switch
R_hindSwitchCtrl = ctrlCreater("R_hind_switch_Ctrl", switch_CurInfo, 13)
pm.rotate(pm.ls("{}.cv[*]".format(R_hindSwitchCtrl))[0], (0, -90, 0), ocp=True, os=True)
pm.move(pm.ls("{}.cv[*]".format(R_hindSwitchCtrl))[0], (0, 0, -32), os=True, r=True)
R_hindSwitchGrp = pm.group(R_hindSwitchCtrl, n="{}_GRP".format(R_hindSwitchCtrl))
R_hindSwitchGrp.zeroTransformPivots()
pointMatch(R_hindSwitchGrp, R_hindAnkleJnt)
pm.parentConstraint(R_hindAnkleJnt, R_hindSwitchGrp, mo=True)
R_hindSwitchCtrl_att = R_hindSwitchCtrl.listAnimatable()
for att in R_hindSwitchCtrl_att[:-1]:
    pm.setAttr(att, lock=True, channelBox=False, keyable=False)
pm.addAttr(R_hindSwitchCtrl, longName="IK_FK", at="float", k=True, min=0, max=1)

# R_front_leg_Switch
R_frontSwitchCtrl = ctrlCreater("R_front_switch_Ctrl", switch_CurInfo, 13)
pm.rotate(
    pm.ls("{}.cv[*]".format(R_frontSwitchCtrl))[0], (0, -90, 0), ocp=True, os=True
)
pm.move(pm.ls("{}.cv[*]".format(R_frontSwitchCtrl))[0], (0, 0, -32), os=True, r=True)
R_frontSwitchGrp = pm.group(R_frontSwitchCtrl, n="{}_GRP".format(R_frontSwitchCtrl))
R_frontSwitchGrp.zeroTransformPivots()
pointMatch(R_frontSwitchGrp, R_frontAnkleJnt)
pm.parentConstraint(R_frontAnkleJnt, R_frontSwitchGrp, mo=True)
R_frontSwitchCtrl_att = R_frontSwitchCtrl.listAnimatable()
for att in R_frontSwitchCtrl_att[:-1]:
    pm.setAttr(att, lock=True, channelBox=False, keyable=False)
pm.addAttr(R_frontSwitchCtrl, longName="IK_FK", at="float", k=True, min=0, max=1)

switchCtrlGrp = pm.group(
    L_hindSwitchGrp,
    L_frontSwitchGrp,
    R_hindSwitchGrp,
    R_frontSwitchGrp,
    n="IK_switch_Ctrl_GRP",
)


# set IK_FK Switch connect
def connectIKFKToSkinJnt(fkJnt, ikJnt, skinJnt, ctrlName, fkCtrlGrp, ikCtrlGrp):
    parentConstraintNode = []
    for i in range(len(fkJnt)):
        parCon = pm.parentConstraint(fkJnt[i], ikJnt[i], skinJnt[i], w=1)
        reverseNode = pm.createNode("reverse")
        pm.connectAttr(
            "{}.IK_FK".format(ctrlName), "{}.{}W0".format(parCon, fkJnt[i]), force=True
        )
        pm.connectAttr(
            "{}.{}W0".format(parCon, fkJnt[i]),
            "{}.inputX".format(reverseNode),
            force=True,
        )
        pm.connectAttr(
            "{}.outputX".format(reverseNode), "{}.{}W1".format(parCon, ikJnt[i])
        )

    visReverseNode = pm.createNode("reverse")
    pm.connectAttr(
        "{}.IK_FK".format(ctrlName), "{}.inputX".format(visReverseNode), force=True
    )
    pm.connectAttr("{}.IK_FK".format(ctrlName), "{}.v".format(fkCtrlGrp), force=True)
    pm.connectAttr(
        "{}.outputX".format(visReverseNode), "{}.v".format(ikCtrlGrp), force=True
    )


connectIKFKToSkinJnt(
    L_hindLeg_FkJntList,
    L_hindLeg_IkJntList,
    L_hindLeg_JntList,
    L_hindSwitchCtrl,
    L_hindLeg_FkList[1][0],
    L_hindIkVis_Grp,
)
connectIKFKToSkinJnt(
    L_frontLeg_FkJntList,
    L_frontLeg_IkJntList,
    L_frontLeg_JntList,
    L_frontSwitchCtrl,
    L_frontLeg_FkList[1][0],
    L_frontIkVis_Grp,
)
connectIKFKToSkinJnt(
    R_hindLeg_FkJntList,
    R_hindLeg_IkJntList,
    R_hindLeg_JntList,
    R_hindSwitchCtrl,
    R_hindLeg_FkList[1][0],
    R_hindIkVis_Grp,
)
connectIKFKToSkinJnt(
    R_frontLeg_FkJntList,
    R_frontLeg_IkJntList,
    R_frontLeg_JntList,
    R_frontSwitchCtrl,
    R_frontLeg_FkList[1][0],
    R_frontIkVis_Grp,
)

"""--------------------------------------------------Create tail joint --------------------------------------------------"""


def insertJointTool(rootJoint, jointCount, jointName):
    rootJointPos = rootJoint.getTranslation(space="world")  # 获取首根骨骼的位置
    endJointPos = rootJoint.getChildren()[0].getTranslation(
        space="world"
    )  # 获取末端骨骼的位置
    difVal = endJointPos - rootJointPos  # 获取首尾骨骼位置的差值
    segmentVal = difVal / (jointCount + 1)  # 获取每段新骨骼的差值
    pm.select(rootJoint)  # 选择首根骨骼
    for i in range(jointCount):
        targetJoint = pm.selected()[0]  # 获取所选骨骼为目标骨骼
        targetJointPos = targetJoint.getTranslation(space="world")  # 获取目标骨骼位置
        newJoint = pm.insertJoint(targetJoint)  # 在目标骨骼上插入新骨骼
        pm.joint(
            newJoint, component=True, edit=True, p=(targetJointPos + segmentVal)
        )  # 调整新骨骼位置
    pm.select(rootJoint, hi=True)
    jntChainList = pm.selected()
    for j in range(len(jntChainList)):
        jntChainList[j].rename("{}_{}_JNT".format(jointName, j + 1))  # 骨骼链重命名
    pm.joint(jntChainList[-1], zso=1, ch=1, e=1, oj="none")  # 调整骨骼方向
    pm.select(cl=True)  # 取消选择
    return jntChainList  # 返回骨骼链列表


tail_jointList = insertJointTool(tailRootJnt, 5, "tail")
# Create Spline IK
tailSpineIk = pm.ikHandle(
    sol="ikSplineSolver",
    ns=6,
    sj=tail_jointList[0],
    ee=tail_jointList[-1],
    n="tail_spline_IK",
)  # 创建线性IK
tailSpineIkGrp = pm.group(
    tailSpineIk[0], tailSpineIk[2], n="tail_spline_IK_GRP"
)  # 线性IK手柄和曲线打组
tailSpineIkGrp.inheritsTransform.set(0)  # 取消继承transform,防止双重位移
tailSpineIk[2].rename("tail_splineIK_curve")  # 曲线重命名
tailSpineIkCVList = pm.ls("{}.cv[*]".format(tailSpineIk[2]), fl=True)  # 获取曲线上的点
tailSpineIkCVNum = len(tailSpineIkCVList)  # 获取曲线上点数量
tailClusterList = [
    pm.cluster(tailSpineIkCVList[0], rel=True, n="tail_Cluster1")[1]
]  # 第一个点创建簇
tailClusterGrpList = [
    pm.group(tailClusterList[0], n="{}_GRP".format(tailClusterList[0]))
]  # 给簇打组
for i in range((tailSpineIkCVNum - 1) / 2):  # 创建剩下的簇，两两打簇
    tempCluster = pm.cluster(
        tailSpineIkCVList[(i + 1) * 2 : (i * 2) + 3],
        rel=True,
        n="tail_Cluster{}".format(i + 2),
    )[1]
    tempClusterGrp = pm.group(tempCluster, n="{}_GRP".format(tempCluster))
    tailClusterList.append(tempCluster)
    tailClusterGrpList.append(tempClusterGrp)

tailIKCtrlList = []
tailIKCtrlGrpList = []
for cluster in tailClusterList:  # 为线性IK 创建控制器
    tailIKCtrl = ctrlCreater("{}_Ctrl".format(cluster), ik_CurInfo, 17)
    tailIKCtrlGrp = pm.group(tailIKCtrl, n="{}_GRP".format(tailIKCtrl))
    pointMatch(tailIKCtrlGrp, cluster)
    orientMatch(tailIKCtrlGrp, tailRootJnt)
    pm.parentConstraint(tailIKCtrl, cluster)
    tailIKCtrlList.append(tailIKCtrl)
    tailIKCtrlGrpList.append(tailIKCtrlGrp)
# Create Tail FK Ctrl
tailRootFkCtrl = ctrlCreater("tail_root_FK_Ctrl", fk_CurInfo, 17)
tailRootFkCtrlGrp = pm.group(tailRootFkCtrl, n="{}_GRP".format(tailRootFkCtrl))
tailMidFkCtrl = ctrlCreater("tail_mid_FK_Ctrl", fk_CurInfo, 17)
tailMidFkCtrlGrp = pm.group(tailMidFkCtrl, n="{}_GRP".format(tailMidFkCtrl))
tailEndFkCtrl = ctrlCreater("tail_end_FK_Ctrl", fk_CurInfo, 17)
tailEndFkCtrlGrp = pm.group(tailEndFkCtrl, n="{}_GRP".format(tailEndFkCtrl))

tailRootFkCtrlGrp.t.set(tailSpineIkCVList[0].getPosition())
tailMidFkCtrlGrp.t.set(tailSpineIkCVList[4].getPosition())
tailEndFkCtrlGrp.t.set(tailSpineIkCVList[7].getPosition())

orientMatch(tailRootFkCtrlGrp, tailRoot)
orientMatch(tailMidFkCtrlGrp, tailRoot)
orientMatch(tailEndFkCtrlGrp, tailRoot)

pm.parent(tailIKCtrlGrpList[-1], tailIKCtrlGrpList[-2], tailEndFkCtrl)
pm.parent(tailIKCtrlGrpList[-3], tailMidFkCtrl)
pm.parent(tailIKCtrlGrpList[0], tailIKCtrlGrpList[1], tailRootFkCtrl)

pm.parent(tailEndFkCtrlGrp, tailMidFkCtrl)
pm.parent(tailMidFkCtrlGrp, tailRootFkCtrl)

pm.parent(tailMidFkCtrlGrp, tailRootFkCtrl)
