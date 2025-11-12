from __future__ import annotations
from typing import List, Tuple
import random

from .carta import Carta, EstadoCarta

Pos = Tuple[int, int]

class Tablero:
    def __init__(self, n: int, semilla: int | None = None) -> None:
        if n % 2 != 0:
            # Para un N×N con parejas perfectas, N debe ser par (N*N es par).
            # (Si prefieres permitir N impar, haríamos un hueco/comodín.)
            raise ValueError("El tamaño N debe ser par para formar parejas exactas.")
        self.n = n
        self._cartas: List[Carta] = self._generar_cartas(n, semilla)

    @staticmethod
    def _generar_cartas(n: int, semilla: int | None) -> List[Carta]:
        total = n * n
        pares = total // 2
        valores = list(range(pares)) * 2  # p.ej. [0,0,1,1,2,2,...]
        rnd = random.Random(semilla)
        rnd.shuffle(valores)
        cartas = [Carta(id=i, valor=val) for i, val in enumerate(valores)]
        return cartas

    def _idx(self, pos: Pos) -> int:
        fila, col = pos
        if not (0 <= fila < self.n and 0 <= col < self.n):
            raise IndexError("Posición fuera del tablero")
        return fila * self.n + col

    def carta_en(self, pos: Pos) -> Carta:
        return self._cartas[self._idx(pos)]

    def voltear(self, pos: Pos) -> bool:
        c = self.carta_en(pos)
        if c.puede_voltearse():
            c.voltear()
            return True
        return False

    def bajar(self, pos: Pos) -> None:
        self.carta_en(pos).bajar()

    def marcar_emparejadas(self, pos1: Pos, pos2: Pos) -> None:
        self.carta_en(pos1).emparejar()
        self.carta_en(pos2).emparejar()

    def todas_emparejadas(self) -> bool:
        return all(c.estado == EstadoCarta.EMPAREJADA for c in self._cartas)