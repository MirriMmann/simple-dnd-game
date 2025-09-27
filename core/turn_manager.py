# core/turn_manager.py
from core.game_state import GameState
from typing import List
from models.entities import Entity

# 🎨 Цвета
from colorama import Fore, Style, init
init(autoreset=True)


class TurnManager:
    def __init__(self, game_state: GameState):
        self.state = game_state
        self.order: List[Entity] = []
        self.index = 0
        self.running = False

    def build_order(self):
        self.order = [e for e in self.state.entities if e.is_alive()]
        self.index = 0

    def start(self):
        """Запустить цикл ходов (блокирующий)."""
        self.running = True
        self.build_order()
        print(Fore.MAGENTA + Style.BRIGHT + f"\n🎲 Гейм мастер: Запуск цикла. "
              f"Игроков в очереди: {len(self.order)}")
        while self.running:
            if not self.order:
                print(Fore.MAGENTA + Style.BRIGHT + "⚠ Гейм мастер: Нет сущностей для ходов. Выход.")
                break

            if self.index >= len(self.order):
                self.index = 0
                self.state.current_round += 1
                print(Fore.MAGENTA + Style.BRIGHT + f"\n--- Раунд {self.state.current_round} ---")

            current = self.order[self.index]

            # если умер — просто пропускаем
            if not current.is_alive():
                self.index += 1
                continue

            # посылаем событие начала хода
            self.state.event_bus.publish("start_turn", current)

            self.build_order()
            try:
                pos = self.order.index(current)
                self.index = pos + 1
            except ValueError:
                self.index = min(self.index, len(self.order))

        print(Fore.MAGENTA + Style.BRIGHT + "🛑 Гейм мастер: Цикл остановлен.")

    def stop(self):
        self.running = False
