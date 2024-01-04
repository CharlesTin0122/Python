"""
mzSnakeTool_b03.py

Version: b03  updated: April 06, 2023
Author:  Steven Thomasson (www.mayazoo.net)
Description: Snake Animation Tool

Copyright (C) 2023 Steven Thomasson. All rights reserved.

"""
import maya.cmds as cmds
from maya.OpenMaya import MVector
import math


def mzSnakeTool_UI():
    """
    interface
    """
    if checkWorkingUnits() == "No":
        return

    ds = DefaultSnakeSettings()

    if cmds.window("mzSnakeToolWindow", exists=True):
        cmds.deleteUI("mzSnakeToolWindow", window=True)
    window = cmds.window(
        "mzSnakeToolWindow", title="mzSnakeTool", widthHeight=(240, 600)
    )
    cmds.scrollLayout("scrollLayout")
    cmds.columnLayout(
        adjustableColumn=True, columnOffset=("both", 4)
    )  # , backgroundColor=[1.0,0.0,0.0] )
    # ------------------------------------------------------------------
    # Skeleton
    cmds.columnLayout(rowSpacing=5)
    cmds.rowColumnLayout(
        numberOfColumns=2,
        columnWidth=[(1, 70), (2, 150)],
        columnSpacing=[(1, 0), (2, 2)],
    )
    cmds.text("Snake Name:")
    cmds.textFieldGrp("objectName_grp", text=ds.objectName, cc=changeObjectSetting)
    cmds.setParent("..")
    cmds.rowColumnLayout(
        numberOfColumns=2,
        columnWidth=[(1, 70), (2, 150)],
        columnSpacing=[(1, 0), (2, 2)],
    )
    cmds.button(
        "selectMesh_btn",
        label="Select Mesh",
        height=20,
        width=70,
        command=updateMeshField,
    )
    cmds.textFieldGrp("meshName_grp", text=ds.meshName, enable=True)
    cmds.setParent("..")
    cmds.button("createRig_btn", label="Create Rig", h=30, w=220, c=createRig)
    cmds.button(
        "attachRig_btn", label="Attach Rig", en=True, h=30, w=220, command=attachRig
    )
    cmds.text("t1", label="")
    cmds.rowColumnLayout(
        numberOfColumns=2,
        columnWidth=[(1, 70), (2, 150)],
        columnSpacing=[(1, 0), (2, 2)],
    )
    cmds.button(
        "selectPath_grp",
        label="Select Path",
        height=20,
        width=60,
        command=updatePathField,
    )
    cmds.textFieldGrp("pathName_grp", text=ds.pathName)
    cmds.setParent("..")
    cmds.rowColumnLayout(
        numberOfColumns=2,
        columnWidth=[(1, 200), (2, 15)],
        columnSpacing=[(1, 0), (2, 5), (3, 5)],
    )
    cmds.button(
        "attachSnakeToPath_btn",
        label="Attach Snake To Path",
        h=30,
        w=200,
        c=AttachSnakeToPath,
    )
    cmds.button(
        "detachSnakeFromPath_btn",
        label="D",
        en=True,
        h=30,
        w=15,
        command=detachSnakeFromPath,
    )
    cmds.setParent("..")
    cmds.rowColumnLayout(
        numberOfColumns=2,
        columnWidth=[(1, 200), (2, 15)],
        columnSpacing=[(1, 0), (2, 5), (3, 5)],
    )
    cmds.button(
        "animate_btn",
        label="Create Animation",
        h=30,
        w=200,
        command=animateWithSpeedChanges,
    )
    cmds.button(
        "deleteAnim_btn", label="D", en=True, h=30, w=15, command=deleteAnimations
    )
    cmds.setParent("..")
    cmds.text("t3", label="")
    cmds.setParent("..")
    cmds.setParent("..")
    # ------------------------------------------------------------------
    # Animation Settings
    cmds.frameLayout(collapsable=True, collapse=True, w=230, label="Animation Settings")
    cmds.columnLayout(rowSpacing=0)
    cmds.floatFieldGrp(
        "startTime_grp",
        label="          Start Frame",
        numberOfFields=1,
        value1=ds.start,
        cc=changeTimeRange,
    )
    cmds.floatFieldGrp(
        "endTime_grp",
        label="            End Frame",
        numberOfFields=1,
        value1=ds.end,
        cc=changeTimeRange,
    )
    cmds.floatFieldGrp(
        "speed_grp",
        label="Average Speed (cm/f) ",
        pre=2,
        numberOfFields=1,
        v1=ds.speed,
        cc=changeSpeedSetting,
    )
    cmds.floatFieldGrp(
        "waveLengths_grp", label="Wave Length", numberOfFields=1, v1=ds.waveLengths
    )
    cmds.floatFieldGrp(
        "waveAmplitude_grp",
        label="Wave Amplitude",
        pre=2,
        numberOfFields=1,
        v1=ds.waveAmplitude,
    )
    cmds.floatFieldGrp(
        "waveRate_grp", label="Wave Rate", pre=2, numberOfFields=1, v1=ds.waveRate
    )
    cmds.floatFieldGrp(
        "pathUValue_grp", label="Path U Value", pre=3, numberOfFields=1, v1=0.0
    )
    cmds.setParent("..")
    cmds.setParent("..")
    # ------------------------------------------------------------------
    # Add Keyframes Settings
    cmds.frameLayout(collapsable=True, collapse=True, w=230, label="Add Keyframes")
    cmds.columnLayout(rowSpacing=0)
    cmds.rowColumnLayout(
        numberOfColumns=2, columnWidth=[(1, 120), (2, 110)], columnSpacing=[(2, 0)]
    )
    cmds.checkBox("preActive_chb", label="Always Active", v=ds.preActive)
    cmds.button(
        "addKeys_btn", label="Add Keyframes", height=20, width=110, c=addKeyframes
    )
    cmds.setParent("..")
    cmds.floatFieldGrp(
        "precision_grp", label="Precision", pre=2, numberOfFields=1, value1=ds.precision
    )
    cmds.rowColumnLayout(
        numberOfColumns=3,
        columnWidth=[(1, 140), (2, 60), (3, 15)],
        columnSpacing=[(2, 2), (3, 5)],
    )
    cmds.text("Apply From Frame", align="right")
    cmds.floatField("addKeyStart_grp", pre=1, value=ds.start)
    cmds.button("addKeyStartSel_btn", label="S", height=20, width=15, c=selectKeyFrom)
    cmds.setParent("..")
    cmds.rowColumnLayout(
        numberOfColumns=3,
        columnWidth=[(1, 140), (2, 60), (3, 15)],
        columnSpacing=[(2, 2), (3, 5)],
    )
    cmds.text("To Frame", align="right")
    cmds.floatField("addKeyEnd_grp", pre=1, value=ds.end)
    cmds.button("addKeyEndSel_btn", label="S", height=20, width=15, c=selectKeyTo)
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.setParent("..")
    # ------------------------------------------------------------------
    # Custom Rig Settings
    cmds.frameLayout(collapsable=True, collapse=True, w=230, label="Rig Settings")
    cmds.columnLayout(rowSpacing=0)
    cmds.intFieldGrp(
        "numberOfJoints_grp",
        label="Number of Joints",
        numberOfFields=1,
        value1=ds.numberOfJoints,
    )
    cmds.intFieldGrp(
        "numberOfControls_grp",
        label="Number of Controls",
        numberOfFields=1,
        value1=ds.numberOfControls,
    )
    cmds.intFieldGrp(
        "numberOfHandles_grp",
        label="Number of Handles",
        numberOfFields=1,
        value1=ds.numberOfHandles,
    )
    cmds.rowColumnLayout(
        numberOfColumns=2,
        columnWidth=[(1, 140), (2, 80)],
        columnSpacing=[(1, 0), (2, 2)],
    )
    cmds.button(
        "enableJointLength_btn",
        label="Joint Length",
        height=15,
        width=70,
        command=enableJointLengthField,
    )
    cmds.floatField(
        "jointLength_grp", enable=False, width=80, pre=4.0, v=ds.jointLength
    )
    cmds.setParent("..")
    cmds.floatFieldGrp(
        "snakeLength_grp",
        label="Snake Length",
        enable=False,
        pre=4.0,
        numberOfFields=1,
        value1=ds.snakeLength,
    )
    cmds.setParent("..")
    cmds.setParent("..")
    # ------------------------------------------------------------------
    # Progress Bar
    cmds.frameLayout(collapsable=False, collapse=False, w=230, label="Progress Bar")
    cmds.textField("progressUpdate_fld", text=" ... ", width=100)
    cmds.progressBar("progressControl_grp", maxValue=100, width=220)
    cmds.setParent("..")
    cmds.setParent("..")

    updateUI(ds.objectName)
    cmds.showWindow("mzSnakeToolWindow")


# ----------------------------------------------------------------------------------------------------
# CLASS DECLARATIONS
# ----------------------------------------------------------------------------------------------------
class DefaultSnakeSettings:
    def __init__(self):
        self.objectName = "snake1"
        self.meshName = "..."
        self.pathName = "..."
        self.speed = 1.0
        self.numberOfJoints = 30
        self.numberOfControls = 15
        self.numberOfHandles = 2
        self.jointLength = 0.1
        self.snakeLength = 0.0
        self.start = 0.0
        self.end = 2000.0
        self.waveLengths = 4.0
        self.waveAmplitude = 1.00
        self.waveRate = 1.0
        self.pathUValue = 0.0
        self.precision = 1.0
        self.preActive = False


