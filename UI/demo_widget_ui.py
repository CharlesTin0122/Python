# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'demo_widget.ui'
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
        Form.resize(272, 223)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pb_create = QPushButton(Form)
        self.pb_create.setObjectName(u"pb_create")

        self.horizontalLayout_2.addWidget(self.pb_create)

        self.pb_close = QPushButton(Form)
        self.pb_close.setObjectName(u"pb_close")

        self.horizontalLayout_2.addWidget(self.pb_close)


        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 1, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.comboBox = QComboBox(Form)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.horizontalLayout_3.addWidget(self.comboBox)


        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.rb_sphere = QRadioButton(Form)
        self.buttonGroup = QButtonGroup(Form)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.rb_sphere)
        self.rb_sphere.setObjectName(u"rb_sphere")
        self.rb_sphere.setChecked(True)

        self.horizontalLayout.addWidget(self.rb_sphere)

        self.rb_cube = QRadioButton(Form)
        self.buttonGroup.addButton(self.rb_cube)
        self.rb_cube.setObjectName(u"rb_cube")

        self.horizontalLayout.addWidget(self.rb_cube)

        self.rb_cylinder = QRadioButton(Form)
        self.buttonGroup.addButton(self.rb_cylinder)
        self.rb_cylinder.setObjectName(u"rb_cylinder")

        self.horizontalLayout.addWidget(self.rb_cylinder)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pb_create.setText(QCoreApplication.translate("Form", u"create", None))
        self.pb_close.setText(QCoreApplication.translate("Form", u"Close", None))
        self.label.setText(QCoreApplication.translate("Form", u"select geo", None))
        self.rb_sphere.setText(QCoreApplication.translate("Form", u"sphere", None))
        self.rb_cube.setText(QCoreApplication.translate("Form", u"cube", None))
        self.rb_cylinder.setText(QCoreApplication.translate("Form", u"cylinder", None))
    # retranslateUi

