"""
CAPA DE MODELOS: CONTIENE ABSTRACCIONES DE LAS ENTIDADES DE NEGOCIO
"""

from .carta import Carta, EstadoCarta
from .tablero import Tablero, Pos
from .juego import Juego, ResultadoDeMovimiento

__all__ = ["Carta", "EstadoCarta", "Pos", "Juego", "Tablero", "ResultadoDeMovimiento"]