from layout import do_main_layout

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
	
	def __init__(self):
		super().__init__()
		do_main_layout(self)
		self.color = QColor(0,0,0)	

	