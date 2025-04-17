import pygame


class Let:
    """
    Класс препятствия
    """

    def __init__(self, strength, x, y):
        """
        Инициализирует базовый объект препятствия.
        :param strength: Прочность препятствия (int). Определяет, сколько урона оно может выдержать.
        :param x: Координата X препятствия (int).
        :param y: Координата Y препятствия (int).
        Атрибуты:
            - self.strength: Прочность препятствия.
            - self.size: Размер препятствия в пикселях (по умолчанию 40).
            - self.image: Изображение препятствия (pygame.Surface). По умолчанию None.
            - self.x: Координата X препятствия.
            - self.y: Координата Y препятствия.
        """
        self.strength = strength
        self.size = 40
        self.image = None
        self.x = x
        self.y = y


class Brick(Let):
    """
    Препятствие - кирпич
    """

    def __init__(self, strength, x, y):
        """
        Аналогично родительскому
        """
        super().__init__(strength, x, y)
        self.strength = strength
        brick_image = pygame.image.load("../game_images/brick.png")
        self.image = pygame.transform.scale(
            brick_image, (self.size, self.size)
        )


class Ice(Let):
    """
    Препятствие - лёд
    """

    def __init__(self, x, y):
        """
        Аналогично родительскому
        """
        super().__init__(2, x, y)
        brick_image = pygame.image.load("../game_images/ice.png")
        self.image = pygame.transform.scale(
            brick_image, (self.size, self.size)
        )


class Water(Let):
    """
    Препятствие - вода
    """

    def __init__(self, x, y):
        """
        Аналогично родительскому
        """
        super().__init__(999, x, y)
        brick_image = pygame.image.load("../game_images/water.png")
        self.image = pygame.transform.scale(
            brick_image, (self.size, self.size)
        )


class Plant(Let):
    """
    Препятсвтие - растение
    """

    def __init__(self, x, y):
        """
        Аналогично родительскому
        """
        super().__init__(1, x, y)
        brick_image = pygame.image.load("../game_images/plant.png")
        self.image = pygame.transform.scale(
            brick_image, (self.size, self.size)
        )


class Rock(Let):
    """
    Препятствие - камень
    """

    def __init__(self, x, y):
        """
        Аналогично родительскому
        """
        super().__init__(5, x, y)
        brick_image = pygame.image.load("../game_images/rock.jpg")
        self.image = pygame.transform.scale(
            brick_image, (self.size, self.size)
        )
