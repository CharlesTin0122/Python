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
    """该函数用于调用mel2py工具将mel字符串转换为pymel字符串"""
    mel_cmd = pm.scrollField("melcode", q=1, tx=1)  # 读取输入的mel语言字符串
    py_cmd = mel2py.mel2pyStr(mel_cmd, pymelNamespace="pm")  # 将mel字符串转换为pymel字符串
    py_fixed = py_cmd.replace("pymel.all", "pymel.core")  # 修正pymel字符串
    pm.scrollField("pymelcode", e=1, tx=py_fixed)  # 将修正后的字符串写入UI


def mel2py_ui():
    """UI界面编写"""
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


if __name__ == "__main__":
    mel2py_ui()
