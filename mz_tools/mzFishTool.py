"""
mzFishTool_b01.py

Version: b01  updated: August 19, 2020
Author:  Steven Thomasson (www.mayazoo.net)
Description: Fish Animation Tool

Copyright (C) 2020 Steven Thomasson. All rights reserved.

"""
import maya.cmds as cmds
import maya.api.OpenMaya as om
import math

def mzFishTool_UI():
    """
    interface
    """
    if checkWorkingUnits()=='No':
        return 

    ds = DefaultFishSettings()
      
    if cmds.window( "mzFishToolWindow", exists=True ):
        cmds.deleteUI( "mzFishToolWindow", window=True )
    #if cmds.windowPref( "mzFishToolWindow", exists=True ):
    #    cmds.windowPref( "mzFishToolWindow", remove=True )
    window = cmds.window( "mzFishToolWindow", title="mzFishTool", widthHeight=(240, 670) )
    cmds.scrollLayout( "scrollLayout" );
    cmds.columnLayout( adjustableColumn=True, columnOffset=("both", 4) ) #, backgroundColor=[1.0,0.0,0.0] )
    #------------------------------------------------------------------  
    # Name
    cmds.columnLayout( rowSpacing=5 )
    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1,70),(2,150)], columnSpacing=[(1,0), (2,2)] ) 
    cmds.text("Fish Name:") 
    cmds.textFieldGrp( "objectName_grp", text=ds.objectName, tcc=changeObjectSetting )
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.setParent("..")
    #------------------------------------------------------------------  
    # Rigging
    cmds.frameLayout( 'rigging_grp', collapsable=True, collapse=False, w=230, label="Rigging" )
    cmds.columnLayout( rowSpacing=5, co=['left',5] )
    #cmds.checkBox( "useSelectedJoints_chb",label='Use Selected Joints',v=ds.useSelectedJoints )
    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1,70),(2,150)], columnSpacing=[(1,0), (2,2)] ) 
    cmds.button( "selectMesh_btn", label="Select Mesh", height=20, width=70, command=updateMeshField )                 
    cmds.textFieldGrp( "meshName_grp", text=ds.meshName, enable=True )
    cmds.setParent("..")
    cmds.button( "createRig_btn", label="Create Rig", h=30, w=220, c=createRig ) 
    cmds.button( "attachRig_btn", label="Attach Rig", en=True, h=30, w=220, command=attachRig ) 
    cmds.text("t1", label="")
    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1,70),(2,150)], columnSpacing=[(1,0), (2,2)] ) 
    cmds.button( "selectPath_grp", label="Select Path", height=20, width=60, command=updatePathField )                 
    cmds.textFieldGrp( "pathName_grp", text=ds.pathName )
    cmds.setParent("..")
    cmds.rowColumnLayout( numberOfColumns=2, columnSpacing=[(1,0),(2,5),(3,5)] )
    cmds.button( "attachFishToPath_btn", label="Attach Fish To Path", h=30, w=200, c=AttachFishToPath ) 
    cmds.button( "detachFromPath_btn", label="D", en=True, h=30, w=15, command=detachFromPath )
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.rowColumnLayout( numberOfColumns=2, rowOffset=[1,'top',3], columnSpacing=[(1,6),(2,5),(3,5)] )
    cmds.button( "animate_btn", label="Create Animation", h=30, w=200, command=createAnimation )
    cmds.button( "deleteAnim_btn", label="D", en=True, h=30, w=15, command=deleteAnimations )
    cmds.setParent("..")
    cmds.text("t3", label="")
    cmds.setParent("..")
    cmds.setParent("..")
    #------------------------------------------------------------------  
    # Animation Settings   
    cmds.frameLayout( 'animationSettings_grp', collapsable=True, collapse=True, w=230, label="Animation Settings" )
    cmds.columnLayout( rowSpacing=0 )
    cmds.floatFieldGrp( "startTime_grp", label="Animation Start Frame", numberOfFields=1, value1=ds.start, cc=changeTimeRange) 
    cmds.floatFieldGrp( "endTime_grp", label="            End Frame", numberOfFields=1, value1=ds.end, cc=changeTimeRange) 
    cmds.floatFieldGrp( "speed_grp", label="Average Speed (cm/s) ",numberOfFields=1, v1=ds.speed, cc=changeSpeedSetting ) 
    cmds.floatFieldGrp( "waveLengths_grp", label="Wave Length", pre=2, numberOfFields=1, v1=ds.waveLengths ) 
    cmds.floatFieldGrp( "waveAmplitude_grp", label="Wave Amplitude", pre=2, numberOfFields=1, v1=ds.waveAmplitude )
    cmds.floatFieldGrp( "waveRate_grp", label="Wave Rate", pre=2,numberOfFields=1, v1=ds.waveRate )
    cmds.floatFieldGrp( "tailAmplitude_grp", label="Tail Amplitude", pre=2,numberOfFields=1, v1=ds.tailAmplitude )
    cmds.floatFieldGrp( "tailFlex_grp", label="Tail Flex", pre=2,numberOfFields=1, v1=ds.tailFlex, cc=clampTailFlex )
    cmds.floatFieldGrp( "effort_grp", label="Effort", pre=2,numberOfFields=1, v1=ds.effort )
    cmds.floatFieldGrp( "pathUValue_grp",label="Path U Value", pre=3, numberOfFields=1, v1=0.0 )
    cmds.setParent("..")
    cmds.setParent("..")
    #------------------------------------------------------------------  
    # Add Keyframes Settings 
    cmds.frameLayout( collapsable=True, collapse=True, w=230, label="Add Keyframes" )
    cmds.columnLayout( rowSpacing=0 )
    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1,120),(2,110)], columnSpacing=[(2,0)] )
    cmds.checkBox( "preActive_chb",label='Always Active',v=ds.preActive )
    cmds.button( "addKeys_btn", label="Add Keyframes", height=20, width=110, c=addKeyframes)
    cmds.setParent("..")
    cmds.floatFieldGrp( "precision_grp", label="Precision", pre=2, numberOfFields=1, value1=ds.precision) 
    cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1,140),(2,60),(3,15)], columnSpacing=[(2,2),(3,5)] )
    cmds.text("Apply From Frame",align='right')
    cmds.floatField( "preStart_grp", pre=1, value=ds.start )
    cmds.button( "preStartSel_btn", label="S", height=20, width=15,c="selectTime('preStart_grp')") 
    cmds.setParent("..")
    cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1,140),(2,60),(3,15)], columnSpacing=[(2,2),(3,5)] )
    cmds.text("To Frame",align='right')
    cmds.floatField( "preEnd_grp", pre=1, value=ds.end )
    cmds.button( "preEndSel_btn", label="S", height=20, width=15,c="selectTime('preEnd_grp')") 
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.setParent("..")
    #------------------------------------------------------------------  
    # Custom Rig Settings   
    cmds.frameLayout( collapsable=True, collapse=True, w=230, label="Rig Settings"  )
    cmds.columnLayout( rowSpacing=0 )
    cmds.intFieldGrp( "numberOfJoints_grp", label="Number of Joints", numberOfFields=1, value1=ds.numberOfJoints)
    cmds.intFieldGrp( "numberOfControls_grp", label="Number of Controls", numberOfFields=1, value1=ds.numberOfControls) 
    #cmds.intFieldGrp( "numberOfHandles_grp", label="Number of Handles", numberOfFields=1, value1=ds.numberOfHandles) 
    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1,140),(2,80)], columnSpacing=[(1,0), (2,2)] ) 
    cmds.button( "enableRigLength_btn", label="Rig Length", height=15, width=70, command=enableRigLengthField )                 
    cmds.floatField( "rigLength_grp", enable=False,width=80, pre=4.0, v=ds.rigLength ) 
    cmds.setParent("..")
    cmds.floatFieldGrp( "length_grp", label="Fish Length",enable=False,pre=4.0,numberOfFields=1,value1=ds.length)
    cmds.setParent("..")
    cmds.setParent("..")
    #------------------------------------------------------------------ 
    # Progress Bar
    cmds.frameLayout( collapsable=False, collapse=False, w=230, label="Progress Bar"  )
    cmds.textField( "progressUpdate_fld", text=" ... ", width=100)
    cmds.progressBar( "progressControl_grp", maxValue=100, width=220  )             
    cmds.setParent( ".." )
    cmds.setParent( ".." ) 

    updateUI( ds.objectName )
    cmds.showWindow( "mzFishToolWindow" )
#-----------------------------------------------------------
# HELPFULL FUNCTIONS
#-----------------------------------------------------------
def getDAGPath( mesh ):
    try:
        selectionList = om.MSelectionList()
        selectionList.add( mesh )
        nodeDagPath = selectionList.getDagPath(0)
    except:
        raise RuntimeError('could node find dag path for %s' % mesh)
    return nodeDagPath
#----------------------------------------------------------------------------------------------------
# CLASS DECLARATIONS
#----------------------------------------------------------------------------------------------------
class DefaultFishSettings:
    def __init__(self):
        self.objectName = 'fish1'
        self.meshName = '...'
        self.pathName = '...'
        self.speed = 40.0
        self.numberOfJoints = 10
        self.numberOfControls = 10
        self.numberOfHandles = 2
        self.rigLength = 0.0
        self.length = 0.0
        self.start = 0.0
        self.end = 400.0
        self.waveLengths = 1.0
        self.waveAmplitude = 1.50
        self.waveRate = 1.3 
        self.tailAmplitude = 8.0
        self.tailFlex = 0.5
        self.effort = 1.0
        self.pathUValue = 0.0 
        self.precision = 1.0  
        self.preActive = False 
        self.useSelectedJoints = False  
        self.sideFinRotation = 20.0
        self.sideFinRotShift = 0.0
        self.sideFinTimeShift = 0.0 
        self.display_L = "display_L"

class FishToolUI:
    'settings for each individual Fish'
    def __init__(self):        
        self.objectName = cmds.textFieldGrp( "objectName_grp", query=True, text=True )
        self.meshName = cmds.textFieldGrp( "meshName_grp", query=True, text=True )
        #self.useSelectedJoints = cmds.checkBox( "useSelectedJoints_chb", query=True, v=True )
        self.useSelectedJoints = False
        self.pathName = cmds.textFieldGrp( "pathName_grp", query=True, text=True )
        self.speed = cmds.floatFieldGrp( "speed_grp", query=True, v1=True ) 
        self.numberOfJoints = cmds.intFieldGrp( "numberOfJoints_grp", query=True, v1=True )
        self.numberOfControls = cmds.intFieldGrp( "numberOfControls_grp", query=True, v1=True )
        #self.numberOfHandles = cmds.intFieldGrp( "numberOfHandles_grp", query=True, v1=True )
        self.rigLength = cmds.floatField( "rigLength_grp", query=True, v=True )
        self.length = cmds.floatFieldGrp( "length_grp",query=True,v1=True )
        self.start = cmds.floatFieldGrp( "startTime_grp", query=True, v1=True )
        self.end =  cmds.floatFieldGrp( "endTime_grp", query=True, v1=True )
        self.waveLengths = cmds.floatFieldGrp( "waveLengths_grp", query=True, v1=True )
        self.waveAmplitude = cmds.floatFieldGrp( "waveAmplitude_grp", query=True, v1=True )
        self.waveRate = cmds.floatFieldGrp( "waveRate_grp", query=True, v1=True )
        self.tailAmplitude = cmds.floatFieldGrp( "tailAmplitude_grp", query=True, v1=True )
        self.tailFlex = cmds.floatFieldGrp( "tailFlex_grp", query=True, v1=True )
        self.effort = cmds.floatFieldGrp( "effort_grp", query=True, v1=True )
        self.preActive = cmds.checkBox( "preActive_chb",query=True,v=True )
        self.precision = cmds.floatFieldGrp( "precision_grp",query=True,v1=True )
        self.preStart = cmds.floatField( "preStart_grp",query=True,v=True )
        self.preEnd = cmds.floatField( "preEnd_grp",query=True,v=True )

    def set_objectName( self,objectName ):
        self.objectName = objectName 
        cmds.textFieldGrp( "objectName_grp", edit=True, text=objectName )
                
    def set_meshName( self,meshName ):
        self.meshName = meshName
        cmds.textFieldGrp( "meshName_grp",edit=True,text=meshName ) 
        
    def set_pathName(self,pathName):
        self.pathName = pathName
        cmds.textFieldGrp( "pathName_grp",edit=True,text=pathName ) 
    
    def set_rigLength(self,rigLength):
        self.rigLength = rigLength
        cmds.floatField("rigLength_grp",edit=True,value=rigLength) 
        
    def set_length(self,length):
        self.length = length
        cmds.floatFieldGrp("length_grp",edit=True,value1=length)    
    
    def set_numberOfJoints(self,numberOfJoints):
        self.numberOfJoints = numberOfJoints
        cmds.intFieldGrp( "numberOfJoints_grp", edit=True, v1=numberOfJoints )
        
    def set_numberOfControls(self,numberOfControls): 
        self.numberOfControls = numberOfControls   
        cmds.intFieldGrp( "numberOfControls_grp", edit=True, v1=numberOfControls )
            
    def rigLengthEnabled(self):
        return cmds.floatField("rigLength_grp",query=True,enable=True)
        
    def enableRigLengthField(self):
        if self.rigLengthEnabled():
            cmds.floatField("rigLength_grp",edit=True,enable=False)
        else:
            cmds.floatField("rigLength_grp",edit=True,enable=True)  
    
    def set_endTime(self,t):
        self.end = t
        cmds.floatFieldGrp( "endTime_grp", edit=True, v1=t )         

