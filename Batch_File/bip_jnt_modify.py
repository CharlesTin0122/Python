# -*- coding: utf-8 -*-
"""
@FileName      : bip_jnt_modify.py
@DateTime      : 2024/05/23 17:05:32
@Author        : Tian Chao
@Contact       : tianchao0533@163.com
@Software      : Maya 2024.2
@PythonVersion : python 3.10.8
@librarys      : pymel 1.4.0
@Description   :
"""

import pymel.core as pm

# maya时间设置
pm.currentUnit(time="ntsc")  # 30fps
time_value = pm.keyframe(
    "Bip001.rotateX", query=True, timeChange=True, absolute=True
)  # 获取骨骼动画时长
# 设置首末帧，round四舍五入，舍去小数帧
first_frame = round(time_value[0])
last_frame = round(time_value[-1])
pm.env.setMinTime(first_frame)
pm.env.setMaxTime(last_frame)
# 设置当前帧为第0帧
pm.setCurrentTime(0)
# 设置变量
jnts = ["weapon_L", "weapon_R"]

weapon_l = pm.nodetypes.Joint("weapon_L")
weapon_r = pm.nodetypes.Joint("weapon_R")

weapon_l_matrix = [
    -0.8106585875962652,
    -0.550373023256934,
    -0.19980597600183178,
    0.0,
    0.5806263330224721,
    -0.7996543815908144,
    -0.15305610024459432,
    0.0,
    -0.07553775754875423,
    -0.24008879596756177,
    0.9678075310904293,
    0.0,
    9.291847229003906,
    1.5546540021896362,
    2.279982328414917,
    1.0,
]

weapon_r_matrix_sword = [
    0.6539482754137247,
    0.7215536562066229,
    -0.2274026699453418,
    0.0,
    -0.7367404743293531,
    0.6757003883073929,
    0.025346769541666446,
    0.0,
    0.1719451266200214,
    0.15096127469021056,
    0.9734708865577499,
    0.0,
    9.282442092895508,
    2.597752094268799,
    0.9325157403945923,
    1.0,
]

weapon_r_matrix_long = [
    -0.4953533356762547,
    0.8306557596401006,
    0.2542362716276629,
    0.0,
    -0.8021417773522256,
    -0.5497201995559207,
    0.23318720210682894,
    0.0,
    0.3334571064779099,
    -0.08842347639018606,
    0.9386094219442154,
    0.0,
    -9.624337196350098,
    8.965066909790039,
    -48.42610549926758,
    1.0,
]

weapon_r_matrix_bow = [
    0.9607324820165305,
    -0.10296465248028168,
    -0.25766524472262803,
    0.0,
    -0.26963233654521185,
    -0.12719188562965345,
    -0.9545263890114003,
    0.0,
    0.06550954959031982,
    0.986519388846255,
    -0.14995997580316378,
    0.0,
    8.799854278564453,
    3.300562620162964,
    0.2589511573314667,
    1.0,
]

# 移除骨骼动画
for jnt in jnts:
    wp_jnt = pm.nodetypes.Joint(jnt)
    attrs = wp_jnt.listAnimatable()
    for attr in attrs:
        attr.disconnect()

# 设置骨骼位置
weapon_l.setMatrix(weapon_l_matrix)
pm.setKeyframe(weapon_l)
weapon_r.setMatrix(weapon_r_matrix_bow)
pm.setKeyframe(weapon_r)
# 设置Biped骨架扭曲骨骼位置
for frame in range(last_frame + 1):
    pm.currentTime(frame)

    upperarm_r = pm.nodetypes.Joint("Bip001FBXASC032RFBXASC032UpperArm")
    upperarm_r_matrix = upperarm_r.getMatrix()
    UpArmTwist_r = pm.nodetypes.Joint("Bip001FBXASC032RUpArmTwist")
    UpArmTwist_r.setMatrix(upperarm_r_matrix)
    pm.setKeyframe(UpArmTwist_r)

    upperarm_l = pm.nodetypes.Joint("Bip001FBXASC032LFBXASC032UpperArm")
    upperarm_l_matrix = upperarm_l.getMatrix()
    UpArmTwist_l = pm.nodetypes.Joint("Bip001FBXASC032LUpArmTwist")
    UpArmTwist_l.setMatrix(upperarm_l_matrix)
    pm.setKeyframe(UpArmTwist_l)

    Forearm_r = pm.nodetypes.Joint("Bip001FBXASC032RFBXASC032Forearm")
    Forearm_r_matrix = Forearm_r.getMatrix()
    ForeTwist_r = pm.nodetypes.Joint("Bip001FBXASC032RFBXASC032ForeTwist")
    ForeTwist_r.setMatrix(Forearm_r_matrix)
    pm.setKeyframe(ForeTwist_r)

    Forearm_l = pm.nodetypes.Joint("Bip001FBXASC032LFBXASC032Forearm")
    Forearm_l_matrix = Forearm_l.getMatrix()
    ForeTwist_l = pm.nodetypes.Joint("Bip001FBXASC032LFBXASC032ForeTwist")
    ForeTwist_l.setMatrix(Forearm_l_matrix)
    pm.setKeyframe(ForeTwist_l)
