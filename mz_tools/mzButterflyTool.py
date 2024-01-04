"""
mzButterflyTool_b02.py

Version: b02  updated: July 12, 2021
Author: Steven Thomasson
Copyright (c) 2021 Steven Thomasson

"""
import maya.cmds as cmds
import maya.api.OpenMaya as om
import os, errno
import json
import math 

def mzButterflyTool_UI():
    # user interface for mzButterflyTool
    if checkWorkingUnits()=='No':
        return 
    ds = DefaultButterflySettings()
      
    if cmds.window( "mzButterflyToolWindow", exists=True ):
        cmds.deleteUI( "mzButterflyToolWindow", window=True )
    # if cmds.windowPref( "mzButterflyToolWindow", exists=True ):
    #     cmds.windowPref( "mzButterflyToolWindow", remove=True )
    window = cmds.window( "mzButterflyToolWindow", title="mzButterflyTool", widthHeight=(240, 680) )
    cmds.scrollLayout( "scrollLayout" )
    cmds.columnLayout( adjustableColumn=True, columnOffset=("both", 4) ) #, backgroundColor=[1.0,0.0,0.0] )
    #------------------------------------------------------------------  
    # Object name
    cmds.columnLayout( rowSpacing=5 )
    #cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1,70),(2,150)], columnSpacing=[(1,0), (2,2)] ) 
    cmds.textFieldGrp( "objectName_grp", label="Butterfly:      ",text=ds.objectName, columnWidth2=[72,144],cc=changeObjectName )
    cmds.setParent("..")
    cmds.setParent("..") 
    cmds.setParent("..")    
    #------------------------------------------------------------------  
    # Rigging
    cmds.frameLayout( 'rigging_fl', collapsable=True, collapse=False, w=230, label="Rigging" )
    cmds.columnLayout( rowSpacing=5, co=['left',5] )
    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1,70),(2,150)], columnSpacing=[(1,0), (2,2)] ) 
    cmds.button( "selectRig_btn", label="Select Rig", height=20, width=70, command=updateMeshField )                 
    cmds.textFieldGrp( "rigName_grp", text=ds.rigName, enable=True )
    cmds.setParent("..")
    cmds.button( "createRig_btn", label="Setup Rig Group", h=30, w=220, c=setupRigGroup ) 
    # cmds.button( "parentRig_btn", label="Parent Rig", en=True, h=30, w=220, command=parentRig ) 
    cmds.text("t1", label="")
    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1,70),(2,146)], columnSpacing=[(1,0), (2,2)] ) 
    cmds.button( "selectPath_grp", label="Select Path", height=20, width=60, command=updatePathField )                 
    cmds.textFieldGrp( "pathName_grp", text=ds.pathName, cc=changePathName )
    cmds.setParent("..")
    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1,200),(2,15)], columnSpacing=[(1,0),(2,5),(3,5)] )
    cmds.button( "attachButterflyToPath_btn", label="Attach Butterfly To Path", h=30, w=200, c=attachButterflyToPath ) 
    cmds.button( "detachFromPath_btn", label="D", en=True, h=30, w=15, command=detachButterflyFromPath )
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.rowColumnLayout( numberOfColumns=2, rowOffset=[1,'top',2], columnWidth=[(1,200),(2,15)], columnSpacing=[(1,6),(2,5),(3,5)] )
    cmds.button( "animate_btn", label="Create Animation", h=30, w=200, command=animate )
    cmds.button( "deleteAnim_btn", label="D", en=True, h=30, w=15, command=deleteAnimations )
    cmds.setParent("..")
    cmds.text("t3", label="")
    cmds.setParent("..")
    cmds.setParent("..")
    #------------------------------------------------------------------  
    # Animation Settings   
    cmds.frameLayout( "animationSettings_fl",collapsable=True, collapse=True, w=230, label="Animation Settings" )
    cmds.columnLayout( rowSpacing=0 )
    cmds.floatFieldGrp( "startTime_grp", label="Start Frame", numberOfFields=1, value1=ds.start, cc=changeStartTime) 
    cmds.floatFieldGrp( "endTime_grp", label="End Frame", enable=True, numberOfFields=1, value1=ds.end,cc=changeEndTime) 
    cmds.floatFieldGrp( "velocity_grp", label="Average Speed (cm/s)", numberOfFields=1, v1=ds.velocity,cc=changeSpeedSetting ) 
    cmds.floatFieldGrp( "cycleRate_grp", label="Wing Cycle Rate", numberOfFields=1, pre=2,v1=ds.wingCycleRate, cc=changeCycleRate)
    cmds.floatFieldGrp( "glide_grp", label="Glide", numberOfFields=1, v1=ds.glide, pre=2,cc=changeGlide  )
    cmds.floatFieldGrp( "roll_grp", label="Roll", numberOfFields=1, v1=ds.roll, pre=2,cc=changeRoll  )
    cmds.floatFieldGrp( "pathUValue_grp",label="Path U Value", pre=3, numberOfFields=1, v1=0.0 ) 
    cmds.setParent("..")
    cmds.setParent("..")
    #------------------------------------------------------------------  
    # Physics Settings   
    cmds.frameLayout( "physicsSettings_fl",collapsable=True, collapse=True, w=230, label="Physics Settings" )
    cmds.columnLayout( rowSpacing=0 )
    cmds.floatFieldGrp( "liftCoefficient_grp", label="Lift Coefficient ", numberOfFields=1, v1=ds.liftCoefficient, cc=changeLiftCoefficient )     
    cmds.floatFieldGrp( "gravity_grp", label="Gravity (cm/s)", numberOfFields=1, v1=ds.g, cc=changeGravity ) 
    cmds.floatFieldGrp( "wingLength_grp", label="Wing Length (cm) ", numberOfFields=1, v1=ds.wingLength, cc=changeWingLength ) 
    cmds.floatFieldGrp( "frameRate_grp", label="Frame Rate ", numberOfFields=1, v1=ds.fps ) 
    cmds.setParent("..")
    cmds.setParent("..")
    #------------------------------------------------------------------  
    # Rig Orientation
    cmds.frameLayout( "rigOrientation_fl",collapsable=True, collapse=True, w=230, label="Rig Orientation" )
    cmds.columnLayout( rowSpacing=0 )
    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1,139),(2,50)],columnSpacing=[(1,0),(2,2)] )
    cmds.text( "frontAxis_txt",align='right',label="Front Axis")
    cmds.optionMenu("frontAxis_menu",cc=changeRigOrientation)
    cmds.menuItem(l='+x',da=0) 
    cmds.menuItem(l='-x',da=1)
    cmds.menuItem(l='+z',da=2)
    cmds.menuItem(l='-z',da=3)
    cmds.setParent("..")     
    cmds.setParent("..")
    cmds.setParent("..")
    #------------------------------------------------------------------  
    # Wing Cycle Settings   
    cmds.frameLayout( "wingCycleSettingsMain_fl",collapsable=True, collapse=False, w=230, label="Wing Cycle" )
    cmds.textFieldGrp( "cycleName_grp", label="Cycle Name  ",text=ds.cycleName, columnWidth2=[72,144],cc=changeCycleName )
    cmds.frameLayout( "wingCycleSettings_fl",collapsable=True, collapse=False, w=230, label="Save A New Wing Cycle" )
    cmds.columnLayout( rowSpacing=5, columnOffset=("both", 5) )
    cmds.button( "selectWings_btn", label="Select Wings", h=30, w=220, c=selectWings )
    cmds.optionMenu("selectCtrl_menu", enable=False, w=220)
    cmds.menuItem('...') 
    cmds.setParent("..")
    cmds.columnLayout( rowSpacing=0 )
    cmds.floatFieldGrp( "wcStart_grp", label="Start Frame", numberOfFields=1, value1=ds.wcStart )
    cmds.floatFieldGrp( "wcEnd_grp", label="End Frame", numberOfFields=1, value1=ds.wcEnd )
    cmds.setParent("..")
    cmds.columnLayout( rowSpacing=5, columnOffset=("both", 5) )
    cmds.button( "saveWingCycle_btn", label="Save Wing Cycle", h=30, w=220, c=saveWingCycle ) 
    cmds.setParent("..")
    cmds.setParent("..")
    #------------------------------------------------------------------ 
    # Progress Bar
    cmds.frameLayout( collapsable=False, collapse=False, w=230, label="Progress Bar"  )
    cmds.textField( "progressUpdate_fld", text=" ... ", width=100)
    cmds.progressBar( "progressControl_grp", maxValue=100, width=220  )             
    cmds.setParent( ".." )
    cmds.setParent( ".." ) 

    updateUI()
    updateCycleButtons()
    cmds.showWindow( "mzButterflyToolWindow" )
#----------------------------------------------------------------------------------------------------
# PROGRESS BAR FUNCTIONS
#----------------------------------------------------------------------------------------------------
def resetProgressBar( args ):
    resetButterflyProgressControl()
def butterflyProgressControl():
    cmds.progressBar("progressControl_grp",edit=True, step=1)
def resetButterflyProgressControl():
    cmds.progressBar("progressControl_grp",edit=True, progress=0)
def setButterflyProgressControlMaxValue( maxValue ):
    cmds.progressBar("progressControl_grp",edit=True, maxValue=maxValue) 
def endButterflyProgressControl():
    maxValue = cmds.progressBar("progressControl_grp",query=True, maxValue=True)  
    progress = cmds.progressBar("progressControl_grp",query=True, progress=True)
    step = maxValue - progress
    cmds.progressBar("progressControl_grp",edit=True, step=step)  
def butterflyProgressUpdate( textUpdate ):
    cmds.textField("progressUpdate_fld",edit=True,text=textUpdate)   
#----------------------------------------------------------------------------------------------------
# MODULE - Dialog Boxes
#----------------------------------------------------------------------------------------------------    
def errorMessage( msg ):
    cmds.confirmDialog( title="mzButterflyTool", message=msg, button="OK", defaultButton="OK", cancelButton="OK", dismissString="OK")
def okDialogBox( msg ):
    cmds.confirmDialog( title=" ", message=msg, button="OK", defaultButton="OK", cancelButton="OK", dismissString="OK")
def yesNoDialogBox( msg ):
    return cmds.confirmDialog( title=" ", message=msg, button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )       
#----------------------------------------------------------------------------------------------------
# UI FUNCTIONS
#----------------------------------------------------------------------------------------------------    
#-----------------------------------------------------------------------------
def checkWorkingUnits():
    workingUnits = cmds.currentUnit( query=True, linear=True )
    if workingUnits != "cm":
        msg = "mzButterflyTool requires Working Units set to centimeter\nSet working units to centimeter?";
        ok = cmds.confirmDialog( title="Working Units", message=msg, button=['Yes','No'], defaultButton="Yes", cancelButton="No", dismissString="No")
        if ok=='Yes':
            cmds.currentUnit( linear="cm") 
        return ok  

def changeObjectName( args ):
    objectName = cmds.textFieldGrp("objectName_grp",query=True,text=True)
    if cmds.objExists(objectName):
        cmds.select(objectName)
        cycleName = updateCycleName()
        if cycleName:
            updateCycle(cycleName)
    updateUI()     

def updateMeshField( args ):
    ui = ButterflyToolUI()
    mesh = selectRig()
    if mesh:
        ui.set_rigName( mesh )
        updateButtons()
        
def updatePathField( args ):
    selection = cmds.ls( sl=True )
    if len(selection) == 0:
        errorMessage("Select a path for the butterfly to follow!")
        return
    if isValidButterflyPath(selection[0]):
        cmds.textFieldGrp( 'pathName_grp', edit=True, text=selection[0] )
        updateSpeedSetting()

def changePathName( args ):
    ui = ButterflyToolUI()
    if cmds.objExists(ui.pathName):
        if isValidButterflyPath(ui.pathName):
            updateSpeedSetting()
    else:
        errorMessage( "Can't find a path called %s" % ui.pathName )            

def updateControlMenu( menuList ):
    oMenu =  cmds.optionMenu( "selectCtrl_menu", query=True, fullPathName=True )
    addItemsToMenu( oMenu, menuList ) 

def selectRig():
    selection = cmds.ls( sl=True )
    if len(selection) == 0:
        errorMessage("Select a butterfly rig node!")
        return None
    return selection[0] 

def changeCycleName( args ):
    cn = ButterflyControlNames() 
    if updateCycle( cn.cycleName ):
        if cmds.objExists( cn.objectName ):
            updateRigCycleName( cn )
    updateUI() 
    updateCycleButtons()
  
def selectWings( args ):
    # uses WingCycleExportAssistant to make sure valid wings are selected
    selection = cmds.ls( sl=True, l=True )
    wcea = WingCycleExportAssistant()
    if wcea.collectRigInfo(selection):
        wcea.collectKeyedNodeNames()
        wingNames = wcea.getWingNames()
        # oMenu = cmds.optionMenu( "selectCtrl_menu", query=True, fullPathName=True )
        #  addItemsToMenu( oMenu,wingNames )
        ui = ButterflyToolUI()
        ui.addItemsToMenu(wingNames)
        butterflyProgressUpdate('... wings have been selected ...')
        updateSaveCycleButton()

def saveWingCycle( arg ):
    success = exportWingCycle()
    if success:
        cn = ButterflyControlNames() 
        if cmds.objExists( cn.objectName ):
            updateRigCycleName(cn)

def changeCycleRate(args):
    objectName = cmds.textFieldGrp( "objectName_grp", query=True, text=True )
    wingCycleRate = cmds.floatFieldGrp("cycleRate_grp",query=True,value1=True)
    if wingCycleRate <= 0.0:
        cmds.setAttr( "%s.cycleRate" % objectName, 0.1 )
        errorMessage('Wing Cycle Rate must be above 0.0')

def limitInput(uiid,lower,upper):
    objectName = cmds.textFieldGrp( "objectName_grp", query=True, text=True )
    fieldValue = cmds.floatFieldGrp("%s_grp"%uiid,query=True,value1=True)
    if lower != None:
        if fieldValue < lower:
            cmds.setAttr("%s.%s"%(objectName,uiid),lower)
    if upper != None:
        if fieldValue > upper:
            cmds.setAttr("%s.%s"%(objectName,uiid),upper)            

def changeGlide(args):
    limitInput('glide',0.0,1.0)

def changeRoll(args):
    limitInput('roll',0.0,3.0)

def changeLiftCoefficient(args):
    limitInput('liftCoefficient',0.0,None)

def changeGravity(args):
    limitInput('gravity',1.0,None)
        
def changeWingLength(args):
    limitInput('wingLength',1.0,None)
      
def changeRigOrientation(args):
    ui = ButterflyToolUI()
    cn = ButterflyControlNames()
    if cmds.objExists( cn.motionPathName ):
        errorMessage('Detach Butterfly From Path to change Front Axis!')
        return
    setRotateControlToFrontAxis(ui,cn)
        
