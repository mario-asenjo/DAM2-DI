# Comentario de "__main__" y __name__:
#
# if __name__ == "__main__":
#    si yo llamo desde la consola o entrada -> lo reconoce y discriminamos el contenido de 
#                        la clase donde lo pongamos haciendo lo que haya dentro del if 
#                        directamente.
#    si importo esta clase desde otro sitio este if da false, por lo que no se ejecutará lo
#                       que haya dentro.

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
import sys

def main():
    """
    PUNTO DE ENTRADA PRINCIPAL DE LA APLICACIÓN
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()