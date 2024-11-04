from PySide6.QtWidgets import QMainWindow, QFileDialog
from PySide6.QtCore import QPoint

import json


from shape import Shape
from layouts import do_main_layout


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        do_main_layout(self)

    def set_tool(self, tool):
        self.drawing_area.current_tool = tool

    def edit_shape(self):
        if self.drawing_area.selected_shape:
            try:
                x = float(self.param_change_1.text())
                y = float(self.param_change_2.text())

                shape = self.drawing_area.selected_shape
                shape.points[1] = QPoint(
                    shape.points[0].x() + int(x), shape.points[0].y() + int(y)
                )

                self.drawing_area.update()
            except ValueError:
                print("Nieprawidłowe wartości parametrów")
                pass
            
    def create_shape(self):
        try:
            x1 = int(self.param_create_1x.text())
            y1 = int(self.param_create_1y.text())
            x2 = int(self.param_create_2x.text())
            y2 = int(self.param_create_2y.text())

            shape = Shape(self.drawing_area.current_tool, [QPoint(x1, y1), QPoint(x2, y2)])
            self.drawing_area.shapes.append(shape)
            self.drawing_area.update()
        except ValueError:
            print("Nieprawidłowe wartości parametrów")

    def save_shapes(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Zapisz kształty", "", "JSON files (*.json)"
        )
        if filename:
            if not filename.endswith('.json'):
                filename += '.json'
            shapes_data = [shape.to_dict() for shape in self.drawing_area.shapes]
            with open(filename, "w") as f:
                json.dump(shapes_data, f)

    def load_shapes(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Wczytaj kształty", "", "JSON files (*.json)"
        )
        if filename:
            with open(filename, "r") as f:
                shapes_data = json.load(f)
                self.clear()
                self.drawing_area.shapes = [
                    Shape.from_dict(data) for data in shapes_data]
                
                self.drawing_area.update()

    def clear(self):
        self.drawing_area.shapes = []
        self.drawing_area.update()
