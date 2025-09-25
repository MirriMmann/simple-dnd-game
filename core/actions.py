import random
from core.checks import perform_check
from core.damage_system import apply_damage
from models.scenes import SCENES

def resolve_action(entity, action_key):
    for action in entity.current_scene["actions"]:
        key = action[0]
        label = action[1]
        next_scene = action[2] if len(action) > 2 else None
        extra = action[3] if len(action) > 3 else {}

        if key == action_key:
            if "check" in extra:
                expr, _, dc = extra["check"].partition(" vs ")
                expr, dc = expr.strip(), int(dc.strip())

                success, total, rolls = perform_check(entity, expr, dc)

                if success:
                    print(f"✅ Проверка успешна! ({total} против {dc}, броски: {rolls})")
                    if next_scene:
                        entity.current_scene = SCENES[next_scene]
                else:
                    print(f"❌ Провал ({total} против {dc}, броски: {rolls})")
                    fail_scene = extra.get("fail_scene")
                    if fail_scene:
                        damage = random.randint(1, 3)
                        apply_damage(entity, damage)
                        if entity.is_alive():
                            entity.current_scene = SCENES[fail_scene]
            else:
                if next_scene:
                    entity.current_scene = SCENES[next_scene]
                    print(f"{entity.name} переходит в {next_scene}.")
                else:
                    print(f"{entity.name} завершил путь действием {action_key}.")
            return

    print(f"{entity.name} сделал неизвестное действие ({action_key}).")
