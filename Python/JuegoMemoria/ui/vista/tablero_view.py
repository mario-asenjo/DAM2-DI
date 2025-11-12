# ui/vistas/tablero_view.py
from __future__ import annotations
from typing import Dict, Tuple, Optional

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QGridLayout

from app.event_bus import EventBus
from app.eventos import (
    CartaClicadaIntent,
    TableroCreadoEvt,
    CartaMostradaEvt,
    AciertoEvt,
    FalloEvt,
    PartidaTerminadaEvt,
)
from ui.recursos.image_provider import ImageProvider
from .carta_view import CartaView

Pos = Tuple[int, int]

class TableroView(QWidget):
    """
    Vista del tablero: grid N×N de CartaView.
    Pide pixmaps al ImageProvider para anverso/reverso.
    """

    def __init__(self, bus: EventBus, provider: ImageProvider, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.bus = bus
        self.provider = provider

        self._n: Optional[int] = None
        self._grid = QGridLayout(self)
        self._grid.setSpacing(8)
        self._grid.setContentsMargins(8, 8, 8, 8)

        self._cartas: Dict[Pos, CartaView] = {}
        self._subs: list[tuple[type, callable]] = []

        # Subs
        self._sub(TableroCreadoEvt, self._on_tablero_creado)
        self._sub(CartaMostradaEvt, self._on_carta_mostrada)
        self._sub(AciertoEvt, self._on_acierto)
        self._sub(FalloEvt, self._on_fallo)
        self._sub(PartidaTerminadaEvt, self._on_fin)

        self.destroyed.connect(lambda *_: self._unsubscribe_all())
        
    def _sub(self, tipo, handler):
            self.bus.subscribe(tipo, handler)
            self._subs.append((tipo, handler))

    def _unsubscribe_all(self):
            for tipo, handler in self._subs:
                self.bus.unsubscribe(tipo, handler)
            self._subs.clear()
    # ========== EVENTOS (Controller -> UI) ==========

    def _on_tablero_creado(self, evt: TableroCreadoEvt) -> None:
        # Limpiar layout anterior (si lo hubiera)
        while self._grid.count():
            item = self._grid.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)
        self._cartas.clear()
        self._n = evt.n

        # Reverso base; lo escalamos aproximando carta ~tamaño inicial
        back_pm = self.provider.pixmap_back()

        for fila in range(evt.n):
            for col in range(evt.n):
                cv = CartaView((fila, col), parent=self)
                cv.clicked.connect(self._on_carta_click)
                cv.set_pixmap_reverso(back_pm)
                self._grid.addWidget(cv, fila, col)
                self._cartas[(fila, col)] = cv

        self.updateGeometry()

    def _on_carta_mostrada(self, evt: CartaMostradaEvt) -> None:
        cv = self._cartas.get(evt.pos)
        if not cv:
            return
        # Obtenemos el tamaño disponible aproximado para escalar el anverso
        # (El QLabel tiene scaledContents=True; esto es opcional.)
        target = cv.size() if not cv.size().isEmpty() else None
        pm = self.provider.pixmap_for_value(evt.valor, target_size=target if target else None)
        cv.mostrar_anverso_pixmap(pm)

    def _on_acierto(self, evt: AciertoEvt) -> None:
        for pos in (evt.pos1, evt.pos2):
            cv = self._cartas.get(pos)
            if cv:
                cv.marcar_emparejada()

    def _on_fallo(self, evt: FalloEvt) -> None:
        for pos in (evt.pos1, evt.pos2):
            cv = self._cartas.get(pos)
            if cv:
                cv.mostrar_reverso()

    def _on_fin(self, evt: PartidaTerminadaEvt) -> None:
        pass  # podrías publicar un MensajeEvt o mostrar overlay

    # ========== INTENTS (UI -> Controller) ==========

    def _on_carta_click(self, pos: Pos) -> None:
        self.bus.publish(CartaClicadaIntent(pos=pos))

    # (Opcional) si quieres re-escalar todo al redimensionar:
    # def resizeEvent(self, ev):  # type: ignore[override]
    #     super().resizeEvent(ev)
    #     if not self._n:
    #         return
    #     # Calcular lado ideal por celda
    #     w = max(self.width() - self._grid.contentsMargins().left() - self._grid.contentsMargins().right(), 0)
    #     h = max(self.height() - self._grid.contentsMargins().top() - self._grid.contentsMargins().bottom(), 0)
    #     lado = min(w // self._n, h // self._n)
    #     for cv in self._cartas.values():
    #         if lado > 0:
    #             cv.setMinimumSize(lado, lado)
