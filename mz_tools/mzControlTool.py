"""
mzControlTool_b03.py

Version: b03  updated: June 2, 2021
Author:  Steven Thomasson (www.mayazoo.net)
Description: Control Tool for mz Animal Tools

Copyright (C) 2021 Steven Thomasson. All rights reserved.

"""
import maya.api.OpenMaya as om
import maya.cmds as cmds


# -----------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------
def getDAGPath(mesh):
    try:
        selectionList = om.MSelectionList()
        selectionList.add(mesh)
        nodeDagPath = selectionList.getDagPath(0)
    except:
        raise RuntimeError("could not find dag path for %s" % mesh)
    return nodeDagPath


def errorMessage(msg):
    cmds.confirmDialog(
        title=" ",
        message=msg,
        button="OK",
        defaultButton="OK",
        cancelButton="OK",
        dismissString="OK",
    )


# -----------------------------------------------------------------------------
# UI CLASS
# -----------------------------------------------------------------------------
class DefaultControlSettings:
    def __init__(self):
        self.sliderRange = 100.0


class mzControlUI:
    def __init__(self, mct):
        self.ds = DefaultControlSettings()
        self.mct = mct  # mzControlTool class object
        self.initSliderValue = self.ds.sliderRange * 0.5
        self.createControlUI()

    def createControlUI(self):
        if cmds.window("mzControlToolWnd", exists=True):
            cmds.deleteUI("mzControlToolWnd", window=True)
        # if cmds.windowPref( "mzControlToolWnd", exists=True ):
        #    cmds.windowPref( "mzControlToolWnd", remove=True )
        window = cmds.window(
            "mzControlToolWnd", title="mzControlTool", widthHeight=(294, 84)
        )
        cmds.scrollLayout("scrollLayout")
        cmds.columnLayout(
            adjustableColumn=True, columnOffset=("both", 4)
        )  # , backgroundColor=[1.0,0.0,0.0] )
        # ------------------------------------------------------------------
        # Name
        cmds.columnLayout(rowSpacing=5)
        cmds.textFieldGrp("mzcObjectName_grp", visible=False, text="")
        cmds.rowColumnLayout(
            numberOfColumns=6,
            columnSpacing=[(1, 0), (2, 13), (3, 13), (4, 5), (5, 5), (6, 5)],
        )
        cmds.button("select_btn", label="Select", h=28, w=50, command=self.selectObject)
        cmds.button(
            "createKey_btn",
            label="Key",
            en=True,
            h=28,
            w=45,
            command=self.mct.createKey,
        )
        cmds.button("slower_btn", label="<", h=28, w=25, command=self.mct.slow)
        cmds.button("slow_btn", label="< Slow", h=28, w=45, command=self.mct.slower)
        cmds.button("fast_btn", label="Fast >", h=28, w=45, command=self.mct.faster)
        cmds.button("faster_btn", label=">", h=28, w=25, command=self.mct.fast)
        cmds.setParent("..")
        # ------------------------------------------------------------------
        # Move Keyframes
        cmds.rowColumnLayout(
            numberOfColumns=6,
            columnSpacing=[(1, 0), (2, 5), (3, 5), (4, 15), (5, 15), (6, 5)],
        )
        cmds.button(
            "prev_btn", label="|<", height=28, width=30, command=self.mct.prevKey
        )
        cmds.button(
            "play_btn",
            label="Play",
            height=28,
            width=45,
            command=self.mct.playAnimation,
        )
        cmds.button(
            "next_btn", label=">|", height=28, width=30, command=self.mct.nextKey
        )
        cmds.button(
            "mzCtrlAnimate_btn",
            label="Animate",
            height=28,
            width=60,
            command=self.mct.createAnimation,
        )
        cmds.button(
            "displayKeys_btn", label="Display", h=28, w=45, command=self.mct.displayKeys
        )
        cmds.button("size_btn", label="S", h=28, w=20, command=self.setDisplaySize)
        cmds.setParent("..")
        # ------------------------------------------------------------------
        # Animation Controls
        cmds.intSlider(
            "slider_grp",
            min=0,
            max=self.ds.sliderRange,
            width=250,
            visible=False,
            value=self.initSliderValue,
            step=1,
            cc=self.changeDisplaySize,
        )
        cmds.setParent("..")
        cmds.showWindow("mzControlToolWnd")

    def selectObject(self, args):
        self.mct.selectObject()

    def setInitialDisplaySize(self):
        cmds.window("mzControlToolWnd", edit=True, height=84)

    def setDisplaySize(self, args):
        if not self.mct.toolSelected():
            errorMessage("Nothing Selected!")
            return
        height = cmds.window("mzControlToolWnd", query=True, height=True)
        if cmds.intSlider("slider_grp", query=True, visible=True):
            cmds.intSlider("slider_grp", edit=True, visible=False)
            self.mct.showKeyframeLocators("off")
            if height > 84:
                cmds.window("mzControlToolWnd", edit=True, height=84)
        else:
            # sliderValue = ((self.mct.radius*self.locatorScale)/self.rigLength)*self.sliderRange
            sliderValue = self.mct.getCurrentSliderValue()
            cmds.intSlider("slider_grp", edit=True, value=sliderValue)
            cmds.intSlider("slider_grp", edit=True, visible=True)
            self.mct.showKeyframeLocators("on")
            if height < 100:
                cmds.window("mzControlToolWnd", edit=True, height=110)

    def changeDisplaySize(self, args):
        sliderValue = cmds.intSlider("slider_grp", query=True, v=True)
        self.mct.changeDisplaySize(sliderValue)

    def setSliderPosition(self, value):
        if cmds.intSlider("slider_grp", query=True, visible=True):
            cmds.intSlider("slider_grp", edit=True, v=value)

    def updateButtons(self, btn):
        if btn == "select":
            cmds.button("select_btn", edit=True, bgc=(0.1, 0.5, 0.3))
            cmds.button("mzCtrlAnimate_btn", edit=True, bgc=(0.365, 0.365, 0.365))
        if btn == "animate":
            cmds.button("select_btn", edit=True, bgc=(0.365, 0.365, 0.365))
            cmds.button("mzCtrlAnimate_btn", edit=True, bgc=(0.1, 0.5, 0.3))


