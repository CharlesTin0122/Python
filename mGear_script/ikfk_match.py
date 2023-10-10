import pymel.core as pm
from mgear.core import anim_utils

# 选择所有控制器并尅帧

# grp = "rig_controllers_grp"  # 所有控制器组的名称
# members = pm.PyNode(grp).members()
# pm.setKeyframe(members)

# 获取时间栏首末帧
env = pm.Env()
max_time = env.getMaxTime()
min_time = env.getMinTime()
# 获取手脚host控制器
arm_r_host = pm.PyNode("armUI_R0_ctl")
arm_l_host = pm.PyNode("armUI_L0_ctl")
leg_r_host = pm.PyNode("legUI_R0_ctl")
leg_l_host = pm.PyNode("legUI_L0_ctl")
# 遍历时间栏并将FK匹配到IK
for frame in range(int(min_time), int(max_time) + 1):
    # 设置当前帧设置为FK
    pm.currentTime(frame)
    arm_r_host.arm_blend.set(0)
    arm_l_host.arm_blend.set(0)
    leg_r_host.leg_blend.set(0)
    leg_l_host.leg_blend.set(0)
    # 将FK匹配到IK
    anim_utils.ikFkMatch(
        "rig",
        "arm_blend",
        "armUI_R0_ctl",
        ["arm_R0_fk0_ctl", "arm_R0_fk1_ctl", "arm_R0_fk2_ctl"],
        "arm_R0_ik_ctl",
        "arm_R0_upv_ctl"
    )
    anim_utils.ikFkMatch(
        "rig",
        "arm_blend",
        "armUI_L0_ctl",
        ["arm_L0_fk0_ctl", "arm_L0_fk1_ctl", "arm_L0_fk2_ctl"],
        "arm_L0_ik_ctl",
        "arm_L0_upv_ctl"
    )
    anim_utils.ikFkMatch(
        "rig",
        "leg_blend",
        "legUI_R0_ctl",
        ["leg_R0_fk0_ctl", "leg_R0_fk1_ctl", "leg_R0_fk2_ctl"],
        "leg_R0_ik_ctl",
        "leg_R0_upv_ctl",
    )
    anim_utils.ikFkMatch(
        "rig",
        "leg_blend",
        "legUI_L0_ctl",
        ["leg_L0_fk0_ctl", "leg_L0_fk1_ctl", "leg_L0_fk2_ctl"],
        "leg_L0_ik_ctl",
        "leg_L0_upv_ctl",
    )
