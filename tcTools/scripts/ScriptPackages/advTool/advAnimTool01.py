# coding=utf-8

import pymel.core as pm
import os

fbxList = []
tsList = None
itemList = []

attr = []
attrVal = []
data = {}

def mainUI():
	try:
		pm.deleteUI('advTool')
	except Exception as e:
		print(e)

	global tsList
	
	temlate = pm.uiTemplate('ctTemplate',force=True)
	temlate.define(pm.button,w=200,h=30)
	temlate.define(pm.frameLayout,borderVisible=True,cll=True,cl=False)

	with pm.window('advTool',title='advAnimtools')as win:
		with temlate:
			with pm.columnLayout(rowSpacing=5,adj=True):

				with pm.frameLayout(label = 'Import single FBX'):
					with pm.columnLayout(adj = 1):
						pm.button(label="Import fbx",c=impAnim)

				with pm.frameLayout(label='Import multiple FBX'):
					with pm.columnLayout(w=200,h=150,adj=True):
						tsList = pm.textScrollList(allowMultiSelection = True, h =150, w =240)

					with pm.rowLayout(numberOfColumns=3,adj = 1):
						pm.button(label="Load",w=80,h=30, c = load)
						pm.button(label="remove",w=80,h=30, c = remove)
						pm.button(label="clear",w=80,h=30, c = clear)

					with pm.rowLayout(numberOfColumns=3,
									  columnWidth3=(55,140,5),
									  adjustableColumn=2,
									  columnAlign=(1, 'right'),
									  columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)]
					):
						pm.text(label='Save Path:')
						pm.textField("ImporterTextField")
						pm.button(label='...',w=30,h=20,c=selectPath)

					with pm.columnLayout(adj = 1):
						pm.button(label="Import fbx And Save File !!!",c=impNSavCMD)

				with pm.frameLayout(label='Motion Switch'):
					with pm.columnLayout(adj = 1):
						pm.button(label='Local Motion',c=rootToLocal)
						pm.button(label='Root Motion',c=localToRoot)

				with pm.frameLayout(label='Copy Paste Pose'):
					with pm.columnLayout(adj = 1):
						pm.button(label='Copy Pose',c=copyPose)
						pm.button(label='Paste Pose',c=pastePose)
						pm.button(label='Paste Mirror Pose',c=pasteMirPose)

	pm.window(win,e=True,w=240,h=300)
	pm.showWindow(win)

