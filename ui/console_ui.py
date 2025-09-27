# ui/console_ui.py
from typing import List, Dict
import os
import random
from colorama import init, Fore, Style

from models.entities import Entity, RACE_OPTIONS, CLASS_FEATURES
from utils.dice_parser import roll_4d6_drop_lowest, roll_dice
from storage.save_load import save_players, list_saves, load_players
from models.scenes import SCENES

init(autoreset=True)

ABILITY_KEYS = ["Сила", "Ловкость", "Выносливость", "Интелект", "Мудрость", "Харизма"]

CLASSES = {
    "1": ("Воин", {"Сила": 15, "Ловкость": 10, "Интеллект": 8, "Выносливость": 14, "Мудрость": 10, "Харизма": 10}),
    "2": ("Маг", {"Сила": 8, "Ловкость": 12, "Интеллект": 15, "Выносливость": 10, "Мудрость": 12, "Харизма": 10}),
    "3": ("Плут", {"Сила": 10, "Ловкость": 15, "Интеллект": 10, "Выносливость": 12, "Мудрость": 10, "Харизма": 12}),
    "4": ("Жрец", {"Сила": 10, "Ловкость": 8, "Интеллект": 12, "Выносливость": 12, "Мудрость": 15, "Харизма": 10}),
    "5": ("Варвар", {"Сила": 16, "Ловкость": 12, "Интеллект": 8, "Выносливость": 15, "Мудрость": 10, "Харизма": 8}),
    "6": ("Паладин", {"Сила": 15, "Ловкость": 10, "Интеллект": 8, "Выносливость": 14, "Мудрость": 12, "Харизма": 14}),
    "7": ("Следопыт", {"Сила": 12, "Ловкость": 15, "Интеллект": 10, "Выносливость": 12, "Мудрость": 14, "Харизма": 8}),
    "8": ("Варлок", {"Сила": 8, "Ловкость": 10, "Интеллект": 12, "Выносливость": 12, "Мудрость": 10, "Харизма": 15}),
    "9": ("Бард", {"Сила": 8, "Ловкость": 12, "Интеллект": 10, "Выносливость": 10, "Мудрость": 10, "Харизма": 15}),
    "10": ("Монах", {"Сила": 12, "Ловкость": 15, "Интеллект": 10, "Выносливость": 12, "Мудрость": 14, "Харизма": 8}),
    "11": ("Друид", {"Сила": 8, "Ловкость": 10, "Интеллект": 12, "Выносливость": 12, "Мудрость": 15, "Харизма": 10}),
    "12": ("Чародей", {"Сила": 8, "Ловкость": 12, "Интеллект": 10, "Выносливость": 10, "Мудрость": 10, "Харизма": 15}),
}

BACKGROUNDS = [
    "Аскет", "Солдат", "Благородный", "Преступник", "Ученый",
    "Шут/Артист", "Путник", "Ремесленник"
]

ALIGNMENTS = [
    "Законопослушный добрый", "Нейтральный добрый", "Хаотично добрый",
    "Законопослушный нейтральный", "Истинно нейтральный", "Хаотично нейтральный",
    "Законопослушный злой", "Нейтрально злой", "Хаотично злой"
]


def main_menu():
    while True:
        print(Style.BRIGHT + Fore.YELLOW + "\n=== Главное меню ===")
        print("1. Начать новую игру (создать персонажей)")
        print("2. Загрузить игру")
        print("3. Выйти")

        choice = input(Fore.CYAN + "Выберите действие: ").strip()
        if choice == "1":
            players = create_characters()
            slot = input(Fore.CYAN + "Введите номер слота для сохранения (по умолчанию 1): ").strip()
            slot = int(slot) if slot.isdigit() else 1
            save_players(players, slot)
            return players
        elif choice == "2":
            saves = list_saves()
            if not saves:
                print(Fore.RED + "Сохранений нет.")
                continue
            print(Style.BRIGHT + Fore.YELLOW + "\nДоступные сохранения:")
            for i, s in enumerate(saves, 1):
                print(f"{i}. {s['filename']}  | Игроки: {', '.join(s['players'])} | {s['mtime']}")
            pick = input(Fore.CYAN + "Выберите номер сохранения: ").strip()
            if pick.isdigit() and 1 <= int(pick) <= len(saves):
                slot = saves[int(pick)-1]["slot"]
                return load_players(slot)
            else:
                print(Fore.RED + "Неверный выбор.")
        elif choice == "3":
            print(Fore.MAGENTA + "Выход.")
            os._exit(0)
        else:
            print(Fore.RED + "Неверный ввод.")


