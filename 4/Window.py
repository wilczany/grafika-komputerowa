from PySide6.QtGui import QColor
from PySide6.QtWidgets import QMainWindow

import Layout

class MainWindow(QMainWindow):
	
	def __init__(self):
		super().__init__()
		Layout.do_main_layout(self)

	