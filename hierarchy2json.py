import pymel.core as pm
import pymel.core.nodetypes as nt
import json

def hierarchy2json(parents,dump2json=True,tree=None,init=True,):
	"""选择一个物体，获取物体之下的子物体 转为json存储

	Args:
		parents (_type_): _description_
		dump2json (bool, optional): _description_. Defaults to True.
		tree (_type_, optional): _description_. Defaults to None.
		init (bool, optional): _description_. Defaults to True.

	Returns:
		_type_: _description_
	"""
	parents = parents if isinstance(parents,list) else [parents]
	_tree = {str(p):{} if isinstance(p,nt.Transform) else p.type() for p in parents} if not isinstance(tree,dict) else tree

	for parent in parents:
		tree = _tree[str(parent)] if init else _tree
		for child in parent.getChildren():
			tree[str(child)] = {} if isinstance(child,nt.Transform) else child.type()
			hierarchy2json(child,tree=tree[str(child)],init=False)

	if init:
		return json.dumps(_tree) if dump2json else _tree

# for sel in pm.selected():
#     print(json.dumps(hierarchy2json(sel)))

print((hierarchy2json(pm.selected())))

#方法2
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