# -----------------------------------------------------------------------------
# TOOL CLASSES
# -----------------------------------------------------------------------------
class ToolInfo:
    def __init__(self, name, windowName):
        self.name = name
        self.windowName = windowName
        self.uiObjectNameGrp = None  # handle to mzToolUI 'objectName_grp'
        self.uiPathNameGrp = None  # handle to mzToolUI 'pathName_grp'
        self.uiEndTimeGrp = None  # handle to mzToolUI 'endTime_grp'
        self.animate = None  # handle to mzTool.CreateAnimation()
        self.connected = False  # flag - if UI is open & connected
        self.maxKeyDisplayRadius = 0.0  # keyframe display circles

    def linkToUI(self, uiName, name):
        if name == "animate_btn":
            self.animate = cmds.button(uiName, query=True, c=True)
        if name == "objectName_grp":
            self.uiObjectNameGrp = uiName
        elif name == "pathName_grp":
            self.uiPathNameGrp = uiName
        elif name == "endTime_grp":
            self.uiEndTimeGrp = uiName

    def uiLinkSuccessfull(self):
        if self.uiObjectNameGrp == None:
            return False
        if self.animate == None:
            return False
        if self.uiPathNameGrp == None:
            return False
        if self.uiEndTimeGrp == None:
            return False
        return True


class FishToolInfo(ToolInfo):
    def __init__(self, name, windowName):
        ToolInfo.__init__(self, name, windowName)
        self.uiRigLength = None  # handle to mzToolUI 'rigLength_grp'
        self.attributes = [
            "pathUValue",
            "waveLengths",
            "waveAmplitude",
            "waveRate",
            "tailAmplitude",
            "tailFlex",
            "effort",
        ]

    def linkToUI(self, uiName, name):
        ToolInfo.linkToUI(self, uiName, name)
        if name == "rigLength_grp":
            self.uiRigLength = uiName

    def uiLinkSuccessfull(self):
        if not ToolInfo.uiLinkSuccessfull(self):
            self.connected = False
            return False
        if self.uiRigLength == None:
            self.connected = False
            return False
        self.connected = True
        return True


