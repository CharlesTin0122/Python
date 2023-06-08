# -*- coding: utf-8 -*-
"""
@FileName    :   weightDriverEditRBF.py
@DateTime    :   2023/06/06 11:46:17
@Author  :   Tian Chao
@Contact :   tianchao0533@163.com
"""

import pymel.core as pm


def _getShape(node):
    """---------------------------------------------------------------------
    weightDriverEditRBF.mel

    Weight Driver Version: 3.6

    Description:
         Editor for the weightDriver in generic RBF mode.

    Input Arguments:
         None

    Return Value:
         None
    ---------------------------------------------------------------------
    ---------------------------------------------------------------------

    Usage:

     Run by executing the following command:

         weightDriverEditRBF;

    ---------------------------------------------------------------------

    Procedure Name:
         getShape

    Description:
         Return the shape node name of the weight driver.

    Input Arguments:
         string node     The transform node name of the weight driver.

    Return Value:
         string
    """

    if pm.nodeType(node) == "transform":
        rel = pm.listRelatives(node, shapes=1)
        return rel[0]

    return node


def _getTransform(node):
    """
    Procedure Name:
         getTransform

    Description:
         Return the name of the transform node of the weight driver.

    Input Arguments:
         string node     The shape node name of the weight driver.

    Return Value:
         string
    """

    if pm.nodeType(node) == "weightDriver":
        rel = pm.listRelatives(node, parent=1)
        return rel[0]

    return node


def weightDriverCloseRBFUI():
    """---------------------------------------------------------------------
    cleanup
    ---------------------------------------------------------------------

    Procedure Name:
         weightDriverCloseRBFUI

    Description:
         Close the edit window.

    Input Arguments:
         None

    Return Value:
         None
    """

    if pm.window("weightDriverEditRBFWin", exists=1):
        pm.deleteUI("weightDriverEditRBFWin")


def _clearPoseItems():
    """
    Procedure Name:
         clearPoseItems

    Description:
         Remove all pose item children from the pose data layout.

    Input Arguments:
         None

    Return Value:
         None
    """

    items = pm.scrollLayout("wdUI_poseDataLayout", query=1, childArray=1)
    for i in items:
        pm.deleteUI(i)


def _clearAll():
    """
    Procedure Name:
         clearAll

    Description:
         Clear all fields and lists in the edit window.

    Input Arguments:
         None

    Return Value:
         None
    """

    pm.melGlobals.initVar("int", "gWeightDriverDriverAttrCount")
    pm.melGlobals.initVar("int", "gWeightDriverDrivenAttrCount")
    pm.melGlobals["gWeightDriverDriverAttrCount"] = 0
    pm.melGlobals["gWeightDriverDrivenAttrCount"] = 0
    pm.textField("wdUI_driverField", edit=1, text="")
    pm.textField("wdUI_drivenField", edit=1, text="")
    pm.iconTextScrollList("wdUI_driverAttrList", edit=1, removeAll=1)
    pm.iconTextScrollList("wdUI_drivenAttrList", edit=1, removeAll=1)
    _clearPoseItems()


def _buildDriverMenu():
    """---------------------------------------------------------------------
    solver option menu
    ---------------------------------------------------------------------

    Procedure Name:
         buildDriverMenu

    Description:
         Build the option menu for the solvers and collect all weight
         driver nodes in the scene.

    Input Arguments:
         None

    Return Value:
         None
    """

    if pm.optionMenu("wdUI_weightDriverNodeOption", exists=1):
        items = pm.optionMenu("wdUI_weightDriverNodeOption", query=1, itemListLong=1)
        for c in items:
            pm.deleteUI(c)

    pm.menuItem(label="New", parent="wdUI_weightDriverNodeOption")
    nodes = pm.ls(type="weightDriver")
    for n in nodes:
        if pm.getAttr(str(n) + ".type"):
            pm.menuItem(label=(_getTransform(n)), parent="wdUI_weightDriverNodeOption")

    if not len(nodes):
        _clearAll()


def weightDriverGetSelectedNodeOption():
    """
    Procedure Name:
         weightDriverGetSelectedNodeOption

    Description:
         Return the name of the selected node from the driver option
         menu.

    Input Arguments:
         None

    Return Value:
         string
    """

    node = str(pm.optionMenu("wdUI_weightDriverNodeOption", query=1, value=1))
    if node == "New":
        node = ""

    return node


def weightDriverRefreshUI():
    """
    Procedure Name:
         weightDriverRefreshUI

    Description:
         Rebuild the driver menu and clears all fields and lists.

    Input Arguments:
         None

    Return Value:
         None
    """

    _buildDriverMenu()
    _clearAll()


