#coding:UTF-8
#***********************************************//
#                                               //
#               RePARENT PRO 1.5.1              //
#      copyright Dmitrii Kolpakov 2020          //
#                                               //
#***********************************************//

import pymel.core as pm

pm.progressWindow(endProgress=1)
pm.optionVar(intValue=('animBlendingOpt', 1))
if pm.window('ReParentPanel', ex=1):
	pm.deleteUI('ReParentPanel')
	
window=str(pm.window('ReParentPanel', s=0, toolbox=1, menuBar=1, t="ReParent v1.5.1 Pro", wh=(142, 159)))
pm.menu('aboutMenu', to=0, l="Advanced")
pm.menuItem('onLayerMode', cb=0, ann="Each new overlapping animation will be baked on new animation layer", l="Bake on anim layer")
pm.menuItem('DelRed', cb=1, ann="Delete all redundant keys on rePaent locators", l="Delete redundant")
pm.menuItem(c=lambda *args: pm.mel.BakeAndDelete_reParent(), ann="Bake All animation and delete rePaent locators", l="BAKE AND DELETE")
pm.menu('helpMenu', to=0, l="Help")
pm.menuItem(c=lambda *args: pm.mel.reParentIntro(), l="Intro")
pm.menuItem(c=lambda *args: pm.mel.reParentTutorial(), l="Tutorial")
pm.rowColumnLayout()
pm.rowLayout(nc=2, cw=(30, 30))
pm.rowColumnLayout(nc=1)
pm.checkBox('PinCheckBox', h=18, ann="Pin selected controls (delete all animation and constrain to locator)", v=0, label=" Pin ")
pm.rowColumnLayout(columnWidth=[(1, 70), (2, 50)], nc=2)
pm.checkBox('IKCheckBox', h=18, ann="rePArent three FK controls to IK mode", v=0, label=" IK mode ")
pm.checkBox('IKCheckLocalBox', h=18, ann="rePArent three FK controls to IK mode with parent to the first control", v=0, label=" Local ")
pm.setParent('..')
pm.rowLayout(nc=1, cw=(30, 30))
pm.rowColumnLayout(columnWidth=(1, 130), nc=1)
pm.checkBox('ManualCheckBox', h=18, ann="Move reParent locator to set required pivot and press Go", v=0, label=" Manual pivot ")
pm.checkBox('FreezeCheckBox', h=18, ann="Freeze all contols regarding the first selected control", v=0, label=" Freeze main ")
pm.checkBox('RelativeCheckBox', h=18, ann="Select controls for reParent then last control for relative", v=0, label=" All to the last ")
pm.button('reParentButton', h=40, c=lambda *args: pm.mel.reParentStarter(), bgc=(.8, .8, .8), l="reParent", w=120)
pm.rowColumnLayout(columnWidth=[(1, 70), (2, 50)], nc=2, rs=(1, 100))
pm.button(h=40, c=lambda *args: pm.mel.manualModeGo(), bgc=(.8, .8, .8), l="Go", w=40)
pm.button(h=40, c=lambda *args: pm.mel.manualModeCancel(), bgc=(.22, .22, .22), l="Cancel", w=60)
pm.setParent('..')
pm.window('ReParentPanel', edit=1, widthHeight=(142, 159))
pm.showWindow('ReParentPanel')

def _reParentIntro():
	
	pm.launch(web="https://www.youtube.com/watch?v=7jqzIceFKbo")
	


def _BakeAndDelete_reParent():
	
	currentR=int(pm.playbackOptions(q=1, min=1))
	currentL=int(pm.playbackOptions(q=1, max=1))
	pm.select('All_Sessions_reParentControls_set', r=1)
	pm.bakeResults(sparseAnimCurveBake=0, 
		minimizeRotation=1, 
		removeBakedAttributeFromLayer=0, 
		removeBakedAnimFromLayer=0, 
		bakeOnOverrideLayer=0, 
		preserveOutsideKeys=1, 
		simulation=1, 
		sampleBy=1, 
		shape=0, 
		t=(str(currentL) + ":" + str(currentR)), 
		at=["tx", 
			"ty", 
			"tz", 
			"rx", 
			"ry", "rz"], 
		disableImplicitControl=1, 
		controlPoints=0)
	if pm.objExists("All_Session_reParentLocator_set"):
		pm.select('All_Session_reParentLocator_set', r=1)
		pm.delete()
		
	if pm.objExists("reParent_sets"):
		pm.delete('reParent_sets')
		
	if pm.objExists("All_Sessions_reParentControls_set"):
		pm.delete('All_Sessions_reParentControls_set')
		
	if pm.objExists("Last_Session_reParentControls_set"):
		pm.delete('Last_Session_reParentControls_set')
		
	if pm.objExists("*_reParentIK_grp"):
		pm.delete("*_reParentIK_grp")
		
	if pm.objExists("*:*_reParentIK_grp"):
		pm.delete("*:*_reParentIK_grp")
		
	if pm.objExists("*_ReParent_grp"):
		pm.delete("*_ReParent_grp")
		
	if pm.objExists("*:*_ReParent_grp"):
		pm.delete("*:*_ReParent_grp")
		
	


def _reParentTutorial():
	
	pm.launch(web="https://www.youtube.com/watch?v=7jqzIceFKbo")
	


def reParentStarter():
	
	FreezeButton=int(pm.checkBox('FreezeCheckBox', q=1, v=1))
	RelativeButton=int(pm.checkBox('RelativeCheckBox', q=1, v=1))
	IKButton=int(pm.checkBox('IKCheckBox', q=1, v=1))
	PinButton=int(pm.checkBox('PinCheckBox', q=1, v=1))
	ManualButton=int(pm.checkBox('ManualCheckBox', q=1, v=1))
	SelectedControls=pm.ls(sl=1)
	if not len(SelectedControls):
		pm.confirmDialog(b="Ok", m="SELECT ANY CONTROL", t="Oooops..")
		
	
	elif FreezeButton + RelativeButton + IKButton + PinButton + ManualButton>1:
		pm.confirmDialog(b="Ok", m="Select one of mode", t="Oooops..")
		
	
	elif IKButton == 1:
		SelectedControls=pm.ls(sl=1)
		if len(SelectedControls) != 3:
			pm.confirmDialog(b="Ok", m="IK mode works only for three controls", t="Oooops..")
			
		
		else:
			pm.mel.IKmode()
			
		
	if FreezeButton == 1:
		pm.mel.reParentStayHere()
		
	if FreezeButton == 0 and RelativeButton == 0 and IKButton == 0 and ManualButton == 0:
		pm.mel.reParent()
		
	if FreezeButton == 0 and RelativeButton == 1 and IKButton == 0 and ManualButton == 0:
		pm.mel.reParentRelativeStart()
		
	if FreezeButton == 0 and RelativeButton == 0 and IKButton == 0 and ManualButton == 1:
		pm.mel.reParentManualStarter()
		
	


