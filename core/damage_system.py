# core/damage_system.py
import random

def apply_damage(entity, amount: int):
    """Наносит урон существу и проверяет смерть"""
    entity.hp_current = max(0, entity.hp_current - amount)
    print(f"{entity.name} получает {amount} урона! "
          f"HP: {entity.hp_current}/{entity.hp_max}")

    if not entity.is_alive():
        handle_death(entity)

def handle_death(entity):
    """Механика смерти (сцена смерти или конец игры)"""
    print(f"💀 {entity.name} погиб!")
    # можно переключить на отдельную сцену:
    from models.scenes import SCENES
    entity.current_scene = SCENES.get("scene_death", {"text": "Конец пути.", "actions": []})