def _buildEditWindow():
    """---------------------------------------------------------------------
    window
    ---------------------------------------------------------------------

    Procedure Name:
         buildEditWindow

    Description:
         Build the window and controls for editing the RBF solver.

    Input Arguments:
         None

    Return Value:
         None
    """

    if pm.window("weightDriverEditRBFWin", exists=1):
        pm.deleteUI("weightDriverEditRBFWin")

    pm.window(
        "weightDriverEditRBFWin", title="Edit RBF WeightDriver", widthHeight=(700, 500)
    )
    state = int(pm.optionVar(query="weightDriverAutoFillValues"))
    pm.menuBarLayout()
    pm.menu(label="Settings")
    pm.menuItem(
        label="Auto Fill Blend Shape Values",
        checkBox=state,
        command=lambda *args: pm.optionVar(iv=("weightDriverAutoFillValues", args[0])),
    )
    pm.setParent("..")
    mainForm = str(pm.formLayout())
    # -------------------
    # weight driver node
    # -------------------
    nodeOptionForm = str(pm.formLayout())
    nodeLabel = str(pm.text(label="RBF Node", align="left", width=64))
    pm.optionMenu(
        "wdUI_weightDriverNodeOption",
        changeCommand=lambda *args: pm.mel.weightDriverGetData(),
    )
    pm.menuItem(label="None")
    pm.popupMenu()
    pm.menuItem(
        label="Select Solver",
        command=lambda *args: pm.mel.eval(
            'if (weightDriverGetSelectedNodeOption() != "") \
                            select -r (weightDriverGetSelectedNodeOption());'
        ),
    )
    pm.menuItem(divider=1)
    pm.menuItem(
        label="Delete Solver",
        command=lambda *args: pm.mel.eval(
            'if (weightDriverGetSelectedNodeOption() != "") \
                            { select -r (weightDriverGetSelectedNodeOption()); delete; weightDriverRefreshUI; }'
        ),
    )
    refreshButton = str(
        pm.button(
            label="Refresh",
            width=60,
            command=lambda *args: pm.mel.weightDriverRefreshUI(),
        )
    )
    pm.formLayout(
        nodeOptionForm,
        edit=1,
        attachForm=[
            (nodeLabel, "top", 7),
            (nodeLabel, "left", 5),
            ("wdUI_weightDriverNodeOption", "top", 5),
            (refreshButton, "top", 3),
            (refreshButton, "right", 5),
        ],
        attachControl=[
            ("wdUI_weightDriverNodeOption", "left", 3, nodeLabel),
            ("wdUI_weightDriverNodeOption", "right", 15, refreshButton),
        ],
    )
    pm.setParent("..")
    sep1 = str(pm.separator(style="in", height=15))
    # -------------------
    # rbf driver & driven
    # -------------------
    attrForm = str(pm.formLayout(height=182))
    driverLabel = str(pm.text(label="Driver", width=60, align="left"))
    pm.textField("wdUI_driverField", width=100)
    driverButton = str(
        pm.button(
            label="Select", command=lambda *args: pm.mel.weightDriverGetNode("driver")
        )
    )
    driverAttrLabel = str(pm.text(label="Attributes", width=60, align="left"))
    driverAttrList = str(
        pm.iconTextScrollList("wdUI_driverAttrList", ams=1, height=150)
    )
    state = int(pm.optionVar(query="weightDriverAttributeDisplayDriver"))
    pm.popupMenu()
    pm.menuItem(
        label="Show Keyable Only",
        checkBox=state,
        command=lambda *args: pm.mel.eval(
            "optionVar -iv weightDriverAttributeDisplayDriver #1; \
                            weightDriverListAttributes driver"
        ),
    )
    drivenLabel = str(pm.text(label="Driven", width=60, align="left"))
    pm.textField("wdUI_drivenField", width=100)
    drivenButton = str(
        pm.button(
            label="Select", command=lambda *args: pm.mel.weightDriverGetNode("driven")
        )
    )
    drivenAttrLabel = str(pm.text(label="Attributes", width=60, align="left"))
    drivenAttrList = str(
        pm.iconTextScrollList("wdUI_drivenAttrList", allowMultiSelection=1, height=150)
    )
    state = int(pm.optionVar(query="weightDriverAttributeDisplayDriven"))
    pm.popupMenu()
    pm.menuItem(
        label="Show Keyable Only",
        checkBox=state,
        command=lambda *args: pm.mel.eval(
            "optionVar -iv weightDriverAttributeDisplayDriven #1; \
                            weightDriverListAttributes driven"
        ),
    )
    div = str(pm.separator(style="in", horizontal=0))
    pm.formLayout(
        attrForm,
        edit=1,
        attachForm=[
            (driverLabel, "top", 5),
            (driverLabel, "left", 5),
            ("wdUI_driverField", "top", 2),
            (driverButton, "top", 0),
            (driverAttrLabel, "left", 5),
            (div, "top", 5),
            (div, "bottom", 5),
            (drivenLabel, "top", 5),
            ("wdUI_drivenField", "top", 2),
            (drivenButton, "top", 0),
            (drivenButton, "right", 5),
            (drivenAttrList, "right", 5),
        ],
        attachControl=[
            ("wdUI_driverField", "left", 5, driverLabel),
            ("wdUI_driverField", "right", 5, driverButton),
            (driverAttrLabel, "top", 17, driverLabel),
            (driverAttrList, "top", 10, "wdUI_driverField"),
            (driverAttrList, "left", 5, driverAttrLabel),
            ("wdUI_drivenField", "left", 5, drivenLabel),
            ("wdUI_drivenField", "right", 5, drivenButton),
            (drivenAttrLabel, "top", 17, drivenLabel),
            (drivenAttrList, "top", 10, "wdUI_drivenField"),
            (drivenAttrList, "left", 5, drivenAttrLabel),
        ],
        attachPosition=[
            (driverButton, "right", 15, 50),
            (driverAttrList, "right", 15, 50),
            (drivenLabel, "left", 15, 50),
            (drivenAttrLabel, "left", 15, 50),
            (div, "left", 0, 50),
        ],
    )
    pm.setParent("..")
    sep2 = str(pm.separator(style="in", height=15))
    # -------------------
    # pose data
    # -------------------
    pm.scrollLayout("wdUI_poseDataLayout", childResizable=1)

    pm.setParent("..")
    sep3 = str(pm.separator(style="in", height=15))
    buttonAdd = str(
        pm.button(
            label="Add Pose",
            height=25,
            command=lambda *args: pm.mel.weightDriverAddPose(),
        )
    )
    buttonApply = str(
        pm.button(
            label="Apply", height=25, command=lambda *args: pm.mel.weightDriverApply(0)
        )
    )
    buttonConnect = str(
        pm.button(
            label="Connect",
            height=25,
            command=lambda *args: pm.mel.weightDriverApply(1),
        )
    )
    buttonCancel = str(
        pm.button(
            label="Close",
            height=25,
            command=lambda *args: pm.mel.weightDriverCloseRBFUI(),
        )
    )
    pm.formLayout(
        mainForm,
        edit=1,
        attachForm=[
            (nodeOptionForm, "top", 5),
            (nodeOptionForm, "left", 5),
            (nodeOptionForm, "right", 5),
            (sep1, "left", 10),
            (sep1, "right", 10),
            (attrForm, "left", 5),
            (attrForm, "right", 5),
            (sep2, "left", 10),
            (sep2, "right", 10),
            ("wdUI_poseDataLayout", "left", 10),
            ("wdUI_poseDataLayout", "right", 10),
            (sep3, "left", 10),
            (sep3, "right", 10),
            (buttonAdd, "left", 5),
            (buttonAdd, "bottom", 5),
            (buttonApply, "bottom", 5),
            (buttonConnect, "bottom", 5),
            (buttonCancel, "right", 5),
            (buttonCancel, "bottom", 5),
        ],
        attachControl=[
            (sep1, "top", 0, nodeOptionForm),
            (attrForm, "top", 0, sep1),
            (sep2, "top", 0, attrForm),
            ("wdUI_poseDataLayout", "top", 0, sep2),
            ("wdUI_poseDataLayout", "bottom", 10, sep3),
            (sep3, "bottom", 0, buttonApply),
        ],
        attachPosition=[
            (buttonAdd, "right", 5, 25),
            (buttonApply, "left", 5, 25),
            (buttonApply, "right", 5, 50),
            (buttonConnect, "left", 5, 50),
            (buttonConnect, "right", 5, 75),
            (buttonCancel, "left", 5, 75),
        ],
    )
    pm.setParent("..")
    pm.showWindow("weightDriverEditRBFWin")
    _buildDriverMenu()


