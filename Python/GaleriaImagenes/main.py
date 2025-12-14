import sys

from PySide6.QtWidgets import QApplication
from app.galeria_app import GaleriaApp

def main() -> None:
    """
    Punto de entrada del programa, inicia la ventana con el carousel,
    la principal y la lanza.
    :return:
    """
    app = QApplication(sys.argv)
    galeria = GaleriaApp()
    galeria.window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