def changeSpeedSetting(args):
    updateTimeRange()
    updatePathAnimation()

def changeStartTime(args):
    start = cmds.floatFieldGrp("startTime_grp",query=True,value1=True )
    end = cmds.floatFieldGrp("endTime_grp",query=True,value1=True )
    if start >= end:
        errorMessage('Start Frame must be before End Frame!')        
        cmds.floatFieldGrp("startTime_grp",edit=True,value1=end-1)
    updateSpeedSetting()
    updatePathAnimation() 
    
def changeEndTime(args):
    start = cmds.floatFieldGrp("startTime_grp",query=True,value1=True )
    end = cmds.floatFieldGrp("endTime_grp",query=True,value1=True )
    if end <= start:
        errorMessage('End Frame must be after Start Frame!')        
        cmds.floatFieldGrp("endTime_grp",edit=True,value1=start+1)
    updateSpeedSetting()
    updatePathAnimation() 
          
def updateTimeRange():
    path = cmds.textFieldGrp("pathName_grp",query=True,text=True) 
    speed = cmds.floatFieldGrp("velocity_grp",query=True,value1=True)
    start = cmds.floatFieldGrp("startTime_grp",query=True,value1=True )
    end = cmds.floatFieldGrp("endTime_grp",query=True,value1=True )
    if cmds.objExists( path ):
        fps = cmds.floatFieldGrp( "frameRate_grp", query=True, v1=True ) 
        pathLength = cmds.arclen( path )
        end = (pathLength/speed) * fps + start
    cmds.floatFieldGrp("endTime_grp",edit=True,v1=end)   
        
def updateSpeedSetting(): 
    start = cmds.floatFieldGrp("startTime_grp",query=True,value1=True )
    end = cmds.floatFieldGrp("endTime_grp",query=True,value1=True )
    path = cmds.textFieldGrp("pathName_grp",query=True,text=True) 
    if cmds.objExists( path ):
        fps = cmds.floatFieldGrp( "frameRate_grp", query=True, v1=True ) 
        pathLength = cmds.arclen( path )
        timeRange = end - start
        speed = pathLength*fps/timeRange
        cmds.floatFieldGrp("velocity_grp",edit=True,value1=speed)

def updatePathAnimation():
    # if Butterfly is attached to the path then update the path uValues
    ui = ButterflyToolUI()
    cn = ButterflyControlNames() 
    if cmds.objExists( cn.pathUValue ): 
        start = ui.start
        end = ui.end
        numberOfKeys = cmds.keyframe(cn.pathUValue,q=True,kc=True)
        if numberOfKeys < 2:
            errorMessage('Missing path U Value keyframes')
            return
        first = cmds.findKeyframe( cn.pathUValue, which='first' )
        last = cmds.findKeyframe( cn.pathUValue, which='last' ) 
        
        # get a list of all keyed nodes
        keyedNodes = []
        keyedNodes.append(ui.objectName)
        descendents = cmds.listRelatives(ui.objectName,allDescendents=True,fullPath=True)
        for node in descendents:
            if cmds.keyframe(node,q=True, kc=True): 
                keyedNodes.append(node) 
                
        # shift the keyframes and then scale them
        ctrls = ui.getWingNameList()
        amount = start - first
        ts = (end-start)/(last-first)
        for node in keyedNodes:
            numberOfKeys = cmds.keyframe(node,q=True,kc=True)
            if numberOfKeys:
                cmds.keyframe( node, t=(first,last), relative=True, timeChange=amount ) 
                cmds.scaleKey( node, t=(first,last), timeScale=ts, timePivot=start, valueScale=1.0, valuePivot=0.0  ) 

def checkAttributes(objectName):
    if not cmds.objExists(objectName):
        return
    ds = DefaultButterflySettings()
    for at in ds.attributes: 
        if ds.type[at] == 'string':
            if not cmds.objExists('%s.%s' % (objectName,at)):
                cmds.addAttr( objectName, ln=at, dt='string')
                cmds.setAttr( "%s.%s" % (objectName,at), edit=True, channelBox=True ) 
        if ds.type[at] == 'key':
            if not cmds.objExists('%s.%s' % (objectName,at)):
                cmds.addAttr( objectName, ln=at,at='double', dv=ds.value[at])
                cmds.setAttr( "%s.%s" % (objectName,at), edit=True, keyable=True ) 
            cmds.connectControl( '%s_grp' % at, '%s.%s' % (objectName,at), index=2 )
        if ds.type[at] == 'nokey':
            if not cmds.objExists('%s.%s' % (objectName,at)):
                cmds.addAttr( objectName, ln=at,at='double', dv=ds.value[at])
                cmds.setAttr( "%s.%s" % (objectName,at), edit=True, cb=True, keyable=False ) 
            cmds.connectControl( '%s_grp' % at, '%s.%s' % (objectName,at), index=2 ) 
    if not cmds.objExists('%s.%s' % (objectName,ds.axis['name'])):
        cmds.addAttr(objectName,ln=ds.axis['name'],at='enum',en=ds.axis['en'])  
        cmds.setAttr('%s.%s' % (objectName,ds.axis['name']), e=True, cb=True ) 
    cmds.connectControl('%s_menu' % ds.axis['name'],'%s.%s' % (objectName,ds.axis['name']) )    

def isAttachedToPath():
    cn = ButterflyControlNames() 
    if cmds.objExists(cn.motionPathName):
        path = cmds.listConnections(cn.motionPathName,type='nurbsCurve') 
        if path:
            return path[0] 
    return False    

def updateRigCycleName(cn):
    global wingCycleFileManager
    loaded = wingCycleFileManager.isLoaded(cn.cycleName)
    if loaded:
        cmds.setAttr(cn.cycleNameAttribute,cn.cycleName,type='string')

def updateCycleName():
    # updates the ui.cycleName from the hidden cycleName attribute
    cn = ButterflyControlNames()
    if cmds.objExists(cn.cycleNameAttribute):
        cycleName = cmds.getAttr(cn.cycleNameAttribute)
        if cycleName:
            cmds.textFieldGrp('cycleName_grp', edit=True, text=cycleName)
            return cycleName    
    return False    

def updateCycle( cycleName ):
    ui = ButterflyToolUI()
    # check for wing cycle data file and load if found
    global wingCycleFileManager
    wc = wingCycleFileManager.getCycle(cycleName)
    if wc:
        keyedNodeNames = wc.keyedNodeNames
        ui.addItemsToMenu( keyedNodeNames )
        ui.set_wcStart( wc.start )
        ui.set_wcEnd( wc.end )
        return True
    else:
        ui.emptyMenu()     
        return False
                     
def updateUI():
    ui = ButterflyToolUI()
    objectName = ui.objectName
    if cmds.objExists( objectName ):
        # make sure object has all attributes
        checkAttributes(objectName)   
        # update rig info
        cn = ButterflyControlNames() 
        cycleName = updateCycleName()
        if cycleName:
            updateCycle(cycleName)
        
        children = cmds.listRelatives(cn.rigGrp,children=True,type='transform',f=True)
        if children:
            cmds.textFieldGrp( "rigName_grp",edit=True,text=children[0] )                
        # update path animation info
        pathName = isAttachedToPath()
        if pathName:
        #if cmds.objExists( pathName ):
            cmds.textFieldGrp("pathName_grp",edit=True,text=pathName)
            path_uValue = "%s.pathUValue" % objectName
            if cmds.objExists( path_uValue ):
                numberOfKeys = cmds.keyframe(path_uValue,q=True,kc=True)
                if numberOfKeys >= 2:
                    firstKeyframe = cmds.findKeyframe( path_uValue, which='first' )
                    lastKeyframe = cmds.findKeyframe( path_uValue, which='last' )
                    cmds.floatFieldGrp( "startTime_grp", edit=True, v1=firstKeyframe)
                    cmds.floatFieldGrp( "endTime_grp", edit=True, v1=lastKeyframe)
            updateSpeedSetting()
        cn = ButterflyControlNames() 
        try:
            numberOfKeys = cmds.keyframe(cn.getMovementControlName(),q=True,kc=True)
            if numberOfKeys:
                lastKeyframe = cmds.findKeyframe( cn.getMovementControlName(), which='last' )
                cmds.floatFieldGrp("endTime_grp",edit=True,v1=lastKeyframe)  
        except:
            errorMessage('Found %s. But rig setup is incorrect!' % objectName) 
            resetButtons()
            return                
    else:
        ds = DefaultButterflySettings()
        cmds.textFieldGrp("pathName_grp",edit=True,text=ds.pathName) 
    updateButtons()

def resetButtons():
    cmds.button("createRig_btn",edit=True,bgc=(0.365,0.365,0.365))  
    # cmds.button("parentRig_btn",edit=True,bgc=(0.365,0.365,0.365))    
    cmds.button("attachButterflyToPath_btn",edit=True,bgc=(0.365,0.365,0.365)) 
    cmds.button("animate_btn",edit=True,bgc=(0.365,0.365,0.365)) 
    cmds.button("selectWings_btn",edit=True,bgc=(0.365,0.365,0.365))
    cmds.button("saveWingCycle_btn",edit=True,bgc=(0.365,0.365,0.365))        
    cmds.frameLayout( 'rigging_fl',edit=True, collapse=False ) 
    cmds.frameLayout("animationSettings_fl",edit=True,collapse=True)       

def updateSaveCycleButton():
    ui = ButterflyToolUI()
    oMenu = ui.getMenuItems()
    if oMenu:
        cmds.button("selectWings_btn",edit=True,bgc=(0.365,0.365,0.365)) 
        cmds.button("saveWingCycle_btn",edit=True,bgc=(0.1,0.5,0.3))         
    else:
        cmds.button("selectWings_btn",edit=True,bgc=(0.1,0.5,0.3))      
    
def updateCycleButtons():
    ui = ButterflyToolUI()
    global wingCycleFileManager
    if wingCycleFileManager.isLoaded(ui.cycleName):
        cmds.frameLayout( "wingCycleSettings_fl",edit=True,collapse=True )
        cmds.button("selectWings_btn",edit=True,bgc=(0.365,0.365,0.365))
        cmds.button("saveWingCycle_btn",edit=True,bgc=(0.365,0.365,0.365))   
    else:
        cmds.frameLayout( "wingCycleSettings_fl",edit=True,collapse=False )
        oMenu = ui.getMenuItems()
        if oMenu:
            cmds.button("selectWings_btn",edit=True,bgc=(0.365,0.365,0.365)) 
            cmds.button("saveWingCycle_btn",edit=True,bgc=(0.1,0.5,0.3))         
        else:
            cmds.button("selectWings_btn",edit=True,bgc=(0.1,0.5,0.3))    

def updateButtons():
    ui = ButterflyToolUI()
    resetButtons()    
    # find which button should be green
    if not cmds.objExists( ui.objectName ):
        cmds.button("createRig_btn",edit=True,bgc=(0.1,0.5,0.3))      
        return    
    cn = ButterflyControlNames()
    if not cmds.objExists( cn.motionPathName ):
        cmds.button("attachButterflyToPath_btn",edit=True,bgc=(0.1,0.5,0.3)) 
        return
    cmds.frameLayout( 'rigging_fl',edit=True, collapse=True )       
    if not ui.wingNameList:
        cmds.button("selectWings_btn",edit=True,bgc=(0.1,0.5,0.3)) 
        return
    cmds.frameLayout("animationSettings_fl",edit=True,collapse=False)         
    cmds.button("animate_btn",edit=True,bgc=(0.1,0.5,0.3)) 
#----------------------------------------------------------------------------------------------------
# USEFULL FUNCTIONS
#----------------------------------------------------------------------------------------------------    
def checkTypeIs(node,testType):
    node_type = cmds.objectType( node )
    if node_type == testType:
        return True
    shape = cmds.listRelatives(node,s=True)    
    if shape:
        type = cmds.nodeType(shape[0])
        if testType == type:
            return True
    return False               

def angleBetweenVectors(vecTo,vecFrom):
    v1 = om.MVector(vecFrom.x,0,vecFrom.z)
    v2 = om.MVector(vecTo.x,0,vecTo.z)
    a = cmds.angleBetween(euler=False,v1=v1,v2=v2)
    # get direction by y axis value a[1] * angle a[3]
    angle = a[1]*a[3]
    return angle

def getVectorBetweenJoints(jnt1,jnt2):
    v1 = cmds.xform( jnt1,q=True, rp=True, ws=True )
    v2 = cmds.xform( jnt2,q=True, rp=True, ws=True )
    vec = om.MVector(v2[0],v2[1],v2[2])-om.MVector(v1[0],v1[1],v1[2])
    return vec 
    
def isInList(item,list):
    for n in list:
        if item == n:
            return True
    return False
        
def getItemInListWithHighestValue(list):
    highest = list[0]
    item = 0
    for i in range(1,len(list)):
        if list[i] > highest:
            highest = list[i]
            item = i
    return item
        
def createKeyframe(key):
    cmds.setKeyframe( key.name, attribute=key.at,v=key.v,t=key.t,itt=key.itt,ott=key.ott)
    
def getDAGPath( mesh ):
    try:
        selectionList = om.MSelectionList()
        selectionList.add( mesh )
        nodeDagPath = selectionList.getDagPath(0)
    except:
        raise RuntimeError('could node find dag path for %s' % mesh)
    return nodeDagPath
#-----------------------------------------------------------
# CLASSES
#-----------------------------------------------------------       
class DefaultButterflySettings:
    def __init__(self):
        self.objectName = 'butterfly1'
        self.folder = 'data'
        self.rigName = '...'
        self.pathName = '...'
        self.cycleName = '...'
        self.velocity = 100.0 
        self.wingCycleRate = 1.0
        self.glide = 0.5
        self.roll = 1.0
        self.liftCoefficient = 1.0
        self.wingLength = 5.0    # cm
        self.pathUValue = 0.0 
        self.fps = 30.0
        self.g = 980.0        # gravity
        self.wcStart = 100.0
        self.wcEnd = 150.0
        self.start = 300.0
        self.end = 450.0 #1000.0
        self.avg = 150.0
        self.attributes = ['cycleRate','glide','roll','pathUValue','liftCoefficient','gravity',
                           'wingLength','frameRate','cycleName']
        self.type = {'cycleRate':'key','glide':'key','roll':'key','pathUValue':'key',
                     'liftCoefficient':'key','gravity':'key','wingLength':'key',
                     'frameRate':'nokey','cycleName':'string'}
        self.axis = {'name':'frontAxis','en':'+x:-x:+z:-z'}
        self.value = {'cycleRate':self.wingCycleRate,'glide':self.glide,'roll':self.roll,
                      'pathUValue':self.pathUValue,'liftCoefficient':self.liftCoefficient,
                      'gravity':self.g,'wingLength':self.wingLength,'frameRate':self.fps}
        self.maxPitchRot = 35.0  # butterfly rotation when flying upwards 
        self.maxCycleRot = 15.0  # butterfly rotation during a wing cycle 
        self.maxBrakeRot = 90.0           

       
