import pygame


class DefaultBullet:
    """Класс со стандартной пулей"""

    def __init__(self, x, y, direction):
        """
        Инициализирует объект пули.
        :param x: Начальная координата X пули (int).
        :param y: Начальная координата Y пули (int).
        :param direction: Направление движения пули (0 - вверх, 180 - вниз, 90 - влево, -90 - вправо).
        Атрибуты:
            - self.x: Текущая координата X пули.
            - self.y: Текущая координата Y пули.
            - self.direction: Направление движения пули.
            - self.bullet_speed: Скорость движения пули (float).
            - self.bullet_image: Изображение пули (pygame.Surface).
            - self.can_break_wall: Флаг, указывающий, может ли пуля разрушать стены (bool).
            - self.fire: Флаг, указывающий, оставляет ли пуля огонь (bool).
            - self.damage: Урон, наносимый пулей (int).
        """
        self.x = x
        self.y = y
        self.direction = direction
        self.bullet_speed = 7.5
        self.bullet_image = pygame.image.load("../game_images/bullet.png")
        self.bullet_image = pygame.transform.scale(self.bullet_image, (30, 15))
        self.can_break_wall = False
        self.fire = False
        self.damage = 20

    def update(self, screen):
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
        if self.direction == 0:
            self.y -= self.bullet_speed
        if self.direction == 180:
            self.y += self.bullet_speed
        if self.direction == 90:
            self.x -= self.bullet_speed
        if self.direction == -90:
            self.x += self.bullet_speed
        rotated_bullet = pygame.transform.rotate(
            self.bullet_image, self.direction + 90
        )
        bullet_rect = rotated_bullet.get_rect(
            center=(int(self.x), int(self.y))
        )
        screen.blit(rotated_bullet, bullet_rect)
        return bullet_rect


class PlayerBullet(DefaultBullet):
    """
    Класс пользовательской пули
    """

    def __init__(self, x, y, direction):
        """
        Аналогично родительскому классу
        """
        super().__init__(x, y, direction)
        self.can_break_wall = True
        self.damage = 35


class ConcretePunchingBullet(DefaultBullet):
    """
    Класс пули способной ломать стены
    """

    def __init__(self, x, y, direction):
        """
        Аналогично родительскому классу
        """
        super().__init__(x, y, direction)
        self.can_break_wall = True


class IncendiaryBullet(DefaultBullet):
    """
    Класс зажигательной пули
    """

    def __init__(self, x, y, direction):
        """
        Аналогично родительскому классу
        """
        super().__init__(x, y, direction)
        self.fire = True


class WeakBullet(DefaultBullet):
    """
    Класс слабой пули
    """

    def __init__(self, x, y, direction):
        """
        Аналогично родительскому классу
        """
        super().__init__(x, y, direction)
        self.damage = 15
