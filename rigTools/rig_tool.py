import pymel.core as pm

def rename_obj(name='tail{3}Grp'):
	name = name.replace('{','{i:0>')
	objList = pm.selected()
	for i,obj in enumerate(objList):
		pm.rename(obj,name.format(i=i+1))

rename_obj(name='tail{2}jnt')


def creatFKCtrl():
	obj_list = pm.selected()
	prefix = 'FK'
	ctrl = pm.group(n='{}Grp'.format(prefix),em=True)

	for i ,jnt in enumerate(obj_list):
		print(i,jnt)
		grpName = pm.createNode('transform',n='{}{i:0>2}Grp'.format(prefix,i=i+1),p=jnt)
		pm.parent(grpName,ctrl)
		ctrl = pm.circle(ch=False,nr=[1,0,0],n='{}{i:0>2}ctrl'.format(prefix,i=i+1),r=30)[0]
		pm.parent(ctrl,grpName)
		pm.setAttr(ctrl+'.t',0,0,0)
		pm.setAttr(ctrl+'.r',0,0,0)	
		pm.createNode('joint',p=ctrl,n='{}{i:0>2}Jnt'.format(prefix,i=i+1))

creatFKCtrl()

def getSkinJoint():

	for mesh in pm.ls(ni=1,v=1,type="mesh"):
		for skin in mesh.listHistory(type="skinCluster"):
			jnt = skin.listHistory(type="joint")