def create_characters() -> List[Entity]:
    players: List[Entity] = []
    while True:
        print(Style.BRIGHT + Fore.YELLOW + "\n--- Создание персонажа ---")
        name = input(Fore.CYAN + "Имя персонажа: ").strip()
        race = choose_race()
        char_class = choose_class()
        controller = choose_controller()
        background = choose_background()
        alignment = choose_alignment()
        stats = generate_ability_scores_interactive()
        appearance = choose_appearance_for_race(race)

        ent = Entity(
            name=name,
            char_class=char_class,
            race=race,
            stats=stats,
            controller=controller,
            background=background,
            appearance=appearance,
            level=1,
            xp=0,
            current_scene=SCENES["scene_1"]
        )
        print(Fore.GREEN + "\nНачальные фичи и экипировка:")
        for f in ent.features[:6]:
            print("  -", f)
        for e in ent.equipment[:6]:
            print("  *", e)

        players.append(ent)

        more = input(Fore.CYAN + "\nДобавить ещё персонажа? (y/n): ").strip().lower()
        if more != "y":
            break
    return players


def choose_race() -> str:
    races = list(RACE_OPTIONS.keys())
    print(Style.BRIGHT + Fore.YELLOW + "\nВыберите расу:")
    for i, r in enumerate(races, 1):
        traits = ", ".join(RACE_OPTIONS[r]["traits"])
        print(f"{i}. {r} ({traits})")
    while True:
        ch = input(Fore.CYAN + "Ваш выбор (номер, r для случайной): ").strip().lower()
        if ch == "r":
            pick = random.choice(races)
            print(Fore.BLUE + "Случайная раса: " + pick)
            return pick
        if ch.isdigit() and 1 <= int(ch) <= len(races):
            return races[int(ch)-1]
        print(Fore.RED + "Неверный ввод.")


def choose_class() -> str:
    print(Style.BRIGHT + Fore.YELLOW + "\nВыберите класс:")
    for k, (name, base) in CLASSES.items():
        stats_str = ", ".join([f"{kk.upper()}={vv}" for kk, vv in base.items()])
        print(f"{k}. {name} ({stats_str})")
    while True:
        ch = input(Fore.CYAN + "Выбор (номер): ").strip()
        if ch in CLASSES:
            return CLASSES[ch][0]
        print(Fore.RED + "Неверный ввод.")


def choose_controller() -> str:
    print(Style.BRIGHT + Fore.YELLOW + "\nКто будет управлять персонажем?")
    print("1. Игрок")
    print("2. ИИ")
    print("3. Гибрид (ИИ предлагает варианты, игрок выбирает)")
    while True:
        ch = input(Fore.CYAN + "Выбор: ").strip()
        if ch == "1":
            return "player"
        if ch == "2":
            return "ai"
        if ch == "3":
            return "hybrid"
        print(Fore.RED + "Неверный ввод.")


def choose_background() -> str:
    print(Style.BRIGHT + Fore.YELLOW + "\nВыберите фон (Предистория):")
    for i, b in enumerate(BACKGROUNDS, 1):
        print(f"{i}. {b}")
    while True:
        ch = input(Fore.CYAN + "Выбор (номер, r - случайный): ").strip().lower()
        if ch == "r":
            pick = random.choice(BACKGROUNDS)
            print(Fore.BLUE + "Случайный фон: " + pick)
            return pick
        if ch.isdigit() and 1 <= int(ch) <= len(BACKGROUNDS):
            return BACKGROUNDS[int(ch)-1]
        print(Fore.RED + "Неверный ввод.")


