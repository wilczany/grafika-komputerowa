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
    QDialog,
)

from PySide6.QtCore import Qt

from Transform import Transformations
from Quality import QualityEnchance
from ImageView import ImageViewer
from PySide6.QtWidgets import QFormLayout, QRadioButton, QButtonGroup


def do_main_layout(window: QMainWindow):

    window.setWindowTitle("Color Converter")
    window.setFixedSize(1200, 800)

    tab_widget = QTabWidget()
    tab_widget.addTab(Transformations(), "Przekształcenia punktowe")
    tab_widget.addTab(QualityEnchance(), "Polepszenie jakości")
    window.setCentralWidget(tab_widget)


def do_transformation_layout(window: QWidget):
    main_layout = QHBoxLayout()

    # Create a toolbar
    toolbar = QWidget()
    toolbar_layout = QVBoxLayout(toolbar)

    # wczytywanie obrazu
    load_button = QPushButton("Wczytaj obraz")
    load_button.clicked.connect(window.load_image)
    toolbar_layout.addWidget(load_button)
    
    buttons_form_layout = QFormLayout()
    colors_form_layout = QFormLayout()
    window.button_group = QButtonGroup(window)

    operations = [
        "Dodawanie",
        "Odejmowanie", 
        "Mnożenie", 
        "Dzielenie",
        "Zmiana jasności"
    ]

    for name in operations:
        radio_button = QRadioButton(name)
        window.button_group.addButton(radio_button)
        buttons_form_layout.addRow(radio_button)

    execute_button = QPushButton("Wykonaj operację")
    execute_button.clicked.connect(
        lambda: window.transform() if window.button_group.checkedButton() else None
    )
    
    

    for color in ["Red", "Green", "Blue", "Brightness"]:
        spin_box = QSpinBox()
        spin_box.setRange(0, 255)
        label = QLabel(color)
        colors_form_layout.addWidget(label)
        colors_form_layout.addWidget(spin_box)
        setattr(window, f"{color.lower()}_spin", spin_box)
        setattr(window, f"{color.lower()}_label", label)
    window.brightness_spin.hide()
    window.brightness_label.hide()
    
    toolbar_layout.addLayout(buttons_form_layout)
    toolbar_layout.addLayout(colors_form_layout)
    toolbar_layout.addWidget(execute_button)

    get_values_button = QPushButton("Get RGB Values")
    get_values_button.clicked.connect(lambda: print(window.get_rgb_values()))
    toolbar_layout.addWidget(get_values_button)
    main_layout.addWidget(toolbar)
    
    image_panel = QWidget()
  
    main_layout.addWidget(image_panel)
    window.image_viewer = ImageViewer()
    main_layout.addWidget(window.image_viewer)
    window.setLayout(main_layout)
    
    def update_spin_boxes():
        fields = ["Red", "Green", "Blue"]
        if window.button_group.checkedButton().text() == "Zmiana jasności":
            for field in fields:
                getattr(window, f"{field.lower()}_spin").hide()
                getattr(window, f"{field.lower()}_label").hide()
            window.brightness_spin.show()
            window.brightness_label.setVisible(True)
        else:
            for field in fields:
                getattr(window, f"{field.lower()}_spin").show()
                getattr(window, f"{field.lower()}_label").show()
            window.brightness_spin.hide()
            window.brightness_label.setVisible(False)

    window.button_group.buttonClicked.connect(update_spin_boxes)


def do_quality_layout(window: QWidget):
    layout = QVBoxLayout()

    label = QLabel("Jakość")
    layout.addWidget(label)


# def do_dialog_layout(window: QDialog):
#     main_layout = QVBoxLayout()

#     input_layout = QHBoxLayout()
#     colors = ["red", "green", "blue"]

#     for color in colors:
#         sub_layout = QVBoxLayout()
#         setattr(window, f"{color}_spin", QSpinBox(Qt.Horizontal))
#         slider = getattr(window, f"{color}_spin")
#         slider.setRange(0, 255)
#         sub_layout.addWidget(QLabel(color + ":"))
#         sub_layout.addWidget(slider)

#     main_layout.addLayout(input_layout)

#     ok_button = QPushButton("OK")
#     ok_button.clicked.connect(window.accept)

#     main_layout.addWidget(ok_button)

#     window.setLayout(main_layout)
