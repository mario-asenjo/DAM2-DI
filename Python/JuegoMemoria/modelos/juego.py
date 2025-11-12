from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple

from .tablero import Tablero, Pos

@dataclass(frozen=True)
class ResultadoDeMovimiento:
    tipo: str  # "primera" | "acierto" | "fallo"
    primera: Optional[Pos]
    segunda: Optional[Pos]
    terminado: bool
    turnos: int
    aciertos: int

class Juego:
    def __init__(self, n: int, semilla: int | None = None) -> None:
        self.tablero = Tablero(n, semilla=semilla)
        self._seleccion_actual: Optional[Pos] = None
        self.turnos = 0
        self.aciertos = 0

    def voltear(self, pos: Pos) -> ResultadoDeMovimiento:
        # Ignorar doble click sobre misma carta levantada
        if self._seleccion_actual == pos:
            return self._estado("primera", self._seleccion_actual, None)

        # Intento de voltear
        exito = self.tablero.voltear(pos)
        if not exito:
            # No se puede voltear (estaba emparejada o ya arriba)
            return self._estado("primera" if self._seleccion_actual else "primera", self._seleccion_actual, None)

        # Caso: no había primera → guardamos y listo
        if self._seleccion_actual is None:
            self._seleccion_actual = pos
            return self._estado("primera", self._seleccion_actual, None)

        # Caso: ya había primera → comparamos con segunda
        primera = self._seleccion_actual
        segunda = pos
        self.turnos += 1

        c1 = self.tablero.carta_en(primera)
        c2 = self.tablero.carta_en(segunda)

        if c1.valor == c2.valor:
            # Acierto: ambas boca arriba
            self.tablero.marcar_emparejadas(primera, segunda)
            self._seleccion_actual = None
            self.aciertos += 1
            terminado = self.tablero.todas_emparejadas()
            return self._estado("acierto", primera, segunda, terminado)
        else:
            # Fallo: devolver ambas boca abajo
            self.tablero.bajar(primera)
            self.tablero.bajar(segunda)
            self._seleccion_actual = None
            return self._estado("fallo", primera, segunda)

    # ================== helpers ==================

    def _estado(
        self,
        tipo: str,
        primera: Optional[Pos],
        segunda: Optional[Pos],
        terminado: bool | None = None,
    ) -> ResultadoDeMovimiento:
        if terminado is None:
            terminado = self.tablero.todas_emparejadas()
        return ResultadoDeMovimiento(
            tipo=tipo,
            primera=primera,
            segunda=segunda,
            terminado=terminado,
            turnos=self.turnos,
            aciertos=self.aciertos,
        )