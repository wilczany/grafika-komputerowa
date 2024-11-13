from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QFrame,
)

from PySide6.QtCore import Qt


def do_main_layout(window):
    window.setWindowTitle("Projekt2")
    window.setGeometry(100, 100, 800, 600)
    window.setFixedSize(1000, 800)

    # Główny widget i layout
    main_widget = QWidget()
    window.setCentralWidget(main_widget)

    # Horizontal layout for main window
    layout = QHBoxLayout(main_widget)

    # Container widget for buttons with fixed width
    button_container = QWidget()
    button_container.setFixedWidth(200)  # Set fixed width for button panel

    # Vertical layout for buttons on left side
    button_layout = QVBoxLayout(button_container)

    # Przyciski
    window.btn_load_p3 = QPushButton("Wczytaj PPM P3")
    window.btn_load_p6 = QPushButton("Wczytaj PPM P6")
    window.btn_load_p3.clicked.connect(lambda: window.load_ppm("P3"))
    window.btn_load_p6.clicked.connect(lambda: window.load_ppm("P6"))

    # Label na obraz
    window.image_label = QLabel()
    window.image_label.setAlignment(Qt.AlignCenter)

    # Dodanie przycisków do lewego layoutu
    button_layout.addWidget(window.btn_load_p3)
    button_layout.addWidget(window.btn_load_p6)
    button_layout.addStretch()

    # Vertical line separator
    line = QFrame()
    line.setFrameShape(QFrame.VLine)
    line.setFrameShadow(QFrame.Sunken)

    # Dodanie layoutów do głównego layoutu
    layout.addWidget(button_container)
    layout.addWidget(line)
    layout.addWidget(window.image_label)
