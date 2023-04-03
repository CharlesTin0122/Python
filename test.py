import pymel.core as pm
import json


def get_joint_hierarchy(root_joint):
    """
    获取骨骼层级信息
    :param root_joint: joint
    :return: 层级列表
    """
    hierarchy = []
    joint_list = [root_joint]
    while joint_list:
        current_joint = joint_list.pop(0)
        hierarchy.append(current_joint.name())
        children = current_joint.getChildren(ad=True, type='joint')
        joint_list.extend(children)
    return hierarchy


# 获取场景中的根骨骼
root_joint = pm.ls(type='joint', l=True)[0]

# 获取骨骼层级信息
joint_hierarchy = get_joint_hierarchy(root_joint)

# 将骨骼层级信息写入JSON文件
with open('joint_hierarchy.json', 'w') as f:
    json.dump(joint_hierarchy, f)