def reParent():
	"""/////////////////////////////////////
	              reParent             //
	/////////////////////////////////////"""
	

	PinButton=int(pm.checkBox('PinCheckBox', q=1, v=1))
	DelRedMode=int(pm.menuItem('DelRed', query=1, cb=1))
	SelCtrl = ""
	SelectedControls=pm.ls(sl=1)
	currentR=int(pm.playbackOptions(q=1, min=1))
	currentL=int(pm.playbackOptions(q=1, max=1))
	if pm.objExists("TempLocator"):
		pm.delete('TempLocator')
		
	if not pm.objExists("reParent_sets"):
		createSetResult=pm.sets(em=1, name="reParent_sets")
		#Create Sets
		
	if pm.objExists("All_Sessions_reParentControls_set"):
		pm.sets(SelectedControls, edit=1, forceElement='All_Sessions_reParentControls_set')
		pm.sets('All_Sessions_reParentControls_set', edit=1, fe='reParent_sets')
		
	
	else:
		createSetResult=pm.sets(name="All_Sessions_reParentControls_set")
		pm.sets('All_Sessions_reParentControls_set', edit=1, fe='reParent_sets')
		
	if pm.objExists("Last_Session_reParentControls_set"):
		pm.delete('Last_Session_reParentControls_set')
		createSetResult=pm.sets(name="Last_Session_reParentControls_set")
		pm.sets(SelectedControls, edit=1, forceElement='Last_Session_reParentControls_set')
		pm.sets('Last_Session_reParentControls_set', edit=1, fe='reParent_sets')
		
	
	else:
		createSetResult=pm.sets(name="Last_Session_reParentControls_set")
		pm.sets('Last_Session_reParentControls_set', edit=1, fe='reParent_sets')
		
	pm.select(cl=1)
	if pm.objExists("Last_Session_reParentLocator_set"):
		pm.delete('Last_Session_reParentLocator_set')
		createSetResult=pm.sets(name="Last_Session_reParentLocator_set")
		pm.sets('Last_Session_reParentLocator_set', edit=1, fe='reParent_sets')
		
	
	else:
		createSetResult=pm.sets(name="Last_Session_reParentLocator_set")
		pm.sets('Last_Session_reParentLocator_set', edit=1, fe='reParent_sets')
		
	if not pm.objExists("All_Session_reParentLocator_set"):
		createSetResult=pm.sets(em=1, name="All_Session_reParentLocator_set")
		pm.sets('All_Session_reParentLocator_set', edit=1, fe='reParent_sets')
		
	for SelCtrl in SelectedControls:
		pm.select(SelCtrl, r=1)
		SelectedControls=pm.ls(sl=1)
		pm.spaceLocator(n='TempLocator')
		pm.setAttr("TempLocator.rotateOrder", 2)
		pm.matchTransform('TempLocator', SelectedControls[0], rot=1, pos=1)
		pm.select(SelCtrl, r=1)
		pm.mel.reParentLocatorSize()
		# create Last_Session_reParentLocator_set
		pm.sets('TempLocator', edit=1, forceElement='Last_Session_reParentLocator_set')
		pm.sets('TempLocator', edit=1, forceElement='All_Session_reParentLocator_set')
		pm.select(SelCtrl, 'TempLocator', r=1)
		print (PinButton)
		if PinButton == 0:
			pm.select(SelCtrl, 'TempLocator', r=1)
			pm.orientConstraint(mo=1, weight=1, n='TempOrientConst')
			pm.pointConstraint(mo=1, weight=1, n='TempPointConst')
			
		pm.select('TempLocator')
		pm.rename('TempLocator', (str(SelCtrl) + "_ReParent_Locator"))
		pm.select(cl=1)
		
	pm.select('Last_Session_reParentLocator_set', r=1)
	if PinButton == 0:
		pm.bakeResults(sparseAnimCurveBake=0, 
			minimizeRotation=1, 
			removeBakedAttributeFromLayer=0, 
			removeBakedAnimFromLayer=0, 
			bakeOnOverrideLayer=0, 
			preserveOutsideKeys=1, 
			simulation=1, 
			sampleBy=1, 
			shape=0, 
			t=(str(currentL) + ":" + str(currentR)), 
			at=["tx", 
				"ty", 
				"tz", 
				"rx", 
				"ry", "rz"], 
			disableImplicitControl=1, 
			controlPoints=0)
		
	pm.delete("TempOrientConst*", "TempPointConst*")
	if pm.objExists("TempLocator"):
		pm.delete("TempOrientConst*", "TempPointConst*")
		
	for SelCtrl in SelectedControls:
		if pm.getAttr((str(SelCtrl) + ".tx"), 
			keyable=1) == 1 and pm.getAttr((str(SelCtrl) + ".tx"), 
			lock=1) == 0:
			pm.select((str(SelCtrl) + "_ReParent_Locator"), 
				SelCtrl)
			pm.pointConstraint(weight=1, n=(str(SelCtrl) + "ReParent"))
			
		if pm.getAttr((str(SelCtrl) + ".rx"), 
			keyable=1) == 1 and pm.getAttr((str(SelCtrl) + ".rx"), 
			lock=1) == 0:
			pm.select((str(SelCtrl) + "_ReParent_Locator"), 
				SelCtrl)
			pm.orientConstraint(weight=1, n=(str(SelCtrl) + "ReParent"))
			
		pm.cutKey(SelCtrl, at=["tx", "ty", "tz", "rx", "ry", "rz"], f=":", t=":", cl=1)
		
	if DelRedMode == 1:
		pm.select('Last_Session_reParentLocator_set', r=1)
		# simplifier///
		SelectedControls=pm.ls(sl=1)
		pm.selectKey(k=1, r=1)
		selectedCurves=pm.keyframe(q=1, selected=1, name=1)
		#delete redundant
		for currentAnimCurve in selectedCurves:
			allKeys=pm.keyframe(currentAnimCurve, q=1, timeChange=1)
			valArray=pm.keyframe(currentAnimCurve, q=1, valueChange=1)
			keysSize=len(allKeys)
			for s in range(1,keysSize - 1):
				if valArray[s] == valArray[s - 1] and valArray[s] == valArray[s + 1]:
					pm.cutKey(currentAnimCurve, clear=1, time=allKeys[s])
					
				
			
		
	ClearElemwnts = 0
	# euler all anim curves	
	pm.melGlobals.initVar('string[]', 'eulerFilterCurves')
	ClearElemwnts=len(pm.melGlobals['eulerFilterCurves'])
	for s in range(0,ClearElemwnts):
		pm.melGlobals['eulerFilterCurves'].pop(0)
		
	pm.select('Last_Session_reParentLocator_set', r=1)
	EulerArrays=pm.ls(sl=1)
	for obj in EulerArrays:
		listAnimAttrs=pm.listAttr(obj, k=1)
		for attr in listAnimAttrs:
			animCurve=pm.listConnections((str(obj) + "." + str(attr)), 
				type="animCurve")
			ClearElemwnts=len(animCurve)
			pm.melGlobals['eulerFilterCurves'] += animCurve[:ClearElemwnts]
			
		
	pm.filterCurve(pm.melGlobals['eulerFilterCurves'])
	pm.select(SelectedControls, r=1)
	


