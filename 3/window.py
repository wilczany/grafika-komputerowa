from PySide6.QtGui import QColor
from PySide6.QtWidgets import QMainWindow

import layout

class MainWindow(QMainWindow):
	
	def __init__(self):
		super().__init__()
		layout.do_main_layout(self)
		self.color = QColor(0,0,0)	

	