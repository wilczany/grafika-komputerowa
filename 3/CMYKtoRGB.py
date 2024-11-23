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
	
		self.rgb_values = [r, g, b]
		self.rgb_values_text.setText(f"R: {round(r,2)} G: {round(g,2)} B: {round(b,2)}")
	
		
		self.rgb_values_text.adjustSize()
	
		self.rgb_values_text.move(
			self.rgb_values_text.parent().width() // 2 - self.rgb_values_text.width() // 2,
			self.rgb_values_text.parent().height() // 2 - self.rgb_values_text.height() // 2,
		)
	
		self.rgb_values_text.show()
	
		self.rgb_color_display