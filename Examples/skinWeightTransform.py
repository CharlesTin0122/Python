import pymel.core as pm
pm.melGlobals.initVar('string', 'gShelfTopLevel')
currentShelf=str(pm.tabLayout(pm.melGlobals['gShelfTopLevel'], query=1, selectTab=1))
pm.setParent(currentShelf)
asInstallScriptLocation=str(pm.mel.asInstallScriptLocation())
if pm.mel.gmatch(asInstallScriptLocation, "*\*"):
	asInstallScriptLocation=str(pm.mel.substituteAllString(asInstallScriptLocation, "\\", "/"))
	
scriptName="AdvancedSkeleton5"
sourceFile=asInstallScriptLocation + scriptName + ".mel"
command="source \"" + sourceFile + "\";" + scriptName + ";"
iconExt="png"
if pm.mel.asMayaVersionAsFloat()<2012:
	iconExt="xpm"
	
icon=asInstallScriptLocation + "AdvancedSkeleton5Files/icons/AS5." + iconExt
if not pm.pm.cmds.file(sourceFile, q=1, ex=1):
	pm.pm.mel.error("Something went wrong, can not find: \"" + sourceFile + "\"")
	
pm.shelfButton(sourceType="mel", 
	image=icon, 
	label=scriptName, 
	command=lambda *args: pm.mel.command(), 
	image1=icon, 
	annotation=scriptName)
#--installTemplate pause--//
pm.shelfButton(sourceType="mel", 
	image=(asInstallScriptLocation + "AdvancedSkeleton5Files/icons/asBiped." + iconExt), 
	label="Selector:biped", 
	command=lambda *args: pm.mel.source(" + asInstallScriptLocation + AdvancedSkeleton5Files/Selector/biped.mel"), 
	image1=(asInstallScriptLocation + "AdvancedSkeleton5Files/icons/asBiped." + iconExt), 
	annotation="Selector:biped")
pm.shelfButton(sourceType="mel", 
	image=(asInstallScriptLocation + "AdvancedSkeleton5Files/icons/asFace." + iconExt), 
	label="Selector:face", 
	command=lambda *args: pm.mel.source(" + asInstallScriptLocation + AdvancedSkeleton5Files/Selector/face.mel"), 
	image1=(asInstallScriptLocation + "AdvancedSkeleton5Files/icons/asFace." + iconExt), 
	annotation="Selector:face")
pm.shelfButton(sourceType="mel", 
	image=(asInstallScriptLocation + "AdvancedSkeleton5Files/picker/pickerFiles/icons/picker." + iconExt), 
	label="picker", 
	command=lambda *args: pm.mel.source(" + asInstallScriptLocation + AdvancedSkeleton5Files/picker/picker.mel"), 
	image1=(asInstallScriptLocation + "AdvancedSkeleton5Files/picker/pickerFiles/icons/picker." + iconExt), 
	annotation="picker")
#--installTemplate resume--//
print ("\n// " + scriptName + " has been added to current shelf.\n")

def asInstallScriptLocator():
	
	pass
	


def asInstallScriptLocation():
	
	whatIs=str(pm.mel.whatIs('asInstallScriptLocator'))
	fullPath=whatIs[24:999]
	buffer = []
	slash="/"
	if pm.mel.gmatch(whatIs, "*\\\\*"):
		slash="\\"
		#sourced from ScriptEditor
		
	numTok=int(buffer=fullPath.split(slash))
	numLetters=len(fullPath)
	numLettersLastFolder=len(buffer[numTok - 1])
	scriptLocation=fullPath[0:numLetters - numLettersLastFolder]
	return scriptLocation
	


def asMayaVersionAsFloat():
	
	version=float(2012)
	if pm.mel.exists('getApplicationVersionAsFloat'):
		return pm.mel.getApplicationVersionAsFloat()
		
	versionString=str(pm.about(v=1))
	tempString = []
	char = ""
	tempString=versionString.split()
	#default to 2012, if versionString is not all numbers
	for i in range(0,len(tempString[0])):
		char=tempString[0][i + 1-1:i + 1]
		if not pm.mel.gmatch(char, "[0-9]"):
			return 2012
			
		
	version=float(tempString[0])
	return version
	