class ControlNames:
    def __init__(self,ui):
        self.objectName = ui.objectName
        self.numberOfJoints = ui.numberOfJoints
        self.numberOfControls = ui.numberOfControls
        #self.numberOfHandles = ui.numberOfHandles
        self.skeletonGrp = '%s_skeleton' % ui.objectName
        self.controlGrp = '%s_controls' % ui.objectName
        self.handleName = 'spine_CTRL'
        self.skinClusterName = "%s_skinCluster" % ui.objectName
        self.pathName = '%s_path' % ui.objectName
        self.mPathName = '%s_mPath' % ui.objectName   # motion path names
        self.ctrlPositions = '%s_ctrlPositions' % ui.objectName
        self.ctrlCurve = '%s_ctrlCurve' % ui.objectName
        self.pathUValue = '%s.pathUValue' % ui.objectName
        self.pathCtrl = 'ctrl_'
        self.posCtrl = 'ctrl_pos_'
        self.skelCtrl = 'ctrlJN_'
        self.headTrnCtrl = 'head_TRN_CTRL'
        self.frontTwistCtrl = 'twist_FRONT_CTRL'
        self.backTwistCtrl = 'twist_BACK_CTRL'
        self.expName_uValues = '%s_exp_uValues' % ui.objectName
        self.expName_twistControls = '%s_exp_twistControls' % ui.objectName
        self.waveLengths = '%s.waveLengths' % ui.objectName
        self.waveAmplitude = '%s.waveAmplitude' % ui.objectName
        self.waveRate = '%s.waveRate' % ui.objectName
        #self.tailAmplitude = '%s.tailAmplitude' % ui.objectName
        #self.tailFlex = '%s.tailFlex' % ui.objectName
        #self.effort = '%s.effort' % ui.objectName
    
    
    #def getHeadJointName(self):
    #    return ('%s|%s|ctrl_0|%s|%s_head' % (self.objectName,self.controlGrp,self.headTrnCtrl,self.objectName) )  
        
    #def getHeadTrnCtrlName(self):
    #    return ('%s|%s|ctrl_0|%s' % (self.objectName,self.controlGrp,self.headTrnCtrl) )        
    
    def getJointNames(self): 
        jointNames = []
        name = "%s|%s|joint1" % (self.objectName,self.skeletonGrp)
        jointNames.append( name )
        for n in range(2,self.numberOfJoints+1):
            name += "|joint%i" % (n)
            jointNames.append( name )
        return jointNames
            
    def getPathControlNames(self):
        pathCtrls = []
        for n in range(0,self.numberOfControls):
            pathCtrls.append( '%s|%s|%s%i' % (self.objectName,self.controlGrp,self.pathCtrl,n) )
        return pathCtrls 

    def getCtrlPosNames(self):
        posCtrls = []
        for n in range(0,self.numberOfControls):
            posCtrls.append( '%s|%s|%s%i|%s%i' % (self.objectName,self.controlGrp,self.pathCtrl,n,self.posCtrl,n  ))
        return posCtrls    
    
    def getCtrlJointNames(self):
        skelCtrls = []
        for n in range(0,self.numberOfControls):
            #skelCtrls.append( '%s|%s|%s%i|%s%i|%s%i' % (self.objectName,self.controlGrp,self.pathCtrl,n,self.posCtrl,n,self.skelCtrl,n)  )
            skelCtrls.append( '%s|%s|%s%i|%s%i' % (self.objectName,self.controlGrp,self.pathCtrl,n,self.skelCtrl,n)  )
        return skelCtrls  
    
    def getSpineHandleNames(self):
        names = []
        for n in range(0,self.numberOfHandles):
            names.append( 'spine_CTRL%i' % (n+1) )
        return names
            
    def getMotionPathNames(self):
        mPathNames = []
        for n in range(0,self.numberOfControls):
            mPathNames.append( '%s%i' % (self.mPathName,n+1) )
        return mPathNames 

class PathManager:
    def __init__(self,ui):
        pathName = ui.pathName
        nodeDagPath = getDAGPath( pathName )
        self.crvFn = om.MFnNurbsCurve(nodeDagPath)
        self.pathLength = self.crvFn.length()
        self.paramLength = self.crvFn.findParamFromLength(self.pathLength) 
        self.distance = 0.0
        self.prevDist = 0.0
        self.dDist = 0.0            # distance from prev .position to current .position
        self.position = 0.0         # distance along the path
        self.direction = 0.0        # path direction at current .position   

    def setInitialPosition(self,puv):
        self.distance = puv*self.pathLength
        
    def getPathPosition(self):      # distance along the path
        return self.position
        
    def getPathDirection(self):     # path direction at current .position   
        return self.direction

    def getDistanceMoved(self):
        return self.dDist
        
    def getDistanceAtUValue(self,puv):
        return puv*self.pathLength    
        
    def convertToLocalSpace(self,dir,vec):
        up = om.MVector(0,1,0)
        tan = dir^up
        x = dir*vec
        z = tan*vec
        return om.MVector(x,0,z)
                
    def getCtrlDirection(self,ctrlPos):
        distance = self.distance - ctrlPos
        parameter = self.crvFn.findParamFromLength(distance)
        dir = self.crvFn.tangent(parameter, om.MSpace.kWorld)
        return dir

    def getCtrlPathPos(self,ctrlPos):
        length = self.distance - ctrlPos
        param = self.crvFn.findParamFromLength(length)
        return self.crvFn.getPointAtParam(param, om.MSpace.kWorld)

    def getTurnValue(self,ctrlPos0,endCtrlPos):
        half = (endCtrlPos - ctrlPos0)/2.0 + ctrlPos0 
        #dir0 = self.direction
        dir1 = self.getCtrlDirection(half)
        dir2 = self.getCtrlDirection(endCtrlPos)
        #head = dir0*dir1
        #tail = dir1*dir2
        #angle1 = cmds.angleBetween(euler=False,v1=dir0,v2=dir1)[3]
        angle2 = cmds.angleBetween(euler=False,v1=dir1,v2=dir2)[3]
        #old = 1.0 - head/tail
        turnValue = angle2/90.0
        return turnValue 

    def getTurnSide(self,ctrlPos,side):
        # returns true if  
        norm = self.direction^om.MVector(0,1,0)
        vec = self.getCtrlPathPos(ctrlPos) - self.position 
        d = norm*vec
        #print (d)
        if d > 0 and side > 0:
            return -1        # inside
        elif d < 0 and side < 0:
            return -1        # inside
        return +1            # outside
     
    def moveAlongPath(self,puv):  # d is distance along the path
        self.prevDist = self.distance
        self.distance = puv*self.pathLength
        self.dDist = self.distance - self.prevDist
        parameter = self.crvFn.findParamFromLength(self.distance)
        self.position = self.crvFn.getPointAtParam(parameter, om.MSpace.kWorld) 
        self.direction = self.crvFn.tangent(parameter, om.MSpace.kWorld)
        if self.distance >= self.pathLength:
            return True    # return True when end of path is reached
        return False
 
class Physics:
    def __init__(self):
        ds = DefaultFishSettings()
        ui = FishToolUI()
        dragCoefficient = 0.03     #ui.dragCoefficient
        waterDensity = 0.000997                  # (cm/m^3)  == 997 kg/m^3 
        fishMass = 0.5                           # kg
        fishArea = 50.0                          # cm^2
        self.dragMultiplier = (dragCoefficient*waterDensity*fishArea)/(2.0*fishMass) 
        #self.fps = ui.fps                          # frame rate (frames/sec)

    def getDrag(self,vel):
        return self.dragMultiplier*vel*vel    

class SideFin:
    def __init__(self,jn,pcn,pcp,jcn):
        self.jointName = jn
        self.pathCtrlName = pcn
        self.ctrlPos = pcp
        self.jointCtrlName = jcn
        self.side = 0

    def display(self):
        print(self.jointName)
        print(self.pathCtrlName)
        print(self.ctrlPos)
        print(self.jointCtrlName)
        print(self.side)
              
class SideFinManager:
    def __init__(self,finJoints):
        self.ui = FishToolUI()
        cn = ControlNames(self.ui)
        self.pm = PathManager(self.ui)

        self.skeletonGrp = '%s_skeleton' % self.ui.objectName
        self.pathCtrlNames = cn.getPathControlNames() 
        self.ctrlJointNames = cn.getCtrlJointNames() 
        self.jointNames = cn.getJointNames()
        self.numberOfControls = len(self.pathCtrlNames)
        
        #self.ctrlPos = []
        self.ctrlPos = getControlPositions(cn.ctrlPositions, self.ui)
        self.sideFins = self.getSideFins( finJoints )
        #self.currentFrame = cmds.currentTime(q=True)

    def getClosest(self,node,nodes,t):
        closest = 0
        min_dist = self.getDistanceBetween(nodes[0],node,t)
        for n in range(1,len(nodes)):
            dist = self.getDistanceBetween(nodes[n],node,t)
            if dist < min_dist:
                min_dist = dist
                closest = n
        return closest        
        
    def getSideFins(self,finJoints):
        t = cmds.currentTime(q=True)
        sideFins = []
        # find the closest controls to the fin joint
        for fin in finJoints:
            i = self.getClosest(fin,self.ctrlJointNames,t)
    
            pcn = self.pathCtrlNames[i] 
            jcn = self.ctrlJointNames[i]
            pcp = self.ctrlPos[i]
            sideFin = SideFin(fin,pcn,pcp,jcn )
            sideFin.side = self.getFinSideOfBody( fin )
            sideFins.append(sideFin)
        return sideFins     

    def getFinSideOfBody(self,fin): # need finPos,ctrlPos
        t = cmds.currentTime(q=True)
        i = self.getClosest(fin,self.jointNames,t)
        # get joint direction
        if i < len(self.jointNames)-1:
            dir = self.getVector(self.jointNames[i],self.jointNames[i+1],t)
        else:
            dir = self.getVector(self.jointNames[i-1],self.jointNames[i],t)    
        yAxis = om.MVector(0,1,0)
        cross = dir^yAxis
        #print (fin.jointNames)
        #print (type(fin.jointName))
        #print (self.jointNames[i])
        #print (type(self.jointNames[i]))
        wp = getWorldSpacePositionAtTime(fin,t) 
        jp = getWorldSpacePositionAtTime(self.jointNames[i],t)
        vec = (wp - jp).normal()
        
        dot = vec*cross
        if dot >= 0:
            return 1
        return -1
          
    def getDistanceBetween(self,node1,node2,t):
        n1_pos = getWorldSpacePositionAtTime(node1,t)
        n2_pos = getWorldSpacePositionAtTime(node2,t)
        return (n2_pos-n1_pos).length()

    def getVector(self,node1,node2,t):
        n1_pos = getWorldSpacePositionAtTime(node1,t)
        n2_pos = getWorldSpacePositionAtTime(node2,t)
        return (n2_pos-n1_pos).normal()

    def getKeyValueRange(self,kv):
        min = kv[0]
        max = kv[0]
        for n in kv:
            if n > max:
                max = n
            if n < min:
                min = n
        return max - min