def impAnim(*args):

	singleFbx = pm.fileDialog2(fileFilter="*fbx",fileMode=1)

	if not singleFbx:
		pm.PopupError("Nothing Selected!!!")
		return

	FKIKAttr = ["FKIKArm_L.FKIKBlend",
			"FKIKArm_R.FKIKBlend",
			"FKIKSpine_M.FKIKBlend",
			"FKIKLeg_R.FKIKBlend",
			"FKIKLeg_L.FKIKBlend"
			]
	for a in FKIKAttr:
		pm.setAttr(a,0)

	pm.duplicate("NameMatcher:root")
	pm.select("root",hi=True)
	pm.delete(constraints=True)

	pm.parentConstraint("root","root_ctrl",mo=True)
	pm.parentConstraint("root","Main",mo=True)
	pm.parentConstraint("pelvis","RootX_M",mo=True)

	jointSl = ["spine_01","spine_02","spine_03","neck_01","head","clavicle_l","upperarm_l","lowerarm_l","hand_l","thumb_01_l","thumb_02_l",
	"thumb_03_l","index_01_l","index_02_l","index_03_l","middle_01_l","middle_02_l","middle_03_l","ring_01_l","ring_02_l","ring_03_l","pinky_01_l",
	"pinky_02_l","pinky_03_l","clavicle_r","upperarm_r","lowerarm_r","hand_r","thumb_01_r","thumb_02_r","thumb_03_r","index_01_r","index_02_r",
	"index_03_r","middle_01_r","middle_02_r","middle_03_r","ring_01_r","ring_02_r","ring_03_r","pinky_01_r","pinky_02_r","pinky_03_r","thigh_l",
	"thigh_r","calf_l","calf_r","foot_l","foot_r","ball_l","ball_r"]

	ctrlSl = ["FKSpine1_M","FKSpine2_M","FKChest_M","FKNeck_M","FKHead_M","FKScapula_L","FKShoulder_L","FKElbow_L","FKWrist_L","FKThumbFinger1_L",
	"FKThumbFinger2_L","FKThumbFinger3_L","FKIndexFinger1_L","FKIndexFinger2_L","FKIndexFinger3_L","FKMiddleFinger1_L","FKMiddleFinger2_L","FKMiddleFinger3_L",
	"FKRingFinger1_L","FKRingFinger2_L","FKRingFinger3_L","FKPinkyFinger1_L","FKPinkyFinger2_L","FKPinkyFinger3_L","FKScapula_R","FKShoulder_R","FKElbow_R",
	"FKWrist_R","FKThumbFinger1_R","FKThumbFinger2_R","FKThumbFinger3_R","FKIndexFinger1_R","FKIndexFinger2_R","FKIndexFinger3_R","FKMiddleFinger1_R",
	"FKMiddleFinger2_R","FKMiddleFinger3_R","FKRingFinger1_R","FKRingFinger2_R","FKRingFinger3_R","FKPinkyFinger1_R","FKPinkyFinger2_R","FKPinkyFinger3_R",
	"FKHip_L","FKHip_R","FKKnee_L","FKKnee_R","FKAnkle_L","FKAnkle_R","IKToes_L","IKToes_R"]

	for i in range(len(jointSl)):
		pm.parentConstraint(jointSl[i],ctrlSl[i],mo=True,skipTranslate=["x","y","z"])

	pm.importFile(singleFbx[0])

	firstFrame = pm.findKeyframe('root',which="first")
	lastFrame = pm.findKeyframe('root',which="last")
	pm.env.setMinTime(firstFrame)
	pm.env.setMaxTime(lastFrame)
	ctrlBk = [
		'FKWeaponAS_R','FKRingFinger3_R','FKRingFinger2_R','FKRingFinger1_R','FKWrist_R','FKElbow_R','FKShoulder_R','FKToes_R','FKAnkle_R','FKKnee_R','FKHip_R','FKToes_L','FKAnkle_L',
		'FKKnee_L','FKHip_L','RootX_M','AimEye_L','AimEye_R','AimEye_M','FKNeck_M','HipSwinger_M','FKChest_M','FKSpine2_M','FKEye_R','FKJaw_M','FKHead_M','FKScapula_L','FKWeaponASB_R',
		'FKScapula_R','FKEye_L','FKThumbFinger2_R','FKThumbFinger1_R','FKMiddleFinger3_R','FKMiddleFinger2_R','FKMiddleFinger1_R','FKThumbFinger1_L','FKMiddleFinger3_L','FKMiddleFinger2_L',
		'FKMiddleFinger1_L','FKIndexFinger2_L','FKIndexFinger1_L','FKThumbFinger3_L','FKThumbFinger2_L','FKIndexFinger3_R','FKIndexFinger2_R','FKIndexFinger1_R','FKThumbFinger3_R','FKPinkyFinger3_R',
		'FKPinkyFinger2_R','FKPinkyFinger1_R','FKCup_R','MainExtra2','FKSpine1_M','FKRoot_M','root_ctrl','Main','MainExtra1','FKPinkyFinger2_L','FKPinkyFinger1_L','FKCup_L','FKIndexFinger3_L','FKRingFinger3_L',
		'FKRingFinger2_L','FKRingFinger1_L','FKPinkyFinger3_L','Fingers_L','Fingers_R','FKWrist_L','FKElbow_L','FKShoulder_L','PoleLeg_R','IKToes_R','RollToes_R','RollToesEnd_R','RollHeel_R','IKLeg_L',
		'PoleLeg_L','IKToes_L','RollToes_L','RollToesEnd_L','RollHeel_L','IKLeg_R','FKWeaponAS_L'
		]
	pm.select(ctrlBk)
	pm.bakeResults(time=(firstFrame, lastFrame))
	pm.filterCurve()
	pm.delete('root')
	print("Done")

def load(*args):

	global itemList

	itemList = pm.textScrollList(tsList, query = True, allItems = 1)
	if itemList == None:
		itemList = []

	fbxList = pm.fileDialog2(fileFilter="*fbx",fileMode=4)

	for fbx in fbxList:
		if fbx not in itemList:
			pm.textScrollList(tsList, edit = True, append = fbx)
			itemList.append(fbx)
			continue

def remove(*args):
	global itemList
	itemList = pm.textScrollList(tsList, query = True, selectItem = True)
	for item in itemList:
		pm.textScrollList(tsList, edit = True, removeItem = item)
	itemList = pm.textScrollList(tsList, query = True, selectItem = True)

def clear(*args):		
	global itemList
	pm.textScrollList(tsList, edit = True, removeAll = True)
	itemList = []

def selectPath(*args):
	savePath = pm.fileDialog2(fileFilter='*folder',fileMode=2)
	if savePath:
		savePath = savePath[0]
		pm.textField("ImporterTextField",e=True,text=savePath)

