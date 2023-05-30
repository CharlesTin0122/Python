# coding:UTF-8
# ************************************************************************************************************
# Title: lr_leg_rig.py
# Author: li ran
# Created: 2017 03 01
# Last Update: 2017 03 01
# version: 1.0
# ************************************************************************************************************

import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel


def cre_joint(n, LR, final_int_sel):
    joint_sel = []
    jointCoo = [[2.0, 16.000000000000004, 0.0], [2.0000000000000027, 9.000000000000004, 1.0000000000000004], \
                [2.000000000000005, 1.0000000000000018, -2.220446049250313e-16],
                [2.0000000000000138, 1.1102230246251565e-15, 2.0000000000000018], \
                [2.0000000000000133, 9.853229343548264e-16, 4.0000000000000036],
                [3.0000000000000036, 1.64625257870199e-15, 2.2000000000000037], \
                [1.0000000000000036, 7.494005416219807e-16, 2.200000000000001],
                [2.000000000000027, 2.1094237467877974e-15, -1.0000000000000016]]
    jointName = ['leg', 'knee', 'ankle', 'ball', 'toe', 'outside', 'inside', 'heel']
    # 创建腿部基础骨骼并命名
    for i in range(len(jointCoo) - 3):
        cooInt = cmds.joint(p=jointCoo[i])
        joint_sel.append(cooInt)
    for j in range(len(jointName) - 3):
        finalInt = cmds.rename(joint_sel[j], '%s_%s_%s_%s' % (n, LR, jointName[j], 'skInt'))
        final_int_sel.append(finalInt)

    # 剩下的辅助定点的三个骨骼
    for k in range(5, len(jointCoo)):
        cooInt = cmds.joint(p=jointCoo[k])
        joint_sel.append(cooInt)
    for l in range(5, len(jointName)):
        finalInt = cmds.rename(joint_sel[l], '%s_%s_%s_%s' % (n, LR, jointName[l], 'skInt'))
        final_int_sel.append(finalInt)

    cmds.parent(final_int_sel[5], final_int_sel[6], final_int_sel[3])
    cmds.parent(final_int_sel[7], final_int_sel[2])
    # 骨骼校轴
    cmds.select(final_int_sel[0])
    cmds.joint(e=True, oj='xyz', secondaryAxisOrient='zup', ch=True, zso=True)
    cmds.setAttr(final_int_sel[4] + '.jointOrient', 0, 0, 0)
    cmds.select(cl=True)

    return final_int_sel


def snap_joint(objs, TR):
    # 创建loctor 拾取位置
    if TR == 0:
        tr = cmds.xform(objs, q=True, ws=True, t=True)
        loc = cmds.spaceLocator(n=objs.replace('_ikInt', '_loc'))
        cmds.xform(loc, t=tr, ws=True)
        return loc
    # 创建loctor 拾取位置旋转
    if TR == 1:
        tr = cmds.xform(objs, q=True, ws=True, t=True)
        loc = cmds.spaceLocator(n=objs.replace('_ikInt', '_loc'))
        cmds.xform(loc, t=tr, ws=True)

        oriCt = cmds.orientConstraint(objs, loc, mo=False)
        cmds.delete(oriCt[0])
        return loc


def dup_loc(first, second, n, LR, name):
    tr = cmds.xform(first, q=True, t=True, ws=True)
    cmds.select(second)
    loc = cmds.duplicate(n='%s_%s_%s_%s' % (n, LR, name, 'loc'))[0]
    cmds.xform(loc, t=tr, ws=1)
    return loc


def real_snap(first, second, method):
    # 点约束
    if method == 0:
        point = cmds.pointConstraint(first, second, mo=False)
        cmds.delete(point[0])
    # 父子约束
    if method == 1:
        parent = cmds.parentConstraint(first, second, mo=False)
        cmds.delete(parent[0])
    # 改变物体旋转中心
    if method == 2:
        pos = cmds.xform(first, q=True, t=True, ws=True)
        cmds.xform(second, piv=pos, ws=True)


def attr(objs, method):
    attr = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.visibility']
    # 获取tx
    if method == 0:
        tx = cmds.getAttr(objs + '.translateX')
        return tx
    # 锁定隐藏 缩放、显示
    if method == 1:
        for i in range(6, 10):
            cmds.setAttr(objs + attr[i], lock=True, keyable=False)
    # 锁定隐藏 旋转 缩放 显示
    if method == 2:
        for j in range(3, 10):
            cmds.setAttr(objs + attr[j], lock=True, keyable=False)
    # 隐藏该项
    if method == 3:
        for k in range(9, 10):
            cmds.setAttr(objs + attr[k], 0)
    # 返回查询到该项的translation
    if method == 4:
        t = cmds.xform(objs, q=1, t=1, ws=1)
        return t
    if method == 5:
        for i in range(0, 10):
            cmds.setAttr(objs + attr[i], lock=True, keyable=False)


def add_attr(objs, name, method):
    if method == 0:
        cmds.addAttr(objs, ln=name)
    # tilt
    if method == 1:
        cmds.addAttr(objs, ln=name, min=-90, max=90)
    # stretch
    if method == 2:
        cmds.addAttr(objs, ln=name, min=0, max=1, dv=1)
    # lenght
    if method == 3:
        cmds.addAttr(objs, ln=str(name), dv=1)
    if method == 4:
        cmds.addAttr(objs, ln=name, min=0, max=1)
    if method == 5:
        cmds.addAttr(objs, ln=name, min=0)

    cmds.setAttr(objs + '.' + str(name), e=True, keyable=1)


