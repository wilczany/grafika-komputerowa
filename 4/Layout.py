from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSlider,
    QSpinBox,
    QPushButton,
    QWidget,
    QDialog
)

from PySide6.QtCore import Qt

from Transform import Transformations
from Quality import QualityEnchance
from ImageView import ImageViewerWidget

def do_main_layout(window: QMainWindow):

    window.setWindowTitle("Color Converter")
    window.setFixedSize(800, 600)

    tab_widget = QTabWidget()
    tab_widget.addTab(Transformations(), "Przekształcenia punktowe")
    tab_widget.addTab(QualityEnchance(), "Polepszenie jakości")
    window.setCentralWidget(tab_widget)

def do_transformation_layout(window: QWidget):
    main_layout = QVBoxLayout()
    
    # Create a toolbar
    toolbar = QWidget()
    toolbar_layout = QHBoxLayout(toolbar)
    
    # wczytywanie obrazu
    load_button = QPushButton("Wczytaj obraz")
    load_button.clicked.connect(window.load_image)
    toolbar_layout.addWidget(load_button)
    
    operations = [
        ("Dodawanie", window.add_value),
        ("Odejmowanie", window.subtract_value),
        ("Mnożenie", window.multiply_value),
        ("Dzielenie", window.divide_value),
        ("Zmiana jasności", window.change_brightness)
    ]
    for name, func in operations:
        btn = QPushButton(name)
        btn.clicked.connect(func)
        toolbar_layout.addWidget(btn)

    main_layout.addWidget(toolbar)
    image_viewer = ImageViewerWidget()
        
    main_layout.addWidget(image_viewer)
    window.setLayout(main_layout)


def do_quality_layout(window: QWidget):
    layout = QVBoxLayout()

    label = QLabel("Jakość")
    layout.addWidget(label)
    

def do_dialog_layout(window: QDialog):
    main_layout = QVBoxLayout()
    
    input_layout = QHBoxLayout()
    colors = ['red', 'green', 'blue']
    
    for color in colors:
        sub_layout = QVBoxLayout()
        setattr(window, f'{color}_spin', QSpinBox(Qt.Horizontal))
        slider =  getattr(window, f'{color}_spin')
        slider.setRange(0, 255)
        sub_layout.addWidget(QLabel(color+':'))
        sub_layout.addWidget(slider)

    main_layout.addLayout(input_layout)
    
    ok_button = QPushButton('OK')
    ok_button.clicked.connect(window.accept)
    
    main_layout.addWidget(ok_button)

    window.setLayout(main_layout)
    