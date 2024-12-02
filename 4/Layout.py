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
    QComboBox
)

from PySide6.QtCore import Qt

from Transform import Transformations
from Quality import QualityEnhance
from ImageView import ImageViewer
from PySide6.QtWidgets import QFormLayout, QRadioButton, QButtonGroup


def do_main_layout(window: QMainWindow):

    window.setWindowTitle("Color Converter")
    window.setFixedSize(1200, 800)

    tab_widget = QTabWidget()
    tab_widget.addTab(Transformations(), "Przekształcenia punktowe")
    tab_widget.addTab(QualityEnhance(), "Polepszenie jakości")
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
    
    window.brightness_spin.setRange(-255, 255)
    window.brightness_spin.hide()
    window.brightness_label.hide()
    
    toolbar_layout.addLayout(buttons_form_layout)
    colors_form_layout.addWidget(execute_button)
    toolbar_layout.addLayout(colors_form_layout)

    
    image_panel = QWidget()

    
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

    grayscale_layout = QVBoxLayout()

    window.grayscale_combo = QComboBox()
    window.grayscale_combo.addItems(["Średnia arytmetyczna", "Model yuv"])
    grayscale_layout.addWidget(QLabel("Metoda skali szarości:"))
    grayscale_layout.addWidget(window.grayscale_combo)
    
    grayscale_btn = QPushButton("Konwertuj do skali szarości")
    grayscale_btn.clicked.connect(window.convert_to_grayscale)
    grayscale_layout.addWidget(grayscale_btn)
    toolbar_layout.addLayout(grayscale_layout)
    main_layout.addWidget(toolbar)

    main_layout.addWidget(image_panel)
    window.image_viewer = ImageViewer()
    main_layout.addWidget(window.image_viewer)
    window.setLayout(main_layout)


def do_quality_layout(window: QWidget):
    window.setWindowTitle('Image Filters')
    window.layout = QVBoxLayout()
    
    window.original_view = ImageViewer()
    window.filtered_view = ImageViewer()
    
    window.image_layout = QHBoxLayout()
    window.image_layout.addWidget(window.original_view)
    window.image_layout.addWidget(window.filtered_view)
    

    filter_buttons = [
        ('Filtr uśredniający', 'mean'),
        ('Filtra medianowy', 'median'),
        ('Filtr wykrywania krawędzi', 'sobel'),
        ('Filtr wyostrzający', 'sharpen'),
        ('Rozmycie Gaussa', 'gaussian')
    ]
    
    window.btn_layout = QHBoxLayout()
    load_image_button = QPushButton('Wczytaj obraz')
    load_image_button.clicked.connect(window.load_image)

    window.btn_layout.addWidget(load_image_button)

    for btn_text, filter_type in filter_buttons:
        btn = QPushButton(btn_text)
        window.btn_layout.addWidget(btn)
        
        btn.clicked.connect(lambda checked, ft=filter_type: window.apply_filter(ft))
    
    window.layout.addLayout(window.image_layout)
    window.layout.addLayout(window.btn_layout)
    window.setLayout(window.layout)
