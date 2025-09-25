# core/turn_manager.py
from core.game_state import GameState
from typing import List
from models.entities import Entity


class TurnManager:
    def __init__(self, game_state: GameState):
        self.state = game_state
        self.order: List[Entity] = []
        self.index = 0
        self.running = False

    def build_order(self):
        # порядок — порядок добавления в game_state.entities, только живые
        self.order = [e for e in self.state.entities if e.is_alive()]
        self.index = 0

    def start(self):
        """Запустить цикл ходов (блокирующий)."""
        self.running = True
        self.build_order()
        print(f"\nГейм мастер: Запуск цикла. Игроков в очереди: {len(self.order)}")
        while self.running:
            if not self.order:
                print("Гейм мастер: Нет сущностей для ходов. Выход.")
                break

            if self.index >= len(self.order):
                self.index = 0
                self.state.current_round += 1
                print(f"\n--- Раунд {self.state.current_round} ---")

            current = self.order[self.index]

            # если умер — просто пропускаем
            if not current.is_alive():
                self.index += 1
                continue

            # посылаем событие начала хода
            self.state.event_bus.publish("start_turn", current)

            # после хода обновляем порядок (на случай, если кто-то погиб или появились новые сущности)
            # сохраним текущую позицию по отношению к order: если order укоротился, корректируем индекс
            self.build_order()
            # индекс остаётся на следующем элементе (если текущий ещё жив — сдвинем на 1)
            # найдём индекс текущ в новом order, чтобы продолжить корректно
            try:
                pos = self.order.index(current)
                self.index = pos + 1
            except ValueError:
                # текущего больше нет — не сдвигаем, оставим на текущем индексе
                # (index уже указывает на следующий)
                self.index = min(self.index, len(self.order))
        print("Гейм мастер: Цикл остановлен.")

    def stop(self):
        self.running = False
