import pymel.core as pm
 
template = pm.uiTemplate('cpTemplate', force=True)
template.define(pm.button, width=100, height=30, align='right')
template.define(pm.frameLayout, borderVisible=True, labelVisible=False)
 
if pm.window('cpWindow', exists = 1):
	pm.deleteUI('cpWindow', window = True)
with pm.window('cpWindow',menuBar=True,menuBarVisible=True, title = 'WithWindow') as win:

	with template:
		with pm.columnLayout( rowSpacing=5, adj = 1 ):
			with pm.frameLayout():
				with pm.columnLayout(adj = 1):
					pm.button(label='Copy Pose')
					pm.button(label='Paste Pose')
					pm.button(label='Paste Mirror Pose')
					
			with pm.frameLayout():
				with pm.horizontalLayout() as h5:
					pm.button(label = 'Select Ctrl')
					pm.button(label = 'Select Mirror Ctrl')
					h5.redistribute(30, 30)
			with pm.frameLayout():
				with pm.optionMenu():
					pm.menuItem(label='Red')
					pm.menuItem(label='Green')
					pm.menuItem(label='Blue')
 
	# add a menu to an existing window
with win:
	with pm.menu(label = 'File'):
		pm.menuItem(label='One')
		pm.menuItem(label='Two')
		with pm.subMenuItem(label='Sub'):
			pm.menuItem(label='A')
			pm.menuItem(label='B')
		pm.menuItem(label='Three')