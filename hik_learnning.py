# -*- coding: utf-8 -*-
'''
@FileName    :   hik_learnning.py
@DateTime    :   2023/06/13 16:36:57
@Author  :   Tian Chao
@Contact :   tianchao0533@163.com
'''

import pymel.core as pm

pm.mel.HIKCharacterControlsTool()  # 打开hik窗口
pm.mel.hikCreateDefinition()  # 打开自定义hik骨骼窗口
pm.mel.hikCreateControlRig()  # 创建控制装备

allCharacter = pm.optionMenuGrp("hikCharacterList", query=True, itemListLong=True)  # 获取所有角色
sourceChar = pm.menuItem(allCharacter[1], query=True, label=True)  # 获取角色标签名称

optMenu = "hikCharacterList|OptionMenu"  # 定义角色列表窗口变量
pm.optionMenu(optMenu, edit=True, select=2)  # 设置角色窗口内的角色
# hik更新
pm.mel.hikUpdateCurrentCharacterFromUI()
pm.mel.hikUpdateContextualUI()
pm.mel.hikUpdateCharacterMenu()
pm.mel.hikUpdateCharacterControlsUICallback()


allSource = pm.optionMenuGrp("hikSourceList", query=True, itemListLong=True)  # 获取所有动画源
sourceChar = pm.menuItem(allSource[1], query=True, label=True)  # 获取动画源标签名称
optMenu = "hikSourceList|OptionMenu"   # 定义动画源列表窗口变量
pm.optionMenu(optMenu, edit=True, select=1)  # 设置动画源窗口内的角色
# hik更新
pm.mel.hikUpdateCurrentSourceFromUI()
pm.mel.hikUpdateContextualUI()
pm.mel.hikControlRigSelectionChangedCallback()