def _readPoseData(node, id):
    """---------------------------------------------------------------------
    get the data from an existing setup
    ---------------------------------------------------------------------

    Procedure Name:
         readPoseData

    Description:
         Populate all fields based on the current solver selection.

    Input Arguments:
         string node         The name of the solver.
         int id              The index of the pose to get the data from.

    Return Value:
         None
    """

    pm.setParent("wdUI_poseDataLayout")
    attrSize = int(pm.getAttr((node + ".input"), size=1))
    valSize = int(pm.getAttr((node + ".output"), size=1))
    if attrSize == 0 or valSize == 0:
        return

    pm.rowLayout(
        ("wdUI_poseData_" + str(id) + "_row"), numberOfColumns=(attrSize + valSize + 7)
    )
    pm.text(label=("Pose " + str(id)), width=60, align="left")
    for i in range(0, attrSize):
        v = float(
            pm.getAttr(node + ".poses[" + str(id) + "].poseInput[" + str(i) + "]")
        )
        pm.floatField(
            ("wdUI_poseData_" + str(id) + "_a" + str(i)), precision=3, value=v
        )

    pm.separator(style="in", horizontal=0, width=25, height=20)
    for i in range(0, valSize):
        v = float(
            pm.getAttr(node + ".poses[" + str(id) + "].poseValue[" + str(i) + "]")
        )
        pm.floatField(
            ("wdUI_poseData_" + str(id) + "_v" + str(i)), precision=3, value=v
        )

    pm.separator(style="none", width=10)
    pm.button(
        label="Recall",
        width=50,
        command=lambda *args: pm.mel.eval(("weightDriverRecallPose " + str(id))),
    )
    pm.separator(style="none", width=10)
    # button -label "Update" -width 50 -command ("weightDriverUpdatePose " + $id);
    pm.separator(style="none", width=77)
    pm.button(
        label="Delete",
        command=lambda *args: pm.mel.eval(
            ("deleteUI wdUI_poseData_" + str(id) + "_row")
        ),
    )
    pm.setParent("..")