class SnakeToolUI:
    "settings for each individual snake"

    def __init__(self):
        self.objectName = cmds.textFieldGrp("objectName_grp", query=True, text=True)
        self.meshName = cmds.textFieldGrp("meshName_grp", query=True, text=True)
        self.pathName = cmds.textFieldGrp("pathName_grp", query=True, text=True)
        self.speed = cmds.floatFieldGrp("speed_grp", query=True, v1=True)
        self.numberOfJoints = cmds.intFieldGrp(
            "numberOfJoints_grp", query=True, v1=True
        )
        self.numberOfControls = cmds.intFieldGrp(
            "numberOfControls_grp", query=True, v1=True
        )
        self.numberOfHandles = cmds.intFieldGrp(
            "numberOfHandles_grp", query=True, v1=True
        )
        self.jointLength = cmds.floatField("jointLength_grp", query=True, v=True)
        self.snakeLength = cmds.floatFieldGrp("snakeLength_grp", query=True, v1=True)
        self.start = cmds.floatFieldGrp("startTime_grp", query=True, v1=True)
        self.end = cmds.floatFieldGrp("endTime_grp", query=True, v1=True)
        self.waveLengths = cmds.floatFieldGrp("waveLengths_grp", query=True, v1=True)
        self.waveAmplitude = cmds.floatFieldGrp(
            "waveAmplitude_grp", query=True, v1=True
        )
        self.waveRate = cmds.floatFieldGrp("waveRate_grp", query=True, v1=True)
        self.preActive = cmds.checkBox("preActive_chb", query=True, v=True)
        self.precision = cmds.floatFieldGrp("precision_grp", query=True, v1=True)
        self.addKeyStart = cmds.floatField("addKeyStart_grp", query=True, v=True)
        self.addKeyEnd = cmds.floatField("addKeyEnd_grp", query=True, v=True)

    def set_meshName(self, meshName):
        self.meshName = meshName
        cmds.textFieldGrp("meshName_grp", edit=True, text=meshName)

    def set_pathName(self, pathName):
        self.pathName = pathName
        cmds.textFieldGrp("pathName_grp", edit=True, text=pathName)

    def set_jointLength(self, jointLength):
        self.jointLength = jointLength
        cmds.floatField("jointLength_grp", edit=True, value=jointLength)

    def set_snakeLength(self, snakeLength):
        self.snakeLength = snakeLength
        cmds.floatFieldGrp("snakeLength_grp", edit=True, value1=snakeLength)

    def set_addKeyFrom(self, t):
        self.addKeyStart = t
        if t >= self.addKeyEnd:
            self.addKeyStart = self.addKeyEnd - 1
        cmds.floatField("addKeyStart_grp", edit=True, value=self.addKeyStart)

    def set_addKeyTo(self, t):
        self.addKeyEnd = t
        if t <= self.addKeyStart:
            self.addKeyEnd = self.addKeyStart + 1
        cmds.floatField("addKeyEnd_grp", edit=True, value=self.addKeyEnd)

    def jointLengthEnabled(self):
        return cmds.floatField("jointLength_grp", query=True, enable=True)

    def enableJointLengthField(self):
        if self.jointLengthEnabled():
            cmds.floatField("jointLength_grp", edit=True, enable=False)
        else:
            cmds.floatField("jointLength_grp", edit=True, enable=True)


class SnakeControlNames:
    def __init__(self, ui):
        self.objectName = ui.objectName
        self.numberOfJoints = ui.numberOfJoints
        self.numberOfControls = ui.numberOfControls
        self.numberOfHandles = ui.numberOfHandles
        self.skeletonGrp = "%s_skeleton" % ui.objectName
        self.controlGrp = "%s_controls" % ui.objectName
        self.handleName = "spine_CTRL"
        self.pathName = "%s_path" % ui.objectName
        self.ctrlPositions = "%s_ctrlPositions" % ui.objectName
        self.ctrlCurve = "%s_ctrlCurve" % ui.objectName
        self.pathUValue = "%s.pathUValue" % ui.objectName
        self.pathCtrl = "ctrl_"
        self.skelCtrl = "ctrlJN_"
        self.headTrnCtrl = "head_TRN_CTRL"
        self.frontTwistCtrl = "twist_FRONT_CTRL"
        self.backTwistCtrl = "twist_BACK_CTRL"
        self.expName_uValues = "%s_exp_uValues" % ui.objectName
        self.expName_twistControls = "%s_exp_twistControls" % ui.objectName

    def getHeadJointName(self):
        return "%s|%s|ctrl_0|%s|%s|%s_head" % (
            self.objectName,
            self.controlGrp,
            self.frontTwistCtrl,
            self.headTrnCtrl,
            self.objectName,
        )

    def getHeadTrnCtrlName(self):
        return "%s|%s|ctrl_0|%s|%s" % (
            self.objectName,
            self.controlGrp,
            self.frontTwistCtrl,
            self.headTrnCtrl,
        )

    def getJointNames(self):
        jointNames = []
        jointNames.append(self.getHeadJointName())
        name = "%s|%s|joint1" % (self.objectName, self.skeletonGrp)
        for n in range(2, self.numberOfJoints + 1):
            name += "|joint%i" % (n)
            jointNames.append(name)
        return jointNames

    def getPathControlNames(self):
        pathCtrls = []
        for n in range(0, self.numberOfControls):
            pathCtrls.append(
                "%s|%s|%s%i" % (self.objectName, self.controlGrp, self.pathCtrl, n)
            )
        return pathCtrls

    def getCurveControlNames(self):
        skelCtrls = []
        skelCtrls.append(
            "%s|%s|%s0|%s|%s|%s0"
            % (
                self.objectName,
                self.controlGrp,
                self.pathCtrl,
                self.frontTwistCtrl,
                self.headTrnCtrl,
                self.skelCtrl,
            )
        )
        i = 1
        for n in range(0, self.numberOfHandles):
            skelCtrls.append(
                "%s|%s|%s%i|%s%i|%s%i"
                % (
                    self.objectName,
                    self.controlGrp,
                    self.pathCtrl,
                    i,
                    self.handleName,
                    i,
                    self.skelCtrl,
                    i,
                )
            )
            i += 1
        for n in range(i, self.numberOfControls):
            skelCtrls.append(
                "%s|%s|%s%i|%s%i"
                % (self.objectName, self.controlGrp, self.pathCtrl, n, self.skelCtrl, n)
            )
        return skelCtrls

    def getSpineHandleNames(self):
        names = []
        for n in range(0, self.numberOfHandles):
            names.append("spine_CTRL%i" % (n + 1))
        return names

    def getMotionPathNames(self):
        mPathNames = []
        for n in range(0, self.numberOfControls):
            mPathNames.append("%s_mPath%i" % (self.objectName, n + 1))
        return mPathNames


class SnakeInfo:
    def __init__(self, meshName):
        self.meshName = meshName
        self.bb = cmds.polyEvaluate(meshName, b=True)
        self.length = self.bb[0][1] - self.bb[0][0]
        self.height = self.bb[1][1] - self.bb[1][0]