def reParentManualStarter():
	"""/////////////////////////////////////
	            Manual MODE            //
	/////////////////////////////////////"""
	

	pm.window('ReParentPanel', edit=1, widthHeight=(142, 203))
	pm.button('reParentButton', edit=1, en=0)
	PinButton=int(pm.checkBox('PinCheckBox', q=1, v=1))
	SelCtrl = ""
	SelectedControls=pm.ls(sl=1)
	if pm.objExists("TempLocator"):
		pm.delete('TempLocator')
		
	if not pm.objExists("reParent_sets"):
		createSetResult=pm.sets(em=1, name="reParent_sets")
		#Create Sets
		
	if pm.objExists("All_Sessions_reParentControls_set"):
		pm.sets(SelectedControls, edit=1, forceElement='All_Sessions_reParentControls_set')
		pm.sets('All_Sessions_reParentControls_set', edit=1, fe='reParent_sets')
		
	
	else:
		createSetResult=pm.sets(name="All_Sessions_reParentControls_set")
		pm.sets('All_Sessions_reParentControls_set', edit=1, fe='reParent_sets')
		
	if pm.objExists("Last_Session_reParentControls_set"):
		pm.delete('Last_Session_reParentControls_set')
		createSetResult=pm.sets(name="Last_Session_reParentControls_set")
		pm.sets(SelectedControls, edit=1, forceElement='Last_Session_reParentControls_set')
		pm.sets('Last_Session_reParentControls_set', edit=1, fe='reParent_sets')
		
	
	else:
		createSetResult=pm.sets(name="Last_Session_reParentControls_set")
		pm.sets('Last_Session_reParentControls_set', edit=1, fe='reParent_sets')
		
	pm.select(cl=1)
	if pm.objExists("Last_Session_reParentLocator_set"):
		pm.delete('Last_Session_reParentLocator_set')
		createSetResult=pm.sets(name="Last_Session_reParentLocator_set")
		pm.sets('Last_Session_reParentLocator_set', edit=1, fe='reParent_sets')
		
	
	else:
		createSetResult=pm.sets(name="Last_Session_reParentLocator_set")
		pm.sets('Last_Session_reParentLocator_set', edit=1, fe='reParent_sets')
		
	if not pm.objExists("All_Session_reParentLocator_set"):
		createSetResult=pm.sets(em=1, name="All_Session_reParentLocator_set")
		pm.sets('All_Session_reParentLocator_set', edit=1, fe='reParent_sets')
		
	for SelCtrl in SelectedControls:
		pm.select(SelCtrl, r=1)
		SelectedControls=pm.ls(sl=1)
		pm.spaceLocator(n='TempLocator')
		pm.setAttr("TempLocator.rotateOrder", 2)
		pm.matchTransform('TempLocator', SelectedControls[0])
		pm.select(SelCtrl, r=1)
		pm.mel.reParentLocatorSize()
		pm.sets('TempLocator', edit=1, forceElement='Last_Session_reParentLocator_set')
		pm.sets('TempLocator', edit=1, forceElement='All_Session_reParentLocator_set')
		pm.select(SelCtrl, 'TempLocator', r=1)
		temps=pm.pointConstraint(weight=1, offset=(0, 0, 0))
		pm.delete(temps)
		temps=pm.orientConstraint(weight=1, offset=(0, 0, 0))
		pm.delete(temps)
		pm.select('TempLocator')
		pm.rename('TempLocator', (str(SelCtrl) + "_ReParent_Locator"))
		
	


def manualModeCancel():
	
	if (pm.window('ManualWindow', ex=1)) == True:
		pm.deleteUI('ManualWindow')
		
	pm.window('ReParentPanel', edit=1, widthHeight=(142, 159))
	pm.button('reParentButton', edit=1, en=1)
	pm.select('Last_Session_reParentLocator_set', r=1)
	pm.delete()
	


def manualModeGo():
	
	if (pm.window('ManualWindow', ex=1)) == True:
		pm.deleteUI('ManualWindow')
		
	PinButton=int(pm.checkBox('PinCheckBox', q=1, v=1))
	DelRedMode=int(pm.menuItem('DelRed', query=1, cb=1))
	pm.select('Last_Session_reParentControls_set', r=1)
	SelectedControls=pm.ls(sl=1)
	currentR=int(pm.playbackOptions(q=1, min=1))
	currentL=int(pm.playbackOptions(q=1, max=1))
	for SelCtrl in SelectedControls:
		if PinButton == 0:
			pm.select(SelCtrl, 
				(str(SelCtrl) + "_ReParent_Locator"), 
				r=1)
			pm.parentConstraint(mo=1, weight=1, n='TempParentConst')
			
		
	pm.select('Last_Session_reParentLocator_set', r=1)
	if PinButton == 0:
		pm.bakeResults(sparseAnimCurveBake=0, 
			minimizeRotation=1, 
			removeBakedAttributeFromLayer=0, 
			removeBakedAnimFromLayer=0, 
			bakeOnOverrideLayer=0, 
			preserveOutsideKeys=1, 
			simulation=1, 
			sampleBy=1, 
			shape=0, 
			t=(str(currentL) + ":" + str(currentR)), 
			at=["tx", 
				"ty", 
				"tz", 
				"rx", 
				"ry", "rz"], 
			disableImplicitControl=1, 
			controlPoints=0)
		
	pm.delete("TempParentConst*")
	if pm.objExists("TempLocator"):
		pm.delete("TempOrientConst*", "TempPointConst*")
		
	for SelCtrl in SelectedControls:
		if pm.getAttr((str(SelCtrl) + ".tx"), 
			keyable=1) == 1 and pm.getAttr((str(SelCtrl) + ".tx"), 
			lock=1) == 0 and pm.getAttr((str(SelCtrl) + ".rx"), 
			keyable=1) == 1 and pm.getAttr((str(SelCtrl) + ".rx"), 
			lock=1) == 0:
			pm.select((str(SelCtrl) + "_ReParent_Locator"), 
				SelCtrl)
			pm.parentConstraint(mo=1, weight=1, n=(str(SelCtrl) + "ReParent"))
			
		
		else:
			if pm.getAttr((str(SelCtrl) + ".tx"), 
				keyable=1) == 1 and pm.getAttr((str(SelCtrl) + ".tx"), 
				lock=1) == 0:
				pm.select((str(SelCtrl) + "_ReParent_Locator"), 
					SelCtrl)
				pm.pointConstraint(mo=1, weight=1, n=(str(SelCtrl) + "ReParent"))
				
			if pm.getAttr((str(SelCtrl) + ".rx"), 
				keyable=1) == 1 and pm.getAttr((str(SelCtrl) + ".rx"), 
				lock=1) == 0:
				pm.select((str(SelCtrl) + "_ReParent_Locator"), 
					SelCtrl)
				pm.orientConstraint(mo=1, weight=1, n=(str(SelCtrl) + "ReParent"))
				
			
		pm.cutKey(SelCtrl, at=["tx", "ty", "tz", "rx", "ry", "rz"], f=":", t=":", cl=1)
		
	if DelRedMode == 1:
		pm.select('Last_Session_reParentLocator_set', r=1)
		# simplifier///
		SelectedControls=pm.ls(sl=1)
		pm.selectKey(k=1, r=1)
		selectedCurves=pm.keyframe(q=1, selected=1, name=1)
		#delete redundant
		for currentAnimCurve in selectedCurves:
			allKeys=pm.keyframe(currentAnimCurve, q=1, timeChange=1)
			valArray=pm.keyframe(currentAnimCurve, q=1, valueChange=1)
			keysSize=len(allKeys)
			for s in range(1,keysSize - 1):
				if valArray[s] == valArray[s - 1] and valArray[s] == valArray[s + 1]:
					pm.cutKey(currentAnimCurve, clear=1, time=allKeys[s])
					
				
			
		
	ClearElemwnts = 0
	# euler all anim curves	
	pm.melGlobals.initVar('string[]', "pm.melGlobals['eulerFilterCurves'")
	ClearElemwnts=len(pm.melGlobals['eulerFilterCurves'])
	for s in range(0,ClearElemwnts):
		pm.melGlobals['eulerFilterCurves'].pop(0)
		
	pm.select('Last_Session_reParentLocator_set', r=1)
	EulerArrays=pm.ls(sl=1)
	for obj in EulerArrays:
		listAnimAttrs=pm.listAttr(obj, k=1)
		for attr in listAnimAttrs:
			animCurve=pm.listConnections((str(obj) + "." + str(attr)), 
				type="animCurve")
			ClearElemwnts=len(animCurve)
			pm.melGlobals['eulerFilterCurves'] += animCurve[:ClearElemwnts]
			
		
	pm.filterCurve(pm.melGlobals['eulerFilterCurves'])
	pm.select(SelectedControls, r=1)
	pm.window('ReParentPanel', edit=1, widthHeight=(142, 159))
	pm.button('reParentButton', edit=1, en=1)
	


def reParentRelativeStart():
	"""/////////////////////////////////////
	         reParentRelative          //
	/////////////////////////////////////"""
	

	SelectedControls=pm.ls(sl=1)
	amountCheck=len(SelectedControls)
	if amountCheck>1:
		pm.mel.reParentRelative()
		
	
	else:
		pm.confirmDialog(b="Ok", m=" FOR RELATIVE MODE YOU NEED TO SELECT 2 AND MORE CONTROLS \n             First for reparent and second relative", t="Oooops..")
		
	


