# coding=utf-8
import maya.cmds as cmd
import maya.mel as mel

def ShowUI():
    if cmd.window('windowMain', exists = True):
        cmd.deleteUI('windowMain')
    window = cmd.window('windowMain', maximizeButton = True, minimizeButton = True, sizeable = 1, title = '生成变形对象', widthHeight = (258, 466))
    form = cmd.formLayout()
    
    objLab = cmd.text(label = '需要变形的对象')
    objList = cmd.textScrollList('objList', allowMultiSelection = True, height = 215, width = 190)
    Add = cmd.button(label = '加载', width = 60, c = 'ObjList("objList",0)')
    Remove = cmd.button(label = '删除', width = 60, c = 'ObjList("objList",1)')
    Clear = cmd.button(label = '清空', width = 60, c = 'ObjList("objList",2)')

    objLabOther = cmd.text(label = '混合变形目标体(Blendshape)')
    objListOther = cmd.textScrollList('objListOther', allowMultiSelection = True, height = 215, width = 190)
    AddOther = cmd.button(label = '加载', width = 60, c = 'ObjList("objListOther",0)')
    RemoveOther = cmd.button(label = '删除', width = 60, c = 'ObjList("objListOther",1)')
    ClearOther = cmd.button(label = '清空', width = 60, c = 'ObjList("objListOther",2)')

    BaseObj = cmd.textField('BaseObj_field', w = 150, fi = '')
    BaseObject = cmd.button(label = '对象', c = "sel=cmd.ls(sl=1);cmd.textField('BaseObj_field', e=1 ,fi = sel[0])")
    GenerateObject = cmd.button(label = '生成变形物体', h = 50, w = 150, c = 'GenerateBlendObject()')
    cmd.formLayout(form, edit = True, attachForm = [
        (objLab, 'top', 5),
        (objLab, 'left', 5),
        (objList, 'top', 25),
        (objList, 'left', 5),
        (Add, 'top', 245),
        (Add, 'left', 5),
        (Remove, 'top', 245),
        (Clear, 'top', 245),
        (AddOther, 'top', 520),
        (AddOther, 'left', 5),
        (RemoveOther, 'top', 520),
        (ClearOther, 'top', 520),
        (BaseObj, 'top', 560),
        (BaseObj, 'left', 5),
        (BaseObject, 'top', 557),
        (BaseObject, 'left', 160),
        (objLabOther, 'top', 280),
        (objLabOther, 'left', 5),
        (objListOther, 'top', 300),
        (objListOther, 'left', 5),
        (GenerateObject, 'left', 5),
        (GenerateObject, 'right', 5),
        (GenerateObject, 'bottom', 5)], attachControl = [
        (Remove, 'left', 5, Add),
        (RemoveOther, 'left', 5, AddOther),
        (Clear, 'left', 5, Remove),
        (ClearOther, 'left', 5, RemoveOther),
        (GenerateObject, 'top', 15, BaseObj)])
    cmd.setParent('..')
    cmd.showWindow(window)


def ObjList(List, command):
    if command == 0:
        itemList = cmd.textScrollList(List, query = True, allItems = 1)
        if itemList == None:
            itemList = []
        selection = cmd.filterExpand(selectionMask = 12)
        for item in selection:
            if item not in itemList:
                cmd.textScrollList(List, edit = True, append = item)
                itemList.append(item)
                continue
    if command == 1:
        selection = cmd.textScrollList(List, query = True, selectItem = True)
        for item in selection:
            cmd.textScrollList(List, edit = True, removeItem = item)
        
    if command == 2:
        cmd.textScrollList(List, edit = True, removeAll = True)
        itemList = []


def GenerateBlendObject():
    baseGeo = cmd.textField('BaseObj_field', q = 1, fi = 1)
    TargetAll = cmd.textScrollList('objList', query = True, allItems = 1)
    BlendshapeAll = cmd.textScrollList('objListOther', query = True, allItems = 1)
    cmd.select(TargetAll, r = 1)
    cmd.select(baseGeo, tgl = 1)
    mel.eval('performCreateWrap false')
    cmd.blendShape(BlendshapeAll, baseGeo, n = 'BS')
    obj = []
    for mesh in TargetAll:
        for temp in BlendshapeAll:
            cmd.setAttr('BS.' + temp, 1)
            meshFix = mesh.replace('|', '_')
            cmd.duplicate(mesh, n = meshFix + '_BS_' + temp)
            cmd.setAttr('BS.' + temp, 0)
            obj.append(meshFix + '_BS_' + temp)
        
        blendShapeName = cmd.blendShape(obj, mesh)
        i = 0
        for temp in BlendshapeAll:
            mel.eval('blendShapeRenameTargetAlias' + ' ' + blendShapeName[0] + ' ' + str(i) + ' ' + temp)
            i = i + 1
        
        cmd.hide(obj)
        obj[:] = []
    
    cmd.delete('BS', baseGeo + 'Base')