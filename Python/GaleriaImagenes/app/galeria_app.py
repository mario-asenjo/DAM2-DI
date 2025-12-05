from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtGui import QAction
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QLabel, QListWidget, QWidget

from datos.DatosGaleria import UI_DIR

class GaleriaApp:
    """
    App mínima que carga los .ui en runtime (QUiLoader) y conecta señales a stubs.
    Mantiene referencias a widgets encontrados vía objectName.
    """
    def __init__(self) -> None:
        self.loader = QUiLoader()

        # Cargamos la ventana principal
        self.window: QMainWindow = self._load_ui(UI_DIR / "ventana_principal.ui")
        self.window.setWindowTitle("Galería Imagenes Mario Asenjo 2 DAM")

        # Configura el carousel, lógica que en el ui no está
        self._configurar_carousel()

        # Conectamos las señales de momento a stubs
        self._conectar_signals()

        # Lista de imágenes e índice actual de imagen
        self.imagenes: list[Path] = []
        self._indice_actual: int = -1

        # Cargar Widgets y Actions por objectName
            # cargamos los widgets
        self.label_main: QLabel | None = self.window.findChild(QLabel, "lblMain")
        self.list_thumbnails: QListWidget | None = self.window.findChild(QListWidget, "listThumbs")
            # acciones menú archivo
        self.accion_abrir_carpeta: QAction | None = self.window.findChild(QAction, "action_abrirCarpeta")
        self.accion_imprimir: QAction | None = self.window.findChild(QAction, "actionImprimir")
        self.accion_salir: QAction | None = self.window.findChild(QAction, "actionSalir")
            # accion menú acerca de...
        self.accion_acerca_de: QAction | None = self.window.findChild(QAction, "actionAcerca_de")

        self._load_carousel()

    def _load_ui(self, path: Path) -> QWidget | QMainWindow:
        archivo: QFile = QFile(str(path))
        if not archivo.open(QIODevice.OpenModeFlag.ReadOnly):
            raise RuntimeError(f"No se pudo abrir el .ui -> {path}")
        widget: QMainWindow | QWidget = self.loader.load(archivo, None) # al no tener parent -> toplevel a nivel de UI
        archivo.close()
        if widget is None:
            raise RuntimeError(f"QUiLoader.load() ha devuelto None!!")
        return widget

    def _configurar_carousel(self):
        pass

    def _conectar_signals(self):
        pass