def reParentRelative():
	
	PinButton=int(pm.checkBox('PinCheckBox', q=1, v=1))
	DelRedMode=int(pm.menuItem('DelRed', query=1, cb=1))
	SelectedControls=pm.ls(sl=1)
	amountCheck=len(SelectedControls)
	currentR=int(pm.playbackOptions(q=1, min=1))
	currentL=int(pm.playbackOptions(q=1, max=1))
	if pm.objExists("TempLocator"):
		pm.delete('TempLocator')
		
	if not pm.objExists("reParent_sets"):
		createSetResult=pm.sets(em=1, name="reParent_sets")
		#Create Sets
		
	if pm.objExists("All_Sessions_reParentControls_set"):
		pm.sets(SelectedControls, edit=1, forceElement='All_Sessions_reParentControls_set')
		pm.sets('All_Sessions_reParentControls_set', edit=1, fe='reParent_sets')
		
	
	else:
		createSetResult=pm.sets(name="All_Sessions_reParentControls_set")
		pm.sets('All_Sessions_reParentControls_set', edit=1, fe='reParent_sets')
		
	if pm.objExists("Last_Session_reParentControls_set"):
		pm.delete('Last_Session_reParentControls_set')
		createSetResult=pm.sets(name="Last_Session_reParentControls_set")
		pm.sets(SelectedControls, edit=1, forceElement='Last_Session_reParentControls_set')
		pm.sets('Last_Session_reParentControls_set', edit=1, fe='reParent_sets')
		
	
	else:
		createSetResult=pm.sets(name="Last_Session_reParentControls_set")
		pm.sets('Last_Session_reParentControls_set', edit=1, fe='reParent_sets')
		
	pm.select(cl=1)
	if pm.objExists("Last_Session_reParentLocator_set"):
		pm.delete('Last_Session_reParentLocator_set')
		createSetResult=pm.sets(name="Last_Session_reParentLocator_set")
		pm.sets('Last_Session_reParentLocator_set', edit=1, fe='reParent_sets')
		
	
	else:
		createSetResult=pm.sets(name="Last_Session_reParentLocator_set")
		pm.sets('Last_Session_reParentLocator_set', edit=1, fe='reParent_sets')
		
	if not pm.objExists("All_Session_reParentLocator_set"):
		createSetResult=pm.sets(em=1, name="All_Session_reParentLocator_set")
		pm.sets('All_Session_reParentLocator_set', edit=1, fe='reParent_sets')
		
	amountOfAllCtrls=len(SelectedControls)
	for r in range(0,amountOfAllCtrls - 1):
		pm.select(SelectedControls[r], r=1)
		pm.spaceLocator(n='TempLocator')
		pm.setAttr("TempLocator.rotateOrder", 2)
		pm.matchTransform('TempLocator', SelectedControls[r])
		pm.select(SelectedControls[r], r=1)
		pm.mel.reParentLocatorSize()
		pm.sets('TempLocator', edit=1, forceElement='Last_Session_reParentLocator_set')
		pm.sets('TempLocator', edit=1, forceElement='All_Session_reParentLocator_set')
		pm.group('TempLocator', name=(SelectedControls[r] + "_ReParent_grp"))
		pm.parentConstraint(SelectedControls[amountOfAllCtrls - 1], 
			(SelectedControls[r] + "_ReParent_grp"), 
			mo=1, w=1, n=(SelectedControls[r] + "_ReParent_Const"))
		pm.select(SelectedControls[r], 'TempLocator', r=1)
		pm.orientConstraint(mo=1, weight=1, n=(SelectedControls[r] + "TempOrientConst"))
		pm.pointConstraint(mo=1, weight=1, n=(SelectedControls[r] + "TempPointConst"))
		pm.rename('TempLocator', (SelectedControls[r] + "_ReParent_Locator"))
		
	pm.select('Last_Session_reParentLocator_set', r=1)
	pm.bakeResults(sparseAnimCurveBake=0, 
		minimizeRotation=1, 
		removeBakedAttributeFromLayer=0, 
		removeBakedAnimFromLayer=0, 
		bakeOnOverrideLayer=0, 
		preserveOutsideKeys=1, 
		simulation=1, 
		sampleBy=1, 
		shape=0, 
		t=(str(currentL) + ":" + str(currentR)), 
		at=["tx", 
			"ty", 
			"tz", 
			"rx", 
			"ry", "rz"], 
		disableImplicitControl=1, 
		controlPoints=0)
	for r in range(0,amountOfAllCtrls - 1):
		if pm.getAttr((SelectedControls[r] + ".tx"), 
			keyable=1) == 1 and pm.getAttr((SelectedControls[r] + ".tx"), 
			lock=1) == 0:
			pm.select((SelectedControls[r] + "_ReParent_Locator"), 
				SelectedControls[r])
			pm.pointConstraint(weight=1, n=(SelectedControls[r] + "ReParent"))
			
		if pm.getAttr((SelectedControls[r] + ".rx"), 
			keyable=1) == 1 and pm.getAttr((SelectedControls[r] + ".rx"), 
			lock=1) == 0:
			pm.select((SelectedControls[r] + "_ReParent_Locator"), 
				SelectedControls[r])
			pm.orientConstraint(weight=1, n=(SelectedControls[r] + "ReParent"))
			
		pm.cutKey(SelectedControls[r], at=["tx", "ty", "tz", "rx", "ry", "rz"], f=":", t=":", cl=1)
		pm.delete((SelectedControls[r] + "TempOrientConst"), (SelectedControls[r] + "TempPointConst"))
		
	if DelRedMode == 1:
		pm.select('Last_Session_reParentLocator_set', r=1)
		# simplifier///
		SelectedControls=pm.ls(sl=1)
		pm.selectKey(k=1, r=1)
		selectedCurves=pm.keyframe(q=1, selected=1, name=1)
		#delete redundant
		for currentAnimCurve in selectedCurves:
			allKeys=pm.keyframe(currentAnimCurve, q=1, timeChange=1)
			valArray=pm.keyframe(currentAnimCurve, q=1, valueChange=1)
			keysSize=len(allKeys)
			for s in range(1,keysSize - 1):
				if valArray[s] == valArray[s - 1] and valArray[s] == valArray[s + 1]:
					pm.cutKey(currentAnimCurve, clear=1, time=allKeys[s])
					
				
			
		
	ClearElemwnts = 0
	# euler all anim curves	
	pm.melGlobals.initVar('string[]', "pm.melGlobals['eulerFilterCurves'")
	ClearElemwnts=len(pm.melGlobals['eulerFilterCurves'])
	for s in range(0,ClearElemwnts):
		pm.melGlobals['eulerFilterCurves'].pop(0)
		
	pm.select('Last_Session_reParentLocator_set', r=1)
	EulerArrays=pm.ls(sl=1)
	for obj in EulerArrays:
		listAnimAttrs=pm.listAttr(obj, k=1)
		for attr in listAnimAttrs:
			animCurve=pm.listConnections((str(obj) + "." + str(attr)), 
				type="animCurve")
			ClearElemwnts=len(animCurve)
			pm.melGlobals['eulerFilterCurves'] += animCurve[:ClearElemwnts]
			
		
	pm.filterCurve(pm.melGlobals['eulerFilterCurves'])
	pm.select(SelectedControls, r=1)
	


