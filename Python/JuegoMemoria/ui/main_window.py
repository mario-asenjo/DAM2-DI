# ui/main_window.py
from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QDockWidget,
    QTextEdit,
    QMessageBox,
)

class MainWindow(QMainWindow):
    """
    Ventana base reutilizable (shell):
    - Menú Archivo (Nueva partida, Preferencias, Salir)
    - Menú Ver (Mostrar/Ocultar registro)
    - Menú Ayuda (Acerca de)
    - Barra de estado para mensajes breves
    - Dock inferior con registro (QTextEdit de solo lectura)
    - Slot central para inyectar la vista principal del proyecto
    - Señales propias para desacoplar acciones de la lógica
    """

    # Señales propias → las escuchará “quien coordine” (controller)
    nueva_partida_solicitada = Signal()
    preferencias_solicitadas = Signal()
    salir_solicitado = Signal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Esqueleto Qt • Juego de Memoria")
        self.resize(900, 700)

        # --- Barra de estado (feedback rápido abajo) ---
        self.statusBar().showMessage("Listo", 2000)

        # --- Dock de registro (logs) ---
        self._dock_registro = QDockWidget("Registro", self)
        self._dock_registro.setObjectName("dock_registro")
        self._dock_registro.setAllowedAreas(Qt.BottomDockWidgetArea | Qt.RightDockWidgetArea)

        self._txt_registro = QTextEdit(self._dock_registro)
        self._txt_registro.setReadOnly(True)
        self._dock_registro.setWidget(self._txt_registro)

        self.addDockWidget(Qt.BottomDockWidgetArea, self._dock_registro)

        # --- Zona central vacía (ya lista para tu vista) ---
        # De momento no ponemos nada; se inyectará con set_central_view(...)
        self._central_view: Optional[QWidget] = None

        # --- Menús y acciones ---
        self._crear_acciones()
        self._crear_menus()
        self._wiring_acciones()

    # ================== API pública reusable ==================

    def set_central_view(self, widget: QWidget) -> None:
        """
        Inyecta la vista principal (p. ej. un tablero).
        Si había otra, Qt la destruye al perder parent (por ser central).
        """
        self._central_view = widget
        self.setCentralWidget(widget)
        self.log("Vista central actualizada.")

    def log(self, mensaje: str) -> None:
        """
        Añade una línea al registro y muestra un flash en la barra de estado.
        """
        self._txt_registro.append(mensaje)
        self.statusBar().showMessage(mensaje, 2500)

    # ================== Wiring interno ==================

    def _crear_acciones(self) -> None:
        # Archivo
        self.act_nueva = QAction("Nueva partida", self)
        self.act_nueva.setShortcut(QKeySequence.New)  # Ctrl+N / Cmd+N
        self.act_nueva.setStatusTip("Comenzar una nueva partida")

        self.act_preferencias = QAction("Preferencias…", self)
        # Atajo estándar de “Preferencias”
        self.act_preferencias.setShortcut(QKeySequence.StandardKey.Preferences)
        self.act_preferencias.setStatusTip("Abrir preferencias de la aplicación")

        self.act_salir = QAction("Salir", self)
        self.act_salir.setShortcut(QKeySequence.Quit)  # Ctrl+Q / Cmd+Q
        self.act_salir.setStatusTip("Cerrar la aplicación")

        # Ver
        self.act_toggle_registro = self._dock_registro.toggleViewAction()
        self.act_toggle_registro.setText("Mostrar registro")

        # Ayuda
        self.act_acerca = QAction("Acerca de…", self)

    def _crear_menus(self) -> None:
        menu_archivo = self.menuBar().addMenu("&Archivo")
        menu_archivo.addAction(self.act_nueva)
        menu_archivo.addSeparator()
        menu_archivo.addAction(self.act_preferencias)
        menu_archivo.addSeparator()
        menu_archivo.addAction(self.act_salir)

        menu_ver = self.menuBar().addMenu("&Ver")
        menu_ver.addAction(self.act_toggle_registro)

        menu_ayuda = self.menuBar().addMenu("A&yuda")
        menu_ayuda.addAction(self.act_acerca)

    def _wiring_acciones(self) -> None:
        # Conecta acciones de menú a señales propias (desacople)
        self.act_nueva.triggered.connect(self.nueva_partida_solicitada.emit)
        self.act_preferencias.triggered.connect(self.preferencias_solicitadas.emit)
        self.act_salir.triggered.connect(self._on_salir)

        self.act_acerca.triggered.connect(self._on_acerca)

    # ================== Slots internos ==================

    def _on_acerca(self) -> None:
        QMessageBox.about(
            self,
            "Acerca de",
            "<b>Juego de Memoria</b><br>"
            "Esqueleto PySide6 reutilizable con menú, estado y registro.",
        )

    def _on_salir(self) -> None:
        """
        Emite señal de salida (para que el 'controller' pueda guardar estado, etc.).
        Si nadie la maneja, cierra por defecto.
        """
        self.salir_solicitado.emit()
        self.close()

    # Limpieza delicada al cerrar (p. ej. confirmar)
    def closeEvent(self, event) -> None:  # type: ignore[override]
        # Aquí podríamos pedir confirmación, o dejar que el controller decida
        # mostrando un diálogo antes. Mantengo cierre directo:
        super().closeEvent(event)