class AnimationManager:
    def __init__(self):
        self.ui = SnakeToolUI()
        self.cn = SnakeControlNames(self.ui)

        path = self.ui.pathName
        self.curveLength = cmds.arclen(path)
        self.path_uValue = self.cn.pathUValue
        self.objectName = self.ui.objectName
        self.numberOfJoints = self.ui.numberOfJoints
        self.numberOfControls = self.ui.numberOfControls
        self.jointLength = self.ui.jointLength
        self.snakeLength = (self.numberOfJoints - 1) * self.jointLength

        self.ctrlNames = self.cn.getCurveControlNames()  # control names used for keying

        self.delay = []  # controls distance behind 1st control
        self.amplitude = []  # controls maximum sidewards movement
        self.initializeMovementSettings()

        self.nDist = []  # controls current distance along movement cycle
        self.nSide = []  # side to side movement (which side for ontrols next key)
        self.wAmp = []  # controls sidewards movement for it's next key
        self.cycDist = []  # movement distance until this controls next key

        self.dz = []  # temp precision setting
        self.tz = []
        self.preActive = self.ui.preActive
        self.precision = self.ui.precision
        self.addKeyStart = self.ui.addKeyStart
        self.addKeyEnd = self.ui.addKeyEnd

        self.waveLengths = 1.0
        self.waveAmplitude = 1.0
        self.waveRate = 1.0

        self.snakeHasStopped = False
        self.snakeIsMotionless = False
        self.snakeHasStarted = False

        self.kf = []
        self.nextKey = -1
        # self.findPathKeyframes( path_uValue )

    def findPathKeyframes(self, path_uValue):
        numberOfKeys = cmds.keyframe(path_uValue, q=True, kc=True)
        if numberOfKeys >= 2:
            firstKeyframe = cmds.findKeyframe(path_uValue, which="first")
            lastKeyframe = cmds.findKeyframe(path_uValue, which="last")
            t = firstKeyframe
            for n in range(numberOfKeys):
                self.kf.append(t)
                t = cmds.findKeyframe(path_uValue, time=(t, t), which="next")

    def initializeMovementSettings(self):
        # calculate control positions for each control
        # ctrlPos = []
        ctrlPositionsCurve = self.cn.ctrlPositions
        ctrlPos = calculateControlPositions(ctrlPositionsCurve, self.ui)

        # set initial delay offset distances for each control
        for n in range(self.numberOfControls):
            self.delay.append(ctrlPos[n])

        # calculate maximum side movement for each ctrl
        initialWaveAmplitude = (self.numberOfJoints * self.jointLength) * 0.06
        for n in range(0, self.numberOfControls):
            self.amplitude.append(
                math.sin((ctrlPos[n] / ctrlPos[self.numberOfControls - 1]) * math.pi)
                * initialWaveAmplitude
            )

    def initializePrecision(self):
        for n in range(self.numberOfControls):
            self.dz.append(0.0)
            self.tz.append(0.0)

    def updatePrecision(self, t, tt):
        # t1 = t+1
        distPerFrame = self.getDistanceMovedThisFrame(t)

        for n in range(self.numberOfControls):
            tempCycDist = self.cycDist[n]
            if self.cycDist[n] == -1:
                tempCycDist = self.cycDist[0]

            if self.preActive or (t >= self.addKeyStart and t <= self.addKeyEnd):
                tz = (
                    self.nSide[n]
                    * math.cos((self.nDist[n] / tempCycDist) * math.pi)
                    * self.amplitude[n]
                    * self.wAmp[n]
                )
                dz = cmds.getAttr("%s.translateZ" % self.ctrlNames[n], t=(t))
                d = abs(tz - dz)
                allreadyKeyed = cmds.selectKey(
                    "%s.translateZ" % self.ctrlNames[n], add=True, k=True, t=(t, t)
                )
                if not allreadyKeyed and d > self.precision:
                    cmds.setKeyframe(
                        self.ctrlNames[n], time=(t, t), attribute="translateZ", value=tz
                    )
                    cmds.keyTangent(self.ctrlNames[n], time=(t, t), itt=tt, ott=tt)

            self.nDist[n] += distPerFrame

            if self.nDist[n] >= self.cycDist[n] and self.cycDist[n] != -1:
                if n == 0:
                    for i in range(1, self.numberOfControls):
                        if self.cycDist[i] == -1:
                            self.cycDist[i] = self.cycDist[0]

                self.nSide[n] = self.switchSides(self.nSide[n])
                self.nDist[n] = self.nDist[n] - self.cycDist[n]

                if n < self.numberOfControls - 1:
                    self.wAmp[n + 1] = self.wAmp[n]

                if self.delay[n] < self.nDist[0]:
                    self.cycDist[n] = -1
                else:
                    self.cycDist[n] = self.cycDist[n - 1]

    def updateAnimationSettings(self, t):
        self.waveLengths = cmds.getAttr("%s.waveLengths" % self.objectName, t=(t))
        self.waveAmplitude = cmds.getAttr("%s.waveAmplitude" % self.objectName, t=(t))
        self.waveRate = cmds.getAttr("%s.waveRate" % self.objectName, t=(t))

    def switchSides(self, side):
        if side == 1:
            return -1
        else:
            return 1

    def setInitialPosition(self, t):
        # create keyframes for snakes starting position
        self.updateAnimationSettings(t)
        swimCycleDistance = self.snakeLength / (self.waveLengths * 2.0)

        for n in range(0, self.numberOfControls):
            self.nDist.append(swimCycleDistance - self.delay[n] % swimCycleDistance)
            self.wAmp.append(self.waveAmplitude)
            self.cycDist.append(swimCycleDistance)
            # save which side the control is currently on
            s = -1
            numberOfCycles = 1
            while self.delay[n] > (numberOfCycles * swimCycleDistance):
                numberOfCycles += 1
                s = self.switchSides(s)
            self.nSide.append(s)

            sideMovement = (
                math.cos((self.delay[n] / swimCycleDistance) * math.pi)
                * self.amplitude[n]
                * self.waveAmplitude
            )
            cmds.setKeyframe(
                self.ctrlNames[n],
                time=(t, t),
                attribute="translateZ",
                value=sideMovement,
            )
            cmds.keyTangent(self.ctrlNames[n], time=(t, t), itt="linear", ott="linear")

    def getDistanceMovedThisFrame(self, t):
        # calc distance the snake moves from this frame to the next
        t0 = t + 0
        t1 = t + 1
        v0 = cmds.getAttr(self.path_uValue, t=(t0))
        v1 = cmds.getAttr(self.path_uValue, t=(t1))
        distPerFrame = (v1 - v0) * self.curveLength * self.waveRate
        return distPerFrame

    def snakeHasStoppedMoving(self):
        if self.snakeHasStopped:
            self.snakeHasStopped = False
            return True
        return False

    def snakeHasStartedMoving(self):
        if self.snakeHasStarted:
            self.snakeHasStarted = False
            return True
        return False

    def updateSnakeMovement(self, dist):
        if dist <= 0.0:
            if not self.snakeIsMotionless:
                self.snakeHasStopped = True
                self.snakeIsMotionless = True
        else:
            if self.snakeIsMotionless:
                self.snakeHasStarted = True
                self.snakeIsMotionless = False

    def moveAlongPath(self, t):
        self.updateAnimationSettings(t)
        self.wAmp[0] = self.waveAmplitude
        self.cycDist[0] = self.snakeLength / (self.waveLengths * 2.0)  # *waveRate

    def keyAllControlsAtTime(self, t, tt):
        cycleDist = []
        for n in range(self.numberOfControls):
            cycleDist.append(self.cycDist[n])
            if self.cycDist[n] == -1:
                cycleDist[n] = self.cycDist[0]

        for n in range(self.numberOfControls):
            sideMovement = (
                self.nSide[n]
                * math.cos((self.nDist[n] / cycleDist[n]) * math.pi)
                * self.amplitude[n]
                * self.wAmp[n]
            )  # waveAmplitude
            cmds.setKeyframe(
                self.ctrlNames[n],
                time=(t, t),
                attribute="translateZ",
                value=sideMovement,
            )
            cmds.keyTangent(self.ctrlNames[n], time=(t, t), itt=tt, ott=tt)

    def update(self, t):
        # create keyframes for each control if required at this frame
        # t1 = t+1
        distPerFrame = self.getDistanceMovedThisFrame(t)
        self.updateSnakeMovement(distPerFrame)

        for n in range(self.numberOfControls):
            self.nDist[n] += distPerFrame

        for n in range(self.numberOfControls):
            if self.nDist[n] >= self.cycDist[n] and self.cycDist[n] != -1:
                # update any controls waiting for a cycDist
                if n == 0:
                    for i in range(1, self.numberOfControls):
                        if self.cycDist[i] == -1:
                            self.cycDist[i] = self.cycDist[0]

                sideMovement = 0.0 - self.nSide[n] * self.amplitude[n] * self.wAmp[n]
                self.nSide[n] = self.switchSides(self.nSide[n])
                cmds.setKeyframe(
                    self.ctrlNames[n],
                    time=(t, t),
                    attribute="translateZ",
                    value=sideMovement,
                )
                cmds.keyTangent(self.ctrlNames[n], time=(t, t), itt="flat", ott="flat")
                self.nDist[n] = self.nDist[n] - self.cycDist[n]

                # update control amplitudes to follow movement of control in front
                if n < self.numberOfControls - 1:
                    self.wAmp[n + 1] = self.wAmp[n]

                # cycDist[0] changes each frame so wait for it to key before setting following cycDist's
                if self.delay[n] < self.nDist[0]:
                    self.cycDist[n] = -1
                else:
                    self.cycDist[n] = self.cycDist[n - 1]


class uValueKey:
    def __init__(self, t, value, itt, ott):
        self.t = t
        self.value = value
        self.itt = itt
        self.ott = ott


# -----------------------------------------------------------------------------
# Dialog Boxes
# -----------------------------------------------------------------------------
def errorMessage(msg):
    cmds.confirmDialog(
        title=" ",
        message=msg,
        button="OK",
        defaultButton="OK",
        cancelButton="OK",
        dismissString="OK",
    )


def yesNoDialogBox(msg):
    return cmds.confirmDialog(
        title=" ",
        message=msg,
        button=["Yes", "No"],
        defaultButton="Yes",
        cancelButton="No",
        dismissString="No",
    )


# -----------------------------------------------------------------------------
# Progress Bar Functions
# -----------------------------------------------------------------------------
def progressControl():
    cmds.progressBar("progressControl_grp", edit=True, step=1)


def resetProgressControl():
    cmds.progressBar("progressControl_grp", edit=True, progress=0)


def setProgressControlMaxValue(maxValue):
    cmds.progressBar("progressControl_grp", edit=True, maxValue=maxValue)


def progressControlUpdate(textUpdate):
    cmds.textField("progressUpdate_fld", edit=True, text=textUpdate)


# -----------------------------------------------------------------------------
def checkWorkingUnits():
    workingUnits = cmds.currentUnit(query=True, linear=True)
    if workingUnits != "cm":
        msg = "mzSnakeTool requires Working Units set to centimeter\nIs it ok to reset working units to centimeter?"
        ok = cmds.confirmDialog(
            title="Working Units",
            message=msg,
            button=["Yes", "No"],
            defaultButton="Yes",
            cancelButton="No",
            dismissString="No",
        )
        if ok == "Yes":
            cmds.currentUnit(linear="cm")
        return ok


# -----------------------------------------------------------------------------
# UPDATE UI - functions
# -----------------------------------------------------------------------------
def updateMeshField(args):
    ui = SnakeToolUI()
    mesh = selectMesh()
    if mesh:
        ui.set_meshName(mesh)
        snakeLength = getLengthOfMesh(mesh)
        ui.set_snakeLength(snakeLength)
        updateButtons()


def updatePathField(args):
    ui = SnakeToolUI()
    path = selectPath()
    if path:
        ui.set_pathName(path)


