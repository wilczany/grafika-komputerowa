
from PySide6.QtWidgets import QMainWindow, QTabWidget
from RGBtoCMK import RGBtoCMYK
from CMYKtoRGB import CMYKtoRGB

def do_main_layout(window: QMainWindow):

	
	window.setWindowTitle("Color Converter")
	window.setFixedSize(800, 200)
	
	tab_widget = QTabWidget()
	tab_widget.addTab(CMYKtoRGB(), "CMYK to RGB")
	tab_widget.addTab(RGBtoCMYK(), "RGB to CMYK")
	
def do_CMK_layout(window: CMYKtoRGB):
	window.setWindowTitle("CMK Converter")
	window.setFixedSize(800, 200)

def do_RGB_layout(window: RGBtoCMYK):
	window.setWindowTitle("RGB Converter")
	window.setFixedSize(800, 200)
