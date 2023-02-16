from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class FunWeight(QWidget):
	
	def __init__(self):
		QWidget.__init__(self)
		layout = QVBoxLayout()
		self.setLayout(layout)

		from_layout = QFormLayout()
		layout.addLayout(from_layout)

		button_layout = QHBoxLayout()
		apply_button = QPushButton('apply')
		close_button = QPushButton("close")
		button_layout.addWidget(apply_button)
		button_layout.addWidget(close_button)
		layout.addLayout(button_layout)

app = QApplication([])
window = FunWeight
window.show()
app.exec_()