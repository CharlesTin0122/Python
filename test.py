import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim


def split_target():
    """获取两个选择物体的长名称"""
    selected = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(selected)
    if selected.length() != 2:
        return
    target_path = OpenMaya.MDagPath()
    base_path = OpenMaya.MDagPath()
    selected.getDagPath(0, target_path)
    selected.getDagPath(1, base_path)
    print(target_path.fullPathName(), base_path.fullPathName())
    """获取两个模型的点坐标"""
    target_points = OpenMaya.MPointArray()
    base_points = OpenMaya.MPointArray()
    target_mesh_fn = OpenMaya.MFnMesh(target_path)
    target_mesh_fn.getPoints(target_points)
    print(target_points.length())
    base_mesh_fn = OpenMaya.MFnMesh(base_path)
    base_mesh_fn.getPoints(base_points)
    print(base_points.length())
    """获取蒙皮节点"""
    skin_cluster = []
    status = OpenMaya.MGlobal.executeCommand("findRelatedSkinCluster " + base_path.fullPathName(), skin_cluster)
    if status == 0 or len(skin_cluster) == 0:
        return
    skin_cluster = skin_cluster[0]
    print(skin_cluster)
    """获取蒙皮权重"""
    skin_node = OpenMaya.MSelectionList()
    skin_node.add(skin_cluster)
    skin_depen_node = OpenMaya.MObject()
    skin_node.getDependNode(0, skin_depen_node)
    joint_path = OpenMaya.MDagPathArray()
    skin_fn = OpenMayaAnim.MFnSkinCluster(skin_cluster)
    skin_fn.influenceObjects(joint_path)
    joint_names = []
    for i in range(joint_path.length()):
        joint_names.append(joint_path[i].fullPathName())
    print(joint_names)
    base_obj_vtxs = OpenMaya.MSelectionList()
    base_obj_vtxs.add(base_path.fullPathName() + ".vtx[*]")
    components = OpenMaya.MObject()
    base_obj_vtxs.getDagPath(0, base_path, components)
    influenceindeices = OpenMaya.MIntArray()
    weights = []
    for i in range(joint_path.length()):
        influenceindeices.append(i)
    skin_fn.getWeights(base_path, components, influenceindeices, weights)


split_target()