def choose_alignment() -> str:
    print(Style.BRIGHT + Fore.YELLOW + "\nВыберите мировоззрение:")
    for i, a in enumerate(ALIGNMENTS, 1):
        print(f"{i}. {a}")
    while True:
        ch = input(Fore.CYAN + "Выбор (номер, Enter для нейтрального): ").strip()
        if ch == "":
            return "Истинно нейтральный"
        if ch.isdigit() and 1 <= int(ch) <= len(ALIGNMENTS):
            return ALIGNMENTS[int(ch)-1]
        print(Fore.RED + "Неверный ввод.")


def generate_ability_scores_interactive() -> Dict[str, int]:
    print(Style.BRIGHT + Fore.YELLOW + "\nГенерация характеристик. Выберите метод:")
    print("1. Стандартный массив [15,14,13,12,10,8]")
    print("2. 4d6 drop lowest (каждая характеристика)")
    print("3. Ввести вручную")
    while True:
        ch = input(Fore.CYAN + "Выбор (1/2/3): ").strip()
        if ch == "1":
            pool = [15, 14, 13, 12, 10, 8]
            return assign_scores(pool)
        elif ch == "2":
            pool = [roll_4d6_drop_lowest() for _ in range(6)]
            print(Fore.MAGENTA + "Брошено (6 значений): " + str(pool))
            return assign_scores(pool)
        elif ch == "3":
            return manual_enter_scores()
        else:
            print(Fore.RED + "Неверный ввод.")


def assign_scores(pool: List[int]) -> Dict[str, int]:
    pool = sorted(pool, reverse=True)
    print(Style.BRIGHT + Fore.YELLOW + "\nНазначьте значения характеристик. Доступные значения:", pool)
    assigned = {}
    for key in ABILITY_KEYS:
        while True:
            print(f"\nДоступные: {pool}")
            pick = input(Fore.CYAN + f"Выберите значение для {key.upper()}: ").strip()
            if pick.isdigit() and int(pick) in pool:
                val = int(pick)
                assigned[key] = val
                pool.remove(val)
                break
            print(Fore.RED + "Неверный ввод или значение недоступно.")
    print(Fore.GREEN + "Назначение завершено: " + str(assigned))
    return assigned


def manual_enter_scores() -> Dict[str, int]:
    print(Style.BRIGHT + Fore.YELLOW + "\nВвод характеристик вручную (введите число от 1 до 30).")
    assigned = {}
    for key in ABILITY_KEYS:
        while True:
            v = input(Fore.CYAN + f"{key.upper()}: ").strip()
            if v.isdigit() and 1 <= int(v) <= 30:
                assigned[key] = int(v)
                break
            print(Fore.RED + "Неверный ввод.")
    return assigned


def choose_appearance_for_race(race: str) -> Dict[str, str]:
    opts = RACE_OPTIONS.get(race, {}).get("appearance", {})
    result = {}
    print(Style.BRIGHT + Fore.YELLOW + f"\nВнешность ({race}). Можно выбрать варианты или random.")
    for attr, choices in opts.items():
        print(f"{attr}:")
        for i, c in enumerate(choices, 1):
            print(f"  {i}. {c}")
        while True:
            ch = input(Fore.CYAN + f"Выберите {attr} (номер, r - случайно): ").strip().lower()
            if ch == "r" or ch == "":
                pick = random.choice(choices)
                result[attr] = pick
                print(Fore.BLUE + f"  -> {pick}")
                break
            if ch.isdigit() and 1 <= int(ch) <= len(choices):
                result[attr] = choices[int(ch)-1]
                break
            print(Fore.RED + "Неверный ввод.")
    return result


def dice_roll_interactive(expr: str, modifier: int = 0, target: int = None):
    total, rolls = roll_dice(expr)
    total += modifier
    print(Fore.MAGENTA + f"Бросок {expr} (кости: {rolls}), модификатор {modifier:+}, итог = {total}")
    if target is not None:
        if total >= target:
            print(Fore.GREEN + f"✅ Успех (нужно {target}+)")
            return True
        else:
            print(Fore.RED + f"❌ Провал (нужно {target}+)")
            return False
    return total