class AnimationManager:
    def __init__(self):
        self.ui = FishToolUI()
        self.cn = ControlNames(self.ui)
        self.pm = PathManager(self.ui) 
        self.physics = Physics()       

        self.pathName = self.ui.pathName
        pathShapeNode = cmds.listRelatives(self.pathName, shapes=True)[0]
        self.crvFn = om.MFnNurbsCurve(getDAGPath(pathShapeNode)) 
        self.pathLength = self.crvFn.length()
        self.path_uValue = self.cn.pathUValue
        self.objectName = self.ui.objectName
        self.numberOfJoints = self.ui.numberOfJoints
        self.numberOfControls = self.ui.numberOfControls
        self.rigLength = self.ui.rigLength
        self.length = getLength( self.objectName )
  
        self.ctrlNames = self.cn.getCtrlJointNames()   # control names used for keying
        #self.ctrlPosNames = self.cn.getCtrlPosNames()

        self.paramLength = self.crvFn.findParamFromLength(self.pathLength) 

        #self.ctrlPos = []
        self.ctrlPos = getControlPositions(self.cn.ctrlPositions, self.ui)

        self.delay = []                      # controls distance behind 1st control
        self.amplitude = []                  # controls maximum sidewards movement
     
        self.nDist = []                      # controls current distance along movement cycle
        self.nSide = []                      # side to side movement (which side for ontrols next key)
        self.wAmp = []                       # controls sidewards movement for it's next key
        self.cycDist = []                    # movement distance until this controls next key
        
        #self.dz = []                         # temp precision setting
        #self.tz = []
        self.preActive = self.ui.preActive
        self.precision = self.ui.precision
        self.preStart = self.ui.preStart
        self.preEnd = self.ui.preEnd
        
        self.waveLengths = 1.0
        self.waveAmplitude = 1.0
        self.waveRate = 1.0
        self.tailAmplitude = self.ui.tailAmplitude
        self.tailFlex = self.ui.tailFlex
        self.effort = self.ui.effort
        self.initializeMovementSettings()   
        
        self.FishHasStopped = False
        self.FishHasStarted = False
        
        self.curVel = 0.0
        self.prevVel = 0.0
        self.prevTime = 0.0
        self.fps = 25.0
        #self.prevTurnValue = 0.0

    def initializeMovementSettings(self):
        # calculate control positions for each control
        #ctrlPos = []
        #ctrlPositionsCurve = self.cn.ctrlPositions
        ctrlPos = getControlPositions(self.cn.ctrlPositions,self.ui)
 
        # set initial delay offset distances for each control  
        for n in range(self.numberOfControls):
            self.delay.append( ctrlPos[n] ) 

        # calculate maximum side movement for each ctrl
        #initialWaveAmplitude = (self.numberOfJoints * self.rigLength) * 0.06
        #tail = self.ui.tailAmplitude           # amount of tail movement
        #flex = self.ui.tailFlex                # proportion of body where tail movement extends
        #initialWaveAmplitude = self.length * 0.06
        for n in range(0,self.numberOfControls):
            i = clamp((ctrlPos[n]/ctrlPos[self.numberOfControls-1]-self.tailFlex)/(1.0-self.tailFlex),0.0,1.0)
            amp = (1.0 - (1.0 - float(i)**2))*self.tailAmplitude + 1.0
            self.amplitude.append(amp)

    def initializePrecision(self):
        pass
        #self.curVel = 0.0
        #self.prevVel = 0.0
        #self.prevTime = 0.0
        #for n in range(self.numberOfControls):
        #    self.dz.append(0.0)
        #    self.tz.append(0.0)
            
    def updatePrecision(self,t,tt):
        df = t - self.prevTime
        dt = df/self.fps
        self.prevTime = t
        
        self.moveAlongPath(t)
        dDist = self.pm.getDistanceMoved()
        self.curVel = dDist/dt
        a = (self.curVel - self.prevVel)/dt
        self.prevVel = self.curVel
        
        if a > 0.0:
            accelRate = 1.0 + (a*self.effort)/(self.length*4.0) #4.0 just looks good
        else:
            accelRate = 1.0    
        dCycleDist = self.pm.getDistanceMoved()*accelRate*self.waveRate
        turnValue = self.pm.getTurnValue(self.ctrlPos[0],self.ctrlPos[self.numberOfControls-1])

        for n in range(self.numberOfControls):
            tempCycDist = self.cycDist[n]
            if self.cycDist[n] == -1:
                tempCycDist = self.cycDist[0]

            # if this time t is in the add keyframes time period, add keyframes if necessary
            if self.preActive or (t >= self.preStart and t <= self.preEnd):
                #sideMovement = math.cos( (self.delay[n]/swimCycleDistance)*math.pi ) * self.amplitude[n] * self.waveAmplitude
                tz = -self.nSide[n] * math.cos( (self.nDist[n]/tempCycDist)*math.pi ) * self.amplitude[n] * self.wAmp[n]
                if tz > 0: 
                    tz = tz + turnValue*tz
                else:
                    tz = tz - turnValue*tz
                dz = cmds.getAttr( '%s.translateZ' % self.ctrlNames[n], t=(t) )
                d = abs(tz - dz)
                allreadyKeyed = cmds.selectKey('%s.translateZ' % self.ctrlNames[n], add=True,k=True,t=(t,t))
                if not allreadyKeyed and d > self.precision:
                    cmds.setKeyframe( self.ctrlNames[n], time=(t,t), attribute='translateZ', value=tz )
                    cmds.keyTangent( self.ctrlNames[n], time=(t,t), itt=tt, ott=tt )  

            self.nDist[n] += dCycleDist

            if self.nDist[n] >= self.cycDist[n] and self.cycDist[n] != -1:
                if n == 0:
                    for i in range(1,self.numberOfControls):
                        if self.cycDist[i] == -1:
                            self.cycDist[i] = self.cycDist[0]
                
                self.nSide[n] = self.switchSides( self.nSide[n] )
                self.nDist[n] = self.nDist[n] - self.cycDist[n]
                
                if n < self.numberOfControls-1:  
                    self.wAmp[n+1] = self.wAmp[n]
                    
                if self.delay[n] < self.nDist[0]:
                    self.cycDist[n] = -1
                else:
                    self.cycDist[n] = self.cycDist[n-1] 
               
    
    def updateAnimationSettings(self,t):
        self.waveLengths = cmds.getAttr( "%s.waveLengths" % self.objectName, t=(t) )
        self.waveAmplitude = cmds.getAttr( "%s.waveAmplitude" % self.objectName, t=(t) )
        self.waveRate = cmds.getAttr( "%s.waveRate" % self.objectName, t=(t) ) 
        #self.tailAmplitude = cmds.getAttr( "%s.tailAmplitude" % self.objectName, t=(t) ) 
        #self.tailFlex = cmds.getAttr( "%s.tailFlex" % self.objectName, t=(t) ) 
        #self.effort = cmds.getAttr( "%s.effort" % self.objectName, t=(t) ) 
   
    def switchSides( self,side ):
        if side == 1:
            return -1
        else:
            return 1
        
    def setInitialPosition(self,t):
        # create keyframes for Fishs starting position
        uValue = self.getPathUValueAtTime(t)
        self.pm.setInitialPosition(uValue)
        self.updateAnimationSettings(t)
        swimCycleDistance = self.length/(self.waveLengths*2.0)
        uValueNext = self.getPathUValueAtTime(t+1)
        self.prevVel = (self.pm.getDistanceAtUValue(uValueNext)-self.pm.getDistanceAtUValue(uValue))/(1.0/self.fps)
        self.prevTime = t
  
        for n in range(self.numberOfControls):
            self.nDist.append( swimCycleDistance - self.delay[n]%swimCycleDistance )
            self.wAmp.append( self.waveAmplitude )
            self.cycDist.append( swimCycleDistance )
            # save which side the control is currently on
            s = 1
            numberOfCycles = 1
            while self.delay[n] >= (numberOfCycles * swimCycleDistance):
                numberOfCycles += 1
                s = self.switchSides( s )
            self.nSide.append( s ) 
            
            sideMovement = math.cos( (self.delay[n]/swimCycleDistance)*math.pi ) * self.amplitude[n] * self.waveAmplitude
            cmds.setKeyframe( self.ctrlNames[n], time=(t,t), attribute='translateZ', value=sideMovement )
            cmds.keyTangent( self.ctrlNames[n], time=(t,t), itt='linear', ott='linear' )

    
    def FishHasStoppedMoving(self):
        if self.FishHasStopped:
            print ('Stopped------------------------------')
            return True
        return False
        
    def FishHasStartedMoving(self):
        if self.FishHasStarted:
            print ('Started------------------------------')
            self.FishHasStarted = False
            return True
        return False

    def keyAllControlsAtTime(self,t,tt):
        cycleDist = []
        for n in range(self.numberOfControls):
            cycleDist.append( self.cycDist[n] )
            if self.cycDist[n] == -1:
                cycleDist[n] = self.cycDist[0]
        
        for n in range(self.numberOfControls):
            sideMovement = self.nSide[n] * math.cos( (self.nDist[n]/cycleDist[n])*math.pi ) * self.amplitude[n] * self.wAmp[n] #waveAmplitude
            cmds.setKeyframe( self.ctrlNames[n], time=(t,t), attribute='translateZ', value=sideMovement )
            cmds.keyTangent( self.ctrlNames[n], time=(t,t), itt=tt, ott=tt )         
               
    def updateFishMovement(self,dist):        
        if dist <= 0.0:
            self.FishHasStopped = True
        else:    
            if self.FishHasStopped:
                self.FishHasStarted = True
                self.FishHasStopped = False

    def getPathUValueAtTime(self,t):
        return cmds.getAttr( self.path_uValue, t=t)

    def moveAlongPath(self,t):
        uValue = self.getPathUValueAtTime(t)
        self.pm.moveAlongPath(uValue)
        self.updateAnimationSettings(t)    # update current waveLength,waveAmplitude,waveRate
        self.wAmp[0] = self.waveAmplitude
        self.cycDist[0] = self.length/(self.waveLengths*2.0) # *waveRate

    def update(self,t):
        df = t - self.prevTime          # change in time (in frames)
        dt = df/self.fps                # change in time (in seconds)
        self.prevTime = t
        
        self.moveAlongPath(t)
      
        dDist = self.pm.getDistanceMoved()
        self.curVel = dDist/dt
        a = (self.curVel-self.prevVel)/dt 
        #dr = self.physics.getDrag(self.curVel)
        self.prevVel = self.curVel

        # increase the rate as it accelerates (extra effort to get moving)  
        if a > 0.0:
            accelRate = 1.0 + (a*self.effort)/(self.length*4.0) #4.0 just looks good
        else:
            accelRate = 1.0    
        dCycleDist = self.pm.getDistanceMoved()*accelRate*self.waveRate
        self.updateFishMovement(dCycleDist)      # update .FishHasStopped/Started
        
        # update the movement distance for each control
        for n in range(self.numberOfControls):
            self.nDist[n] += dCycleDist
        
        # turnValue represents how much of a turn and at what stage of a turn      
        turnValue = self.pm.getTurnValue(self.ctrlPos[0],self.ctrlPos[self.numberOfControls-1])
        #self.prevTurnValue = turnValue    
        
        for n in range(self.numberOfControls):
            if self.nDist[n] >= self.cycDist[n] and self.cycDist[n] != -1:
                # update any controls waiting for a cycDist
                if n == 0:
                    for i in range(1,self.numberOfControls):
                        if self.cycDist[i] == -1:
                            self.cycDist[i] = self.cycDist[0]    
                
                sideMovement = 0.0 + self.nSide[n] * self.amplitude[n] * self.wAmp[n] 
                sideMovement = sideMovement + self.nSide[n]*turnValue*sideMovement

                #cmds.setKeyframe( self.ctrlPosNames[n], time=(t,t), attribute='translateX', value=pos.x )
                #cmds.setKeyframe( self.ctrlPosNames[n], time=(t,t), attribute='translateZ', value=pos.z )
                #cmds.keyTangent( self.ctrlPosNames[n], time=(t,t), itt='flat', ott='flat' ) 

                # key side movement
                #cmds.setKeyframe( self.ctrlNames[n], time=(t,t), attribute='translateX', value=0.0 )
                cmds.setKeyframe( self.ctrlNames[n], time=(t,t), attribute='translateZ', value=sideMovement )
                cmds.keyTangent( self.ctrlNames[n], time=(t,t), itt='flat', ott='flat' ) 

                # **** -------------------------------------------     
                self.nSide[n] = self.switchSides( self.nSide[n] )
                self.nDist[n] = self.nDist[n] - self.cycDist[n]
                
                # update control amplitudes to follow movement of control in front
                if n < self.numberOfControls-1:  
                    self.wAmp[n+1] = self.wAmp[n] 
                
                # cycDist[0] changes each frame so wait for it to key before setting following cycDist's
                if self.delay[n] < self.nDist[0]:
                    self.cycDist[n] = -1
                else:
                    self.cycDist[n] = self.cycDist[n-1] 
                                           
