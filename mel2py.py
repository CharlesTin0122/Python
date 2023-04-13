# -*- coding: utf-8 -*-
"""
@FileName    :   mel2py.py
@DateTime    :   2023/04/13 10:57:57
@Author  :   Tian Chao
@Contact :   tianchao0533@163.com
"""

import pymel.core as pm
import pymel.tools.mel2py as mel2py


def mel2pymel(*args):
    melCmd = pm.scrollField("melcode", q=1, tx=1)
    pyCmd = mel2py.mel2pyStr(melCmd, pymelNamespace="pm")
    pyFixed = pyCmd.replace("pymel.all", "pymel.core")
    pm.scrollField("pymelcode", e=1, tx=pyFixed)


def mel2py_ui():
    try:
        pm.deleteUI("melpy")
    except Exception as e:
        print(e)

    with pm.window("melpy", title="mel2py", h=150, w=240):
        with pm.columnLayout(adj=1):
            with pm.frameLayout(label="mel"):
                pm.scrollField("melcode", h=100, w=200)
            with pm.frameLayout(label="pymel"):
                pm.scrollField("pymelcode", h=100, w=200)
        with pm.columnLayout(adj=1):
            pm.button(label="Tanslate Mel To Pymel", w=80, h=30, c=mel2pymel)


mel2py_ui()
