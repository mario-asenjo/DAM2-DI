"""
Aplicación PySide6 con arquitectura de capas
Archivo principal de ejecución
"""
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    """
    PUNTO DE ENTRADA PRINCIPAL DE LA APLICACIÓN
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())