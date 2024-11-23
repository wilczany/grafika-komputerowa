from layout import do_CMK_layout

class CMYKtoRGB(QWidget):
	
	def __init__(self):
		do_CMK_layout(self)
		self.color = QColor(0,0,0)