def selectKeyFrom(args):
    t = cmds.currentTime(query=True)
    ui = SnakeToolUI()
    ui.set_addKeyFrom(t)


def selectKeyTo(args):
    t = cmds.currentTime(query=True)
    ui = SnakeToolUI()
    ui.set_addKeyTo(t)


def updateTimeRange():
    speed = cmds.floatFieldGrp("speed_grp", query=True, value1=True)
    path = cmds.textFieldGrp("pathName_grp", query=True, text=True)
    start = cmds.floatFieldGrp("startTime_grp", query=True, value1=True)
    end = cmds.floatFieldGrp("endTime_grp", query=True, value1=True)

    if cmds.objExists(path):
        curveLength = cmds.arclen(path)
        end = (curveLength / speed) + start
    cmds.floatFieldGrp("endTime_grp", edit=True, v1=end)


def changeSpeedSetting(args):
    updateTimeRange()
    updatePathAnimation()


def changeTimeRange(args):
    start = cmds.floatFieldGrp("startTime_grp", query=True, value1=True)
    end = cmds.floatFieldGrp("endTime_grp", query=True, value1=True)
    updateSpeedSetting(start, end)
    updatePathAnimation()


def updateSpeedSetting(start, end):
    path = cmds.textFieldGrp("pathName_grp", query=True, text=True)
    if cmds.objExists(path):
        curveLength = cmds.arclen(path)
        timeRange = end - start
        speed = curveLength / timeRange
        cmds.floatFieldGrp("speed_grp", edit=True, value1=speed)


def updatePathAnimation():
    # if fish is attached to the path then update the path uValues
    ui = SnakeToolUI()
    cn = SnakeControlNames(ui)
    if cmds.objExists(cn.pathUValue):
        start = ui.start
        end = ui.end
        numberOfKeys = cmds.keyframe(cn.pathUValue, q=True, kc=True)
        if numberOfKeys < 2:
            errorMessage("Missing path U Value keyframes")
            return
        first = cmds.findKeyframe(cn.pathUValue, which="first")
        last = cmds.findKeyframe(cn.pathUValue, which="last")

        # shift the keyframes and then scale them
        amount = start - first
        cmds.keyframe(cn.pathUValue, t=(first, last), relative=True, timeChange=amount)
        ts = (end - start) / (last - first)
        cmds.scaleKey(
            cn.pathUValue, timeScale=ts, timePivot=start, valueScale=1.0, valuePivot=0.0
        )


def changeObjectSetting(args):
    objectName = cmds.textFieldGrp("objectName_grp", query=True, text=True)
    updateUI(objectName)


def enableJointLengthField(args):
    ui = SnakeToolUI()
    ui.enableJointLengthField()


def checkTypeIs(node, testType):
    shape = cmds.listRelatives(node, s=True)
    if shape:
        type = cmds.nodeType(shape[0])
        if testType == type:
            return True
    else:
        if cmds.objectType(node, isType=testType):
            return True
    return False


def getTransformNode(node):
    if cmds.objectType(node, isType="transform"):
        return node
    else:
        p = cmds.listRelatives(node, p=True)[0]
        if cmds.objectType(p, isType="transform"):
            return p
    return None


def selectMesh():
    selection = cmds.ls(sl=True)
    if len(selection) == 0:
        errorMessage("Select a mesh for the snake's body!")
        return None
    if not checkTypeIs(selection[0], "mesh"):
        errorMessage("Select a Mesh")
        return None
    return getTransformNode(selection[0])


def selectPath():
    selection = cmds.ls(sl=True)
    if len(selection) == 0:
        errorMessage("Select a path for the snake to move along!")
        return None
    if not checkTypeIs(selection[0], "nurbsCurve"):
        errorMessage("Select a Curve for the snake's path!")
        return None
    return getTransformNode(selection[0])


def getNumberOfJoints(objectName):
    n = 1
    jointName = "%s|%s_skeleton|joint%i" % (objectName, objectName, n)
    numberOfJoints = 0
    while cmds.objExists(jointName):
        numberOfJoints += 1
        n += 1
        jointName += "|joint%i" % (n)
    return numberOfJoints


def getNumberOfControls(objectName):
    n = 0
    ctrlName = "%s|%s_controls|ctrl_%i" % (objectName, objectName, n)
    numberOfControls = 0
    while cmds.objExists(ctrlName):
        numberOfControls += 1
        n += 1
        ctrlName = "%s|%s_controls|ctrl_%i" % (objectName, objectName, n)
    return numberOfControls


def getNumberOfHandles(objectName):
    ui = SnakeToolUI()
    cn = SnakeControlNames(ui)
    n = 1
    handleName = "%s|%s_controls|%s%i|%s%i" % (
        objectName,
        objectName,
        cn.pathCtrl,
        n,
        cn.handleName,
        n,
    )
    numberOfHandles = 0
    while cmds.objExists(handleName):
        numberOfHandles += 1
        n += 1
        handleName = "%s|%s_controls|%s%i|%s%i" % (
            objectName,
            objectName,
            cn.pathCtrl,
            n,
            cn.handleName,
            n,
        )
    return numberOfHandles


def calculateJointLength(objectName):
    ctrl_0 = "%s|%s_skeleton|joint1" % (objectName, objectName)
    ctrl_1 = "%s|%s_skeleton|joint1|joint2" % (objectName, objectName)
    pos0 = cmds.xform(ctrl_0, worldSpace=True, query=True, translation=True)
    pos1 = cmds.xform(ctrl_1, worldSpace=True, query=True, translation=True)
    vec = MVector(pos1[0], pos1[1], pos1[2]) - MVector(pos0[0], pos0[1], pos0[2])
    return vec.length()


def getLength(objectName):
    ui = SnakeToolUI()
    cn = SnakeControlNames(ui)
    ctrlPosCurve = cn.ctrlPositions
    length = cmds.arclen(ctrlPosCurve)
    return length


def updateUI(objectName):
    if cmds.objExists(objectName):
        meshName = "%s_mesh" % objectName
        pathName = "%s_path" % objectName
        if cmds.objExists(meshName):
            cmds.textFieldGrp("meshName_grp", edit=True, text=meshName)
        if cmds.objExists(pathName):
            cmds.textFieldGrp("pathName_grp", edit=True, text=pathName)
            path_uValue = "%s.pathUValue" % objectName
            if cmds.objExists(path_uValue):
                numberOfKeys = cmds.keyframe(path_uValue, q=True, kc=True)
                if numberOfKeys >= 2:
                    firstKeyframe = cmds.findKeyframe(path_uValue, which="first")
                    lastKeyframe = cmds.findKeyframe(path_uValue, which="last")
                    cmds.floatFieldGrp("startTime_grp", edit=True, v1=firstKeyframe)
                    cmds.floatFieldGrp("endTime_grp", edit=True, v1=lastKeyframe)
                    cmds.floatField("addKeyStart_grp", edit=True, v=firstKeyframe)
                    cmds.floatField("addKeyEnd_grp", edit=True, v=lastKeyframe)
                    updateSpeedSetting(firstKeyframe, lastKeyframe)
        cmds.intFieldGrp(
            "numberOfJoints_grp", edit=True, v1=getNumberOfJoints(objectName)
        )
        cmds.intFieldGrp(
            "numberOfControls_grp", edit=True, v1=getNumberOfControls(objectName)
        )
        cmds.intFieldGrp(
            "numberOfHandles_grp", edit=True, v1=getNumberOfHandles(objectName)
        )
        cmds.floatField(
            "jointLength_grp", edit=True, v=calculateJointLength(objectName)
        )
        cmds.floatFieldGrp("snakeLength_grp", edit=True, v1=getLength(objectName))
    else:
        ds = DefaultSnakeSettings()
        cmds.textFieldGrp("meshName_grp", edit=True, text=ds.meshName)
        cmds.textFieldGrp("pathName_grp", edit=True, text=ds.pathName)
        cmds.intFieldGrp("numberOfJoints_grp", edit=True, v1=ds.numberOfJoints)
        cmds.intFieldGrp("numberOfControls_grp", edit=True, v1=ds.numberOfControls)
        cmds.floatField("jointLength_grp", edit=True, v=ds.jointLength)
        cmds.floatFieldGrp("startTime_grp", edit=True, v1=ds.start)
        cmds.floatFieldGrp("endTime_grp", edit=True, v1=ds.end)
        cmds.floatFieldGrp("waveLengths_grp", edit=True, v1=ds.waveLengths)
        cmds.floatFieldGrp("waveAmplitude_grp", edit=True, v1=ds.waveAmplitude)
        cmds.floatFieldGrp("waveRate_grp", edit=True, v1=ds.waveRate)
    if cmds.objExists("%s.waveLengths" % objectName):
        cmds.connectControl("waveLengths_grp", "%s.waveLengths" % objectName, index=2)
    if cmds.objExists("%s.waveAmplitude" % objectName):
        cmds.connectControl(
            "waveAmplitude_grp", "%s.waveAmplitude" % objectName, index=2
        )
    if cmds.objExists("%s.waveRate" % objectName):
        cmds.connectControl("waveRate_grp", "%s.waveRate" % objectName, index=2)
    if cmds.objExists("%s.pathUValue" % objectName):
        cmds.connectControl("pathUValue_grp", "%s.pathUValue" % objectName, index=2)
    updateButtons()