def impNSavCMD(*args):

	if not itemList:
		pm.PopupError('Nothing To Import')
		return

	FKIKAttr = ["FKIKArm_L.FKIKBlend",
			"FKIKArm_R.FKIKBlend",
			"FKIKSpine_M.FKIKBlend",
			"FKIKLeg_R.FKIKBlend",
			"FKIKLeg_L.FKIKBlend"
			]
	for a in FKIKAttr:
		pm.setAttr(a,0)
		
	for s in range(len(itemList)):

		pm.duplicate("NameMatcher:root")
		pm.select("root",hi=True)
		pm.delete(constraints=True)

		pm.parentConstraint("root","root_ctrl",mo=True)
		pm.parentConstraint("root","Main",mo=True)
		pm.parentConstraint("pelvis","RootX_M",mo=True)

		jointSl = ["spine_01","spine_02","spine_03","neck_01","head","clavicle_l","upperarm_l","lowerarm_l","hand_l","thumb_01_l","thumb_02_l",
		"thumb_03_l","index_01_l","index_02_l","index_03_l","middle_01_l","middle_02_l","middle_03_l","ring_01_l","ring_02_l","ring_03_l","pinky_01_l",
		"pinky_02_l","pinky_03_l","clavicle_r","upperarm_r","lowerarm_r","hand_r","thumb_01_r","thumb_02_r","thumb_03_r","index_01_r","index_02_r",
		"index_03_r","middle_01_r","middle_02_r","middle_03_r","ring_01_r","ring_02_r","ring_03_r","pinky_01_r","pinky_02_r","pinky_03_r","thigh_l",
		"thigh_r","calf_l","calf_r","foot_l","foot_r","ball_l","ball_r"]

		ctrlSl = ["FKSpine1_M","FKSpine2_M","FKChest_M","FKNeck_M","FKHead_M","FKScapula_L","FKShoulder_L","FKElbow_L","FKWrist_L","FKThumbFinger1_L",
		"FKThumbFinger2_L","FKThumbFinger3_L","FKIndexFinger1_L","FKIndexFinger2_L","FKIndexFinger3_L","FKMiddleFinger1_L","FKMiddleFinger2_L","FKMiddleFinger3_L",
		"FKRingFinger1_L","FKRingFinger2_L","FKRingFinger3_L","FKPinkyFinger1_L","FKPinkyFinger2_L","FKPinkyFinger3_L","FKScapula_R","FKShoulder_R","FKElbow_R",
		"FKWrist_R","FKThumbFinger1_R","FKThumbFinger2_R","FKThumbFinger3_R","FKIndexFinger1_R","FKIndexFinger2_R","FKIndexFinger3_R","FKMiddleFinger1_R",
		"FKMiddleFinger2_R","FKMiddleFinger3_R","FKRingFinger1_R","FKRingFinger2_R","FKRingFinger3_R","FKPinkyFinger1_R","FKPinkyFinger2_R","FKPinkyFinger3_R",
		"FKHip_L","FKHip_R","FKKnee_L","FKKnee_R","FKAnkle_L","FKAnkle_R","IKToes_L","IKToes_R"]

		for i in range(len(jointSl)):
			pm.parentConstraint(jointSl[i],ctrlSl[i],mo=True,skipTranslate=["x","y","z"])

		pm.importFile(fbxList[s])

		firstFrame = pm.findKeyframe('root',which="first")
		lastFrame = pm.findKeyframe('root',which="last")
		pm.env.setMinTime(firstFrame)
		pm.env.setMaxTime(lastFrame)

		ctrlBk = [
			'FKWeaponAS_R','FKRingFinger3_R','FKRingFinger2_R','FKRingFinger1_R','FKWrist_R','FKElbow_R','FKShoulder_R','FKToes_R','FKAnkle_R','FKKnee_R','FKHip_R','FKToes_L','FKAnkle_L',
			'FKKnee_L','FKHip_L','RootX_M','AimEye_L','AimEye_R','AimEye_M','FKNeck_M','HipSwinger_M','FKChest_M','FKSpine2_M','FKEye_R','FKJaw_M','FKHead_M','FKScapula_L','FKWeaponASB_R',
			'FKScapula_R','FKEye_L','FKThumbFinger2_R','FKThumbFinger1_R','FKMiddleFinger3_R','FKMiddleFinger2_R','FKMiddleFinger1_R','FKThumbFinger1_L','FKMiddleFinger3_L','FKMiddleFinger2_L',
			'FKMiddleFinger1_L','FKIndexFinger2_L','FKIndexFinger1_L','FKThumbFinger3_L','FKThumbFinger2_L','FKIndexFinger3_R','FKIndexFinger2_R','FKIndexFinger1_R','FKThumbFinger3_R','FKPinkyFinger3_R',
			'FKPinkyFinger2_R','FKPinkyFinger1_R','FKCup_R','MainExtra2','FKSpine1_M','FKRoot_M','root_ctrl','Main','MainExtra1','FKPinkyFinger2_L','FKPinkyFinger1_L','FKCup_L','FKIndexFinger3_L','FKRingFinger3_L',
			'FKRingFinger2_L','FKRingFinger1_L','FKPinkyFinger3_L','Fingers_L','Fingers_R','FKWrist_L','FKElbow_L','FKShoulder_L','PoleLeg_R','IKToes_R','RollToes_R','RollToesEnd_R','RollHeel_R','IKLeg_L',
			'PoleLeg_L','IKToes_L','RollToes_L','RollToesEnd_L','RollHeel_L','IKLeg_R','FKWeaponAS_L'
			]
		pm.select(ctrlBk)
		pm.bakeResults(time=(firstFrame,lastFrame))
		pm.filterCurve()
		pm.delete('root')
		print("Done")
		
		savePath = pm.textField("ImporterTextField",q=True,text=True)
		shortName=fbxList[s].split('/')[-1].split('.')[-2]
		filePath = savePath + '/' + shortName + ".mb"
		print(filePath)
		pm.saveAs(filePath,force=True)

	confirm = pm.confirmDialog(title='Finish',message="Done!",button=['OK','Open Folder'])
	if confirm == 'Open Folder':
		os.startfile(savePath)

