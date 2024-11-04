from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QGroupBox,
)

from drawing import DrawingArea


def do_main_layout(window):
    window.setWindowTitle("Program do rysowania")
    window.setGeometry(100, 100, 1000, 800)
    window.setFixedSize(1000, 800)

    # Główny widget i układ
    main_widget = QWidget()
    window.setCentralWidget(main_widget)
    main_layout = QHBoxLayout(main_widget)

    # Lewy panel narzędzi
    left_panel = QWidget()
    left_panel.setFixedWidth(150)
    left_layout = QVBoxLayout(left_panel)

    # Grupy narzędzi
    tools_group = QGroupBox("Narzędzia")
    tools_layout = QVBoxLayout()

    # Przyciski ksształtów
    window.line_button = QPushButton("/")
    window.rectangle_button = QPushButton("□")
    window.circle_button = QPushButton("○")

    tools_layout.addWidget(window.line_button)
    tools_layout.addWidget(window.rectangle_button)
    tools_layout.addWidget(window.circle_button)
    tools_group.setLayout(tools_layout)

    # Grupa do zmiany rozmiaru
    edit_group = QGroupBox("Zmiana rozmiaru")
    edit_layout = QFormLayout()

    window.param_change_1 = QLineEdit()
    window.param_change_2 = QLineEdit()

    edit_layout.addRow(QLabel("X:"), window.param_change_1)
    edit_layout.addRow(QLabel("Y:"), window.param_change_2)

    window.edit_button = QPushButton("Zastosuj")
    edit_layout.addRow(window.edit_button)

    edit_group.setLayout(edit_layout)

    # Grupa do tworzenia
    create_group = QGroupBox("Nowy kształt")
    create_layout = QFormLayout()

    window.param_create_1x = QLineEdit()
    window.param_create_1y = QLineEdit()
    window.param_create_2x = QLineEdit()
    window.param_create_2y = QLineEdit()

    create_layout.addRow(QLabel("X1:"), window.param_create_1x)
    create_layout.addRow(QLabel("Y1:"), window.param_create_1y)
    create_layout.addRow(QLabel("X2:"), window.param_create_2x)
    create_layout.addRow(QLabel("Y2:"), window.param_create_2y)

    window.create_button = QPushButton("Utwórz")
    create_layout.addRow(window.create_button)

    create_group.setLayout(create_layout)

    # Grupa operacji na plikach
    file_group = QGroupBox("Operacje na pliku")
    file_layout = QVBoxLayout()
    window.save_button = QPushButton("Zapisz")
    window.load_button = QPushButton("Wczytaj")

    file_layout.addWidget(window.save_button)
    file_layout.addWidget(window.load_button)
    file_group.setLayout(file_layout)

    window.clear_button = QPushButton("Wyczyść")

    # Dodawanie grup do lewego panelu
    left_layout.addWidget(tools_group)
    left_layout.addWidget(create_group)
    left_layout.addWidget(edit_group)
    left_layout.addWidget(file_group)
    left_layout.addStretch()
    left_layout.addWidget(window.clear_button)

    # Obszar rysowania
    right_panel = QWidget()
    right_layout = QVBoxLayout(right_panel)
    window.drawing_area = DrawingArea()
    right_layout.addWidget(window.drawing_area)

    # Dodawanie paneli do głównego układu
    main_layout.addWidget(left_panel)
    main_layout.addWidget(
        right_panel, stretch=1
    )  # stretch=1 pozwala na rozciąganie obszaru rysowania

    # Podłączanie sygnałów
    window.line_button.clicked.connect(lambda: window.set_tool("line"))
    window.rectangle_button.clicked.connect(lambda: window.set_tool("rectangle"))
    window.circle_button.clicked.connect(lambda: window.set_tool("circle"))
    window.edit_button.clicked.connect(window.edit_shape)
    window.create_button.clicked.connect(window.create_shape)
    window.save_button.clicked.connect(window.save_shapes)
    window.load_button.clicked.connect(window.load_shapes)
    window.clear_button.clicked.connect(window.clear)
