import pymel.core as pm
import pymel.core.nodetypes as nt
import json

def hierarchy2json(parents,dump2json=True,tree=None,init=True,):
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
	parents = parents if isinstance(parents,list) else [parents]
	# 如果 tree 不是字典类型，则初始化一个字典
	_tree = {str(p):{} if isinstance(p,nt.Transform) else p.type() for p in parents} if not isinstance(tree,dict) else tree
	 # 遍历每个父节点
	for parent in parents:
		tree = _tree[str(parent)] if init else _tree # 如果不是根节点，则使用指定的 tree 字典
		# 遍历每个子节点
		for child in parent.getChildren(): 
			tree[str(child)] = {} if isinstance(child,nt.Transform) else child.type() # 初始化子节点的字典
			hierarchy2json(child,tree=tree[str(child)],init=False)# 递归处理子节点
	# 如果是根节点，则返回处理结果（可以选择将结果转换为 JSON 格式）
	if init:
		return json.dumps(_tree) if dump2json else _tree

# for sel in pm.selected():
#     print(json.dumps(hierarchy2json(sel)))

print((hierarchy2json(pm.selected())))


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