# -*- coding: utf-8 -*-
"""
@FileName    :   joint_orient_ transfer.py
@DateTime    :   2023/04/20 11:12:22
@Author  :   Tian Chao
@Contact :   tianchao0533@163.com
"""

import json
import pymel.core as pm


def joint_orient_to_json(dady_joint: str, rite_json_path: str) -> dict:
	"""
	将父骨骼之下的所有骨骼的joint orient值写入json文件
	Args:
		dady_joint: 父骨骼
		rite_json_path: json文件路径

	Returns:骨骼轴向字典

	"""
	selection = pm.PyNode(dady_joint)  # 父骨骼放入变量

	joints = pm.ls(selection[0], dag=True, type="joint")  # 列出骨骼链的所有骨骼

	jnt_jo_attr = ['{}.jointOrient'.format(jnt) for jnt in joints]  # 获取骨骼jointOrient属性列表
	jnt_jo_val = [pm.getAttr(val) for val in jnt_jo_attr]  # 获取获取骨骼jointOrient属性列表属性值向量列表
	jnt_jo_val_list = [list(vec) for vec in jnt_jo_val]  # 获取获取骨骼jointOrient属性列表属性值列表
	data = dict(zip(jnt_jo_attr, jnt_jo_val_list))  # 将属性和属性值打包成字典

	jsondata = json.dumps(data)  # 将字典转化成json格式
	with open(rite_json_path, 'w') as f:  # 打开json文件
		f.write(jsondata)  # 写入字典数据
	return data  # 返回字典


def json_to_joint_orient(mesh_list: list, read_json_path: str) -> dict:
	"""

	Args:
		mesh_list: 要修改蒙皮的模型列表
		read_json_path: json文件路径

	Returns:骨骼轴向字典

	"""
	skin_clusters = [pm.listHistory(mesh, type='skinCluster') for mesh in mesh_list]  # 获取所有模型的蒙皮节点
	# 将所有蒙皮节点打开骨骼移动模式
	for cluster in skin_clusters:
		pm.skinCluster(cluster, edit=True, moveJointsMode=True)
	# 读取并转码json文件数据
	with open(read_json_path, 'r') as f:
		data = f.read()
	dict_data = json.JSONDecoder().decode(data)
	# del dict_data['facebase.jointOrient']

	# 设置骨骼属性
	for k, v in dict_data.items():
		pm.setAttr(k, v)
	# 将所有蒙皮节点关闭骨骼移动模式
	for cluster in skin_clusters:
		pm.skinCluster(cluster, edit=True, moveJointsMode=False)

	jnt = pm.skinCluster(skin_clusters[0], query=True, inf=True)[1]  # 通过蒙皮节点获取一根骨骼
	root_joint = jnt.getAllParents()[-1]  # 获取该骨骼的根骨骼
	jnt_list = pm.ls(root_joint, dag=True, type="joint")  # 获取该根骨骼的整个骨骼链
	pm.select(jnt_list)  # 选中骨骼链中的所有骨骼
	dag_pose = pm.dagPose(bindPose=True, q=True)  # 获取所有骨骼的绑定姿态
	pm.delete(dag_pose)  # 删除所有绑定姿态
	pm.dagPose(bindPose=True, save=True)  # 创建新绑定姿态
	return dict_data  # 返回属性信息


"""--------------------------------函数使用-----------------------------------------"""

# dadyjoint = pm.selected()
# jo_json_path = r'D:\Backup\Documents\maya\scripts\joint_orient.json'
# joint_orient_to_json(dadyjoint, jo_json_path)

# meshlist = pm.selected()
# jo_json_path = r'D:\Backup\Documents\maya\scripts\joint_orient.json'
# json_to_joint_orient(meshlist, jo_json_path)