# 物体打组
def add_grp(objs, n, LR, name):
    grp = cmds.group(objs, n='%s_%s_%s_%s' % (n, LR, name, 'grp'))
    return grp


# 颜色设置
def color_set(objs, method):
    if method == 'red':
        cmds.setAttr(objs + '.overrideEnabled', 1)
        cmds.setAttr(objs + '.overrideColor', 13)
    if method == 'blue':
        cmds.setAttr(objs + '.overrideEnabled', 1)
        cmds.setAttr(objs + '.overrideColor', 6)


# fk控制器
def fk_con():
    cir = []
    cir_grp = []
    sel = cmds.ls(sl=True)
    for i in range(len(sel)):
        cre_cir = cmds.circle(n=sel[i] + '_fkCon', nr=(1, 0, 0))
        mel.eval('DeleteHistory')
        attr(cre_cir[0], 1)
        cir.append(cre_cir[0])

        grp = cmds.group(cre_cir[0], n=sel[i] + '_fkCon_grp')
        real_snap(sel[i], grp, 1)
        cir_grp.append(grp)

        cmds.parentConstraint(cre_cir[0], sel[i], mo=True)
    # 层级整理
    for j in range(len(cir)):
        k = j + 1
        if k < len(cir):
            cmds.parent(cir_grp[k], cir[j])
    return cir_grp[0]


# 极向量控制器的位置
def place_correct_pole_locator(joint1, joint2, joint3):
    joint_start_position = pm.xform(joint1, q=1, ws=1, rp=1)
    joint_mid_position = pm.xform(joint2, q=1, ws=1, rp=1)
    joint_end_position = pm.xform(joint3, q=1, ws=1, rp=1)
    # 坐标转化向量
    joint_start_vector = pm.dt.Vector(joint_start_position)
    joint_mid_vector = pm.dt.Vector(joint_mid_position)
    joint_end_vector = pm.dt.Vector(joint_end_position)
    # 生成两边向量
    start_end_vector = joint_end_vector - joint_start_vector
    start_mid_vector = joint_mid_vector - joint_start_vector
    # 向量点乘得到长边模，和短边在长边阴影的乘积。 获得该阴影的长度。 获得长边的方向向量。
    dotP = start_mid_vector.dot(start_end_vector)
    proj = float(dotP) / float(start_end_vector.length())
    start_end_normal = start_end_vector.normal()
    # 获得阴影向量。求出对边的向量。对边整理为，长边除以对边得出一个倍数，再乘以一个参数。
    proj_vector = start_end_normal * proj
    arrow_vector = start_mid_vector - proj_vector
    arrow_vector *= 0.6 * start_end_vector.length() / arrow_vector.length()
    final_vector = arrow_vector + joint_mid_vector  # ...

    locator = pm.spaceLocator()
    locator.t.set(final_vector)


def import_joint(arg):
    n = cmds.textField('name', q=True, tx=True)

    LR = 'L'

    final_int_sel = []

    final_int_sel = cre_joint(n, LR, final_int_sel)

    nodeL = cmds.createNode('unknown')
    cmds.addAttr(ln="selObjects", at='message', multi=1, im=0)
    for intL in final_int_sel:
        cmds.connectAttr(intL + '.message', nodeL + ".selObjects", na=True)


def auto_joint():
    Num = cmds.checkBox('checkBox_test', q=True, v=True)

    l_leg_int = cmds.listConnections('unknown1' + '.selObjects')

    # 校轴
    if int(Num) == 0:
        cmds.select(l_leg_int[0])
        cmds.joint(e=True, oj='xyz', secondaryAxisOrient='zup', ch=True, zso=True)


def mirror_joint(arg):
    # 获取左侧腿部骨骼的列表
    l_leg_int = cmds.listConnections('unknown1' + '.selObjects')
    # 清节点
    unknownsel = cmds.ls(type='unknown')
    cmds.delete(unknownsel)

    cmds.setAttr(l_leg_int[4] + '.jointOrient', 0, 0, 0)
    cmds.select(cl=True)
    # 冻结旋转
    for i in range(len(l_leg_int)):
        cmds.makeIdentity(l_leg_int[i], apply=True, rotate=True)

    # 镜像骨骼
    cmds.select(l_leg_int[0])
    final_R_int_sel = cmds.mirrorJoint(mirrorYZ=True, mirrorBehavior=True, searchReplace=('L', 'R'))
    # 为后续创建辅助节点
    nodeL = cmds.createNode('unknown')
    cmds.addAttr(ln="selObjects", at='message', multi=1, im=0)
    for intL in l_leg_int:
        cmds.connectAttr(intL + '.message', nodeL + ".selObjects", na=True)

    nodeR = cmds.createNode('unknown')
    cmds.addAttr(ln="selObjects", at='message', multi=1, im=0)
    for intR in final_R_int_sel:
        cmds.connectAttr(intR + '.message', nodeR + ".selObjects", na=True)


