import unittest

import pygame

from game.BehaviorStrategy import (
    AttackerStrategy,
    ChaserStrategy,
    PatrolStrategy,
)


class TestPatrolStrategy(unittest.TestCase):
    def setUp(self):
        # Инициализация объекта PatrolStrategy
        self.patrol = PatrolStrategy(x=0, y=0, fin_x=100, fin_y=100)

    def test_initial_position(self):
        """Проверка начальных координат."""
        self.assertEqual(self.patrol.x, 0)
        self.assertEqual(self.patrol.y, 0)

    def test_update_movement(self):
        """Проверка обновления координат."""

        pygame.init()
        mock_screen = pygame.Surface((800, 600))

        # Первый вызов update: движение по оси X
        self.patrol.update(mock_screen, speed=10, hp=100, armor=50)
        self.assertEqual(self.patrol.x, 10)  # Движение по оси X
        self.assertEqual(self.patrol.current_axis, "x")

        # Продолжаем движение до конца оси X
        for _ in range(9):
            self.patrol.update(mock_screen, speed=10, hp=100, armor=50)
        self.assertEqual(self.patrol.x, 100)
        self.patrol.update(mock_screen, speed=10, hp=100, armor=50)
        self.assertEqual(
            self.patrol.current_axis, "y"
        )  # Переключение на ось Y

        # Движение по оси Y
        self.patrol.update(mock_screen, speed=10, hp=100, armor=50)
        self.assertEqual(self.patrol.y, 20)

    def test_set_new_point(self):
        """Проверка установки новой точки."""
        self.patrol.set_new_point(200, 200)
        self.assertEqual(self.patrol.fin_x, 200)
        self.assertEqual(self.patrol.fin_y, 200)


class TestAttackerStrategy(unittest.TestCase):
    def setUp(self):
        # Карта для тестирования
        self.map_data = [
            "bbbbbbbb",
            "b      b",
            "b      b",
            "b      b",
            "b      b",
            "bbbbbbbb",
        ]

    def test_attacker_initialization(self):
        strategy = AttackerStrategy(40, 40, 80, 80)
        self.assertEqual(strategy.x, 40)
        self.assertEqual(strategy.y, 40)

    def test_attacker_find_path(self):
        strategy = AttackerStrategy(40, 40, 200, 200)
        start = (2, 2)
        end = (5, 4)
        strategy.find_path(self.map_data, start, end)
        self.assertIsNotNone(strategy.path)
        self.assertIsInstance(strategy.path, list)
        self.assertGreater(len(strategy.path), 0)

    def test_attacker_update_moves(self):
        pygame.init()
        mock_screen = pygame.Surface((800, 400))
        strategy = AttackerStrategy(40, 40, 120, 40)
        strategy.path = [(120, 40), (160, 40)]
        strategy.fin_x = 120
        strategy.fin_y = 40
        old_x = strategy.x

        strategy.update(mock_screen, speed=10, hp=100, armor=50)
        self.assertGreater(strategy.x, old_x)


class TestChaserStrategy(unittest.TestCase):
    def setUp(self):
        # Карта для тестирования
        self.map_data = [
            "bbbbbbbb",
            "b      b",
            "b      b",
            "b      b",
            "b      b",
            "bbbbbbbb",
        ]
        self.chaser = ChaserStrategy(x=0, y=0, map_data=self.map_data)

    def test_chaser_initialization(self):
        strategy = ChaserStrategy(80, 80, self.map_data)
        self.assertEqual(strategy.x, 80)
        self.assertEqual(strategy.y, 80)

    def test_chaser_pathfinding(self):
        strategy = ChaserStrategy(80, 80, self.map_data)
        start = (2, 2)
        goal = (4, 5)
        path = strategy.a_star_search(start, goal)
        self.assertIsNotNone(path)
        self.assertIsInstance(path, list)
        self.assertGreater(len(path), 0)

    def test_chaser_update_moves(self):
        pygame.init()
        mock_screen = pygame.Surface((800, 500))
        strategy = ChaserStrategy(80, 80, self.map_data)
        old_x, old_y = strategy.x, strategy.y
        player_x, player_y = 200, 200

        # Делаем update один раз
        strategy.update(
            mock_screen,
            speed=10,
            hp=100,
            armor=50,
            player_x=player_x,
            player_y=player_y,
        )

        # Ожидаем, что координаты изменились
        moved = strategy.x != old_x or strategy.y != old_y
        self.assertTrue(moved)
