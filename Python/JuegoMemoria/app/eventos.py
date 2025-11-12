from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Optional

Pos = Tuple[int, int]

# --------- INTENTS (UI -> Controller) ---------

@dataclass(frozen=True)
class NuevaPartidaIntent:
    n: int  # tamaño del tablero (n x n)
    semilla: Optional[int] = None

@dataclass(frozen=True)
class CartaClicadaIntent:
    pos: Pos  # (fila, col)

@dataclass(frozen=True)
class AbrirPreferenciasIntent:
    pass

@dataclass(frozen=True)
class SalirIntent:
    pass


# --------- EVENTOS (Controller -> UI) ---------

@dataclass(frozen=True)
class MensajeEvt:
    texto: str

@dataclass(frozen=True)
class TableroCreadoEvt:
    n: int

@dataclass(frozen=True)
class CartaMostradaEvt:
    pos: Pos
    valor: int  # la UI lo mapeará a imagen

@dataclass(frozen=True)
class AciertoEvt:
    pos1: Pos
    pos2: Pos

@dataclass(frozen=True)
class FalloEvt:
    pos1: Pos
    pos2: Pos

@dataclass(frozen=True)
class PartidaTerminadaEvt:
    turnos: int
    aciertos: int