def updateButtons():
    objectName = cmds.textFieldGrp("objectName_grp", query=True, text=True)
    # reset all buttons to grey
    cmds.button("createRig_btn", edit=True, bgc=(0.365, 0.365, 0.365))
    cmds.button("attachRig_btn", edit=True, bgc=(0.365, 0.365, 0.365))
    cmds.button("attachSnakeToPath_btn", edit=True, bgc=(0.365, 0.365, 0.365))
    cmds.button("animate_btn", edit=True, bgc=(0.365, 0.365, 0.365))
    # find which button should be green
    if not cmds.objExists(objectName):
        cmds.button("createRig_btn", edit=True, bgc=(0.1, 0.5, 0.3))
        return
    if not cmds.objExists("%s_skinCluster" % objectName):
        cmds.button("attachRig_btn", edit=True, bgc=(0.1, 0.5, 0.3))
        return
    if not cmds.objExists("%s_mPath1" % objectName):
        cmds.button("attachSnakeToPath_btn", edit=True, bgc=(0.1, 0.5, 0.3))
        return
    cmds.button("animate_btn", edit=True, bgc=(0.1, 0.5, 0.3))


# -----------------------------------------------------------------------------
# DELETE SNAKE
# -----------------------------------------------------------------------------
def DeleteAll(args):
    progressControlUpdate("... DeleteAll() ...")
    objectName = cmds.textFieldGrp("objectName_grp", query=True, text=True)
    if cmds.objExists(objectName):
        cmds.delete(objectName)


# -----------------------------------------------------------------------------
# CREATE RIG (SKELETON & CONTROLS)
# -----------------------------------------------------------------------------
def createRig(args):
    ui = SnakeToolUI()
    cn = SnakeControlNames(ui)
    ds = DefaultSnakeSettings()
    selection = cmds.ls(sl=True)
    if cmds.objExists(ui.objectName):
        result = yesNoDialogBox(
            "%s already exists!\nWould you like to create a new Rig?" % ui.objectName
        )
        if result == "Yes":
            cmds.delete(ui.objectName)
        else:
            return
    if not cmds.objExists(ui.meshName):
        mesh = selectMesh()
        if mesh:
            updateMesh(ui, mesh)
        else:
            return
    updateMesh(ui, ui.meshName)
    if not checkTypeIs(ui.meshName, "mesh"):
        errorMessage("Select a polygon mesh for the snake's body")
        return
    result = createSkeleton(ui, cn, ds)
    if not result:
        return
    createControls(ui, cn)
    updateButtons()
    progressControlUpdate("... finished creating Rig ... ")


# -----------------------------------------------------------------------------
# rig helper functions
# -----------------------------------------------------------------------------
def getLengthOfMesh(meshName):
    # get the mesh bounding box
    bb = cmds.polyEvaluate(meshName, b=True)
    xLength = bb[0][1] - bb[0][0]
    zLength = bb[2][1] - bb[2][0]

    # make sure mesh is aligned with positive x-axis
    if zLength > xLength:
        errorMessage(
            "mesh position error: Make sure snake is aligned along the positive x-axis"
        )
        return 0
    if abs(bb[0][1]) > abs(bb[0][0]):  # if abs(xMax) > abs(xMin)
        errorMessage("mesh position error: See instructions for mesh positioning")
        return 0
    return abs(bb[0][0])  # length from neck to tail


def createMeshBackup(objectName, bodyName):
    # create a layer for the backup copy
    origBodyLayer = "snake_meshOrig_L"
    if not cmds.objExists(origBodyLayer):
        cmds.createDisplayLayer(name=origBodyLayer, number=1, empty=True)

    # create the backup copy
    origBodyName = "%s_mesh_orig" % objectName
    if not cmds.objExists(origBodyName):
        cmds.duplicate(bodyName, n=origBodyName)
        cmds.editDisplayLayerMembers(origBodyLayer, origBodyName, noRecurse=True)


def updateMesh(ui, mesh):
    objectName = ui.objectName
    meshName = "%s_mesh" % objectName
    meshOrig = "%s_mesh_orig" % objectName
    meshLayer = "snake_mesh_L"

    if cmds.objExists(mesh):
        cmds.rename(mesh, meshName)

    # create a backup copy of the skin mesh
    if not cmds.objExists(meshOrig):
        createMeshBackup(objectName, meshName)

    # if no mesh exists duplicate one from the original skin mesh
    if not cmds.objExists(meshName):
        cmds.duplicate(meshOrig, n=meshName)

    if not cmds.objExists(meshLayer):
        cmds.createDisplayLayer(name=meshLayer, number=1, empty=True)
    cmds.editDisplayLayerMembers(meshLayer, meshName, noRecurse=True)
    cmds.textFieldGrp("meshName_grp", edit=True, text=meshName)
    ui.set_meshName(meshName)

    cmds.select(cl=True)
    cmds.select(meshName, r=True)
    cmds.delete(constructionHistory=True)
    cmds.select(cl=True)


# -----------------------------------------------------------------------------
# CREATE SKELETON
# -----------------------------------------------------------------------------
def createSkeleton(ui, cn, ds):
    progressControlUpdate("... creating Skeleton ... ")

    objectName = ui.objectName
    meshName = ui.meshName
    numberOfJoints = ui.numberOfJoints
    numberOfControls = ui.numberOfControls
    jointLength = ui.jointLength
    splineHandleName = objectName + "_splineHandle"
    jointLayer = "snake_joints_L"
    ctrlCurve = cn.ctrlCurve
    ctrlPositionsCurve = cn.ctrlPositions
    numberOfCVs = numberOfControls - 1

    # get mesh length for joint length calculation
    snakeLength = getLengthOfMesh(meshName)
    if not snakeLength:
        return snakeLength
    ui.set_snakeLength(snakeLength)

    if not ui.jointLengthEnabled():
        jointLength = snakeLength / float(numberOfJoints - 1)
        ui.set_jointLength(jointLength)

    # create a joint for the head
    cmds.select(clear=True)
    headJointName = "%s_head" % objectName
    if cmds.objExists(headJointName):
        print("Error: head joint already exists")
        return
    cmds.joint(p=(0, 0, 0), name=headJointName)
    cmds.setAttr("%s.visibility" % headJointName, 0)

    # create the body joints
    cmds.select(clear=True)
    if cmds.objExists("%s|joint1" % objectName):
        print("Error: joint1 already exists")
        return False
    x = 0
    for n in range(1, numberOfJoints + 1):
        jointName = "|joint%i" % (n)
        cmds.joint(p=(x, 0, 0), name=jointName)
        x -= jointLength

    # set joint transforms to work with splineIK
    cmds.select(clear=True)
    jointName = ""
    for n in range(1, numberOfJoints):
        jointName += "|joint%i" % (n)
        cmds.select(jointName)
        cmds.joint(edit=True, zso=True, oj="xyz", sao="yup")

    # attach splineIK to skeleton
    joint1 = "|joint1"
    endJoint = ""
    for n in range(1, numberOfJoints + 1):
        endJoint += "|joint%i" % (n)
    result = cmds.ikHandle(
        sol="ikSplineSolver",
        ns=numberOfCVs,
        pcv=True,
        sj=joint1,
        ee=endJoint,
        name=splineHandleName,
    )
    splineCurveName = getCurveName(result)
    cmds.setAttr("%s.visibility" % splineHandleName, 0)
    cmds.setAttr("%s.visibility" % splineCurveName, 0)
    cmds.rename(splineCurveName, ctrlCurve)

    # add skeleton to the joints layer
    if cmds.objExists(jointLayer) == False:
        cmds.createDisplayLayer(name=jointLayer, number=1, empty=True)
        cmds.setAttr("%s.color" % jointLayer, 18)
    cmds.editDisplayLayerMembers(jointLayer, joint1)

    # create a control curve to be used in Animate() function
    cmds.duplicate(ctrlCurve, rr=True, name=ctrlPositionsCurve)
    cmds.setAttr("%s.visibility" % ctrlPositionsCurve, 0)

    # add ikHandle and other control curves to joints layer
    cmds.editDisplayLayerMembers(jointLayer, ctrlCurve)
    cmds.editDisplayLayerMembers(jointLayer, splineHandleName)
    cmds.editDisplayLayerMembers(jointLayer, ctrlPositionsCurve)

    # create a group for this object
    cmds.group(em=True, name=objectName)
    cmds.group(em=True, name="%s_skeleton" % objectName)
    cmds.group(em=True, name="%s_doNotTouch" % objectName)
    cmds.parent("|joint1", "%s_skeleton" % objectName)
    cmds.parent(ctrlCurve, "%s_doNotTouch" % objectName)
    cmds.parent(splineHandleName, "%s_doNotTouch" % objectName)
    cmds.parent(ctrlPositionsCurve, "%s_doNotTouch" % objectName)
    cmds.parent(meshName, objectName)
    cmds.parent("%s_skeleton" % objectName, objectName)
    cmds.parent("%s_doNotTouch" % objectName, objectName)
    cmds.setAttr("%s_doNotTouch.visibility" % objectName, 0)

    # add attributes for keyframing
    cmds.addAttr(objectName, ln="waveLengths", at="double", dv=ds.waveLengths)
    cmds.addAttr(objectName, ln="waveAmplitude", at="double", dv=ds.waveAmplitude)
    cmds.addAttr(objectName, ln="waveRate", at="double", dv=ds.waveRate)
    cmds.addAttr(
        objectName,
        ln="pathUValue",
        niceName="path U Value",
        at="double",
        dv=ds.pathUValue,
    )
    cmds.setAttr("%s.waveLengths" % objectName, edit=True, keyable=True)
    cmds.setAttr("%s.waveAmplitude" % objectName, edit=True, keyable=True)
    cmds.setAttr("%s.waveRate" % objectName, edit=True, keyable=True)
    cmds.setAttr("%s.pathUValue" % objectName, edit=True, keyable=True)
    cmds.connectControl("waveLengths_grp", "%s.waveLengths" % objectName, index=2)
    cmds.connectControl("waveAmplitude_grp", "%s.waveAmplitude" % objectName, index=2)
    cmds.connectControl("waveRate_grp", "%s.waveRate" % objectName, index=2)
    cmds.connectControl("pathUValue_grp", "%s.pathUValue" % objectName, index=2)

    return True


