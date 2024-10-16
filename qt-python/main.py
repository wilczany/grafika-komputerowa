import sys
from PySide6.QtWidgets import (
    QGraphicsScene,
    QGraphicsView,
    QApplication,
    QGraphicsItem,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    )
from PySide6.QtCore import Qt, QPoint, QRect
from PySide6.QtGui import QPen, QPainter, QPixmap
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(0,0,800,200)
        self.pix = QPixmap(self.rect().size())

        vbox = QVBoxLayout()

        line_button = QPushButton( "/" )
        vbox.addWidget(line_button)

        rect_button = QPushButton( "□" )
        vbox.addWidget(rect_button)

        elipse_button = QPushButton( "○" )
        vbox.addWidget(elipse_button)

        view = QGraphicsView(self.scene)
        view.setFixedSize(1000, 800)
        view.setRenderHint(QPainter.Antialiasing)

        hbox = QHBoxLayout(self)
        hbox.addLayout(vbox)
        hbox.addWidget(view)

        self.setLayout(hbox)


        
        self.begin, self.destination = QPoint(), QPoint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(QPoint(),self.pix)

        if not self.begin.isNull() and not self.destination.isNull():
            rect = QRect(self.begin, self.destination)
            # rect.setFlags(Qt.ItemIsMovable)
            painter.drawRect(rect.normalized())
    
    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.destination = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.destination = event.pos()
        self.update()
    
    def mouseReleaseEvent(self, event):

        rect = QRect(self.begin, self.destination)
        painter = QPainter(self.pix)
        painter.drawRect(rect.normalized())

# app = QApplication(sys.argv)

# # Defining a scene rect of 400x200, with it's origin at 0,0.
# # If we don't set this on creation, we can set it later with .setSceneRect
# scene = QGraphicsScene(0, 0, 800, 200)

# rect = scene.addRect(0, 0, 100, 100)
# rect.setBrush(Qt.red)

# pen = QPen(Qt.cyan)
# pen.setWidth(3)
# rect.setPen(pen)

# rect.setFlag(QGraphicsItem.ItemIsMovable)

# view = QGraphicsView(scene)
# view.setFixedSize(1000, 800)


app = QApplication(sys.argv)
w = Window()
w.show()
app.exec()
