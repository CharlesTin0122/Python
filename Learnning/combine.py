import pymel.core as pm
def main():
    selList = pm.ls(sl=True)
    lastSel = selList[-1]
    p = lastSel.getParent()
    a = pm.polyUnite(selList)[0]
    a.setParent(p)
    pm.delete(a,ch=True)
    a.rename("combMesh")
    