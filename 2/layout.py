from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QSpinBox,
)

from PySide6.QtCore import Qt
from image_viewer_widget import ImageViewerWidget

def do_main_layout(window):
        window.setWindowTitle("Image Viewer")
        window.setMinimumSize(800, 600)
        
        # Main widget and layout
        main_widget = QWidget()
        window.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        # image viewer
        window.image_viewer = ImageViewerWidget()

        # Buttons
        window.load_button = QPushButton("Load Image")
        window.save_button = QPushButton("Save as JPEG")
        window.zoom_in_button = QPushButton("Zoom In")
        window.zoom_out_button = QPushButton("Zoom Out")
        
        # JPEG compression quality spinner
        window.quality_label = QLabel("JPEG Quality:")
        window.quality_spinner = QSpinBox()
        window.quality_spinner.setRange(1, 100)
        window.quality_spinner.setValue(85)
        
        # Add widgets to toolbar
        toolbar.addWidget(window.load_button)
        toolbar.addWidget(window.save_button)
        toolbar.addWidget(window.zoom_in_button)
        toolbar.addWidget(window.zoom_out_button)
        toolbar.addWidget(window.quality_label)
        toolbar.addWidget(window.quality_spinner)
        toolbar.addStretch()
        
        # Image viewer
        window.image_viewer = ImageViewerWidget()
        
        # Add layouts to main layout
        layout.addLayout(toolbar)
        layout.addWidget(window.image_viewer)
        
        # Connect signals
        window.load_button.clicked.connect(window.load_image)
        window.save_button.clicked.connect(window.save_image)
        window.zoom_in_button.clicked.connect(window.image_viewer.zoom_in)
        window.zoom_out_button.clicked.connect(window.image_viewer.zoom_out)
        
