import maya.OpenMaya as om

def get_selected():
	#创建物体列表
	sel = om.MSelectionList()
	#获取选择物体并传入sel列表
	om.MGlobal.getActiveSelectionList(sel)
	#遍历sel列表
	for i in range(sel.length()):
		#创建物体路径列表，MDagPath：物体的路径（物体的层级和父子关系）
		dag_path = om.MDagPath()
		#将物体传入dag_path列表
		sel.getDagPath(i,dag_path)
		#打印dag_path列表每项的长名称
		print(dag_path.fullPathName())
		
get_selected()


def selected_by_name(nameList):
	#创建物体列表
	sel = om.MSelectionList()
	#遍历提供的名称列表
	for name in nameList:
		#将名称添加到物体列表
		sel.add(name)
	#设置物体列表到选择列表
	om.MGlobal.setActiveSelectionList(sel)
	
selected_by_name(['pCube2','pSphere1'])