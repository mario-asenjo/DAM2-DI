# ui/vistas/carta_view.py
from __future__ import annotations
from typing import Optional, Tuple

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QWidget, QStackedLayout, QLabel

Pos = Tuple[int, int]

class CartaView(QWidget):
    """
    Carta visual con dos caras en un QStackedLayout:
    - índice 0: reverso (pixmap del dorso)
    - índice 1: anverso (pixmap del valor)
    Emite señal 'clicked' con su posición cuando el usuario hace clic.
    """

    clicked = Signal(tuple)  # (fila, col)

    def __init__(self, pos: Pos, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.pos = pos

        self.stack = QStackedLayout(self)
        self.stack.setContentsMargins(0, 0, 0, 0)
        self.stack.setSpacing(0)

        # --- Reverso ---
        self.lbl_reverso = QLabel(self)
        self.lbl_reverso.setAlignment(Qt.AlignCenter)
        self.lbl_reverso.setScaledContents(True)  # que el QLabel escale el pixmap

        # --- Anverso ---
        self.lbl_anverso = QLabel(self)
        self.lbl_anverso.setAlignment(Qt.AlignCenter)
        self.lbl_anverso.setScaledContents(True)

        self.stack.addWidget(self.lbl_reverso)  # idx 0
        self.stack.addWidget(self.lbl_anverso)  # idx 1
        self.stack.setCurrentIndex(0)

        self.setMinimumSize(72, 72)

        self._emparejada = False

    # --------- API pública ---------

    def set_pixmap_reverso(self, pm: QPixmap) -> None:
        self.lbl_reverso.setPixmap(pm)

    def mostrar_reverso(self) -> None:
        if not self._emparejada:
            self.stack.setCurrentIndex(0)

    def mostrar_anverso_pixmap(self, pm: QPixmap) -> None:
        self.lbl_anverso.setPixmap(pm)
        self.stack.setCurrentIndex(1)

    def marcar_emparejada(self) -> None:
        self._emparejada = True
        self.setEnabled(False)

    # --------- Eventos Qt ---------

    def mouseReleaseEvent(self, ev) -> None:  # type: ignore[override]
        if ev.button() == Qt.LeftButton and not self._emparejada:
            self.clicked.emit(self.pos)
        super().mouseReleaseEvent(ev)