class uValueKey:
    def __init__(self,t,value,itt,ott):
        self.t = t
        self.value = value
        self.itt = itt
        self.ott = ott

#-----------------------------------------------------------------------------
# Dialog Boxes
#-----------------------------------------------------------------------------
def errorMessage( msg ):
    cmds.confirmDialog( title=" ", message=msg, button="OK", defaultButton="OK", cancelButton="OK", dismissString="OK")

def yesNoDialogBox( msg ):
    return cmds.confirmDialog( title=" ", message=msg, button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
#-----------------------------------------------------------------------------
# Progress Bar Functions
#-----------------------------------------------------------------------------
def progressControl():
    cmds.progressBar("progressControl_grp",edit=True, step=1)
def resetProgressControl():
    cmds.progressBar("progressControl_grp",edit=True, progress=0)
def setProgressControlMaxValue( maxValue ):
    cmds.progressBar("progressControl_grp",edit=True, maxValue=maxValue) 
def progressControlUpdate( textUpdate ):
    cmds.textField("progressUpdate_fld",edit=True,text=textUpdate)         
#-----------------------------------------------------------------------------
def checkWorkingUnits():
    workingUnits = cmds.currentUnit( query=True, linear=True )
    if workingUnits != "cm":
        msg = "mzFishTool requires Working Units set to centimeter\nIs it ok to reset working units to centimeter?";
        ok = cmds.confirmDialog( title="Working Units", message=msg, button=['Yes','No'], defaultButton="Yes", cancelButton="No", dismissString="No")
        if ok=='Yes':
            cmds.currentUnit( linear="cm") 
        return ok      
#-----------------------------------------------------------------------------
# UI - functions
#-----------------------------------------------------------------------------
def updateMeshField( args ):
    ui = FishToolUI()
    mesh = selectMesh()
    if mesh:
        objectName = ui.objectName
        meshName = "%s_mesh" % objectName
        mesh = cmds.rename( mesh, meshName )
        ui.set_meshName( mesh )
        length = getLengthOfMesh( mesh )
        ui.set_length( length )
        ui.set_rigLength( length )
        updateButtons()

def updatePathField(args):
    ui = FishToolUI()
    path = selectPath()
    if path:
        ui.set_pathName( path ) 

def selectMesh():
    selection = cmds.ls( sl=True )
    if len(selection) == 0:
        errorMessage("Select a mesh for the fish's body!")
        return None
    if not checkTypeIs(selection[0],'mesh'):
        errorMessage("Select a Mesh")
        return None
    return getTransformNode(selection[0])    

def selectPath():
    selection = cmds.ls( sl=True )
    if len(selection) == 0:
        errorMessage("Select a path for the fish to move along!")
        return None
    if not checkTypeIs(selection[0],'nurbsCurve'):
        errorMessage("Select a Curve for the fish's path!")
        return None
    return getTransformNode(selection[0])  
    
def addItemsToMenu( oMenu, menuList ):
    # delete existing menus in the optionMenu
    for item in cmds.optionMenu(oMenu, q=True, ill=True): # or []:
        cmds.deleteUI(item)
    
    # add selected items to the menu
    cmds.menuItem( label="... selected ...", parent=oMenu )
    for item in menuList:
        cmds.menuItem(label = item, enable=False, parent=oMenu)
    cmds.optionMenu( oMenu, e=True, enable=True ) 
    
def selectFinJoints( args ):
    selection = cmds.ls( sl=True, l=True )
    oMenu = cmds.optionMenu( "finJoints_menu", query=True, fullPathName=True )
    addItemsToMenu( oMenu,selection )
    updateButtons()
    
def selectTime(UIGrp):
    t = cmds.currentTime( query=True )
    cmds.floatField( UIGrp, edit=True, v=t )
    
def updateTimeRange():
    speed = cmds.floatFieldGrp("speed_grp",query=True,value1=True)
    path = cmds.textFieldGrp("pathName_grp",query=True,text=True) 
    start = cmds.floatFieldGrp("startTime_grp",query=True,value1=True )
    end = cmds.floatFieldGrp("endTime_grp",query=True,value1=True )
    
    if cmds.objExists( path ):
        fps = 25 #cmds.currentUnit(query=True, time=True)
        pathLength = cmds.arclen( path )
        end = (pathLength/speed) * fps + start
    cmds.floatFieldGrp("endTime_grp",edit=True,v1=end)          

def clampTailFlex(args):
    input = cmds.floatFieldGrp("tailFlex_grp",query=True,value1=True)
    if input > 1.0:
        cmds.floatFieldGrp("tailFlex_grp",edit=True,value1=1.0) 
    if input < 0.0:
        cmds.floatFieldGrp("tailFlex_grp",edit=True,value1=0.0)            
        

def changeSpeedSetting(args):
    updateTimeRange()
    updatePathAnimation()

def changeTimeRange( args ):
    start = cmds.floatFieldGrp("startTime_grp",query=True,value1=True )
    end = cmds.floatFieldGrp("endTime_grp",query=True,value1=True )
    updateSpeedSetting(start,end)
    updatePathAnimation()

def updateSpeedSetting(start,end):    
    path = cmds.textFieldGrp("pathName_grp",query=True,text=True) 
    if cmds.objExists( path ):
        fps = 25
        pathLength = cmds.arclen( path )
        timeRange = end - start
        speed = pathLength*fps/timeRange
        cmds.floatFieldGrp("speed_grp",edit=True,value1=speed)

def updatePathAnimation():
    # if fish is attached to the path then update the path uValues
    ui = FishToolUI()
    cn = ControlNames(ui) 
    if cmds.objExists( cn.pathUValue ): 
        start = ui.start
        end = ui.end
        numberOfKeys = cmds.keyframe(cn.pathUValue,q=True,kc=True)
        if numberOfKeys < 2:
            errorMessage('Missing path U Value keyframes')
            return
        first = cmds.findKeyframe( cn.pathUValue, which='first' )
        last = cmds.findKeyframe( cn.pathUValue, which='last' ) 
        
        # shift the keyframes and then scale them
        amount = start - first
        cmds.keyframe( cn.pathUValue, t=(first,last), relative=True, timeChange=amount ) 
        cmds.keyframe( cn.waveLengths, t=(first,last), relative=True, timeChange=amount ) 
        cmds.keyframe( cn.waveAmplitude, t=(first,last), relative=True, timeChange=amount ) 
        cmds.keyframe( cn.waveRate, t=(first,last), relative=True, timeChange=amount ) 
        ts = (end-start)/(last-first)
        cmds.scaleKey( cn.pathUValue, timeScale=ts, timePivot=start, valueScale=1.0, valuePivot=0.0  ) 
        cmds.scaleKey( cn.waveLengths, timeScale=ts, timePivot=start, valueScale=1.0, valuePivot=0.0  ) 
        cmds.scaleKey( cn.waveAmplitude, timeScale=ts, timePivot=start, valueScale=1.0, valuePivot=0.0  ) 
        cmds.scaleKey( cn.waveRate, timeScale=ts, timePivot=start, valueScale=1.0, valuePivot=0.0  ) 
  
def changeObjectSetting( args ):
    objectName = cmds.textFieldGrp("objectName_grp",query=True,text=True)
    updateUI( objectName )
    if cmds.objExists(objectName):
        cmds.select(objectName)  

def enableRigLengthField( args ):
    ui = FishToolUI()
    ui.enableRigLengthField()

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
            
def checkEveryTypeIs(nodes,testType):
    for n in nodes:
        if not checkTypeIs(n,testType):
            return False
    return True
    
def getTransformNode(node):
    if cmds.objectType(node,isType='transform'):
        return node
    else:
        p = cmds.listRelatives(node,p=True)[0]
        if cmds.objectType(p,isType='transform'):
            return p
    return None

      
def getNumberOfJoints( objectName ):
    n = 1
    jointName = "%s|%s_skeleton|joint%i" % (objectName,objectName,n)
    numberOfJoints = 0 
    while cmds.objExists( jointName ):
        numberOfJoints += 1
        n += 1
        jointName += "|joint%i" % (n)
    return numberOfJoints

def getNumberOfControls( objectName ):
    n = 0
    ctrlName = "%s|%s_controls|ctrl_%i" % (objectName,objectName,n)
    numberOfControls = 0 
    while cmds.objExists( ctrlName ):
        numberOfControls += 1
        n += 1
        ctrlName = "%s|%s_controls|ctrl_%i" % (objectName,objectName,n)
    return numberOfControls

def calculateRigLength( objectName ):
    return getLength( objectName )               

def getLength( objectName ):
    ui = FishToolUI()
    cn = ControlNames(ui)
    ctrlPosCurve = cn.ctrlPositions
    length = cmds.arclen(ctrlPosCurve)
    return length

def updateUI( objectName ):
    if cmds.objExists( objectName ):
        meshName = "%s_mesh" % objectName
        pathName = "%s_path" % objectName
        if not cmds.objExists( meshName ):
            return
        cmds.textFieldGrp("meshName_grp",edit=True,text=meshName) 
        if cmds.objExists( pathName ):
            cmds.textFieldGrp("pathName_grp",edit=True,text=pathName)
            path_uValue = "%s.pathUValue" % objectName
            if cmds.objExists( path_uValue ):
                numberOfKeys = cmds.keyframe(path_uValue,q=True,kc=True)
                if numberOfKeys >= 2:
                    firstKeyframe = cmds.findKeyframe( path_uValue, which='first' )
                    lastKeyframe = cmds.findKeyframe( path_uValue, which='last' )
                    cmds.floatFieldGrp( "startTime_grp", edit=True, v1=firstKeyframe)
                    cmds.floatFieldGrp( "endTime_grp", edit=True, v1=lastKeyframe)
                    cmds.floatField( "preStart_grp",edit=True,v=firstKeyframe )
                    cmds.floatField( "preEnd_grp",edit=True,v=lastKeyframe )
                    updateSpeedSetting( firstKeyframe,lastKeyframe )
        try:            
            cmds.intFieldGrp( "numberOfJoints_grp", edit=True, v1=getNumberOfJoints(objectName) )
            cmds.intFieldGrp( "numberOfControls_grp", edit=True,v1=getNumberOfControls(objectName) ) 
            cmds.floatField( "rigLength_grp", edit=True, v=calculateRigLength(objectName) )
            cmds.floatFieldGrp( "length_grp",edit=True,v1=getLength(objectName) )
        except:
            return    
    else:
        ds = DefaultFishSettings()
        cmds.textFieldGrp("meshName_grp",edit=True,text=ds.meshName) 
        cmds.textFieldGrp("pathName_grp",edit=True,text=ds.pathName) 
        cmds.intFieldGrp( "numberOfJoints_grp", edit=True, v1=ds.numberOfJoints)
        cmds.intFieldGrp( "numberOfControls_grp", edit=True,v1=ds.numberOfControls) 
        cmds.floatField( "rigLength_grp", edit=True, v=ds.rigLength )
        cmds.floatFieldGrp( "startTime_grp", edit=True, v1=ds.start)
        cmds.floatFieldGrp( "endTime_grp", edit=True, v1=ds.end) 
        cmds.floatFieldGrp( "waveLengths_grp", edit=True,v1=ds.waveLengths ) 
        cmds.floatFieldGrp( "waveAmplitude_grp", edit=True,v1=ds.waveAmplitude )
        cmds.floatFieldGrp( "waveRate_grp", edit=True, v1=ds.waveRate ) 
        cmds.floatFieldGrp( "tailAmplitude_grp", edit=True, v1=ds.tailAmplitude ) 
        cmds.floatFieldGrp( "tailFlex_grp", edit=True, v1=ds.tailFlex ) 
        cmds.floatFieldGrp( "effort_grp", edit=True, v1=ds.effort ) 
         
    if cmds.objExists( "%s.waveLengths" % objectName ):
        cmds.connectControl('waveLengths_grp', '%s.waveLengths' % objectName, index=2 ) 
    if cmds.objExists( "%s.waveAmplitude" % objectName ):    
        cmds.connectControl( "waveAmplitude_grp", "%s.waveAmplitude" % objectName, index=2 ) 
    if cmds.objExists( "%s.waveRate" % objectName ):    
        cmds.connectControl( "waveRate_grp", "%s.waveRate" % objectName, index=2 )  
    #if cmds.objExists( "%s.tailAmplitude" % objectName ):    
    #    cmds.connectControl( "tailAmplitude_grp", "%s.tailAmplitude" % objectName, index=2 ) 
    #if cmds.objExists( "%s.tailFlex" % objectName ):    
    #    cmds.connectControl( "tailFlex_grp", "%s.tailFlex" % objectName, index=2 ) 
    #if cmds.objExists( "%s.effort" % objectName ):    
    #    cmds.connectControl( "effort_grp", "%s.effort" % objectName, index=2 )       
    if cmds.objExists( "%s.pathUValue" % objectName ):    
        cmds.connectControl( "pathUValue_grp", "%s.pathUValue" % objectName, index=2 ) 
    updateButtons()

def updateButtons():
    ui = FishToolUI()
    cn = ControlNames(ui)
    objectName = cmds.textFieldGrp("objectName_grp",query=True,text=True)
    #reset all buttons to grey
    cmds.button("createRig_btn",edit=True,bgc=(0.365,0.365,0.365))  
    cmds.button("attachRig_btn",edit=True,bgc=(0.365,0.365,0.365))    
    cmds.button("attachFishToPath_btn",edit=True,bgc=(0.365,0.365,0.365)) 
    cmds.button("animate_btn",edit=True,bgc=(0.365,0.365,0.365)) 
    # find which button should be green
    if not cmds.objExists( cn.skeletonGrp ):
        cmds.button("createRig_btn",edit=True,bgc=(0.1,0.5,0.3))
        cmds.frameLayout( 'rigging_grp',edit=True, collapse=False ) 
        return
    if not cmds.objExists( cn.skinClusterName ):
        cmds.button("attachRig_btn",edit=True,bgc=(0.1,0.5,0.3)) 
        cmds.frameLayout( 'rigging_grp',edit=True, collapse=False ) 
        return   
    if not cmds.objExists( '%s1' % cn.mPathName ):
        cmds.button("attachFishToPath_btn",edit=True,bgc=(0.1,0.5,0.3)) 
        cmds.frameLayout( 'rigging_grp',edit=True, collapse=False ) 
        return
    cmds.frameLayout( 'rigging_grp',edit=True, collapse=True ) 
    cmds.frameLayout( 'animationSettings_grp',edit=True, collapse=False )    
    cmds.button("animate_btn",edit=True,bgc=(0.1,0.5,0.3))  
#-----------------------------------------------------------------------------             
# Helper Functions
#-----------------------------------------------------------------------------      
def clamp(x,min_value,max_value):
    return max(min(x, max_value), min_value) 
    
def getWorldSpacePositionAtTime(ctrl,t):     
    worldMatrix = om.MMatrix(cmds.getAttr(ctrl+'.worldMatrix[0]', time=t))
    rotPiv = cmds.getAttr(ctrl+'.rotatePivot', time=t)[0]
    rotPivVec = om.MPoint(rotPiv[0], rotPiv[1], rotPiv[2], 1.0)
    rotPivWorld = rotPivVec * worldMatrix
    return om.MVector(rotPivWorld.x,rotPivWorld.y,rotPivWorld.z)                  

#-----------------------------------------------------------------------------             
# DELETE Fish
#-----------------------------------------------------------------------------               
def DeleteAll( args ):
    progressControlUpdate("... DeleteAll() ...")
    objectName = cmds.textFieldGrp("objectName_grp",query=True, text=True)
    if cmds.objExists( objectName ):
        cmds.delete( objectName ) 
#-----------------------------------------------------------------------------             
# Helper Functions FOR CREATE RIG
#-----------------------------------------------------------------------------             
def getLengthOfMesh( meshName ):
    # get the mesh bounding box
    bb = cmds.polyEvaluate( meshName,b=True )
    xLength = bb[0][1] - bb[0][0]
    zLength = bb[2][1] - bb[2][0] 
    # make sure mesh is aligned with positive x-axis
    if zLength > xLength:
        errorMessage( "mesh position error: Make sure Fish is aligned along the positive x-axis")
        return 0
    if abs(bb[0][1]) > abs(bb[0][0]):  # if abs(xMax) > abs(xMin)
        errorMessage( "mesh position error: See instructions for mesh positioning" )
        return 0 
    return abs(bb[0][0]) # length from neck to tail  

def createMeshBackup( objectName,bodyName ):
    #create a layer for the backup copy
    origBodyLayer = "Fish_meshOrig_L"
    if not cmds.objExists( origBodyLayer ):
        cmds.createDisplayLayer( name=origBodyLayer, number=1, empty=True) 
    
    #create the backup copy
    origBodyName = "%s_mesh_orig" % objectName    
    if not cmds.objExists( origBodyName ): 
        cmds.duplicate( bodyName, n=origBodyName )
        cmds.editDisplayLayerMembers( origBodyLayer, origBodyName, noRecurse=True ) 

def updateMesh( ui,mesh ):
    objectName = ui.objectName
    meshName = "%s_mesh" % objectName
    meshOrig = "%s_mesh_orig" % objectName
    meshLayer = "Fish_mesh_L"
    
    if cmds.objExists( mesh ):
        cmds.rename( mesh, meshName )
    
    # create a backup copy of the skin mesh
    if not cmds.objExists( meshOrig ):
        createMeshBackup(objectName,meshName)
      
    # if no mesh exists duplicate one from the original skin mesh
    if not cmds.objExists( meshName ): 
        cmds.duplicate( meshOrig, n=meshName )
    
    if not cmds.objExists( meshLayer ):
        cmds.createDisplayLayer( name=meshLayer, number=1, empty=True )
    cmds.editDisplayLayerMembers( meshLayer, meshName, noRecurse=True )
    cmds.textFieldGrp( "meshName_grp", edit=True, text=meshName )
    ui.set_meshName( meshName )    
   
    #if not ui.useSelectedJoints:
    cmds.select( cl=True )
    cmds.select( meshName, r=True )
    cmds.delete( constructionHistory=True )
    cmds.select( cl=True )
    
def checkSelectedJointPositions( selection ):
    p = cmds.xform( selection[0], worldSpace=True, query=True, translation=True ) 
    origin = om.MVector(0,0,0)
    pos = om.MVector(p[0],p[1],p[2])
    if  pos != origin:
        d = origin - pos
        cmds.move(d.x,d.y,d.z,selection[0],r=True)
        errorMessage('joint1 moved to origin!')
        
    for n in range(1,len(selection)):
        pos = cmds.xform( selection[n], worldSpace=True, query=True, translation=True ) 
        #print ('%s  %f  %f  %f' % (selection[n],pos[0],pos[1],pos[2]))  
        if pos[2] != 0.0 and pos[0] >= 0.0:
            return False
    return True  
      
def checkIfSkinAttachedToJoints(selection,ui,cn):
    clusterCount = 0
    clusterName = None
    skinAttached = cmds.listConnections(selection[0],t='skinCluster')
    if skinAttached:
        clusterName = skinAttached[0]
        clusterCount += 1
        for n in selection:
            clusters = cmds.listConnections(n,t='skinCluster')
            if clusters:
                for i in clusters:
                    if i != clusterName:
                        clusterCount += 1
    if clusterCount >= 1:
        meshName = '%s_mesh' % ui.objectName
        clusterMesh = cmds.listConnections(clusterName,t='mesh')
        cmds.rename(clusterMesh,meshName)
        ui.set_meshName( meshName )
        cmds.rename(clusterName,cn.skinClusterName)
        if clusterCount > 1:
            errorMessage('Joints have more then 1 mesh Attached!') 
        return True
    return False

def checkSelectedJointsAreOk(selection):
    if not checkEveryTypeIs(selection,'joint'):
        errorMessage( "Select joints for the Fish's spine" )
        return False
    if not checkSelectedJointPositions(selection):
        errorMessage( "Root joint must be at origin!\nAnd spine joints along -x axis" )
        return False
    return True        
                             
#-----------------------------------------------------------------------------             
# CREATE RIG (SKELETON & CONTROLS)
#-----------------------------------------------------------------------------             
def createRig(args):
    ui = FishToolUI()
    cn = ControlNames(ui)
    ds = DefaultFishSettings()
    selection = cmds.ls(sl=True)
    if cmds.objExists( ui.objectName ):
        result = yesNoDialogBox( "%s rig already exists!\nWould you like to create a new Rig?" % ui.objectName )
        if result=='Yes':
            cmds.delete( ui.objectName )
        else: 
            return 
    if not cmds.objExists( ui.meshName ):
        mesh = selectMesh()
        if mesh:     
            updateMesh( ui,mesh ) 
        else:
            return    
    updateMesh( ui, ui.meshName )   
     
    # useSelectedJoints creates controls for user selected joints 
    #if ui.useSelectedJoints:
    #    if not checkSelectedJointsAreOk(selection):
    #        return
    #    if not checkIfSkinAttachedToJoints(selection,ui,cn):
    #        if not checkIfAMeshHasBeenSelected(selection,ui):
    #            errorMessage("Select a mesh for the Fish's body")
    #            return 
    #    ui.set_numberOfJoints( len(selection) )
    #    ui.set_numberOfControls( len(selection) )  
    #else:
    #if not checkIfAMeshHasBeenSelected(selection,ui):
    #    errorMessage("Select a mesh for the Fish's body")
    #    return              

    if not createSkeleton( ui,cn,ds ):
        return
    createControls( ui,cn )
    updateButtons()
    progressControlUpdate("... finished creating Rig ... ")

#-----------------------------------------------------------------------------     
# CREATE SKELETON         
#-----------------------------------------------------------------------------       
def createSkeleton( ui,cn,ds ):
    progressControlUpdate("... creating Skeleton ... ")
    
    objectName = ui.objectName
    meshName = ui.meshName
    numberOfJoints = ui.numberOfJoints
    numberOfControls = ui.numberOfControls
    #rigLength = ui.rigLength
    splineHandleName =  objectName + "_splineHandle"
    jointLayer = "Fish_joints_L";
    ctrlCurve = cn.ctrlCurve
    ctrlPositionsCurve = cn.ctrlPositions
    numberOfCVs = numberOfControls - 1;
    
    if not ui.useSelectedJoints:
        # get mesh length for joint length calculation
        length = getLengthOfMesh( meshName )
        if not length:
            return length

        if ui.rigLengthEnabled():
            length = ui.rigLength

        # create the body joints
        cmds.select( clear=True)
        if cmds.objExists( "%s|joint1" % objectName ):
            print ("Error: joint1 already exists")
            return False
        sum = 0
        sizes = []
        jointPositions = []
        for n in range(numberOfJoints):
            size = 1.0 - (n/float(numberOfJoints-1))**2  # decreasing length
            sum += size
            sizes.append(size)
        x = 0
        for n,size in enumerate(sizes,1):
            jointName = "|joint%i" % (n)
            jntPos = [x,0,0]
            cmds.joint( p=jntPos,name=jointName )
            jointPositions.append(jntPos)
            x -= (size/sum)*length
        
        # set joint transforms to work with splineIK
        cmds.select( clear=True )
        jointName = ""
        for n in range(1,numberOfJoints):
            jointName += "|joint%i" % (n)
            cmds.select( jointName )
            cmds.joint( edit=True,zso=True, oj="xyz", sao="yup" )
        
        # attach splineIK to skeleton
        joint1 = "|joint1"
        endJoint = "" 
        for n in range(1,numberOfJoints+1):
            endJoint += "|joint%i"%(n)
        
        splineCurveName = createCurve( jointPositions ) 
        cmds.ikHandle( sol="ikSplineSolver", curve=splineCurveName, ccv=False, pcv=True, sj=joint1, ee=endJoint, name=splineHandleName )
    else:
        # attach splineIK to skeleton
        joint1 = "|joint1"
        endJoint = "" 
        for n in range(1,numberOfJoints+1):
            endJoint += "|joint%i"%(n)
        result = cmds.ikHandle( sol="ikSplineSolver", ns=numberOfCVs, pcv=True, sj=joint1, ee=endJoint, name=splineHandleName )
        splineCurveName = getCurveName( result )
    cmds.setAttr("%s.visibility" % splineHandleName, 0 )
    cmds.setAttr("%s.visibility" % splineCurveName, 0 )
    cmds.rename( splineCurveName, ctrlCurve )

    # add skeleton to the joints layer
    if cmds.objExists( jointLayer ) == False:
        cmds.createDisplayLayer( name=jointLayer, number=1, empty=True)
    cmds.editDisplayLayerMembers( jointLayer, joint1 )
    
    # create a control curve to be used in Animate() function
    cmds.duplicate( ctrlCurve, rr=True, name=ctrlPositionsCurve ) 
    cmds.setAttr( "%s.visibility" % ctrlPositionsCurve, 0 )

    # add ikHandle and other control curves to joints layer
    cmds.editDisplayLayerMembers( jointLayer, ctrlCurve )
    cmds.editDisplayLayerMembers( jointLayer, splineHandleName )
    cmds.editDisplayLayerMembers( jointLayer, ctrlPositionsCurve )

    # create a group for this object
    cmds.group( em=True, name=objectName )
    cmds.group( em=True, name='%s_skeleton' % objectName)
    cmds.group( em=True, name='%s_doNotTouch' % objectName )
    cmds.parent( "|joint1", '%s_skeleton' % objectName )
    cmds.parent( ctrlCurve, '%s_doNotTouch' % objectName ) 
    cmds.parent( splineHandleName, '%s_doNotTouch' % objectName ) 
    cmds.parent( ctrlPositionsCurve, '%s_doNotTouch' % objectName ) 
    cmds.parent( meshName, objectName )     
    cmds.parent( '%s_skeleton' % objectName, objectName )
    cmds.parent( '%s_doNotTouch' % objectName, objectName )
    cmds.setAttr( '%s_doNotTouch.visibility' % objectName, 0 )

    # add attributes for keyframing
    cmds.addAttr( objectName, ln="waveLengths",at='double', dv=ds.waveLengths )
    cmds.addAttr( objectName, ln="waveAmplitude",at='double', dv=ds.waveAmplitude )
    cmds.addAttr( objectName, ln="waveRate",at='double', dv=ds.waveRate )
    cmds.addAttr( objectName, ln="tailAmplitude",at='double', dv=ds.tailAmplitude )
    cmds.addAttr( objectName, ln="tailFlex",at='double', dv=ds.tailFlex )
    cmds.addAttr( objectName, ln="effort",at='double', dv=ds.effort )
    cmds.addAttr( objectName, ln="pathUValue",niceName="path U Value",at='double', dv=ds.pathUValue )
    cmds.setAttr( "%s.waveLengths" % objectName, edit=True, keyable=True ) 
    cmds.setAttr( "%s.waveAmplitude" % objectName, edit=True, keyable=True ) 
    cmds.setAttr( "%s.waveRate" % objectName, edit=True, keyable=True ) 
    #cmds.setAttr( "%s.tailAmplitude" % objectName, edit=True, keyable=True ) 
    #cmds.setAttr( "%s.tailFlex" % objectName, edit=True, keyable=True ) 
    #cmds.setAttr( "%s.effort" % objectName, edit=True, keyable=True ) 
    cmds.setAttr( "%s.pathUValue" % objectName, edit=True, keyable=True ) 
    cmds.connectControl( 'waveLengths_grp', '%s.waveLengths' % objectName, index=2 )
    cmds.connectControl( 'waveAmplitude_grp', '%s.waveAmplitude' % objectName, index=2 )
    cmds.connectControl( 'waveRate_grp', '%s.waveRate' % objectName, index=2 )
    #cmds.connectControl( 'tailAmplitude_grp', '%s.waveRate' % objectName, index=2 )
    #cmds.connectControl( 'tailFlex_grp', '%s.waveRate' % objectName, index=2 )
    #cmds.connectControl( 'effort_grp', '%s.waveRate' % objectName, index=2 )
    cmds.connectControl( 'pathUValue_grp', '%s.pathUValue' % objectName, index=2 )
    
    length = getLength( objectName )
    ui.set_length( length )
    return True
#-----------------------------------------------------------------------------     
# control helper functions   
#-----------------------------------------------------------------------------  
def getControlPositions(ctrl, ui):
    ctrlPos = []
    # returns the cv postions of the _ctrlPositions curve
    numberOfControls = ui.numberOfControls
    cv = ctrl+".cv[0]"
    pos = cmds.xform( cv, worldSpace=True, query=True, translation=True )
    ctrlPosition0 = om.MVector(pos[0],pos[1],pos[2])
    ctrlPos.append( 0.0 )
    # calculate ctrl world position relative to first control
    for n in range(1,numberOfControls):
        cv = ctrl+".cv[%i]" % n
        pos = cmds.xform( cv, worldSpace=True, query=True, translation=True );
        ctrlVector = om.MVector( pos[0],pos[1],pos[2]) - ctrlPosition0
        ctrlPos.append( ctrlVector.length() )
    return ctrlPos    

def createCurve( cvPos ):
    degree = 3
    noOfKnots = len(cvPos) + degree - 1
    k = [0,0]
    for n in range(noOfKnots-4):
        k.append(n)
    k.append(n)
    k.append(n)  
    curveName = cmds.curve(d=degree, p=cvPos, k=k)
    return curveName
      
def createControlBox(width,height,depth, ctrlName):
    x = width/2.0
    y = height/2.0
    z = depth/2.0
    curveName = cmds.curve( d=(1), p=[(x,y,z),(x,y,-z),(x,-y,-z),(x,-y,z),(x,y,z),(-x,y,z),(-x,-y,z),(x,-y,z),(x,-y,-z),(-x,-y,-z),(-x,y,-z),(x,y,-z),(x,y,z),(-x,y,z),(-x,y,-z),(-x,-y,-z),(-x,-y,z)],k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16] ) 
    cmds.rename( curveName, ctrlName )

