# -*- coding: utf-8 -*-
# @FileName :  snake_rig.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/4/14 15:15
# @Software : PyCharm
# Description:
import pymel.core as pm


def create_snake_rig(snake_model, snake_skeleton):
    """
    This function creates a snake rig with controls for a given snake model and skeleton.

    :param snake_model: The snake model to create the rig for.
    :type snake_model: str
    :param snake_skeleton: The snake skeleton to create the rig for.
    :type snake_skeleton: str
    :return: The root control of the snake rig.
    :rtype: PyNode
    """

    # Create a new group to contain the rig
    snake_rig_grp = pm.group(empty=True, name='{}_rig_grp'.format(snake_model))

    # Create a new joint chain to use as the IK handle chain
    ik_joints = pm.duplicate(snake_skeleton, renameChildren=True)
    for joint in ik_joints:
        joint.replace('jnt', 'ik_jnt')

    # Create an IK handle for the new joint chain
    ik_handle, effector = pm.ikHandle(startJoint=ik_joints[0], endEffector=ik_joints[-1], solver='ikSplineSolver')

    # Create a curve to use as the IK handle curve
    curve = pm.curve(name='{}_curve'.format(snake_model),
                     degree=3,
                     point=[(0, 0, 0), (0, 5, 0), (0, 10, 0), (0, 15, 0)])

    # Attach the curve to the IK handle
    pm.parent(curve, snake_rig_grp)
    pm.parent(ik_handle, curve)

    # Create a cluster for each CV on the curve
    clusters = []
    for i in range(curve.numCVs()):
        cluster = pm.cluster('{}.cv[{}]'.format(curve.name(), i),
                             name='{}_cluster_{}'.format(snake_model, i))
        clusters.append(cluster)

    # Create a control for each cluster
    controls = []
    for cluster in clusters:
        control = pm.circle(name='{}_ctrl'.format(cluster), normal=(1, 0, 0), radius=0.5)[0]
        pm.parent(control, snake_rig_grp)
        pm.matchTransform(control, cluster)
        pm.parent(cluster, control)
        controls.append(control)

    # Create a root control for the snake rig
    root_control = pm.circle(name='{}_root_ctrl'.format(snake_model), normal=(1, 0, 0), radius=1)[0]
    pm.parent(root_control, snake_rig_grp)
    pm.matchTransform(root_control, snake_skeleton)

    # Parent the IK handle to the root control
    pm.parent(ik_handle, root_control)

    # Create a bend deformer for the curve
    bend_deformer = pm.nonLinear(curve, type='bend')[0]
    pm.parent(bend_deformer, root_control)

    # Connect the root control to the bend deformer
    pm.connectAttr('{}.rotateX'.format(root_control), '{}.curvature'.format(bend_deformer))

    # Connect the controls to the IK handle
    for i in range(len(controls)):
        pm.connectAttr('{}.translate'.format(controls[i]), '{}.clusterOffset[{}].translate'.format(clusters[i], i))

    return root_control


"""
这是一个使用PyMel创建蛇类生物绑定的脚本。它会创建一个包含控制器和绑定的组，并返回根控制器的PyNode对象。

脚本的大致流程如下：

1. 创建一个新的组来包含绑定和控制器。
2. 复制蛇的骨骼，创建一个新的关节链作为IK控制器链。
3. 为新的关节链创建一个IK控制器。
4. 创建一个曲线来作为IK控制器的曲线。
5. 为曲线上的每个CV创建一个集群。
6. 为每个集群创建一个控制器。
7. 创建一个根控制器来控制整个蛇的姿态。
8. 将IK控制器的根节点连接到根控制器。
9. 为曲线创建一个弯曲变形器，并将其连接到根控制器。
10. 将每个控制器连接到相应的集群。

你需要提供蛇的模型和骨骼的名称作为参数来运行这个脚本。
"""
