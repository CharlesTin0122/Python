import pymel.core as pm
import os

fileList = []
objList = []
slyFile = None
slyOBJ = None

def mainUI():
	try:
		pm.deleteUI('fbxExport')
	except Exception as e:
		print(e)

	global slyFile,slyOBJ
	
	temlate = pm.uiTemplate('ctTemplate',force=True)
	temlate.define(pm.button,w=200,h=30)
	temlate.define(pm.frameLayout,borderVisible=True,cll=True,cl=False)

	with pm.window('fbxExport',title='fbxExporter')as win:
		with temlate:
			with pm.columnLayout(rowSpacing=5,adj=True):

				with pm.frameLayout(label='Export multiple File'):
					with pm.columnLayout(adj = 1):
						pm.button(label="Load All Export File",c=loadFile)
					with pm.scrollLayout(w=200,h=150,bgc=(0.5,0.5,0.5)) as slyFile:
						pm.text('File Name:')
					with pm.columnLayout(adj = 1):
						pm.button(label="Load OBJ To Export",c=loadOBJ)
					with pm.scrollLayout(w=200,h=150,bgc=(0.5,0.5,0.5)) as slyOBJ:
						pm.text('OBJ Name:')
					with pm.rowLayout(numberOfColumns=3,
									  columnWidth3=(55,140,5),
									  adjustableColumn=2,
									  columnAlign=(1, 'right'),
									  columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)]
					):
						pm.text(label='Export Path:',w=65)
						pm.textField("ExporterTextField")
						pm.button(label='...',w=30,h=20,c=exportPath)
					with pm.columnLayout(adj = 1):
						pm.button(label="Export All !!!",c=exportAll)

	pm.window(win,e=True,w=250,h=300)
	pm.showWindow(win)

def loadFile(*args):
	global fileList,slyFile
	fileList = pm.fileDialog2(fileFilter="*mb",fileMode=4)

	if not fileList:
		pm.PopupError('Nothing Selected')
		fileList = []
		return

	for i in range(len(fileList)):
		fileName = os.path.basename(fileList[i])
		with slyFile:
			pm.text(label=fileName)	

def loadOBJ(*args):
	global slyOBJ,objList
	objList = pm.selected()
	for obj in objList:
		with slyOBJ:
			pm.text(label=obj)

def exportPath(*args):
	exportPath = pm.fileDialog2(fileFilter='*folder',fileMode=2)
	if exportPath:
		exportPath = exportPath[0]
		pm.textField("ExporterTextField",e=True,text=exportPath)

def exportAll(*args):
	for f in fileList:
		fileName = os.path.basename(f)
		baceName = os.path.splitext(fileName)
		expName = str(baceName[0]) + '.fbx'
		
		pm.openFile(f,force=True)
		pm.select(objList)
		pm.bakeResults(t=(pm.env.getMaxTime(),pm.env.getMinTime()),bol=True)
		pm.select(objList)
		pm.exportSelected(exportPath[0]+'/'+expName,force=True)
		pm.delete('BakeResultsContainer')
