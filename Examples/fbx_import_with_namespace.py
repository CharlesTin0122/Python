# -*- coding: utf-8 -*-
"""
@FileName      : fbx_import_with_namespace.py
@DateTime      : 2024/04/30 16:40:48
@Author        : Tian Chao
@Contact       : tianchao0533@163.com
@Software      : Maya 2024.2
@PythonVersion : python 3.10.8
@librarys      : maya.cmds
@Description   : Imports a FBX file into the scene with the specified namespace.
"""

import maya.cmds as cmds

"""
要想使导入的FBX资产具有指定的命名空间,
必须首先在场景中创建并激活该命名空间,
然后导入文件时使用该命名空间cmds.file(i=True,namespace=ns)。
"""


def fbx_import_with_namespace(ns="targetNamespace"):
    """
    Imports a FBX file into the scene with the specified namespace.

    Args:
        ns (str): The namespace to import the FBX file into. Defaults to "targetNamespace".

    Returns:
        None
    """
    current_namespace = cmds.namespaceInfo(cur=True)  # 获取当前激活的名称空间

    if not cmds.namespace(exists=f":{ns}"):  # 如果当前场景中没有参数名称空间
        cmds.namespace(add=f":{ns}")  # 创建参数名称空间

    cmds.namespace(set=f":{ns}")  # 切换到参数名称空间
    # 通过文件对话框获取要导入的文件路径
    pathList = cmds.fileDialog2(fileMode=1, dialogStyle=2, fileFilter=("FBX(*.fbx)"))
    # 如果没有选择文件直接返回
    if not pathList:
        return
    # 导入文件
    cmds.file(
        pathList[0],
        i=True,
        type="FBX",
        ignoreVersion=True,
        ra=True,
        mergeNamespacesOnClash=False,
        namespace=ns,
        options="fbx",
        preserveReferences=True,
        importTimeRange="combine",
    )

    # 返回之前的名称空间
    cmds.namespace(set=current_namespace)


if __name__ == "__main__":
    fbx_import_with_namespace(ns="Ex")
