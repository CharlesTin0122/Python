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
    scene_name = pm.sceneName()
    clipboard = QtWidgets.QApplication.clipboard()
    clipboard.setText(scene_name)
