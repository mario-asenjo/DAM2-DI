from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto

class EstadoCarta(Enum):
    BOCA_ABAJO = auto()
    BOCA_ARRIBA = auto()
    EMPAREJADA = auto()

@dataclass
class Carta:
    id: int
    valor: int
    estado: EstadoCarta = EstadoCarta.BOCA_ABAJO

    def puede_voltearse(self) -> bool:
        return self.estado == EstadoCarta.BOCA_ABAJO

    def voltear(self) -> None:
        if self.puede_voltearse():
            self.estado = EstadoCarta.BOCA_ARRIBA

    def bajar(self) -> None:
        # Volver boca abajo sólo si está levantada
        if self.estado == EstadoCarta.BOCA_ARRIBA:
            self.estado = EstadoCarta.BOCA_ABAJO

    def emparejar(self) -> None:
        # Marcar como resuelta
        self.estado = EstadoCarta.EMPAREJADA
        