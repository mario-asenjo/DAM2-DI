from pathlib import Path

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice
import sys

class MiApp(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_file = QFile("saludo.ui")
        loader = QUiLoader()
        self.ui = loader.load(ui_file, self)
        self.ui.show()
        self.btn = self.ui.findChild(QPushButton, "pushButton")
        self.btn.clicked.connect(self.mostrar_saludo)

    def mostrar_saludo(self):
        print("¡Hola! Has hecho click en el botón.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MiApp()
    sys.exit(app.exec_())