def weightDriverGetData():
    """
    Procedure Name:
         weightDriverGetData

    Description:
         Get the driver and driven nodes for the current solver and
         gather the attributes and pose values to populate the ui.

    Input Arguments:
         None

    Return Value:
         None
    """

    pm.melGlobals.initVar("int", "gWeightDriverDriverAttrCount")
    pm.melGlobals.initVar("int", "gWeightDriverDrivenAttrCount")
    _clearAll()
    node = str(weightDriverGetSelectedNodeOption())
    if node == "":
        return

    node = str(_getShape(node))
    # driver
    input = pm.listConnections(
        (node + ".input"),
        source=1,
        destination=0,
        plugs=1,
        connections=1,
        skipConversionNodes=1,
    )
    driver = ""
    driverAttrs = []
    for i in range(0, len(input), 2):
        items = input[i + 1].split(".")
        if driver == "":
            driver = items[0]

        driverAttrs.append(items[1])

    pm.melGlobals["gWeightDriverDriverAttrCount"] = len(driverAttrs)
    pm.textField("wdUI_driverField", edit=1, text=driver)
    listItems = pm.mel.weightDriverListAttributes("driver")
    for a in driverAttrs:
        if a in listItems:
            pm.iconTextScrollList("wdUI_driverAttrList", edit=1, selectItem=a)

    output = pm.listConnections(
        (node + ".output"),
        source=0,
        destination=1,
        plugs=1,
        connections=1,
        skipConversionNodes=1,
    )
    # driven
    driven = ""
    drivenAttrs = []
    for i in range(0, len(output), 2):
        items = output[i + 1].split(".")
        if driven == "":
            driven = items[0]

        drivenAttrs.append(items[1])

    pm.melGlobals["gWeightDriverDrivenAttrCount"] = len(drivenAttrs)
    pm.textField("wdUI_drivenField", edit=1, text=driven)
    listItems = pm.mel.weightDriverListAttributes("driven")
    for a in drivenAttrs:
        if a in listItems:
            pm.iconTextScrollList("wdUI_drivenAttrList", edit=1, selectItem=a)

    poseIds = pm.getAttr((node + ".poses"), multiIndices=1)
    # poses
    if poseIds[0] != 0:
        pm.setAttr((node + ".poses[0].poseInput[0]"), 0)
        pm.setAttr((node + ".poses[0].poseValue[0]"), 0)
        poseIds = pm.getAttr((node + ".poses"), multiIndices=1)

    for id in poseIds:
        _readPoseData(node, id)