def reParentStayHere():
	"""/////////////////////////////////////
	             freezeMain            //
	/////////////////////////////////////"""
	

	amount=0
	#progressBar
	pm.progressWindow(status="Progress: 0%", 
		progress=amount, 
		isInterruptable=True, 
		title="progress...")
	SelCtrl = ""
	SelectedControls=pm.ls(sl=1)
	currentR=int(pm.playbackOptions(q=1, min=1))
	currentL=int(pm.playbackOptions(q=1, max=1))
	#Create Sets
	if not pm.objExists("reParent_sets"):
		createSetResult=pm.sets(em=1, name="reParent_sets")
		
	if pm.objExists("TempLocator"):
		pm.delete('TempLocator')
		
	if pm.objExists("Last_Session_reParentControls_set"):
		pm.delete('Last_Session_reParentControls_set')
		createSetResult=pm.sets(name="Last_Session_reParentControls_set")
		pm.sets(SelectedControls, edit=1, forceElement='Last_Session_reParentControls_set')
		pm.sets('Last_Session_reParentControls_set', edit=1, fe='reParent_sets')
		
	
	else:
		createSetResult=pm.sets(name="Last_Session_reParentControls_set")
		pm.sets('Last_Session_reParentControls_set', edit=1, fe='reParent_sets')
		
	pm.select(cl=1)
	if pm.objExists("Last_Session_reParentLocator_set"):
		pm.delete('Last_Session_reParentLocator_set')
		createSetResult=pm.sets(name="Last_Session_reParentLocator_set")
		
	
	else:
		createSetResult=pm.sets(name="Last_Session_reParentLocator_set")
		
	amount+=20
	#progressBar	
	pm.progressWindow(edit=1, progress=amount, 
		status=("Progress: " + str(amount) + "%"))
	for SelCtrl in SelectedControls:
		pm.select(SelCtrl, r=1)
		SelectedControls=pm.ls(sl=1)
		pm.spaceLocator(n='TempLocator')
		pm.setAttr("TempLocator.rotateOrder", 2)
		pm.matchTransform('TempLocator', SelectedControls[0], rot=1, pos=1)
		pm.select(SelCtrl, r=1)
		pm.mel.reParentLocatorSize()
		pm.sets('TempLocator', edit=1, forceElement='Last_Session_reParentLocator_set')
		pm.select(SelCtrl, 'TempLocator', r=1)
		pm.select(SelCtrl, 'TempLocator', r=1)
		pm.orientConstraint(mo=1, weight=1, n='TempOrientConst')
		pm.pointConstraint(mo=1, weight=1, n='TempPointConst')
		pm.select('TempLocator')
		pm.rename('TempLocator', (str(SelCtrl) + "_ReParent_Locator"))
		pm.select(cl=1)
		
	amount+=20
	#progressBar	
	pm.progressWindow(edit=1, progress=amount, 
		status=("Progress: " + str(amount) + "%"))
	pm.select('Last_Session_reParentLocator_set', r=1)
	pm.bakeResults(sparseAnimCurveBake=0, 
		minimizeRotation=1, 
		removeBakedAttributeFromLayer=0, 
		removeBakedAnimFromLayer=0, 
		bakeOnOverrideLayer=0, 
		preserveOutsideKeys=1, 
		simulation=1, 
		sampleBy=1, 
		shape=0, 
		t=(str(currentL) + ":" + str(currentR)), 
		at=["tx", 
			"ty", 
			"tz", 
			"rx", 
			"ry", "rz"], 
		disableImplicitControl=1, 
		controlPoints=0)
	#progressBar	
	amount+=20
	pm.progressWindow(edit=1, progress=amount, 
		status=("Progress: " + str(amount) + "%"))
	pm.delete((SelectedControls[0]), 
		constraints=1)
	for SelCtrl in SelectedControls:
		if pm.getAttr((str(SelCtrl) + ".tx"), 
			keyable=1) == 1 and pm.getAttr((str(SelCtrl) + ".tx"), 
			lock=1) == 0:
			pm.select((str(SelCtrl) + "_ReParent_Locator"), 
				SelCtrl)
			pm.pointConstraint(weight=1, n=(str(SelCtrl) + "ReParent"))
			
		if pm.getAttr((str(SelCtrl) + ".rx"), 
			keyable=1) == 1 and pm.getAttr((str(SelCtrl) + ".rx"), 
			lock=1) == 0:
			pm.select((str(SelCtrl) + "_ReParent_Locator"), 
				SelCtrl)
			pm.orientConstraint(weight=1, n=(str(SelCtrl) + "ReParent"))
			
		
	pm.select(SelectedControls[0], r=1)
	pm.cutKey((SelectedControls[0]), 
		at=["tx", "ty", "tz", "rx", "ry", "rz"], f=":", t=":", cl=1)
	pm.delete((SelectedControls[0]), 
		constraints=1)
	#progressBar	
	amount+=20
	pm.progressWindow(edit=1, progress=amount, 
		status=("Progress: " + str(amount) + "%"))
	pm.select('Last_Session_reParentControls_set', r=1)
	pm.select(SelectedControls[0], d=1)
	pm.bakeResults(sparseAnimCurveBake=0, 
		minimizeRotation=1, 
		removeBakedAttributeFromLayer=0, 
		removeBakedAnimFromLayer=0, 
		bakeOnOverrideLayer=0, 
		preserveOutsideKeys=1, 
		simulation=0, 
		sampleBy=1, 
		shape=0, 
		t=(str(currentL) + ":" + str(currentR)), 
		at=["tx", 
			"ty", 
			"tz", 
			"rx", 
			"ry", "rz"], 
		disableImplicitControl=1, 
		controlPoints=0)
	#progressBar	
	amount+=20
	pm.progressWindow(edit=1, progress=amount, 
		status=("Progress: " + str(amount) + "%"))
	pm.select('Last_Session_reParentLocator_set', r=1)
	pm.delete()
	pm.select(SelectedControls, r=1)
	pm.progressWindow(endProgress=1)
	


