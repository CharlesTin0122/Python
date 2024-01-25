# -*- coding: utf-8 -*-
# @FileName :  copy_scensename_to_clipboard.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/5/30 10:08
# @Software : PyCharm
# Description:
import pymel.core as pm
from PySide2 import QtWidgets


def copy_name():
    scene_path = pm.sceneName()
    scene_name = scene_path.split("/")[-1].split(".")[0]
    clipboard = QtWidgets.QApplication.clipboard()
    if scene_name:
        clipboard.setText(scene_name)
        pm.inViewMessage(
            amg="ScenceName copied to clipboard",
            alpha=0.5,
            dragKill=True,
            pos="midCenterTop",
            fade=True,
        )
    else:
        pm.inViewMessage(
            amg="ScenceName not found",
            alpha=0.5,
            dragKill=True,
            pos="midCenterTop",
            fade=True,
        )


if __name__ == "__main__":
    copy_name()
