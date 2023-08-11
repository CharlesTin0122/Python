import pymel.core as pm


def OverlapperRelease():
    pm.optionVar(intValue=("animBlendingOpt", 1))
    if (pm.window("OverlapperPanel", ex=1)):
        pm.deleteUI("OverlapperPanel")

    pm.mel.CleanUpProc()
    window = str(
        pm.window(
            "OverlapperPanel",
            title="Overlapper 1.1",
            toolbox=1,
            s=1,
            menuBar=1,
            widthHeight=(172, 133),
        )
    )
    pm.menu("aboutMenu", l="Advanced", to=0)
    pm.menuItem(
        "debMode",
        l="Debug mode",
        cb=0,
        ann="Don't delete Overlapping offset controls. Expert mode. Be careful",
    )
    pm.menuItem(
        "onLayerMode",
        l="Bake on anim layer",
        cb=0,
        ann="Each new overlapping animation will be baked on new animation layer",
    )
    pm.menuItem(
        "adScaleMode",
        l="Adaptive scale",
        cb=1,
        ann="Overlap Scale parameter automaticly changes for distance between selected controls",
    )
    pm.menuItem(
        "ovCrSelSet",
        l="Create selection set",
        cb=1,
        ann="Create selection set of overlapped controls for last overlapper session",
    )
    pm.menuItem(
        l="CleanUp",
        ann="Delete all Oveplapper stuff",
        c=lambda *args: pm.mel.CleanUpProc(),
    )
    pm.menu("helpMenu", l="Help", to=0)
    pm.menuItem(l="Intro", c=lambda *args: pm.mel.hIntro())
    pm.menuItem(l="Tutorial", c=lambda *args: pm.mel.hTutorial())
    pm.columnLayout()
    pm.rowColumnLayout(nc=2)
    pm.text(
        label="     Softness    ",
        align="center",
        ann="More animation velocity, less softness",
    )
    pm.floatField("timeShift", v=3, w=10, precision=2)
    pm.text(
        label="     Scale    ", align="center", ann="More Scale, more overlap apmlitude"
    )
    pm.floatField("globalScale", v=1.0, w=10, precision=2)
    pm.rowColumnLayout(nc=1)
    pm.rowColumnLayout(nc=1)
    pm.checkBox(
        "WindCheckBox",
        ann="Add wind animation on overlapped controls",
        label=" Wind",
        v=0,
        h=18,
    )
    pm.setParent("..")
    pm.setParent("..")
    pm.rowColumnLayout(nc=2)
    pm.text(label=" Scale", align="center", ann="More Scale, more wind apmlitude")
    pm.floatField("windScale", v=1, w=48, bgc=(0.45, 0.52, 0.57), precision=2)
    pm.text(label=" Speed ", align="center", ann="More Speed, more wind frequence")
    pm.floatField("windSpeed", v=1, w=20, precision=2, bgc=(0.45, 0.52, 0.57))
    pm.setParent("..")
    pm.setParent("..")
    pm.setParent("..")
    pm.rowColumnLayout(nc=1)
    theLayout = str(
        pm.frameLayout(
            cc=lambda *args: pm.mel.OverlapperPanelBig(),
            ec=lambda *args: pm.mel.OverlapperPanelSmall(),
            collapsable=1,
            collapse=1,
            l="Options",
        )
    )
    pm.checkBox(
        "firstCtrl",
        l="Don't use first controls",
        v=0,
        ann="Don't use first controls in selected sequence of controls",
    )
    pm.checkBox(
        "IKmode",
        l="Add translate",
        v=0,
        ann="Add translate overlap for selected controls",
    )
    pm.checkBox(
        "HierarchyCheckBox",
        l="Hierarchy",
        v=0,
        ann="Add all controls below the hierarchy. Works with Advanced Skeleton rigs",
    )
    pm.checkBox(
        "CycleCheckBox",
        l="Cycle",
        v=0,
        ann="Create seamless overlapping action for cycle animation. The first and the last keys on timeline must be the same",
    )
    pm.setParent("..")
    pm.button(
        w=160,
        label="Overlap",
        bgc=(0.85, 0.85, 0.85),
        command=lambda *args: pm.mel.OverlapperStarter(),
    )
    pm.showWindow(window)
    pm.window("OverlapperPanel", edit=1, widthHeight=(163, 163))


def OverlapperPanelBig():
    pm.window("OverlapperPanel", edit=1, widthHeight=(163, 163))


def OverlapperPanelSmall():
    pm.window("OverlapperPanel", edit=1, widthHeight=(163, 236))


def _hIntro():
    pm.launch(web="https://vimeo.com/286860063")


def _hTutorial():
    pm.launch(web="https://vimeo.com/287771379")


def CleanUpProc():
    if pm.objExists("*_OverlapJoint*"):
        pm.delete("*_OverlapJoint*")

    if pm.objExists("*:*_OverlapJoint*"):
        pm.delete("*:*_OverlapJoint*")

    if pm.objExists("*:*:*_OverlapJoint*"):
        pm.delete("*:*:*_OverlapJoint*")

    if pm.objExists("*overlapOffsetLocator*"):
        pm.delete("*overlapOffsetLocator*")

    if pm.objExists("overlapResultLocatorOut*"):
        pm.delete("overlapResultLocatorOut*")

    if pm.objExists("TEMP_Offset_locator*"):
        pm.delete("TEMP_Offset_locator*")

    if pm.objExists("*overlapOffsetIKLocator*"):
        pm.delete("*overlapOffsetIKLocator*")

    if pm.objExists("OverlapperSet"):
        pm.delete("OverlapperSet")

    if pm.objExists("OverlapperWorkSet"):
        pm.delete("OverlapperWorkSet")

    pm.progressWindow(endProgress=1)


