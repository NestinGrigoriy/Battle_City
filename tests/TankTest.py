import unittest
from unittest.mock import MagicMock

from game.BehaviorStrategy import PatrolStrategy
from game.Tank import (
    ArmorTank,
    DefaultTank,
    FastTank,
    PlayerTank,
    RapidFireTank,
    WeakTank,
)


class TestDefaultTank(unittest.TestCase):
    def setUp(self):
        # Создаем объект DefaultTank
        self.strategy = PatrolStrategy(x=0, y=0, fin_x=100, fin_y=100)
        self.bullet = MagicMock()  # Mock-объект пули
        self.tank = DefaultTank(
            x=50, y=50, bullet=self.bullet, direction=0, strategy=self.strategy
        )

    def test_initialization(self):
        """Проверка инициализации."""
        self.assertEqual(self.tank.x, 50)
        self.assertEqual(self.tank.y, 50)
        self.assertEqual(self.tank.direction, 0)
        self.assertEqual(self.tank.speed, 1)
        self.assertEqual(self.tank.attack_speed, 2.5)
        self.assertEqual(self.tank.health_point, 80)
        self.assertEqual(self.tank.armor, 0)
        self.assertIsInstance(self.tank.strategy, PatrolStrategy)

    def test_update_last_shot(self):
        """Проверка обновления времени последнего выстрела."""
        self.tank.update_last_shot(10)
        self.assertEqual(self.tank.last_shot, 10)


class TestPlayerTank(unittest.TestCase):
    def setUp(self):
        # Создаем объект PlayerTank
        self.strategy = PatrolStrategy(x=0, y=0, fin_x=100, fin_y=100)
        self.bullet = MagicMock()  # Mock-объект пули
        self.tank = PlayerTank(
            x=50, y=50, bullet=self.bullet, direction=0, strategy=self.strategy
        )

    def test_initialization(self):
        """Проверка инициализации."""
        self.assertEqual(self.tank.x, 50)
        self.assertEqual(self.tank.y, 50)
        self.assertEqual(self.tank.direction, 0)
        self.assertEqual(self.tank.speed, 2)  # Увеличенная скорость
        self.assertEqual(
            self.tank.attack_speed, 2
        )  # Уменьшенная задержка атаки
        self.assertEqual(self.tank.health_point, 80)
        self.assertEqual(self.tank.armor, 0)
        self.assertIsInstance(self.tank.strategy, PatrolStrategy)

    def test_inheritance(self):
        """Проверка наследования."""
        self.assertIsInstance(self.tank, DefaultTank)


class TestFastTank(unittest.TestCase):
    def setUp(self):
        # Создаем объект FastTank
        self.strategy = PatrolStrategy(x=0, y=0, fin_x=100, fin_y=100)
        self.bullet = MagicMock()  # Mock-объект пули
        self.tank = FastTank(
            x=50, y=50, bullet=self.bullet, direction=0, strategy=self.strategy
        )

    def test_initialization(self):
        """Проверка инициализации."""
        self.assertEqual(self.tank.x, 50)
        self.assertEqual(self.tank.y, 50)
        self.assertEqual(self.tank.direction, 0)
        self.assertEqual(self.tank.speed, 1.5)  # Увеличенная скорость
        self.assertEqual(self.tank.attack_speed, 2.5)
        self.assertEqual(self.tank.health_point, 80)
        self.assertEqual(self.tank.armor, 0)
        self.assertIsInstance(self.tank.strategy, PatrolStrategy)

    def test_inheritance(self):
        """Проверка наследования."""
        self.assertIsInstance(self.tank, DefaultTank)


class TestArmorTank(unittest.TestCase):
    def setUp(self):
        # Создаем объект ArmorTank
        self.strategy = PatrolStrategy(x=0, y=0, fin_x=100, fin_y=100)
        self.bullet = MagicMock()  # Mock-объект пули
        self.tank = ArmorTank(
            x=50, y=50, bullet=self.bullet, direction=0, strategy=self.strategy
        )

    def test_initialization(self):
        """Проверка инициализации."""
        self.assertEqual(self.tank.x, 50)
        self.assertEqual(self.tank.y, 50)
        self.assertEqual(self.tank.direction, 0)
        self.assertEqual(self.tank.speed, 1)
        self.assertEqual(self.tank.attack_speed, 2.5)
        self.assertEqual(self.tank.health_point, 80)
        self.assertEqual(self.tank.armor, 50)  # Броня добавлена
        self.assertIsInstance(self.tank.strategy, PatrolStrategy)

    def test_inheritance(self):
        """Проверка наследования."""
        self.assertIsInstance(self.tank, DefaultTank)


class TestWeakTank(unittest.TestCase):
    def setUp(self):
        # Создаем объект WeakTank
        self.strategy = PatrolStrategy(x=0, y=0, fin_x=100, fin_y=100)
        self.bullet = MagicMock()  # Mock-объект пули
        self.tank = WeakTank(
            x=50, y=50, bullet=self.bullet, direction=0, strategy=self.strategy
        )

    def test_initialization(self):
        """Проверка инициализации."""
        self.assertEqual(self.tank.x, 50)
        self.assertEqual(self.tank.y, 50)
        self.assertEqual(self.tank.direction, 0)
        self.assertEqual(self.tank.speed, 1)
        self.assertEqual(self.tank.attack_speed, 2.5)
        self.assertEqual(self.tank.health_point, 50)  # Уменьшено здоровье
        self.assertEqual(self.tank.armor, 0)
        self.assertIsInstance(self.tank.strategy, PatrolStrategy)

    def test_inheritance(self):
        """Проверка наследования."""
        self.assertIsInstance(self.tank, DefaultTank)


class TestRapidFireTank(unittest.TestCase):
    def setUp(self):
        # Создаем объект RapidFireTank
        self.strategy = PatrolStrategy(x=0, y=0, fin_x=100, fin_y=100)
        self.bullet = MagicMock()  # Mock-объект пули
        self.tank = RapidFireTank(
            x=50, y=50, bullet=self.bullet, direction=0, strategy=self.strategy
        )

    def test_initialization(self):
        """Проверка инициализации."""
        self.assertEqual(self.tank.x, 50)
        self.assertEqual(self.tank.y, 50)
        self.assertEqual(self.tank.direction, 0)
        self.assertEqual(self.tank.speed, 1)
        self.assertEqual(
            self.tank.attack_speed, 2
        )  # Уменьшенная задержка атаки
        self.assertEqual(self.tank.health_point, 80)
        self.assertEqual(self.tank.armor, 0)
        self.assertIsInstance(self.tank.strategy, PatrolStrategy)

    def test_inheritance(self):
        """Проверка наследования."""
        self.assertIsInstance(self.tank, DefaultTank)
