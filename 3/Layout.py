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

def do_RGB_layout(window: RGBtoCMYK):
    main_layout = QVBoxLayout()
    pallete_layout = QHBoxLayout()

    colors = ["red", "green", "blue"]

    for c in colors:
        setattr(
            window,c,
            dict(
                [
                    ("slider", QSlider(Qt.Horizontal)),
                    ("spin", QSpinBox()),
                    ("label", QLabel(c.capitalize() + ":")),
                ]
            ),
        )

        getattr(window, c)["slider"].setRange(0, 255)
        getattr(window, c)["spin"].setRange(0, 255)

        # Connect slider and spinbox to each other
        getattr(window, c)["slider"].valueChanged.connect(
            getattr(window, c)["spin"].setValue
        )
        getattr(window, c)["spin"].valueChanged.connect(
            getattr(window, c)["slider"].setValue
        )

        # Update color when slider is moved
        getattr(window, c)["slider"].valueChanged.connect(window.updateColor)

        pallete_layout.addWidget(getattr(window, c)["label"])
        pallete_layout.addWidget(getattr(window, c)["slider"])
        pallete_layout.addWidget(getattr(window, c)["spin"])
    # end of loop

    # CMYK Color Labels and display

    window.cmyk_values = []

    cmyk_outer_layout = QVBoxLayout()
    cmyk_layout = QHBoxLayout()
    cmyk_label = QLabel("CMYK:")
    window.cmyk_values_text = QLabel()

    cmyk_layout.addWidget(cmyk_label)
    cmyk_layout.addWidget(window.cmyk_values_text)
    cmyk_outer_layout.addLayout(cmyk_layout)
    cmyk_outer_layout.addWidget(window.cmyk_color_display)

    main_layout.addLayout(pallete_layout)
    main_layout.addLayout(cmyk_outer_layout)

    window.setLayout(main_layout)

def do_CMK_layout(window: CMYKtoRGB):

    main_layout = QVBoxLayout()
    pallette_layout = QHBoxLayout()
    
    colors = ["cyan", "magenta", "yellow", "black"]

    for c in colors:
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

        getattr(window, c)["slider"].setRange(0, 100)
        getattr(window, c)["spin"].setRange(0, 100)

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
    
    # end of loop
    
    # RGB Color Labels and display
    
    window.rgb_values = []
    
    rgb_outer_layout = QVBoxLayout()
    rgb_layout = QHBoxLayout()
    rgb_label = QLabel("RGB:")
    window.rgb_values_text = QLabel()
    
    rgb_layout.addWidget(rgb_label)
    rgb_layout.addWidget(window.rgb_values_text)
    rgb_outer_layout.addLayout(rgb_layout)
    rgb_outer_layout.addWidget(window.rgb_color_display)
    
    main_layout.addLayout(pallette_layout)
    main_layout.addLayout(rgb_outer_layout)
    
    window.setLayout(main_layout)
    
    