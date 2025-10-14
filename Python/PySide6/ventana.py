from PySide6.QtWidgets import QMainWindow, QLabel

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración básica de la ventana
        self.setWindowTitle("Mi primera ventana con PySide6")
        self.setGeometry(100, 100, 400, 200)

        # Creamos un QLabel (widget de texto)
        etiqueta = QLabel("¡Hola Mundo con PySide6!", self)
        etiqueta.move(120, 80)  # Posición dentro de la ventana