def weightDriverGetNode(type):
    """---------------------------------------------------------------------
    attribute lists
    ---------------------------------------------------------------------

    Procedure Name:
         weightDriverGetNode

    Description:
         Load the selected node from the scene as either a driver or
         driven node and list the attributes.

    Input Arguments:
         string type         The type of which the node should be loaded
                             as. Use "driver" or "driven".

    Return Value:
         None
    """

    sel = pm.ls(selection=1)
    if not len(sel):
        return

    if type == "driver":
        pm.textField("wdUI_driverField", edit=1, text=sel[0])

    else:
        pm.textField("wdUI_drivenField", edit=1, text=sel[0])

    pm.mel.weightDriverListAttributes(type)


def weightDriverListAttributes(type):
    """
    Procedure Name:
         weightDriverListAttributes

    Description:
         List and return the attributes of the driver or driven node
         depending on the keyable/non-keyable preference setting.

    Input Arguments:
         string type         The type usage of the node.
                             Use "driver" or "driven".

    Return Value:
         string[]
    """

    list = ""
    node = ""
    flag = ""
    if type == "driver":
        list = "wdUI_driverAttrList"
        node = str(pm.textField("wdUI_driverField", query=1, text=1))
        if pm.optionVar(query="weightDriverAttributeDisplayDriver"):
            flag = "-keyable "

    else:
        list = "wdUI_drivenAttrList"
        node = str(pm.textField("wdUI_drivenField", query=1, text=1))
        if pm.optionVar(query="weightDriverAttributeDisplayDriven"):
            flag = "-keyable "

    pm.iconTextScrollList(list, edit=1, removeAll=1)
    cmd = "listAttr -multi " + flag + node
    attributes = pm.mel.eval(cmd)
    for a in attributes:
        pm.iconTextScrollList(list, edit=1, append=a)

    return attributes


def _getSelectedNodeAttributes(type):
    """
    Procedure Name:
         getSelectedNodeAttributes

    Description:
         Return the selected node attributes in the list.

    Input Arguments:
         string type         The type usage of the node.
                             Use "driver" or "driven".

    Return Value:
         string[]
    """

    list = ""
    if type == "driver":
        list = "wdUI_driverAttrList"

    else:
        list = "wdUI_drivenAttrList"

    attributes = pm.iconTextScrollList(list, query=1, selectItem=1)
    return attributes


def _getAttributes(driverAttrs, drivenAttrs):
    """
    Procedure Name:
         getAttributes

    Description:
         Get the driver and driven attributes through the given string
         arrays.
         Also perform a check if the attribute count matches the count of
         existing pose attributes and return it.

    Input Arguments:
         string[] driverAttrs        The attribute list of all driver
                                     attributes for the solver.
         string[] drivenAttrs        The attribute list of all driven
                                     attributes for the solver.

    Return Value:
         int (bool)
    """

    pm.melGlobals.initVar("int", "gWeightDriverDriverAttrCount")
    pm.melGlobals.initVar("int", "gWeightDriverDrivenAttrCount")
    driver = str(pm.textField("wdUI_driverField", query=1, text=1))
    driven = str(pm.textField("wdUI_drivenField", query=1, text=1))
    if driver == "" or driven == "":
        return 0

    driverAttrs = str(_getSelectedNodeAttributes("driver"))
    if not len(driverAttrs):
        pm.mel.error("No driver attributes selected")
        return 0

    elif pm.melGlobals["gWeightDriverDriverAttrCount"] != 0 and pm.melGlobals[
        "gWeightDriverDriverAttrCount"
    ] != len(driverAttrs):
        pm.mel.error(
            "The driver attribute count is different from the already existing poses"
        )
        return 0

    else:
        pm.melGlobals["gWeightDriverDriverAttrCount"] = len(driverAttrs)

    drivenAttrs = str(_getSelectedNodeAttributes("driven"))
    if not len(drivenAttrs):
        pm.mel.error("No driven attributes selected")
        return 0

    elif pm.melGlobals["gWeightDriverDrivenAttrCount"] != 0 and pm.melGlobals[
        "gWeightDriverDrivenAttrCount"
    ] != len(drivenAttrs):
        pm.mel.error(
            "The driven attribute count is different from the already existing poses"
        )
        return 0

    else:
        pm.melGlobals["gWeightDriverDrivenAttrCount"] = len(drivenAttrs)

    return 1


def _getPoseIndices():
    """---------------------------------------------------------------------
    poses
    ---------------------------------------------------------------------

    Procedure Name:
         getPoseIndices

    Description:
         Return a list of all pose indices.

    Input Arguments:
         None

    Return Value:
         int[]
    """

    ids = []
    items = pm.scrollLayout("wdUI_poseDataLayout", query=1, childArray=1)
    for i in items:
        temp = i.split("_")
        ids.append(int(temp[-2]))

    return ids


