from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor


import Layout

class QualityEnchance(QWidget):
    
    def __init__(self):
        super().__init__()
        Layout.do_quality_layout(self)
        self.color = QColor(0,0,0)