# -----------------------------------------------------------------------------
# control helper functions
# -----------------------------------------------------------------------------
def calculateControlPositions(ctrl, ui):
    ctrlPos = []
    numberOfControls = ui.numberOfControls
    cv = ctrl + ".cv[0]"
    pos = cmds.xform(cv, worldSpace=True, query=True, translation=True)
    ctrlPosition0 = MVector(pos[0], pos[1], pos[2])
    ctrlPos.append(0.0)
    # calculate ctrl world position relative to first control
    for n in range(1, numberOfControls):
        if n == (numberOfControls - 1):
            cv = ctrl + ".cv[%i]" % (n + 2)  # skip the second last cv
        else:
            cv = ctrl + ".cv[%i]" % (n + 1)  # skip the second cv
        pos = cmds.xform(cv, worldSpace=True, query=True, translation=True)
        ctrlVector = MVector(pos[0], pos[1], pos[2]) - ctrlPosition0
        ctrlPos.append(ctrlVector.length())
    return ctrlPos


def createControlBox(width, height, depth, ctrlName):
    x = width / 2.0
    y = height / 2.0
    z = depth / 2.0
    curveName = cmds.curve(
        d=(1),
        p=[
            (x, y, z),
            (x, y, -z),
            (x, -y, -z),
            (x, -y, z),
            (x, y, z),
            (-x, y, z),
            (-x, -y, z),
            (x, -y, z),
            (x, -y, -z),
            (-x, -y, -z),
            (-x, y, -z),
            (x, y, -z),
            (x, y, z),
            (-x, y, z),
            (-x, y, -z),
            (-x, -y, -z),
            (-x, -y, z),
        ],
        k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    )
    cmds.rename(curveName, ctrlName)


def createRotateControl(size, offset, ctrlName):
    curveName = cmds.curve(
        degree=1,
        k=[
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
        ],
        p=[
            (0.0, 0.56, 0.83),
            (0.15, 0.56, 0.83),
            (0.1, 0.38, 0.92),
            (0.05, 0.20, 0.98),
            (0, 0.00, 1.00),
            (-0.05, 0.20, 0.98),
            (-0.1, 0.38, 0.92),
            (-0.15, 0.56, 0.83),
            (0.0, 0.56, 0.83),
            (0, 0.71, 0.71),
            (0, 0.83, 0.56),
            (0, 0.92, 0.38),
            (0, 0.98, 0.20),
            (0, 1.00, 0.00),
            (0, 0.98, -0.20),
            (0, 0.92, -0.38),
            (0, 0.83, -0.56),
            (0, 0.71, -0.71),
            (0.0, 0.56, -0.83),
            (-0.15, 0.56, -0.83),
            (-0.1, 0.38, -0.92),
            (-0.05, 0.20, -0.98),
            (0, 0, -1.0),
            (0.05, 0.20, -0.98),
            (0.1, 0.38, -0.92),
            (0.15, 0.56, -0.83),
            (0, 0.56, -0.83),
        ],
    )
    cmds.setAttr("%s.scaleX" % curveName, size)
    cmds.setAttr("%s.scaleY" % curveName, size)
    cmds.setAttr("%s.scaleZ" % curveName, size)
    cmds.move(
        -offset,
        "%s.scalePivot" % curveName,
        "%s.rotatePivot" % curveName,
        y=True,
        ws=True,
    )
    cmds.move(offset, curveName, y=True, ws=True)
    cmds.makeIdentity(curveName, apply=True, t=1, r=1, s=1, n=2)
    cmds.rename(curveName, ctrlName)


def createTranslateControl(size, width, yOffset, ctrlName):
    w = size / 2.0  # height of arrow head
    z = size / 5.0  # half width of base
    curveName = cmds.curve(
        d=(1),
        p=[
            (0, 0, 0),
            (0, w, w),
            (0, w, z),
            (0, size, z),
            (0, size, -z),
            (0, w, -z),
            (0, w, -w),
            (0, 0, 0),
        ],
        k=[0, 1, 2, 3, 4, 5, 6, 7],
    )
    cmds.rename(curveName, ctrlName)
    cmds.move(
        -yOffset,
        "%s.scalePivot" % ctrlName,
        "%s.rotatePivot" % ctrlName,
        y=True,
        ws=True,
    )
    cmds.move(yOffset, "|%s" % ctrlName, y=True, ws=True)
    cmds.setAttr("|%s.scaleZ" % ctrlName, width)
    cmds.makeIdentity("|%s" % ctrlName, apply=True, t=1, r=1, s=1, n=2)
    return ctrlName


def getCurveName(list):
    for n in range(0, len(list)):
        if "curve" in list[n]:
            return list[n]
    return False


# -----------------------------------------------------------------------------
# CREATE CONTROLS
# -----------------------------------------------------------------------------
def createControls(ui, cn):
    progressControlUpdate("... creating Controls ... ")
    objectName = ui.objectName
    numberOfJoints = ui.numberOfJoints
    numberOfControls = ui.numberOfControls
    numberOfHandles = ui.numberOfHandles
    spineHandleNames = cn.getSpineHandleNames()
    lastControlNumber = numberOfControls - 1
    jointLength = ui.jointLength
    splineHandleName = objectName + "_splineHandle"
    ctrlCurve = cn.ctrlCurve
    ctrlLayer = "snake_controls_L"
    ctrlBack = "ctrl_backTwist"
    ctrlGroup = objectName + "_controls"
    # ctrlBoxSize = ui.snakeLength/1000.0
    snakeInfo = SnakeInfo(ui.meshName)

    # if no control_L exists, create one
    if not cmds.objExists(ctrlLayer):
        cmds.createDisplayLayer(name=ctrlLayer, number=1, empty=True)
        cmds.setAttr("%s.color" % ctrlLayer, 17)

    # get the control positions
    # ctrlPos = []
    ctrlPos = calculateControlPositions(ctrlCurve, ui)

    # create controls
    for n in range(0, numberOfControls):
        cmds.select(clear=True)
        jointName = "|ctrlJN_%i" % (n)
        if cmds.objExists(jointName):
            print("Error: " + jointName + " already exists")
            for i in range(1, n):
                cmds.delete("|ctrlJN_%i" % (i))
            return
        cmds.joint(p=(-ctrlPos[n], 0, 0), name=jointName)
        cmds.setAttr("%s.visibility" % jointName, 0)

        ctrlName = "|ctrl_%i" % (n)
        if n == 0:
            ctrlBoxSize = snakeInfo.length / 1000.0
            createControlBox(ctrlBoxSize, ctrlBoxSize, ctrlBoxSize, "ctrl_0")
        else:
            ctrlOrig = "|ctrl_0"
            newName = cmds.duplicate(ctrlOrig, rr=True, name=ctrlName)
            cmds.rename(newName[0], "ctrl_%i" % n)

        tx = ctrlName + ".translateX"
        cmds.setAttr(tx, -ctrlPos[n])
        cmds.editDisplayLayerMembers(ctrlLayer, ctrlName)

    # create head control handle
    size = snakeInfo.length / 25.0
    width = 0.05 * size
    yOffset = 0.75 * snakeInfo.height
    headTrnCtrlName = createTranslateControl(size, width, yOffset, cn.headTrnCtrl)

    # create spine control handles
    width = 0.5 * width
    for n in range(0, numberOfHandles):
        hCtrlName = createTranslateControl(size, width, yOffset, spineHandleNames[n])
        cmds.move(-ctrlPos[n + 1], "|%s" % hCtrlName, x=True, ws=True)

    # create Twist control handles
    twistCtrlSize = 0.75 * size
    twistCtrlOffset = 2.0 * snakeInfo.height

    createRotateControl(twistCtrlSize, twistCtrlOffset, cn.frontTwistCtrl)
    createRotateControl(twistCtrlSize, twistCtrlOffset, cn.backTwistCtrl)
    cmds.move((-twistCtrlSize / 2.0), "|%s" % cn.frontTwistCtrl, x=True, ws=True)
    cmds.move(-ctrlPos[numberOfControls - 1], "|%s" % cn.backTwistCtrl, x=True, ws=True)

    # bind the controls to the ctrl curve
    cmds.select(clear=True)
    cmds.select("|ctrlJN_0", r=True)
    for n in range(1, numberOfControls):
        ctrl = "|ctrlJN_%i" % (n)
        cmds.select(ctrl, add=True)
    cmds.select(ctrlCurve, add=True)
    cmds.skinCluster(toSelectedBones=True, bm=0, nw=1, wd=0, mi=3, dr=4.0, rui=True)

    # organize controls
    cmds.parent("|%s_head" % objectName, "|%s" % headTrnCtrlName)
    cmds.parent("|ctrlJN_0", "|%s" % headTrnCtrlName)
    cmds.parent("|%s" % headTrnCtrlName, "|%s" % cn.frontTwistCtrl)
    cmds.parent("|%s" % cn.frontTwistCtrl, "|ctrl_0")
    cmds.parent("|%s" % cn.backTwistCtrl, "|ctrl_%i" % lastControlNumber)

    for n in range(1, numberOfControls):
        jointName = "|ctrlJN_%i" % (n)
        ctrlName = "|ctrl_%i" % (n)
        if n <= numberOfHandles:
            cmds.parent(jointName, "|%s" % spineHandleNames[n - 1])
            cmds.parent("|%s" % spineHandleNames[n - 1], ctrlName)
        else:
            cmds.parent(jointName, ctrlName)

    # group controls
    cmds.group("|ctrl_0", name=ctrlGroup)
    for n in range(1, numberOfControls):
        ctrl = "|ctrl_%i" % (n)
        cmds.parent(ctrl, ctrlGroup)
    cmds.parent(ctrlGroup, objectName)

    # set Twist controls
    firstControl = "%s|%s|ctrl_0|%s.xformMatrix" % (
        objectName,
        ctrlGroup,
        cn.frontTwistCtrl,
    )
    lastControl = "%s|%s|ctrl_%i|%s.xformMatrix" % (
        objectName,
        ctrlGroup,
        lastControlNumber,
        cn.backTwistCtrl,
    )
    dTwistControlEnable = "%s|%s_doNotTouch|%s_splineHandle.dTwistControlEnable" % (
        objectName,
        objectName,
        objectName,
    )
    dWorldUpType = "%s|%s_doNotTouch|%s_splineHandle.dWorldUpType" % (
        objectName,
        objectName,
        objectName,
    )
    dWorldUpMatrix = "%s|%s_doNotTouch|%s_splineHandle.dWorldUpMatrix" % (
        objectName,
        objectName,
        objectName,
    )
    dWorldUpMatrixEnd = "%s|%s_doNotTouch|%s_splineHandle.dWorldUpMatrixEnd" % (
        objectName,
        objectName,
        objectName,
    )
    cmds.setAttr(dTwistControlEnable, 1)
    cmds.setAttr(dWorldUpType, 4)
    cmds.connectAttr(firstControl, dWorldUpMatrix, f=True)
    cmds.connectAttr(lastControl, dWorldUpMatrixEnd, f=True)


