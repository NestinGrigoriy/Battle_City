from typing import Union

import game.bullets
from game.behavior_strategy import ChaserStrategy
from game.bullets import DefaultBullet


class DefaultTank:
    def __init__(
        self,
        x: int,
        y: int,
        bullet: DefaultBullet,
        direction: int,
        strategy: game.behavior_strategy.ChaserStrategy,
    ):
        """
        Инициализатор
        """
        self._direction = direction
        self._x = x
        self._y = y
        self._bullet = bullet
        self._speed: float = 1.0
        self._attack_speed: float = 2.5
        self._health_point: float = 80
        self._armor: float = 0
        self._strategy = strategy
        self._last_shot: float = 0.0

    def get_x(self) -> Union[float, int]:
        """
        Геттер
        """
        return self._x

    def get_y(self) -> Union[float, int]:
        """
        Геттер
        """
        return self._y

    def get_bullet(self) -> DefaultBullet:
        """
        Геттер
        """
        return self._bullet

    def get_strategy(self) -> game.behavior_strategy.ChaserStrategy:
        """
        Геттер
        """
        return self._strategy

    def get_direction(self) -> int:
        """
        Геттер
        """
        return self._direction

    def get_speed(self) -> float:
        """
        Геттер
        """
        return self._speed

    def get_attack_speed(self) -> float:
        """
        Геттер
        """
        return self._attack_speed

    def get_armor(self) -> float:
        """
        Геттер
        """
        return self._armor

    def get_health_point(self) -> float:
        """
        Геттер
        """
        return self._health_point

    def get_last_shot(self) -> float:
        """
        Геттер
        """
        return self._last_shot

    def set_x(self, x: int) -> None:
        """
        Сеттер
        """
        self._x = x

    def set_y(self, y: int) -> None:
        """
        Сеттер
        """
        self._y = y

    def set_direction(self, direction: int) -> None:
        """
        Сеттер
        """
        self._direction = direction

    def set_speed(self, speed: float) -> None:
        """
        Сеттер
        """
        self._speed = speed

    def set_armor(self, armor: Union[int, float]) -> None:
        """
        Сеттер
        """
        self._armor = armor

    def set_health_point(self, hp: Union[int, float]) -> None:
        """
        Сеттер
        """
        self._health_point = hp

    def update_last_shot(self, time: float) -> None:
        """
        Обновляет время последнего выстрела
        """
        self._last_shot = time


class PlayerTank(DefaultTank):
    """
    Пользовательский танк
    """

    def __init__(
        self,
        x: int,
        y: int,
        bullet: DefaultBullet,
        direction: int,
        strategy: ChaserStrategy,
    ):
        """
        Инициализатор
        """
        super().__init__(x, y, bullet, direction, strategy)
        self._speed = 2
        self._attack_speed = 1.25


class FastTank(DefaultTank):
    """
    Быстрый танк
    """

    def __init__(
        self,
        x: int,
        y: int,
        bullet: DefaultBullet,
        direction: int,
        strategy: ChaserStrategy,
    ):
        """
        Инициализатор
        """
        super().__init__(x, y, bullet, direction, strategy)
        self._speed = 1.5


class ArmorTank(DefaultTank):
    """
    Бронированный танк
    """

    def __init__(
        self,
        x: int,
        y: int,
        bullet: DefaultBullet,
        direction: int,
        strategy: "game.behavior_strategy.ChaserStrategy",
    ):
        """
        Инициализатор
        """
        super().__init__(x, y, bullet, direction, strategy)
        self._armor = 50


class WeakTank(DefaultTank):
    """
    Слабый танк
    """

    def __init__(
        self,
        x: int,
        y: int,
        bullet: DefaultBullet,
        direction: int,
        strategy: "game.behavior_strategy.ChaserStrategy",
    ):
        """
        Инициализатор
        """
        super().__init__(x, y, bullet, direction, strategy)
        self._health_point = 50


class RapidFireTank(DefaultTank):
    """
    Скорострельный танк
    """

    def __init__(
        self,
        x: int,
        y: int,
        bullet: DefaultBullet,
        direction: int,
        strategy: ChaserStrategy,
    ):
        """
        Инициализатор
        """
        super().__init__(x, y, bullet, direction, strategy)
        self._attack_speed = 2
