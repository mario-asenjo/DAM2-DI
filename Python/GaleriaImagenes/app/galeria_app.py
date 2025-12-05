from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtGui import QAction
from PySide6.QtPrintSupport import QPrintDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QLabel, QListWidget, QWidget, QDialog, QDialogButtonBox, QMessageBox

from datos.datos_galeria import UI_DIR, EXTENSIONES


class GaleriaApp:
    """
    App mínima que carga los archivos .ui en runtime (QUiLoader) y conecta señales a stubs.
    Mantiene referencias a widgets encontrados vía objectName.
    """
    def __init__(self) -> None:
        self.loader = QUiLoader()

        # Cargamos la ventana principal
        self.window: QMainWindow = self._load_ui(UI_DIR / "ventana_principal.ui")
        self.window.setWindowTitle("Galería Imagenes Mario Asenjo 2 DAM")

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

        # Validamos la importación de la UI
        self._verificar_importaciones()

        # Configura el carousel, lógica que en el ui no está
        self._configurar_carousel()

        # Conectamos las señales de momento a stubs
        self._conectar_signals()

    def _verificar_importaciones(self) -> None:
        for nombre, objeto in {
            "label_main": self.label_main,
            "list_thumbnails": self.list_thumbnails,
            "accion_abrir_carpeta": self.accion_abrir_carpeta,
            "accion_imprimir": self.accion_imprimir,
            "accion_salir": self.accion_salir,
            "accion_acerca_de": self.accion_acerca_de
        }.items():
            if objeto is None:
                QMessageBox.warning(self.window, "Error", f"No se ha encontrado '{nombre}' en ventana_principal.ui")

    def _load_ui(self, path: Path) -> QDialog | QMainWindow:
        archivo: QFile = QFile(str(path))
        if not archivo.open(QIODevice.OpenModeFlag.ReadOnly):
            raise RuntimeError(f"No se pudo abrir el .ui -> {path}")
        widget: QMainWindow | QWidget = self.loader.load(archivo, None) # al no tener parent -> toplevel a nivel de UI
        archivo.close()
        if widget is None:
            raise RuntimeError(f"QUiLoader.load() ha devuelto None!!")
        return widget

    def _configurar_carousel(self) -> None:
        # Como en el Designer no he confirado nada más el tamaño de cada icono y cada celda,
        # aquí se configura el funcionamiento del carousel como tal
        self.list_thumbnails.setViewMode(QListWidget.ViewMode.IconMode)
        self.list_thumbnails.setFlow(QListWidget.Flow.LeftToRight)
        self.list_thumbnails.setMovement(QListWidget.Movement.Static)
        self.list_thumbnails.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.list_thumbnails.setSelectionMode(QListWidget.SelectionMode.SingleSelection)

    def _listar_carpeta_imagenes(self, directorio: Path) -> list[Path]:
        archivos: list[Path] = []
        try:
            for path in sorted(directorio.iterdir()):
                if path.is_file() and path.suffix.lower() in EXTENSIONES:
                    archivos.append(path)
        except Exception as e:
            QMessageBox.warning(self.window, "Error", f"No se pudo leer la carpeta: \n{e}")
        return archivos

    def _poblar_tumbnails(self) -> None:
        pass

    def _mostrar_imagen(self, indice: int) -> None:
        pass

    def _actualizar_estado(self) -> None:
        pass

    def on_abrir_carpeta(self) -> None:
        self.window.statusBar().showMessage("Abrir carpeta ...", 2000)

    def on_imprimir_imagen(self) -> None:
        # Realmente no vamos a imprimir dice Luis, así que solo mostramos el dialogo de impresion.
        dialogo_impresion: QPrintDialog = QPrintDialog(self.window)
        dialogo_impresion.exec()

    def on_acerca_de(self) -> None:
        dialogo_acerca: QDialog = self._load_ui(UI_DIR / "about_dialog.ui")
        button_box: QDialogButtonBox = dialogo_acerca.findChild(QDialogButtonBox, "buttonBox")
        if button_box:
            button_box.rejected.connect(dialogo_acerca.reject)

        # Rellenamos los labels
        nombre: QLabel = dialogo_acerca.findChild(QLabel, "nombre_app_label")
        autor: QLabel = dialogo_acerca.findChild(QLabel, "autor_label")
        info: QLabel = dialogo_acerca.findChild(QLabel, "info_app_label")
        if nombre: nombre.setText("Galería de Imágenes - v1.0")
        if autor: autor.setText("Autor: Mario Asenjo Pérez - 2º DAM - UAX")
        if info: info.setText("Proyecto de práctica con PySide6 y Designer de Widgets.\nRepositorio en: https://github.com/mario-asenjo/DAM2-DI/tree/main/Python/GaleriaImagenes .")

        # Hacemos que el dialogo sea modal
        dialogo_acerca.setModal(True)
        dialogo_acerca.exec()

    def on_cambio_de_tumbnail(self, row: int):
        if row < 0:
            return
        self.window.statusBar().showMessage(f"Seleccionaste miniatura ${row}", 1500)

    def _conectar_signals(self) -> None:
        # Menú
        self.accion_abrir_carpeta.triggered.connect(self.on_abrir_carpeta)
        self.accion_imprimir.triggered.connect(self.on_imprimir_imagen)
        self.accion_salir.triggered.connect(self.window.close)
        self.accion_acerca_de.triggered.connect(self.on_acerca_de)

        # Carousel
        self.list_thumbnails.currentRowChanged.connect(self.on_cambio_de_tumbnail)