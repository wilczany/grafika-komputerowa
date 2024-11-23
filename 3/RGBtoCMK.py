from layout import do_RGB_layout

class RGBtoCMYK(QWidget):
	
	def __init__(self):
		do_RGB_layout(self)
		self.color = QColor(0,0,0)