def IKmode():
	"""/////////////////////////////////////
	              IK mode              //
	/////////////////////////////////////"""
	

	SelectedControls=pm.ls(sl=1)
	pm.melGlobals.initVar('string[]', 'UpHierarchyObject')
	#Create Sets
	if not pm.objExists("reParent_sets"):
		createSetResult=pm.sets(em=1, name="reParent_sets")
		
	if pm.objExists("All_Sessions_reParentControls_set"):
		pm.sets(SelectedControls, edit=1, forceElement='All_Sessions_reParentControls_set')
		pm.sets('All_Sessions_reParentControls_set', edit=1, fe='reParent_sets')
		
	
	else:
		createSetResult=pm.sets(name="All_Sessions_reParentControls_set")
		pm.sets('All_Sessions_reParentControls_set', edit=1, fe='reParent_sets')
		
	if pm.objExists("Last_Session_reParentControls_set"):
		pm.delete('Last_Session_reParentControls_set')
		createSetResult=pm.sets(name="Last_Session_reParentControls_set")
		pm.sets(SelectedControls, edit=1, forceElement='Last_Session_reParentControls_set')
		pm.sets('Last_Session_reParentControls_set', edit=1, fe='reParent_sets')
		
	
	else:
		createSetResult=pm.sets(name="Last_Session_reParentControls_set")
		pm.sets('Last_Session_reParentControls_set', edit=1, fe='reParent_sets')
		
	pm.select(cl=1)
	if pm.objExists("Last_Session_reParentLocator_set"):
		pm.delete('Last_Session_reParentLocator_set')
		createSetResult=pm.sets(name="Last_Session_reParentLocator_set")
		pm.sets('Last_Session_reParentLocator_set', edit=1, fe='reParent_sets')
		
	
	else:
		createSetResult=pm.sets(name="Last_Session_reParentLocator_set")
		pm.sets('Last_Session_reParentLocator_set', edit=1, fe='reParent_sets')
		
	if not pm.objExists("All_Session_reParentLocator_set"):
		createSetResult=pm.sets(em=1, name="All_Session_reParentLocator_set")
		pm.sets('All_Session_reParentLocator_set', edit=1, fe='reParent_sets')
		
	# create locators for Joints
	for i in range(0,3):
		pm.spaceLocator(n=(SelectedControls[i] + "_reParentIKlocator"))
		pm.parentConstraint(SelectedControls[i], 
			(SelectedControls[i] + "_reParentIKlocator"), 
			weight=1)
		
	pm.select(cl=1)
	# create Joints
	for i in range(0,3):
		WorldTr=pm.xform((SelectedControls[i] + "_reParentIKlocator"), 
			q=1, ws=1, t=1)
		pm.joint(p=(WorldTr[0], WorldTr[1], WorldTr[2]), rad=1, n=(SelectedControls[i] + "_reParentIKJoint"))
		if i>0:
			pm.joint((SelectedControls[i - 1] + "_reParentIKJoint"), 
				zso=1, e=1, oj='yxz', secondaryAxisOrient='zup')
			
		
	pm.spaceLocator(n=(SelectedControls[1] + "_reParentIKPole"))
	PoleVectorLengths=float((pm.getAttr(SelectedControls[1] + "_reParentIKJoint.translateY")) + (pm.getAttr(SelectedControls[2] + "_reParentIKJoint.translateY")))
	PoleVectorMult=float((pm.getAttr(SelectedControls[2] + "_reParentIKJoint.translateY")) / (pm.getAttr(SelectedControls[1] + "_reParentIKJoint.translateY")))
	firstRePArentIK_locator_vector=pm.xform((SelectedControls[0] + "_reParentIKlocator"), 
		q=1, ws=1, t=1)
	secondRePArentIK_locator_vector=pm.xform((SelectedControls[1] + "_reParentIKlocator"), 
		q=1, ws=1, t=1)
	thindRePArentIK_locator_vector=pm.xform((SelectedControls[2] + "_reParentIKlocator"), 
		q=1, ws=1, t=1)
	mainVector=((thindRePArentIK_locator_vector - firstRePArentIK_locator_vector) / (1 + PoleVectorMult)) + firstRePArentIK_locator_vector
	poleVector=(secondRePArentIK_locator_vector - mainVector)
	poleVectorLen=float(pm.mel.sqrt(pow((poleVector.x), 2) + pow((poleVector.y), 2) + pow((poleVector.z), 2)))
	poleNorm=[((poleVector.x) / poleVectorLen), ((poleVector.y) / poleVectorLen), ((poleVector.z) / poleVectorLen)]
	FinalPoleVector=(poleNorm * (PoleVectorLengths) + mainVector)
	pm.xform((SelectedControls[1] + "_reParentIKPole"), 
		ws=1, t=((FinalPoleVector.x), (FinalPoleVector.y), (FinalPoleVector.z)))
	pm.parent((SelectedControls[1] + "_reParentIKPole"), (SelectedControls[1] + "_reParentIKlocator"))
	pm.setAttr((SelectedControls[1] + "_reParentIKPole.translateX"), 
		0)
	pm.setAttr((SelectedControls[1] + "_reParentIKPole.translateY"), 
		0)
	pm.setAttr((SelectedControls[1] + "_reParentIKPole.translateZ"), 
		0)
	pm.setAttr((SelectedControls[1] + "_reParentIKPole.rotateX"), 
		0)
	pm.setAttr((SelectedControls[1] + "_reParentIKPole.rotateY"), 
		0)
	pm.setAttr((SelectedControls[1] + "_reParentIKPole.rotateZ"), 
		0)
	pm.duplicate((SelectedControls[1] + "_reParentIKPole"), 
		n=(SelectedControls[1] + "_reParentIKoffset"))
	pm.xform((SelectedControls[1] + "_reParentIKPole"), 
		ws=1, t=((FinalPoleVector.x), (FinalPoleVector.y), (FinalPoleVector.z)))
	pm.parent((SelectedControls[1] + "_reParentIKoffset"), (SelectedControls[1] + "_reParentIKJoint"))
	pm.parentConstraint((SelectedControls[1] + "_reParentIKlocator"), (SelectedControls[1] + "_reParentIKoffset"), 
		mo=1, weight=1)
	pm.spaceLocator(n=(SelectedControls[0] + "_reParentIKoffset"))
	pm.parent((SelectedControls[0] + "_reParentIKoffset"), (SelectedControls[0] + "_reParentIKlocator"))
	pm.setAttr((SelectedControls[0] + "_reParentIKoffset.translateX"), 
		0)
	pm.setAttr((SelectedControls[0] + "_reParentIKoffset.translateY"), 
		0)
	pm.setAttr((SelectedControls[0] + "_reParentIKoffset.translateZ"), 
		0)
	pm.setAttr((SelectedControls[0] + "_reParentIKoffset.rotateX"), 
		0)
	pm.setAttr((SelectedControls[0] + "_reParentIKoffset.rotateY"), 
		0)
	pm.setAttr((SelectedControls[0] + "_reParentIKoffset.rotateZ"), 
		0)
	pm.parent((SelectedControls[0] + "_reParentIKoffset"), (SelectedControls[0] + "_reParentIKJoint"))
	pm.parentConstraint((SelectedControls[0] + "_reParentIKlocator"), (SelectedControls[0] + "_reParentIKoffset"), 
		mo=1, weight=1)
	pm.parent((SelectedControls[1] + "_reParentIKPole"), 
		w=1)
	pm.parentConstraint((SelectedControls[1] + "_reParentIKlocator"), (SelectedControls[1] + "_reParentIKPole"), 
		mo=1, weight=1)
	pm.ikHandle(ee=(SelectedControls[2] + "_reParentIKJoint"), sj=(SelectedControls[0] + "_reParentIKJoint"), w=1, p=1, n=(SelectedControls[1] + "_ikHandle"))
	pm.poleVectorConstraint((SelectedControls[1] + "_reParentIKPole"), (SelectedControls[1] + "_ikHandle"), 
		n=(SelectedControls[1] + "poleVectorConstraint"))
	pm.parentConstraint((SelectedControls[0] + "_reParentIKlocator"), (SelectedControls[0] + "_reParentIKJoint"), 
		mo=1, weight=1)
	pm.parentConstraint((SelectedControls[2] + "_reParentIKlocator"), (SelectedControls[1] + "_ikHandle"), 
		mo=1, weight=1)
	#Locked attrs
	if pm.getAttr((SelectedControls[1] + ".rotateX"), 
		l=1) == 1 or pm.getAttr((SelectedControls[1] + ".rotateY"), 
		l=1) == 1 or pm.getAttr((SelectedControls[1] + ".rotateZ"), 
		l=1) == 1:
		if pm.objExists(SelectedControls[1] + "tempLockedCtrl"):
			pm.delete(SelectedControls[1] + "tempLockedCtrl")
			
		pm.duplicate(SelectedControls[1], po=1, n=(SelectedControls[1] + "tempLockedCtrl"))
		pm.melGlobals.initVar('string', 'LockedAttr1')
		pm.melGlobals.initVar('string', 'LockedAttr2')
		if pm.getAttr((SelectedControls[1] + ".rotateX"), 
			l=1) == 0:
			pm.melGlobals['LockedAttr1']="y"
			pm.melGlobals['LockedAttr2']="z"
			
		if pm.getAttr((SelectedControls[1] + ".rotateY"), 
			l=1) == 0:
			pm.melGlobals['LockedAttr1']="x"
			pm.melGlobals['LockedAttr2']="z"
			
		if pm.getAttr((SelectedControls[1] + ".rotateZ"), 
			l=1) == 0:
			pm.melGlobals['LockedAttr1']="y"
			pm.melGlobals['LockedAttr2']="x"
			
		pm.setAttr((SelectedControls[1] + "tempLockedCtrl.rotateX"), 
			k=1)
		pm.setAttr((SelectedControls[1] + "tempLockedCtrl.rotateY"), 
			k=1)
		pm.setAttr((SelectedControls[1] + "tempLockedCtrl.rotateZ"), 
			k=1)
		pm.setAttr((SelectedControls[1] + "tempLockedCtrl.rotateX"), 
			lock=0)
		pm.setAttr((SelectedControls[1] + "tempLockedCtrl.rotateY"), 
			lock=0)
		pm.setAttr((SelectedControls[1] + "tempLockedCtrl.rotateZ"), 
			lock=0)
		#parent to First Control    
		pm.select(SelectedControls[0], r=1)
		pm.pickWalk(d='up')
		pm.melGlobals['UpHierarchyObject']=pm.ls(sl=1)
		if SelectedControls[0] != pm.melGlobals['UpHierarchyObject'][0]:
			pm.group((SelectedControls[0] + "_reParentIKlocator"), 
				n=(SelectedControls[0] + "_reParentIK_offset_grp"))
			pm.parentConstraint(pm.melGlobals['UpHierarchyObject'][0], 
				(SelectedControls[0] + "_reParentIK_offset_grp"), 
				mo=1, weight=1)
			
		pm.group((SelectedControls[1] + "_reParentIKlocator"), (SelectedControls[2] + "_reParentIKlocator"), (SelectedControls[0] + "_reParentIKJoint"), (SelectedControls[1] + "_ikHandle"), (SelectedControls[1] + "_reParentIKPole"), (SelectedControls[0] + "_reParentIK_offset_grp"), 
			n=(SelectedControls[0] + "_reParentIK_grp"))
		#group
		# Local mode
		LocalPinButton=int(pm.checkBox('IKCheckLocalBox', q=1, v=1))
		pm.select(SelectedControls[0], r=1)
		pm.pickWalk(d='up')
		pm.melGlobals['UpHierarchyObject']=pm.ls(sl=1)
		if LocalPinButton == 1 and SelectedControls[0] != pm.melGlobals['UpHierarchyObject'][0]:
			pm.delete((SelectedControls[0] + "_reParentIK_offset_grp"), 
				constraints=1)
			pm.parentConstraint(pm.melGlobals['UpHierarchyObject'][0], 
				(SelectedControls[0] + "_reParentIK_grp"), 
				mo=1, weight=1)
			
		currentR=int(pm.playbackOptions(q=1, min=1))
		currentL=int(pm.playbackOptions(q=1, max=1))
		pm.bakeResults((SelectedControls[2] + "_reParentIKlocator"), (SelectedControls[0] + "_reParentIKlocator"), (SelectedControls[1] + "_reParentIKlocator"), (SelectedControls[1] + "_reParentIKPole"), (SelectedControls[0] + "_reParentIKoffset"), (SelectedControls[1] + "_reParentIKoffset"), 
			sparseAnimCurveBake=0, 
			minimizeRotation=1, 
			removeBakedAttributeFromLayer=0, 
			removeBakedAnimFromLayer=0, 
			bakeOnOverrideLayer=0, 
			preserveOutsideKeys=1, 
			simulation=0, 
			sampleBy=1, 
			shape=0, 
			t=(str(currentL) + ":" + str(currentR)), 
			at=["tx", 
				"ty", 
				"tz", 
				"rx", 
				"ry", 
				"rz"], 
			disableImplicitControl=1, 
			controlPoints=0)
		pm.transformLimits((SelectedControls[1] + "tempLockedCtrl"), 
			erx=(0, 0))
		pm.transformLimits((SelectedControls[1] + "tempLockedCtrl"), 
			ery=(0, 0))
		pm.transformLimits((SelectedControls[1] + "tempLockedCtrl"), 
			erz=(0, 0))
		pm.transformLimits(SelectedControls[1], erx=(0, 0))
		pm.transformLimits(SelectedControls[1], ery=(0, 0))
		pm.transformLimits(SelectedControls[1], erz=(0, 0))
		pm.orientConstraint((SelectedControls[1] + "_reParentIKoffset"), (SelectedControls[1] + "tempLockedCtrl"), 
			mo=1, weight=1)
		pm.orientConstraint((SelectedControls[0] + "_reParentIKoffset"), 
			SelectedControls[0], mo=1, weight=1)
		pm.orientConstraint((SelectedControls[1] + "tempLockedCtrl"), 
			SelectedControls[1], skip=[pm.melGlobals['LockedAttr1'], pm.melGlobals['LockedAttr2']], mo=1, weight=1)
		pm.orientConstraint((SelectedControls[2] + "_reParentIKlocator"), 
			SelectedControls[2], mo=1, weight=1)
		
	
	else:
		pm.select(SelectedControls[0], r=1)
		#parent to First Control    
		pm.pickWalk(d='up')
		pm.melGlobals['UpHierarchyObject']=pm.ls(sl=1)
		if SelectedControls[0] != pm.melGlobals['UpHierarchyObject'][0]:
			pm.group((SelectedControls[0] + "_reParentIKlocator"), 
				n=(SelectedControls[0] + "_reParentIK_offset_grp"))
			pm.parentConstraint(pm.melGlobals['UpHierarchyObject'][0], 
				(SelectedControls[0] + "_reParentIK_offset_grp"), 
				mo=1, weight=1)
			
		currentR=int(pm.playbackOptions(q=1, min=1))
		currentL=int(pm.playbackOptions(q=1, max=1))
		#group
		pm.group((SelectedControls[1] + "_reParentIKlocator"), (SelectedControls[2] + "_reParentIKlocator"), (SelectedControls[0] + "_reParentIKJoint"), (SelectedControls[1] + "_ikHandle"), (SelectedControls[1] + "_reParentIKPole"), (SelectedControls[0] + "_reParentIK_offset_grp"), 
			n=(SelectedControls[0] + "_reParentIK_grp"))
		# Local mode
		LocalPinButton=int(pm.checkBox('IKCheckLocalBox', q=1, v=1))
		pm.select(SelectedControls[0], r=1)
		pm.pickWalk(d='up')
		pm.melGlobals['UpHierarchyObject']=pm.ls(sl=1)
		if LocalPinButton == 1 and SelectedControls[0] != pm.melGlobals['UpHierarchyObject'][0]:
			pm.delete((SelectedControls[0] + "_reParentIK_offset_grp"), 
				constraints=1)
			pm.parentConstraint(pm.melGlobals['UpHierarchyObject'][0], 
				(SelectedControls[0] + "_reParentIK_grp"), 
				mo=1, weight=1)
			
		pm.bakeResults((SelectedControls[2] + "_reParentIKlocator"), (SelectedControls[0] + "_reParentIKlocator"), (SelectedControls[1] + "_reParentIKPole"), (SelectedControls[0] + "_reParentIKoffset"), (SelectedControls[1] + "_reParentIKoffset"), 
			sparseAnimCurveBake=0, 
			minimizeRotation=1, 
			removeBakedAttributeFromLayer=0, 
			removeBakedAnimFromLayer=0, 
			bakeOnOverrideLayer=0, 
			preserveOutsideKeys=1, 
			simulation=0, 
			sampleBy=1, 
			shape=0, 
			t=(str(currentL) + ":" + str(currentR)), 
			at=["tx", 
				"ty", 
				"tz", 
				"rx", 
				"ry", 
				"rz"], 
			disableImplicitControl=1, 
			controlPoints=0)
		pm.orientConstraint((SelectedControls[0] + "_reParentIKoffset"), 
			SelectedControls[0], mo=1, weight=1)
		pm.orientConstraint((SelectedControls[1] + "_reParentIKoffset"), 
			SelectedControls[1], mo=1, weight=1)
		pm.orientConstraint((SelectedControls[2] + "_reParentIKlocator"), 
			SelectedControls[2], mo=1, weight=1)
		
	pm.setAttr((SelectedControls[0] + "_reParentIKJoint.drawStyle"), 
		2)
	#visibility
	pm.setAttr((SelectedControls[1] + "_reParentIKJoint.drawStyle"), 
		2)
	pm.setAttr((SelectedControls[2] + "_reParentIKJoint.drawStyle"), 
		2)
	pm.setAttr((SelectedControls[0] + "_reParentIKlocator.visibility"), 
		0)
	pm.setAttr((SelectedControls[1] + "_reParentIKlocator.visibility"), 
		0)
	pm.setAttr((SelectedControls[0] + "_reParentIKoffset.visibility"), 
		0)
	pm.setAttr((SelectedControls[1] + "_reParentIKoffset.visibility"), 
		0)
	pm.setAttr((SelectedControls[1] + "_ikHandle.visibility"), 
		0)
	#size
	JointLentgts=float(pm.getAttr(SelectedControls[1] + "_reParentIKJoint.translateY"))
	pm.setAttr((SelectedControls[2] + "_reParentIKlocator.localScaleX"), (JointLentgts / 2))
	pm.setAttr((SelectedControls[2] + "_reParentIKlocator.localScaleY"), (JointLentgts / 2))
	pm.setAttr((SelectedControls[2] + "_reParentIKlocator.localScaleZ"), (JointLentgts / 2))
	pm.setAttr((SelectedControls[1] + "_reParentIKPole.localScaleX"), (JointLentgts / 4))
	pm.setAttr((SelectedControls[1] + "_reParentIKPole.localScaleY"), (JointLentgts / 4))
	pm.setAttr((SelectedControls[1] + "_reParentIKPole.localScaleZ"), (JointLentgts / 4))
	#color
	pm.setAttr((SelectedControls[2] + "_reParentIKlocatorShape.overrideEnabled"), 
		1)
	pm.setAttr((SelectedControls[2] + "_reParentIKlocatorShape.overrideColor"), 
		17)
	pm.setAttr((SelectedControls[1] + "_reParentIKPoleShape.overrideEnabled"), 
		1)
	pm.setAttr((SelectedControls[1] + "_reParentIKPoleShape.overrideColor"), 
		13)
	pm.sets((SelectedControls[2] + "_reParentIKlocator"), 
		edit=1, forceElement='Last_Session_reParentLocator_set')
	pm.sets((SelectedControls[2] + "_reParentIKlocator"), 
		edit=1, forceElement='All_Session_reParentLocator_set')
	pm.sets((SelectedControls[1] + "_reParentIKPole"), 
		edit=1, forceElement='Last_Session_reParentLocator_set')
	pm.sets((SelectedControls[1] + "_reParentIKPole"), 
		edit=1, forceElement='All_Session_reParentLocator_set')
	pm.select((SelectedControls[2] + "_reParentIKlocator"), 
		r=1)
	