class ButterflyToolUI:
    'settings for each individual Butterfly'
    def __init__(self):        
        self.objectName = cmds.textFieldGrp( "objectName_grp", query=True, text=True )
        self.cycleName = cmds.textFieldGrp( "cycleName_grp", query=True, text=True )
        self.rigName = cmds.textFieldGrp( "rigName_grp", query=True, text=True )
        self.pathName = cmds.textFieldGrp( "pathName_grp", query=True, text=True )
        self.wcStart = cmds.floatFieldGrp( "wcStart_grp", query=True, v1=True )
        self.wcEnd = cmds.floatFieldGrp( "wcEnd_grp", query=True, v1=True )
        self.wingNameList = self.getWingNameList()        
        self.start = cmds.floatFieldGrp( "startTime_grp", query=True, v1=True )
        self.end =  cmds.floatFieldGrp( "endTime_grp", query=True, v1=True )
        self.velocity = cmds.floatFieldGrp( "velocity_grp", query=True, v1=True )
        self.wingCycleRate = 1.0/cmds.floatFieldGrp( "cycleRate_grp", query=True, v1=True )
        self.glide = cmds.floatFieldGrp( "glide_grp", query=True, v1=True )
        self.roll = cmds.floatFieldGrp( "roll_grp",query=True,v1=True )
        self.liftCoefficient = cmds.floatFieldGrp( "liftCoefficient_grp", query=True, v1=True )
        self.wingLength = cmds.floatFieldGrp( "wingLength_grp", query=True, v1=True )
        self.g = cmds.floatFieldGrp( "gravity_grp", query=True, v1=True )
        self.fps = cmds.floatFieldGrp( "frameRate_grp", query=True, v1=True )

    def set_pathName(self,pathName):
        self.pathName = pathName
        cmds.textFieldGrp( "pathName_grp",edit=True,text=pathName ) 

    def set_rigName( self,rigName ):
        self.rigName = rigName
        cmds.textFieldGrp( "rigName_grp",edit=True,text=rigName ) 
        
    def set_wcStart(self,cycleStart):
        cmds.floatFieldGrp( "wcStart_grp", edit=True, v1=cycleStart )
        self.wcStart = cycleStart

    def set_wcEnd(self,cycleEnd):
        cmds.floatFieldGrp( "wcEnd_grp", edit=True, v1=cycleEnd )
        self.wcEnd = cycleEnd
        
    def emptyMenu( self ):
        # delete existing menus in the optionMenu
        oMenu = cmds.optionMenu( "selectCtrl_menu", query=True, fullPathName=True )
        items = cmds.optionMenu(oMenu, q=True, ill=True)
        if items:
            for item in items : 
                cmds.deleteUI(item)
        cmds.optionMenu( oMenu, e=True, enable=False )         
                
    def getMenuItems( self ):
        oMenu = cmds.optionMenu( "selectCtrl_menu", query=True, fullPathName=True )
        items = cmds.optionMenu(oMenu, q=True, ill=True)
        menuItemList = []
        if items:
            for n in range(1,len(items)):
                itemName = cmds.menuItem( items[n], query=True,  label=True )
                menuItemList.append( itemName )
        return menuItemList    

    def addItemsToMenu( self, menuList ):
        oMenu = cmds.optionMenu( "selectCtrl_menu", query=True, fullPathName=True )
        # delete existing menus in the optionMenu
        self.emptyMenu()
        # add selected items to the menu
        cmds.menuItem( label="... selected ...", parent=oMenu )
        for item in menuList:
            cmds.menuItem(label=item, enable=False, parent=oMenu)
        cmds.optionMenu( oMenu, e=True, enable=True )  
        
    def getWingNameList(self):
        return self.getMenuItems()

    def getFrontAxisId(self):
        return cmds.optionMenu( "frontAxis_menu", query=True, sl=True ) - 1
                
    def getFrontAxis(self):
        frontAxis = cmds.optionMenu( "frontAxis_menu", query=True, sl=True )
        if frontAxis == 1:              #'+x'
            return 'x',False
        elif frontAxis == 2:            #'-x'
            return 'x',True
        elif frontAxis == 3:            #'+z'
            return 'z',False
        elif frontAxis == 4:            #'-z'
            return 'z',True 

    def getFrontAxisVector(self):
        frontAxis = cmds.optionMenu( "frontAxis_menu", query=True, sl=True )
        if frontAxis == 1:              #'+x'
            return om.MVector(1,0,0)
        elif frontAxis == 2:            #'-x'
            return om.MVector(-1,0,0)
        elif frontAxis == 3:            #'+z'
            return om.MVector(0,0,1)
        elif frontAxis == 4:            #'-z'
            return om.MVector(0,0,-1)    

    def getPitchAxis(self):
        frontAxis = cmds.optionMenu( "frontAxis_menu", query=True, sl=True )
        if frontAxis == 1:              #'+x'
            return 1.0,'rotateZ'
        elif frontAxis == 2:            #'-x'
            return -1.0,'rotateZ'
        elif frontAxis == 3:            #'+z'
            return -1.0,'rotateX'
        elif frontAxis == 4:            #'-z'
            return 1.0,'rotateX'             
                
    def display(self):
        print ("%s ----------" % self.objectName )
        print ("Start Frame: %f" % self.wcStart)
        print ("   Duration: %f" % self.wcEnd)
        print ("Controls:")
        for n in self.wingNameList:
            print ("\t%s" % n)  


class ButterflyControlNames:
    def __init__(self):
        ui = ButterflyToolUI()
        ds = DefaultButterflySettings()
        self.objectName = ui.objectName
        self.meshGrp = '%s_mesh' % ui.objectName
        self.rigGrp = '%s_rig' % ui.objectName
        self.controlGrp = '%s_controls' % ui.objectName
        self.controlLayer = 'butterfly_ctrls_L'
        self.pathName = '%s_path' % ui.objectName
        self.pathUValue = '%s.pathUValue' % ui.objectName
        self.motionPathName = '%s_mPath' % ui.objectName   # motion path names
        self.rigConstraint = '%s_rigParent' % ui.objectName 
        self.cycleName = ui.cycleName
        self.cycleNameAttribute = '%s.cycleName' % ui.objectName
        self.motionPathCtrl = 'movement_ctrl'
        self.rotateCtrl = 'rotate_ctrl'

    def getMovementControlName(self):
        return '%s|%s|%s' % (self.objectName,self.controlGrp,self.motionPathCtrl)

    def getRotateControlName(self):
        pathCtrlName = self.getMovementControlName()
        return '%s|%s' % (pathCtrlName,self.rotateCtrl)   
        
                  
class PathManager:
    def __init__(self):
        self.ui = ButterflyToolUI()
        self.cn = ButterflyControlNames()
        pathName = self.ui.pathName
        self.count = 0
        nodeDagPath = getDAGPath( pathName )
        self.crvFn = om.MFnNurbsCurve(nodeDagPath)
        self.pathLength = self.crvFn.length()
        self.distance = 0.0
        self.position = self.getPathStartPosition()
        self.direction = self.getPathStartDirection()

    def setPathPositionToTime(self,t):
        uValue = cmds.getAttr(self.cn.pathUValue,t=t)
        self.distance = self.getDistanceAtPathUValue(uValue)
        parameter = self.crvFn.findParamFromLength(self.distance)
        self.position = self.crvFn.getPointAtParam(parameter, om.MSpace.kWorld) 
        self.direction = self.crvFn.tangent(parameter, om.MSpace.kWorld)
          
    def getPathStartPosition(self):
        parameter = self.crvFn.findParamFromLength(0.0)
        return self.crvFn.getPointAtParam(parameter, om.MSpace.kWorld) 
    
    def getPathStartDirection(self):  # d is distance along the path
        parameter = self.crvFn.findParamFromLength(0.0)
        return self.crvFn.tangent(parameter, om.MSpace.kWorld)
                
    def getPathPosition(self):  # d is distance along the path
        return self.position
        
    def getPathDirection(self):
        return self.direction
        
    def getPathDistance(self):
        return self.distance    
        
    def getPathUValue(self):
        uValue = self.distance/self.pathLength
        return uValue

    def getDistanceAtPathUValue(self,uValue):
        return uValue*self.pathLength
        
    def getPathDistanceAtTime(self,t):
        uValue = cmds.getAttr(self.cn.pathUValue,t=t)
        return self.getDistanceAtPathUValue(uValue)
        
    def getPathPositionAtTime(self,t):
        uValue = cmds.getAttr(self.cn.pathUValue,t=t) 
        d = self.getDistanceAtPathUValue(uValue) 
        return self.getPathPositionAtDistance(d)
        
    def getPathDirectionAtTime(self,t):
        uValue = cmds.getAttr(self.cn.pathUValue,t=t) 
        d = self.getDistanceAtPathUValue(uValue) 
        parameter = self.crvFn.findParamFromLength(d)
        return self.crvFn.tangent(parameter, om.MSpace.kWorld)

    def getPathPositionAtDistance(self,d):
        parameter = self.crvFn.findParamFromLength(d)
        return self.crvFn.getPointAtParam(parameter, om.MSpace.kWorld) 
 
    def getPathDirectionAtDistance(self,d):
        parameter = self.crvFn.findParamFromLength(d)
        return self.crvFn.tangent(parameter, om.MSpace.kWorld)

    def getPathVelocityAtTime(self,t):
        # returns velocity in cm/fr
        dt = 0.1
        uValue1 = cmds.getAttr(self.cn.pathUValue,t=t)
        d1 = self.getDistanceAtPathUValue(uValue1)
        if uValue1 >= 1.0:
            uValue2 = cmds.getAttr(self.cn.pathUValue,t=t-dt)
            d2 = self.getDistanceAtPathUValue(uValue2)
        else:
            uValue2 = cmds.getAttr(self.cn.pathUValue,t=t+dt)
            d2 = self.getDistanceAtPathUValue(uValue2)
        return (abs(d2-d1)/dt) 
                               
    def moveAlongPath(self,d):  # d is distance along the path
        self.distance = self.distance + d
        parameter = self.crvFn.findParamFromLength(self.distance)
        self.position = self.crvFn.getPointAtParam(parameter, om.MSpace.kWorld) 
        self.direction = self.crvFn.tangent(parameter, om.MSpace.kWorld)
        if self.distance >= self.pathLength:
            return True    # return True when end of path is reached
        return False


class KeyFrame:
    'object used to contain all KeyFrame info for a single Keyframe'
    def __init__(self,name,at,t,value,itt='spline',ott='spline'):
        self.name = name
        self.at = at
        self.t = t
        self.v = value
        self.itt = itt
        self.ott = ott
        
    def toJson(self):
        str = ('{"name": "%s", "at": "%s", "t": %f, "v": %f, "itt":"%s", "ott":"%s"}' 
                % (self.name,self.at,self.t,self.v,self.itt,self.ott))
        return str
       
    def display(self):
        print( "KeyFrame('%s','%s',%s,%s,%s,%s)" % (self.name,self.at,self.t,self.v,self.itt,self.ott))


class uValueKey:
    'for temporary storage of uValue keyframe info'
    def __init__(self,t,value,itt,ott):
        self.t = t
        self.value = value
        self.itt = itt
        self.ott = ott
              

class WingAttributeInfo:
    """ used by WingInfoExportAssistant to extract keyframe info for individual wing attributes """
    def __init__(self,attr):
        self.attr = attr
        self.keyframes = []     # all keyframes for this attribute
        self.max = 0.0          # rotation angle at top of cycle
        self.min = 0.0          # rotation angle at bottom of cycle
        self.rotRange = 0.0     # rotation angle between maxRot and minRot 
        self.tMax = 0.0         # cycle time when rotation is at top of cycle
        self.tMin = 0.0         # cycle time when rotation is at bottom of cycle

    def collectAttributeInfo(self): 
        if len(self.keyframes) < 2:
            return    
        # extracts keyframe range info for this attribute
        self.max = self.keyframes[0].v
        self.min = self.keyframes[0].v
        self.tMax = self.keyframes[0].t
        self.tMin = self.keyframes[0].t
        for key in self.keyframes:
            if key.v > self.max:
                self.max = key.v
                self.tMax = key.t
            if key.v < self.min:
                self.min = key.v
                self.tMin = key.t
        self.rotRange = self.max - self.min

    def reverse(self):
        max = self.max
        self.max = self.min
        self.min = max
        tMax = self.tMax
        self.tMax = self.tMin
        self.tMin = tMax      
        
class WingInfoAssistant:
    """ used to extract keyframe info for an individual wing """
    def __init__(self,wingName):
        self.name = wingName
        self.xRot = WingAttributeInfo('rotateX')
        self.yRot = WingAttributeInfo('rotateY')
        self.zRot = WingAttributeInfo('rotateZ')
        self.mainAxis = ''

    def findMainRotationAxis(self):
        self.xRot.collectAttributeInfo()
        self.yRot.collectAttributeInfo()
        self.zRot.collectAttributeInfo()
        item = getItemInListWithHighestValue([self.xRot.rotRange,self.yRot.rotRange,self.zRot.rotRange])
        if item == 0: 
            self.mainAxis = 'rotateX'
        elif item == 1:
            self.mainAxis = 'rotateY'
        elif item == 2:
            self.mainAxis = 'rotateZ' 
            
    def getMainAxisAttributeInfo(self):
        if self.mainAxis == 'rotateX':
            return self.xRot
        elif self.mainAxis == 'rotateY':
            return self.yRot
        else: 
            return self.zRot                     


class Wing:
    """ container for individual wing info used when gliding """
    def __init__(self,name):
        self.name = name
        self.at = []       # rotateX, rotateY, rotateZ
        self.rMax = []     # rotation angle at top of cycle
        self.rMin = []     # rotation angle at bottom of cycle
        self.rRange = []   # rotation angle between maxRot and minRot

    def toJson(self):
        str = '{"name":"%s", "at":' % self.name
        str = str + json.dumps(self.at) + ', "rMax":'
        str = str + json.dumps(self.rMax) + ', "rMin":' 
        str = str + json.dumps(self.rMin) + ', "rRange":'
        str = str + json.dumps(self.rRange) + '}'
        return str
 
    def loadFromJson(self,data):
        self.name = data["name"]
        self.at = data["at"]
        self.rMax = data["rMax"]
        self.rMin = data["rMin"]
        self.rRange = data["rRange"]
                        
    def display(self):
        print ('Wing: %s -----------' % self.name)
        print (self.at)
        print ('rMax:')
        print (self.rMax)
        print ('rMin:')
        print (self.rMin)
        print ('rRange')
        print (self.rRange)  


