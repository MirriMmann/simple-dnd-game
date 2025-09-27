# models/entities.py

import random
from typing import Dict, List
from models.scenes import SCENES

# Хиты на 1 уровень — классическая DnD5e логика (max hit die на 1 уровне)
CLASS_HIT_DIE = {
    "Воин": 10,
    "Маг": 6,
    "Плут": 8,
    "Жрец": 8,
    "Варвар": 12,
    "Паладин": 10,
    "Следопыт": 10,
    "Варлок": 8,
    "Бард": 8,
    "Монах": 8,
    "Друид": 8,
    "Чародей": 6,
}

CLASS_FEATURES = {
    "Воин": ["Бонус атаки", "Боевой стиль"],
    "Маг": ["Заклинания уровня 1", "Arcane Recovery"],
    "Плут": ["Sneak Attack", "Expertise"],
    "Жрец": ["Божественные заклинания", "Channel Divinity"],
    "Варвар": ["Rage"],
    "Паладин": ["Divine Sense", "Lay on Hands"],
    "Следопыт": ["Favored Enemy", "Natural Explorer"],
    "Варлок": ["Pact Magic"],
    "Бард": ["Bardic Inspiration"],
    "Монах": ["Unarmored Defense", "Martial Arts"],
    "Друид": ["Spellcasting", "Wild Shape (позже)"],
    "Чародей": ["Sorcery Points"],
}

CLASS_EQUIPMENT = {
    "Воин": ["Меч", "Щит", "Кольчуга"],
    "Маг": ["Посох", "Книга заклинаний", "Роба"],
    "Плут": ["Кинжал", "Луки/лук", "Кожаная броня"],
    "Жрец": ["Молниеносный символ", "Булава", "Цепь"],
    "Варвар": ["Топор", "Доспех лёгкий"],
    "Паладин": ["Меч", "Щит", "Клепаная броня"],
    "Следопыт": ["Лук", "Длинный меч", "Кожаная броня"],
    "Варлок": ["Посох", "Книга заклинаний"],
    "Бард": ["Лютня", "Лёгкая броня"],
    "Монах": ["Короткие посохи", "Нет брони"],
    "Друид": ["Посох", "Щит (не всегда)"],
    "Чародей": ["Посох/Кинжал", "Роба"],
}

RACE_OPTIONS = {
    "Человек": {"traits": ["+1 ко всем характеристикам"], "appearance": {"Волосы": ["тёмные","светлые","рыжие","чёрные","седые"], "Глаза": ["карие","зеленые","голубые","серые"], "Кожа": ["светлая","смуглая","оливковая"], "Тело": ["стройный","средний","крепкий"]}},
    "Эльф": {"traits": ["Тёмное зрение","Ловкость +2"], "appearance": {"Волосы":["светлые","серебристые","тёмные"], "Глаза":["зеленые","серые","янтарные"], "Кожа":["бледноватая","светлая"], "Тело":["стройный","грациозный"]}},
    "Дварф": {"traits": ["Тёмное зрение","Выносливость +2"], "appearance":{"Волосы":["тёмные","рыжие","бородатые"], "Глаза":["карие","серые"], "Кожа":["бледная","смуглая"], "Тело":["коренастый"]}},
    "Полурослик": {"traits": ["Счастливая удача"], "appearance":{"Волосы":["тёмные","светлые"], "Глаза":["карие","голубые"], "Кожа":["светлая"], "Тело":["низкий","пухлый"]}},
    "Драконорожденный": {"traits":["Дыхание дракона","Сила +2"], "appearance":{"Волосы":["нет"], "Глаза":["жёлтые","красные"], "Кожа":["чешуйчатая (разные цвета)"], "Тело":["мощный"]}},
    "Гном": {"traits":["Интеллект +2","Тёмное зрение"], "appearance":{"Волосы":["густые бороды","тёмные"], "Глаза":["карие","серые"], "Кожа":["светлая","оливковая"], "Тело":["низкий","коренастый"]}},
    "Половинаэльф": {"traits":["Харизма +2","Смешанные черты"], "appearance":{"Волосы":["разные"], "Глаза":["разные"], "Кожа":["разные"], "Тело":["средний","стройный"]}},
    "Половинаорк": {"traits":["Сила +2","Интенсивность"], "appearance":{"Волосы":["тёмные","стриженные"], "Глаза":["тёмные"], "Кожа":["серовато-зелёная"], "Тело":["мощный"]}},
    "Тифлинг": {"traits":["Интеллект/Харизма +1","Темное зрение"], "appearance":{"Волосы":["чёрные","алые"], "Глаза":["жёлтые","фиолетовые"], "Кожа":["красная","фиолетовая","тёмная"], "Тело":["стройный","средний"]}},
}

