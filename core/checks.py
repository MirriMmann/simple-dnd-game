# core/checks.py
from utils.dice_parser import roll_check

def perform_check(entity, expr: str, dc: int) -> tuple[bool, int, list[int]]:
    """Выполняет проверку с кубами"""
    success, total, rolls = roll_check(expr, dc, entity)
    return success, total, rolls