def _getNewPoseIndex():
    """
    Procedure Name:
         getNewPoseIndex

    Description:
         Return a new pose index.

    Input Arguments:
         None

    Return Value:
         int
    """

    ids = _getPoseIndices()
    if len(ids):
        return ids[-1] + 1

    return 0


def _hasRestPose():
    """
    Procedure Name:
         hasRestPose

    Description:
         Return true if the first row is filled with zeros.

    Input Arguments:
         None

    Return Value:
         int (bool)
    """

    result = 0
    if pm.rowLayout("wdUI_poseData_0_row", query=1, exists=1):
        sum = float(0)
        items = pm.rowLayout("wdUI_poseData_0_row", query=1, childArray=1)
        for i in items:
            if pm.mel.gmatch(i, "*_v*"):
                sum += float(pm.floatField(i, query=1, value=1))

        if sum == 0:
            result = 1

    return result


def _addPoseData(id, driverAttrs, drivenAttrs):
    """
    Procedure Name:
         addPoseData

    Description:
         Create a new row of pose data in the pose section of the ui.

    Input Arguments:
         int id                  The index of the pose on the solver.
         string[] driverAttrs    The list of driver attributes.
         string[] drivenAttrs    The list of driven attributes.

    Return Value:
         None
    """

    pm.setParent("wdUI_poseDataLayout")
    attrSize = len(driverAttrs)
    valSize = len(drivenAttrs)
    driver = str(pm.textField("wdUI_driverField", query=1, text=1))
    driven = str(pm.textField("wdUI_drivenField", query=1, text=1))
    if driver == "" or driven == "":
        return

    isBlendShape = 0
    asRest = 0
    hasRest = 0
    if pm.nodeType(driven) == "blendShape" and pm.optionVar(
        query="weightDriverAutoFillValues"
    ):
        isBlendShape = 1
        hasRest = int(_hasRestPose())
        if _getNewPoseIndex() == 0:
            confirm = str(
                pm.confirmDialog(
                    title="WeightDriver",
                    message="Add the first pose as the rest pose?",
                    button=["OK", "Cancel"],
                    defaultButton="OK",
                    cancelButton="Cancel",
                    dismissString="Cancel",
                )
            )
            if confirm == "OK":
                asRest = 1

    pm.rowLayout(
        ("wdUI_poseData_" + str(id) + "_row"), numberOfColumns=(attrSize + valSize + 8)
    )
    pm.text(label=("Pose " + str(id)), width=60, align="left")
    for i in range(0, attrSize):
        v = float(pm.getAttr(driver + "." + driverAttrs[i]))
        pm.floatField(
            ("wdUI_poseData_" + str(id) + "_a" + str(i)), precision=3, value=v
        )

    pm.separator(style="in", horizontal=0, width=25, height=20)
    for i in range(0, valSize):
        v = float(0)
        if not asRest:
            if not isBlendShape:
                v = float(pm.getAttr(driven + "." + drivenAttrs[i]))

            else:
                position = id - hasRest
                if i == position:
                    v = float(1)

        pm.floatField(
            ("wdUI_poseData_" + str(id) + "_v" + str(i)), precision=3, value=v
        )

    pm.separator(style="none", width=10)
    pm.button(
        label="Recall",
        width=50,
        command=lambda *args: pm.mel.eval(("weightDriverRecallPose " + str(id))),
    )
    pm.separator(style="none", width=10)
    pm.button(
        label="Update",
        width=50,
        command=lambda *args: pm.mel.eval(("weightDriverUpdatePose " + str(id))),
    )
    pm.separator(style="none", width=25)
    pm.button(
        label="Delete",
        command=lambda *args: pm.mel.eval(
            ("deleteUI wdUI_poseData_" + str(id) + "_row")
        ),
    )
    pm.setParent("..")


def weightDriverAddPose():
    """
    Procedure Name:
         weightDriverAddPose

    Description:
         Create a new pose based on the scene state.

    Input Arguments:
         None

    Return Value:
         None
    """

    driverAttrs = []
    drivenAttrs = []
    result = int(_getAttributes(driverAttrs, drivenAttrs))
    if result == 0:
        return

    _addPoseData(_getNewPoseIndex(), driverAttrs, drivenAttrs)