# -----------------------------------------------------------------------------------------
#  SKINNING
# ----------------------------------------------------------------------------------------
def attachRig(args):
    ui = SnakeToolUI()
    cn = SnakeControlNames(ui)
    # check if skin is already attached to a rig
    if cmds.objExists(ui.objectName):
        try:
            joints = cmds.skinCluster(ui.meshName, query=True, wi=True)
            errorMessage("Rig is already attached!")
        except:
            attachSkin(ui, cn)
            weightSkin(ui, cn)
    else:
        errorMessage("Create a Rig First!")
        updateButtons()
        return
    updateButtons()
    progressControlUpdate("... finished attaching rig ... ")


# -------------------------------------------------------------
def unbindSkin(args):
    ui = SnakeToolUI()
    meshName = ui.meshName
    skinClusterName = "%s_skinCluster" % meshName
    if cmds.objExists(skinClusterName):
        cmds.skinCluster(skinClusterName, e=True, ub=True)
    progressControlUpdate("... finished detaching mesh ...")
    resetProgressControl()


# -------------------------------------------------------------
# attachSkin()
# -------------------------------------------------------------
def attachSkin(ui, cn):
    progressControlUpdate("... attaching mesh ... ")

    objectName = ui.objectName
    numberOfJoints = ui.numberOfJoints
    headJointName = cn.getHeadJointName()
    jointNames = cn.getJointNames()

    cmds.select(cl=True)
    cmds.select(jointNames[0:numberOfJoints], r=True)
    cmds.select(ui.meshName, add=True)
    clusterName = "%s_skinCluster" % objectName
    cmds.skinCluster(
        name=clusterName,
        bindMethod=0,
        normalizeWeights=1,
        weightDistribution=0,
        mi=3,
        omi=True,
        dr=4,
        rui=True,
    )
    cmds.select(cl=True)


# -------------------------------------------------------------
# weightSkin()
# -------------------------------------------------------------
def weightSkin(ui, cn):
    progressControlUpdate("... adjusting skin weights ... ")

    objectName = ui.objectName
    meshName = ui.meshName
    numberOfJoints = ui.numberOfJoints
    jointNames = cn.getJointNames()
    numberOfVertices = cmds.polyEvaluate(meshName, v=True)
    meshShape = cmds.listRelatives(meshName)
    skinClusterName = "%s_skinCluster" % objectName
    normWeights = "%s.normalizeWeights" % skinClusterName
    maxInfluences = "%s.maxInfluences" % skinClusterName
    cmds.setAttr(normWeights, 0)
    cmds.setAttr(maxInfluences, 3)

    resetProgressControl()
    setProgressControlMaxValue(100)

    # store joint positions
    jointPosition = []
    jointVector = []
    jointLength = []

    # store joint positions, vectors, and lengths
    for n in range(0, numberOfJoints):
        pos = cmds.xform(jointNames[n], worldSpace=True, query=True, translation=True)
        jointPosition.append(MVector(pos[0], pos[1], pos[2]))

        if n > 0:
            v = jointPosition[n] - jointPosition[n - 1]
            jointVector.append(MVector(v.x, v.y, v.z))
            jointLength.append(v.length())

    progressCurrentStep = 0
    progressIncrement = numberOfVertices / 100
    showProgress = progressIncrement

    for n in range(0, numberOfVertices):
        # progress bar
        if showProgress:
            step = n / progressIncrement
            if step > progressCurrentStep + 1:
                progressCurrentStep += 1
                progressControl()

        cv = "%s.vtx[%i]" % (meshName, n)

        # work out which joint the cv is closest too
        cvPos = cmds.xform(cv, worldSpace=True, query=True, translation=True)
        cvPosVec = MVector(cvPos[0], cvPos[1], cvPos[2])
        j = 0  # $j stores the vertices closest joint
        jPrev = -1
        jNext = -1
        jLast = numberOfJoints - 2
        jDot = 0.0

        for i in range(0, numberOfJoints - 1):
            # calc dot product of (joint vector . joint->cv vector)
            v1 = cvPosVec - jointPosition[i]
            v2 = jointVector[i]
            v2 = v2.normal()
            d = (v1 * v2) / jointLength[i]

            # if vertex is in front of first joint
            if i == 0 and d < 0.0:
                j = 0
                jNext = 1
                jDot = 0.0

            # if vertex is past last joint
            if i == jLast and d > 1.0:
                j = jLast
                jPrev = j - 1
                jDot = 1.0

            # if vertex is inside this joints area
            if d >= 0.0 and d <= 1.0:
                j = i
                if j > 0:
                    jPrev = j - 1
                jNext = j + 1
                jDot = d

                if j == jLast:
                    jNext = -1

        # calculate and apply skin weights
        wPos = jDot
        wNext = 0.0
        wPrev = 0.0

        # zero all weights except for nearest joint
        cmds.skinPercent(skinClusterName, cv, zri=True, tv=[(jointNames[j], 1.0)])

        if j < jLast:  # add weighting from next joint along
            wNext = 0.5 * (wPos * wPos)
            cmds.skinPercent(
                skinClusterName, cv, nrm=False, tv=[(jointNames[jNext], wNext)]
            )

        if j > 0:  # add weighting from previous joint
            wPrev = 0.5 * (1 - wPos) * (1 - wPos)
            cmds.skinPercent(
                skinClusterName, cv, nrm=False, tv=[(jointNames[jPrev], wPrev)]
            )

        w = 1 - wNext - wPrev
        cmds.skinPercent(skinClusterName, cv, nrm=False, tv=[(jointNames[j], w)])

    progressControl()


# -------------------------------------------------------------
# detachSnakeFromPath()
# -----------------------------------------------------------------------------
def detachSnakeFromPath(args):
    ui = SnakeToolUI()
    cn = SnakeControlNames(ui)
    objectName = ui.objectName
    numberOfControls = ui.numberOfControls
    ctrlNames = cn.getPathControlNames()
    mPaths = cn.getMotionPathNames()

    # delete expressions controlling motion path uValues and twist controls
    if cmds.objExists(cn.expName_uValues):
        cmds.delete(cn.expName_uValues)
    if cmds.objExists(cn.expName_twistControls):
        cmds.delete(cn.expName_twistControls)

    # delete motion path constraints
    cmds.cycleCheck(e=False)
    for mp in mPaths:
        if cmds.objExists(mp):
            # delete connected nodes
            result = cmds.listConnections(mp, s=False)
            if result:
                for n in result:
                    node_type = cmds.objectType(n)
                    if node_type == "addDoubleLinear":
                        cmds.delete(n)
            cmds.delete(mp)
    cmds.cycleCheck(e=True)

    # reset control positions
    ctrlPositionsCurve = cn.ctrlPositions
    # ctrlPos = []
    ctrlPos = calculateControlPositions(ctrlPositionsCurve, ui)
    for n in range(0, numberOfControls):
        cmds.setAttr("%s.translateX" % ctrlNames[n], -ctrlPos[n])
        cmds.setAttr("%s.translateY" % ctrlNames[n], 0.0)
        cmds.setAttr("%s.translateZ" % ctrlNames[n], 0.0)
        cmds.setAttr("%s.rotateX" % ctrlNames[n], 0.0)
        cmds.setAttr("%s.rotateY" % ctrlNames[n], 0.0)
        cmds.setAttr("%s.rotateZ" % ctrlNames[n], 0.0)

    updateUI(cn.objectName)