def createRotateControl( size,offset,ctrlName ):
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
    cmds.rename( curveName, ctrlName )
                        
def createTranslateControl( size, width, yOffset,ctrlName ):
    w = size/2.0     # height of arrow head
    z = size/5.0     # half width of base
    curveName = cmds.curve(d=(1), p=[(0,0,0),(0,w,w),(0,w,z),(0,size,z),(0,size,-z),(0,w,-z),(0,w,-w),(0,0,0)],k=[0,1,2,3,4,5,6,7] )
    cmds.rename( curveName, ctrlName ) 
    cmds.move( -yOffset, "%s.scalePivot" % ctrlName, "%s.rotatePivot" % ctrlName, y=True, ws=True )
    cmds.move( yOffset, '|%s' % ctrlName, y=True, ws=True )
    cmds.setAttr( '|%s.scaleZ' % ctrlName, width)
    cmds.makeIdentity( '|%s' % ctrlName, apply=True, t=1, r=1, s=1, n=2 )
    return ctrlName     
        
def getCurveName( list ):
    for n in range(0,len(list)):
        if 'curve' in list[n]:
            return list[n]
    return False
#-----------------------------------------------------------------------------     
# CREATE CONTROLS    
#-----------------------------------------------------------------------------   
def createControls(ui,cn):
    progressControlUpdate("... creating Controls ... ")
    objectName = ui.objectName
    numberOfJoints = ui.numberOfJoints
    numberOfControls = ui.numberOfControls
    #numberOfHandles = ui.numberOfHandles
    #spineHandleNames = cn.getSpineHandleNames()
    lastControlNumber = numberOfControls - 1
    #rigLength = ui.rigLength
    splineHandleName = objectName + "_splineHandle"
    ctrlCurve = cn.ctrlCurve
    ctrlLayer = "Fish_controls_L"
    ctrlBack = "ctrl_backTwist"
    ctrlGroup = objectName + "_controls"
    ctrlBoxSize = ui.length/1000.0
   
    # if no control_L exists, create one
    if not cmds.objExists( ctrlLayer ):
        cmds.createDisplayLayer( name=ctrlLayer, number=1, empty=True )
        cmds.setAttr( '%s.color' % ctrlLayer,17)

    # get the control positions
    #ctrlPos = []
    #getControlPositions(ctrlCurve, ctrlPos,ui)
    ctrlPos = getControlPositions(cn.ctrlPositions, ui)

    # create controls
    for n in range(0,numberOfControls):
        cmds.select( clear=True )
        jointName = "|ctrlJN_%i" % (n)
        if cmds.objExists( jointName ):
            print ("Error: "+jointName+" already exists")
            for i in range(1,n):
                cmds.delete( "|ctrlJN_%i" %(i) )
            return 
        cmds.joint( p=(-ctrlPos[n],0,0), name=jointName )
        cmds.setAttr( "%s.visibility" % jointName,0 )
        
        ctrlName = "|ctrl_%i" % (n)
        #ctrlPosName = "|ctrl_pos_%i" % (n)
        if n == 0:
            createControlBox( ctrlBoxSize,ctrlBoxSize,ctrlBoxSize, "ctrl_0" )
            #createControlBox( ctrlBoxSize,ctrlBoxSize,ctrlBoxSize, "ctrl_pos_0" )
        else:  
            ctrlOrig = "|ctrl_0"  
            newName = cmds.duplicate( ctrlOrig, rr=True, name=ctrlName ) 
            cmds.rename( newName[0], "ctrl_%i" % n )
            #newName = cmds.duplicate( ctrlOrig, rr=True, name=ctrlPosName )
            #cmds.rename( newName[0], "ctrl_pos_%i" % n )
        
        cmds.setAttr( '%s.translateX' % ctrlName, -ctrlPos[n]) 
        #cmds.setAttr( '%s.translateX' % ctrlPosName, -ctrlPos[n])
        cmds.editDisplayLayerMembers( ctrlLayer, ctrlName )
        #cmds.editDisplayLayerMembers( ctrlLayer, ctrlPosName )

    # create Twist control handles
    #twistCtrlSize = 8.0
    #twistCtrlOffset = 0.0

    #createRotateControl( twistCtrlSize,twistCtrlOffset, cn.frontTwistCtrl )
    #createRotateControl( twistCtrlSize,twistCtrlOffset, cn.backTwistCtrl )
    #cmds.move( (-twistCtrlSize/2.0), '|%s' % cn.frontTwistCtrl, x=True, ws=True )
    #cmds.move( -ctrlPos[numberOfControls-1], '|%s' % cn.backTwistCtrl, x=True, ws=True )    

    # bind the controls to the ctrl curve 
    cmds.select( clear=True )
    cmds.select( "|ctrlJN_0", r=True )
    for n in range(1,numberOfControls):
        ctrl = "|ctrlJN_%i" % (n)
        cmds.select( ctrl, add=True )
    cmds.select( ctrlCurve, add=True )
    cmds.skinCluster( toSelectedBones=True,  bm=0, nw=1, wd=0, mi=3, dr=4.0, rui=True, fnw=True)
    
    # organize controls
    cmds.parent( '|ctrlJN_0','|ctrl_0' )
    #cmds.parent( '|ctrlJN_0','|ctrl_pos_0' )
    #cmds.parent( '|ctrl_pos_0','|ctrl_0')
    #cmds.parent( '|%s' % cn.backTwistCtrl, '|ctrl_%i' % lastControlNumber )
    #cmds.parent( '|%s' % cn.frontTwistCtrl, '|ctrl_0' )
    
    for n in range(1,numberOfControls): 
        jointName = "|ctrlJN_%i" % (n)
        ctrlName =  "|ctrl_%i" % (n)
        #ctrlPosName = "|ctrl_pos_%i" % (n)
        #cmds.parent( jointName, ctrlPosName )
        #cmds.parent( ctrlPosName, ctrlName )
        cmds.parent( jointName, ctrlName )

    # group controls
    cmds.group( "|ctrl_0", name=ctrlGroup )
    for n in range(1,numberOfControls):
        ctrl = "|ctrl_%i" % (n)
        cmds.parent( ctrl, ctrlGroup )
    cmds.parent( ctrlGroup, objectName )    
 
    # set Twist controls
    #firstControl = "%s|%s|ctrl_0|head_TRN_CTRL|ctrlJN_0.xformMatrix" % (objectName,ctrlGroup)
    firstControl = "%s|%s|ctrl_0|ctrlJN_0.xformMatrix" % (objectName,ctrlGroup)
    lastControl = "%s|%s|ctrl_%i|ctrlJN_%i.xformMatrix" % (objectName,ctrlGroup,lastControlNumber,lastControlNumber)
    dTwistControlEnable = "%s|%s_doNotTouch|%s_splineHandle.dTwistControlEnable" % (objectName,objectName,objectName)
    dWorldUpType = "%s|%s_doNotTouch|%s_splineHandle.dWorldUpType" % (objectName,objectName,objectName)
    dWorldUpMatrix = "%s|%s_doNotTouch|%s_splineHandle.dWorldUpMatrix" % (objectName,objectName,objectName)
    dWorldUpMatrixEnd = "%s|%s_doNotTouch|%s_splineHandle.dWorldUpMatrixEnd" % (objectName,objectName,objectName)
    cmds.setAttr( dTwistControlEnable,1)
    cmds.setAttr( dWorldUpType,4)
    cmds.connectAttr( firstControl, dWorldUpMatrix, f=True)
    cmds.connectAttr( lastControl, dWorldUpMatrixEnd, f=True)
    
    # link the Twist control handle to the twist control joints
    #expName = objectName + "_exp_twistControls"
    #expName = cn.expName_twistControls 
    #if cmds.objExists(expName):
    #    cmds.delete(expName)
    #rxFrontTwistCtrl = "%s|%s_controls|ctrl_0|%s|%s.rotateX" % (objectName,objectName,headTrnCtrlName,cn.frontTwistCtrl)
    #rxFirstJoint = "%s|%s_controls|ctrl_0|%s|ctrlJN_0.rotateX" % (objectName,objectName,headTrnCtrlName)
    #rxFrontTwistCtrl = "%s|%s_controls|ctrl_0|%s.rotateX" % (objectName,objectName,cn.frontTwistCtrl)
    #rxFirstJoint = "%s|%s_controls|ctrl_0|ctrl_pos_0|ctrlJN_0.rotateX" % (objectName,objectName)
    #rxBackTwistCtrl = "%s|%s_controls|ctrl_%i|%s.rotateX" % (objectName,objectName,lastControlNumber,cn.backTwistCtrl)
    #rxLastJoint = "%s|%s_controls|ctrl_%i|ctrl_pos_%i|ctrlJN_%i.rotateX" % (objectName,objectName,lastControlNumber,lastControlNumber,lastControlNumber)
    #exp = "%s = %s;\n%s = %s;\n" % (rxFirstJoint,rxFrontTwistCtrl,rxLastJoint,rxBackTwistCtrl) 
    #cmds.expression( s=exp, name=expName )
