import sys

from Window import MainWindow
from PySide6.QtWidgets import QApplication


# Używająć srodowiska wayladn należy wyeksportować zmienną środowiskową:
# export QT_QPA_PLATFORM=xcb

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

