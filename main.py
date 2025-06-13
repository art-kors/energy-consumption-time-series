import sys
from sys import argv

from library.ui.app import App
from PySide6.QtWidgets import QApplication


def main():
    app = QApplication(argv)
    window = App()
    window.resize(350, 250)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
