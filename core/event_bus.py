# core/event_bus.py
from typing import Callable, Dict, List, Any


class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable[[Any], None]]] = {}

    def subscribe(self, event_name: str, handler: Callable[[Any], None]):
        self.subscribers.setdefault(event_name, []).append(handler)

    def publish(self, event_name: str, data: Any = None):
        for handler in list(self.subscribers.get(event_name, [])):
            try:
                handler(data)
            except Exception as e:
                print(f"[EventBus] Ошибка в обработчике события '{event_name}': {e}")