class WingInfo:
    """ container for all wing info used when gliding """
    def __init__(self):
        self.wings = []    # Wing class objects
        self.tMax = 0.0    # cycle time (0->1) of main wing maximum rotation
        self.tMin = 0.0    # cycle time (0->1) of main wing minimum rotation
        self.mainWingName = ''       # main wing in self.wings
        self.mainWingAttribute = ''  # main wing rotation axis
  
    def getMainWingRotationInfo(self):
        return self.getWingInfo(self.mainWingName,self.mainWingAttribute)
   
    def getWingInfo(self,wingName,at):
        for wing in self.wings:
            if wing.name == wingName:
                for n in range(len(wing.at)):
                    if wing.at[n] == at:
                        return wing.rMax[n],wing.rMin[n]

    def collectInfo(self,wingNames,start,end):
        rotationAttributes = ['rotateX','rotateY','rotateZ']
        t0 = self.tMax*(end-start) + start
        t1 = self.tMin*(end-start) + start
        for wingName in wingNames:
            wing = Wing(wingName)
            for attr in rotationAttributes:
                wing.at.append(attr)
                rMax = cmds.getAttr('%s.%s' % (wingName,attr),t=t0)
                rMin = cmds.getAttr('%s.%s' % (wingName,attr),t=t1)
                wing.rMax.append(rMax)
                wing.rMin.append(rMin)
                wing.rRange.append(rMax-rMin)
            self.wings.append(wing)

    def toJson(self):
        str = '{"wings":[' + self.wings[0].toJson()
        for w in range(1,len(self.wings)):
            str = str + ',' + self.wings[w].toJson()
        str = str + '], "tMax": %f,' % self.tMax
        str = str + ' "tMin": %f,' % self.tMin
        str = str + ' "mainWingName":"%s",' % self.mainWingName
        str = str + ' "mainWingAttribute":"%s" }' % self.mainWingAttribute
        return str

    def loadFromJson(self,data):
        self.wings = []
        for w in data["wings"]:
            wing = Wing('')
            wing.loadFromJson(w)
            self.wings.append( wing )
        self.tMax = data["tMax"]
        self.tMin = data["tMin"]
        self.mainWingName = data["mainWingName"]
        self.mainWingAttribute = data["mainWingAttribute"]
      
    def display(self):
        print ('------------ WingInfo --------------')
        print ('tMax: %0.2f   tMin: %0.2f' % (self.tMax,self.tMin))
        print ('mainWingName: %s' % self.mainWingName)
        print ('mainWingAttribute: %s' % self.mainWingAttribute)
        for wing in self.wings:
            wing.display()  
            

class WingCycleExportAssistant:
    """ Interface for validating wing cycle info before saving to file """
    def __init__(self):
        self.grpName = ''
        self.cycleName = ''
        self.start = 0
        self.end = 0 
        self.duration = 0
        self.wingNames = []
        self.keyedNodeNames = []
        self.keys = []
        self.keysSorted = []
        self.wingInfo = WingInfo()

    def getKeyedNodeNames(self):
        return self.keyedNodeNames
        
    def getWingNames(self):
        return self.wingNames    

    def setCycleName(self,cycleName):
        # self.grpName = grpName
        self.cycleName = cycleName

    def setCycleInfo(self,start,end):
        self.start = start
        self.end = end
        self.duration = end - start

    def addKeyframe(self,key):
        self.keys.append(key)

    def collectRigInfo(self,selection): 
        if len(selection) == 0: 
           errorMessage ('No rig has been selected!') 
           return False
        if not cmds.objExists(selection[0]): 
            errorMessage('Select a rig to copy from!')
            return False      
        # find the butterfly group name (root parent of selected wings)      
        allParents = cmds.listRelatives(selection[0],ap=True,f=True)
        if allParents:
            rootParent = allParents[0].split('|')[1:][0]    
        else:
            rootParent = selection[0]  
        self.butterflyName = allParents[0].split('|')[1:][0]  
        # make sure the user has selected valid wing nodes   
        if not self.validWings(selection):
            errorMessage('Selected wings are not valid wing nodes!')
            return False 
        for n in selection:
            self.wingNames.append(n)  
        return True       

    def collectWingInfo(self):
        wingInfoAssistants = []        # WingInfoAssistant class for each wing name
        for wingName in self.wingNames:
            wia = WingInfoAssistant(wingName)
            wingInfoAssistants.append(wia)
        
        # separate all keyframes into each wing.attribute            
        for wing in wingInfoAssistants:
            for k in self.keys:
                if k.name == wing.name:
                    if k.at == 'rotateX':
                        wing.xRot.keyframes.append(k)
                    if k.at == 'rotateY':
                        wing.yRot.keyframes.append(k)
                    if k.at == 'rotateZ':
                        wing.zRot.keyframes.append(k) 

        # find the main wing and main attribute and save wingInfo
        mainWing = ''
        maxRange = 0.0
        mainWingAttributeInfo = 0
        for wing in wingInfoAssistants:
            wing.findMainRotationAxis()  # analyzes keyframe info to find main axis for this wing
            wingAttributeInfo = wing.getMainAxisAttributeInfo()        
            if wingAttributeInfo.rotRange > maxRange:
                self.checkJointOrientation(wing,wingAttributeInfo)    
                if wingAttributeInfo.tMax == 0: # main wing movement must start at cycle time 0.0
                    mainWing = wing.name
                    mainWingAttributeInfo = wingAttributeInfo
                    maxRange = wingAttributeInfo.rotRange
        if mainWing == '':
            errorMessage('Unable to collect Wing keyframes! Check the Wing Cycle')
            return False            
        self.wingInfo.mainWingName = mainWing
        self.wingInfo.mainWingAttribute = mainWingAttributeInfo.attr    
        self.wingInfo.tMax = mainWingAttributeInfo.tMax
        self.wingInfo.tMin = mainWingAttributeInfo.tMin
        # collect wing rotation information for all the wings
        self.wingInfo.collectInfo(self.wingNames,self.start,self.end)
        return True
 
    def validWings(self,selection):
        rotationAttributes = ['rotateX','rotateY','rotateZ']
        for wing in selection:
            for at in rotationAttributes:
                keycount = cmds.keyframe(wing,q=True,at=at,kc=True)
                if keycount >= 2:
                    return True
            errorMessage( '%s has less then 2 rotation keyframes' % wing)
            return False
           
    def collectKeyedNodeNames(self):
        descendents = cmds.listRelatives(self.butterflyName,allDescendents=True,fullPath=True)
        for n in descendents:
            if cmds.keyframe(n,q=True, kc=True): 
                self.keyedNodeNames.append(n) 
        return self.keyedNodeNames   

    def checkJointOrientation(self,wing,wingAttributeInfo):
        t = cmds.currentTime(q=True)
        wingName = wing.name
        attr = wingAttributeInfo.attr
        start = self.start
        end = self.end
        tMax = wingAttributeInfo.tMax*(end-start) + start
        tMin = wingAttributeInfo.tMin*(end-start) + start
        cmds.currentTime(tMax)
        children = cmds.listRelatives(wingName,children=True,f=True)
        dyMax = getVectorBetweenJoints(wingName,children[0])[1]
        cmds.currentTime(tMin)
        dyMin = getVectorBetweenJoints(wingName,children[0])[1]
        if dyMin > dyMax:
            wingAttributeInfo.reverse()
        cmds.currentTime(t)

    def sort(self,item):
        """ sorts keyframes by key time """
        if len(self.keysSorted) == 0:
            self.keysSorted.append( item )
            return
        n = 0
        for i,k in enumerate(self.keysSorted):
            if item.t <= k.t:
                self.keysSorted.insert( i, item )
                return
        # if item has not been inserted, add to end of list        
        self.keysSorted.append( item )          

    def sortKeyframes(self):
        """ sorts keyframes by key time """
        for k in self.keys:
            # k.name = k.name.replace(self.grpName,self.cycleName,1)
            self.sort( k )
        
    def getWingCycleInfoForExport(self):
        wingCycleInfo = WingCycleInfo()
        wingCycleInfo.start = self.start
        wingCycleInfo.end = self.end
        # save wingNames using cycleName
        for wingName in self.wingNames:
            # name = wingName.replace(self.grpName,self.cycleName,1) 
            # wingCycleInfo.wingNames.append(name)
            wingCycleInfo.wingNames.append(wingName)
        # save keyedNodeNames using cycleName
        for keyedNodeName in self.keyedNodeNames:
            # name = keyedNodeName.replace(self.grpName,self.cycleName,1)
            # wingCycleInfo.keyedNodeNames.append(name) 
            wingCycleInfo.keyedNodeNames.append(keyedNodeName) 
        # sorts keyframes by time
        self.sortKeyframes()
        wingCycleInfo.keys = self.keysSorted
        wingCycleInfo.wingInfo = self.wingInfo
        return wingCycleInfo


class WingCycleInfo:
    def __init__(self):
        self.start = 0
        self.end = 0
        self.wingNames = []
        self.keyedNodeNames = []
        self.keys = []
        self.wingInfo = None

    def getWingNameList(self):
        return self.wingNames

    def toJson(self):
        str = '{"start": %i, "end": %i, "wingNames":' % (self.start,self.end)
        str = str + json.dumps(self.wingNames) + ', "keyedNodeNames":'
        str = str + json.dumps(self.keyedNodeNames) + ',"keys":['   # self.wingNames
        str = str + self.keys[0].toJson() 
        for k in range(1,len(self.keys)):
            str = str + ',' + self.keys[k].toJson()    
        str = str + '], "wingInfo":' + self.wingInfo.toJson() + '}' 
        return json.loads(str) # return as json
    
    def loadFromJson(self,data):
        self.start = data["start"]
        self.end = data["end"]
        self.wingNames = data["wingNames"]
        self.keyedNodeNames = data["keyedNodeNames"]
        self.keys = []
        for k in data["keys"]:
            self.keys.append(KeyFrame(k["name"],k["at"],k["t"],k["v"],k["itt"],k["ott"]) )
        self.wingInfo = WingInfo()
        self.wingInfo.loadFromJson( data["wingInfo"] )        

    def display(self):
        print ('-- WingCycleInfo --')
        print ('start: %f' % self.start)
        print ('end:   %f' % self.end)
        print ('wingNames:')
        print (self.wingNames)
        print ('keyedNodeNames')
        print (self.keyedNodeNames)
        print ('keys:')
        for key in self.keys:
            key.display()
        if self.wingInfo:    
            self.wingInfo.display()
        else:
            print ('wingInfo = None')    


class WingCycle:
    """ Interface for extracting keyframe info from wingCycleKeyframeInfo object """
    def __init__(self,wcInfo): 
        self.start = wcInfo.start
        self.end = wcInfo.end
        self.keys = wcInfo.keys             # list of keys
        self.numberOfKeys = len(self.keys)
        self.next = 0                     # pointer to next keyframe
        self.moreKeys = True
        self.wingNames = wcInfo.wingNames
        self.keyedNodeNames = wcInfo.keyedNodeNames
        self.wingInfo = wcInfo.wingInfo

    def isAWing(self,name):
        for wingName in self.wingNames:
            if wingName == name:
                return True
        return False
        
    def startNewCycle(self):
        self.next = 0
       
    def getNextKeyTime(self):
        return self.keys[self.next].t
      
    def getNextKeyframes(self,cycleTime):
        keys = []
        t = self.getNextKeyTime()
        while self.moreKeys and t <= cycleTime:    
            try:
                keys.append( self.keys[self.next] )
            except:
                print ('next: %i   numberOfKeys: %i' % (self.next,self.numberOfKeys))
                raise IndexError    
            self.next += 1 
            if self.next == self.numberOfKeys:
                self.next = 0
                break
            t = self.getNextKeyTime()
        return keys

    def display(self):
        print ('------ WingCycle ------')
        print (self.wingNames)
        print (self.keyedNodeNames)
        print ('-- mainWing: %s.%s' % (self.wingInfo.mainWingName,self.wingInfo.mainWingAttribute))
        max,min = self.wingInfo.getWingInfo(self.wingInfo.mainWingName,self.wingInfo.mainWingAttribute)
        print ('-- tMax: %0.2f   tMin: %0.2f' % (self.wingInfo.tMax,self.wingInfo.tMin))
        print ('-- max: %0.2f   min: %0.2f' % (max,min))
        self.wingInfo.display()
        


class ButterflyInfo:
    def __init__(self,rig):
        self.rig = rig

    def getAttachedMeshNames(self):
        attachedMeshNames = []
        rigNodes = cmds.listRelatives(self.rig,allDescendents=True,fullPath=True) 
        rigNodes.append(self.rig)   
        skinClusters = self.getSkinClusters(rigNodes)
        for item in skinClusters:
            meshName = self.getMeshName(item)
            if meshName not in rigNodes:
                attachedMeshNames.append(meshName)
        return attachedMeshNames   
        
    def getMeshLength(self,frontAxis):
        boundingBoxes = []
        # rigNodes = cmds.listRelatives(self.rig,allDescendents=True,fullPath=True) 
        rigNodes = cmds.ls(self.rig,dag=True,ap=True)  
        skinClusters = self.getSkinClusters(rigNodes)
        for item in skinClusters:
            meshName = self.getMesh(item)
            if meshName:
                bb = cmds.polyEvaluate(meshName,b=True)
                boundingBoxes.append(bb)
        return self.getLengthFromBoundingBoxes(boundingBoxes,frontAxis)     

    def getRigLength(self,frontAxis):
        jntNames = cmds.ls(self.rig,dag=True,ap=True,type='joint')
        if jntNames:
            pos = cmds.joint(jntNames[0],q=True,p=True,a=True)
            bb = [[pos[0],pos[0]],[pos[1],pos[1]],[pos[2],pos[2]]]
            for jnt in jntNames:
                p = cmds.joint(jnt,q=True,p=True,a=True)
                if p[0] < bb[0][0]:
                    bb[0][0] = p[0]
                if p[0] > bb[0][1]:
                    bb[0][1] = p[0]
                if p[1] < bb[1][0]:
                    bb[1][0] = p[1]
                if p[1] > bb[1][1]:
                    bb[1][1] = p[1]
                if p[2] < bb[2][0]:
                    bb[2][0] = p[2]
                if p[2] > bb[2][1]:
                    bb[2][1] = p[2]  
            return self.getLengthFromBoundingBoxes([bb],frontAxis)
                        
    def getSkinClusters(self,nodes):
        list = []
        for node in nodes:
            con = cmds.listConnections(node,type='skinCluster')
            if con:
                for item in con:    
                    if item not in list:
                        list.append(item)
        return list   

    def getMesh(self,clusterName): # returns the meshShape node
        return cmds.skinCluster(clusterName,q=True,g=True)

    def getMeshName(self,clusterName):
        mesh = cmds.skinCluster(clusterName,q=True,g=True)   
        return cmds.listRelatives(mesh[0],parent=True,fullPath=True)[0]
        
    def getLengthFromBoundingBoxes(self,bb,frontAxis):
        # bb = [ [[xmin,xmax],[ymin,ymax],[zmin,zmax]],[[xmin,xmax],[ymin,ymax],[zmin,zmax]] ]
        if len(bb) == 0:
            return 0
        if frontAxis == 'x':    
            xMin = bb[0][0][0]
            xMax = bb[0][0][1] 
            for b in bb:
                if b[0][0] < xMin:
                    xMin = b[0][0]
                if b[0][1] > xMax:
                    xMax = b[0][1]
            return (xMax - xMin)
        if frontAxis == 'z':
            zMin = bb[0][2][0]
            zMax = bb[0][2][1] 
            for b in bb:
                if b[2][0] < zMin:
                    zMin = b[2][0]
                if b[2][1] > zMax:
                    zMax = b[2][1]
            return (zMax - zMin)  
            
                    
