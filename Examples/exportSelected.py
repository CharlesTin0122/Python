import pymel.core as pm
import os

selList: list = []


def main():
    global selList
    selList = pm.ls(sl=True)

    if not selList:
        pm.PopupError("Nothing Selected!!!")
        return

    try:
        pm.deleteUI("ExpSelWin")
    except Exception as e:
        print(e)

    UI = pm.window("ExpSelWin", title="Exportor")
    forLay = pm.formLayout()
    pText = pm.text(label="Path:")
    pTextF = pm.textField("ExportorTextField")
    btnExp = pm.button(label="Export!", c=exportCMD)
    btnFile = pm.button(label="...", c=selectPath, w=50)

    scrlay = pm.scrollLayout(w=150, h=200)
    for s in selList:
        pm.text(label=s.name())

    pm.formLayout(
        forLay,
        e=True,
        af=[
            (scrlay, "top", 5),
            (scrlay, "left", 5),
            (btnExp, "top", 5),
            (btnExp, "right", 5),
            (pText, "left", 5),
            (pText, "bottom", 5),
            (pTextF, "bottom", 5),
            (btnFile, "bottom", 5),
            (btnFile, "right", 5),
        ],
        ac=[
            (pTextF, "left", 5, pText),
            (pTextF, "right", 5, btnFile),
            (btnExp, "left", 5, scrlay),
            (btnExp, "bottom", 5, btnFile),
            (scrlay, "bottom", 5, pTextF),
        ],
    )
    pm.window(UI, e=True, w=200, h=200)
    pm.showWindow(UI)


def selectPath(*args):
    savePath = pm.fileDialog2(fileFilter="*folder", fileMode=2)
    if savePath:
        savePath = savePath[0]
        pm.textField("ExportorTextField", e=True, text=savePath)


def exportCMD(*args):
    savePath = pm.textField("ExportorTextField", q=True, text=True)
    print(savePath)
    for s in selList:
        pm.select(s)
        filePath = savePath + "/" + s.name() + ".fbx"
        print(filePath)
        pm.exportSelected(filePath, force=True)
    pm.select(selList)

    confirm = pm.confirmDialog(
        title="Finish", message="Done!", button=["OK", "Open Folder"]
    )
    if confirm == "Open Folder":
        os.startfile(savePath)
