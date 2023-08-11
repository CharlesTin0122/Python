# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'overlapper.ui'
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
            Form.setObjectName("Form")
        Form.resize(300, 317)
        Form.setMinimumSize(QSize(0, 300))
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName("label")
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.Softness_SP = QDoubleSpinBox(Form)
        self.Softness_SP.setObjectName("Softness_SP")
        self.Softness_SP.setMinimum(-999.000000000000000)
        self.Softness_SP.setMaximum(999.000000000000000)
        self.Softness_SP.setSingleStep(0.100000000000000)
        self.Softness_SP.setValue(3.000000000000000)

        self.horizontalLayout.addWidget(self.Softness_SP)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.Scale_SP = QDoubleSpinBox(Form)
        self.Scale_SP.setObjectName("Scale_SP")
        self.Scale_SP.setMinimum(-999.000000000000000)
        self.Scale_SP.setMaximum(999.000000000000000)
        self.Scale_SP.setSingleStep(0.100000000000000)
        self.Scale_SP.setValue(1.000000000000000)

        self.horizontalLayout_2.addWidget(self.Scale_SP)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.Wind_CB = QGroupBox(Form)
        self.Wind_CB.setObjectName("Wind_CB")
        self.Wind_CB.setAlignment(Qt.AlignCenter)
        self.Wind_CB.setFlat(False)
        self.Wind_CB.setCheckable(True)
        self.Wind_CB.setChecked(False)
        self.verticalLayout_3 = QVBoxLayout(self.Wind_CB)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QLabel(self.Wind_CB)
        self.label_4.setObjectName("label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label_4)

        self.Wind_Scale_SP = QDoubleSpinBox(self.Wind_CB)
        self.Wind_Scale_SP.setObjectName("Wind_Scale_SP")
        self.Wind_Scale_SP.setMinimum(-999.000000000000000)
        self.Wind_Scale_SP.setMaximum(999.000000000000000)
        self.Wind_Scale_SP.setSingleStep(0.100000000000000)
        self.Wind_Scale_SP.setValue(1.000000000000000)

        self.horizontalLayout_5.addWidget(self.Wind_Scale_SP)

        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_5 = QLabel(self.Wind_CB)
        self.label_5.setObjectName("label_5")
        self.label_5.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_6.addWidget(self.label_5)

        self.Wind_Speed_SP = QDoubleSpinBox(self.Wind_CB)
        self.Wind_Speed_SP.setObjectName("Wind_Speed_SP")
        self.Wind_Speed_SP.setMinimum(-999.000000000000000)
        self.Wind_Speed_SP.setMaximum(999.000000000000000)
        self.Wind_Speed_SP.setSingleStep(0.100000000000000)
        self.Wind_Speed_SP.setValue(1.000000000000000)

        self.horizontalLayout_6.addWidget(self.Wind_Speed_SP)

        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.verticalLayout.addWidget(self.Wind_CB)

        self.verticalGroupBox_2 = QGroupBox(Form)
        self.verticalGroupBox_2.setObjectName("verticalGroupBox_2")
        self.verticalGroupBox_2.setAlignment(Qt.AlignCenter)
        self.verticalGroupBox_2.setFlat(False)
        self.verticalGroupBox_2.setCheckable(False)
        self.verticalGroupBox_2.setChecked(False)
        self.verticalLayout_4 = QVBoxLayout(self.verticalGroupBox_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.First_CB = QCheckBox(self.verticalGroupBox_2)
        self.First_CB.setObjectName("First_CB")

        self.verticalLayout_4.addWidget(self.First_CB)

        self.Translate_CB = QCheckBox(self.verticalGroupBox_2)
        self.Translate_CB.setObjectName("Translate_CB")

        self.verticalLayout_4.addWidget(self.Translate_CB)

        self.Hierarchy_CB = QCheckBox(self.verticalGroupBox_2)
        self.Hierarchy_CB.setObjectName("Hierarchy_CB")

        self.verticalLayout_4.addWidget(self.Hierarchy_CB)

        self.Cycle_CB = QCheckBox(self.verticalGroupBox_2)
        self.Cycle_CB.setObjectName("Cycle_CB")

        self.verticalLayout_4.addWidget(self.Cycle_CB)

        self.Bake_CB = QCheckBox(self.verticalGroupBox_2)
        self.Bake_CB.setObjectName("Bake_CB")

        self.verticalLayout_4.addWidget(self.Bake_CB)

        self.verticalLayout.addWidget(self.verticalGroupBox_2)

        self.Overlap_BTN = QPushButton(Form)
        self.Overlap_BTN.setObjectName("Overlap_BTN")

        self.verticalLayout.addWidget(self.Overlap_BTN)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", "Overlapper 1.2 ", None))
        self.label.setText(QCoreApplication.translate("Form", "Softness", None))
        self.label_2.setText(QCoreApplication.translate("Form", "Scale", None))
        self.Wind_CB.setTitle(QCoreApplication.translate("Form", "Wind", None))
        self.label_4.setText(QCoreApplication.translate("Form", "Scale", None))
        self.label_5.setText(QCoreApplication.translate("Form", "Speed", None))
        self.verticalGroupBox_2.setTitle(
            QCoreApplication.translate("Form", "Option", None)
        )
        self.First_CB.setText(
            QCoreApplication.translate("Form", "Dont't use first controls", None)
        )
        self.Translate_CB.setText(
            QCoreApplication.translate("Form", "Add translate", None)
        )
        self.Hierarchy_CB.setText(QCoreApplication.translate("Form", "Hierarchy", None))
        self.Cycle_CB.setText(QCoreApplication.translate("Form", "Cycle", None))
        self.Bake_CB.setText(
            QCoreApplication.translate("Form", "Bake on anim layer", None)
        )
        self.Overlap_BTN.setText(QCoreApplication.translate("Form", "Overlap", None))

    # retranslateUi
