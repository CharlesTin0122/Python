# -*- coding: utf-8 -*-
'''
@FileName    :   maya_file.py
@DateTime    :   2023/06/13 17:27:43
@Author  :   Tian Chao
@Contact :   tianchao0533@163.com
'''

import pymel.core as pm
import maya.cmds as cmds

path = r"D:\Work_MobilGame\MU_Human_female_001.0001.mb"

"""--------------------------------------cmds------------------------------------------------"""
# 创建新窗口
cmds.file(new=True, force=True)

# 用于导入文件到当前场景。path表示源蒙皮文件的路径，i=True表示导入文件，renameAll=True表示在导入时重命名可能冲突的名称，
# mergeNamespacesOnClash=True表示在命名空间冲突时合并命名空间，namespace=":"表示导入到全局命名空间。
cmds.file(path, i=True, renameAll=True, mergeNamespacesOnClash=True, namespace=":")
# 用于导入文件到当前场景。Path表示动画文件的路径，i=True表示导入文件，renameAll=True表示在导入时重命名可能冲突的名称，
# type='fbx'表示导入的文件类型为FBX，mergeNamespacesOnClash=True表示在命名空间冲突时合并命名空间，
# namespace=":"表示导入到全局命名空间，options="fbx"表示使用FBX导入选项，
# importFrameRate=True表示导入动画时保留原始帧率，importTimeRange='override'表示覆盖当前时间范围。
cmds.file(
    path, i=True, renameAll=True, type='fbx', mergeNamespacesOnClash=True,
    namespace=":", options="fbx", importFrameRate=True, importTimeRange='override'
    )

# 用于导入目标蒙皮文件到当前场景。与导入源蒙皮文件的代码类似，不同之处在于mergeNamespacesOnClash=False表示在命名空间冲突时不合并命名空间，
# namespace="target"表示导入到名为"target"的命名空间。
cmds.file(path, i=True, renameAll=True, mergeNamespacesOnClash=False, namespace="target")

"""---------------------------------------pymel----------------------------------------------------"""
pm.newFile(force=True)
pm.importFile(path, renameAll=True, mergeNamespacesOnClash=True, namespace=":")
pm.importFile(
    path, renameAll=True, type='fbx', mergeNamespacesOnClash=True,
    namespace=":", options="fbx", importFrameRate=True, importTimeRange='override'
    )
pm.importFile(path, renameAll=True, mergeNamespacesOnClash=False, namespace="target")
pm.openFile()
