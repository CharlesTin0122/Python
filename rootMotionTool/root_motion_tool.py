# coding=utf-8

import pymel.core as pm


def mainUI():
    try:
        pm.deleteUI('motionTool')
    except Exception as e:
        print(e)

    temlate = pm.uiTemplate('ctTemplate', force=True)
    temlate.define(pm.button, w=200, h=50)
    temlate.define(pm.frameLayout, borderVisible=True, cll=True, cl=False)

    with pm.window('motionTool', title='Motion Tool') as win:
        with temlate:
            with pm.columnLayout(rowSpacing=5, adj=True):
                with pm.frameLayout(label='Motion Switch'):
                    with pm.columnLayout(adj=1, columnAttach=('both', 5), rowSpacing=10):
                        pm.button(label='Local Motion', c=rootToLocal)
                        pm.button(label='Root Motion', c=localToRoot)
    pm.window(win, e=True, w=250, h=100)
    pm.showWindow(win)


def rootToLocal(*args):
    firstFrame = pm.findKeyframe('RootX_M', which="first")
    lastFrame = pm.findKeyframe('RootX_M', which="last")

    pm.spaceLocator(name="locPelvis")
    pm.spaceLocator(name="locLFoot")
    pm.spaceLocator(name="locRFoot")

    pm.parentConstraint('RootX_M', 'locPelvis')
    pm.parentConstraint('IKLeg_L', 'locLFoot')
    pm.parentConstraint('IKLeg_R', 'locRFoot')

    pm.bakeResults('locPelvis', 'locLFoot', 'locRFoot', time=(firstFrame, lastFrame))

    pm.parentConstraint('locPelvis', 'RootX_M')
    pm.parentConstraint('locLFoot', 'IKLeg_L')
    pm.parentConstraint('locRFoot', 'IKLeg_R')

    disAttr = [
        "Main.tx", "Main.ty", "Main.tz", "Main.rx", "Main.ry", "Main.rz",
        "root_ctrl.tx", "root_ctrl.ty", "root_ctrl.tz", "root_ctrl.rx", "root_ctrl.ry", "root_ctrl.rz"
    ]

    for _ in disAttr:
        pm.disconnectAttr(disAttr)

    pm.xform('Main', translation=(0, 0, 0), rotation=(0, 0, 0))
    pm.xform('root_ctrl', translation=(0, 0, 0), rotation=(0, 0, 0))

    pm.bakeResults('RootX_M', 'IKLeg_L', 'IKLeg_R', time=(firstFrame, lastFrame))

    pm.delete('locPelvis', 'locLFoot', 'locRFoot')


def localToRoot(*args):
    firstFrame = pm.findKeyframe('RootX_M', which="first")
    lastFrame = pm.findKeyframe('RootX_M', which="last")

    pm.spaceLocator(name="locPelvis")
    pm.spaceLocator(name="locLFoot")
    pm.spaceLocator(name="locRFoot")

    pm.parentConstraint('RootX_M', 'locPelvis')
    pm.parentConstraint('IKLeg_L', 'locLFoot')
    pm.parentConstraint('IKLeg_R', 'locRFoot')

    pm.bakeResults('locPelvis', 'locLFoot', 'locRFoot', time=(firstFrame, lastFrame))

    pm.parentConstraint('locPelvis', 'RootX_M')
    pm.parentConstraint('locLFoot', 'IKLeg_L')
    pm.parentConstraint('locRFoot', 'IKLeg_R')

    pelvisTX = pm.getAttr('RootX_M.translateX')
    # pelvisTY = pm.getAttr('RootX_M.translateY')
    pelvisTZ = pm.getAttr('RootX_M.translateZ')
    # pelvisRX = pm.getAttr('RootX_M.rotateX')
    pelvisRY = pm.getAttr('RootX_M.rotateY')
    # pelvisRZ = pm.getAttr('RootX_M.rotateZ')

    pm.setAttr('root_ctrl.translateX', pelvisTX)
    pm.setAttr('root_ctrl.translateY', pelvisTZ * -1)
    pm.setAttr('root_ctrl.translateZ', 0)
    pm.setAttr('root_ctrl.rotateX', 0)
    pm.setAttr('root_ctrl.rotateY', 0)
    pm.setAttr('root_ctrl.rotateZ', pelvisRY)

    pm.parentConstraint('locPelvis', 'root_ctrl', mo=True, skipTranslate=["z"], skipRotate=["x", "y"])

    pm.bakeResults('RootX_M', 'IKLeg_L', 'IKLeg_R', 'root_ctrl', 'Main', time=(firstFrame, lastFrame))

    pm.delete('locPelvis', 'locLFoot', 'locRFoot')


if __name__ == '__main__':
    mainUI()
