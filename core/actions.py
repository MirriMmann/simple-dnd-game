import random
from core.checks import perform_check
from core.damage_system import apply_damage
from models.scenes import SCENES

from colorama import Fore, Style, init
init(autoreset=True)


def resolve_action(entity, action_key):
    for action in entity.current_scene["actions"]:
        key = action[0]
        label = action[1]
        next_scene = action[2] if len(action) > 2 else None
        extra = action[3] if len(action) > 3 else {}

        if key == action_key:
            # Если требуется проверка
            if "check" in extra:
                expr, _, dc = extra["check"].partition(" vs ")
                expr, dc = expr.strip(), int(dc.strip())

                success, total, rolls = perform_check(entity, expr, dc)

                if success:
                    print(Fore.GREEN + f"✅ Проверка успешна!"
                          + Fore.CYAN + f" ({total} против {dc}, броски: {rolls})")
                    if next_scene:
                        entity.current_scene = SCENES[next_scene]
                else:
                    print(Fore.RED + f"❌ Провал"
                          + Fore.CYAN + f" ({total} против {dc}, броски: {rolls})")
                    fail_scene = extra.get("fail_scene")
                    if fail_scene:
                        damage = random.randint(1, 3)
                        apply_damage(entity, damage)
                        if entity.is_alive():
                            entity.current_scene = SCENES[fail_scene]

            # Если это просто переход без проверки
            else:
                if next_scene:
                    print(Fore.YELLOW + f"➡ {entity.name}"
                          + Fore.WHITE + f" переходит в "
                          + Fore.MAGENTA + f"{next_scene}.")
                    entity.current_scene = SCENES[next_scene]
                else:
                    print(Fore.YELLOW + f"🏁 {entity.name}"
                          + Fore.WHITE + f" завершил путь действием "
                          + Fore.CYAN + f"{action_key}.")
            return

    # Если действие не найдено
    print(Fore.RED + f"⚠ {entity.name} сделал неизвестное действие "
          + Fore.CYAN + f"({action_key}).")
