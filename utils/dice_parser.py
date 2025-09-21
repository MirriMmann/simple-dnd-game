# utils/dice_parser.py
import random
import re
from typing import Tuple, List


DICE_RE = re.compile(r'^\s*(\d+)[dD](\d+)\s*([+-]\s*\d+)?\s*$')


def roll_dice(expr: str) -> Tuple[int, List[int]]:

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
    """Классический метод генерации характеристики: 4d6 drop lowest"""
    rolls = [random.randint(1, 6) for _ in range(4)]
    rolls.sort()
    total = sum(rolls[1:])  # броски 1..4, drop lowest
    return total
