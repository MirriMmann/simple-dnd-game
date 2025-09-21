# models/actions_map.py

from models.scenes import (
    scene_1, SCENE_ACTIONS_1,
    scene_2a, SCENE_ACTIONS_2A,
    scene_2b, SCENE_ACTIONS_2B,
    scene_2c, SCENE_ACTIONS_2C,
    scene_2d, SCENE_ACTIONS_2D,
)

ACTIONS_TO_SCENES = {
    # стартовые действия
    "go_path":       {"text": scene_2a, "actions": SCENE_ACTIONS_2A, "msg": "пошёл по тропинке вправо"},
    "go_leaves":     {"text": scene_2b, "actions": SCENE_ACTIONS_2B, "msg": "прошёл по светлячкам"},
    "inspect_wheel": {"text": scene_2c, "actions": SCENE_ACTIONS_2C, "msg": "осмотрел колесо"},
    "wait":          {"text": scene_2d, "actions": SCENE_ACTIONS_2D, "msg": "подождал"},

    # ветка 2a
    "explore_ruins": {"text": "Заглушка для руин", "actions": [], "msg": "исследовал башню"},
    "hunt":          {"text": "Заглушка для охоты", "actions": [], "msg": "отправился на охоту"},
    "camp":          {"text": "Заглушка для лагеря", "actions": [], "msg": "разбил лагерь и отдохнул"},

    # ветка 2b
    "drink_water":   {"text": "Заглушка для воды", "actions": [], "msg": "попробовал воду"},
    "catch_light":   {"text": "Заглушка для светлячка", "actions": [], "msg": "попытался поймать светлячка"},
    "sing":          {"text": "Заглушка для песни", "actions": [], "msg": "ответил на звон песней"},
    "move_on":       {"text": "Заглушка для движения дальше", "actions": [], "msg": "прошёл дальше мимо пруда"},

    # ветка 2c
    "search_inside": {"text": "Заглушка для поиска", "actions": [], "msg": "заглянул внутрь колеса"},
    "break_apart":   {"text": "Заглушка для разлома", "actions": [], "msg": "разломал колесо"},
    "retreat":       {"text": "Заглушка для отхода", "actions": [], "msg": "отошёл и наблюдает издалека"},

    # ветка 2d
    "approach_creature": {"text": "Заглушка для существа", "actions": [], "msg": "подошёл к существу"},
    "hide":              {"text": "Заглушка для укрытия", "actions": [], "msg": "спрятался за кустами"},
    "shout":             {"text": "Заглушка для крика", "actions": [], "msg": "крикнул"},
    "ignore":            {"text": "Заглушка для игнора", "actions": [], "msg": "проигнорировал и пошёл дальше"},
}
