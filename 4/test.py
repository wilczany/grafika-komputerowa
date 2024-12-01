import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Create labels
        self.label1 = QLabel("Label 1")
        self.label2 = QLabel("Label 2")
        
        # Create toggle button
        self.toggle_button = QPushButton("Toggle Labels")
        self.toggle_button.clicked.connect(self.toggle_labels)
        
        # Track label visibility state
        self.labels_visible = True
    
    def toggle_labels(self):
        # Toggle visibility
        self.label1.setVisible(not self.label1.isVisible())
        self.label2.setVisible(not self.label2.isVisible())
        
        # Optionally update button text
        self.labels_visible = not self.labels_visible
        self.toggle_button.setText("Show Labels" if not self.labels_visible else "Hide Labels")


app = QApplication(sys.argv)
window = MyWindow()
window.show()
