# storage/save_load.py
import json
import os
import time
from typing import List, Dict
from models.entities import Entity
from core.game_state import GameState

SAVE_DIR = os.path.join(os.path.dirname(__file__), "saves")
os.makedirs(SAVE_DIR, exist_ok=True)


def _get_save_path(slot: int) -> str:
    return os.path.join(SAVE_DIR, f"save_{slot}.json")


def save_players(players: List[Entity], slot: int = 1):
    path = _get_save_path(slot)
    data = [p.to_dict() for p in players]
    meta = {
        "_meta": {
            "players": [p.name for p in players],
            "saved_at": time.time()
        }
    }
    to_write = {"meta": meta, "data": data}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(to_write, f, ensure_ascii=False, indent=2)
    print(f"Сохранено в {path}")


def load_players(slot: int = 1) -> List[Entity]:
    path = _get_save_path(slot)
    try:
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        raw = payload.get("data", payload)
        players = [Entity.from_dict(d) for d in raw]
        print(f"Загружено {len(players)} персонажей из слота {slot}.")
        return players
    except FileNotFoundError:
        print("Файл сохранения не найден.")
        return []

def save_game(state: GameState, slot: int = 1):
    path = _get_save_path(slot)
    data = [p.to_dict() for p in state.entities]
    meta = {
        "_meta": {
            "players": [p.name for p in state.entities],
            "saved_at": time.time(),
            "scene": state.current_scene,
            "round": state.current_round,
        }
    }
    to_write = {"meta": meta, "data": data}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(to_write, f, ensure_ascii=False, indent=2)
    print(f"Сохранено в {path}")


def load_game(state: GameState, slot: int = 1):
    path = _get_save_path(slot)
    try:
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        raw = payload.get("data", payload)
        state.entities = [Entity.from_dict(d) for d in raw]

        meta = payload.get("meta", {}).get("_meta", {})
        state.current_scene = meta.get("scene", "scene_1")
        state.current_round = meta.get("round", 1)

        print(f"Загружено {len(state.entities)} персонажей, сцена {state.current_scene}, раунд {state.current_round}")
        return state
    except FileNotFoundError:
        print("Файл сохранения не найден.")
        return state




def list_saves() -> List[Dict]:
    files = []
    for fn in os.listdir(SAVE_DIR):
        if not fn.startswith("save_") or not fn.endswith(".json"):
            continue
        full = os.path.join(SAVE_DIR, fn)
        slot = int(fn.replace("save_", "").replace(".json", ""))
        try:
            with open(full, "r", encoding="utf-8") as f:
                payload = json.load(f)
            meta = payload.get("meta", {}).get("_meta", {})
            players = meta.get("players", [])
        except Exception:
            players = []
        mtime = time_str(os.path.getmtime(full))
        files.append({"slot": slot, "filename": fn, "players": players, "mtime": mtime})
    files.sort(key=lambda x: x["slot"])
    return files


def time_str(ts: float) -> str:
    return datetime_from_ts(ts).strftime("%Y-%m-%d %H:%M:%S")


def datetime_from_ts(ts: float):
    import datetime
    return datetime.datetime.fromtimestamp(ts)
