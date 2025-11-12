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
from app.event_bus import EventBus
from app.puente_ui_window import UIBridge
from app.juego_controller import JuegoController
from ui.recursos import ImageProvider
from ui.vista.tablero_view import TableroView
import sys

def main():
    """
    PUNTO DE ENTRADA PRINCIPAL DE LA APLICACIÓN
    """
    app = QApplication(sys.argv)

    bus = EventBus()
    window = MainWindow()

    window.bridge = UIBridge(window, bus)
    window.controller = JuegoController(bus, parent=window)

    provider = ImageProvider()
    tablero = TableroView(bus, provider, parent=window)
    window.set_central_view(tablero)   # ← una sola vez

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()