class SnakeToolInfo(ToolInfo):
    def __init__(self, name, windowName):
        ToolInfo.__init__(self, name, windowName)
        self.uiRigLength = None  # handle to mzToolUI 'rigLength_grp'
        self.attributes = ["pathUValue", "waveLengths", "waveAmplitude", "waveRate"]

    def linkToUI(self, uiName, name):
        ToolInfo.linkToUI(self, uiName, name)
        if name == "snakeLength_grp":
            self.uiRigLength = uiName

    def uiLinkSuccessfull(self):
        if not ToolInfo.uiLinkSuccessfull(self):
            self.connected = False
            return False
        if self.uiRigLength == None:
            self.connected = False
            return False
        self.connected = True
        return True


class TurtleToolInfo(ToolInfo):
    def __init__(self, name, windowName):
        ToolInfo.__init__(self, name, windowName)
        self.attributes = ["pathUValue", "swimCycle", "tilt"]


class ButterflyToolInfo(ToolInfo):
    def __init__(self, name, windowName):
        ToolInfo.__init__(self, name, windowName)
        self.attributes = [
            "pathUValue",
            "cycleRate",
            "glide",
            "roll",
            "frameRate",
            "liftCoefficient",
            "gravity",
            "wingLength",
        ]


class mzToolManager:
    def __init__(self):
        snakeInfo = SnakeToolInfo("mzSnakeTool", "mzSnakeToolWindow")
        fishInfo = FishToolInfo("mzFishTool", "mzFishToolWindow")
        turtleInfo = TurtleToolInfo("mzTurtleTool", "mzTurtleToolWindow")
        butterflyInfo = ButterflyToolInfo("mzButterflyTool", "mzButterflyToolWindow")
        self.tools = [snakeInfo, fishInfo, turtleInfo, butterflyInfo]
        self.currentTool = None
        self.displayGroup = "_key_display"

    def toolSelected(self):
        if self.currentTool:
            return True
        return False

    def getToolNameForType(self, type):
        if type == "fish":
            return "mzFishTool"
        if type == "snake":
            return "mzSnakeTool"
        if type == "turtle":
            return "mzTurtleTool"
        if type == "butterfly":
            return "mzButterflyTool"
        return None

    def setTool(self, type):
        toolName = self.getToolNameForType(type)
        for tool in self.tools:
            if tool.name == toolName:
                if cmds.window(tool.windowName, exists=True):
                    if tool.connected:
                        self.currentTool = tool
                        return True
                    else:
                        self.linkToolWindowElements(tool)
                        if tool.uiLinkSuccessfull():
                            self.currentTool = tool
                            return True
        return False

    def linkToolWindowElements(self, tool):
        # search all UI elements (full path) and match our tool elements
        uiNames = cmds.lsUI(l=True, controls=True)
        for uiName in uiNames:
            id = uiName.split("|")
            if id[0] == tool.windowName:
                name = id[len(id) - 1]
                tool.linkToUI(uiName, name)

    def findToolWindows(self):
        # find and link all open mzTool UI Windows
        for tool in self.tools:
            if cmds.window(tool.windowName, exists=True):
                self.linkToolWindowElements(tool)
                tool.uiLinkSuccessfull()  # checks the link

    def setObjectName(self, name):
        uiObjectNameGrp = self.currentTool.uiObjectNameGrp
        try:
            cmds.textFieldGrp(uiObjectNameGrp, edit=True, text=name)
        except:
            self.findToolWindows()
            uiObjectNameGrp = self.currentTool.uiObjectNameGrp
            cmds.textFieldGrp(uiObjectNameGrp, edit=True, text=name)

    def setEndTime(self, t):
        uiEndTimeGrp = self.currentTool.uiEndTimeGrp
        try:
            cmds.floatFieldGrp(uiEndTimeGrp, edit=True, v1=t)
        except:
            self.findToolWindows()
            uiEndTimeGrp = self.currentTool.uiEndTimeGrp
            cmds.floatFieldGrp(uiEndTimeGrp, edit=True, v1=t)

    def getAttributes(self):
        if self.currentTool:
            return self.currentTool.attributes

    def getObjectName(self):
        if self.currentTool:
            try:
                uiObjectNameGrp = self.currentTool.uiObjectNameGrp
                return cmds.textFieldGrp(uiObjectNameGrp, query=True, text=True)
            except:
                self.findToolWindows()
                uiObjectNameGrp = self.currentTool.uiObjectNameGrp
                return cmds.textFieldGrp(uiObjectNameGrp, query=True, text=True)

    def getPathName(self):
        if self.currentTool:
            try:
                uiPathNameGrp = self.currentTool.uiPathNameGrp
                return cmds.textFieldGrp(uiPathNameGrp, query=True, text=True)
            except:
                self.findToolWindows()
                uiPathNameGrp = self.currentTool.uiPathNameGrp
                return cmds.textFieldGrp(uiPathNameGrp, query=True, text=True)

    def getPathUValue(self):
        if self.currentTool:
            objectName = self.getObjectName()
            return "%s.%s" % (objectName, self.currentTool.attributes[0])

    def isSetMaxKeyDisplayRadius(self):
        if self.currentTool.maxKeyDisplayRadius == 0.0:
            return False
        else:
            return True

    def setMaxKeyframeDisplayRadius(self, max):
        self.currentTool.maxKeyDisplayRadius = max

    def getMaxKeyframeDisplayRadius(self):
        if self.currentTool:
            return self.currentTool.maxKeyDisplayRadius

    def animate(self, args):
        self.currentTool.animate(args)