def weightDriverUpdatePose(id):
    """
    Procedure Name:
         weightDriverUpdatePose

    Description:
         Update the pose values based on the current scene state.

    Input Arguments:
         int id          The index of the pose on the solver.

    Return Value:
         None
    """

    driverAttrs = []
    drivenAttrs = []
    result = int(_getAttributes(driverAttrs, drivenAttrs))
    if result == 0:
        return

    driver = str(pm.textField("wdUI_driverField", query=1, text=1))
    driven = str(pm.textField("wdUI_drivenField", query=1, text=1))
    if driver == "" or driven == "":
        return

    for i in range(0, len(driverAttrs)):
        v = float(pm.getAttr(driver + "." + driverAttrs[i]))
        pm.floatField(("wdUI_poseData_" + str(id) + "_a" + str(i)), edit=1, value=v)

    for i in range(0, len(drivenAttrs)):
        v = float(pm.getAttr(driven + "." + drivenAttrs[i]))
        pm.floatField(("wdUI_poseData_" + str(id) + "_v" + str(i)), edit=1, value=v)


def weightDriverRecallPose(id):
    """
    Procedure Name:
         weightDriverRecallPose

    Description:
         Apply all values from the current pose to the driver and driven
         nodes.

    Input Arguments:
         int id          The index of the pose on the solver.

    Return Value:
         None
    """

    driverAttrs = []
    drivenAttrs = []
    result = int(_getAttributes(driverAttrs, drivenAttrs))
    if result == 0:
        return

    driver = str(pm.textField("wdUI_driverField", query=1, text=1))
    driven = str(pm.textField("wdUI_drivenField", query=1, text=1))
    if driver == "" or driven == "":
        return

    cmd = ""
    for i in range(0, len(driverAttrs)):
        conn = pm.listConnections(
            (driver + "." + driverAttrs[i]),
            source=1,
            destination=0,
            plugs=1,
            connections=1,
            skipConversionNodes=1,
        )
        if len(conn):
            cmd += "disconnectAttr " + conn[1] + " " + conn[0] + ";\n"

        v = float(
            pm.floatField(
                ("wdUI_poseData_" + str(id) + "_a" + str(i)), query=1, value=1
            )
        )
        cmd += "setAttr " + driver + "." + driverAttrs[i] + " " + str(v) + ";\n"
        if len(conn):
            cmd += "connectAttr " + conn[1] + " " + conn[0] + ";\n"

    for i in range(0, len(drivenAttrs)):
        conn = pm.listConnections(
            (driven + "." + drivenAttrs[i]),
            source=1,
            destination=0,
            plugs=1,
            connections=1,
            skipConversionNodes=1,
        )
        if len(conn):
            cmd += "disconnectAttr " + conn[1] + " " + conn[0] + ";\n"

        v = float(
            pm.floatField(
                ("wdUI_poseData_" + str(id) + "_v" + str(i)), query=1, value=1
            )
        )
        cmd += "setAttr " + driven + "." + drivenAttrs[i] + " " + str(v) + ";\n"
        if len(conn):
            cmd += "connectAttr " + conn[1] + " " + conn[0] + ";\n"

    pm.mel.eval(cmd)


def _createDriver():
    """---------------------------------------------------------------------
    creating/editing the solver node
    ---------------------------------------------------------------------

    Procedure Name:
         createDriver

    Description:
         Create a new weight driver RBF node.
         Return the name of the transform node of the solver.

    Input Arguments:
         None

    Return Value:
         string
    """

    driver = str(pm.textField("wdUI_driverField", query=1, text=1))
    driven = str(pm.textField("wdUI_drivenField", query=1, text=1))
    if driver == "" or driven == "":
        return ""

    sel = pm.ls(selection=1)
    node = str(pm.createNode("weightDriver"))
    pm.setAttr((node + ".type"), 1)
    if len(sel):
        pm.select(sel, replace=1)

    return _getTransform(node)


