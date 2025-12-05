import sys

from PySide6.QtWidgets import QApplication
from app.galeria_app import GaleriaApp

def main() -> None:
    app = QApplication(sys.argv)
    galeria = GaleriaApp()
    galeria.window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
