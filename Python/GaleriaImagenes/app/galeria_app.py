from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QFile, QIODevice, QSize
from PySide6.QtGui import QAction, QPixmap, QIcon, QImage, Qt
from PySide6.QtPrintSupport import QPrintDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (QMainWindow, QLabel, QListWidget, QWidget,
                               QDialog, QDialogButtonBox, QMessageBox, QFileDialog, QListWidgetItem)

from datos.datos_galeria import UI_DIR, EXTENSIONES


class GaleriaApp:
    """
    App mínima que carga los archivos .ui en runtime (QUiLoader) y conecta
    señales a stubs. Mantiene referencias a widgets encontrados vía objectName
    """
    def __init__(self) -> None:
        """
        Genera una ventana con los elementos que hay en los ficheros .ui del
        proyecto, los cuales se han generado usando QtWidgetDesigner.
        """
        self.window: QMainWindow = self._load_ui(
            UI_DIR / "ventana_principal.ui"
        )
        self.window.setWindowTitle("Galería Imagenes Mario Asenjo 2 DAM")
        self._configurar_ventana()
        self.imagenes: list[Path] = []
        self._indice_actual: int = -1
        self._verificar_importaciones()
        self._configurar_carousel()
        self._conectar_signals()

    def _configurar_ventana(self) -> None:
        self.label_main: QLabel | None = self.window.findChild(
            QLabel, "lblMain"
        )
        self.list_thumbnails: QListWidget | None = self.window.findChild(
            QListWidget, "listThumbs"
        )
        self.accion_abrir_carpeta: QAction | None = self.window.findChild(
            QAction, "action_abrirCarpeta"
        )
        self.accion_imprimir: QAction | None = self.window.findChild(
            QAction, "actionImprimir"
        )
        self.accion_salir: QAction | None = self.window.findChild(
            QAction, "actionSalir"
        )
        self.accion_acerca_de: QAction | None = self.window.findChild(
            QAction, "actionAcerca_de"
        )

    def _load_ui(self, path: Path) -> QDialog | QMainWindow:
        """
        Carga desde el path, el fichero ui indicado, para devolver una
        ventana, o un dialogo generado con el designer.
        :param path: Ruta al fichero .ui que contiene el elemento.
        :return:
        """
        loader = QUiLoader()
        archivo: QFile = QFile(str(path))
        try:
            widget: QMainWindow | QWidget = loader.load(archivo, None)
        except FileNotFoundError:
            raise RuntimeError(f"No se pudo abrir el .ui -> {path}")
        if widget is None:
            raise RuntimeError("QUiLoader.load() ha devuelto None!!")
        return widget

    def _verificar_importaciones(self) -> None:
        """
        Verifica que todas las importaciones de los elementos de archivos .ui
        se han cargado correctamente.
        :return:
        """
        for nombre, objeto in {
            "label_main": self.label_main,
            "list_thumbnails": self.list_thumbnails,
            "accion_abrir_carpeta": self.accion_abrir_carpeta,
            "accion_imprimir": self.accion_imprimir,
            "accion_salir": self.accion_salir,
            "accion_acerca_de": self.accion_acerca_de
        }.items():
            if objeto is None:
                QMessageBox.warning(
                    self.window, "Error",
                    f"No se ha encontrado '{nombre}' en ventana_principal.ui"
                )

    def _configurar_carousel(self) -> None:
        """
        Como el designer solo establece la disposición de los elementos, aquí
        definimos el comportamiento de la lista de imágenes (carousel).
        :return:
        """
        self.list_thumbnails.setViewMode(QListWidget.ViewMode.IconMode)
        self.list_thumbnails.setFlow(QListWidget.Flow.LeftToRight)
        self.list_thumbnails.setMovement(QListWidget.Movement.Static)
        self.list_thumbnails.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.list_thumbnails.setSelectionMode(
            QListWidget.SelectionMode.SingleSelection
        )

    def _conectar_signals(self) -> None:
        """
        Conecta todas las señales con sus slots / listeners correspondientes.
        :return:
        """
        self.accion_abrir_carpeta.triggered.connect(self.on_abrir_carpeta)
        self.accion_imprimir.triggered.connect(self.on_imprimir_imagen)
        self.accion_salir.triggered.connect(self.window.close)
        self.accion_acerca_de.triggered.connect(self.on_acerca_de)
        self.list_thumbnails.currentRowChanged.connect(
            self.on_cambio_de_tumbnail
        )

    def _listar_carpeta_imagenes(self, directorio: Path) -> list[Path]:
        """
        Itera el directorio, y si hay archivos con extensión permitida, los
        añade a una lista que va a devolver al final.
        :param directorio: Directorio que hay que iterar.
        :return: Lista de Path de los archivos válidos que haya en el dir.
        """
        archivos: list[Path] = []
        try:
            archivos = sorted(directorio.iterdir())
        except Exception as e:
            QMessageBox.warning(self.window, "Error", f"No se pudo leer "
                                                      f"la carpeta: \n{e}")
            return []
        return [AR for AR in archivos
                if AR.is_file()
                and AR.suffix.lower() in EXTENSIONES]

    def _poblar_tumbnails(self) -> None:
        self.list_thumbnails.clear()
        rutas: list[Path] = []
        for ruta in self.imagenes:
            imagen: QImage = QImage(str(ruta))
            if imagen.isNull(): # imagen no legible, probamos con 1.png vacío.
                continue
            pixmap: QPixmap = QPixmap.fromImage(imagen)
            icono: QIcon = QIcon(pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            item: QListWidgetItem = QListWidgetItem(icono, ruta.name)
            item.setData(Qt.ItemDataRole.UserRole, str(ruta))
            self.list_thumbnails.addItem(item)
            rutas.append(ruta)
        self.imagenes = rutas # dejamos en imagenes solo las que hayamos conseguido cargar.

    def _mostrar_imagen(self, indice: int) -> None:
        if not (0 <= indice < len(self.imagenes)):
            return
        ruta: Path =  self.imagenes[indice]
        pixmap: QPixmap = QPixmap(str(ruta))
        if pixmap.isNull():
            self.window.statusBar().showMessage(f"No se pudo cargar: {ruta.name}", 2000)
            return
        tamaño = self.label_main.contentsRect().size()
        if (tamaño.isEmpty()):
            cw: QWidget = self.window.centralWidget()
            tamaño = (cw.size() if cw is not None else self.window.size())
            if tamaño.isEmpty():
                target = QSize(640, 480)
        pixmap_escalado: QPixmap = pixmap.scaled(tamaño, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.label_main.setPixmap(pixmap_escalado)
        self.label_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._indice_actual = indice
        self._actualizar_estado()


    def _actualizar_estado(self) -> None:
        if 0 <= self._indice_actual < len(self.imagenes):
            self.window.statusBar().showMessage(self.imagenes[self._indice_actual].name)
        else:
            self.window.statusBar().clearMessage()

    def on_abrir_carpeta(self) -> None:
        """
        Slot / Listener para cuando se pulsa abrir carpeta.
        MUestra un QFileDialog para seleccionar carpeta con imagenes.
        Pobla los thumbnails y muestra la primera imagen.
        :return:
        """
        ruta = QFileDialog.getExistingDirectory(self.window, "Selecciona una carpeta con imagenes...")
        if not ruta:
            self.window.statusBar().showMessage("CANCELADO", 1500)
            return
        directorio: Path = Path(ruta)
        self.imagenes: list[Path] = self._listar_carpeta_imagenes(directorio)
        if not self.imagenes:
            QMessageBox.information(self.window, "Sin imagenes", "No se encontraron PNG/JPEG/JPG en la carpeta.")
            self.list_thumbnails.clear()
            self.label_main.setPixmap(QPixmap())
            self.window.statusBar().clearMessage()
            self._indice_actual = -1
            return
        self._poblar_tumbnails()
        self.list_thumbnails.setCurrentRow(0)
        self._mostrar_imagen(0)

    def on_imprimir_imagen(self) -> None:
        """
        Slot / Listener para cuando se pulsa imprimir_imagen. No imprime, pero
        sí muestra el diálogo de impresión.
        :return:
        """
        dialogo_impresion: QPrintDialog = QPrintDialog(self.window)
        dialogo_impresion.exec()

    def on_acerca_de(self) -> None:
        """
        Slot / Listener para cuando se pulsa acerca_de, pobla un diálogo
        cargado de un fichero generado con designer, y lo pobla. Luego
        lo muestra como modal en una nueva ventana emergente.
        :return:
        """
        dialogo_acerca: QDialog = self._load_ui(UI_DIR / "about_dialog.ui")
        button_box: QDialogButtonBox = dialogo_acerca.findChild(
            QDialogButtonBox, "buttonBox"
        )
        if button_box:
            button_box.rejected.connect(dialogo_acerca.reject)
        nombre: QLabel = dialogo_acerca.findChild(QLabel, "nombre_app_label")
        autor: QLabel = dialogo_acerca.findChild(QLabel, "autor_label")
        info: QLabel = dialogo_acerca.findChild(QLabel, "info_app_label")
        if nombre:
            nombre.setText("Galería de Imágenes - v1.0")
        if autor:
            autor.setText("Autor: Mario Asenjo Pérez - 2º DAM - UAX")
        if info:
            info.setText(
                "Proyecto de práctica con PySide6 y Designer de Widgets."
                "\nRepositorio en: https://github.com/mario-asenjo/DAM2-DI"
                "/tree/main/Python/GaleriaImagenes ."
            )
        dialogo_acerca.setModal(True)
        dialogo_acerca.exec()

    def on_cambio_de_tumbnail(self, row: int) -> None:
        """
        Slot / Listener para cuando se seleccione una imágen para cambiar el
        thumbnail.
        :param row: Fila en la cual se encuentra la imagen para posición.
        :return:
        """
        if row < 0:
            return
        self._mostrar_imagen(row)
