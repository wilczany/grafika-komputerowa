from PySide6.QtWidgets import QWidget

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPainter, QPen, QColor
from shape import Shape

class DrawingArea(QWidget):
    def __init__(self):
        super().__init__()
        self.shapes = []
        self.current_shape = None
        self.drawing = False
        self.current_tool = "line"
        self.selected_shape = None
        self.last_mouse_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            point = event.position().toPoint()
            
            # Sprawdzanie czy kliknięto w uchwyt do zmiany rozmiaru
            if self.selected_shape:
                handles = self.selected_shape.get_resize_handles()
                for i, handle in enumerate(handles):
                    if (point - handle).manhattanLength() < 10:
                        self.selected_shape.resizing = True
                        self.selected_shape.resize_handle = i
                        return

            # Sprawdzanie czy kliknięto w istniejący kształt
            for shape in reversed(self.shapes):
                if shape.contains_point(point):
                    self.selected_shape = shape
                    shape.selected = True
                    shape.moving = True
                    self.last_mouse_pos = point
                    self.update()
                    return

            # Rozpoczęcie rysowania nowego kształtu
            self.drawing = True
            self.current_shape = Shape(self.current_tool, [point])
            if self.selected_shape:
                self.selected_shape.selected = False
                self.selected_shape = None

    def mouseMoveEvent(self, event):
        # rysowanie
        if self.drawing and self.current_shape:
            if len(self.current_shape.points) == 1:
                self.current_shape.points.append(event.position().toPoint())
            else:
                self.current_shape.points[-1] = event.position().toPoint()
            self.update()
        # przesuwanie 
        elif self.selected_shape and self.selected_shape.moving:
            delta = event.position().toPoint() - self.last_mouse_pos
            for i in range(len(self.selected_shape.points)):
                self.selected_shape.points[i] += delta
            self.last_mouse_pos = event.position().toPoint()
            self.update()
        # zmiana rozmiaru
        elif self.selected_shape and self.selected_shape.resizing:
            if self.selected_shape.shape_type == "line":
                self.selected_shape.points[self.selected_shape.resize_handle] = event.position().toPoint()
            elif self.selected_shape.shape_type == "rectangle":
                handle_index = self.selected_shape.resize_handle
                if handle_index is not None:
                    points = self.selected_shape.points
                    if handle_index == 0:  # Lewy górny
                        points[0] = event.position().toPoint()
                    elif handle_index == 1:  # Prawy górny
                        points[0] = QPoint(points[0].x(), event.position().toPoint().y())
                        points[1] = QPoint(event.position().toPoint().x(), points[1].y())
                    elif handle_index == 2:  # Lewy dolny
                        points[0] = QPoint(event.position().toPoint().x(), points[0].y())
                        points[1] = QPoint(points[1].x(), event.position().toPoint().y())
                    elif handle_index == 3:  # Prawy dolny
                        points[1] = event.position().toPoint()
            elif self.selected_shape.shape_type == "circle":
                self.selected_shape.points[1] = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.drawing and self.current_shape:
                self.shapes.append(self.current_shape)
                self.current_shape = None
                self.drawing = False
            elif self.selected_shape:
                self.selected_shape.moving = False
                self.selected_shape.resizing = False
                self.selected_shape.resize_handle = None
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Rysowanie wszystkich kształtów
        for shape in self.shapes:
            if shape.selected:
                pen = QPen(QColor(255, 0, 0))
            else:
                pen = QPen(QColor(0, 0, 0))
            painter.setPen(pen)

            if shape.shape_type == "line" and len(shape.points) >= 2:
                painter.drawLine(shape.points[0], shape.points[1])
            elif shape.shape_type == "rectangle" and len(shape.points) >= 2:
                painter.drawRect(shape.get_rect())
            elif shape.shape_type == "circle" and len(shape.points) >= 2:
                center = shape.points[0]
                radius = shape.calculate_radius()
                painter.drawEllipse(center, radius, radius)

            # Rysowanie uchwytów do zmiany rozmiaru dla zaznaczonego kształtu
            if shape.selected:
                handles = shape.get_resize_handles()
                for handle in handles:
                    painter.fillRect(handle.x() - 4, handle.y() - 4, 8, 8, Qt.blue)

        # Rysowanie aktualnie tworzonego kształtu
        if self.current_shape and len(self.current_shape.points) > 0:
            painter.setPen(QPen(QColor(0, 0, 255)))
            if self.current_shape.shape_type == "line" and len(self.current_shape.points) >= 2:
                painter.drawLine(self.current_shape.points[0], self.current_shape.points[1])
            elif self.current_shape.shape_type == "rectangle" and len(self.current_shape.points) >= 2:
                painter.drawRect(self.current_shape.get_rect())
            elif self.current_shape.shape_type == "circle" and len(self.current_shape.points) >= 2:
                center = self.current_shape.points[0]
                radius = self.current_shape.calculate_radius()
                painter.drawEllipse(center, radius, radius)
