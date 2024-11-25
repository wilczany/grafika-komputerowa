from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor

import Layout 
from ColorPreview import ColorPreview

class CMYKtoRGB(QWidget):
	
	def __init__(self):
		super().__init__()
		self.rgb_color_display = ColorPreview()
		Layout.do_CMK_layout(self)
		self.color = QColor(0,0,0)
  
	def updateColor(self):
		c = self.cyan['slider'].value() / 100
		m = self.magenta['slider'].value() / 100
		y = self.yellow['slider'].value() / 100
		k = self.black['slider'].value() / 100
	
		r = 255 * (1 - c) * (1 - k)
		g = 255 * (1 - m) * (1 - k)
		b = 255 * (1 - y) * (1 - k)
	
		self.color = QColor.fromRgb(r, g, b)
	
		self.rgb_color_display.setColor(self.color)
	
		self.color_values_text.setText(f"R: {round(r,2)} G: {round(g,2)} B: {round(b,2)}")
	
	