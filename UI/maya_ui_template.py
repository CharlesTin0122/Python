# -*- coding: utf-8 -*-
'''
@FileName      : maya_UI_Template.py
@DateTime      : 2023/10/20 15:46:47
@Author        : Tian Chao
@Contact       : tianchao0533@163.com
@Software      : Maya 2023.3
@PythonVersion : python 3.9.7
@Description   :
'''
import pymel.core as pm
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtUiTools, QtCore, QtGui, QtWidgets
from functools import partial  # optional, for passing args during signal function calls
import sys


class MayaUITemplate(QtWidgets.QWidget):
    """
    Create a default tool window.
    """
    window = None

    def __init__(self, parent):
        """
        Initialize class.
        """
        # 调用父类的构造函数
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)
        # 引入ui文件
        self.widgetPath = r"G:\Code\Python\UI\demo_widget.ui"
        self.widget = QtUiTools.QUiLoader().load(self.widgetPath)
        # 设置ui文件父对象为当前窗口
        self.widget.setParent(self)
        # 设置构建窗口大小
        self.resize(400, 200)
        # 获取ui部件,findChild方法通过对象的类和名称找到对象
        self.pb_close = self.widget.findChild(QtWidgets.QPushButton, "pb_close")
        self.pb_create = self.widget.findChild(QtWidgets.QPushButton, "pb_create")

        self.rb_sphere = self.widget.findChild(QtWidgets.QRadioButton, "rb_sphere")
        self.rb_cube = self.widget.findChild(QtWidgets.QRadioButton, "rb_cube")
        self.rb_cylinder = self.widget.findChild(QtWidgets.QRadioButton, "rb_cylinder")

        self.combobox = self.widget.findChild(QtWidgets.QComboBox, "comboBox")

        # 为UI部件指定槽函数
        self.pb_close.clicked.connect(self.closeWindow)
        self.pb_create.clicked.connect(self.create_geo)
        self.combobox.currentTextChanged.connect(self.update_selection)

    def resizeEvent(self, event):
        """
        Called on automatically generated resize event
        """
        self.widget.resize(self.width(), self.height())

    def closeWindow(self):
        """
        Close window.
        """
        print("closing window")
        self.destroy()

    def create_geo(self):
        if self.rb_sphere.isChecked():
            mesh_sphere = pm.polySphere()[0]
            self.combobox.addItem(mesh_sphere)
        if self.rb_cylinder.isChecked():
            mesh_cylinder = pm.polyCylinder()[0]
            self.combobox.addItem(mesh_cylinder)
        if self.rb_cube.isChecked():
            mesh_cube = pm.polyCube()
            self.combobox.addItem(mesh_cube)

    def update_selection(self):
        selection = self.combobox.currentText()
        pm.select(selection, replace=True)


def openWindow():
    """
    ID Maya and attach tool window.
    """
    # 检查是否存在QtWidgets.QApplication的实例
    # Maya uses this so it should always return True
    if QtWidgets.QApplication.instance():
        # 查找所有名称为"myToolWindowName"的现有窗口并销毁它们。
        for win in QtWidgets.QApplication.allWindows():
            if "myToolWindowName" in win.objectName():
                win.destroy()

    # QtWidgets.QApplication(sys.argv)

    # 此函数返回主Maya窗口的指针（即mayaMainWindowPtr）。这个指针是一个内存地址的整数值，代表了Maya的主窗口对象。
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()

    # wrapInstance函数将这个整数值转换为一个QtWidgets.QWidget对象（即mayaMainWindow）。
    # wrapInstance函数是shiboken2库中的一个函数，用于将C++对象指针包装成Python对象。
    # 在这里，它将Maya主窗口的指针包装成了一个Qt Widget对象，以便在PySide2中进行操作和使用。
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QtWidgets.QWidget)

    # 用pymel的方法获取主窗口
    # mayaWindow = pm.ui.Window("MayaWindow").asQtObject()

    # MayaUITemplate.window是一个类属性，用于存储和操作MayaUITemplate类的实例对象，
    # 以便在其他地方可以方便地引用和操作自定义UI窗口。
    MayaUITemplate.window = MayaUITemplate(parent=mayaMainWindow)

    # MayaUITemplate.window的对象名称设置为"myToolWindowName"，用于标识目标窗口。
    MayaUITemplate.window.setObjectName("myToolWindowName")
    # 设置MayaUITemplate.window的窗口标题为"Maya UI Template"。
    MayaUITemplate.window.setWindowTitle("Maya UI Template")
    # 显示MayaUITemplate.window
    MayaUITemplate.window.show()


openWindow()