class Physics:
    def __init__(self):
        ui = ButterflyToolUI()
        self.butterflyName = ui.objectName
        self.liftCoefficient = ui.liftCoefficient
        self.dragCoefficient = 5.0
        self.airDensity = 0.0000012                       # (cm/m^3)  == 1.25 kg/m^3
        self.wingLength = ui.wingLength                   # cm
        self.wingArea = self.wingLength*self.wingLength   # cm^2 (2.0 wings) rough approximate
        #self.mass = ui.mass/1000.0     # kg
        self.mass = self.getButterflyMass()
        self.g = -ui.g                                    # gravity (cm/s)
        self.fps = ui.fps                                 # frame rate (frames/sec)
        self.maxLiftVel = self.wingLength*30.0      # maximum lift velocity (lift decreases as velocity increases)

    def updateSettings(self,t):
        self.liftCoefficient = cmds.getAttr( "%s.liftCoefficient" % self.butterflyName, t=(t) )
        self.g = -cmds.getAttr( "%s.gravity" % self.butterflyName, t=(t))  
        self.wingLength = cmds.getAttr( "%s.wingLength" % self.butterflyName, t=(t))  
        self.wingArea = self.wingLength*self.wingLength
        self.mass = self.getButterflyMass()
        
    def getButterflyMass(self):
        #return 0.00000075*self.wingArea**2  # 
        return 0.00000112*self.wingArea**2

    def getDrag(self,vel):
        # x = 1.3*(vel/self.maxLiftVel) - 1.0
        # liftDragRatio = 1.0/(1+(10.0)**(-x))    # increase drag as velocity increases
        drag_ = (self.dragCoefficient*self.airDensity*self.wingArea*vel*vel)/(2.0*self.mass)
        # return liftDragRatio*(self.liftCoefficient*self.airDensity*self.wingArea*vel*vel)/(2.0*self.mass)
        return drag_
                       
    def getLift(self,vel):
        lift = (self.liftCoefficient*self.airDensity*self.wingArea*vel*vel)/(2.0*self.mass)
        return lift
         
            
        
class CurrentPathState:
    def __init__(self,pm,fps,frontAxis):
        self.pm = pm
        self.fps = fps
        self.frontAxis = frontAxis
        self.curDir = 0.0
        self.prevDir = 0.0
        self.avgdAngle = 0.0
        self.dist = 0.0
        self.prevDist = 0.0
        self.curVel = 0.0
        self.curLift = 0.0
        self.vertVel = 0.0
        self.prevAccel = 0.0
        self.curAccel = 0.0
        self.avgAccel = 0.0
        self.ry = 0
        self.dAngle = 0
        self.dirRotY = 0         # 0- ry decreasing, 1- ry increasing
        #self.initialize()
        
    def initialize(self,start):
        self.curDir = self.pm.getPathStartDirection()
        self.prevDir = self.pm.getPathStartDirection()
        self.prevDist = 0.0
        self.ry = angleBetweenVectors( self.pm.getPathStartDirection(),self.frontAxis )
        dist = self.pm.getPathDistanceAtTime(start+1)
        self.curVel = dist*self.fps
        self.prevAccel = 0.0
        self.curAccel = 0.0
        self.vertVel = self.curDir.y * self.curVel 

    def updateYRotation(self):
        self.dAngle = angleBetweenVectors(self.curDir,self.prevDir)
        #self.prevDir = self.curDir
        self.ry = self.ry + self.dAngle
        return self.ry

    def getAverageDirection(self,start):
        smoothing = 5 # smooth by averaging accel for 5 frames ahead
        prevDir = self.curDir
        tPrev = start
        first = start + 1
        last = start + smoothing
        dAngle = angleBetweenVectors(self.curDir,self.prevDir)
        avg = dAngle
        for t in range(first,last):
            dt = (t - tPrev)/self.fps
            dir = self.pm.getPathDirectionAtTime(t)
            dAngle = angleBetweenVectors(dir,prevDir)
            avg += dAngle
            tPrev = t
            prevDir = dir
        return avg/smoothing

    def getAverageAcceleration(self,start):
        smoothing = 5 # smooth by averaging accel for 5 frames ahead
        prevDist = self.dist
        prevVel = self.curVel
        tPrev = start
        first = start + 1
        last = start + smoothing
        avg = self.curAccel
        n = 1
        for t in range(first,last):
            dt = (t - tPrev)/self.fps
            dist = self.pm.getPathDistanceAtTime(t)
            vel  = (dist - prevDist)/dt
            accel = (vel - prevVel)/dt
            if vel != 0.0:
                avg += accel
                n += 1
            tPrev = t
            prevDist = dist
            prevVel = vel
        if n > 0:
            return avg/n 
        else:
            return avg    
   
    def moveAlongPath(self,t,dt):      
        self.prevDist = self.pm.getPathDistance()
        self.pm.setPathPositionToTime(t)
        self.dist = self.pm.getPathDistance()
        prevVel = self.curVel
        self.curVel = (self.dist - self.prevDist)/dt 
        self.prevAccel = self.curAccel
        self.curAccel = (self.curVel - prevVel)/dt
        self.prevDir = self.curDir
        self.curDir = self.pm.getPathDirection() 
        self.vertVel = self.curDir.y*self.curVel
        self.avgAccel = self.getAverageAcceleration(t)
        self.avgdAngle = self.getAverageDirection(t)
        
       
        
class CurrentCycleState:
    def __init__(self,pm,fps):
        self.pm = pm
        self.fps = fps
        self.curTime = 0.0
        self.prevTime = 0.0
        self.wcd = 0.0            # wing cycle duration in frames
        self.wcdIsSet = False
        self.startTime = 0.0
        self.startPos = 0.0
        self.dyPrev = 0.0
        self.initVel = 0.0      # body vertical movement only
        self.initPathDistance = 0.0
        self.pathDist = 0.0
        self.pathVel = 0.0
        self.tPrev = 0.0
        self.avgs = 5  # number of future frames used for acceleration averages

    def initialize(self,start):
        self.startTime = start
        self.startPos = self.pm.getPathPosition()
        self.initVel = 0.0 # self.pm.getPathVerticalVelocityAtTime(self.start)
        self.pathVel = self.pm.getPathVelocityAtTime(start)
        self.tPrev = start
        
    def getCycleTime(self):  # return cycle time as 0->1
        return self.curTime/self.wcd
        
    def getCycleEndTime(self):
        return self.startTime + self.wcd    

    def startNewCycle(self,t):
        self.startTime = self.startTime + self.wcd 
        self.curTime = t - self.startTime
        self.startPos = self.pm.getPathPositionAtTime(self.startTime)
        self.dyPrev = 0
  
    def getPathAccelAverages(self,start,end):
        pathAccelerations = []
        velocities = []
        prevDist = self.pathDist
        prevVel = self.pathVel
        tPrev = self.tPrev
        for t in range(start,end+self.avgs):
            if t == tPrev:
                pathAccelerations.append(0.0)
                continue
            dt = (t - tPrev)/self.fps
            dist = self.pm.getPathDistanceAtTime(t)
            vel  = (dist - prevDist)/dt
            velocities.append(vel)
            pathAccel = (vel - prevVel)/dt
            if vel == 0.0:
                pathAccelerations.append(0.0)
            else:
                pathAccelerations.append(pathAccel)
            tPrev = t
            prevDist = dist
            prevVel = vel
 
        avgs = []
        for t in range(end-start):
            avg = 0.0
            for i in range(t,t+self.avgs):
                avg += pathAccelerations[i]
            avg /= self.avgs
            avgs.append(avg)
        return avgs, velocities
           
    def updatePathInfo(self,t):
        dt = (t - self.tPrev)/self.fps
        if dt == 0.0:
            return
        dist = self.pm.getPathDistanceAtTime(t)
        vel = (dist - self.pathDist)/dt
        self.pathAccel = (vel - self.pathVel)/dt
        self.tPrev = t
        self.pathDist = dist
        self.pathVel = vel


class GlideManager:
    """ Manages movement along path while gliding """
    def __init__(self,cn,wc,pm,crp,rigGrp):
        self.cn = cn                     # ControlNames()
        self.pm = pm                     # PathManager()
        self.wc = wc                     # WingCycle()
        self.cycleName = cn.cycleName
        self.butterflyName = cn.objectName
        self.maxGlideRotation = 0.5      # ie. half the normal wing rotation
        self.rotMin = 0.0
        self.rotMax = 0.0
        self.rotRange = 0.0
        self.setMainWingRotationValues()
        self.sIn = 1.0
        self.sMin = 1.0
        self.sOut = 1.0 
        self.gliding = False 
        self.transitioning = False      
        self.straightIntoGlide = False
        self.finishIntoGlide = False
        self.transitionOutOfGlide = False
        self.keyGlideTransitionCycle = False
        self.cycleRootParent = crp
        self.rigGrp = rigGrp

    def getNodeName(self,node):
        if self.cycleRootParent is None:
            return self.cn.rigGrp + node
        else:    
            return node.replace(self.cycleRootParent,self.cn.rigGrp)
         
    def setMainWingRotationValues(self):
        rMax,rMin = self.wc.wingInfo.getMainWingRotationInfo()
        self.rotMin = rMin
        self.rotMax = rMax
        self.rotRange = rMax-rMin
 
    def getWingRotation(self):  # returns a value between 0 -> self.maxGlideRotation
        """ calculates a wing rotation amount based on current path dir.y """
        dir = self.pm.getPathDirection()
        return (dir.y+1.0)*self.maxGlideRotation  # return 0->1 (from rMax to rMin)

    def keyWingsGlide(self,t,wingRotation):
        # ********** work out wing main rotation ******************
        for wingName in self.wc.wingNames:
            name = self.getNodeName(wingName)
            key = KeyFrame(name,'rotateZ',t,wingRotation)
            createKeyframe(key) 
            
    def updateGlide(self,t):
        glideRotation = self.getWingRotation()
        wingRotation = self.rotMax - glideRotation*self.rotRange 
        self.keyWingsGlide(t,wingRotation)

    def setTransitionVariables(self):
        # called at end of a transition cycle before keying the transition cycle
        glideRotation = self.getWingRotation()
        if self.finishIntoGlide:    
            self.sOut = 1.0 - glideRotation
            self.finishIntoGlide = False
            self.transitioning = False
        elif self.transitionOutOfGlide:
            self.sOut = 1.0

    def endTransitionOutOfGlide(self):
        self.transitionOutOfGlide = False 
        self.transitioning = False 
        self.sIn = 1.0
        
    def movingStraightIntoGlide(self,cycleTime,t):
        if self.straightIntoGlide:
            glideRotation = self.getWingRotation()
            if cycleTime > glideRotation:
                self.transitioning = False
                self.straightIntoGlide = False  # finished transition, start gliding
                self.updateGlide(t)             
            return True
        return False    
          
    def startGliding(self,cycle):
        self.gliding = True
        self.transitioning = True
        self.transitionOutOfGlide = False
        cycleTime = cycle.curTime/cycle.wcd # 0->1
        glideRotation = self.getWingRotation() # 0.5->0.0 when dir.y (0)->(-1)   
        glideRotationPosition = glideRotation*self.wc.wingInfo.tMin #tMin is cycleTime, bot of cycle
        if cycleTime > glideRotationPosition:
            if cycleTime > self.wc.wingInfo.tMin:
                self.finishIntoGlide = True  
                #self.sMin = 1.0
            else:
                self.straightIntoGlide = True
        else:
            self.straightIntoGlide = True  
                        
    def stopGliding(self):
        self.transitioning = True
        if self.straightIntoGlide:
            self.straightIntoGlide = False
            self.gliding = False
        elif self.finishIntoGlide:
            self.finishIntoGlide = False
            self.gliding = False 
        else:  # it's either gliding or transitioning out of a glide
            if not self.transitionOutOfGlide:
                self.gliding = False
                self.transitionOutOfGlide = True 
                self.sIn = 1.0 - self.getWingRotation()
                self.sMin = 1.0


class WeightedAverage:
    """ calculates a weighted average where lower values are weighed > higher values"""
    def __init__(self):
        self.count = 0.0
        self.sumInvWcd = 0.0

    def reset(self):
        self.count = 0.0
        self.sumInvWcd = 0.0 
            
    def getWeightedAverage(self,wcd):
        self.count += 1.0
        self.sumInvWcd += 1.0/wcd
        wAvgWcd = self.count/self.sumInvWcd
        return wAvgWcd 
 
                            