def rootToLocal(*args):

	firstFrame = pm.findKeyframe('RootX_M',which="first")
	lastFrame = pm.findKeyframe('RootX_M',which="last")

	pm.spaceLocator(name="locPelvis")
	pm.spaceLocator(name="locLFoot")
	pm.spaceLocator(name="locRFoot")

	pm.parentConstraint('RootX_M','locPelvis')
	pm.parentConstraint('IKLeg_L','locLFoot')
	pm.parentConstraint('IKLeg_R','locRFoot')

	pm.bakeResults('locPelvis','locLFoot','locRFoot',time=(firstFrame, lastFrame))

	pm.parentConstraint('locPelvis','RootX_M')
	pm.parentConstraint('locLFoot','IKLeg_L')
	pm.parentConstraint('locRFoot','IKLeg_R')

	disAttr = [
		"Main.tx","Main.ty","Main.tz","Main.rx","Main.ry","Main.rz",
		"root_ctrl.tx","root_ctrl.ty","root_ctrl.tz","root_ctrl.rx","root_ctrl.ry","root_ctrl.rz"
	]

	for attr in disAttr:
		pm.disconnectAttr(disAttr)

	pm.xform('Main',translation=(0,0,0),rotation=(0,0,0))
	pm.xform('root_ctrl',translation=(0,0,0),rotation=(0,0,0))


	pm.bakeResults('RootX_M','IKLeg_L','IKLeg_R',time=(firstFrame,lastFrame))

	pm.delete('locPelvis','locLFoot','locRFoot')

def localToRoot(*args):
	firstFrame = pm.findKeyframe('RootX_M',which="first")
	lastFrame = pm.findKeyframe('RootX_M',which="last")

	pm.spaceLocator(name="locPelvis")
	pm.spaceLocator(name="locLFoot")
	pm.spaceLocator(name="locRFoot")

	pm.parentConstraint('RootX_M','locPelvis')
	pm.parentConstraint('IKLeg_L','locLFoot')
	pm.parentConstraint('IKLeg_R','locRFoot')

	pm.bakeResults('locPelvis','locLFoot','locRFoot',time=(firstFrame, lastFrame))

	pm.parentConstraint('locPelvis','RootX_M')
	pm.parentConstraint('locLFoot','IKLeg_L')
	pm.parentConstraint('locRFoot','IKLeg_R')

	pelvisTX = pm.getAttr('RootX_M.translateX')
	pelvisTY = pm.getAttr('RootX_M.translateY')
	pelvisTZ = pm.getAttr('RootX_M.translateZ')
	pelvisRX = pm.getAttr('RootX_M.rotateX')
	pelvisRY = pm.getAttr('RootX_M.rotateY')
	pelvisRZ = pm.getAttr('RootX_M.rotateZ')


	pm.setAttr('root_ctrl.translateX', pelvisTX)
	pm.setAttr('root_ctrl.translateY', pelvisTZ*-1)
	pm.setAttr('root_ctrl.translateZ', 0)
	pm.setAttr('root_ctrl.rotateX', 0)
	pm.setAttr('root_ctrl.rotateY', 0)
	pm.setAttr('root_ctrl.rotateZ', pelvisRY)


	pm.parentConstraint('locPelvis','root_ctrl',mo=True,skipTranslate=["z"],skipRotate=["x","y"])

	pm.bakeResults('RootX_M','IKLeg_L','IKLeg_R','root_ctrl','Main',time=(firstFrame,lastFrame))

	pm.delete('locPelvis','locLFoot','locRFoot')

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