import pymel.core as pm
import maya.mel as mel

radioCol = None
intF = None

def main():

    try:
        pm.deleteUI("selectEdgeUI")
    except Exception as e:
        print(e)

    global radioCol,intF
    UI = pm.window("selectEdgeUI",title='selectEdge')
    formL = pm.formLayout()
    btn = pm.button(label="Select Edge",command=btnCMD)
    colLay = pm.columnLayout(adj=True)
    radioCol = pm.radioCollection()
    ckBtn1 = pm.radioButton(label='Loop')
    ckBtn2 = pm.radioButton(label='Ring')
    pm.radioCollection(radioCol,e=True,select=ckBtn1)
    
    pm.setParent("..")
    intF = pm.intField(value=2,h=35)

    pm.formLayout(
        formL,e=True,
        attachForm=[
            (colLay,"top",5),(colLay,"left",5),
            (btn,"left",5),(btn,"bottom",5),(btn,"right",5),
            (intF,"top",5),(intF,"right",5)

        ],
        attachControl=[
            (intF,"left",30,colLay),
            (btn,"top",5,colLay)
        ]
    )

    pm.showWindow(UI)

def btnCMD(*args):
    radioBtn = pm.radioCollection(radioCol,q=True,select=True)
    mode = pm.radioButton(radioBtn,q=True,label=True)

    N = pm.intField(intF,q=True,value=True)

    print("mode is:"+ mode)
    print("N is:"+ str(N))
    mel.eval("polySelectEdgesEveryN \"edge{}\" {};".format(mode,N))