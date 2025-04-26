import game.behavior_strategy
import game.bullets


class DefaultTank:
    """
    Класс с дефолтным танком
    """

    def __init__(self, x: int, y: int, bullet: game.bullets, direction: int, strategy: game.behavior_strategy):
        """
        Инициализирует базовый объект танка.
        :param x: Начальная координата X танка (int).
        :param y: Начальная координата Y танка (int).
        :param bullet: Объект пули, который использует танк.
        :param direction: Направление танка (0 - вверх, 180 - вниз, 90 - влево, -90 - вправо).
        :param strategy: Стратегия поведения танка (объект класса стратегии).
        Атрибуты:
            - self._direction: Направление танка.
            - self._x: Текущая координата X танка.
            - self._y: Текущая координата Y танка.
            - self.bullet: Объект пули, который использует танк.
            - self.speed: Скорость движения танка (по умолчанию 1).
            - self.attack_speed: Скорострельность танка (по умолчанию 2.5).
            - self.health_point: Здоровье танка (по умолчанию 80).
            - self.armor: Броня танка (по умолчанию 0).
            - self.strategy: Стратегия поведения танка.
            - self.last_shot: Время последнего выстрела (по умолчанию 0).
        """
        self._direction = direction
        self._x = x
        self._y = y
        self._bullet = bullet
        self._speed = 1
        self._attack_speed = 2.5
        self._health_point = 80
        self._armor = 0
        self._strategy = strategy
        self._last_shot = 0

    def get_x(self) -> float or int:
        """Геттер"""
        return self._x

    def get_y(self) -> float or int:
        """Геттер"""
        return self._y

    def get_bullet(self) -> game.bullets:
        """Геттер"""
        return self._bullet

    def get_strategy(self) -> game.behavior_strategy:
        """Геттер"""
        return self._strategy

    def get_direction(self) -> int:
        """Геттер"""
        return self._direction

    def get_speed(self) -> float:
        """Геттер"""
        return self._speed

    def get_attack_speed(self) -> float:
        """Геттер"""
        return self._attack_speed

    def get_armor(self) -> int or float:
        """Геттер"""
        return self._armor

    def get_health_point(self) -> int or float:
        """Геттер"""
        return self._health_point

    def get_last_shot(self) -> int:
        """Геттер"""
        return self._last_shot

    def set_x(self, x: int):
        """Сеттер"""
        self._x = x

    def set_y(self, y: int):
        """Сеттер"""
        self._y = y

    def set_direction(self, direction: int):
        """Сеттер"""
        self._direction = direction

    def set_speed(self, speed: int):
        """Сеттер"""
        self._speed = speed

    def set_armor(self, armor: int):
        """Сеттер"""
        self._armor = armor

    def set_health_point(self, hp: int):
        """Сеттер"""
        self._health_point = hp

    def update_last_shot(self, time: float):
        """
        Обновляет время последнего выстрела.
        :param time: Текущее время (float).
        Действия:
            - Устанавливает атрибут self.last_shot равным текущему времени.
        """
        self._last_shot = time


class PlayerTank(DefaultTank):
    """
    Пользовательский танк
    """

    def __init__(self, x: int, y: int, bullet: game.bullets, direction: int, strategy: game.behavior_strategy):
        """
        Изменяет некоторые параметры,
        Остальное аналогично родительскому
        """
        super().__init__(x, y, bullet, direction, strategy)
        self._speed = 2
        self._attack_speed = 1.25


class FastTank(DefaultTank):
    """
    Быстрый танк
    """

    def __init__(self, x: int, y: int, bullet: game.bullets, direction: int, strategy: game.behavior_strategy):
        """
        Изменяет некоторые параметры,
        Остальное аналогично родительскому
        """
        super().__init__(x, y, bullet, direction, strategy)
        self._speed = 1.5


class ArmorTank(DefaultTank):
    """
    Бронированный танк
    """

    def __init__(self, x: int, y: int, bullet: game.bullets, direction: int, strategy: game.behavior_strategy):
        """
        Изменяет некоторые параметры,
        Остальное аналогично родительскому
        """
        super().__init__(x, y, bullet, direction, strategy)
        self._armor = 50


class WeakTank(DefaultTank):
    """
    Слабый танк
    """

    def __init__(self, x: int, y: int, bullet: game.bullets, direction: int, strategy: game.behavior_strategy):
        """
        Изменяет некоторые параметры,
        Остальное аналогично родительскому
        """
        super().__init__(x, y, bullet, direction, strategy)
        self._bullet = bullet
        self._health_point = 50


class RapidFireTank(DefaultTank):
    """
    Скорострельный танк
    """

    def __init__(self, x: int, y: int, bullet: game.bullets, direction: int, strategy: game.behavior_strategy):
        """
        Изменяет некоторые параметры,
        Остальное аналогично родительскому
        """
        super().__init__(x, y, bullet, direction, strategy)
        self._attack_speed = 2