#-----------------------------------------------------------------------------------------
#  Skinning Helper Functions
# ----------------------------------------------------------------------------------------
def getSkinClusterName(meshName):
    objHist = cmds.listHistory( meshName, pdo=True )
    skinClusters = cmds.ls(objHist, type="skinCluster")
    if len(skinClusters):
        return skinClusters[0]
    else:
        return 0      
#-----------------------------------------------------------------------------------------
#  SKINNING 
# ----------------------------------------------------------------------------------------
def attachRig( args ):
    ui = FishToolUI()
    cn = ControlNames(ui)
    
    if cmds.objExists( ui.objectName ):
        try:    # check if skin is already attached to a rig
            joints = cmds.skinCluster( ui.meshName, query=True, wi=True )
            clusterName = getSkinClusterName(ui.meshName)
            cmds.rename(clusterName,cn.skinClusterName)
            errorMessage( "Rig is already attached!" )
        except:
            attachSkin(ui,cn)
            weightSkin(ui,cn)
    else:
        errorMessage("Create a Rig First!")
        updateButtons()
        return
    updateButtons()
    progressControlUpdate("... finished attaching rig ... ")       
#-------------------------------------------------------------
def unbindSkin( args ):
    ui = FishToolUI()
    cn = ControlNames(ui)
    if cmds.objExists( cn.skinClusterName ):
        cmds.skinCluster( cn.skinClusterName, e=True, ub=True ) 
    progressControlUpdate("... finished detaching mesh ...")
    resetProgressControl()      

