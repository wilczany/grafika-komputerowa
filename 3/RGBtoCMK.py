from PySide6.QtGui import QColor

from PySide6.QtWidgets import QWidget

import layout

from ColorPreview import ColorPreview


class RGBtoCMYK(QWidget):
	
	def __init__(self):
		super().__init__()
		self.cmyk_color_display = ColorPreview()
		layout.do_RGB_layout(self)
		self.color = QColor(0,0,0)

	def updateColor(self):
		r = self.red['slider'].value()
		g = self.green['slider'].value()
		b = self.blue['slider'].value()
	
		r_ = r / 255
		g_ = g / 255
		b_ = b / 255
	
		k = 1 - max(r_, g_, b_)
  
		if k == 1:
			c = m = y = 0
		else:
			c = (1 - r_ - k) / (1 - k)
			m = (1 - g_ - k) / (1 - k)
			y = (1 - b_ - k) / (1 - k)
   
		self.color = QColor.fromCmykF(c, m, y, k)
		
		self.cmyk_color_display.setColor(self.color)
  
		self.cmyk_values = [c, m, y, k]
		self.cmyk_values_text.setText(f"C: {c:.2%} M: {m:.2%} Y: {y:.2%} K: {k:.2%}")
		
  