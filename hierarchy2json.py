import maya.cmds as mc      # 引入Maya命令模块，命名为mc
import pymel.core as pm     # 引入Pymel核心模块，命名为pm
import pymel.core.nodetypes as nt  # 引入Pymel节点类型模块，命名为nt
import json                 # 引入JSON模块，用于转换字典为JSON字符串


def hierarchy2json(parents, dump2json=True, tree=None, init=True):
	"""
	该函数的作用是将指定的父节点列表转换为 JSON 格式的层级结构。具体实现方法为：
	遍历每个父节点，初始化一个子字典，然后递归处理其子节点，并将子节点添加到子字典中。
	如果遍历完了所有的父节点，则返回处理结果。
	其中，如果指定了 dump2json 参数为 True,则将结果转换为 JSON 格式并返回；否则返回字典格式的结果。

	Args:
		parents (list): 要转换的节点
		dump2json (bool, optional): 是否将结果转换为 JSON 格式并返回
		tree (dict, optional): 指定的目标字典
		init (bool, optional): 是否是首次调用函数

	Returns:
			dict or json: 字典
	"""
	# 定义一个将节点层次结构转换为JSON字符串的函数，接受四个参数：要转换的节点，是否转换为JSON字符串，节点层次结构的字典，是否是首次调用函数
	if isinstance(parents, list):   # 如果parents是列表
		parents = parents          # 直接使用该列表
	else:                           # 否则
		parents = [parents]         # 将它转换为仅有一个元素的列表

	if not isinstance(tree, dict):  # 如果tree不是字典
		for p in parents:           # 遍历parents中的节点
			if isinstance(p, nt.Transform):   # 如果节点是Transform类型
				_tree = {str(p): {}}           # 创建以该节点为根节点的空字典
			else:
				_tree = {str(p): {p.type()}}   # 否则创建以该节点为根节点，节点类型为值的字典
	else:                           # 否则，即tree是字典
		_tree = tree                # 直接使用该字典

	for parent in parents:          # 遍历所有父节点
		if init:                    # 如果是首次调用该函数
			tree = _tree[str(parent)]   # 使用该节点为根节点的字典
		else:                       # 否则
			tree = _tree            # 使用输入的字典

		for child in parent.getChildren():   # 遍历该节点的所有子节点
			if isinstance(child, nt.Transform):  # 如果子节点是Transform类型
				tree[str(child)] = {}           # 将该子节点作为键，添加空字典作为值
			else:
				tree[str(child)] = child.type() # 将该子节点作为键，添加节点类型作为值

			hierarchy2json(child, tree=tree[str(child)], init=False)  # 递归遍历该子节点的所有子节点

	if init:                # 如果是首次调用该函数
		return json.dumps(_tree) if dump2json else _tree   # 返回转换为JSON字符串的字典或字典本身
	
print((hierarchy2json(pm.selected())))
'''
这是一个将Maya场景中节点层次结构转换为JSON字符串的Python脚本。它通过递归遍历层次结构并构建嵌套字典来实现这一功能。

该脚本使用Maya Python API获取节点层次结构，并使用Python内置的JSON库将其转换为JSON字符串。

hierarchy2json函数接受两个参数：parents是要从中开始层次结构的Maya节点列表，dump2json是一个布尔标志，指示输出是否应该是JSON字符串还是Python字典。

该函数首先检查parents是否为列表，如果不是，则将其转换为具有单个元素的列表。然后，它使用顶层节点作为层次结构的根节点初始化输出字典。

然后，它递归遍历层次结构，将每个节点及其子节点添加到输出字典中。如果节点是Transform节点（即组节点），它会为其子节点添加一个空字典。否则，它将该节点的类型（例如“mesh”，“camera”）作为字符串添加到字典中。

最后，如果init为True，表示这是对函数的第一次调用，则如果dump2json为True，则将输出作为JSON字符串返回，否则将其作为Python字典返回。否则，它不返回任何内容（因为输出已经添加到父字典中）。

脚本的最后一行调用hierarchy2json函数，并使用当前在Maya场景中选择的节点作为参数，并打印结果。
'''

'''
函数首先将输入物体转换为列表（如果它们还不是列表），然后创建一个名为 _tree 的空字典。
对于输入列表中的每个物体，函数在 _tree 中创建一个新键，键名为物体的名称（转换为字符串），
	键值为一个空字典（如果物体是 Transform 类型），或者是该物体的类型（如果不是 Transform 类型）。
对于每个当前物体的子物体，函数在当前物体对应的字典中创建一个新键，键名为子物体的名称（再次转换为字符串），
	键值为一个空字典（如果子物体是 Transform 类型），或者是该子物体的类型（如果不是 Transform 类型）。
	然后，函数以该子物体的对应字典作为新的 tree 参数递归调用自身。
如果 init 为 True(仅在第一次调用 hierarchy2json 时为 True),则函数返回 _tree 字典的 JSON 字符串版本或 _tree 字典本身（取决于 dump2json 的值）。
如果 init 为 False(在所有后续调用 hierarchy2json 时为 True),则函数不返回任何内容,因为层次结构信息已经被添加到前一步中的 _tree 字典中。
'''


def getRelParent(jnt_list, root):
	"""
	getRelParent 根据长名称获取骨骼列表的父子关系

	Args:
					jnt_list (	list): 蒙皮骨骼列表
					root (Joint): 根骨骼

	Returns:
					dict: 骨骼的父子关系
	"""
	jnt_parent = {}  # 创建父子关系字典
	# 遍历骨骼列表中的每个骨骼
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
a = getRelParent(jnt_list, root)


'''-----------------------------------------------------------------------方法2-------------------------------------------------------------------------'''


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
