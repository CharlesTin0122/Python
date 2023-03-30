import pymel.core as pm
import pymel.core.nodetypes as nt
import json


def hierarchy2json(parents, dump2json=True, tree=None, init=True,):
	"""
	该函数的作用是将指定的父节点列表转换为 JSON 格式的层级结构。具体实现方法为：
	遍历每个父节点，初始化一个子字典，然后递归处理其子节点，并将子节点添加到子字典中。
	如果遍历完了所有的父节点，则返回处理结果。
	其中，如果指定了 dump2json 参数为 True,则将结果转换为 JSON 格式并返回；否则返回字典格式的结果。

	Args:
			parents (list): 是指定的父节点列表
			dump2json (bool, optional): 是否将结果转换为 JSON 格式并返回
			tree (dict, optional): 指定的目标字典
			init (bool, optional): 是否为根节点

	Returns:
			dict or json: 字典
	"""
	# 如果 parents 不是列表类型，则转换为列表类型
	if isinstance(parents, list):
		parents = parents
	else:
		parents = [parents]

	# 如果 tree 不是字典类型，则初始化一个字典	
	if not isinstance(tree, dict):
		for p in parents:
			if isinstance(p, nt.Transform):
				_tree = {str(p): {}}
			else:
				_tree = {str(p): {p.type()}}
	else:
		_tree = tree

	# 遍历每个父节点
	for parent in parents:
	 # 如果不是根节点，则使用指定的 tree 字典
		if init:
			tree = _tree[str(parent)]
		else:
			tree = _tree

		# 遍历每个子节点
		for child in parent.getChildren():
			# 初始化子节点的字典
			if isinstance(child, nt.Transform):
				tree[str(child)] = {}
			else:
				tree[str(child)] = child.type()

			hierarchy2json(child, tree=tree[str(child)], init=False)  # 递归处理子节点
	# 如果是根节点，则返回处理结果（可以选择将结果转换为 JSON 格式）
	if init:
		return json.dumps(_tree) if dump2json else _tree

# for sel in pm.selected():
#     print(json.dumps(hierarchy2json(sel)))
print((hierarchy2json(pm.selected())))



def getRelParent(jnt_list,root):
	"""
	getRelParent 根据长名称获取骨骼列表的父子关系

	Args:
		jnt_list (	list): 蒙皮骨骼列表
		root (Joint): 根骨骼

	Returns:
		dict: 骨骼的父子关系
	"""
	jnt_parent = {} #创建父子关系字典
	#遍历骨骼列表中的每个骨骼
	for jnt in jnt_list:
		hi_tree = jnt.longName().split("|")[1:-1]
		parent = None
		while parent not in jnt_list:
			if not hi_tree: 
				parent = root
				break
			parent = pm.PyNode(hi_tree.pop())
		jnt_parent[jnt] = parent if parent != root else parent
	return jnt_parent
	
jnt_list = pm.ls(sl=True)
root = jnt_list[0]
a = getRelParent(jnt_list,root)



'''-----------------------------------------------------------------------方法2-------------------------------------------------------------------------'''

import maya.cmds as mc

def hierarchyTree(parent, tree):
	children = mc.listRelatives(parent, c=True, type='transform')
	if children:
		tree[parent] = (children, {})
		for child in children:
			hierarchyTree(child, tree[parent][1])

top_node = mc.ls(sl=True)[0]
hierarchy_tree = {}
hierarchyTree(top_node, hierarchy_tree)


def reparent(tree):
	for parent, data in tree.iteritems():
		children, child_tree = data
		mc.parent(children, parent)
		reparent(child_tree)

reparent(hierarchy_tree)