class Entity:
    def __init__(
        self,
        name: str,
        char_class: str,
        race: str,
        stats: dict,
        controller: str = "player",
        level: int = 1,
        xp: int = 0,
        background: str = "",
        appearance: dict = None,
        equipment: list = None,
        features: list = None,
        current_scene: dict = None,
    ):
        self.name = name
        self.char_class = char_class
        self.race = race
        self.stats = stats
        self.controller = controller
        self.level = level
        self.xp = xp
        self.background = background
        self.appearance = appearance or {}
        self.features = features or []
        self.equipment = equipment or []
        self.current_scene = current_scene or SCENES["scene_1"]



        self.hp_max = self._calculate_max_hp()
        self.hp_current = self.hp_max

        # фичи и оборудование (расовые/классовые)
        race_traits = RACE_OPTIONS.get(self.race, {}).get("traits", [])
        for t in race_traits:
            if t not in self.features:
                self.features.append(t)
        for f in CLASS_FEATURES.get(self.char_class, []):
            if f not in self.features:
                self.features.append(f)
        for eq in CLASS_EQUIPMENT.get(self.char_class, []):
            if eq not in self.equipment:
                self.equipment.append(eq)

    def __repr__(self):
        stats_str = ", ".join([f"{k.upper()}={v}" for k, v in self.stats.items()])
        return (f"<{self.char_class} {self.name} (LVL={self.level}, HP={self.hp_current}/{self.hp_max}, "
                f"RAСА={self.race}, CTRL={self.controller}) | {stats_str}>")



    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "char_class": self.char_class,
            "race": self.race,
            "stats": self.stats,
            "controller": self.controller,
            "level": self.level,
            "xp": self.xp,
            "background": self.background,
            "appearance": self.appearance,
            "features": self.features,
            "equipment": self.equipment,
            "hp_max": self.hp_max,
            "hp_current": self.hp_current,
            "current_scene": self.current_scene,
        }


    @classmethod
    def from_dict(cls, data: Dict):
        ent = cls(
            name=data["name"],
            char_class=data["char_class"],
            race=data["race"],
            stats=data["stats"],
            controller=data.get("controller", "player"),
            level=data.get("level", 1),
            xp=data.get("xp", 0),
            background=data.get("background", ""),
            appearance=data.get("appearance", {}),
            equipment=data.get("equipment", []),
            features=data.get("features", []),
            current_scene=data.get("current_scene"),  # <--- восстанавливаем сцену
        )
        ent.hp_max = data.get("hp_max", ent.hp_max)
        ent.hp_current = data.get("hp_current", ent.hp_current)
        return ent


    def is_alive(self) -> bool:
        return self.hp_current > 0

    def ability_modifier(self, score: int) -> int:
        return (score - 10) // 2

    def _calculate_max_hp(self) -> int:
        hd = CLASS_HIT_DIE.get(self.char_class, 8)
        con_mod = self.ability_modifier(self.stats.get("con", 10))
        return max(1, hd + con_mod)

    def add_xp(self, amount: int):
        self.xp += amount
        # простая система: 100 xp = уровень
        while self.xp >= 100 * self.level:
            self.level_up()

    def level_up(self):
        self.level += 1
        # для простоты прибавляем половину куба (rounded up) + con_mod
        hd = CLASS_HIT_DIE.get(self.char_class, 8)
        gained = (hd + 1) // 2 + self.ability_modifier(self.stats.get("con", 10))
        gained = max(1, gained)
        self.hp_max += gained
        self.hp_current += gained
        print(f"[LEVEL UP] {self.name} теперь уровень {self.level} (+{gained} HP).")
