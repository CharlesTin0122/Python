import pymel.core as pm
attr = []
attrVal = []
data = {}

def mainUI():
	template = pm.uiTemplate('cpTemplate', force=True)
	template.define(pm.button, width=200, height=30, align='right')
	template.define(pm.frameLayout, borderVisible=True, labelVisible=False)
	
	if pm.window('cpWindow', exists = 1):
		pm.deleteUI('cpWindow', window = True)
	with pm.window('cpWindow',menuBarVisible=True, title = 'CopyNPastPose'):

		with template:
			with pm.columnLayout( rowSpacing=5, adj = 1 ):
				with pm.frameLayout():
					with pm.columnLayout(adj = 1):
						pm.button(label='Copy Pose',c=copyPose)
						pm.button(label='Paste Pose',c=pastePose)
						pm.button(label='Paste Mirror Pose',c=pasteMirPose)

def copyPose(*args):

	global attr,attrVal,data
	attr = []
	attrVal = []
	data = {}
	
	selObj = pm.selected()

	attrList = [i.listAnimatable() for i in selObj]

	for i in attrList:
		for y in i:
			x = str(y)
			attr.append(x)
			
	attrVal = [pm.getAttr(s) for s in attr]

	zipList = zip(attr,attrVal)

	data = dict(zipList)

def pastePose(*args):
	for key,value in data.items():
		pm.setAttr(key,value)

def pasteMirPose(*args):
	mirList = []
	for a in attr:
		if '_L' in a:
			mir = a.replace('_L', '_R')
		elif '_R' in a:
			mir = a.replace('_R','_L')
		else:
			mir = a
		mirList.append(mir)
	
	mirZipList = zip(mirList,attrVal)
	mirData = dict(mirZipList)

	for key,value in mirData.items():
		if ('IK' in key or 'Pole' in key)and ('translateX' in key or 'rotateY' in key or 'rotateZ' in key) :
			pm.setAttr(key,value*-1)
		elif ('RootX_M' in key) and ('translateX' in key or 'rotateY' in key or 'rotateZ' in key):
			pm.setAttr(key,value*-1)
		elif ('FKRoot' in key or 'Spine' in key or 'Chest'in key or 'Neck'in key or 'Head'in key) and ('rotateX' in key or 'rotateY' in key):
			pm.setAttr(key,value*-1)
		else:
			pm.setAttr(key,value)
