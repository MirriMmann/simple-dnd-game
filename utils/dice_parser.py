# utils/dice_parser.py
import random
import re
from typing import Tuple, List

# Регулярка: "1d20", "2d6+3", "1d8-1"
DICE_RE = re.compile(r'^\s*(\d+)[dD](\d+)\s*([+-]\s*\d+)?\s*$')


def roll_dice(expr: str) -> Tuple[int, List[int]]:
    """
    Бросает кости по выражению вида "XdY(+Z)".
    Возвращает итог и список бросков.
    """
    m = DICE_RE.match(expr)
    if not m:
        raise ValueError("Неправильный формат кубов, ожидается XdY(+Z)")

    n = int(m.group(1))
    s = int(m.group(2))
    tail = m.group(3)  
    modifier = 0
    if tail:
        modifier = int(tail.replace(" ", ""))

    rolls = [random.randint(1, s) for _ in range(n)]
    total = sum(rolls) + modifier
    return total, rolls


def roll_4d6_drop_lowest() -> int:
    """
    Классическая генерация характеристики: 4d6, убираем минимальный.
    """
    rolls = [random.randint(1, 6) for _ in range(4)]
    rolls.sort()
    return sum(rolls[1:])


def roll_check(expr: str, dc: int, entity=None) -> tuple[bool, int, list[int]]:
    """
    Бросок для проверки.
    expr: '1d20+Сила'
    dc: целевое число
    entity: объект с entity.stats
    """
    modifier = 0
    if entity:
        for stat_name, stat_val in entity.stats.items():
            if stat_name in expr:
                modifier = (stat_val - 10) // 2
                # аккуратно заменяем характеристику на число,
                # убираем лишние плюсы
                expr = expr.replace("+" + stat_name, f"+{modifier}")
                expr = expr.replace("-" + stat_name, f"-{modifier}")
                break
    total, rolls = roll_dice(expr)
    success = total >= dc
    return success, total, rolls