class ButterflyAnimationManager:
    """ Main class to manage everything required for butterfly movement along path """
    
    def __init__(self):
        self.ds = DefaultButterflySettings()
        self.ui = ButterflyToolUI()
        self.cn = ButterflyControlNames()
        self.mPath = self.cn.motionPathName
        self.pathUValue = self.cn.pathUValue
        self.rotateCtrlName = self.cn.getRotateControlName()
        self.keyedCtrls = self.ui.getWingNameList()
        self.start = self.ui.start
        self.end = self.ui.end
        self.prevTime = self.ui.start
        self.fps = self.ui.fps
        self.wingLength = self.ui.wingLength
        self.cycleName = self.ui.cycleName
        self.rotateCtrlName = self.cn.getRotateControlName()
        self.wc = None    # WingCycle, initialized in self.initWingCycleManager()
        self.cycleRootParent = None  # initialized in self.initWingCycleManager()
        self.frontAxis = self.ui.getFrontAxisVector()
                
        # self.wc = wingCycleFileManager.getWingCycle()
        self.pm = PathManager()
        self.path = CurrentPathState(self.pm,self.fps,self.frontAxis)
        self.cycle = CurrentCycleState(self.pm,self.fps)
        self.physics = Physics()
        self.gm = None 

        rollAxis, rollDir = self.ui.getFrontAxis()
        self.pitchDir, self.pitchAxis = self.ui.getPitchAxis()   
        self.rollDir = (rollDir*2.0)-1.0 # convert to -1 or +1
        if rollAxis == 'x':
            self.rollAxis = 'rotateX'
        else:
            self.rollAxis = 'rotateZ'  
                    
        self.butterflyName = self.ui.objectName
        self.wingCycleRate = self.ui.wingCycleRate
        self.glide = self.ui.glide
        self.roll = self.ui.roll
      
        self.aPrev = 0.0
        self.daPrev = 0.0
        self.m1 = 0.0
        self.m2 = 0.0

        self.wa = WeightedAverage()
        self.gliding = False
        self.endGlide = False
        self.glideRotation = 0.0
        self.endGlideTimeFactor = 0.0

    def initWingCycleManager(self):        
        global wingCycleFileManager
        self.wc = wingCycleFileManager.getCycle( self.cycleName )
        if not self.wc:
            jfn = JsonFileName(self.cycleName)   
            errorMessage( 'Could not find json file for Wing Cycle: %s !\n' 
                          'Location: %s' % (self.cycleName,jfn.getFullFolderName()) )
            butterflyProgressUpdate("... missing wing cycle json file ...")  
            return False
        self.cycleRootParent = self.getWingCycleRootNode() 
        # find the root node name from the Saved Wing Cycle
        if not self.cycleRootParent and self.cycleRootParent is not None:
            errorMessage( 'Could not match %s rig with saved Wing Cycle rig!' % self.ui.objectName)
            return False  
        # make sure the selected rig matches the Saved Wing Cycle rig
        for node in self.wc.keyedNodeNames:
            matchingNode = self.getNodeName(node)
            if not cmds.objExists(matchingNode):
                errorMessage( 'Could not match %s rig with saved Wing Cycle rig!\nMissing node: %s.' % 
                                (self.ui.objectName,matchingNode))    
                return False                
        self.gm = GlideManager(self.cn,self.wc,self.pm,self.cycleRootParent,self.cn.rigGrp) 
        self.wc.startNewCycle()
        return True  

    def getWingCycleRootNode(self):
        # finds the parent node to be replaced from the saved cycle rig to current rig
        children = cmds.listRelatives(self.cn.rigGrp,c=True,f=True) 
        if children:
            for child in children:
                root = children[0].split('|')[-1] # [1:][0] 
                i = self.wc.keyedNodeNames[0].find(root)-1
                if i == 0:
                    return None
                if i >= 0:
                    return self.wc.keyedNodeNames[0][:i]
        return False  

    def getNodeName(self,node):
        if self.cycleRootParent is None:
            return self.cn.rigGrp + node
        else:    
            return node.replace(self.cycleRootParent,self.cn.rigGrp)

    def keyPosition(self,t,v):
        cmds.setKeyframe(self.pathUValue,v=v,t=t,itt='spline',ott='spline') 
        
    def keyRotation(self,t,at,v):
        cmds.setKeyframe(self.rotateCtrlName,at=at,v=v,t=t,itt='spline',ott='spline')       

    def keyVerticalMovement(self,t,v):
        cmds.setKeyframe(self.rotateCtrlName,at='translateY',v=v,t=t,itt='spline',ott='spline')
        
    def keyPitchRotation(self,t,v):
        v = self.pitchDir*v
        cmds.setKeyframe(self.rotateCtrlName,at=self.pitchAxis,v=v,t=t,itt='spline',ott='spline')    
        
    def scaleKeyframes(self,ts):
        cmds.scaleKey(self.pathUValue,timeScale=ts,timePivot=self.start,valueScale=1,valuePivot=0)
        #cmds.scaleKey(self.rotateCtrlName,at='rotateY',timeScale=ts,timePivot=self.start,valueScale=1,valuePivot=0)

    def getCurrentCycleTime(self):
        """ Returns current cycle time as value between 0 -> 2*pi """
        return (self.cycle.curTime/self.cycle.wcd)*2.0*math.pi 

    def initializeWingCycle(self):
        self.pm.setPathPositionToTime(self.start)
        self.prevTime = self.start
        self.cycle.initialize(self.start)
        self.path.initialize(self.start)
        self.updateAnimationSettings(self.start)
        lft = self.physics.getLift(self.path.curVel)*self.glide
        lift = self.clamp(lft,0,-0.95*self.physics.g)        
        dy = 0.0
        v0 = self.path.vertVel
        # accelFromForces = self.path.curAccel + self.physics.g + lift  # brake force + gravity + lift forces
        accelFromForces = self.physics.g + lift
        wcd = (-v0-math.sqrt(v0**2-2.0*accelFromForces*(2.0*self.wingLength*self.wingCycleRate-dy)))/accelFromForces
        self.cycle.wcd = wcd*self.fps

    def getCycleVelocityAtTime(self,t):
        """ Returns a y velocity for butterfly at cycle time t (t:0->2*pi) """
        v = -self.m1*math.cos(t) + self.m1 + self.m2*t + self.cycle.initVel
        return v

    def getVerticalDistanceForCycleTime(self,t):
        """ Returns a y translation for butterfly at cycle time t (t:0->2*pi) """
        d = -self.m1*math.sin(t) + self.m1*t + 0.5*self.m2*t*t + self.cycle.initVel*t
        return d 

    def startNewCycle(self,t):
        """ initialize values for the start of a new cycle """
        cycleTime = self.cycle.getCycleTime()   # as a value from 0.0 to 1.0

        if self.gm.transitioning:    
            self.keyButterflyGlideTransition(cycleTime,t,self.gm.sIn,self.gm.sMin,self.gm.sOut)
            self.keyBodyVerticalMovement(cycleTime,t) 
            self.gm.endTransitionOutOfGlide() 
        else:  # key previous cycle
            self.keyButterfly(cycleTime,t)
            self.keyBodyVerticalMovement(cycleTime,t)

        self.cycle.startNewCycle(t)
        self.wc.startNewCycle()

    def keyFinalCycle(self,t):
        if self.gm.gliding:
            return
        cycleTime = self.cycle.curTime/self.cycle.wcd
        # self.cycle.finalVel = self.pm.getPathVerticalVelocityAtTime(t)
        if self.gm.transitioning:
            self.keyButterflyGlideTransition(cycleTime,t,self.gm.sIn,self.gm.sMin,self.gm.sOut)
            self.keyBodyVerticalMovement(cycleTime,t) 
        else:
            self.keyButterfly(cycleTime,t)
            self.keyBodyVerticalMovement(cycleTime,t)    

    def keyButterfly(self,cycleTime,t):
        """ Create keyframes for any attributes required at this cycleTime """
        # **** NOTE: *** have to make sure dt is always less then the smallest time gap between keyframes
        # or ensure this section runs through all keyframes in between dt
        keys = self.wc.getNextKeyframes(cycleTime) 
        if keys:
            for k in keys:
                name = self.getNodeName(k.name)
                kt = t - (cycleTime - k.t)*self.cycle.wcd 
                key = KeyFrame(name,k.at,kt,k.v)
                createKeyframe(key)

    def keyButterflyGlideTransition(self,cycleTime,t,sIn,sMin,sOut):
        keys = self.wc.getNextKeyframes(cycleTime) 
        if keys:
            for k in keys:
                name = self.getNodeName(k.name)
                if self.wc.isAWing(k.name):
                    rMax,rMin = self.wc.wingInfo.getWingInfo(k.name,k.at)
                    rRange = rMax-rMin
                    if k.t <= self.wc.wingInfo.tMin:
                        kv = (k.v-rMin)*(sIn-(1.0-sMin))+rRange*(1.0-sMin)+rMin
                    else:
                        kv = (k.v-rMin)*(sOut-(1.0-sMin))+rRange*(1.0-sMin)+rMin 
                else:
                    kv = k.v    
                kt = t - (cycleTime - k.t)*self.cycle.wcd
                key = KeyFrame(name,k.at,kt,kv)
                createKeyframe(key)

    def getBrakingForce(self,accel,dir):
        a = accel - self.physics.g*dir.y
        return self.clamp(a/self.physics.g,0.0,1.0) 
    
    def keyBodyVerticalMovement(self,cycleTime,t):         # cycleTime (0->1.0)   t (frames)
        """ calculate and creates keyframes for butterfly's y translation """  
        # get the start and end frame for this wing cycle 
        tStart = self.cycle.startTime         # t - cycleTime*self.cycle.wcd 
        tEnd = self.cycle.getCycleEndTime()   #t - (cycleTime - 1.0)*(self.cycle.wcd)
        dy = self.pm.getPathPositionAtTime(tEnd).y - self.cycle.startPos.y  # total cycle dy
        fDir = self.pm.getPathDirectionAtTime(tEnd)
        fPathGradient = math.tan(math.asin(fDir.y))     # gradient of path at cycle end
        dGradient = 1.0      # difference from path to butterfly movement at cycle end
        finalVel = fPathGradient - dGradient

        # because the vertical distance is calculated using cycle time 0->2pi
        # we need to convert path and wcd values to 0->2pi         
        v0 = self.cycle.initVel * (self.cycle.wcd/(2.0*math.pi))
        vf = finalVel * (self.cycle.wcd/(2.0*math.pi)) 
        
        m2 = (vf - v0)/(2.0*math.pi)
        m1 = dy/(2.0*math.pi) - m2*math.pi - v0     
     
        start = int(tStart)
        if tStart > start: # then start at the next frame
            start = int(tStart+1)
        end = int(tEnd+1)
        if tEnd > t:    
            end = t+1

        maxPitchRot = self.ds.maxPitchRot 
        maxCycleRot = self.ds.maxCycleRot
        maxBrakeRot = self.ds.maxBrakeRot

        avgs, vels = self.cycle.getPathAccelAverages(start,end)
        i = 0

        for n in range(start,end): # key every frame for the cycle
            ct = ((n-tStart)/self.cycle.wcd)*2.0*math.pi   # cycle time 0->2*pi
            dir = self.pm.getPathDirectionAtTime(n)
            
            # get the cycle vertical movement for the current time
            y = -m1*math.sin(ct) + m1*ct + 0.5*m2*ct*ct + v0*ct

            # keep the butterfly near the path when variation in path height is greather then dy
            # yPath = self.pm.getPathPositionAtTime(n).y - self.pm.getPathPositionAtTime(tStart).y
            ndy = ((n-tStart)/(tEnd-tStart))*dy  # y on linear path from start to end
            ty = 0.15*(y-ndy)   # 0.15 reduces the vertical variation to something which looks good 
            pitchRot = 0.0
            rotToHorz = -math.degrees( math.asin(dir.y)) # rotation from path dir to horizontal
            
            if dir.y > 0:
                # butterfly rotates upwards mid cycle while it is ascending
                # multiplier -> pitch rotation is maximum when dir.y = 0.707 and 0.0 when dir.y = 0.0 & 1.0
                slopeMultiplier = -0.5*math.cos(4.0*math.asin(dir.y))+0.5
                cycleRot = -0.5*math.cos(ct)+0.5  # 0.0 at start and end of cycle, 1.0 at mid cycle
                pitchRot = rotToHorz + (maxPitchRot + maxCycleRot*cycleRot)*slopeMultiplier

            # butterfly rotates back to assist in braking 
            # accel = self.cycle.updatePathInfo(n)
            self.cycle.updatePathInfo(n)
            accel = avgs[i]
            if accel < 0.0:
                brakeAmount = self.clamp(4.0*accel/self.physics.g,0.0,1.0)
                brakeRot = maxBrakeRot*(2.0*math.cos(0.25*(dir.y+1.0)*math.pi) - 1.0)
                pitchRot = brakeAmount*brakeRot

            self.keyVerticalMovement(n,ty)
            self.keyPitchRotation(n,pitchRot)

            i += 1
                
        self.cycle.initVel = finalVel # self.getCycleVelocityAtTime(2.0*math.pi)
        # self.cycle.prevBrakeAmount = endBrakeAmount

    def updateAnimationSettings(self,t):
        self.wingCycleRate = 1.0/cmds.getAttr( "%s.cycleRate" % self.butterflyName, t=(t) )
        self.glide = cmds.getAttr( "%s.glide" % self.butterflyName, t=(t) )
        self.roll = cmds.getAttr( "%s.roll" % self.butterflyName, t=(t) ) 
        self.wingLength = cmds.getAttr( "%s.wingLength" % self.butterflyName, t=(t) ) 
        self.physics.updateSettings(t)

    def clamp(self,v,min_value,max_value):
        return max(min(v, max_value), min_value)
   
    def updateRoll(self,t):
        self.path.updateYRotation()
        wingStrength = -500.0  
        rotationForce = self.clamp((self.roll*self.path.curVel*self.path.avgdAngle)/wingStrength,-1.0,1.0)
        rollAngle = math.degrees( math.asin(rotationForce) )
        self.keyRotation(t,self.rollAxis,rollAngle)
             
    def updateCycle(self,t,df):   # t - time (frames)    df - change in time (frames)  dt - (seconds)
        """ update curCycleTime and check if new cycle needs to start """
        curPos = self.pm.getPathPosition()
        
        lift = self.path.curLift*self.glide
        maxLift = -0.95*self.physics.g
        if lift > maxLift:
            lift = maxLift
   
        dy = (curPos.y - self.cycle.startPos.y) #*self.wingCycleRate   # vertical distance since start of this wcd

        v0 = self.cycle.initVel #self.path.vertVel

        accelFromForces = self.physics.g + lift - abs(self.path.curAccel)  # brake force + gravity + lift forces
        # accelFromForces = self.path.curAccel + self.physics.g + lift
    
        # calculate butterfly vertical movement limit at this initial velocity (prevents divide by zero in wcd calc)
        dyLimit = -(v0**2/(2.0*accelFromForces)-2.0*self.wingLength*self.wingCycleRate)
        if dy >= dyLimit:  # then limit vertical movement for this wing cycle
            # interpolate between frames for more accurate wcd value 
            self.cycle.wcd = ((dyLimit-self.cycle.dyPrev)/(dy-self.cycle.dyPrev))*df + self.cycle.prevTime #/self.wingCycleRate
            self.cycle.wcdIsSet = False
            self.startNewCycle(t)
        else:
            wcd1 = (-v0-math.sqrt(v0**2-2.0*accelFromForces*(2.0*self.wingLength*self.wingCycleRate-dy)))/accelFromForces
            wcd1 *= self.fps

            wAvg = self.wa.getWeightedAverage(wcd1)
            wcd1 = wAvg

            if self.cycle.wcdIsSet:
                if wcd1 < self.cycle.wcd:
                    self.cycle.wcd = wcd1
                if self.cycle.curTime >= self.cycle.wcd:
                    self.startNewCycle(t)
                    self.wa.reset()
                    self.cycle.wcdIsSet = False 
            else: 
                tMin = self.wc.wingInfo.tMin*wcd1
                if self.cycle.curTime >= tMin:
                    # first half of cycle (downward wing) creates the movement, so is the important half
                    # locking in wcd from first half works better when second half requires less wing movement
                    wcd0 = self.cycle.wcd/2.0
                    self.cycle.wcd = ((self.cycle.prevTime*(tMin-wcd0)-df*wcd0)/(tMin-wcd0-df))*2.0
                    self.cycle.wcdIsSet = True

                else:  # continually update wcd using the weighted wcd1 from this frame
                    self.cycle.wcd = wcd1    
                    self.cycle.dyPrev = dy

        # set a minimum wcd1 to prevent high WingCycleRates causing chaos
        if self.cycle.wcd < 1.23:  
            self.cycle.wcd = 1.23 # 1.23 keeps prevents wing cycles syncing to the frame rate
                
    def updateGlideTransition(self,t):
        cycleTime = self.cycle.curTime/self.cycle.wcd
        if self.gm.movingStraightIntoGlide(cycleTime,t):
            # turns off self.gm.transitioning when ready to glide
            self.cycle.updatePathInfo(t)
            return
        # key the transition cycle once it is completed
        if self.cycle.curTime >= self.cycle.wcd:
            # finished transition so create keyframes for the cycle
            cycleTime = self.cycle.curTime/self.cycle.wcd
            self.gm.setTransitionVariables()
            self.keyButterflyGlideTransition(cycleTime,t,self.gm.sIn,self.gm.sMin,self.gm.sOut)
            self.keyBodyVerticalMovement(cycleTime,t)
            self.cycle.startNewCycle(t)
            self.wc.startNewCycle() 
            
    def updateGlideCycle(self,t):
        if self.gm.transitioning:
            self.updateGlideTransition(t) # transition into or out of the glide 
        else:
            self.cycle.updatePathInfo(t)
            self.gm.updateGlide(t)         # update the wings for the glide 
   
    def updateGlideState(self,t):
        lift = self.physics.getLift(self.path.curVel)
        drag_ = self.physics.getDrag(self.path.curVel)

        adjLift = 4.0   # multiply the effect of lift (so that 5cm butterfly can glide at 100cm/s)
        if self.glide > 0.5:
            adjDrag = ((self.glide-0.5)*2.0)*10.0*drag_ + drag_  # 10.0 just looks good
            adjGlide = -((self.glide-0.5)*2.0)*self.physics.g
            glide = adjLift*lift + adjGlide
        else:
            adjDrag = self.glide*2.0*drag_
            adjGlide = self.glide*2.0
            glide = adjGlide*adjLift*lift

        okToGlide = True
        # can't glide if path acceleration is greater then gravity assisted acceleration
        if self.path.curAccel > self.physics.g*self.path.curDir.y:
            okToGlide = False
        # can't glide if path deceleration is greater then can be achieved by drag  
        if self.path.curAccel < (self.physics.g*self.path.curDir.y-adjDrag):
            okToGlide = False

        # calculate the acceleration from the gravitational force opposing the lift force acceleration 
        opposition = -self.physics.g*math.cos(math.asin(self.path.curDir.y))
      
    
        if okToGlide and glide > opposition:
            if not self.gm.gliding:
                self.gm.startGliding(self.cycle)
        else:
            if self.gm.gliding and not self.gm.transitionOutOfGlide:
                self.gm.stopGliding()
                if self.gm.transitionOutOfGlide: 
                    # start transition cycle out of glide
                    self.cycle.startTime = t 
                    self.cycle.curTime = 0.0
                    self.cycle.startPos = self.pm.getPathPositionAtTime(t)
                    self.cycle.dyPrev = 0
                    self.wc.startNewCycle()
        self.path.curLift = adjLift*(lift-self.path.curDir.y*drag_)  

    def updateBraking(self,t):
        maxBrakeRot = self.ds.maxBrakeRot
        dir = self.path.curDir
        brakeAmount = self.clamp(4.0*self.path.avgAccel/self.physics.g,0.0,1.0)
        brakeRot = maxBrakeRot*(2.0*math.cos(0.25*(dir.y+1.0)*math.pi) - 1.0)
        pitchRot = brakeAmount*brakeRot
        self.keyPitchRotation(t,pitchRot)
                        
    def update(self,t):                 # t is current time (in frames)
        """ manage all butterfly updates """
        # update cycle parameters
        df = t - self.prevTime          # change in time (in frames)
        dt = df/self.fps                # change in time (in seconds)
        self.prevTime = t
        self.cycle.prevTime = self.cycle.curTime     # previous cycle time (frames)
        self.cycle.curTime += df                     # current cycle time in (frames)
        self.path.moveAlongPath(t,dt)    # updates butterfly path position
        self.updateAnimationSettings(t)
        self.updateGlideState(t)
        self.updateRoll(t)
        if self.gm.gliding:
            self.updateGlideCycle(t)
            self.updateBraking(t)
        else:
            self.updateCycle(t,df)