def selectExistingSkeleton(joint1):
    selList = []
    result = cmds.listRelatives(joint1,ad=True,f=True)
    for n in result:
        hasChildren = cmds.listRelatives(n,c=True)
        if hasChildren and checkTypeIs(n,'joint'):
            selList.append(n)
    cmds.select(selList)   
#-------------------------------------------------------------
# attachSkin()
#-------------------------------------------------------------
def attachSkin(ui,cn):
    progressControlUpdate("... attaching mesh ... ")
    
    objectName = ui.objectName
    numberOfJoints = ui.numberOfJoints
    #headJointName = cn.getHeadJointName()
    jointNames = cn.getJointNames()
    
    cmds.select(cl=True)
    if ui.useSelectedJoints:
        selectExistingSkeleton(jointNames[0])
    else:    
        cmds.select( jointNames[0:numberOfJoints],r=True )
    cmds.select( ui.meshName, add=True )
    cmds.skinCluster( name=cn.skinClusterName, bindMethod=0, normalizeWeights=1, weightDistribution=0, mi=3, omi=True, dr=4, rui=True, fnw=True )
    cmds.select(cl=True) 
#-------------------------------------------------------------
# weightSkin()
#-------------------------------------------------------------
def weightSkin(ui,cn):
    progressControlUpdate("... adjusting skin weights ... ")

    objectName = ui.objectName
    meshName = ui.meshName
    numberOfJoints = ui.numberOfJoints
    jointNames = cn.getJointNames()
    numberOfVertices = cmds.polyEvaluate( meshName, v=True )
    meshShape = cmds.listRelatives( meshName )
    skinClusterName = cn.skinClusterName
    normWeights = "%s.normalizeWeights" % skinClusterName
    maxInfluences = "%s.maxInfluences" % skinClusterName
    cmds.setAttr( normWeights, 0 )
    cmds.setAttr( maxInfluences, 3 )   

    resetProgressControl(); 
    setProgressControlMaxValue(100);
    
    # store joint positions
    jointPosition = []
    jointVector = []
    jointLength = []

    # store joint positions, vectors, and lengths
    for n in range( 0,numberOfJoints ):
        pos = cmds.xform( jointNames[n], worldSpace=True, query=True, translation=True ) 
        jointPosition.append( om.MVector( pos[0],pos[1],pos[2] ) ) 
   
        if n > 0:
            v = jointPosition[n] - jointPosition[n-1] 
            jointVector.append( om.MVector( v.x, v.y, v.z) )
            jointLength.append( v.length() )

    progressCurrentStep = 0
    progressIncrement = numberOfVertices/100
    showProgress = progressIncrement
   
    for n in range(0,numberOfVertices):
        # progress bar
        if showProgress:
            step = n/progressIncrement
            if step > progressCurrentStep+1:
                progressCurrentStep += 1
                progressControl()
       
        cv = "%s.vtx[%i]" % (meshName,n)
       
        # work out which joint the cv is closest too
        cvPos = cmds.xform( cv, worldSpace=True, query=True, translation=True )
        cvPosVec = om.MVector( cvPos[0],cvPos[1],cvPos[2] )
        j = 0                  # $j stores the vertices closest joint
        jPrev = -1 
        jNext = -1
        jLast = numberOfJoints - 2
        jDot = 0.0

        for i in range(0,numberOfJoints-1):
            # calc dot product of (joint vector . joint->cv vector)
            v1 = cvPosVec - jointPosition[i]
            v2 = jointVector[i]
            v2 = v2.normal()
            d  = (v1*v2)/jointLength[i] 
             
            # if vertex is in front of first joint
            if i == 0 and d < 0.0:  
                j = 0
                jNext = 1
                jDot = 0.0
           
            # if vertex is past last joint
            if i == jLast and d > 1.0:
                j = jLast
                jPrev = j-1
                jDot = 1.0

            # if vertex is inside this joints area
            if d >= 0.0 and d <= 1.0: 
                j = i
                if  j > 0:
                    jPrev = j-1
                jNext = j+1 
                jDot = d  

                if j == jLast:
                    jNext = -1  
     
        #calculate and apply skin weights
        wPos  = jDot 
        wNext = 0.0
        wPrev = 0.0
         
        # zero all weights except for nearest joint
        cmds.skinPercent( skinClusterName, cv, zri=True, tv=[(jointNames[j], 1.0)] )
        
        if j < jLast: # add weighting from next joint along
            wNext = 0.5*(wPos*wPos);
            cmds.skinPercent( skinClusterName, cv, nrm=False, tv=[(jointNames[jNext], wNext)] ) 

        if j > 0:  # add weighting from previous joint
            wPrev = 0.5*(1-wPos)*(1-wPos) 
            cmds.skinPercent( skinClusterName, cv, nrm=False, tv=[(jointNames[jPrev], wPrev)] ) 
            
        w = 1 - wNext - wPrev
        cmds.skinPercent( skinClusterName, cv, nrm=False, tv=[(jointNames[j], w)] )

    progressControl()   