# -----------------------------------------------------------------------------
# MAIN CLASS
# -----------------------------------------------------------------------------
class mzControlTool:
    def __init__(self):
        self.ds = DefaultControlSettings()
        self.display_L = "display_L"
        self.tm = mzToolManager()
        self.tm.findToolWindows()
        self.ui = mzControlUI(self)
        self.ui.setInitialDisplaySize()
        self.ui.updateButtons("select")

    def toolSelected(self):
        if self.tm.toolSelected():
            return True
        return False

    def checkTypeIs(self, node, testType):
        node_type = cmds.objectType(node)
        if node_type == testType:
            return True
        shape = cmds.listRelatives(node, s=True, f=True)
        if shape:
            type = cmds.nodeType(shape[0])
            if testType == type:
                return True
        return False

    def getType(self, object):
        # if cmds.objExists('%s.cycleRate' % object):
        #     return 'turtle'
        if cmds.objExists("%s.wingLength" % object):
            return "butterfly"
        if cmds.objExists("%s.waveLengths" % object):
            if cmds.objExists("%s.tailAmplitude" % object):
                return "fish"
            else:
                return "snake"
        return None

    def findObjectNameAndType(self, selected):
        # check selected node's hierarchy to see if it's a valid mzTool node
        type = self.getType(selected)
        if type:
            if selected[0] == "|":
                return selected[1:], type
            return selected, type
        parents = cmds.listRelatives(selected, parent=True, f=True)
        if parents:
            return self.findObjectNameAndType(parents[0])
        else:
            return selected, None

    def selectObject(self):
        selection = cmds.ls(sl=True)
        if selection:
            selectionName = selection[0]
            if self.checkTypeIs(selection[0], "mesh"):
                try:
                    joints = cmds.skinCluster(selection[0], query=True, wi=True)
                    selectionName = joints[0]
                except:
                    pass
            name, type = self.findObjectNameAndType(selectionName)
            print(name)
            print(type)
            if type:
                cmds.select(name)
                foundToolWindow = self.tm.setTool(type)
                if foundToolWindow:
                    self.tm.setObjectName(name)
                    self.ui.updateButtons("animate")
                    self.updateSliderDisplay()
                    return True
        self.ui.updateButtons("select")
        errorMessage("Unable to find mzTool UI for selected object!")
        return False

    def createAnimation(self, args):
        if not self.selectObject():
            return
        self.tm.animate(args)

    def createKey(self, args):
        if not self.selectObject():
            return
        pathUValue = self.tm.getPathUValue()
        t = cmds.currentTime(query=True)
        if cmds.keyframe(pathUValue, t=(t, t), q=True, kc=True):
            self.deleteKey(pathUValue, t)
            return
        cmds.setKeyframe(pathUValue, t=(t, t))
        self.updateKeyDisplay()

    def deleteKey(self, attribute, t):
        cmds.cutKey(attribute, t=(t, t))
        self.updateKeyDisplay()

    def slow(self, args):
        if not self.selectObject():
            return
        t = cmds.currentTime(q=True)
        pathUValue = self.tm.getPathUValue()
        last = cmds.findKeyframe(pathUValue, which="last")
        self.moveKeys(t, last, 1)

    def slower(self, args):
        if not self.selectObject():
            return
        t = cmds.currentTime(q=True)
        pathUValue = self.tm.getPathUValue()
        last = cmds.findKeyframe(pathUValue, which="last")
        self.moveKeys(t, last, 10)

    def fast(self, args):
        if not self.selectObject():
            return
        t = cmds.currentTime(q=True)
        pathUValue = self.tm.getPathUValue()
        prev = cmds.findKeyframe(pathUValue, which="previous")
        last = cmds.findKeyframe(pathUValue, which="last")
        if t - 1 <= prev:
            errorMessage("Will overwrite previous keyframe!")
            return
        self.moveKeys(t, last, -1)

    def faster(self, args):
        if not self.selectObject():
            return
        t = cmds.currentTime(q=True)
        pathUValue = self.tm.getPathUValue()
        prev = cmds.findKeyframe(pathUValue, which="previous")
        next = cmds.findKeyframe(pathUValue, which="next")
        last = cmds.findKeyframe(pathUValue, which="last")
        if next - 10 <= prev:
            errorMessage("Will overwrite previous keyframe!")
            return
        self.moveKeys(t, last, -10)

    def moveKeys(self, first, last, dt):
        objectName = self.tm.getObjectName()
        attributes = self.tm.getAttributes()
        for attribute in attributes:
            at = "%s.%s" % (objectName, attribute)
            cmds.keyframe(at, t=(first, last), relative=True, timeChange=dt)
        endt = last + dt
        self.tm.setEndTime(endt)

    def prevKey(self, args):
        if not self.selectObject():
            return
        objectName = self.tm.getObjectName()
        if not self.selectObject():
            return
        prev = cmds.findKeyframe(objectName, which="previous")
        cmds.currentTime(prev)

    def nextKey(self, args):
        if not self.selectObject():
            return
        objectName = self.tm.getObjectName()
        if not self.selectObject():
            return
        next = cmds.findKeyframe(objectName, which="next")
        cmds.currentTime(next)

    def playAnimation(self, args):
        if not cmds.play(query=True, state=True):
            cmds.play(forward=True)
            cmds.button("play_btn", edit=True, label="Stop")
        else:
            cmds.play(state=False)
            cmds.button("play_btn", edit=True, label="Play")

    def getCurrentSliderValue(self):
        objectName = self.tm.getObjectName()
        circleName = "%s_k0_circle" % (objectName)
        if cmds.objExists(circleName):
            radius = cmds.getAttr("%s.radius" % circleName)
            maxRadius = self.tm.getMaxKeyframeDisplayRadius()
            value = (radius / maxRadius) * self.ds.sliderRange
        else:
            value = 0.5 * self.ds.sliderRange
        return value

    def changeDisplaySize(self, sliderValue):
        objectName = self.tm.getObjectName()
        pathUValue = self.tm.getPathUValue()
        if self.tm.isSetMaxKeyDisplayRadius():
            maxRadius = self.tm.getMaxKeyframeDisplayRadius()
        else:
            pathName = self.tm.getPathName()
            maxRadius = self.calculateMaxRadiusBasedOnPath(pathName)
            self.tm.setMaxKeyframeDisplayRadius(maxRadius)
        newRadius = (sliderValue / self.ds.sliderRange) * maxRadius
        numberOfKeys = cmds.keyframe(pathUValue, query=True, kc=True)
        for n in range(numberOfKeys):
            circleName = "%s_k%i_circle" % (objectName, n)
            if cmds.objExists(circleName):
                cmds.setAttr("%s.radius" % circleName, newRadius)

    def showKeyframeLocators(self, state):
        if state == "on":
            cmds.setAttr("%s.visibility" % self.display_L, 1)
        else:
            cmds.setAttr("%s.visibility" % self.display_L, 0)

    def calculateMaxRadiusBasedOnPath(self, pathName):
        bb = cmds.exactWorldBoundingBox(pathName)
        avg = (bb[3] - bb[0]) + (bb[4] - bb[1]) + (bb[5] - bb[2]) / 3.0
        return avg / 20.0

    def updateSliderDisplay(self):
        objectName = self.tm.getObjectName()
        circleName = "%s_k0_circle" % (objectName)
        if cmds.objExists(circleName):
            radius = cmds.getAttr("%s.radius" % circleName)
            maxRadius = self.tm.getMaxKeyframeDisplayRadius()
            if not self.tm.isSetMaxKeyDisplayRadius():  # not set yet
                pathName = self.tm.getPathName()
                maxRadius = self.calculateMaxRadiusBasedOnPath(pathName)
                self.tm.setMaxKeyframeDisplayRadius(maxRadius)
            value = (radius / maxRadius) * self.ds.sliderRange
            self.ui.setSliderPosition(value)

    def updateKeyDisplay(self):
        objectName = self.tm.getObjectName()
        pathUValue = self.tm.getPathUValue()
        pathName = self.tm.getPathName()
        grpName = "%s%s" % (objectName, self.tm.displayGroup)
        existingRadius = False
        radius = 0.0
        if not cmds.objExists(grpName):
            # create a keyframe group as child of main creature group
            cmds.group(em=True, n=grpName)
            cmds.parent(grpName, objectName)
            if not cmds.objExists(self.display_L):
                cmds.createDisplayLayer(name=self.display_L, empty=True)
                cmds.setAttr("%s.overrideColorRGB" % self.display_L, 0.05, 0.4, 0.14)
            cmds.editDisplayLayerMembers(self.display_L, grpName, noRecurse=True)
        else:
            # keep the current circle radius or get a new value
            circleName = "%s_k0_circle" % (objectName)
            if cmds.objExists(circleName):
                radius = cmds.getAttr("%s.radius" % circleName)
                existingRadius = True
            # delete existing keyframe circle locators
            children = cmds.listRelatives(grpName, c=True, f=True)
            if children:
                for n in children:
                    cmds.delete(n)
        if not existingRadius:
            if not self.tm.isSetMaxKeyDisplayRadius():
                maxRadius = self.calculateMaxRadiusBasedOnPath(pathName)
                self.tm.setMaxKeyframeDisplayRadius(maxRadius)
            maxRadius = self.tm.getMaxKeyframeDisplayRadius()
            radius = maxRadius / 4.0

        # create new keyframe locator circles
        nodeDagPath = getDAGPath(pathName)
        crvFn = om.MFnNurbsCurve(nodeDagPath)
        keyTimes = cmds.keyframe(pathUValue, query=True)
        n = 0
        circles = []
        for t in keyTimes:
            uValue = cmds.getAttr(pathUValue, t=t)
            parameter = crvFn.findParamFromLength(uValue * crvFn.length())
            p = crvFn.getPointAtParam(parameter, om.MSpace.kWorld)
            norm = crvFn.tangent(parameter, om.MSpace.kWorld)
            circleName = "%s_k%i" % (objectName, n)
            name = cmds.circle(
                n=circleName,
                c=(0, 0, 0),
                nr=(norm.x, norm.y, norm.z),
                sw=360,
                r=radius,
                d=3,
                ut=0,
                tol=0,
                s=6,
                ch=1,
            )
            cmds.move(p.x, p.y, p.z, name, a=True)
            cmds.rename(name[1], "%s_circle" % circleName)
            circles.append(circleName)
            n += 1
        cmds.parent(circles, grpName)
        cmds.select(objectName)

    def displayKeys(self, args):
        if not self.selectObject():
            return
        self.showDisplayInfo()
        self.updateKeyDisplay()

    def showDisplayInfo(self):
        objectName = self.tm.getObjectName()
        displayGrpName = "%s%s" % (objectName, self.tm.displayGroup)
        # keep all key locations in a display layer
        if not cmds.objExists(self.display_L):
            cmds.createDisplayLayer(name=self.display_L, empty=True)
            cmds.setAttr("%s.overrideColorRGB" % self.display_L, 0.05, 0.4, 0.14)
            cmds.setAttr("%s.visibility" % self.display_L, 0)
            cmds.editDisplayLayerMembers(self.display_L, displayGrpName, noRecurse=True)
        if cmds.getAttr("%s.visibility" % self.display_L):
            cmds.setAttr("%s.visibility" % self.display_L, 0)
        else:
            cmds.setAttr("%s.visibility" % self.display_L, 1)
        displayLayer = cmds.listConnections(objectName, type="displayLayer")
        if displayLayer:
            if cmds.getAttr("%s.visibility" % displayLayer[0]):
                cmds.setAttr("%s.visibility" % displayLayer[0], 0)
            else:
                cmds.setAttr("%s.visibility" % displayLayer[0], 1)
