# main.py
import os
import random
from ui.console_ui import main_menu
from core.game_state import GameState
from core.turn_manager import TurnManager
from storage.save_load import save_game
from models.scenes import (
    scene_1, SCENE_ACTIONS_1,
    scene_2a, SCENE_ACTIONS_2A,
    scene_2b, SCENE_ACTIONS_2B,
    scene_2c, SCENE_ACTIONS_2C,
    scene_2d, SCENE_ACTIONS_2D
)


LOG_PATH = os.path.join(os.path.dirname(__file__), "storage", "game_log.txt")
os.makedirs(os.path.join(os.path.dirname(__file__), "storage"), exist_ok=True)

def log_write(line: str):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def handle_start_turn(entity):
    """
    Обработчик события 'start_turn'. Блокирует до выбора действия.
    """
    print(f"\n--- Ход: {entity.name} (класс: {getattr(entity, 'char_class', '?')}, {entity.controller}) ---")
    log_write(f"Round {gs.current_round} - start_turn - {entity.name} (CTRL={entity.controller})")

    # Выбор опций в зависимости от controller
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
    for i, (_, label) in enumerate(entity.current_scene["actions"], 1):
        print(f" {i}. {label}")
    print(" s. Сохраниться")
    print(" q. Выйти из игры")

    while True:
        choice = input(f"Ваш выбор для {entity.name}: ").strip().lower()
        if choice == "q":
            print("Выход по запросу пользователя.")
            tm.stop()
            return
        if choice == "s":
            save_game(gs, slot=1)   # сохраняем текущее состояние
            print("Игра сохранена.")
            continue
        if choice.isdigit() and 1 <= int(choice) <= len(entity.current_scene["actions"]):
            action_key = entity.current_scene["actions"][int(choice)-1][0]
            resolve_action(entity, action_key)
            return
        print("Неверный ввод. Введите номер действия, 's' или 'q'.")





def do_ai_turn(entity):
    # простая логика: случайный выбор
    action_key = random.choice(SCENE_ACTIONS)[0] # type: ignore
    print(f"{entity.name} (ИИ) выбирает: {action_key}")
    resolve_action(entity, action_key)


def do_hybrid_turn(entity):
    # генерируем 2-4 варианта и даём игроку выбрать
    count = random.randint(2, 4)
    options = random.sample(SCENE_ACTIONS, k=count) # type: ignore
    print("ИИ предлагает варианты:")
    for i, (_, label) in enumerate(options, 1):
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
    if action_key == "go_path":
        entity.current_scene = {"text": scene_2a, "actions": SCENE_ACTIONS_2A}
        res = f"{entity.name} пошёл по тропинке вправо."
    elif action_key == "go_leaves":
        entity.current_scene = {"text": scene_2b, "actions": SCENE_ACTIONS_2B}
        res = f"{entity.name} прошёл по светлячкам."
    elif action_key == "inspect_wheel":
        entity.current_scene = {"text": scene_2c, "actions": SCENE_ACTIONS_2C}
        res = f"{entity.name} осмотрел колесо."
    elif action_key == "wait":
        entity.current_scene = {"text": scene_2d, "actions": SCENE_ACTIONS_2D}
        res = f"{entity.name} подождал."
    else:
        res = f"{entity.name} сделал неизвестное действие ({action_key})."

    print(res)
    log_write(f"Round {gs.current_round} - {entity.name} -> {action_key} | {res}")




if __name__ == "__main__":
    # 1) Создаём персонажей через UI
    players = main_menu()  # возвращает список Entity

    # 2) Печатаем сцену
    print("\n=== Текущие сцены игроков ===\n")
    for p in players:
        print(f"Сцена для {p.name}:")
        print(p.current_scene["text"])
        print()


    # 3) Создаём GameState и добавляем игроков в том порядке, как вернул main_menu()
    gs = GameState()
    for p in players:
        gs.add_entity(p)

    # 4) Подписываем обработчик start_turn
    gs.event_bus.subscribe("start_turn", handle_start_turn)

    # 5) Запускаем TurnManager
    tm = TurnManager(gs)
    tm.start()

    print("\nИгра завершена.")
