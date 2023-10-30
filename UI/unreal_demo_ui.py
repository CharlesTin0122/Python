# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'unreal_demo.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(233, 105)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pb_print_actors = QPushButton(Form)
        self.pb_print_actors.setObjectName(u"pb_print_actors")

        self.verticalLayout.addWidget(self.pb_print_actors)

        self.pb_close = QPushButton(Form)
        self.pb_close.setObjectName(u"pb_close")

        self.verticalLayout.addWidget(self.pb_close)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pb_print_actors.setText(QCoreApplication.translate("Form", u"Print Actors", None))
        self.pb_close.setText(QCoreApplication.translate("Form", u"Close", None))
    # retranslateUi

