# -*- coding: utf-8 -*-
"""
@FileName    :   test001.py
@DateTime    :   2023/04/12 18:07:37
@Author  :   Tian Chao
@Contact :   tianchao0533@163.com
"""

import pymel.core as pm

val = []


def copy(*args):
    global val
    sel_obj = pm.selected()
    obj_attr = pm.listAnimatable(sel_obj)
    val = [pm.getAttr(attr) for attr in obj_attr]


def paste(*args):
    sel_obj = pm.selected()
    obj_attr = pm.listAnimatable(sel_obj)
    for i in range(len(obj_attr)):
        if not obj_attr[i].find("translateX") == -1:
            pm.setAttr(obj_attr[i], val[i] * -1)
        else:
            pm.setAttr(obj_attr[i], val[i])


def main_ui():
    try:
        pm.deleteUI("pos_tool")
    except Exception as e:
        print(e)

    pm.window("pos_tool", title="pos_tool", w=240, h=300)
    pm.columnLayout(rowSpacing=5, adj=True)
    pm.button(label="copy", c=copy, w=20, h=80)
    pm.button(label="past", c=paste, w=20, h=80)
    pm.showWindow("pos_tool")


main_ui()

