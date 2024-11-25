from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSlider,
    QSpinBox,
)

from PySide6.QtCore import Qt
from RGBtoCMK import RGBtoCMYK
from CMYKtoRGB import CMYKtoRGB
from Cube import CubeWidget

def do_main_layout(window: QMainWindow):

    window.setWindowTitle("Color Converter")
    window.setFixedSize(800, 600)

    tab_widget = QTabWidget()
    tab_widget.addTab(RGBtoCMYK(), "RGB to CMYK")
    tab_widget.addTab(CMYKtoRGB(), "CMYK to RGB")
    tab_widget.addTab(CubeWidget(), "RGB Cube")
    window.setCentralWidget(tab_widget)

def do_color_layout(window, colors, range, color_label_text, color_display):
    window.main_layout = QVBoxLayout()

    pallette_layout = get_pallette(window, colors, range)

    outer_layout = QVBoxLayout()
    inner_layout = QHBoxLayout()
    color_label = QLabel(color_label_text)
    window.color_values_text = QLabel()

    inner_layout.addWidget(color_label)
    inner_layout.addWidget(window.color_values_text)
    outer_layout.addLayout(inner_layout)
    outer_layout.addWidget(color_display)

    window.main_layout.addLayout(pallette_layout)
    window.main_layout.addLayout(outer_layout)

    window.setLayout(window.main_layout)

def do_RGB_layout(window: RGBtoCMYK):
    do_color_layout(window, ["red", "green", "blue"], 255, "CMYK:", window.cmyk_color_display)

def do_CMK_layout(window: CMYKtoRGB):
    do_color_layout(window, ["cyan", "magenta", "yellow", "black"], 100, "RGB:", window.rgb_color_display)
    

def get_pallette(window, colors_array, range):
        
    pallette_layout = QHBoxLayout()
    for c in colors_array:
        setattr(
            window, c,
            dict(
                [
                    ("slider", QSlider(Qt.Horizontal)),
                    ("spin", QSpinBox()),
                    ("label", QLabel(c.capitalize() + ":")),
                ]
            ),
        )

        getattr(window, c)["slider"].setRange(0, range)
        getattr(window, c)["spin"].setRange(0, range)

        # Connect slider and spinbox to each other
        getattr(window, c)["slider"].valueChanged.connect(
            getattr(window, c)["spin"].setValue
        )
        getattr(window, c)["spin"].valueChanged.connect(
            getattr(window, c)["slider"].setValue
        )

        # Update color when slider is moved
        getattr(window, c)["slider"].valueChanged.connect(window.updateColor)

        pallette_layout.addWidget(getattr(window, c)["label"])
        pallette_layout.addWidget(getattr(window, c)["slider"])
        pallette_layout.addWidget(getattr(window, c)["spin"])

    return pallette_layout