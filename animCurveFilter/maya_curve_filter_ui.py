# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'maya_curve_filter.ui'
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
        Form.resize(502, 244)
        self.verticalLayoutWidget = QWidget(Form)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 481, 221))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName("label_6")

        self.gridLayout.addWidget(self.label_6, 4, 2, 1, 1)

        self.label_4 = QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")

        self.gridLayout.addWidget(self.label_4, 2, 2, 1, 1)

        self.label_5 = QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName("label_5")

        self.gridLayout.addWidget(self.label_5, 3, 2, 1, 1)

        self.label_7 = QLabel(self.verticalLayoutWidget)
        self.label_7.setObjectName("label_7")

        self.gridLayout.addWidget(self.label_7, 6, 2, 1, 1)

        self.radioButton = QRadioButton(self.verticalLayoutWidget)
        self.radioButton.setObjectName("radioButton")

        self.gridLayout.addWidget(self.radioButton, 6, 1, 1, 1)

        self.radioButton_2 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_2.setObjectName("radioButton_2")

        self.gridLayout.addWidget(self.radioButton_2, 1, 1, 1, 1)

        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")

        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)

        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")

        self.gridLayout.addWidget(self.label_3, 1, 2, 1, 1)

        self.radioButton_3 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_3.setObjectName("radioButton_3")

        self.gridLayout.addWidget(self.radioButton_3, 4, 1, 1, 1)

        self.radioButton_4 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_4.setObjectName("radioButton_4")

        self.gridLayout.addWidget(self.radioButton_4, 3, 1, 1, 1)

        self.radioButton_5 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_5.setObjectName("radioButton_5")

        self.gridLayout.addWidget(self.radioButton_5, 2, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Maximum, QSizePolicy.Minimum
        )

        self.gridLayout.addItem(self.horizontalSpacer, 2, 0, 1, 1)

        self.label_8 = QLabel(self.verticalLayoutWidget)
        self.label_8.setObjectName("label_8")

        self.gridLayout.addWidget(self.label_8, 0, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Maximum, QSizePolicy.Minimum
        )

        self.gridLayout.addItem(self.horizontalSpacer_2, 3, 3, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalSpacer_3 = QSpacerItem(
            40, 20, QSizePolicy.Maximum, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.lineEdit = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.lineEdit)

        self.horizontalSlider = QSlider(self.verticalLayoutWidget)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(
            self.horizontalSlider.sizePolicy().hasHeightForWidth()
        )
        self.horizontalSlider.setSizePolicy(sizePolicy1)
        self.horizontalSlider.setMaximum(10)
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.horizontalSlider)

        self.pushButton = QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.horizontalSpacer_4 = QSpacerItem(
            40, 20, QSizePolicy.Maximum, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer_4)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", "Form", None))
        self.label_6.setText(
            QCoreApplication.translate("Form", "\u7b80\u5316\u66f2\u7ebf", None)
        )
        self.label_4.setText(
            QCoreApplication.translate(
                "Form", "\u8c03\u6574\u66f2\u7ebf\u632f\u5e45", None
            )
        )
        self.label_5.setText(
            QCoreApplication.translate(
                "Form",
                "\u5ffd\u7565\u4fdd\u6301\u66f2\u7ebf\u7ec6\u8282,\u8fdb\u884c\u5927\u5e45\u5e73\u6ed1",
                None,
            )
        )
        self.label_7.setText(
            QCoreApplication.translate(
                "Form",
                "\u6839\u636e\u524d\u540e\u5e27\u8ba1\u7b97\u63d2\u503c\u4e2d\u95f4\u5e27",
                None,
            )
        )
        self.radioButton.setText(QCoreApplication.translate("Form", "Twinner", None))
        self.radioButton_2.setText(
            QCoreApplication.translate("Form", "Butterworth", None)
        )
        self.label.setText(QCoreApplication.translate("Form", "Filters:", None))
        self.label_3.setText(
            QCoreApplication.translate(
                "Form",
                "\u4fdd\u6301\u66f2\u7ebf\u7ec6\u8282,\u5bf9\u66f2\u7ebf\u8fdb\u884c\u5e73\u6ed1",
                None,
            )
        )
        self.radioButton_3.setText(QCoreApplication.translate("Form", "Simplify", None))
        self.radioButton_4.setText(QCoreApplication.translate("Form", "Smooth", None))
        self.radioButton_5.setText(QCoreApplication.translate("Form", "Dampen", None))
        self.label_8.setText(
            QCoreApplication.translate("Form", "\u529f\u80fd\u63cf\u8ff0:", None)
        )
        self.label_2.setText(QCoreApplication.translate("Form", "Value", None))
        self.pushButton.setText(QCoreApplication.translate("Form", "Rererse", None))

    # retranslateUi