#------------------------------------------------------------------------------------------------------ 
# JSON File Import Export
#------------------------------------------------------------------------------------------------------
class JsonFileName:
    def __init__(self,cycleName):
        ds = DefaultButterflySettings()
        self.jsonFileName = self.getFileName(cycleName)
        self.folder = ds.folder
        self.fullFolderName = self.getFullFolderName()
        self.fullFileName = self.fullFolderName + "/" + self.jsonFileName

    def getFileName(self,cycleName):
        return cycleName + '.json'

    def getDataFileName(self):
        return self.fullFileName
  
    def getFullFolderName(self):    
        current_directory = cmds.workspace( q=True, rd=True )
        directory = current_directory + self.folder
        if not os.path.exists(directory):
            okDialogBox( "Creating folder to store wing cycle Information:\n%s" % directory ) 
            try:
                os.makedirs(directory)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
                return None
        return directory 
  

class JsonFileManager:
    def __init__(self,cycleName):
        jfn = JsonFileName(cycleName)
        self.fileName = jfn.fullFileName
    
    def saveToFile(self,data):
        try:
            with open(self.fileName, "w") as write_file:
                json.dump(data, write_file)
            write_file.close()  
        except:
            errorMessage('Unable to write json file: %s' % self.fileName)      
                
    def loadFromFile(self):
        data = None
        try:
            with open(self.fileName, "r") as read_file:
                data = json.load(read_file)
            read_file.close() 
        except:
            errorMessage('Unable to read json file: %s' % self.fileName)    
        return data
         
    def fileExists(self):
        return os.path.isfile(self.fileName)   

#----------------------------------------------------------------------------- 
# Fin Cycle Data File Management
#----------------------------------------------------------------------------- 
class WingCycleFileManager:
    def __init__(self):
        self.cycleName = None 
        self.data = None

    def isLoaded(self,cycleName):
        if cycleName == self.cycleName and self.data:
            return True
        return False
        
    def setCycle(self,cycleName):
        jfm = JsonFileManager(cycleName)
        if jfm.fileExists():
            jsonData = jfm.loadFromFile() 
            wingCycleInfo = WingCycleInfo()
            wingCycleInfo.loadFromJson( jsonData )
            self.cycleName = cycleName 
            self.data = WingCycle( wingCycleInfo ) 
        else:
            self.cycleName = None
            self.data = None    

    def getCycle(self,cycleName):
        if cycleName == self.cycleName and self.data:
            butterflyProgressUpdate("... wing cycle is loaded ...")
            return self.data
        self.setCycle(cycleName)
        if self.data:
            butterflyProgressUpdate("... wing cycle is loaded ...")
            return self.data
        return None

    def saveCycle(self,cycleName,data): # data must be json 
        jfm = JsonFileManager(cycleName)
        jfm.saveToFile(data)
        self.setCycle(cycleName)
        butterflyProgressUpdate("... wing cycle has been saved ...")  

#----------------------------------------------------------------------------- 
# GLOBAL Fin Cycle Information
#----------------------------------------------------------------------------- 
wingCycleFileManager = WingCycleFileManager()


#----------------------------------------------------------------------------- 
# Wing Cycle Information Collection
#----------------------------------------------------------------------------- 
def exportWingCycle():
    global wingCycleFileManager
    ui = ButterflyToolUI()
    cycleName = ui.cycleName
    wingCycleInfo = collectWingCycleInfo( ui )  # wingCycleKeyframeInfo object
    # wingCycleInfo.display()
    if wingCycleInfo:
        wingCycleFileManager.saveCycle(cycleName,wingCycleInfo.toJson())
        updateCycleButtons()
        updateButtons()
        return True
    return False
          
def collectWingCycleInfo( ui ):
    'saves Wing cycle keyframe info for the selected controls'
    ds = DefaultButterflySettings()
    cn = ButterflyControlNames()
    wingCycleName = ui.cycleName 
    # movementCtrl = '%s|%s' % (ui.cycleName,ds.movementCtrlName) 
    start = ui.wcStart
    end = ui.wcEnd
    duration = ui.wcEnd - ui.wcStart
    wingNameList = ui.wingNameList
    wingNames = []

    # make sure the wings have been selected
    # if len(wingNameList) < 1:
    #     errorMessage ("Select Wings before Save Wing Cycle!")
    #     return False

    # check the wing cycle is ok before proceeding
    wcea = WingCycleExportAssistant()
    if not wcea.collectRigInfo(wingNameList):
        return False
           
    #replace the wings group name with wingCycleName
    # grpName = wingNameList[0].split('|')[1]
    # wcea.setCycleName(grpName,wingCycleName)
    wcea.setCycleName(wingCycleName)

    # find all butterfly nodes with keyframes    
    wcea.collectKeyedNodeNames()
    keyedNodeList = wcea.getKeyedNodeNames()
     
    # set Wing Cycle duration
    wcea.setCycleInfo(start,end)
    
    # collect keyframe info for all controls
    resetButterflyProgressControl()
    setButterflyProgressControlMaxValue( len(keyedNodeList) )

    for nodeName in keyedNodeList:
        # ignore movementCtrl and rotateCtrl keyframes
        # as these will be keyed by the script
        # if nodeName == cn.getMovementControlName() or nodeName == cn.rotateCtrlName:
        #     continue
        butterflyProgressUpdate( ".. creating control: %s" % nodeName )
        attributes = cmds.listAttr(nodeName,k=True)
        for at in attributes:
            keyTimes = cmds.keyframe( nodeName, at=at, time=(start,end), query=True )
            if keyTimes:
                for t in keyTimes:
                    rot = cmds.getAttr("%s.%s" % (nodeName,at),time=t)
                    tAsPercentage = (t - start)/duration  # percent of WingCycleKeyframeInfo time
                    itt = cmds.keyTangent(nodeName,query=True,time=(t,t),attribute=at,itt=True)
                    ott = cmds.keyTangent(nodeName,query=True,time=(t,t),attribute=at,ott=True)
                    if itt == 'fixed':
                        itt = 'auto'
                    if ott == 'fixed':
                        ott = 'auto'                    
                    key = KeyFrame(nodeName,at,tAsPercentage,rot,itt,ott)
                    wcea.addKeyframe( key )
        butterflyProgressControl()
    
    if not wcea.collectWingInfo():
        return False
        
    wingCycleInfo = wcea.getWingCycleInfoForExport() 
    return wingCycleInfo

#-----------------------------------------------------------------------------             
# HELPFUL FUNCTIONS
#-----------------------------------------------------------------------------             
def createControlBox(width,height,depth, ctrlName):
    x = width/2.0
    y = height/2.0
    z = depth/2.0
    curveName = cmds.curve( d=(1), p=[(x,y,z),(x,y,-z),(x,-y,-z),(x,-y,z),(x,y,z),(-x,y,z),(-x,-y,z),(x,-y,z),(x,-y,-z),(-x,-y,-z),(-x,y,-z),(x,y,-z),(x,y,z),(-x,y,z),(-x,y,-z),(-x,-y,-z),(-x,-y,z)],k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16] ) 
    cmds.rename( curveName, ctrlName )
    
def createRotateControl( size,offset,pos,ctrlName ):
    curveName = cmds.curve( degree = 1,k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26],\
                    p = [(0.0,0.56,0.83),(0.15,0.56,0.83),(0.1,0.38,0.92),(0.05,0.20,0.98),\
                        (0,0.00,1.00),(-0.05,0.20,0.98),(-0.1,0.38,0.92),(-0.15,0.56,0.83),\
                        (0.0,0.56,0.83),(0,0.71,0.71),(0,0.83,0.56),(0,0.92,0.38),\
                        (0,0.98,0.20),(0,1.00,0.00),(0,0.98,-0.20),(0,0.92,-0.38),\
                        (0,0.83,-0.56),(0,0.71,-0.71),(0.0,0.56,-0.83),(-0.15,0.56,-0.83),\
                        (-0.1,0.38,-0.92),(-0.05,0.20,-0.98),(0,0,-1.0),(0.05,0.20,-0.98),\
                        (0.1,0.38,-0.92),(0.15,0.56,-0.83),(0,0.56,-0.83)] )
    cmds.setAttr( '%s.scaleX' % curveName, size)
    cmds.setAttr( '%s.scaleY' % curveName, size)
    cmds.setAttr( '%s.scaleZ' % curveName, size)
    cmds.move( -offset, "%s.scalePivot" % curveName, "%s.rotatePivot" % curveName, y=True, ws=True )
    cmds.move( offset, curveName, y=True, ws=True )
    cmds.makeIdentity( curveName, apply=True, t=1, r=1, s=1, n=2 )
    cmds.move( pos.x,pos.y,pos.z, curveName, xyz=True, ws=True )
    cmds.rename( curveName, ctrlName )
    
def getNumberOfCurveCVs(curveName):
    degree = cmds.getAttr( '%s.degree' % curveName )
    spans = cmds.getAttr( '%s.spans' % curveName)
    return degree + spans    

def getCurveBoundingBox(curveName):
    numberOfCvs = getNumberOfCurveCVs(curveName)
    min = cmds.pointPosition('%s.cv[0]' % curveName,w=True)
    max = cmds.pointPosition('%s.cv[0]' % curveName,w=True)
    for n in range(1,numberOfCvs):
        wp = cmds.pointPosition('%s.cv[%i]' % (curveName,n),w=True)
        for i in range(3):
            if wp[i] < min[i]:
                min[i] = wp[i]
            if wp[i] > max[i]:
                max[i] = wp[i]
    return [ [min[0],max[0]],[min[1],max[1]],[min[2],max[2]] ]           

def getRotateCtrlFrontAxis(rotateCtrlName):
    bb = getCurveBoundingBox(rotateCtrlName)
    dx = bb[0][1]-bb[0][0]
    dz = bb[2][1]-bb[2][0]
    if dz > dx:
        return 'x'
    return 'z' 

def setRotateControlToFrontAxis(ui,cn): 
    rotateCtrlName = cn.getRotateControlName()
    if cmds.objExists(rotateCtrlName):
        frontAxis, dir = ui.getFrontAxis()
        axis = getRotateCtrlFrontAxis(rotateCtrlName)
        if not axis == frontAxis:
            cmds.delete(cn.rigConstraint)
            cmds.setAttr('%s.rotateY' % rotateCtrlName,90)
            cmds.makeIdentity(rotateCtrlName,apply=True,r=True,n=0) 
            cmds.parentConstraint(rotateCtrlName,cn.rigGrp,name=cn.rigConstraint,mo=True,weight=1.0)

