# main.py
import os
import random
from colorama import Fore, Style, init

from ui.console_ui import main_menu
from core.game_state import GameState
from core.turn_manager import TurnManager
from storage.save_load import save_game
from models.scenes import SCENES
from utils.dice_parser import roll_check
from core.actions import resolve_action

# инициализация colorama
init(autoreset=True)

LOG_PATH = os.path.join(os.path.dirname(__file__), "storage", "game_log.txt")
os.makedirs(os.path.join(os.path.dirname(__file__), "storage"), exist_ok=True)


def log_write(line: str):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def handle_start_turn(entity):
    print(Fore.CYAN + f"\n--- Ход: {entity.name} "
          f"(класс: {getattr(entity, 'char_class', '?')}, "
          f"{entity.controller}) ---" + Style.RESET_ALL)

    log_write(f"Round {gs.current_round} - start_turn - {entity.name} (CTRL={entity.controller})")

    if entity.controller == "player":
        do_player_turn(entity)
    elif entity.controller == "ai":
        do_ai_turn(entity)
    elif entity.controller == "hybrid":
        do_hybrid_turn(entity)
    else:
        print(Fore.RED + "Неизвестный тип управления, пропуск хода." + Style.RESET_ALL)
        log_write(f"{entity.name} - unknown controller, skipped")


def do_player_turn(entity):
    print(Fore.YELLOW + f"\nСцена для {entity.name}:" + Style.RESET_ALL)
    print(Fore.WHITE + entity.current_scene["text"] + Style.RESET_ALL)
    print(Fore.GREEN + "Доступные действия:" + Style.RESET_ALL)

    for i, action in enumerate(entity.current_scene["actions"], 1):
        label = action[1]
        print(f" {Fore.CYAN}{i}.{Style.RESET_ALL} {label}")

    print(f" {Fore.MAGENTA}s{Style.RESET_ALL}. Сохраниться")
    print(f" {Fore.RED}q{Style.RESET_ALL}. Выйти из игры")

    while True:
        choice = input(f"{Fore.YELLOW}Ваш выбор для {entity.name}:{Style.RESET_ALL} ").strip().lower()
        if choice == "q":
            print(Fore.RED + "Выход по запросу пользователя." + Style.RESET_ALL)
            save_game(gs, slot=1)
            tm.stop()
            return
        if choice == "s":
            save_game(gs, slot=1)
            print(Fore.GREEN + "Игра сохранена." + Style.RESET_ALL)
            continue
        if choice.isdigit() and 1 <= int(choice) <= len(entity.current_scene["actions"]):
            action_key = entity.current_scene["actions"][int(choice) - 1][0]
            resolve_action(entity, action_key)
            return
        print(Fore.RED + "Неверный ввод. Введите номер действия, 's' или 'q'." + Style.RESET_ALL)


def do_ai_turn(entity):
    action_key = random.choice(entity.current_scene["actions"])[0]
    print(Fore.BLUE + f"{entity.name} (ИИ) выбирает: {action_key}" + Style.RESET_ALL)
    resolve_action(entity, action_key)


def do_hybrid_turn(entity):
    count = random.randint(2, 4)
    options = random.sample(entity.current_scene["actions"], k=count)
    print(Fore.MAGENTA + "ИИ предлагает варианты:" + Style.RESET_ALL)

    for i, (_, label, _) in enumerate(options, 1):
        print(f" {Fore.CYAN}{i}.{Style.RESET_ALL} {label}")
    print(f" {Fore.YELLOW}v{Style.RESET_ALL}. Доверься ИИ (случайный выбор)")

    while True:
        ch = input(f"{Fore.YELLOW}Выберите вариант для {entity.name} (номер/v):{Style.RESET_ALL} ").strip().lower()
        if ch == "v":
            action_key = random.choice(options)[0]
            print(Fore.MAGENTA + f"{entity.name} (hybrid) доверился ИИ: {action_key}" + Style.RESET_ALL)
            resolve_action(entity, action_key)
            return
        if ch.isdigit() and 1 <= int(ch) <= len(options):
            action_key = options[int(ch) - 1][0]
            resolve_action(entity, action_key)
            return
        print(Fore.RED + "Неверный ввод." + Style.RESET_ALL)


if __name__ == "__main__":
    players = main_menu()

    print(Fore.CYAN + "\n=== Текущие сцены игроков ===\n" + Style.RESET_ALL)
    for p in players:
        print(Fore.YELLOW + f"Сцена для {p.name}:" + Style.RESET_ALL)
        print(Fore.WHITE + p.current_scene["text"] + Style.RESET_ALL)
        print()

    gs = GameState()
    for p in players:
        gs.add_entity(p)

    gs.event_bus.subscribe("start_turn", handle_start_turn)

    tm = TurnManager(gs)
    tm.start()

    print(Fore.RED + "\nИгра завершена." + Style.RESET_ALL)