def _createPoses(node, connect):
    """
    Procedure Name:
         createPoses

    Description:
         Create new poses based on the current driver and driven
         attributes.

    Input Arguments:
         string node         The name of the solver's transform node.
         int connect         Wether the attributes for the pose should
                             only get set or connected.

    Return Value:
         None
    """

    driverAttrs = []
    drivenAttrs = []
    result = int(_getAttributes(driverAttrs, drivenAttrs))
    if result == 0:
        return

    driver = str(pm.textField("wdUI_driverField", query=1, text=1))
    driven = str(pm.textField("wdUI_drivenField", query=1, text=1))
    sel = []
    if connect:
        sel = pm.ls(selection=1)
        if not len(sel):
            return

    if driver == "" or driven == "":
        return

    for i in range(0, len(driverAttrs)):
        pm.connectAttr(
            (driver + "." + driverAttrs[i]), (node + ".input[" + str(i) + "]"), force=1
        )

    ids = _getPoseIndices()
    poseCount = 0
    if connect:
        poseCount = len(sel)

    else:
        poseCount = len(ids)

    for p in range(0, poseCount):
        if connect:
            for i in range(0, len(driverAttrs)):
                pm.connectAttr(
                    (sel[p] + "." + driverAttrs[i]),
                    (node + ".poses[" + str(p) + "].poseInput[" + str(i) + "]"),
                    force=1,
                )

            for i in range(0, len(drivenAttrs)):
                pm.connectAttr(
                    (sel[p] + "." + drivenAttrs[i]),
                    (node + ".poses[" + str(p) + "].poseValue[" + str(i) + "]"),
                    force=1,
                )

        else:
            id = ids[p]
            for i in range(0, len(driverAttrs)):
                v = float(
                    pm.floatField(
                        ("wdUI_poseData_" + str(id) + "_a" + str(i)), query=1, value=1
                    )
                )
                pm.setAttr(
                    (node + ".poses[" + str(p) + "].poseInput[" + str(i) + "]"), v
                )

            for i in range(0, len(drivenAttrs)):
                v = float(
                    pm.floatField(
                        ("wdUI_poseData_" + str(id) + "_v" + str(i)), query=1, value=1
                    )
                )
                pm.setAttr(
                    (node + ".poses[" + str(p) + "].poseValue[" + str(i) + "]"), v
                )

    for i in range(0, len(drivenAttrs)):
        pm.connectAttr(
            (node + ".output[" + str(i) + "]"), (driven + "." + drivenAttrs[i]), force=1
        )

    pm.setAttr((node + ".evaluate"), 0)
    pm.setAttr((node + ".evaluate"), 1)


def _deleteData(node):
    """
    Procedure Name:
         deleteData

    Description:
         Remove all array inputs of a pose as a preparation for adding
         new poses.
         Return the name of the transform node of the solver.

    Input Arguments:
         string node         The name of the solver's transform node.

    Return Value:
         string
    """

    node = str(_getShape(node))
    #
    # remove all array inputs as a preparation
    # for adding new poses
    #
    ids = pm.getAttr((node + ".input"), multiIndices=1)
    for id in ids:
        pm.removeMultiInstance((node + ".input[" + str(id) + "]"), b=1)

    ids = pm.getAttr((node + ".poses"), multiIndices=1)
    for id in ids:
        pm.removeMultiInstance((node + ".poses[" + str(id) + "]"), b=1)

    ids = pm.getAttr((node + ".output"), multiIndices=1)
    for id in ids:
        pm.removeMultiInstance((node + ".output[" + str(id) + "]"), b=1)

    return _getTransform(node)


def weightDriverApply(connect):
    """
    Procedure Name:
         weightDriverApply

    Description:
         Creates a new solver or update an existing solver.

    Input Arguments:
         int connect         Defines if pose values should only be set
                             (false) or if they should be connected to
                             the pose attributes (true).

    Return Value:
         None
    """

    sel = pm.ls(selection=1)
    node = str(pm.optionMenu("wdUI_weightDriverNodeOption", query=1, value=1))
    if node == "New":
        node = str(_createDriver())

    else:
        node = str(_deleteData(node))

    if node != "":
        _createPoses(node, connect)
        # select the new or current solver in the option menu

    _buildDriverMenu()
    items = pm.optionMenu("wdUI_weightDriverNodeOption", query=1, itemListLong=1)
    for i in range(0, len(items)):
        label = str(pm.menuItem(items[i], query=1, label=1))
        if label == node:
            pm.optionMenu("wdUI_weightDriverNodeOption", edit=1, select=(i + 1))
            break

    weightDriverGetData()
    pm.catch(lambda: pm.select(sel, replace=1))


def weightDriverEditRBF():
    """---------------------------------------------------------------------
    entry
    ---------------------------------------------------------------------"""

    pm.melGlobals.initVar("int", "gWeightDriverDriverAttrCount")
    pm.melGlobals.initVar("int", "gWeightDriverDrivenAttrCount")
    pm.melGlobals["gWeightDriverDriverAttrCount"] = 0
    pm.melGlobals["gWeightDriverDrivenAttrCount"] = 0
    if not pm.pluginInfo("weightDriver", query=1, loaded=1):
        pm.loadPlugin("weightDriver")

    _buildEditWindow()
