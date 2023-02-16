# -*- coding: utf-8 -*-
'''
@FileName    :   tcTools_Plugins.py
@DateTime    :   2023/02/13 16:31:15
@Author  :   Tian Chao 
@Contact :   tianchao0533@163.com
'''

import maya.cmds as cmds
import tcTools_MenuUI
reload(tcTools_MenuUI)

def load_tcTools():
    tcTools_MenuUI.createMenu()

def unLoad_tcTools():
    tcTools_MenuUI.deleteMenu()

def initializePlugin(mobject):
    load_tcTools()

def uninitializePlugin(mobject):
    unLoad_tcTools()