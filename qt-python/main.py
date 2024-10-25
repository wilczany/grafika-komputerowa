from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLineEdit, QLabel, QFileDialog, QGroupBox)
from PySide6.QtCore import QPoint

import json
import sys

from shape import Shape
from drawing import DrawingArea

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Program do rysowania")
        self.setGeometry(100, 100, 1000, 800)
        self.setFixedSize(1000, 800)
        
        # Główny widget i układ
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget) 

        # Lewy panel narzędzi
        left_panel = QWidget()
        left_panel.setFixedWidth(150)  
        left_layout = QVBoxLayout(left_panel)

        # Grupa narzędzi
        tools_group = QGroupBox("Narzędzia")
        tools_layout = QVBoxLayout()
        
        # Przyciski narzędzi
        self.line_button = QPushButton("/")
        self.rectangle_button = QPushButton("□")
        self.circle_button = QPushButton("○")
        
        tools_layout.addWidget(self.line_button)
        tools_layout.addWidget(self.rectangle_button)
        tools_layout.addWidget(self.circle_button)
        tools_group.setLayout(tools_layout)
        
        # Grupa parametrów
        params_group = QGroupBox("Zmiana rozmaiaru")
        params_layout = QVBoxLayout()
        
        param1_container = QHBoxLayout()
        self.param1_label = QLabel("X:")
        self.param1_input = QLineEdit()
        param1_container.addWidget(self.param1_label)
        param1_container.addWidget(self.param1_input)
        
        param2_container = QHBoxLayout()
        self.param2_label = QLabel("Y:")
        self.param2_input = QLineEdit()
        param2_container.addWidget(self.param2_label)
        param2_container.addWidget(self.param2_input)
        
        self.apply_button = QPushButton("Zastosuj")
        
        params_layout.addLayout(param1_container)
        params_layout.addLayout(param2_container)
        params_layout.addWidget(self.apply_button)
        params_group.setLayout(params_layout)

        # Grupa operacji na plikach
        file_group = QGroupBox("Operacje na pliku")
        file_layout = QVBoxLayout()
        self.save_button = QPushButton("Zapisz")
        self.load_button = QPushButton("Wczytaj")
        
        file_layout.addWidget(self.save_button)
        file_layout.addWidget(self.load_button)
        file_group.setLayout(file_layout)

        # Dodawanie grup do lewego panelu
        left_layout.addWidget(tools_group)
        left_layout.addWidget(params_group)
        left_layout.addWidget(file_group)
        left_layout.addStretch()  

        # Obszar rysowania
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        self.drawing_area = DrawingArea()
        right_layout.addWidget(self.drawing_area)

        # Dodawanie paneli do głównego układu
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, stretch=1)  # stretch=1 pozwala na rozciąganie obszaru rysowania

        # Podłączanie sygnałów
        self.line_button.clicked.connect(lambda: self.set_tool("line"))
        self.rectangle_button.clicked.connect(lambda: self.set_tool("rectangle"))
        self.circle_button.clicked.connect(lambda: self.set_tool("circle"))
        self.apply_button.clicked.connect(self.edit_shape)
        self.save_button.clicked.connect(self.save_shapes)
        self.load_button.clicked.connect(self.load_shapes)

    def set_tool(self, tool):
        self.drawing_area.current_tool = tool

    def edit_shape(self):
        if self.drawing_area.selected_shape:
            try:
                x = float(self.param1_input.text())
                y = float(self.param2_input.text())
                
                shape = self.drawing_area.selected_shape
                shape.points[1] = QPoint(
                    shape.points[0].x() + int(x),
                    shape.points[0].y() + int(y)
                )
                
                self.drawing_area.update()
            except ValueError:
                print("Nieprawidłowe wartości parametrów")
                pass
    

    def save_shapes(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Zapisz kształty", "", "JSON files (*.json)")
        if filename:
            shapes_data = [shape.to_dict() for shape in self.drawing_area.shapes]
            with open(filename, 'w') as f:
                json.dump(shapes_data, f)

    def load_shapes(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Wczytaj kształty", "", "JSON files (*.json)")
        if filename:
            with open(filename, 'r') as f:
                shapes_data = json.load(f)
                self.drawing_area.shapes = [Shape.from_dict(data) for data in shapes_data]
                self.drawing_area.update()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

main()