def l_leg_rig(arg):
    n = cmds.textField('name', q=True, tx=True)
    LR = 'L'

    # ===============================ikInt================================

    cmds.select(cmds.listConnections('unknown1' + '.selObjects')[0])
    mel.eval('searchReplaceNames "skInt" "ikInt" "hierarchy"')
    l_leg_int = cmds.listConnections('unknown1' + '.selObjects')[0:8]

    # ==============================fk===============================
    # 复制fk
    cmds.select(l_leg_int[0])
    cmds.duplicate(n='%s_%s_%s_%s' % (n, LR, 'leg', 'fkInt'))
    # 整体改名ik--fk
    cmds.select(cmds.listConnections('unknown1' + '.selObjects')[9])
    mel.eval('searchReplaceNames "ikInt" "fkInt" "hierarchy"')
    # fk 列表
    l_leg_fkInt = cmds.listConnections('unknown1' + '.selObjects')[8:16]

    cmds.select(l_leg_fkInt[0:4])
    fk_grp = fk_con()

    # ==============================skInt=============================
    cmds.select(l_leg_int[0])
    cmds.duplicate(n='%s_%s_%s_%s' % (n, LR, 'leg', 'skInt'))

    cmds.select(cmds.listConnections('unknown1' + '.selObjects')[17])
    mel.eval('searchReplaceNames "ikInt" "skInt" "hierarchy"')

    l_leg_skInt = cmds.listConnections('unknown1' + '.selObjects')[16:24]

    # ================================IK================================
    # loc create
    ball_loc = snap_joint(l_leg_int[3], 1)[0]

    toe_loc = snap_joint(l_leg_int[4], 1)[0]
    real_snap(l_leg_int[3], toe_loc, 2)

    toejianloc = snap_joint(l_leg_int[4], 1)[0]
    toejian_loc = cmds.rename(toejianloc, toejianloc.replace(toejianloc[-8:], 'toejian_loc'))

    outside_loc = dup_loc(l_leg_int[5], ball_loc, n, LR, 'outside')
    inside_loc = dup_loc(l_leg_int[6], ball_loc, n, LR, 'inside')

    heel_loc = dup_loc(l_leg_int[7], ball_loc, n, LR, 'heel')
    heeloff_loc = dup_loc(l_leg_int[7], ball_loc, n, LR, 'heeloff')

    ankle_loc = snap_joint(l_leg_int[2], 0)[0]
    # loc parent
    cmds.parent(ball_loc, toe_loc, outside_loc)
    cmds.parent(outside_loc, inside_loc)
    cmds.parent(inside_loc, toejian_loc)
    cmds.parent(toejian_loc, heel_loc)
    cmds.parent(heel_loc, heeloff_loc)
    cmds.parent(heeloff_loc, ankle_loc)

    # ik
    ankle_ik = \
    cmds.ikHandle(sj=l_leg_int[0], ee=l_leg_int[2], n='%s_%s_%s_%s' % (n, LR, 'ankle', 'ik'), sol='ikRPsolver')[0]
    ball_ik = \
    cmds.ikHandle(sj=l_leg_int[2], ee=l_leg_int[3], n='%s_%s_%s_%s' % (n, LR, 'ball', 'ik'), sol='ikSCsolver')[0]
    toe_ik = cmds.ikHandle(sj=l_leg_int[3], ee=l_leg_int[4], n='%s_%s_%s_%s' % (n, LR, 'toe', 'ik'), sol='ikSCsolver')[
        0]
    cmds.parent(ankle_ik, ball_loc)
    cmds.parent(ball_ik, ball_loc)
    cmds.parent(toe_ik, toe_loc)

    # foot con
    footpos = [[0.5, 0.5, 0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5], \
               [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], \
               [-0.5, 0.5, -0.5], [-0.5, 0.5, 0.5], [0.5, 0.5, 0.5], \
               [0.5, -0.5, 0.5], [0.5, -0.5, -0.5], [-0.5, -0.5, -0.5], \
               [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [-0.5, -0.5, 0.5], [-0.5, 0.5, 0.5]]
    footcon_cv = cmds.curve(d=1, p=footpos, n=n + '_' + LR + '_foot_con')

    attr(footcon_cv, 1)
    footcon_grp = add_grp(footcon_cv, n, LR, 'foot')

    # 添加属性
    add_attr(footcon_cv, 'roll', 5)
    add_attr(footcon_cv, 'tilt', 1)
    add_attr(footcon_cv, 'toe', 0)
    add_attr(footcon_cv, 'toe_spin', 0)
    add_attr(footcon_cv, 'toe_wiggle', 0)
    add_attr(footcon_cv, 'heel', 5)
    add_attr(footcon_cv, 'stretch', 2)
    add_attr(footcon_cv, 'leg_lenght', 3)
    add_attr(footcon_cv, 'knee_lenght', 3)
    add_attr(footcon_cv, 'global_scale', 3)

    # foot控制器位置
    real_snap(l_leg_int[2], footcon_grp, 0)
    cmds.parent(ankle_loc, footcon_cv)

    # 极向量locater
    place_correct_pole_locator(l_leg_int[0], l_leg_int[1], l_leg_int[2])
    locater = cmds.rename(cmds.ls(sl=1), '%s_%s_%s_%s' % (n, LR, 'leg_pole', 'loc'))
    # pole con
    polepos = [[0.5, 0.0, 0.0], [0.0, 0.0, 0.5], [-0.5, 0.0, 0.0], \
               [0.0, 0.0, -0.5], [0.5, 0.0, 0.0], [0.0, 0.5, 0.0], \
               [-0.5, 0.0, 0.0], [0.0, -0.5, 0.0], [0.0, 0.0, -0.5], \
               [0.0, 0.5, 0.0], [0.0, 0.0, 0.5], [0.0, -0.5, 0.0], [0.5, 0.0, 0.0]]
    polecon_cv = cmds.curve(d=1, p=polepos, n='%s_%s_%s_%s' % (n, LR, 'leg_pole', 'con'))

    polecon_grp = add_grp(polecon_cv, n, LR, 'leg_pole_con')
    real_snap(locater, polecon_grp, 0)

    attr(polecon_cv, 2)
    add_attr(polecon_cv, 'follow', 4)

    cmds.parent(locater, polecon_cv)
    # 连接属性
    cmds.connectAttr(footcon_cv + '.leg_lenght', l_leg_int[0] + '.sx')
    cmds.connectAttr(footcon_cv + '.knee_lenght', l_leg_int[1] + '.sx')

    roll_mul = cmds.createNode('multiplyDivide', n='%s_%s_%s' % (n, LR, 'roll_mul'))
    cmds.connectAttr(footcon_cv + '.roll', roll_mul + '.input1X')
    cmds.setAttr(roll_mul + '.input2X', -1)
    cmds.connectAttr(roll_mul + '.outputX', ball_loc + '.rotateZ')

    cmds.connectAttr(footcon_cv + '.toe', toe_loc + '.rotateZ')
    cmds.connectAttr(footcon_cv + '.toe_spin', toejian_loc + '.rotateY')
    cmds.connectAttr(footcon_cv + '.toe_wiggle', toejian_loc + '.rotateZ')
    cmds.connectAttr(footcon_cv + '.heel', heel_loc + '.rotateZ')
    # tilt
    cmds.setDrivenKeyframe(outside_loc + '.rotateX', cd=footcon_cv + '.tilt', v=0)
    cmds.setAttr(footcon_cv + '.tilt', 90)
    cmds.setDrivenKeyframe(outside_loc + '.rotateX', cd=footcon_cv + '.tilt', v=-90)
    cmds.setAttr(footcon_cv + '.tilt', 0)
    cmds.setDrivenKeyframe(inside_loc + '.rotateX', cd=footcon_cv + '.tilt', v=0)
    cmds.setAttr(footcon_cv + '.tilt', -90)
    cmds.setDrivenKeyframe(inside_loc + '.rotateX', cd=footcon_cv + '.tilt', v=90)
    cmds.setAttr(footcon_cv + '.tilt', 0)
    # follow
    cmds.poleVectorConstraint(polecon_cv, ankle_ik)
    polepar = cmds.parentConstraint(footcon_cv, polecon_grp, mo=1)
    cmds.connectAttr(polecon_cv + '.follow', polepar[0] + '.' + footcon_cv + 'W0')

    leg_loc = snap_joint(l_leg_int[0], 0)[0]
    knee_loc = snap_joint(l_leg_int[1], 0)[0]
    # 测量距离
    cmds.distanceDimension(sp=attr(leg_loc, 4), ep=attr(l_leg_int[2], 4))
    dis = cmds.rename(cmds.ls(sl=1)[1], '%s_%s_%s_%s' % (n, LR, 'leg', 'dis'))
    cmds.pointConstraint(l_leg_int[0], leg_loc, mo=1)
    disup = cmds.distanceDimension(sp=attr(leg_loc, 4), ep=attr(knee_loc, 4))
    disdw = cmds.distanceDimension(sp=attr(knee_loc, 4), ep=attr(l_leg_int[2], 4))
    zonglength = cmds.getAttr(disup + '.distance') + cmds.getAttr(disdw + '.distance')
    cmds.delete(knee_loc)
    cmds.select(cl=1)

    # 拉伸

    dis_mul = cmds.createNode('multiplyDivide', n='%s_%s_%s' % (n, LR, 'distnce_mul'))
    cmds.setAttr(dis_mul + '.operation', 2)

    cmds.connectAttr(dis + '.distance', dis_mul + '.input1X')

    condition = cmds.createNode('condition', n='%s_%s_%s' % (n, LR, 'condition'))
    cmds.setAttr(condition + '.operation', 2)
    cmds.connectAttr(dis_mul + '.outputX', condition + '.firstTerm')
    cmds.connectAttr(dis_mul + '.outputX', condition + '.colorIfTrueR')
    cmds.setAttr(condition + '.secondTerm', zonglength)
    cmds.setAttr(condition + '.colorIfFalseR', zonglength)

    scale_mul = cmds.createNode('multiplyDivide', n='%s_%s_%s' % (n, LR, 'scale_mul'))
    cmds.setAttr(scale_mul + '.operation', 2)

    cmds.connectAttr(condition + '.outColorR', scale_mul + '.input1X')
    cmds.setAttr(scale_mul + '.input2X', zonglength)

    joint_mul = cmds.createNode('multiplyDivide', n='%s_%s_%s' % (n, LR, 'joint_mul'))

    blendColor = cmds.createNode('blendColors', n='%s_%s_%s' % (n, LR, 'blendColor'))
    cmds.connectAttr(footcon_cv + '.stretch', blendColor + '.blender')

    cmds.connectAttr(scale_mul + '.outputX', blendColor + '.color1R')
    cmds.setAttr(blendColor + '.color2R', 1)

    cmds.connectAttr(blendColor + '.outputR', joint_mul + '.input1X')
    cmds.connectAttr(blendColor + '.outputR', joint_mul + '.input1Y')

    cmds.setAttr(joint_mul + '.input2X', attr(l_leg_int[1], 0))
    cmds.setAttr(joint_mul + '.input2Y', attr(l_leg_int[2], 0))

    cmds.connectAttr(joint_mul + '.outputX', l_leg_int[1] + '.translateX')
    cmds.connectAttr(joint_mul + '.outputY', l_leg_int[2] + '.translateX')

    cmds.connectAttr(footcon_cv + '.global_scale', dis_mul + '.input2X')
    # 大纲整理
    attr(dis, 3)
    attr(leg_loc, 3)
    attr(locater, 3)
    attr(ankle_loc, 3)
    ik_rig_grp = cmds.group(l_leg_int[0], dis, leg_loc, polecon_grp, footcon_grp, n='%s_%s_%s' % (n, LR, 'leg_ik_grp'))

    # ============================================ikfk切换====================================
    # ikfk con
    ikfkpos = [[-0.2, 1.0, 0.0], [0.2, 1.0, 0.0], [0.2, 0.2, 0.0], \
               [1.0, 0.2, 0.0], [1.0, -0.2, 0.0], [0.2, -0.2, 0.0], \
               [0.2, -1.0, 0.0], [-0.2, -1.0, 0.0], [-0.2, -0.2, 0.0], \
               [-1.0, -0.2, 0.0], [-1.0, 0.2, 0.0], [-0.2, 0.2, 0.0], [-0.2, 1.0, 0.0]]

    ikfk_cv = cmds.curve(d=1, p=ikfkpos, n='%s_%s_%s_%s' % (n, LR, 'ikfk', 'con'))

    attr(ikfk_cv, 5)
    add_attr(ikfk_cv, 'switch', 2)
    ikfk_grp = add_grp(ikfk_cv, n, LR, 'ikfk')
    real_snap(l_leg_int[2], ikfk_grp, 0)

    # 约束
    parent_leg = cmds.parentConstraint(l_leg_int[0], l_leg_fkInt[0], l_leg_skInt[0], mo=True)
    parent_knee = cmds.parentConstraint(l_leg_int[1], l_leg_fkInt[1], l_leg_skInt[1], mo=True)
    parent_ankle = cmds.parentConstraint(l_leg_int[2], l_leg_fkInt[2], l_leg_skInt[2], mo=True)
    parent_ball = cmds.parentConstraint(l_leg_int[3], l_leg_fkInt[3], l_leg_skInt[3], mo=True)

    ikfk_blend = cmds.createNode('blendColors', n='%s_%s_%s' % (n, LR, 'ikfk_blendColor'))
    cmds.connectAttr(ikfk_cv + '.switch', ikfk_blend + '.blender')

    reverse = cmds.createNode('reverse', n='%s_%s_%s' % (n, LR, 'reverse'))
    cmds.connectAttr(ikfk_blend + '.outputR', reverse + '.inputX')

    cmds.connectAttr(ikfk_blend + '.outputR', parent_leg[0] + '.' + l_leg_int[0] + 'W0')
    cmds.connectAttr(reverse + '.outputX', parent_leg[0] + '.' + l_leg_fkInt[0] + 'W1')

    cmds.connectAttr(ikfk_blend + '.outputR', parent_knee[0] + '.' + l_leg_int[1] + 'W0')
    cmds.connectAttr(reverse + '.outputX', parent_knee[0] + '.' + l_leg_fkInt[1] + 'W1')

    cmds.connectAttr(ikfk_blend + '.outputR', parent_ankle[0] + '.' + l_leg_int[2] + 'W0')
    cmds.connectAttr(reverse + '.outputX', parent_ankle[0] + '.' + l_leg_fkInt[2] + 'W1')

    cmds.connectAttr(ikfk_blend + '.outputR', parent_ball[0] + '.' + l_leg_int[3] + 'W0')
    cmds.connectAttr(reverse + '.outputX', parent_ball[0] + '.' + l_leg_fkInt[3] + 'W1')

    cmds.connectAttr(ikfk_blend + '.outputR', polecon_grp + '.visibility')
    cmds.connectAttr(ikfk_blend + '.outputR', footcon_grp + '.visibility')

    cmds.connectAttr(reverse + '.outputX', fk_grp + '.visibility')

    # 整理层级
    attr(l_leg_fkInt[0], 3)
    attr(l_leg_int[0], 3)
    cmds.group(l_leg_fkInt[0], fk_grp, l_leg_skInt[0], ik_rig_grp, ikfk_grp,
               n='%s_%s_%s_%s' % (n, LR, 'leg_rig', 'grp'))

    sel = cmds.ls(type='unknown')
    cmds.delete(sel[0])

    cmds.setAttr(l_leg_skInt[4] + '.drawStyle', 2)
    cmds.setAttr(l_leg_skInt[5] + '.drawStyle', 2)
    cmds.setAttr(l_leg_skInt[6] + '.drawStyle', 2)
    cmds.setAttr(l_leg_skInt[7] + '.drawStyle', 2)

    # con color
    color_set(fk_grp, 'red')
    color_set(ikfk_grp, 'red')
    color_set(polecon_grp, 'red')
    color_set(footcon_grp, 'red')

    R_leg_rig(n)


# ===========================================R_leg_rig=====================================
# ===============================ikInt================================
def R_leg_rig(n):
    LR = 'R'
    cmds.select(cmds.listConnections('unknown2' + '.selObjects')[0])
    mel.eval('searchReplaceNames "skInt" "ikInt" "hierarchy"')
    R_leg_int = cmds.listConnections('unknown2' + '.selObjects')[0:8]

    # ==============================fk===============================
    # 复制fk
    cmds.select(R_leg_int[0])
    cmds.duplicate(n='%s_%s_%s_%s' % (n, LR, 'leg', 'fkInt'))
    # 整体改名ik--fk
    cmds.select(cmds.listConnections('unknown2' + '.selObjects')[9])
    mel.eval('searchReplaceNames "ikInt" "fkInt" "hierarchy"')
    # fk 列表
    R_leg_fkInt = cmds.listConnections('unknown2' + '.selObjects')[8:16]

    cmds.select(R_leg_fkInt[0:4])
    fk_grp = fk_con()

    # ==============================skInt=============================
    cmds.select(R_leg_int[0])
    cmds.duplicate(n='%s_%s_%s_%s' % (n, LR, 'leg', 'skInt'))

    cmds.select(cmds.listConnections('unknown2' + '.selObjects')[17])
    mel.eval('searchReplaceNames "ikInt" "skInt" "hierarchy"')

    R_leg_skInt = cmds.listConnections('unknown2' + '.selObjects')[16:24]

    # ================================IK================================

    # loc create
    ball_loc = snap_joint(R_leg_int[3], 1)[0]

    toe_loc = snap_joint(R_leg_int[4], 1)[0]
    real_snap(R_leg_int[3], toe_loc, 2)

    toejianloc = snap_joint(R_leg_int[4], 1)[0]
    toejian_loc = cmds.rename(toejianloc, toejianloc.replace(toejianloc[-8:], 'toejian_loc'))

    outside_loc = dup_loc(R_leg_int[5], ball_loc, n, LR, 'outside')
    inside_loc = dup_loc(R_leg_int[6], ball_loc, n, LR, 'inside')

    heel_loc = dup_loc(R_leg_int[7], ball_loc, n, LR, 'heel')
    heeloff_loc = dup_loc(R_leg_int[7], ball_loc, n, LR, 'heeloff')

    ankle_loc = snap_joint(R_leg_int[2], 0)[0]
    # loc parent
    cmds.parent(ball_loc, toe_loc, outside_loc)
    cmds.parent(outside_loc, inside_loc)
    cmds.parent(inside_loc, toejian_loc)
    cmds.parent(toejian_loc, heel_loc)
    cmds.parent(heel_loc, heeloff_loc)
    cmds.parent(heeloff_loc, ankle_loc)

    # ik
    ankle_ik = \
    cmds.ikHandle(sj=R_leg_int[0], ee=R_leg_int[2], n='%s_%s_%s_%s' % (n, LR, 'ankle', 'ik'), sol='ikRPsolver')[0]
    ball_ik = \
    cmds.ikHandle(sj=R_leg_int[2], ee=R_leg_int[3], n='%s_%s_%s_%s' % (n, LR, 'ball', 'ik'), sol='ikSCsolver')[0]
    toe_ik = cmds.ikHandle(sj=R_leg_int[3], ee=R_leg_int[4], n='%s_%s_%s_%s' % (n, LR, 'toe', 'ik'), sol='ikSCsolver')[
        0]
    cmds.parent(ankle_ik, ball_loc)
    cmds.parent(ball_ik, ball_loc)
    cmds.parent(toe_ik, toe_loc)

    # foot con
    footpos = [[0.5, 0.5, 0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5], \
               [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], \
               [-0.5, 0.5, -0.5], [-0.5, 0.5, 0.5], [0.5, 0.5, 0.5], \
               [0.5, -0.5, 0.5], [0.5, -0.5, -0.5], [-0.5, -0.5, -0.5], \
               [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [-0.5, -0.5, 0.5], [-0.5, 0.5, 0.5]]
    footcon_cv = cmds.curve(d=1, p=footpos, n=n + '_' + LR + '_foot_con')

    attr(footcon_cv, 1)
    footcon_grp = add_grp(footcon_cv, n, LR, 'foot')

    # 添加属性
    add_attr(footcon_cv, 'roll', 5)
    add_attr(footcon_cv, 'tilt', 1)
    add_attr(footcon_cv, 'toe', 0)
    add_attr(footcon_cv, 'toe_spin', 0)
    add_attr(footcon_cv, 'toe_wiggle', 0)
    add_attr(footcon_cv, 'heel', 5)
    add_attr(footcon_cv, 'stretch', 2)
    add_attr(footcon_cv, 'leg_lenght', 3)
    add_attr(footcon_cv, 'knee_lenght', 3)
    add_attr(footcon_cv, 'global_scale', 3)

    # foot控制器位置
    real_snap(R_leg_int[2], footcon_grp, 0)
    cmds.parent(ankle_loc, footcon_cv)

    # 极向量locater
    place_correct_pole_locator(R_leg_int[0], R_leg_int[1], R_leg_int[2])
    locater = cmds.rename(cmds.ls(sl=1), '%s_%s_%s_%s' % (n, LR, 'leg_pole', 'loc'))
    # pole con
    polepos = [[0.5, 0.0, 0.0], [0.0, 0.0, 0.5], [-0.5, 0.0, 0.0], \
               [0.0, 0.0, -0.5], [0.5, 0.0, 0.0], [0.0, 0.5, 0.0], \
               [-0.5, 0.0, 0.0], [0.0, -0.5, 0.0], [0.0, 0.0, -0.5], \
               [0.0, 0.5, 0.0], [0.0, 0.0, 0.5], [0.0, -0.5, 0.0], [0.5, 0.0, 0.0]]
    polecon_cv = cmds.curve(d=1, p=polepos, n='%s_%s_%s_%s' % (n, LR, 'leg_pole', 'con'))

    polecon_grp = add_grp(polecon_cv, n, LR, 'leg_pole_con')
    real_snap(locater, polecon_grp, 0)

    attr(polecon_cv, 2)
    add_attr(polecon_cv, 'follow', 4)

    cmds.parent(locater, polecon_cv)
    # 连接属性
    cmds.connectAttr(footcon_cv + '.leg_lenght', R_leg_int[0] + '.sx')
    cmds.connectAttr(footcon_cv + '.knee_lenght', R_leg_int[1] + '.sx')

    roll_mul = cmds.createNode('multiplyDivide', n='%s_%s_%s' % (n, LR, 'roll_mul'))
    cmds.connectAttr(footcon_cv + '.roll', roll_mul + '.input1X')
    cmds.setAttr(roll_mul + '.input2X', -1)
    cmds.connectAttr(roll_mul + '.outputX', ball_loc + '.rotateZ')

    cmds.connectAttr(footcon_cv + '.toe', toe_loc + '.rotateZ')
    cmds.connectAttr(footcon_cv + '.toe_spin', toejian_loc + '.rotateY')
    cmds.connectAttr(footcon_cv + '.toe_wiggle', toejian_loc + '.rotateZ')
    cmds.connectAttr(footcon_cv + '.heel', heel_loc + '.rotateZ')
    # tilt
    cmds.setDrivenKeyframe(outside_loc + '.rotateX', cd=footcon_cv + '.tilt', v=0)
    cmds.setAttr(footcon_cv + '.tilt', 90)
    cmds.setDrivenKeyframe(outside_loc + '.rotateX', cd=footcon_cv + '.tilt', v=-90)
    cmds.setAttr(footcon_cv + '.tilt', 0)
    cmds.setDrivenKeyframe(inside_loc + '.rotateX', cd=footcon_cv + '.tilt', v=0)
    cmds.setAttr(footcon_cv + '.tilt', -90)
    cmds.setDrivenKeyframe(inside_loc + '.rotateX', cd=footcon_cv + '.tilt', v=90)
    cmds.setAttr(footcon_cv + '.tilt', 0)
    # follow
    cmds.poleVectorConstraint(polecon_cv, ankle_ik)
    polepar = cmds.parentConstraint(footcon_cv, polecon_grp, mo=1)
    cmds.connectAttr(polecon_cv + '.follow', polepar[0] + '.' + footcon_cv + 'W0')

    leg_loc = snap_joint(R_leg_int[0], 0)[0]
    knee_loc = snap_joint(R_leg_int[1], 0)[0]
    # 测量距离
    cmds.distanceDimension(sp=attr(leg_loc, 4), ep=attr(R_leg_int[2], 4))
    dis = cmds.rename(cmds.ls(sl=1)[1], '%s_%s_%s_%s' % (n, LR, 'leg', 'dis'))
    cmds.pointConstraint(R_leg_int[0], leg_loc, mo=1)
    disup = cmds.distanceDimension(sp=attr(leg_loc, 4), ep=attr(knee_loc, 4))
    disdw = cmds.distanceDimension(sp=attr(knee_loc, 4), ep=attr(R_leg_int[2], 4))
    zonglength = cmds.getAttr(disup + '.distance') + cmds.getAttr(disdw + '.distance')
    cmds.delete(knee_loc)
    cmds.select(cl=1)

    # 拉伸

    dis_mul = cmds.createNode('multiplyDivide', n='%s_%s_%s' % (n, LR, 'distnce_mul'))
    cmds.setAttr(dis_mul + '.operation', 2)

    cmds.connectAttr(dis + '.distance', dis_mul + '.input1X')

    condition = cmds.createNode('condition', n='%s_%s_%s' % (n, LR, 'condition'))
    cmds.setAttr(condition + '.operation', 2)
    cmds.connectAttr(dis_mul + '.outputX', condition + '.firstTerm')
    cmds.connectAttr(dis_mul + '.outputX', condition + '.colorIfTrueR')
    cmds.setAttr(condition + '.secondTerm', zonglength)
    cmds.setAttr(condition + '.colorIfFalseR', zonglength)

    scale_mul = cmds.createNode('multiplyDivide', n='%s_%s_%s' % (n, LR, 'scale_mul'))
    cmds.setAttr(scale_mul + '.operation', 2)

    cmds.connectAttr(condition + '.outColorR', scale_mul + '.input1X')
    cmds.setAttr(scale_mul + '.input2X', zonglength)

    joint_mul = cmds.createNode('multiplyDivide', n='%s_%s_%s' % (n, LR, 'joint_mul'))

    blendColor = cmds.createNode('blendColors', n='%s_%s_%s' % (n, LR, 'blendColor'))
    cmds.connectAttr(footcon_cv + '.stretch', blendColor + '.blender')

    cmds.connectAttr(scale_mul + '.outputX', blendColor + '.color1R')
    cmds.setAttr(blendColor + '.color2R', 1)

    cmds.connectAttr(blendColor + '.outputR', joint_mul + '.input1X')
    cmds.connectAttr(blendColor + '.outputR', joint_mul + '.input1Y')

    cmds.setAttr(joint_mul + '.input2X', attr(R_leg_int[1], 0))
    cmds.setAttr(joint_mul + '.input2Y', attr(R_leg_int[2], 0))

    cmds.connectAttr(joint_mul + '.outputX', R_leg_int[1] + '.translateX')
    cmds.connectAttr(joint_mul + '.outputY', R_leg_int[2] + '.translateX')

    cmds.connectAttr(footcon_cv + '.global_scale', dis_mul + '.input2X')
    # 大纲整理
    attr(dis, 3)
    attr(leg_loc, 3)
    attr(locater, 3)
    attr(ankle_loc, 3)
    ik_rig_grp = cmds.group(R_leg_int[0], dis, leg_loc, polecon_grp, footcon_grp, n='%s_%s_%s' % (n, LR, 'leg_ik_grp'))

    # ============================================ikfk切换====================================
    # ikfk con
    ikfkpos = [[-0.2, 1.0, 0.0], [0.2, 1.0, 0.0], [0.2, 0.2, 0.0], \
               [1.0, 0.2, 0.0], [1.0, -0.2, 0.0], [0.2, -0.2, 0.0], \
               [0.2, -1.0, 0.0], [-0.2, -1.0, 0.0], [-0.2, -0.2, 0.0], \
               [-1.0, -0.2, 0.0], [-1.0, 0.2, 0.0], [-0.2, 0.2, 0.0], [-0.2, 1.0, 0.0]]

    ikfk_cv = cmds.curve(d=1, p=ikfkpos, n='%s_%s_%s_%s' % (n, LR, 'ikfk', 'con'))

    attr(ikfk_cv, 5)
    add_attr(ikfk_cv, 'switch', 2)
    ikfk_grp = add_grp(ikfk_cv, n, LR, 'ikfk')
    real_snap(R_leg_int[2], ikfk_grp, 0)

    # 约束
    parent_leg = cmds.parentConstraint(R_leg_int[0], R_leg_fkInt[0], R_leg_skInt[0], mo=True)
    parent_knee = cmds.parentConstraint(R_leg_int[1], R_leg_fkInt[1], R_leg_skInt[1], mo=True)
    parent_ankle = cmds.parentConstraint(R_leg_int[2], R_leg_fkInt[2], R_leg_skInt[2], mo=True)
    parent_ball = cmds.parentConstraint(R_leg_int[3], R_leg_fkInt[3], R_leg_skInt[3], mo=True)

    ikfk_blend = cmds.createNode('blendColors', n='%s_%s_%s' % (n, LR, 'ikfk_blendColor'))
    cmds.connectAttr(ikfk_cv + '.switch', ikfk_blend + '.blender')

    reverse = cmds.createNode('reverse', n='%s_%s_%s' % (n, LR, 'reverse'))
    cmds.connectAttr(ikfk_blend + '.outputR', reverse + '.inputX')

    cmds.connectAttr(ikfk_blend + '.outputR', parent_leg[0] + '.' + R_leg_int[0] + 'W0')
    cmds.connectAttr(reverse + '.outputX', parent_leg[0] + '.' + R_leg_fkInt[0] + 'W1')

    cmds.connectAttr(ikfk_blend + '.outputR', parent_knee[0] + '.' + R_leg_int[1] + 'W0')
    cmds.connectAttr(reverse + '.outputX', parent_knee[0] + '.' + R_leg_fkInt[1] + 'W1')

    cmds.connectAttr(ikfk_blend + '.outputR', parent_ankle[0] + '.' + R_leg_int[2] + 'W0')
    cmds.connectAttr(reverse + '.outputX', parent_ankle[0] + '.' + R_leg_fkInt[2] + 'W1')

    cmds.connectAttr(ikfk_blend + '.outputR', parent_ball[0] + '.' + R_leg_int[3] + 'W0')
    cmds.connectAttr(reverse + '.outputX', parent_ball[0] + '.' + R_leg_fkInt[3] + 'W1')

    cmds.connectAttr(ikfk_blend + '.outputR', polecon_grp + '.visibility')
    cmds.connectAttr(ikfk_blend + '.outputR', footcon_grp + '.visibility')

    cmds.connectAttr(reverse + '.outputX', fk_grp + '.visibility')

    # 整理层级
    attr(R_leg_fkInt[0], 3)
    attr(R_leg_int[0], 3)
    cmds.group(R_leg_fkInt[0], fk_grp, R_leg_skInt[0], ik_rig_grp, ikfk_grp,
               n='%s_%s_%s_%s' % (n, LR, 'leg_rig', 'grp'))

    sel = cmds.ls(type='unknown')
    cmds.delete(sel[0])

    cmds.setAttr(R_leg_skInt[4] + '.drawStyle', 2)
    cmds.setAttr(R_leg_skInt[5] + '.drawStyle', 2)
    cmds.setAttr(R_leg_skInt[6] + '.drawStyle', 2)
    cmds.setAttr(R_leg_skInt[7] + '.drawStyle', 2)

    # con color
    color_set(fk_grp, 'blue')
    color_set(ikfk_grp, 'blue')
    color_set(polecon_grp, 'blue')
    color_set(footcon_grp, 'blue')


# ====================================UI=================================
def leg_rig_UI():
    # coding:UTF-8
    if cmds.window('腿部绑定', exists=True):
        cmds.deleteUI('腿部绑定', window=True)
    cmds.window('腿部绑定')
    cmds.columnLayout(columnAttach=('both', 5), rowSpacing=5, columnWidth=300)
    cmds.text(label='角色名称：')
    cmds.textField('name')

    cmds.button(label='                                          导入骨骼                                          ',
                c=import_joint)

    cmds.checkBox('checkBox_test', l='手动校轴(校轴后勾选。校轴方法参照提示）', v=False, cc='auto_joint()')
    cmds.button(label='                                          镜像骨骼                                          ',
                c=mirror_joint)
    cmds.button(label='                                          生成控制                                          ',
                c=l_leg_rig)

    cmds.frameLayout(label='提示', cl=True, cll=True, borderStyle='etchedOut', bgc=[0, 0.25, 0.5])
    cmds.columnLayout(w=10, rowSpacing=5, columnWidth=300)

    cmds.text(label='1.使用方法：')
    cmds.text(label='腿部所有骨骼平行Z轴时（正常情况）：依次点击三个按钮')
    cmds.text(label='腿型特殊时：导入骨骼手动校轴后需要勾选\"手动校轴\"')
    cmds.text(label='生成控制后 ==> 需要关联footCon 的 globalScale')

    cmds.text(label='2.手动校轴方法：')
    cmds.text(label='leg、knee骨骼的 Y轴 指向物体方向==>向前')
    cmds.text(label='ankle、ball骨骼的 Y轴 在同一平面与脚面垂直==>向上')

    cmds.setParent('..')
    cmds.setParent('..')

    cmds.showWindow()


# =============================================================
if __name__ == '__main__':
    leg_rig_UI()
