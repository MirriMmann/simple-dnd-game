import json
from models.entities import Entity


SAVE_FILE = "save.json"


def save_players(players):
    data = [p.to_dict() for p in players]
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\nСохранено {len(players)} игроков в {SAVE_FILE}")

def load_players():
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        players = [Entity.from_dict(d) for d in data]
        print(f"\nЗагружено {len(players)} игроков из {SAVE_FILE}")
        return players
    except FileNotFoundError:
        print("\nСохранение не найдено.")
        return []