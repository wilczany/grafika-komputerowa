from PySide6.QtGui import QColor, QPainter, QBrush
from PySide6.QtWidgets import QWidget

class ColorPreview(QWidget):
    def __init__(self):
        super().__init__()
        self.color = QColor(0, 0, 0)
        self.setMinimumSize(100, 100)

    def setColor(self, color):
        self.color = color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QBrush(self.color))
