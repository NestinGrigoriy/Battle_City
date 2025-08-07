from dataclasses import dataclass, field

import pygame


@dataclass
class DefaultBullet:
    """Класс со стандартной пулей"""

    _x: float
    _y: float
    _direction: int
    _bullet_speed: float = 7.5
    _can_break_wall: bool = False
    _fire: bool = False
    _damage: int = 20

    def __post_init__(self) -> None:
        """
        Инициализация дополнительных атрибутов после создания объекта.
        """
        self._bullet_image = pygame.image.load("../game_images/bullet.png")
        self._transform_bullet_image = pygame.transform.scale(self._bullet_image, (30, 15))

    def get_x(self) -> float:
        """Геттер"""
        return self._x

    def set_x(self, x: int) -> None:
        """Сеттер"""
        self._x = x

    def get_y(self) -> float:
        """Геттер"""
        return self._y

    def set_y(self, y: int) -> None:
        """Сеттер"""
        self._y = y

    def get_fire(self) -> bool:
        """Геттер"""
        return self._fire

    def get_can_break_wall(self) -> bool:
        """Геттер"""
        return self._can_break_wall

    def get_damage(self) -> int:
        """Геттер"""
        return self._damage

    def update(self, screen: pygame.Surface) -> pygame.Rect:
        """
        Обновляет положение пули на экране и отрисовывает её.
        :param screen: Экран, на котором отображается пуля (pygame.Surface).
        Действия:
            - Перемещает пулю в зависимости от её направления.
            - Поворачивает изображение пули согласно направлению.
            - Отрисовывает пулю на экране.
        Возвращаемое значение:
            - Rect пули (pygame.Rect).
        """
        if self._direction == 0:
            self._y -= self._bullet_speed
        elif self._direction == 180:
            self._y += self._bullet_speed
        elif self._direction == 90:
            self._x -= self._bullet_speed
        elif self._direction == -90:
            self._x += self._bullet_speed

        rotated_bullet = pygame.transform.rotate(self._transform_bullet_image, self._direction + 90)
        bullet_rect = rotated_bullet.get_rect(center=(int(self._x), int(self._y)))
        screen.blit(rotated_bullet, bullet_rect)
        return bullet_rect


@dataclass
class PlayerBullet(DefaultBullet):
    """
    Класс пользовательской пули
    """

    _can_break_wall: bool = field(default=True, init=False)
    _damage: int = field(default=35, init=False)


@dataclass
class ConcretePunchingBullet(DefaultBullet):
    """
    Класс пули способной ломать стены
    """

    _can_break_wall: bool = field(default=True, init=False)


@dataclass
class IncendiaryBullet(DefaultBullet):
    """
    Класс зажигательной пули
    """

    _fire: bool = field(default=True, init=False)


@dataclass
class WeakBullet(DefaultBullet):
    """
    Класс слабой пули
    """

    _damage: int = field(default=15, init=False)
