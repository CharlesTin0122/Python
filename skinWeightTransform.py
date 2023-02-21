import maya.cmds as cmds

def transfer_skin_weights(source_joint, target_joint):
    """
    将source_joint的蒙皮权重传递给target_joint
    """
    # 获取源和目标的mesh
    source_mesh = cmds.skinCluster(source_joint, query=True, geometry=True)[0]
    target_mesh = cmds.skinCluster(target_joint, query=True, geometry=True)[0]

    # 获取源和目标的蒙皮权重
    source_weights = cmds.skinPercent(source_joint, source_mesh, query=True, value=True)
    target_weights = cmds.skinPercent(target_joint, target_mesh, query=True, value=True)

    # 将源的蒙皮权重传递到目标
    for i, weight in enumerate(source_weights):
        cmds.skinPercent(target_joint, target_mesh, transformValue=[(source_joint, weight), (i, target_weights[i] + weight)])

# 选择源和目标骨骼
source_joint = cmds.ls(selection=True)[0]
target_joint = cmds.ls(selection=True)[1]

# 将蒙皮权重从源骨骼传递到目标骨骼
transfer_skin_weights(source_joint, target_joint)
