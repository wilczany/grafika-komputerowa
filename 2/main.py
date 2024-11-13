from PySide6.QtWidgets import QApplication
import sys

from window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = MainWindow()
    viewer.show()
    sys.exit(app.exec())