#-------------------------------------------------------------
# DetachControlsFromPath()    
#----------------------------------------------------------------------------- 
def detachFromPath( args ):
    ui = FishToolUI()
    cn = ControlNames(ui)
    objectName = ui.objectName
    numberOfControls = ui.numberOfControls 
    ctrlNames = cn.getPathControlNames()
    mPaths = cn.getMotionPathNames()
    
    # delete expressions controlling motion path uValues and twist controls       
    if cmds.objExists( cn.expName_uValues  ):
        cmds.delete( cn.expName_uValues  )
    if cmds.objExists( cn.expName_twistControls ):
        cmds.delete( cn.expName_twistControls )

    # delete motion path constraints
    cmds.cycleCheck(e=False)
    for mp in mPaths:
        if cmds.objExists(mp):
            # delete connected nodes
            result = cmds.listConnections(mp,s=False)
            if result:
                for n in result:
                    node_type = cmds.objectType( n )
                    if node_type == 'addDoubleLinear':
                        cmds.delete(n)
            cmds.delete(mp)
    cmds.cycleCheck(e=True)
    
    # reset control positions
    #ctrlPositionsCurve = cn.ctrlPositions
    #ctrlPos = []
    #getControlPositions(ctrlPositionsCurve, ctrlPos,ui)
    ctrlPos = getControlPositions(cn.ctrlPositions, ui)
    for n in range(0,numberOfControls): 
        cmds.setAttr( "%s.translateX" % ctrlNames[n], -ctrlPos[n]) 
        cmds.setAttr( "%s.translateY" % ctrlNames[n], 0.0) 
        cmds.setAttr( "%s.translateZ" % ctrlNames[n], 0.0) 
        cmds.setAttr( "%s.rotateX" % ctrlNames[n], 0.0) 
        cmds.setAttr( "%s.rotateY" % ctrlNames[n], 0.0) 
        cmds.setAttr( "%s.rotateZ" % ctrlNames[n], 0.0)  

    updateUI(cn.objectName)

#-----------------------------------------------------------------------------
# ATTACH Fish TO PATH 
#----------------------------------------------------------------------------- 
def AttachFishToPath( args ):
    ui = FishToolUI()
    if not cmds.objExists( ui.objectName ):
        errorMessage("Create a Rig First!")
        updateButtons()
        return
    selection = cmds.ls(sl=True)    
    if not cmds.objExists( ui.pathName ):
        if len( selection ) == 0:
            errorMessage( "Select a path for the Fish to follow" )
            return 
        ui.set_pathName( selection[0] ) 
    if not checkTypeIs(ui.pathName,'nurbsCurve'):
        errorMessage( "Select a nurbs curve path for the Fish path" )
        return 
    attachControlsToPath()
    
def attachControlsToPath():
    """
    - attach each control to motion path
    - create expression so that for each control:
        (ctrl's) motionPath.uValue =  ctrl_0.uValue + ctrlPosition
    """
    ui = FishToolUI()
    cn = ControlNames(ui)
    objectName = ui.objectName
    numberOfJoints = ui.numberOfJoints
    numberOfControls = ui.numberOfControls
    #rigLength = ui.rigLength
    path = ui.pathName
    start = ui.start
    end = ui.end
    speed = ui.speed
    pathLength = cmds.arclen( path )
    ctrl = cn.getPathControlNames()
    mPathNames = cn.getMotionPathNames()
    
    pathName = cn.pathName
    ui.set_pathName( pathName )
    
    if cmds.objExists( path ):
        cmds.rename( path, pathName)
    else:
        errorMessage( "path doesn't exist" )
        return        
    
    #ctrlPos = []
    #ctrlPositionsCurve = cn.ctrlPositions
    #getControlPositions(ctrlPositionsCurve,ctrlPos,ui)
    ctrlPos = getControlPositions(cn.ctrlPositions, ui)
 
    # attach each control to the path
    for n in range(0,numberOfControls):
        cmds.select( clear=True )
        motionPathName = cmds.pathAnimation( ctrl[n], curve=pathName, fractionMode=True, follow=True, followAxis='x', upAxis='y', worldUpType="vector", worldUpVector=[0,1,0], inverseUp=False, inverseFront=False, bank=False, startTimeU=start, endTimeU=end);
        cmds.rename( motionPathName, mPathNames[n] )
    
    # remove motionPath keyframes so expressions govern the ctrl's movement
    for n in range(1,numberOfControls):
        motionPath = '%s.uValue' % mPathNames[n]
        cmds.cutKey( motionPath, option="keys" )

    # create linear tangents for the main path control
    cmds.keyTangent( mPathNames[0], time=(start,start), itt='linear', ott='linear' )
    cmds.keyTangent( mPathNames[0], time=(end,end), itt='linear', ott='linear' )   
      
    # create the expressions for each control
    #expName = objectName + "_exp_uValues" 
    expName = cn.expName_uValues
    if cmds.objExists(expName):
        cmds.delete(expName)
    exp = "float $pathLength = %f;\n" % (pathLength)  
    exp += "float $ctrlPosition[] = {%f" % ctrlPos[0]
    for n in range(1,numberOfControls):
        exp += ",%f" % (ctrlPos[n])
    exp += "};\n"
    for n in range(1,numberOfControls):
        exp += "float $distAlongCurve%i = (%s.uValue * $pathLength) - $ctrlPosition[%i]; \n" % (n,mPathNames[0],n) 
    for n in range(1,numberOfControls):   
        exp += "%s.uValue = $distAlongCurve%i/$pathLength;\n" % (mPathNames[n],n) 
    cmds.expression( s=exp, name=expName )
    
    # calculate Fishs starting position so Fish is entirely on the path
    FishSkeletonLength = ui.length
    uValueStart = FishSkeletonLength/pathLength
    
    # add an attribute to the Fish ctrl object to control movement along the path
    attrName = cn.pathUValue
    path_uValue = '%s.uValue' % mPathNames[0]
    cmds.cutKey(path_uValue, clear = True)
    cmds.setDrivenKeyframe( path_uValue, cd=attrName, itt='linear', ott='linear', dv=0.0, v=0.0 )
    cmds.setDrivenKeyframe( path_uValue, cd=attrName, itt='linear', ott='linear', dv=1.0, v=1.0 )
    cmds.setKeyframe( attrName, time=(start,start),value=uValueStart )
    cmds.setKeyframe( attrName, time=(end,end),value=1.0 )
    cmds.keyTangent( attrName, time=(start,start), itt='linear', ott='linear' )
    cmds.keyTangent( attrName, time=(end,end), itt='linear', ott='linear' )
    
    updateButtons()
    progressControlUpdate("... finished attaching Fish to path ...")


#-------------------------------------------------------------------------------------------
# ANIMATION
#-----------------------------------------------------------------------------  
# deleteAnimations()
#-----------------------------------------------------------
def deleteAnimations( args ):
    deleteAnimationKeyframes()
    
def deleteAnimationKeyframes():    
    ui = FishToolUI()
    cn = ControlNames(ui)
    objectName = ui.objectName
    numberOfControls = ui.numberOfControls
    ctrlNames = cn.getCtrlJointNames()
    #ctrlPosNames = cn.getCtrlPosNames()
    #headCtrlName = cn.getHeadJointName()
    #cmds.cutKey( headCtrlName )
    for n in range(0,numberOfControls):
        if cmds.objExists( ctrlNames[n] ):
            cmds.cutKey( ctrlNames[n] )
            #cmds.cutKey( ctrlPosNames[n] )
            cmds.setAttr( '%s.translateZ' % ctrlNames[n], 0 )
            #cmds.setAttr( '%s.translateX' % ctrlPosNames[n], 0 )
            #cmds.setAttr( '%s.translateZ' % ctrlPosNames[n], 0 )
    #ui.enableSideFins(False)    
    progressControlUpdate("... finished deleting keyframes ... ")            
#-----------------------------------------------------------
def updateMotionPathKeyframes( objectName, path_uValue,start, end ):
    numberOfKeyframes = cmds.keyframe( path_uValue, query=True,kc=True )
    firstKeyframe = cmds.findKeyframe( path_uValue, which='first' )
    lastKeyframe = cmds.findKeyframe( path_uValue, which='last' )
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
#------------------------------------------------------------------
# addAnimationPrecision()
#------------------------------------------------------------------
def addAnimationPrecision():
    ui = FishToolUI()
    cn = ControlNames(ui)

    am = AnimationManager()
    
    # initialize progress bar
    resetProgressControl()
    setProgressControlMaxValue(ui.end-ui.start)
    progressControlUpdate("... adding keyframes ... ")
    
    # create keyframes for Fishs starting position
    am.setInitialPosition(int(ui.start))
    #am.initializePrecision()

    # create keyframes for selected time range
    for t in range( int(ui.start)+1, int(ui.end) ):
        progressControl()
        
        # get Fish waveLength, waveAmplitude, waveRate etc
        #am.moveAlongPath(t)

        # update all control positions and keyframe if required
        am.updatePrecision(t,'spline')
    
    progressControl()
    progressControlUpdate("... finished adding keyframes ... ")    

def addKeyframes( args ):
    addAnimationPrecision()

def checkIfRigged( ui ):
    if cmds.objExists(ui.objectName):
        return True
    return False

def checkIfAttachedToPath(cn,ui):
    if not cmds.objExists(ui.pathName):
        errorMessage( "%s does not exist!" % ui.pathName)
        return False 
    numberOfKeyframes = cmds.keyframe( cn.pathUValue, query=True,kc=True ) 
    if numberOfKeyframes < 2:
        return False
    return True
                  
#------------------------------------------------------------------
# animate_timeChanges()
#------------------------------------------------------------------
def createAnimation( args ):
    ui = FishToolUI()
    cn = ControlNames(ui)

    if not checkIfRigged(ui):
        errorMessage("Create a Rig First!")
        updateButtons()
        return
        
    deleteAnimationKeyframes()    
 
    objectName = ui.objectName
    start = int( ui.start )
    end = int( ui.end )
    path = ui.pathName
    path_uValue = cn.pathUValue
    
    if not checkIfAttachedToPath(cn,ui):
        errorMessage( "Attach to Motion Path before animating!" )
        return      
    
    # update path uValues for current start and end time in Animation Settings 
    updateMotionPathKeyframes( objectName,path_uValue,start,end)
    
    am = AnimationManager()
    #am.display()
    
    # initialize progress bar
    resetProgressControl()
    setProgressControlMaxValue(end-start)
    progressControlUpdate("... creating keyframes ... ")
    
    # create keyframes for Fishs starting position
    am.setInitialPosition(int(start))

    # create keyframes for selected time range
    for t in range( int(start)+1,int(end) ):
        progressControl()

        # update all control positions and keyframe if required
        am.update(t)
        
        # create keyframes for all controls if Fish stops or starts moving
        if am.FishHasStoppedMoving() or am.FishHasStartedMoving():
            am.keyAllControlsAtTime(t,'flat')
                 
    
    # key all controls on the last time frame
    am.keyAllControlsAtTime(int(end),'linear' )
  
    progressControl()
    progressControlUpdate("... finished creating keyframes ... ")
    
    if ui.preActive:
        addAnimationPrecision()