from __future__ import annotations
from collections import defaultdict
from typing import Callable, DefaultDict, List, Type, TypeVar, Any

T = TypeVar("T")

class EventBus:
    """
    Bus de eventos muy simple (sin hilos):
    - subscribe(Tipo, handler)
    - publish(instancia_de_Tipo)
    Los handlers se ejecutan en el hilo actual (el de Qt).
    """

    def __init__(self) -> None:
        # Mapa: Tipo -> lista de handlers
        self._subs: DefaultDict[Type[Any], List[Callable[[Any], None]]] = defaultdict(list)

    def subscribe(self, tipo: Type[T], handler: Callable[[T], None]) -> None:
        self._subs[tipo].append(handler)

    def unsubscribe(self, tipo: Type[T], handler: Callable[[T], None]) -> None:
        if handler in self._subs.get(tipo, []):
            self._subs[tipo].remove(handler)

    def publish(self, evento):
        sus = list(self._subs.get(type(evento), []))
        for handler in sus:
            try:
                handler(evento)
            except RuntimeError as e:
                if "Internal C++ object" in str(e):
                    # handler atado a un QObject ya destruido → limpiar
                    self.unsubscribe(type(evento), handler)
                else:
                    raise