# -----------------------------------------------------------------------------
# ATTACH SNAKE TO PATH
# -----------------------------------------------------------------------------
def AttachSnakeToPath(args):
    ui = SnakeToolUI()
    selection = cmds.ls(sl=True)
    if not cmds.objExists(ui.pathName):
        if len(selection) == 0:
            errorMessage("Select a path for the snake to follow")
            return
        ui.set_pathName(selection[0])
    if not checkTypeIs(ui.pathName, "nurbsCurve"):
        errorMessage("Select a nurbs curve path for the snake path")
        return
    attachControlsToPath()


def attachControlsToPath():
    """
    - attach each control to motion path
    - create expression so that for each control:
        (ctrl's) motionPath.uValue =  ctrl_0.uValue + ctrlPosition
    """
    ui = SnakeToolUI()
    cn = SnakeControlNames(ui)
    objectName = ui.objectName
    numberOfJoints = ui.numberOfJoints
    numberOfControls = ui.numberOfControls
    jointLength = ui.jointLength
    path = ui.pathName
    start = ui.start
    end = ui.end
    speed = ui.speed
    pathLength = cmds.arclen(path)
    ctrl = cn.getPathControlNames()
    mPathNames = cn.getMotionPathNames()
    print("start: %0.2f   end: %0.2f" % (start, end))
    pathName = cn.pathName
    ui.set_pathName(pathName)

    if cmds.objExists(path):
        cmds.rename(path, pathName)
    else:
        errorMessage("path doesn't exist")
        return

    # ctrlPos = []
    ctrlPositionsCurve = cn.ctrlPositions
    ctrlPos = calculateControlPositions(ctrlPositionsCurve, ui)

    # attach each control to the path
    for n in range(0, numberOfControls):
        cmds.select(clear=True)
        motionPathName = cmds.pathAnimation(
            ctrl[n],
            curve=pathName,
            fractionMode=True,
            follow=True,
            followAxis="x",
            upAxis="y",
            worldUpType="vector",
            worldUpVector=[0, 1, 0],
            inverseUp=False,
            inverseFront=False,
            bank=False,
            startTimeU=start,
            endTimeU=end,
        )
        cmds.rename(motionPathName, mPathNames[n])

    # remove motionPath keyframes so expressions govern the ctrl's movement
    for n in range(1, numberOfControls):
        motionPath = "%s.uValue" % mPathNames[n]
        cmds.cutKey(motionPath, option="keys")

    # create linear tangents for the main path control
    cmds.keyTangent(mPathNames[0], time=(start, start), itt="linear", ott="linear")
    cmds.keyTangent(mPathNames[0], time=(end, end), itt="linear", ott="linear")

    # create the expressions for each control
    expName = objectName + "_exp_uValues"
    if cmds.objExists(expName):
        cmds.delete(expName)
    exp = "float $curveLength = %f;\n" % (pathLength)
    exp += "float $ctrlPosition[] = {%f" % ctrlPos[0]
    for n in range(1, numberOfControls):
        exp += ",%f" % (ctrlPos[n])
    exp += "};\n"
    for n in range(1, numberOfControls):
        exp += (
            "float $distAlongCurve%i = (%s.uValue * $curveLength) - $ctrlPosition[%i]; \n"
            % (n, mPathNames[0], n)
        )
    for n in range(1, numberOfControls):
        exp += "%s.uValue = $distAlongCurve%i/$curveLength;\n" % (mPathNames[n], n)
    cmds.expression(s=exp, name=expName)

    # calculate snakes starting position to snake is entirely on the path
    snakeSkeletonLength = ui.snakeLength
    uValueStart = snakeSkeletonLength / pathLength

    # add an attribute to the snake ctrl object to control movement along the path
    attrName = cn.pathUValue
    path_uValue = "%s.uValue" % mPathNames[0]
    cmds.cutKey(path_uValue, clear=True)
    cmds.setDrivenKeyframe(
        path_uValue, cd=attrName, itt="linear", ott="linear", dv=0.0, v=0.0
    )
    cmds.setDrivenKeyframe(
        path_uValue, cd=attrName, itt="linear", ott="linear", dv=1.0, v=1.0
    )
    cmds.setKeyframe(attrName, time=(start, start), value=uValueStart)
    cmds.setKeyframe(attrName, time=(end, end), value=1.0)
    cmds.keyTangent(attrName, time=(start, start), itt="linear", ott="linear")
    cmds.keyTangent(attrName, time=(end, end), itt="linear", ott="linear")

    updateButtons()
    progressControlUpdate("... finished attaching snake to path ...")


# -------------------------------------------------------------------------------------------
# ANIMATION
# -----------------------------------------------------------------------------
# deleteAnimations()
# -----------------------------------------------------------
def deleteAnimations(args):
    deleteAnimationKeyframes()


def deleteAnimationKeyframes():
    ui = SnakeToolUI()
    cn = SnakeControlNames(ui)
    objectName = ui.objectName
    numberOfControls = ui.numberOfControls
    ctrlNames = cn.getCurveControlNames()
    headCtrlName = cn.getHeadJointName()
    cmds.cutKey(headCtrlName)
    for n in range(0, numberOfControls):
        tz = "%s.translateZ" % ctrlNames[n]
        cmds.cutKey(ctrlNames[n])
        cmds.setAttr(tz, 0)
    progressControlUpdate("... finished deleting keyframes ... ")


# -----------------------------------------------------------
def updateMotionPathKeyframes(objectName, path_uValue, start, end):
    firstKeyframe = cmds.findKeyframe(path_uValue, which="first")
    lastKeyframe = cmds.findKeyframe(path_uValue, which="last")
    numberOfKeyframes = cmds.keyframe(path_uValue, query=True, kc=True)
    currentTimeRange = lastKeyframe - firstKeyframe
    newTimeRange = end - start
    conversion = newTimeRange / currentTimeRange

    if start == firstKeyframe and end == lastKeyframe:
        return

    uValue = []
    t = firstKeyframe
    for n in range(0, numberOfKeyframes):
        value = cmds.getAttr(path_uValue, t=(t))
        itt = cmds.keyTangent(path_uValue, query=True, t=(t, t), itt=True)
        ott = cmds.keyTangent(path_uValue, query=True, t=(t, t), ott=True)
        uValue.append(uValueKey(t * conversion, value, itt[0], ott[0]))
        t = cmds.findKeyframe(path_uValue, t=(t, t), which="next")

    cmds.cutKey(path_uValue)
    for n in range(0, numberOfKeyframes):
        cmds.setKeyframe(
            path_uValue, time=(uValue[n].t, uValue[n].t), value=uValue[n].value
        )
        cmds.keyTangent(
            path_uValue,
            time=(uValue[n].t, uValue[n].t),
            itt=uValue[n].itt,
            ott=uValue[n].ott,
        )


# ------------------------------------------------------------------
# addAnimationPrecision()
# ------------------------------------------------------------------
def addAnimationPrecision():
    ui = SnakeToolUI()
    cn = SnakeControlNames(ui)

    am = AnimationManager()

    # initialize progress bar
    resetProgressControl()
    setProgressControlMaxValue(ui.end - ui.start)
    progressControlUpdate("... adding keyframes ... ")

    # create keyframes for snakes starting position
    am.setInitialPosition(int(ui.start))
    am.initializePrecision()

    # create keyframes for selected time range
    for t in range(int(ui.start), int(ui.end)):
        progressControl()

        # get snake waveLength, waveAmplitude, waveRate etc
        am.moveAlongPath(t)

        # update all control positions and keyframe if required
        am.updatePrecision(t, "spline")

    progressControl()
    progressControlUpdate("... finished adding keyframes ... ")


def addKeyframes(args):
    addAnimationPrecision()


# ------------------------------------------------------------------
# animate_timeChanges()
# ------------------------------------------------------------------
def animateWithSpeedChanges(args):
    deleteAnimationKeyframes()
    ui = SnakeToolUI()
    cn = SnakeControlNames(ui)

    objectName = ui.objectName
    start = int(ui.start)
    end = int(ui.end)
    path = ui.pathName
    path_uValue = cn.pathUValue

    if not cmds.objExists(path):
        errorMessage("%s does not exist!" % path)
        return

    if not cmds.objExists(path_uValue):
        errorMessage("Attach to Motion Path before animating!")
        return

    # update path uValues for current start and end time in Animation Settings
    updateMotionPathKeyframes(objectName, path_uValue, start, end)

    am = AnimationManager()

    # initialize progress bar
    resetProgressControl()
    setProgressControlMaxValue(end - start)
    progressControlUpdate("... creating keyframes ... ")

    # create keyframes for snakes starting position
    am.setInitialPosition(int(start))

    # create keyframes for selected time range
    for t in range(int(start), int(end)):
        progressControl()

        # get snake waveLength, waveAmplitude, waveRate etc
        am.moveAlongPath(t)

        # update all control positions and keyframe if required
        am.update(t)

        # create keyframes for all controls if snake stops or starts moving
        if am.snakeHasStoppedMoving() or am.snakeHasStartedMoving():
            am.keyAllControlsAtTime(t, "flat")

    # key all controls on the last time frame
    am.keyAllControlsAtTime(int(end), "linear")

    progressControl()
    progressControlUpdate("... finished creating keyframes ... ")

    if ui.preActive:
        addAnimationPrecision()