#-----------------------------------------------------------------------------             
# CREATE RIG (GROUP & CONTROLS)
#-----------------------------------------------------------------------------             
def setupRigGroup(args):
    ui = ButterflyToolUI()
    cn = ButterflyControlNames()
    # ds = DefaultButterflySettings()
    if cmds.objExists( ui.objectName ):
        result = yesNoDialogBox( "%s already exists!\nWould you like to create a new Rig?" % ui.objectName )
        if result=='Yes':
            cmds.delete( ui.objectName )
        else: 
            return  
    
    if not cmds.objExists( ui.rigName ):
        errorMessage( "Select a Rig!" )
        return 

    # get the rig orientation from the UI
    frontAxisId = ui.getFrontAxisId()
        
    # create a group for this object
    cmds.group( em=True, name=ui.objectName )
    
    # add attributes for keyframing
    checkAttributes(ui.objectName)
    updateRigCycleName(cn)
 
    grpName = cmds.group( em=True, name=cn.meshGrp )
    cmds.setAttr('%s.inheritsTransform' % grpName,0)
    cmds.parent(grpName,ui.objectName)      
    grpName = cmds.group( em=True, name=cn.rigGrp )
    cmds.parent(grpName,ui.objectName)
    grpName = cmds.group( em=True, name=cn.controlGrp )
    cmds.parent(grpName,ui.objectName)

    # group any mesh attached to the rig
    frontAxis, invf = ui.getFrontAxis()
    butterflyInfo = ButterflyInfo(ui.rigName)
    meshNames = butterflyInfo.getAttachedMeshNames()
    if meshNames:
        # save existing mesh group names
        meshGroupNames = []
        for meshName in meshNames:
            parents = cmds.listRelatives(meshName,parent=True,f=True)
            if parents:
                # if not already in list, add to meshGroupNames list
                # if not meshGroupNames.count(parents[0]): 
                if parents[0] not in meshGroupNames:
                    meshGroupNames.append(parents[0])
        # save mesh info and move meshes into new mesh group        
        length = butterflyInfo.getMeshLength(frontAxis)
        cmds.parent( meshNames, cn.meshGrp )
        # if mesh nodes had a parent group which is now empty, delete parent group
        for meshGrp in meshGroupNames:
            children = cmds.listRelatives(meshGrp,allDescendents=True,fullPath=True)
            if not children:
                cmds.delete(meshGrp)
    else:
        errorMessage( 'Could not find a mesh attached to the Rig!' )
        length = butterflyInfo.getRigLength(frontAxis)
    # cmds.setAttr( "%s.length" % ui.objectName, length ) 
    
    # if no control_L exists, create one
    if not cmds.objExists( cn.controlLayer ):
        cmds.createDisplayLayer( name=cn.controlLayer, number=1, empty=True )
        cmds.setAttr( '%s.color' % cn.controlLayer,17)

    # create movement control (for motion path)
    size = length/1000.0
    createControlBox(size,size,size, cn.motionPathCtrl)
    
    # create rotate control for main body rotations    
    ctrlSize = length/10.0
    offset = ctrlSize*3.0 
    pos = om.MVector(0,0,0)   
    createRotateControl( ctrlSize,offset,pos,cn.rotateCtrl )

    cmds.editDisplayLayerMembers( cn.controlLayer, '|%s' % cn.motionPathCtrl )
    cmds.editDisplayLayerMembers( cn.controlLayer, '|%s' % cn.rotateCtrl )

    # group controls
    cmds.parent('|%s' % cn.rotateCtrl,'|%s' % cn.motionPathCtrl)
    cmds.parent('|%s' % cn.motionPathCtrl,cn.controlGrp)

    # parent the rig to the control nodes and delete old parent group
    parents = cmds.listRelatives(ui.rigName,parent=True,f=True)  
    cmds.parent( ui.rigName, cn.rigGrp )
    if parents:
        children = cmds.listRelatives(parents[0],allDescendents=True,fullPath=True)
        if not children:
            cmds.delete(parents[0])
 
    # parent constrain the rig to the rotate control    
    cmds.parentConstraint(cn.getRotateControlName(),cn.rigGrp,name=cn.rigConstraint,mo=True,weight=1.0)
  
    # creating a new objectName group resets the Rig Orientation front axis
    # so set the front axis to the original Rig Orientation front axis
    id = ui.getFrontAxisId()
    if frontAxisId != id:
        ds = DefaultButterflySettings()
        cmds.setAttr('%s.%s' % (ui.objectName,ds.axis['name']),frontAxisId)
        setRotateControlToFrontAxis(ui,cn)
 
    updateButtons()
    butterflyProgressUpdate("... rig setup complete ... ")       
   
#----------------------------------------------------------------------------- 
# ANIMATION            
#----------------------------------------------------------------------------- 
def detachButterflyFromPath( args ):
    cn = ButterflyControlNames() 
    if not isValidRig(cn):
        return   
    detachButterfly(cn.motionPathName)

def detachButterfly(mPath):
    ui = ButterflyToolUI()
    cn = ButterflyControlNames()

    #mPath = cn.motionPathName
    movementCtrl = cn.getMovementControlName()
    rotateCtrl = cn.getRotateControlName()
    
    # delete motion path constraints
    cmds.cycleCheck(e=False)
    if cmds.objExists(mPath):
        # delete connected nodes
        result = cmds.listConnections(mPath,s=False)
        if result:
            for n in result:
                node_type = cmds.objectType( n )
                if node_type == 'addDoubleLinear':
                    cmds.delete(n)
        cmds.delete(mPath)
    cmds.cycleCheck(e=True)
    
    # reset movement control position
    cmds.setAttr( "%s.translateX" % movementCtrl, 0.0) 
    cmds.setAttr( "%s.translateY" % movementCtrl, 0.0) 
    cmds.setAttr( "%s.translateZ" % movementCtrl, 0.0)
    cmds.setAttr( "%s.rotateX" % movementCtrl, 0.0) 
    cmds.setAttr( "%s.rotateY" % movementCtrl, 0.0) 
    cmds.setAttr( "%s.rotateZ" % movementCtrl, 0.0)
    #cmds.setAttr('%s.rotateX' % movementCtrl,lock=False)
    #cmds.setAttr('%s.rotateY' % movementCtrl,lock=False)
    #cmds.setAttr('%s.rotateZ' % movementCtrl,lock=False)
    
    # reset rotate control rotations
    cmds.cutKey(rotateCtrl)
    cmds.setAttr( "%s.rotateX" % rotateCtrl, 0.0) 
    cmds.setAttr( "%s.rotateY" % rotateCtrl,lock=False) 
    cmds.setAttr( "%s.rotateZ" % rotateCtrl, 0.0) 
    cmds.setAttr('%s.translateX' % rotateCtrl,lock=False)
    cmds.setAttr('%s.translateY' % rotateCtrl,0.0)
    cmds.setAttr('%s.translateZ' % rotateCtrl,lock=False) 

    setRotateControlToFrontAxis(ui,cn)
    updateUI()

def isValidButterflyPath(pathName):
    if not checkTypeIs(pathName,'nurbsCurve'):
        errorMessage( "Select a path for the butterfly to follow!" )
        return False 
    return True
       
def getButterflyPath(ui,cn):
    objectName = ui.objectName
    selectedPathName = ui.pathName
    # if ui.pathName doesn't exist, check if a path is selected
    if not cmds.objExists(selectedPathName):
        selection = cmds.ls(sl=True)    
        if len( selection ) == 0:
            errorMessage( "Select a path for the butterfly to follow" )
            return False     
        if not isValidButterflyPath(selection[0]):
            return False
        selectedPathName = selection[0]    
        #ui.set_pathName( selection[0] )       
    
    # check butterfly is already attached to a path
    mPathName = cn.motionPathName
    if cmds.objExists(mPathName):
        attachedPath = cmds.listConnections(mPathName,type='nurbsCurve')[0] 
        if attachedPath == selectedPathName:
            errorMessage('%s is already attached to %s' % (objectName,selectedPathName))
            ui.set_pathName(selectedPathName)
            return False
        else:
            result = yesNoDialogBox('%s is currently attached to %s.\n Would you like to attach it to %s?' % 
                                    (objectName,attachedPath,selectedPathName))
            if result == 'No':
                return False
            else:
                detachButterfly(mPathName)    

    #if selectedPathName != cn.pathName:
    #    if cmds.objExists(cn.pathName):
    #        cmds.rename( cn.pathName, 'path1' )
    #pathName = cn.pathName
    #cmds.rename( selectedPathName, cn.pathName)
    ui.set_pathName( selectedPathName )    
    #return pathName 
    return selectedPathName     
           
def attachButterflyToPath( args ):
    #attach movement control to motion path
    ui = ButterflyToolUI()
    cn = ButterflyControlNames()
    pathName = getButterflyPath(ui,cn)
    if not pathName:
        return
    objectName = ui.objectName
    start = ui.start
    end = ui.end
    frontAxis, invf = ui.getFrontAxis()

    mPathName = cn.motionPathName
    movementCtrl = cn.getMovementControlName()
    rotateCtrl = cn.getRotateControlName()

    # attach movementCtrl to motion path
    cmds.select( clear=True )
    motionPathName = cmds.pathAnimation( movementCtrl, curve=pathName, fractionMode=True, 
                                        follow=True, followAxis=frontAxis, upAxis='y', worldUpType="vector",
                                        worldUpVector=[0,1,0], inverseUp=False, inverseFront=invf, bank=False, 
                                        startTimeU=start, endTimeU=end);
    cmds.rename( motionPathName, mPathName )

    # create linear tangents for the main path control
    cmds.keyTangent( mPathName, time=(start,start), itt='linear', ott='linear' )
    cmds.keyTangent( mPathName, time=(end,end), itt='linear', ott='linear' ) 
    
    # set movement ctrl rotation order
    cmds.setAttr( '%s.rotateOrder' % rotateCtrl,3)  # xzy 
    cmds.setAttr('%s.rotateY' % rotateCtrl,lock=True) 
    cmds.setAttr('%s.translateX' % rotateCtrl,lock=True)
    cmds.setAttr('%s.translateY' % rotateCtrl,lock=False)
    cmds.setAttr('%s.translateZ' % rotateCtrl,lock=True)  

    if not cmds.attributeQuery('pathUValue', node=objectName, exists=True):
        ds = DefaultButterflySettings()
        cmds.addAttr( objectName, ln="pathUValue",niceName="path U Value",at='double', dv=ds.pathUValue )
        cmds.setAttr( "%s.pathUValue" % objectName, edit=True, keyable=True ) 
    cmds.connectControl( 'pathUValue_grp', '%s.pathUValue' % objectName, index=2 )

    # add an attribute to the butterfly to control movement along the path
    attrName = cn.pathUValue
    path_uValue = '%s.uValue' % mPathName
    cmds.cutKey(path_uValue, clear = True)
    cmds.setDrivenKeyframe( path_uValue, cd=attrName, itt='linear', ott='linear', dv=0.0, v=0.0 )
    cmds.setDrivenKeyframe( path_uValue, cd=attrName, itt='linear', ott='linear', dv=1.0, v=1.0 )
    cmds.setKeyframe( attrName, time=(start,start),value=0.0 )
    cmds.setKeyframe( attrName, time=(end,end),value=1.0 )
    cmds.keyTangent( attrName, time=(start,start), itt='linear', ott='linear' )
    cmds.keyTangent( attrName, time=(end,end), itt='linear', ott='linear' )
    
    updateButtons()
    butterflyProgressUpdate("... finished attaching Butterfly to path ...")

#-------------------------------------------------------------------------------------------
# ANIMATION
#-----------------------------------------------------------------------------  
def updateMotionPathKeyframes( objectName, path_uValue,start, end ):
    firstKeyframe = cmds.findKeyframe( path_uValue, which='first' )
    lastKeyframe = cmds.findKeyframe( path_uValue, which='last' )
    numberOfKeyframes = cmds.keyframe( path_uValue, query=True,kc=True )
    currentTimeRange = lastKeyframe - firstKeyframe
    newTimeRange = end - start
    conversion = newTimeRange/currentTimeRange
    
    if start == firstKeyframe and end == lastKeyframe:
        return
    
    uValue = []
    t = firstKeyframe
    for n in range(0,numberOfKeyframes):
        value = cmds.getAttr( path_uValue, t=(t) )
        itt = cmds.keyTangent( path_uValue, query=True, t=(t,t), itt=True ) 
        ott = cmds.keyTangent( path_uValue, query=True, t=(t,t), ott=True )
        uValue.append( uValueKey(t*conversion,value,itt[0],ott[0]) )
        t = cmds.findKeyframe( path_uValue, t=(t,t), which='next' )
    
    cmds.cutKey( path_uValue )
    for n in range(0,numberOfKeyframes):
        cmds.setKeyframe( path_uValue, time=(uValue[n].t,uValue[n].t),value=uValue[n].value )
        cmds.keyTangent( path_uValue, time=(uValue[n].t,uValue[n].t), itt=uValue[n].itt, ott=uValue[n].ott )

def deleteAnimations(args):
    cn = ButterflyControlNames()
    if not isValidRig(cn):
        return
    deleteAnimationKeyframes(cn)
                       
def deleteAnimationKeyframes(cn):
    cmds.cutKey(cn.getRotateControlName())
    nodes = cmds.ls(cn.rigGrp,dag=True,type='transform') # complete list of joint hierarchy
    for node in nodes:
        hasKeyframes = cmds.keyframe(node,q=True,kc=True)    
        if hasKeyframes:
            cmds.cutKey(node)

def isValidRig(cn):
    if not cmds.objExists(cn.getRotateControlName()):
        errorMessage("Could not find a valid %s rig!" % cn.objectName)
        return False
    return True
                 
def animate(args):
    ui = ButterflyToolUI()
    cn = ButterflyControlNames()
    if not isValidRig(cn):
        return
    deleteAnimationKeyframes(cn)
    start = int(ui.start)
    end = int(ui.end)
    path = ui.pathName
    path_uValue = cn.pathUValue
    
    if not cmds.objExists( path ):
        errorMessage( "%s does not exist!" % path)
        return 

    if not cmds.objExists( path_uValue ):
        errorMessage( "Attach to Motion Path before animating!" )
        return  

    # update path uValues for current start and end time in Animation Settings 
    updateMotionPathKeyframes( ui.objectName,path_uValue,start,end)
    
    bam = ButterflyAnimationManager() # wingCycle )
    if not bam.initWingCycleManager():
        return

    #bam.setInitialPosition()   

    resetButterflyProgressControl()
    setButterflyProgressControlMaxValue(end-start)

    bam.initializeWingCycle()
    resetButterflyProgressControl()
    for t in range(start+1,end+1):
        butterflyProgressControl()
        bam.update(t)
    bam.keyFinalCycle(end)    
    butterflyProgressUpdate('...finished animation...')
    cmds.currentTime(start)  