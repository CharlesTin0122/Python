import pymel.core as pm
from mgear.core import anim_utils

name_space = ""

# ikfkmatch
anim_utils.ikFkMatch_with_namespace(
    name_space,
    "arm_blend",
    "armUI_R0_ctl",
    ["arm_R0_fk0_ctl", "arm_R0_fk1_ctl", "arm_R0_fk2_ctl"],
    "arm_R0_ik_ctl",
    "arm_R0_upv_ctl",
    ik_rot="arm_R0_ikRot_ctl",
)

anim_utils.ikFkMatch_with_namespace(
    name_space,
    "arm_blend",
    "armUI_L0_ctl",
    ["arm_L0_fk0_ctl", "arm_L0_fk1_ctl", "arm_L0_fk2_ctl"],
    "arm_L0_ik_ctl",
    "arm_L0_upv_ctl",
    ik_rot="arm_L0_ikRot_ctl",
)

anim_utils.ikFkMatch_with_namespace(
    name_space,
    "leg_blend",
    "legUI_R0_ctl",
    ["leg_R0_fk0_ctl", "leg_R0_fk1_ctl", "leg_R0_fk2_ctl"],
    "leg_R0_ik_ctl",
    "leg_R0_upv_ctl",
)

anim_utils.ikFkMatch_with_namespace(
    name_space,
    "leg_blend",
    "legUI_L0_ctl",
    ["leg_L0_fk0_ctl", "leg_L0_fk1_ctl", "leg_L0_fk2_ctl"],
    "leg_L0_ik_ctl",
    "leg_L0_upv_ctl",
)

# select all
grp = "rig_controllers_grp"
if name_space:
    grp = name_space + ":" + grp
members = pm.PyNode(grp).members()
pm.select(members, r=True)

# key all
grp = "rig_controllers_grp"
if name_space:
    grp = name_space + ":" + grp
members = pm.PyNode(grp).members()
pm.setKeyframe(members)
