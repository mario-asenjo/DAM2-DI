# app/juego_controller.py
from __future__ import annotations

from typing import Optional, Tuple
from PySide6.QtCore import QObject, QTimer

from modelos import Juego, ResultadoDeMovimiento, Pos
from .event_bus import EventBus
from .eventos import (
    NuevaPartidaIntent,
    CartaClicadaIntent,
    AbrirPreferenciasIntent,
    SalirIntent,
    #
    TableroCreadoEvt,
    CartaMostradaEvt,
    AciertoEvt,
    FalloEvt,
    PartidaTerminadaEvt,
    MensajeEvt,
)

class JuegoController(QObject):
    """
    Orquesta intents -> dominio -> eventos.
    No toca widgets; todo va por EventBus.
    """

    def __init__(self, bus: EventBus, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.bus = bus
        self.juego: Optional[Juego] = None

        # Parámetros de UX (pueden venir de Preferencias/QSettings)
        self.delay_fallo_ms = 700

        # Suscripciones a INTENTS
        bus.subscribe(NuevaPartidaIntent, self._on_nueva_partida)
        bus.subscribe(CartaClicadaIntent, self._on_carta_clicada)
        bus.subscribe(AbrirPreferenciasIntent, self._on_preferencias)
        bus.subscribe(SalirIntent, self._on_salir)

    # ============= INTENTS -> MANEJADORES =============

    def _on_nueva_partida(self, intent: NuevaPartidaIntent) -> None:
        # Crea un juego nuevo en dominio
        try:
            self.juego = Juego(n=intent.n, semilla=intent.semilla)
        except Exception as exc:
            self.bus.publish(MensajeEvt(f"Error creando partida: {exc}"))
            return

        # Anuncia a la UI que hay un tablero de tamaño N listo
        self.bus.publish(TableroCreadoEvt(n=intent.n))
        self.bus.publish(MensajeEvt(f"Nueva partida {intent.n}×{intent.n}"))

    def _on_carta_clicada(self, intent: CartaClicadaIntent) -> None:
        if not self.juego:
            self.bus.publish(MensajeEvt("No hay partida activa."))
            return

        pos = intent.pos
        # Invoca dominio
        res: ResultadoDeMovimiento = self.juego.voltear(pos)

        # Según el tipo, publicamos eventos de UI
        if res.tipo == "primera":
            # Mostramos la primera carta levantada
            valor = self.juego.tablero.carta_en(pos).valor
            self.bus.publish(CartaMostradaEvt(pos=pos, valor=valor))

        elif res.tipo == "acierto":
            # Asegurar que la segunda carta se ve
            pos1, pos2 = res.primera, res.segunda
            assert pos1 is not None and pos2 is not None
            valor2 = self.juego.tablero.carta_en(pos2).valor
            self.bus.publish(CartaMostradaEvt(pos=pos2, valor=valor2))
            # Notificar acierto
            self.bus.publish(AciertoEvt(pos1=pos1, pos2=pos2))
            if res.terminado:
                self.bus.publish(PartidaTerminadaEvt(turnos=res.turnos, aciertos=res.aciertos))

        elif res.tipo == "fallo":
            # Mostrar la segunda carta para que el usuario la vea
            pos1, pos2 = res.primera, res.segunda
            assert pos1 is not None and pos2 is not None
            valor2 = self.juego.tablero.carta_en(pos2).valor
            self.bus.publish(CartaMostradaEvt(pos=pos2, valor=valor2))

            # Tras un pequeño delay, decir a la UI que baje ambas
            def _bajar_ambas() -> None:
                self.bus.publish(FalloEvt(pos1=pos1, pos2=pos2))

            QTimer.singleShot(self.delay_fallo_ms, _bajar_ambas)

        else:
            self.bus.publish(MensajeEvt(f"Movimiento desconocido: {res.tipo!r}"))

    def _on_preferencias(self, _: AbrirPreferenciasIntent) -> None:
        # Aquí abriríamos un diálogo de preferencias (UI) o publicaríamos un evento para que la UI lo haga.
        self.bus.publish(MensajeEvt("Preferencias aún no implementadas."))

    def _on_salir(self, _: SalirIntent) -> None:
        # Aquí podríamos persistir settings, etc.
        self.bus.publish(MensajeEvt("Saliendo..."))
        # El cierre real lo hace MainWindow al recibir la señal (ya la emite en _on_salir).
