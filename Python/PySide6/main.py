import sys
from PySide6.QtWidgets import QApplication
from ventana import Ventana

# Punto de entrada principal
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Crea la aplicación Qt
    ventana = Ventana()           # Instancia la ventana
    ventana.show()                # Muestra la interfaz
    sys.exit(app.exec())          # Inicia el bucle de eventos