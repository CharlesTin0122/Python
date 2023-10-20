import unreal
import sys
from functools import partial  # if you want to include args with UI method calls
from PySide2 import QtUiTools, QtWidgets

"""
Be sure to add your default python modules directory path to Unreal:
Project Settings -> Python -> Additional Paths

Default location of installed modules:
C:\\Users\\[USER]]\\AppData\Local\\Programs\\Python\\[PYTHON VERSION]\\Lib\site-packages

This code required PySide2 module which may need to be installed.
To install required modules open windows command prompt and enter:
pip install [MODULENAME]
"""


class UnrealUITemplate(QtWidgets.QWidget):
    """
    Create a default tool window.
    """

    # store ref to window to prevent garbage collection
    window = None

    def __init__(self, parent=None):
        """
        Import UI and connect components
        """
        super(UnrealUITemplate, self).__init__(parent)

        # load the created UI widget
        self.widgetPath = "C:\\"
        self.widget = QtUiTools.QUiLoader().load(
            self.widgetPath + "mainWidget.ui"
        )  # path to PyQt .ui file

        # attach the widget to the instance of this class (aka self)
        self.widget.setParent(self)

        # find interactive elements of UI
        self.btn_close = self.widget.findChild(QtWidgets.QPushButton, "btn_close")

        # assign clicked handler to buttons
        self.btn_close.clicked.connect(self.closewindow)

    """
    Your code goes here.
    """

    def resizeEvent(self, event):
        """
        Called on automatically generated resize event
        """
        self.widget.resize(self.width(), self.height())

    def closewindow(self):
        """
        Close the window.
        """
        self.destroy()


def openWindow():
    """
    Create tool window.
    """
    if QtWidgets.QApplication.instance():
        # Id any current instances of tool and destroy
        for win in QtWidgets.QApplication.allWindows():
            if "toolWindow" in win.objectName():  # update this name to match name below
                win.destroy()
    else:
        QtWidgets.QApplication(sys.argv)

    # load UI into QApp instance
    UnrealUITemplate.window = UnrealUITemplate()
    UnrealUITemplate.window.show()
    UnrealUITemplate.window.setObjectName(
        "toolWindow"
    )  # update this with something unique to your tool
    UnrealUITemplate.window.setWindowTitle("Sample Tool")
    unreal.parent_external_window_to_slate(UnrealUITemplate.window.winId())


openWindow()
