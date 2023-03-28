import pymel.core as pm
joints = pm.ls('head', dag=True, type="joint") 
for jnt in joints:
	pm.setAttr('{}.liw'.format(jnt), 1)
	