def reParentLocatorSize():
	"""Locator Size       """
	

	SelectedControls=pm.ls(sl=1)
	# Clean Joints
	if pm.objectType(SelectedControls[0]) == "joint" and not pm.objExists(SelectedControls[0] + "Shape") and not pm.objExists(SelectedControls[0] + "Shape1"):
		firstPos = []
		secondPos = []
		firstVect = []
		firstLen = 0.0
		pm.melGlobals['UpHierarchyObject'] = []
		pm.select(SelectedControls[0], r=1)
		pm.pickWalk(d='down')
		pm.melGlobals['UpHierarchyObject']=pm.ls(sl=1)
		if SelectedControls[0] != pm.melGlobals['UpHierarchyObject'][0]:
			firstPos=pm.xform(SelectedControls[0], q=1, ws=1, t=1)
			secondPos=pm.xform(pm.melGlobals['UpHierarchyObject'][0], q=1, ws=1, t=1)
			firstVect=(secondPos - firstPos)
			firstLen=float(pm.mel.sqrt(pow((firstVect.x), 2) + pow((firstVect.y), 2) + pow((firstVect.z), 2)))
			pm.setAttr("TempLocatorShape.localScaleX", 
				(firstLen * 2))
			pm.setAttr("TempLocatorShape.localScaleY", 
				(firstLen * 2))
			pm.setAttr("TempLocatorShape.localScaleZ", 
				(firstLen * 2))
			
		
		else:
			pm.select(SelectedControls[0], r=1)
			pm.pickWalk(d='up')
			pm.melGlobals['UpHierarchyObject']=pm.ls(sl=1)
			if SelectedControls[0] != pm.melGlobals['UpHierarchyObject'][0]:
				firstPos=pm.xform(SelectedControls[0], q=1, ws=1, t=1)
				secondPos=pm.xform(pm.melGlobals['UpHierarchyObject'][0], q=1, ws=1, t=1)
				firstVect=(secondPos - firstPos)
				firstLen=float(pm.mel.sqrt(pow((firstVect.x), 2) + pow((firstVect.y), 2) + pow((firstVect.z), 2)))
				pm.setAttr("TempLocatorShape.localScaleX", 
					(firstLen * 2))
				pm.setAttr("TempLocatorShape.localScaleY", 
					(firstLen * 2))
				pm.setAttr("TempLocatorShape.localScaleZ", 
					(firstLen * 2))
				
			
		
	if pm.objectType(SelectedControls[0]) == "joint" and pm.objExists(SelectedControls[0] + "Shape"):
		SelectedControls[0]=(SelectedControls[0] + "Shape")
		# Joint with Shapes
		bbox=pm.exactWorldBoundingBox(SelectedControls[0])
		locatorSizeX=bbox[3] - bbox[0]
		locatorSizeY=bbox[4] - bbox[1]
		locatorSizeZ=bbox[5] - bbox[2]
		locatorSize=((locatorSizeX + locatorSizeY + locatorSizeZ) / 3)
		pm.setAttr("TempLocatorShape.localScaleX", 
			(locatorSize / 1))
		pm.setAttr("TempLocatorShape.localScaleY", 
			(locatorSize / 1))
		pm.setAttr("TempLocatorShape.localScaleZ", 
			(locatorSize / 1))
		
	if pm.objectType(SelectedControls[0]) == "transform":
		bbox=pm.exactWorldBoundingBox(SelectedControls[0])
		# Simple transforms
		locatorSizeX=bbox[3] - bbox[0]
		locatorSizeY=bbox[4] - bbox[1]
		locatorSizeZ=bbox[5] - bbox[2]
		locatorSize=((locatorSizeX + locatorSizeY + locatorSizeZ) / 3)
		if pm.objExists("*ctlArmUpGimbalLf") or pm.objExists("*:*ctlArmUpGimbalLf"):
			pm.setAttr("TempLocatorShape.localScaleX", 0.6)
			pm.setAttr("TempLocatorShape.localScaleY", 0.6)
			pm.setAttr("TempLocatorShape.localScaleZ", 0.6)
			
		
		else:
			pm.setAttr("TempLocatorShape.localScaleX", 
				(locatorSize / 1))
			pm.setAttr("TempLocatorShape.localScaleY", 
				(locatorSize / 1))
			pm.setAttr("TempLocatorShape.localScaleZ", 
				(locatorSize / 1))
			
		
	if pm.objExists("*MotionSystem*") or pm.objExists("*:*MotionSystem*"):
		SelectedControls[0]=(SelectedControls[0] + "Shape")
		# AS
		bbox=pm.exactWorldBoundingBox(SelectedControls[0])
		locatorSizeX=bbox[3] - bbox[0]
		locatorSizeY=bbox[4] - bbox[1]
		locatorSizeZ=bbox[5] - bbox[2]
		locatorSize=((locatorSizeX + locatorSizeY + locatorSizeZ) / 3)
		pm.setAttr("TempLocatorShape.localScaleX", 
			(locatorSize / 1))
		pm.setAttr("TempLocatorShape.localScaleY", 
			(locatorSize / 1))
		pm.setAttr("TempLocatorShape.localScaleZ", 
			(locatorSize / 1))