def OverlapperStarter():
    if pm.objExists("OverlapperWorkSet"):
        pm.delete("OverlapperWorkSet")

    pm.melGlobals.initVar("string", "gPlayBackSlider")
    # time range
    pm.melGlobals.initVar("float", "timeStart")
    pm.melGlobals.initVar("float", "timeEnd")
    pm.melGlobals.initVar("float", "timeStartGlobal")
    pm.melGlobals.initVar("float", "timeEndGlobal")
    RangeStart = 0.0
    Range = []
    Range = pm.timeControl(pm.melGlobals["gPlayBackSlider"], q=1, ra=1)
    RangeStart = Range[1] - Range[0]
    if RangeStart == 1:
        pm.melGlobals["timeStartGlobal"] = float(pm.playbackOptions(q=1, min=1))
        pm.melGlobals["timeEndGlobal"] = float(pm.playbackOptions(q=1, max=1))

    else:
        pm.melGlobals["timeStartGlobal"] = Range[0]
        pm.melGlobals["timeEndGlobal"] = Range[1]

    ctrlsAmount = pm.ls(sl=1)
    # MANY CONTROLS
    if len(ctrlsAmount) > 1:
        if pm.checkBox("HierarchyCheckBox", q=1, v=1) == 1:
            # some ctrls with hierarchy DONE!!!!!!
            for SelCtrl in ctrlsAmount:
                pm.select(SelCtrl, r=1)
                pm.progressWindow(endProgress=1)
                pm.mel.OverlapperWithHierarchy()
                pm.mel.CycleFinal()

        # some ctrls without hierarchy DONE!!!!!!
        else:
            pm.mel.Overlapper()
            pm.mel.CycleFinal()

    # ONE CONTROLS
    elif pm.checkBox("HierarchyCheckBox", q=1, v=1) == 1:
        pm.progressWindow(endProgress=1)
        # with hierarchy DONE!!!!!!
        pm.mel.OverlapperWithHierarchy()
        pm.mel.CycleFinal()

    # without hierarchy
    else:
        pm.confirmDialog(
            b="Ok",
            t="Oooops..",
            m="For correct work you should select more than one control \n            or switch on Hierarchy mode in Options \n\nIf you want overlap one control: \n    1. select two neighboring controls \n    2. check  `Don't use first control`  in Options ",
        )


def _OverlapperWithHierarchy():
    """//////////////// Hierarchy work //////////////////////"""

    ArraySecondGuys = []
    parentArray = []
    nodesArray = []
    Chain = []
    lastElement = ""
    allSceneNurbes = []
    currentShapeType = ""
    CtrlByHierarchy = []
    TypeOfObject = ""
    ClearElemwnts = 0
    ClearElemwnts = len(allSceneNurbes)
    for s in range(0, ClearElemwnts):
        allSceneNurbes.pop(0)

    currentCtrls = pm.ls(sl=1)
    # find type of selection
    pm.select(currentCtrls[0], r=1)
    pm.pickWalk(d="down")
    currentShape = pm.ls(sl=1)
    currentShapeType = str(pm.objectType(currentShape[0]))
    pm.select(currentCtrls, r=1)
    pm.select(hi=1)
    currentCtrls = pm.ls(sl=1)
    if (
        pm.objExists("*Root_M")
        or pm.objExists("*:Root_M")
        or pm.objExists("*DeformationSystem")
        or pm.objExists("*:DeformationSystem")
        or pm.objExists("*MotionSystem")
        or pm.objExists("*:MotionSystem")
        or pm.objExists("*FitSkeleton")
        or pm.objExists("*:FitSkeleton")
    ):
        currentShapeType = "nurbsCurve"

    allSceneNurbes = pm.mel.listTransforms("-type " + currentShapeType)
    Stuff = [x for x in currentCtrls if x not in allSceneNurbes]
    CtrlByHierarchy = [x for x in currentCtrls if x not in Stuff]
    pm.select(CtrlByHierarchy, r=1)
    amountOfAllCtrls = len(CtrlByHierarchy)
    LastCtrlInHierarchy = CtrlByHierarchy[(len(CtrlByHierarchy)) - 1]
    ClearElemwnts = len(Chain)
    for s in range(0, ClearElemwnts):
        Chain.pop(0)

    for i in range(0, amountOfAllCtrls):
        pm.select(CtrlByHierarchy[i], r=1)
        pm.select(hi=1)
        currentCtrls = pm.ls(sl=1)
        Stuff = [x for x in currentCtrls if x not in allSceneNurbes]
        CurrentCtrlByHierarchy = [x for x in currentCtrls if x not in Stuff]
        if (
            CtrlByHierarchy[i + 1] == CurrentCtrlByHierarchy[1]
            and CurrentCtrlByHierarchy[0] != LastCtrlInHierarchy
        ):
            Chain.insert(100, CurrentCtrlByHierarchy[0])
            pm.select(CurrentCtrlByHierarchy[0], r=1)

        else:
            Chain.insert(100, CurrentCtrlByHierarchy[0])
            pm.select(Chain, r=1)
            pm.mel.Overlapper()
            CtrlByHierarchy = [x for x in CtrlByHierarchy if x not in Chain]
            ClearElemwnts = len(Chain)
            for s in range(0, ClearElemwnts):
                Chain.pop(0)

        amountOfAllCtrls = len(CtrlByHierarchy)


