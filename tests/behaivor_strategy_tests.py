import pygame
import pytest

from game.behavior_strategy import AttackerStrategy, ChaserStrategy, PatrolStrategy


@pytest.fixture(autouse=True)
def setup_pygame():
    """Инициализация Pygame перед каждым тестом."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def mock_screen():
    """Создает фиктивный экран для тестирования."""
    return pygame.Surface((800, 600))


class TestPatrolStrategy:
    @pytest.fixture
    def patrol(self):
        """Создает экземпляр PatrolStrategy."""
        return PatrolStrategy(x=0, y=0, fin_x=100, fin_y=100)

    def test_initial_position(self, patrol):
        """Проверка начальных координат."""
        assert patrol._x == 0
        assert patrol._y == 0

    def test_update_movement(self, patrol, mock_screen):
        """Проверка обновления координат."""
        # Первый вызов update: движение по оси X
        patrol.update(mock_screen, speed=10, hp=100, armor=50)
        assert patrol._x == 10  # Движение по оси X
        assert patrol._current_axis == "_x"

        # Продолжаем движение до конца оси X
        for _ in range(9):
            patrol.update(mock_screen, speed=10, hp=100, armor=50)
        assert patrol._x == 100
        patrol.update(mock_screen, speed=10, hp=100, armor=50)
        assert patrol._current_axis == "_y"  # Переключение на ось Y

        # Движение по оси Y
        patrol.update(mock_screen, speed=10, hp=100, armor=50)
        assert patrol._y == 20

    def test_set_new_point(self, patrol):
        """Проверка установки новой точки."""
        patrol.set_new_point(200, 200)
        assert patrol._fin_x == 200
        assert patrol._fin_y == 200


class TestAttackerStrategy:
    @pytest.fixture
    def map_data(self):
        """Карта для тестирования."""
        return [
            "bbbbbbbb",
            "b      b",
            "b      b",
            "b      b",
            "b      b",
            "bbbbbbbb",
        ]

    @pytest.fixture
    def attacker(self, map_data):
        """Создает экземпляр AttackerStrategy."""
        return AttackerStrategy(40, 40, 80, 80)

    def test_attacker_initialization(self, attacker):
        """Проверка инициализации."""
        assert attacker._x == 40
        assert attacker._y == 40

    def test_attacker_find_path(self, attacker, map_data):
        """Проверка поиска пути."""
        start = (2, 2)
        end = (5, 4)
        attacker.find_path(map_data, start, end)
        assert attacker._path is not None
        assert isinstance(attacker._path, list)
        assert len(attacker._path) > 0

    def test_attacker_update_moves(self, attacker, mock_screen):
        """Проверка обновления координат."""
        attacker._path = [(120, 40), (160, 40)]
        attacker._fin_x = 120
        attacker._fin_y = 40
        old_x = attacker._x

        attacker.update(mock_screen, speed=10, hp=100, armor=50)
        assert attacker._x > old_x


class TestChaserStrategy:
    @pytest.fixture
    def map_data(self):
        """Карта для тестирования."""
        return [
            "bbbbbbbb",
            "b      b",
            "b      b",
            "b      b",
            "b      b",
            "bbbbbbbb",
        ]

    @pytest.fixture
    def chaser(self, map_data):
        """Создает экземпляр ChaserStrategy."""
        return ChaserStrategy(x=150, y=150, map_data=map_data)

    def test_chaser_initialization(self, chaser):
        """Проверка инициализации."""
        assert chaser._x == 150  # Используем объект из фикстуры
        assert chaser._y == 150

    def test_chaser_pathfinding(self, chaser):
        """Проверка поиска пути."""
        start = (2, 2)
        goal = (4, 5)
        path = chaser.a_star_search(start, goal)
        assert path is not None
        assert isinstance(path, list)
        assert len(path) > 0

    def test_chaser_update_moves(self, chaser, mock_screen):
        """Проверка обновления координат."""
        old_x, old_y = chaser._x, chaser._y
        player_x, player_y = 200, 150

        # Делаем update один раз
        chaser.update(
            mock_screen,
            speed=10,
            hp=100,
            armor=50,
            player_x=player_x,
            player_y=player_y,
        )

        # Ожидаем, что координаты изменились
        moved = chaser._x != old_x or chaser._y != old_y
        assert moved is True
