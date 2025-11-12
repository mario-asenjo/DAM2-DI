"""
CAPA DE APLICACION: Bus de eventos, eventos y puente entre la UI y MainWindow subscriptor de hooks y controlador.
"""

from .event_bus import EventBus
from .eventos import NuevaPartidaIntent, CartaClicadaIntent, AbrirPreferenciasIntent, SalirIntent
from .eventos import MensajeEvt, FalloEvt, AciertoEvt, CartaMostradaEvt, TableroCreadoEvt, PartidaTerminadaEvt
from .puente_ui_window import UIBridge
from .juego_controller import JuegoController

__all__ = ["UIBridge", "EventBus", "NuevaPartidaIntent", "CartaClicadaIntent", "AbrirPreferenciasIntent", "SalirIntent", "MensajeEvt", "FalloEvt", "AciertoEvt", "CartaMostradaEvt", "TableroCreadoEvt", "PartidaTerminadaEvt", "JuegoController"]