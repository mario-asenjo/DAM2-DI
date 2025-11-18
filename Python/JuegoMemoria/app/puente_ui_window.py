from __future__ import annotations
from typing import Optional
from PySide6.QtCore import QObject

from .event_bus import EventBus
from .eventos import NuevaPartidaIntent, AbrirPreferenciasIntent, SalirIntent
from ui import MainWindow

class UIBridge(QObject):
    """
    Conecta señales Qt de MainWindow con Intents del EventBus.
    (Nada de lógica de juego aquí.)
    """

    def __init__(self, window: MainWindow, bus: EventBus) -> None:
        super().__init__(window)
        self.window = window
        self.bus = bus

        # Señales → Intents
        self.window.nueva_partida_solicitada.connect(self._on_nueva_partida)
        self.window.preferencias_solicitadas.connect(self._on_preferencias)
        self.window.salir_solicitado.connect(self._on_salir)

    # Slots (Qt) → publican Intents
    def _on_nueva_partida(self) -> None:
        # Por ahora, tamaño fijo (p. ej. 4). Más adelante lo leeremos de Preferencias/QSettings.
        self.bus.publish(NuevaPartidaIntent(n=4))

    def _on_preferencias(self) -> None:
        self.bus.publish(AbrirPreferenciasIntent())

    def _on_salir(self) -> None:
        self.bus.publish(SalirIntent())