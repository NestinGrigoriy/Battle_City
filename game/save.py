import pickle
import sys

import pygame
from typing import List, Dict, Any, Optional, Tuple

from tank import PlayerTank


def save(
    lets: List[Any],
    player_tank: PlayerTank,
    patrol_tanks: List[Any],
    attackers: List[Any],
    chasers: List[Any] | None,
    bonus: Optional[Dict[str, Optional[Tuple[int, int]]]],
    level_num: str,
    base_pos: tuple[int, int] | None,
    base_health: int,
    map_data: List[str],
    SPAWN_X: int | None,
    SPAWN_Y: int | None,
) -> None:
    """
    Сохраняет текущий прогресс на уровне
    :param lets: препятствия
    :param player_tank: юзерский танк
    :param patrol_tanks: патрулирующие танки (массив)
    :param attackers: атакующие танки (массив)
    :param chasers: преследующие танки (массив)
    :param bonus: массив с бонусами
    :param level_num: номер уровня
    :param base_pos: позиция базы
    :param base_health: здоровье базы
    :param map_data: карта
    :param SPAWN_X: точка спавна по x
    :param SPAWN_Y: точка спавна по y
    """
    data: Dict[str, Any] = {
        "lets": lets,
        "player_tank": player_tank,
        "patrol_tanks": patrol_tanks,
        "attackers": attackers,
        "chasers": chasers,
        "bonus": bonus,
        "level_num": level_num,
        "base_pos": base_pos,
        "base_health": base_health,
        "map": map_data,
        "SPAWN_X": SPAWN_X,
        "SPAWN_Y": SPAWN_Y,
    }
    remove_surfaces(data)

    with open("savegame.pkl", "wb") as f:
        pickle.dump(data, f)
    sys.exit()


def remove_surfaces(obj: Any) -> None:
    """
    Рекурсивно удаляет все pygame.Surface из объекта.
    """
    if isinstance(obj, dict):
        for k in list(obj.keys()):
            if isinstance(obj[k], pygame.Surface):
                del obj[k]
            else:
                remove_surfaces(obj[k])
    elif isinstance(obj, (list, tuple, set)):
        for item in obj:
            remove_surfaces(item)
    elif hasattr(obj, "__dict__"):
        to_delete = [k for k, v in obj.__dict__.items() if isinstance(v, pygame.Surface)]
        for k in to_delete:
            del obj.__dict__[k]
        for k in dir(obj):
            if not k.startswith("__") and not callable(getattr(obj, k)):
                remove_surfaces(getattr(obj, k))
