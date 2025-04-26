from dataclasses import dataclass, field

import pygame


@dataclass
class Let:
    """
    Класс препятствия
    """

    _strength: int
    _x: int
    _y: int
    _size: int = 40
    _image: pygame.Surface = field(default=None, init=False)
    _transform_image: pygame.Surface = field(default=None, init=False)

    def __post_init__(self):
        """
        Инициализация дополнительных атрибутов после создания объекта.
        """
        self._image = None
        self._transform_image = None

    def get_strength(self) -> int:
        """Геттер"""
        return self._strength

    def set_strength(self, strength: int):
        """Сеттер"""
        self._strength = strength

    def set_x(self, x: int):
        """Сеттер"""
        self._x = x

    def get_x(self) -> int:
        """Геттер"""
        return self._x

    def set_y(self, y: int):
        """Сеттер"""
        self._y = y

    def get_y(self) -> int:
        """Геттер"""
        return self._y

    def get_transform_image(self) -> pygame.Surface:
        """Геттер"""
        return self._transform_image


@dataclass
class Brick(Let):
    """
    Препятствие - кирпич
    """

    def __post_init__(self):
        """
        Инициализация изображения кирпича.
        """
        super().__post_init__()
        brick_image = pygame.image.load("../game_images/brick.png")
        self._transform_image = pygame.transform.scale(brick_image, (self._size, self._size))


@dataclass
class Ice(Let):
    """
    Препятствие - лёд
    """

    def __post_init__(self):
        """
        Инициализация изображения льда.
        """
        super().__post_init__()
        ice_image = pygame.image.load("../game_images/ice.png")
        self._transform_image = pygame.transform.scale(ice_image, (self._size, self._size))


@dataclass
class Water(Let):
    """
    Препятствие - вода
    """

    def __post_init__(self):
        """
        Инициализация изображения воды.
        """
        super().__post_init__()
        water_image = pygame.image.load("../game_images/water.png")
        self._transform_image = pygame.transform.scale(water_image, (self._size, self._size))


@dataclass
class Plant(Let):
    """
    Препятствие - растение
    """

    def __post_init__(self):
        """
        Инициализация изображения растения.
        """
        super().__post_init__()
        plant_image = pygame.image.load("../game_images/plant.png")
        self._transform_image = pygame.transform.scale(plant_image, (self._size, self._size))


@dataclass
class Rock(Let):
    """
    Препятствие - камень
    """

    def __post_init__(self):
        """
        Инициализация изображения камня.
        """
        super().__post_init__()
        rock_image = pygame.image.load("../game_images/rock.jpg")
        self._transform_image = pygame.transform.scale(rock_image, (self._size, self._size))
