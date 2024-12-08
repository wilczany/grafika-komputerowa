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
    # Create central widget and main layout
    # central_widget = QWidget()
    # window.setCentralWidget(central_widget)
    main_layout = QVBoxLayout(window)
    
    # Create image viewer
    window.image_viewer = ImageViewer()
    window.image_viewer.setMinimumSize(600, 400)
    main_layout.addWidget(window.image_viewer)
    
    # Create button layout
    button_layout = QHBoxLayout()
    main_layout.addLayout(button_layout)
    
    # Create buttons
    load_button = QPushButton("Load Image")
    normalize_button = QPushButton("Normalize Histogram")
    equalize_button = QPushButton("Equalize Histogram")
    reset_button = QPushButton("Reset Image")
    
    # Add buttons to layout
    button_layout.addWidget(load_button)
    button_layout.addWidget(normalize_button)
    button_layout.addWidget(equalize_button)
    button_layout.addWidget(reset_button)
    
    # Connect buttons to their respective functions
    load_button.clicked.connect(window.load_image)
    normalize_button.clicked.connect(window.normalize_histogram)
    equalize_button.clicked.connect(window.equalize_histogram)
    reset_button.clicked.connect(window.reset_image)
    
    # Set window properties
    window.setWindowTitle("Image Histogram Processing")
    window.setMinimumSize(800, 600)

def do_binarization_layout(window):
    main_layout = QVBoxLayout(window)
    
    # Add image viewer
    window.image_viewer.setMinimumSize(600, 400)
    main_layout.addWidget(window.image_viewer)
    
    # Create controls layout
    controls_layout = QHBoxLayout()
    main_layout.addLayout(controls_layout)
    
    # Create method selection combo box
    method_combo = QComboBox()
    method_combo.addItems([
        "Manual Threshold",
        "Percent Black Selection",
        "Mean Iterative Selection"
    ])
    controls_layout.addWidget(QLabel("Method:"))
    controls_layout.addWidget(method_combo)
    
    # Create threshold slider and spin box
    threshold_container = QWidget()
    threshold_layout = QHBoxLayout(threshold_container)
    threshold_slider = QSlider(Qt.Horizontal)
    threshold_slider.setRange(0, 255)
    threshold_slider.setValue(127)
    threshold_spin = QSpinBox()
    threshold_spin.setRange(0, 255)
    threshold_spin.setValue(127)
    threshold_layout.addWidget(QLabel("Threshold:"))
    threshold_layout.addWidget(threshold_slider)
    threshold_layout.addWidget(threshold_spin)
    controls_layout.addWidget(threshold_container)
    
    # Create percent slider and spin box
    percent_container = QWidget()
    percent_layout = QHBoxLayout(percent_container)
    percent_slider = QSlider(Qt.Horizontal)
    percent_slider.setRange(0, 100)
    percent_slider.setValue(50)
    percent_spin = QSpinBox()
    percent_spin.setRange(0, 100)
    percent_spin.setValue(50)
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
    
    # Handle method change
    def on_method_changed(index):
        threshold_container.setVisible(index == 0)  # Manual Threshold
        percent_container.setVisible(index == 1)    # Percent Black Selection
        # Mean Iterative Selection needs no controls
    
    method_combo.currentIndexChanged.connect(on_method_changed)
    
    # Initial visibility
    on_method_changed(0)
    
    # Connect buttons
    load_button.clicked.connect(window.load_image)
    
    def on_apply():
        method = method_combo.currentIndex()
        if method == 0:
            window.manual_threshold(threshold_spin.value())
        elif method == 1:
            window.percent_black_selection(percent_spin.value())
        elif method == 2:
            window.mean_iterative_selection()
    
    apply_button.clicked.connect(on_apply)
    reset_button.clicked.connect(lambda: window.display_image(window.original_image))

