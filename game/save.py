import pickle

import pygame
from tank import PlayerTank


def save(
    lets: list,
    player_tank: PlayerTank,
    patrol_tanks: list,
    attackers: list,
    chasers: list,
    bonus: list,
    level_num: str,
    base_pos: tuple,
    base_health: int,
    map: list,
    SPAWN_X: int,
    SPAWN_Y: int,
):
    """
    Сохраняет текущий прогресс на уровне
    :param lets: препятствия
    :param player_tank: юзерский танк
    :param patrol_tanks: патрулирующие танки(массив)
    :param attackers: атакующие танки(массив)
    :param chasers: преследующие танки (массив)
    :param bonus: массив с бонусами
    :param level_num: номер уровня
    :param base_pos: позиция базы
    :param base_health: здоровье базы
    :param map: карта
    :param SPAWN_X: точка спавна по х
    :param SPAWN_Y: точка спавна по y
    """
    data = {
        "lets": lets,
        "player_tank": player_tank,
        "patrol_tanks": patrol_tanks,
        "attackers": attackers,
        "chasers": chasers,
        "bonus": bonus,
        "level_num": level_num,
        "base_pos": base_pos,
        "base_health": base_health,
        "map": map,
        "SPAWN_X": SPAWN_X,
        "SPAWN_Y": SPAWN_Y,
    }
    remove_surfaces(data)
    with open("savegame.pkl", "wb") as f:
        pickle.dump(data, f)
    exit()


def remove_surfaces(obj):
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
