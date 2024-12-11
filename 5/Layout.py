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
    QComboBox,
)

from PySide6.QtCore import Qt

from ImageView import ImageViewer
from PySide6.QtWidgets import QFormLayout, QRadioButton, QButtonGroup
from Histogram import Histogram
from Binarization import Binarization


def do_main_layout(window: QMainWindow):

    window.setWindowTitle("Color Converter")
    window.setFixedSize(1200, 800)

    tab_widget = QTabWidget()
    tab_widget.addTab(Histogram(), "Histogram")
    tab_widget.addTab(Binarization(), "Binaryzacja")
    window.setCentralWidget(tab_widget)


def do_histogram_layout(window: QMainWindow):
    main_layout = QVBoxLayout(window)

    window.image_viewer = ImageViewer()
    window.image_viewer.setMinimumSize(600, 400)
    main_layout.addWidget(window.image_viewer)

    button_layout = QHBoxLayout()
    main_layout.addLayout(button_layout)

    load_button = QPushButton("Load Image")
    normalize_button = QPushButton("Normalize Histogram")
    equalize_button = QPushButton("Equalize Histogram")
    reset_button = QPushButton("Reset Image")

    button_layout.addWidget(load_button)
    button_layout.addWidget(normalize_button)
    button_layout.addWidget(equalize_button)
    button_layout.addWidget(reset_button)

    load_button.clicked.connect(window.load_image)
    normalize_button.clicked.connect(window.normalize_histogram)
    equalize_button.clicked.connect(window.equalize_histogram)
    reset_button.clicked.connect(window.reset_image)

    window.setWindowTitle("Image Histogram Processing")
    window.setMinimumSize(800, 600)


def do_binarization_layout(window):
    main_layout = QVBoxLayout(window)

    window.image_viewer.setMinimumSize(600, 400)
    main_layout.addWidget(window.image_viewer)

    controls_layout = QHBoxLayout()
    main_layout.addLayout(controls_layout)

    method_combo = QComboBox()
    method_combo.addItems(
        [
            "Ręczny próg",
            "Procentowa selekcja czarnego",
            "Selekcja iteratywna średniej",
            "Selekcja entropii",
        ]
    )
    controls_layout.addWidget(QLabel("Method:"))
    controls_layout.addWidget(method_combo)

    threshold_container = QWidget()
    threshold_layout = QHBoxLayout(threshold_container)
    threshold_slider = QSlider(Qt.Horizontal)
    threshold_slider.setRange(0, 255)
    threshold_spin = QSpinBox()
    threshold_spin.setRange(0, 255)
    threshold_layout.addWidget(QLabel("Threshold:"))
    threshold_layout.addWidget(threshold_slider)
    threshold_layout.addWidget(threshold_spin)
    controls_layout.addWidget(threshold_container)

    percent_container = QWidget()
    percent_layout = QHBoxLayout(percent_container)
    percent_slider = QSlider(Qt.Horizontal)
    percent_slider.setRange(0, 100)
    percent_spin = QSpinBox()
    percent_spin.setRange(0, 100)
    percent_layout.addWidget(QLabel("Black %:"))
    percent_layout.addWidget(percent_slider)
    percent_layout.addWidget(percent_spin)
    controls_layout.addWidget(percent_container)

    # Create buttons
    button_layout = QHBoxLayout()
    load_button = QPushButton("Load Image")
    apply_button = QPushButton("Apply")
    reset_button = QPushButton("Reset")

    button_layout.addWidget(load_button)
    button_layout.addWidget(apply_button)
    button_layout.addWidget(reset_button)
    main_layout.addLayout(button_layout)

    # Connect signals
    threshold_slider.valueChanged.connect(threshold_spin.setValue)
    threshold_spin.valueChanged.connect(threshold_slider.setValue)
    percent_slider.valueChanged.connect(percent_spin.setValue)
    percent_spin.valueChanged.connect(percent_slider.setValue)

    def on_method_changed(index):
        threshold_container.setVisible(index == 0)
        percent_container.setVisible(index == 1)
        # brak wyświetlania dla innych metod

    method_combo.currentIndexChanged.connect(on_method_changed)

    # Initial visibility
    on_method_changed(0)

    load_button.clicked.connect(window.load_image)

    def on_apply():
        method = method_combo.currentIndex()
        if method == 0:
            window.manual_threshold(threshold_spin.value())
        elif method == 1:
            window.percent_black_selection(percent_spin.value())
        elif method == 2:
            window.mean_iterative_selection()
        elif method == 3:
            window.entropy_selection()

    apply_button.clicked.connect(on_apply)
    reset_button.clicked.connect(lambda: window.reset_image())
