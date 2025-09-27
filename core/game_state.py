# core/game_state.py
from typing import List, Optional
from core.event_bus import EventBus
from models.entities import Entity


class GameState:
    def __init__(self, event_bus: Optional[EventBus] = None):
        self.entities: List[Entity] = []
        self.current_round: int = 1
        self.event_bus = event_bus or EventBus()
        self.current_scene: str = "scene_1"

    def add_entity(self, entity: Entity):
        """Добавить сущность в конец очереди (сохранится порядок создания)."""
        self.entities.append(entity)

    def remove_entity(self, entity: Entity):
        self.entities = [e for e in self.entities if e != entity]

    def get_living_entities(self) -> List[Entity]:
        return [e for e in self.entities if e.is_alive()]

    def reset(self):
        self.entities.clear()
        self.current_round = 1

    def __repr__(self):
        ents = ", ".join([e.name for e in self.entities])
        return f"<GameState Round={self.current_round}, Entities=[{ents}]>"
