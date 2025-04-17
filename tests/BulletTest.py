import unittest
from unittest.mock import MagicMock

from game.Bullet import (
    ConcretePunchingBullet,
    DefaultBullet,
    IncendiaryBullet,
    PlayerBullet,
    WeakBullet,
)


class TestBullet(unittest.TestCase):
    def setUp(self):
        # Создаем объект DefaultBullet
        self.bullet = DefaultBullet(x=100, y=100, direction=0)

    def test_initialization(self):
        """Проверка инициализации."""
        self.assertEqual(self.bullet.x, 100)
        self.assertEqual(self.bullet.y, 100)
        self.assertEqual(self.bullet.direction, 0)
        self.assertEqual(self.bullet.bullet_speed, 7.5)
        self.assertFalse(self.bullet.can_break_wall)
        self.assertFalse(self.bullet.fire)
        self.assertEqual(self.bullet.damage, 20)

    def test_update_movement(self):
        """Проверка обновления координат."""
        mock_screen = MagicMock()

        # Обновляем положение пули
        bullet_rect = self.bullet.update(mock_screen)

        # Проверяем новые координаты
        self.assertEqual(self.bullet.x, 100)  # x не меняется при direction=0
        self.assertEqual(self.bullet.y, 100 - self.bullet.bullet_speed)

        # Проверяем возвращаемое значение (bullet_rect)
        self.assertIsNotNone(bullet_rect)
        self.assertEqual(
            bullet_rect.center, (int(self.bullet.x), int(self.bullet.y))
        )

    def test_directions(self):
        """Проверка движения в разных направлениях."""
        directions = {
            0: (100, 100 - self.bullet.bullet_speed),  # Вверх
            180: (100, 100 + self.bullet.bullet_speed),  # Вниз
            90: (100 - self.bullet.bullet_speed, 100),  # Влево
            -90: (100 + self.bullet.bullet_speed, 100),  # Вправо
        }

        for direction, expected_coords in directions.items():
            self.bullet.__init__(x=100, y=100, direction=direction)
            mock_screen = MagicMock()
            self.bullet.update(mock_screen)
            self.assertEqual((self.bullet.x, self.bullet.y), expected_coords)

    def test_player_bullet_inheritance(self):
        """Проверка, что PlayerBullet наследуется от DefaultBullet."""
        bullet = PlayerBullet(x=100, y=100, direction=0)
        self.assertIsInstance(bullet, DefaultBullet)

    def test_concrete_punching_bullet_inheritance(self):
        """Проверка, что ConcretePunchingBullet наследуется от DefaultBullet."""
        bullet = ConcretePunchingBullet(x=100, y=100, direction=0)
        self.assertIsInstance(bullet, DefaultBullet)

    def test_incendiary_bullet_inheritance(self):
        """Проверка, что IncendiaryBullet наследуется от DefaultBullet."""
        bullet = IncendiaryBullet(x=100, y=100, direction=0)
        self.assertIsInstance(bullet, DefaultBullet)

    def test_weak_bullet_inheritance(self):
        """Проверка, что WeakBullet наследуется от DefaultBullet."""
        bullet = WeakBullet(x=100, y=100, direction=0)
        self.assertIsInstance(bullet, DefaultBullet)
