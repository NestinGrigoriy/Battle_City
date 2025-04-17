class DefaultTank:
    """
    Класс с дефолтным танком
    """

    def __init__(self, x, y, bullet, direction, strategy):
        """
        Инициализирует базовый объект танка.
        :param x: Начальная координата X танка (int).
        :param y: Начальная координата Y танка (int).
        :param bullet: Объект пули, который использует танк.
        :param direction: Направление танка (0 - вверх, 180 - вниз, 90 - влево, -90 - вправо).
        :param strategy: Стратегия поведения танка (объект класса стратегии).
        Атрибуты:
            - self.direction: Направление танка.
            - self.x: Текущая координата X танка.
            - self.y: Текущая координата Y танка.
            - self.bullet: Объект пули, который использует танк.
            - self.speed: Скорость движения танка (по умолчанию 1).
            - self.attack_speed: Скорострельность танка (по умолчанию 2.5).
            - self.health_point: Здоровье танка (по умолчанию 80).
            - self.armor: Броня танка (по умолчанию 0).
            - self.strategy: Стратегия поведения танка.
            - self.last_shot: Время последнего выстрела (по умолчанию 0).
        """
        self.direction = direction
        self.x = x
        self.y = y
        self.bullet = bullet
        self.speed = 1
        self.attack_speed = 2.5
        self.health_point = 80
        self.armor = 0
        self.strategy = strategy
        self.last_shot = 0

    def update_last_shot(self, time):
        """
        Обновляет время последнего выстрела.
        :param time: Текущее время (float).
        Действия:
            - Устанавливает атрибут self.last_shot равным текущему времени.
        """
        self.last_shot = time


class PlayerTank(DefaultTank):
    """
    Пользовательский танк
    """

    def __init__(self, x, y, bullet, direction, strategy):
        """
        Изменяет некоторые параметры,
        Остальное аналогично родительскому
        """
        super().__init__(x, y, bullet, direction, strategy)
        self.speed = 2
        self.attack_speed = 1.25


class FastTank(DefaultTank):
    """
    Быстрый танк
    """

    def __init__(self, x, y, bullet, direction, strategy):
        """
        Изменяет некоторые параметры,
        Остальное аналогично родительскому
        """
        super().__init__(x, y, bullet, direction, strategy)
        self.speed = 1.5


class ArmorTank(DefaultTank):
    """
    Бронированный танк
    """

    def __init__(self, x, y, bullet, direction, strategy):
        """
        Изменяет некоторые параметры,
        Остальное аналогично родительскому
        """
        super().__init__(x, y, bullet, direction, strategy)
        self.armor = 50


class WeakTank(DefaultTank):
    """
    Слабый танк
    """

    def __init__(self, x, y, bullet, direction, strategy):
        """
        Изменяет некоторые параметры,
        Остальное аналогично родительскому
        """
        super().__init__(x, y, bullet, direction, strategy)
        self.bullet = bullet
        self.health_point = 50


class RapidFireTank(DefaultTank):
    """
    Скорострельный танк
    """

    def __init__(self, x, y, bullet, direction, strategy):
        """
        Изменяет некоторые параметры,
        Остальное аналогично родительскому
        """
        super().__init__(x, y, bullet, direction, strategy)
        self.attack_speed = 2
