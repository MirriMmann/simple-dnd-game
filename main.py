import os
import random
from ui.console_ui import main_menu
from core.game_state import GameState
from core.turn_manager import TurnManager
from storage.save_load import save_game
from models.scenes import SCENES


LOG_PATH = os.path.join(os.path.dirname(__file__), "storage", "game_log.txt")
os.makedirs(os.path.join(os.path.dirname(__file__), "storage"), exist_ok=True)


def log_write(line: str):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def handle_start_turn(entity):
    print(f"\n--- Ход: {entity.name} (класс: {getattr(entity, 'char_class', '?')}, {entity.controller}) ---")
    log_write(f"Round {gs.current_round} - start_turn - {entity.name} (CTRL={entity.controller})")

    if entity.controller == "player":
        do_player_turn(entity)
    elif entity.controller == "ai":
        do_ai_turn(entity)
    elif entity.controller == "hybrid":
        do_hybrid_turn(entity)
    else:
        print("Неизвестный тип управления, пропуск хода.")
        log_write(f"{entity.name} - unknown controller, skipped")


def do_player_turn(entity):
    print("\nСцена для", entity.name)
    print(entity.current_scene["text"])
    print("Доступные действия:")
    for i, (_, label, _) in enumerate(entity.current_scene["actions"], 1):
        print(f" {i}. {label}")
    print(" s. Сохраниться")
    print(" q. Выйти из игры")

    while True:
        choice = input(f"Ваш выбор для {entity.name}: ").strip().lower()
        if choice == "q":
            print("Выход по запросу пользователя.")
            save_game(gs, slot=1)
            tm.stop()
            return
        if choice == "s":
            save_game(gs, slot=1)
            print("Игра сохранена.")
            continue
        if choice.isdigit() and 1 <= int(choice) <= len(entity.current_scene["actions"]):
            action_key = entity.current_scene["actions"][int(choice)-1][0]
            resolve_action(entity, action_key)
            return
        print("Неверный ввод. Введите номер действия, 's' или 'q'.")


def do_ai_turn(entity):
    action_key = random.choice(entity.current_scene["actions"])[0]
    print(f"{entity.name} (ИИ) выбирает: {action_key}")
    resolve_action(entity, action_key)


def do_hybrid_turn(entity):
    count = random.randint(2, 4)
    options = random.sample(entity.current_scene["actions"], k=count)
    print("ИИ предлагает варианты:")
    for i, (_, label, _) in enumerate(options, 1):
        print(f" {i}. {label}")
    print(" v. Доверься ИИ (случайный выбор)")
    while True:
        ch = input(f"Выберите вариант для {entity.name} (номер/v): ").strip().lower()
        if ch == "v":
            action_key = random.choice(options)[0]
            print(f"{entity.name} (hybrid) доверился ИИ: {action_key}")
            resolve_action(entity, action_key)
            return
        if ch.isdigit() and 1 <= int(ch) <= len(options):
            action_key = options[int(ch)-1][0]
            resolve_action(entity, action_key)
            return
        print("Неверный ввод.")


def resolve_action(entity, action_key):
    # ищем действие в текущей сцене
    for key, _, next_scene in entity.current_scene["actions"]:
        if key == action_key:
            if next_scene is None:
                res = f"{entity.name} завершил путь действием: {action_key}."
            else:
                entity.current_scene = SCENES[next_scene]
                res = f"{entity.name} сделал действие: {action_key}, переход в {next_scene}."
            print(res)
            log_write(f"Round {gs.current_round} - {entity.name} -> {action_key} | {res}")
            return

    res = f"{entity.name} сделал неизвестное действие ({action_key})."
    print(res)
    log_write(f"Round {gs.current_round} - {entity.name} -> {action_key} | {res}")


if __name__ == "__main__":
    players = main_menu()

    print("\n=== Текущие сцены игроков ===\n")
    for p in players:
        print(f"Сцена для {p.name}:")
        print(p.current_scene["text"])
        print()

    gs = GameState()
    for p in players:
        gs.add_entity(p)

    gs.event_bus.subscribe("start_turn", handle_start_turn)

    tm = TurnManager(gs)
    tm.start()

    print("\nИгра завершена.")