def _Overlapper():
    """/////////// Overlapper /////////////"""

    pm.cycleCheck(e=False)
    pm.melGlobals.initVar("float", "timeStartGlobal")
    pm.melGlobals.initVar("float", "timeEndGlobal")
    pm.melGlobals.initVar("float", "timeStart")
    pm.melGlobals.initVar("float", "timeEnd")
    pm.melGlobals["timeStart"] = pm.melGlobals["timeStartGlobal"]
    pm.melGlobals["timeEnd"] = pm.melGlobals["timeEndGlobal"]
    ClearElemwnts = 0
    OverTimeShift = float(pm.floatField("timeShift", q=1, v=1))
    OverGlobalScale = float(pm.floatField("globalScale", q=1, v=1))
    if OverGlobalScale <= 0:
        OverGlobalScale = 0.001

    windScaleValue = float(pm.floatField("windScale", q=1, v=1))
    windSpeedValue = float(pm.floatField("windSpeed", q=1, v=1))
    deBugMode = int(pm.menuItem("debMode", query=1, cb=1))
    onLayerSwitch = int(pm.menuItem("onLayerMode", query=1, cb=1))
    adptScale = int(pm.menuItem("adScaleMode", query=1, cb=1))
    OvSelectionSet = int(pm.menuItem("ovCrSelSet", query=1, cb=1))
    TRANSLATEmode = int(pm.checkBox("IKmode", q=1, v=1))
    useFirstCtrl = int(pm.checkBox("firstCtrl", q=1, v=1))
    WindSwitch = int(pm.checkBox("WindCheckBox", q=1, v=1))
    CycleCheckBox = int(pm.checkBox("CycleCheckBox", q=1, v=1))
    timeShift = OverTimeShift
    overlapIntensity = OverGlobalScale
    scaleModulator = float(5)
    overlapJointsArray = []
    overlapJointsLenghtArray = []
    averageLenghtJoints = 0.0
    pm.melGlobals.initVar("float", "sumLenghtJoints")
    ControlName = []
    cycleLenghts = 0.0
    SelectedControlsClearNameSpaces = []
    SelectedControls = []
    pm.melGlobals.initVar("string[]", "eulerFilterCurves")
    ClearElemwnts = len(overlapJointsArray)
    for i in range(0, ClearElemwnts):
        overlapJointsArray.pop(0)

    ClearElemwnts = len(overlapJointsLenghtArray)
    for i in range(0, ClearElemwnts):
        pm.mel.floatArrayRemoveAtIndex(0, overlapJointsLenghtArray)

    ClearElemwnts = len(SelectedControls)
    for i in range(0, ClearElemwnts):
        SelectedControls.pop(0)

    ClearElemwnts = len(SelectedControlsClearNameSpaces)
    for i in range(0, ClearElemwnts):
        SelectedControlsClearNameSpaces.pop(0)

    currentTime = float(pm.currentTime(query=1))
    # time range
    # set frame
    pm.currentTime(pm.melGlobals["timeStart"], e=1)
    SelectedControls = pm.ls(sl=1)
    iLoop = len(SelectedControls)
    DividedName = ControlName = SelectedControls[0].split(":")
    if DividedName > 1:
        for i in range(0, iLoop):
            DividedNameCurve = ControlName = SelectedControls[i].split(":")
            ClearNameCtrl = ControlName[(DividedNameCurve - 1)]
            SelectedControlsClearNameSpaces.insert(100, ClearNameCtrl)

    else:
        SelectedControlsClearNameSpaces = SelectedControls

    pm.select(cl=1)
    # progressBar
    amount = 0
    prAmount = float(100 / iLoop)
    pm.progressWindow(
        title="progress...",
        progress=amount,
        status="Progress: 0%",
        isInterruptable=True,
    )
    # create locators for Joints
    for i in range(0, iLoop):
        pm.spaceLocator(n=("TEMP_Offset_locator" + str(i)))
        pm.select(SelectedControls[i], ("TEMP_Offset_locator" + str(i)), r=1)
        pm.parentConstraint(weight=1)

    pm.select(cl=1)
    # create Joints
    for i in range(0, iLoop):
        WorldTr = pm.xform(("TEMP_Offset_locator" + str(i)), q=1, ws=1, t=1)
        pm.joint(
            rad=1,
            n=(SelectedControls[i] + "_OverlapJoint"),
            p=(WorldTr[0], WorldTr[1], WorldTr[2]),
        )
        if i > 0:
            pm.joint(
                (SelectedControls[i - 1] + "_OverlapJoint"),
                e=1,
                zso=1,
                oj="xyz",
                sao="yup",
            )

        overlapJointsArray.insert(100, (SelectedControls[i] + "_OverlapJoint"))

    pm.delete("TEMP_Offset_locator*")
    overlapJointsAnmount = len(SelectedControls)
    pm.select((overlapJointsArray[overlapJointsAnmount - 1]), r=1)
    pm.duplicate(rr=1)
    LastOrientJoints = pm.ls(sl=1)
    pm.pm.cmds.move(2, 0, 0, r=1, ls=1, wd=1)
    WorldLastTr = pm.xform(LastOrientJoints[0], q=1, ws=1, t=1)
    pm.select((SelectedControls[i - 1] + "_OverlapJoint"), r=1)
    pm.joint(
        rad=1,
        n=(SelectedControls[i - 1] + "LastOrientJoint"),
        p=(WorldLastTr[0], WorldLastTr[1], WorldLastTr[2]),
    )
    pm.joint(
        (SelectedControls[i - 1] + "_OverlapJoint"), e=1, zso=1, oj="xyz", sao="yup"
    )
    pm.delete(LastOrientJoints)
    LastOrientJoints = pm.ls(sl=1)
    overlapJointsArray.insert(100, LastOrientJoints[0])
    pm.select(overlapJointsArray, r=1)
    pm.joint(e=1, oj="xyz", secondaryAxisOrient="zup", ch=1, zso=1)
    ClearElemwnts = len(overlapJointsLenghtArray)
    for s in range(0, ClearElemwnts):
        pm.mel.floatArrayRemoveAtIndex(0, overlapJointsLenghtArray)

    # joints lengths
    for i in range(1, (iLoop + 1)):
        DistanceBetween = float(pm.getAttr(overlapJointsArray[i] + ".translateX"))
        pm.mel.floatArrayInsertAtIndex(100, overlapJointsLenghtArray, DistanceBetween)

    JointsLentghtsAmount = len(overlapJointsLenghtArray)
    # average
    pm.melGlobals["sumLenghtJoints"] = float(0)
    for i in range(0, (JointsLentghtsAmount)):
        pm.melGlobals["sumLenghtJoints"] = (
            pm.melGlobals["sumLenghtJoints"] + overlapJointsLenghtArray[i]
        )

    averageLenghtJoints = (pm.melGlobals["sumLenghtJoints"] - 2) / JointsLentghtsAmount
    pm.setAttr(
        (SelectedControls[i - 1] + "LastOrientJoint.translateX"), averageLenghtJoints
    )
    # constrain joint to controls
    for i in range(0, iLoop):
        pm.select(SelectedControls[i], (SelectedControls[i] + "_OverlapJoint"), r=1)
        pm.pointConstraint(weight=1, mo=1)
        pm.orientConstraint(weight=1, mo=1)

    pm.select(overlapJointsArray, r=1)
    # bake jonts
    pm.bakeResults(
        overlapJointsArray,
        simulation=0,
        t=(str(pm.melGlobals["timeStart"]) + ":" + str(pm.melGlobals["timeEnd"])),
        sampleBy=1,
        disableImplicitControl=1,
        preserveOutsideKeys=1,
        sparseAnimCurveBake=1,
        bakeOnOverrideLayer=0,
        minimizeRotation=0,
    )
    pm.delete(constraints=1)
    # Cycling (copy curves, add time)
    if CycleCheckBox == 1:
        for i in range(0, (iLoop - 1)):
            pm.selectKey(
                (SelectedControlsClearNameSpaces[i] + "_OverlapJoint_translateX"),
                (SelectedControlsClearNameSpaces[i] + "_OverlapJoint_translateY"),
                (SelectedControlsClearNameSpaces[i] + "_OverlapJoint_translateZ"),
                (SelectedControlsClearNameSpaces[i] + "_OverlapJoint_rotateX"),
                (SelectedControlsClearNameSpaces[i] + "_OverlapJoint_rotateY"),
                (SelectedControlsClearNameSpaces[i] + "_OverlapJoint_rotateZ"),
                r=1,
                k=1,
                t=(
                    str(pm.melGlobals["timeStart"])
                    + ":"
                    + str(pm.melGlobals["timeEnd"])
                ),
            )
            pm.copyKey()
            pm.pasteKey(
                time=pm.melGlobals["timeEnd"],
                float=pm.melGlobals["timeEnd"],
                option="insert",
                copies=2,
                connect=0,
                timeOffset=0,
                floatOffset=0,
                valueOffset=0,
            )
            pm.select(cl=1)

        cycleLenghts = pm.melGlobals["timeEnd"] - pm.melGlobals["timeStart"]
        pm.melGlobals["timeEnd"] = pm.melGlobals["timeEnd"] + 2 * cycleLenghts

    # Overlaping
    for i in range(0, iLoop):
        amount += int(prAmount)
        # progressBar
        pm.progressWindow(
            edit=1, progress=amount, status=("Progress: " + str(amount) + "%")
        )
        # create locator
        pm.spaceLocator(n=("overlapOffsetLocator" + str(i)))
        pm.select(overlapJointsArray[i], ("overlapOffsetLocator" + str(i)), r=1)
        temps = pm.pointConstraint(offset=(0, 0, 0), weight=1)
        pm.delete(temps)
        temps = pm.orientConstraint(offset=(0, 0, 0), weight=1)
        pm.delete(temps)
        # create IK locator
        pm.spaceLocator(n=("overlapOffsetIKLocator" + str(i)))
        pm.select(overlapJointsArray[i], ("overlapOffsetIKLocator" + str(i)), r=1)
        temps = pm.pointConstraint(offset=(0, 0, 0), weight=1)
        pm.delete(temps)
        temps = pm.orientConstraint(offset=(0, 0, 0), weight=1)
        pm.delete(temps)
        pm.select(("overlapOffsetLocator" + str(i)), r=1)
        if adptScale == 1:
            scaleModulator = averageLenghtJoints

        overlapIntensityMult = averageLenghtJoints / overlapIntensity * 5
        pm.pm.cmds.move(overlapIntensityMult, 0, 0, r=1, os=1, ls=1)
        pm.select(overlapJointsArray[i], ("overlapOffsetLocator" + str(i)), r=1)
        pm.parentConstraint(mo=1, weight=1)
        pm.select(overlapJointsArray[i], ("overlapOffsetIKLocator" + str(i)), r=1)
        pm.parentConstraint(mo=1, weight=1)
        pm.bakeResults(
            ("overlapOffsetLocator" + str(i)),
            ("overlapOffsetIKLocator" + str(i)),
            simulation=0,
            t=(str(pm.melGlobals["timeStart"]) + ":" + str(pm.melGlobals["timeEnd"])),
            sampleBy=1,
            disableImplicitControl=1,
            preserveOutsideKeys=1,
            sparseAnimCurveBake=0,
            removeBakedAttributeFromLayer=0,
            removeBakedAnimFromLayer=0,
            bakeOnOverrideLayer=0,
            minimizeRotation=0,
            controlPoints=0,
            shape=1,
        )
        pm.filterCurve(
            ("overlapOffsetLocator" + str(i) + "_rotateX"),
            ("overlapOffsetLocator" + str(i) + "_rotateY"),
            ("overlapOffsetLocator" + str(i) + "_rotateZ"),
        )
        pm.spaceLocator(n=("overlapOffsetLocatorWind" + str(i)))
        pm.parent(
            ("overlapOffsetLocatorWind" + str(i)), ("overlapOffsetLocator" + str(i))
        )
        pm.makeIdentity(apply=False, t=1, r=1, s=1)
        timeShiftNeg = float(-1 * timeShift)
        timeShiftCurrent = timeShift + 1
        pm.keyframe(
            ("overlapOffsetLocator" + str(i) + "_translateX"),
            e=1,
            iub=True,
            r=1,
            o="over",
            tc=timeShift,
        )
        pm.keyframe(
            ("overlapOffsetLocator" + str(i) + "_translateY"),
            e=1,
            iub=True,
            r=1,
            o="over",
            tc=timeShift,
        )
        pm.keyframe(
            ("overlapOffsetLocator" + str(i) + "_translateZ"),
            e=1,
            iub=True,
            r=1,
            o="over",
            tc=timeShift,
        )
        pm.keyframe(
            ("overlapOffsetIKLocator" + str(i) + "_translateX"),
            e=1,
            iub=True,
            r=1,
            o="over",
            tc=timeShift,
        )
        pm.keyframe(
            ("overlapOffsetIKLocator" + str(i) + "_translateY"),
            e=1,
            iub=True,
            r=1,
            o="over",
            tc=timeShift,
        )
        pm.keyframe(
            ("overlapOffsetIKLocator" + str(i) + "_translateZ"),
            e=1,
            iub=True,
            r=1,
            o="over",
            tc=timeShift,
        )
        pm.keyframe(
            ("overlapOffsetLocator" + str(i) + "_rotateX"),
            e=1,
            iub=True,
            r=1,
            o="over",
            tc=timeShift,
        )
        pm.keyframe(
            ("overlapOffsetLocator" + str(i) + "_rotateY"),
            e=1,
            iub=True,
            r=1,
            o="over",
            tc=timeShift,
        )
        pm.keyframe(
            ("overlapOffsetLocator" + str(i) + "_rotateZ"),
            e=1,
            iub=True,
            r=1,
            o="over",
            tc=timeShift,
        )
        pm.selectKey(
            ("overlapOffsetLocator" + str(i) + "_translateX"),
            add=1,
            k=1,
            t=timeShiftCurrent,
        )
        pm.selectKey(
            ("overlapOffsetLocator" + str(i) + "_translateY"),
            add=1,
            k=1,
            t=timeShiftCurrent,
        )
        pm.selectKey(
            ("overlapOffsetLocator" + str(i) + "_translateZ"),
            add=1,
            k=1,
            t=timeShiftCurrent,
        )
        pm.selectKey(
            ("overlapOffsetIKLocator" + str(i) + "_translateX"),
            add=1,
            k=1,
            t=timeShiftCurrent,
        )
        pm.selectKey(
            ("overlapOffsetIKLocator" + str(i) + "_translateY"),
            add=1,
            k=1,
            t=timeShiftCurrent,
        )
        pm.selectKey(
            ("overlapOffsetIKLocator" + str(i) + "_translateZ"),
            add=1,
            k=1,
            t=timeShiftCurrent,
        )
        pm.selectKey(
            ("overlapOffsetLocator" + str(i) + "_rotateX"),
            add=1,
            k=1,
            t=timeShiftCurrent,
        )
        pm.selectKey(
            ("overlapOffsetLocator" + str(i) + "_rotateY"),
            add=1,
            k=1,
            t=timeShiftCurrent,
        )
        pm.selectKey(
            ("overlapOffsetLocator" + str(i) + "_rotateZ"),
            add=1,
            k=1,
            t=timeShiftCurrent,
        )
        pm.keyframe(
            animation="keys", option="over", relative=1, timeChange=timeShiftNeg
        )
        pm.spaceLocator(n=("overlapInLocator_first_" + str(i)))
        pm.spaceLocator(n=("overlapInLocator_second_" + str(i)))
        pm.spaceLocator(n=("overlapResultLocator_" + str(i)))
        pm.select(
            ("overlapInLocator_first_" + str(i)),
            (SelectedControls[i] + "_OverlapJoint"),
            r=1,
        )
        pm.Parent()
        pm.select(
            ("overlapInLocator_second_" + str(i)),
            (SelectedControls[i] + "_OverlapJoint"),
            r=1,
        )
        pm.Parent()
        pm.select(
            ("overlapResultLocator_" + str(i)),
            (SelectedControls[i] + "_OverlapJoint"),
            r=1,
        )
        pm.Parent()
        pm.select(
            ("overlapInLocator_first_" + str(i)),
            ("overlapInLocator_second_" + str(i)),
            ("overlapResultLocator_" + str(i)),
            r=1,
        )
        pm.makeIdentity(apply=False, t=1, r=1, s=1)
        pm.select(("overlapInLocator_second_" + str(i)), r=1)
        pm.pm.cmds.move(overlapIntensityMult, 0, 0, r=1, os=1, ls=1)
        pm.select(("overlapInLocator_first_" + str(i)), r=1)
        pm.group(n=("overlapInLocator_first_" + str(i) + "grp"))
        # IK mode
        if TRANSLATEmode == 1:
            pm.select(
                ("overlapOffsetIKLocator" + str(i)),
                ("overlapInLocator_first_" + str(i) + "grp"),
                r=1,
            )
            pm.pointConstraint(mo=1, weight=1)

        pm.select(
            ("overlapOffsetLocatorWind" + str(i)),
            ("overlapInLocator_second_" + str(i)),
            r=1,
        )
        pm.parentConstraint(mo=1, weight=1)
        pm.select(
            ("overlapInLocator_second_" + str(i)),
            ("overlapInLocator_first_" + str(i) + "grp"),
            r=1,
        )
        pm.aimConstraint(
            mo=1,
            weight=1,
            aimVector=(1, 0, 0),
            upVector=(0, 1, 0),
            worldUpType="object",
            worldUpObject=("overlapInLocator_second_" + str(i)),
        )
        pm.select(
            ("overlapInLocator_second_" + str(i)),
            ("overlapInLocator_first_" + str(i)),
            r=1,
        )
        pm.orientConstraint(mo=1, skip=["y", "z"], weight=1)
        pm.select(
            ("overlapInLocator_first_" + str(i)),
            ("overlapResultLocator_" + str(i)),
            r=1,
        )
        pm.parentConstraint(mo=1, weight=1)
        # /Wind
        if i < 1 and WindSwitch == 1:
            pm.select("overlapOffsetLocatorWind0", r=1)
            WindFirstControl = pm.ls(sl=1)
            windMultiply = 0.07 * overlapIntensityMult * windScaleValue
            speedMultiply = float(20 / windSpeedValue)
            pm.setKeyframe(
                "overlapOffsetLocatorWind0",
                attribute=["translateY", "translateZ"],
                t=pm.melGlobals["timeStart"],
            )
            pm.bakeResults(
                "overlapOffsetLocatorWind0",
                simulation=0,
                t=(
                    str(pm.melGlobals["timeStart"])
                    + ":"
                    + str((pm.melGlobals["timeEnd"] + speedMultiply))
                ),
                sampleBy=speedMultiply,
                oversamplingRate=1,
                disableImplicitControl=True,
                preserveOutsideKeys=1,
                sparseAnimCurveBake=False,
                removeBakedAttributeFromLayer=False,
                removeBakedAnimFromLayer=False,
                bakeOnOverrideLayer=False,
                minimizeRotation=True,
                at=["ty", "tz"],
            )
            listAnimAttrs = pm.listAttr("overlapOffsetLocatorWind0", k=1)
            for attr in listAnimAttrs:
                animCurve = pm.listConnections(
                    ("overlapOffsetLocatorWind0." + str(attr)), type="animCurve"
                )
                # array of animated atributes
                for animCurveCurrent in animCurve:
                    animCurveCurrentKeysTimeArray = pm.keyframe(
                        animCurveCurrent,
                        time=(
                            str(pm.melGlobals["timeStart"])
                            + ":"
                            + str(pm.melGlobals["timeEnd"])
                        ),
                        query=1,
                        timeChange=1,
                    )
                    # array of keys
                    # array of values
                    for animCurveCurrentKeysTime in animCurveCurrentKeysTimeArray:
                        animCurveCurrentKeysTimeArray = pm.keyframe(
                            animCurveCurrent,
                            time=animCurveCurrentKeysTime,
                            query=1,
                            valueChange=1,
                        )
                        # Randomazer
                        RandomizerValue = float(pm.mel.rand(-1, 1))
                        animCurveCurrentKeysValueArrayAddRandom = (
                            animCurveCurrentKeysTimeArray[0]
                            + windMultiply * RandomizerValue
                        )
                        pm.keyframe(
                            animCurveCurrent,
                            e=1,
                            iub=True,
                            r=1,
                            o="over",
                            vc=animCurveCurrentKeysValueArrayAddRandom,
                            t=animCurveCurrentKeysTime,
                        )

            pm.keyframe(
                "overlapOffsetLocatorWind0_translateY",
                e=1,
                iub=True,
                r=1,
                o="over",
                tc=(speedMultiply / 2),
            )
            pm.selectKey(
                "overlapOffsetLocatorWind0_translateY",
                add=1,
                k=1,
                t=((speedMultiply / 2) + 1),
            )
            pm.keyframe(
                animation="keys",
                option="over",
                relative=1,
                timeChange=(speedMultiply / -2),
            )

        pm.bakeResults(
            ("overlapResultLocator_" + str(i)),
            simulation=0,
            t=(str(pm.melGlobals["timeStart"]) + ":" + str(pm.melGlobals["timeEnd"])),
            sampleBy=1,
            disableImplicitControl=1,
            preserveOutsideKeys=1,
            sparseAnimCurveBake=0,
            removeBakedAttributeFromLayer=0,
            removeBakedAnimFromLayer=0,
            bakeOnOverrideLayer=0,
            minimizeRotation=0,
            controlPoints=0,
            shape=1,
        )
        if deBugMode == 0:
            pm.delete(
                ("overlapInLocator_first_" + str(i)),
                ("overlapInLocator_first_" + str(i) + "grp"),
                ("overlapOffsetLocator" + str(i)),
                ("overlapInLocator_second_" + str(i)),
            )

        pm.spaceLocator(n=("overlapResultLocatorOut_" + str(i)))
        if pm.objExists("OverlapperOverlapResultLocatorSet"):
            pm.pm.cmds.sets(
                ("overlapResultLocatorOut_" + str(i)),
                edit=1,
                forceElement="OverlapperOverlapResultLocatorSet",
            )

        else:
            createSetResult = pm.pm.cmds.sets(name="OverlapperOverlapResultLocatorSet")

        pm.select(
            ("overlapResultLocator_" + str(i)),
            ("overlapResultLocatorOut_" + str(i)),
            r=1,
        )
        pm.parentConstraint(weight=1)
        pm.bakeResults(
            ("overlapResultLocatorOut_" + str(i)),
            simulation=0,
            t=(str(pm.melGlobals["timeStart"]) + ":" + str(pm.melGlobals["timeEnd"])),
            sampleBy=1,
            disableImplicitControl=1,
            preserveOutsideKeys=1,
            sparseAnimCurveBake=0,
            removeBakedAttributeFromLayer=0,
            removeBakedAnimFromLayer=0,
            bakeOnOverrideLayer=0,
            minimizeRotation=0,
            controlPoints=0,
            shape=1,
        )
        if deBugMode == 0:
            pm.delete("overlapResultLocator_" + str(i))

        pm.select(
            ("overlapResultLocatorOut_" + str(i)),
            (SelectedControls[i] + "_OverlapJoint"),
            r=1,
        )
        pm.parentConstraint(weight=1, mo=1)

    if useFirstCtrl == 1:
        # constrain controls back to joint
        for i in range(1, iLoop):
            if (
                pm.getAttr((SelectedControls[i] + ".rx"), keyable=1) == 1
                and pm.getAttr((SelectedControls[i] + ".rx"), lock=1) == 0
                and pm.getAttr((SelectedControls[i] + ".ry"), keyable=1) == 1
                and pm.getAttr((SelectedControls[i] + ".ry"), lock=1) == 0
                and pm.getAttr((SelectedControls[i] + ".rx"), keyable=1) == 1
                and pm.getAttr((SelectedControls[i] + ".rx"), lock=1) == 0
            ):
                pm.select(
                    (SelectedControls[i] + "_OverlapJoint"), SelectedControls[i], r=1
                )
                # orient constraint
                pm.orientConstraint(mo=1, weight=1)

            if (
                pm.getAttr((SelectedControls[i] + ".tx"), keyable=1) == 1
                and pm.getAttr((SelectedControls[i] + ".tx"), lock=1) == 0
                and pm.getAttr((SelectedControls[i] + ".ty"), keyable=1) == 1
                and pm.getAttr((SelectedControls[i] + ".ty"), lock=1) == 0
                and pm.getAttr((SelectedControls[i] + ".tx"), keyable=1) == 1
                and pm.getAttr((SelectedControls[i] + ".tx"), lock=1) == 0
            ):
                pm.pointConstraint(mo=1, weight=1)
                # point constraint

    else:
        for i in range(0, iLoop):
            if (
                pm.getAttr((SelectedControls[i] + ".rx"), keyable=1) == 1
                and pm.getAttr((SelectedControls[i] + ".rx"), lock=1) == 0
                and pm.getAttr((SelectedControls[i] + ".ry"), keyable=1) == 1
                and pm.getAttr((SelectedControls[i] + ".ry"), lock=1) == 0
                and pm.getAttr((SelectedControls[i] + ".rx"), keyable=1) == 1
                and pm.getAttr((SelectedControls[i] + ".rx"), lock=1) == 0
            ):
                pm.select(
                    (SelectedControls[i] + "_OverlapJoint"), SelectedControls[i], r=1
                )
                # orient constraint
                pm.orientConstraint(mo=1, weight=1)

            if (
                pm.getAttr((SelectedControls[i] + ".tx"), keyable=1) == 1
                and pm.getAttr((SelectedControls[i] + ".tx"), lock=1) == 0
                and pm.getAttr((SelectedControls[i] + ".ty"), keyable=1) == 1
                and pm.getAttr((SelectedControls[i] + ".ty"), lock=1) == 0
                and pm.getAttr((SelectedControls[i] + ".tx"), keyable=1) == 1
                and pm.getAttr((SelectedControls[i] + ".tx"), lock=1) == 0
            ):
                pm.pointConstraint(mo=1, weight=1)
                # point constraint

    if CycleCheckBox == 1:
        pm.melGlobals["timeStart"] = float(pm.playbackOptions(q=1, min=1))
        pm.melGlobals["timeEnd"] = float(pm.playbackOptions(q=1, max=1))
        cycleLenghts = pm.melGlobals["timeEnd"] - pm.melGlobals["timeStart"]
        pm.select("OverlapperOverlapResultLocatorSet", r=1)
        EulerArrays = pm.ls(sl=1)
        for obj in EulerArrays:
            pm.keyframe(
                (str(obj) + "_translateX"),
                e=1,
                iub=True,
                r=1,
                o="over",
                tc=(-2 * cycleLenghts),
            )
            pm.keyframe(
                (str(obj) + "_translateY"),
                e=1,
                iub=True,
                r=1,
                o="over",
                tc=(-2 * cycleLenghts),
            )
            pm.keyframe(
                (str(obj) + "_translateZ"),
                e=1,
                iub=True,
                r=1,
                o="over",
                tc=(-2 * cycleLenghts),
            )
            pm.keyframe(
                (str(obj) + "_rotateX"),
                e=1,
                iub=True,
                r=1,
                o="over",
                tc=(-2 * cycleLenghts),
            )
            pm.keyframe(
                (str(obj) + "_rotateY"),
                e=1,
                iub=True,
                r=1,
                o="over",
                tc=(-2 * cycleLenghts),
            )
            pm.keyframe(
                (str(obj) + "_rotateZ"),
                e=1,
                iub=True,
                r=1,
                o="over",
                tc=(-2 * cycleLenghts),
            )

    pm.select(SelectedControls, r=1)
    pm.melGlobals["timeStart"] = float(pm.playbackOptions(q=1, min=1))
    pm.melGlobals["timeEnd"] = float(pm.playbackOptions(q=1, max=1))
    pm.bakeResults(
        SelectedControls,
        simulation=0,
        t=(str(pm.melGlobals["timeStart"]) + ":" + str(pm.melGlobals["timeEnd"])),
        sampleBy=1,
        disableImplicitControl=1,
        preserveOutsideKeys=1,
        sparseAnimCurveBake=0,
        removeBakedAttributeFromLayer=0,
        removeBakedAnimFromLayer=0,
        bakeOnOverrideLayer=onLayerSwitch,
        minimizeRotation=0,
        controlPoints=0,
        shape=1,
    )
    # create selection set
    if OvSelectionSet == 1:
        if pm.objExists("OverlapperSet*"):
            pm.pm.cmds.sets(SelectedControls, edit=1, forceElement="OverlapperSet")

        else:
            createSetResult = pm.pm.cmds.sets(name="OverlapperSet")

    if pm.objExists("OverlapperWorkSet*"):
        pm.pm.cmds.sets(SelectedControls, edit=1, forceElement="OverlapperWorkSet")

    else:
        createSetResult = pm.pm.cmds.sets(name="OverlapperWorkSet")

    if deBugMode == 0:
        pm.delete(
            overlapJointsArray, "overlapResultLocatorOut*", "*overlapOffsetIKLocator*"
        )
        # finalization

    pm.currentTime(currentTime, e=1)
    pm.select(SelectedControls, r=1)
    pm.cycleCheck(e=True)
    pm.progressWindow(endProgress=1)
    # select ovelapped controls set
    if pm.objExists("OverlapperSet"):
        pm.select("OverlapperSet", r=1)


def CycleFinal():
    """Finalizing"""

    SelectedControlsClearNameSpaces = []
    SelectedControls = []
    pm.melGlobals.initVar("string[]", "pm.melGlobals['eulerFilterCurves'")
    ControlName = []
    cycleLenghts = 0.0
    # euler all anim curves
    ClearElemwnts = len(pm.melGlobals["eulerFilterCurves"])
    for s in range(0, ClearElemwnts):
        pm.melGlobals["eulerFilterCurves"].pop(0)

    pm.select("OverlapperWorkSet", r=1)
    EulerArrays = pm.ls(sl=1)
    for obj in EulerArrays:
        listAnimAttrs = pm.listAttr(obj, k=1)
        for attr in listAnimAttrs:
            animCurve = pm.listConnections(
                (str(obj) + "." + str(attr)), type="animCurve"
            )
            ClearElemwnts = len(animCurve)
            pm.melGlobals["eulerFilterCurves"] += animCurve[:ClearElemwnts]

    pm.filterCurve(pm.melGlobals["eulerFilterCurves"])
    pm.delete("OverlapperWorkSet")


OverlapperRelease()
