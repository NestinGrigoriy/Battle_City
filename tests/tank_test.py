from unittest.mock import MagicMock

import pytest

from game.behavior_strategy import PatrolStrategy

# Импорты из вашего проекта
from game.tank import ArmorTank, DefaultTank, FastTank, PlayerTank, RapidFireTank, WeakTank


@pytest.fixture
def mock_bullet():
    """Создает мок объекта пули."""
    return MagicMock()


@pytest.fixture
def mock_strategy():
    """Создает мок объекта стратегии."""
    return PatrolStrategy(x=0, y=0, fin_x=100, fin_y=100)


class TestDefaultTank:
    @pytest.fixture
    def default_tank(self, mock_bullet, mock_strategy):
        """Создает экземпляр DefaultTank."""
        return DefaultTank(x=50, y=50, bullet=mock_bullet, direction=0, strategy=mock_strategy)

    def test_initialization(self, default_tank, mock_bullet, mock_strategy):
        """Проверка инициализации."""
        assert default_tank._x == 50
        assert default_tank._y == 50
        assert default_tank._direction == 0
        assert default_tank._speed == 1
        assert default_tank._attack_speed == 2.5
        assert default_tank._health_point == 80
        assert default_tank._armor == 0
        assert isinstance(default_tank._strategy, PatrolStrategy)

    def test_update_last_shot(self, default_tank):
        """Проверка обновления времени последнего выстрела."""
        default_tank.update_last_shot(10)
        assert default_tank._last_shot == 10


class TestPlayerTank:
    @pytest.fixture
    def player_tank(self, mock_bullet, mock_strategy):
        """Создает экземпляр PlayerTank."""
        return PlayerTank(x=50, y=50, bullet=mock_bullet, direction=0, strategy=mock_strategy)

    def test_initialization(self, player_tank, mock_bullet, mock_strategy):
        """Проверка инициализации."""
        assert player_tank._x == 50
        assert player_tank._y == 50
        assert player_tank._direction == 0
        assert player_tank._speed == 2  # Увеличенная скорость
        assert player_tank._attack_speed == 1.25  # Уменьшенная задержка атаки
        assert player_tank._health_point == 80
        assert player_tank._armor == 0
        assert isinstance(player_tank._strategy, PatrolStrategy)

    def test_inheritance(self, player_tank):
        """Проверка наследования."""
        assert isinstance(player_tank, DefaultTank)


class TestFastTank:
    @pytest.fixture
    def fast_tank(self, mock_bullet, mock_strategy):
        """Создает экземпляр FastTank."""
        return FastTank(x=50, y=50, bullet=mock_bullet, direction=0, strategy=mock_strategy)

    def test_initialization(self, fast_tank, mock_bullet, mock_strategy):
        """Проверка инициализации."""
        assert fast_tank._x == 50
        assert fast_tank._y == 50
        assert fast_tank._direction == 0
        assert fast_tank._speed == 1.5  # Увеличенная скорость
        assert fast_tank._attack_speed == 2.5
        assert fast_tank._health_point == 80
        assert fast_tank._armor == 0
        assert isinstance(fast_tank._strategy, PatrolStrategy)

    def test_inheritance(self, fast_tank):
        """Проверка наследования."""
        assert isinstance(fast_tank, DefaultTank)


class TestArmorTank:
    @pytest.fixture
    def armor_tank(self, mock_bullet, mock_strategy):
        """Создает экземпляр ArmorTank."""
        return ArmorTank(x=50, y=50, bullet=mock_bullet, direction=0, strategy=mock_strategy)

    def test_initialization(self, armor_tank, mock_bullet, mock_strategy):
        """Проверка инициализации."""
        assert armor_tank._x == 50
        assert armor_tank._y == 50
        assert armor_tank._direction == 0
        assert armor_tank._speed == 1
        assert armor_tank._attack_speed == 2.5
        assert armor_tank._health_point == 80
        assert armor_tank._armor == 50  # Броня добавлена
        assert isinstance(armor_tank._strategy, PatrolStrategy)

    def test_inheritance(self, armor_tank):
        """Проверка наследования."""
        assert isinstance(armor_tank, DefaultTank)


class TestWeakTank:
    @pytest.fixture
    def weak_tank(self, mock_bullet, mock_strategy):
        """Создает экземпляр WeakTank."""
        return WeakTank(x=50, y=50, bullet=mock_bullet, direction=0, strategy=mock_strategy)

    def test_initialization(self, weak_tank, mock_bullet, mock_strategy):
        """Проверка инициализации."""
        assert weak_tank._x == 50
        assert weak_tank._y == 50
        assert weak_tank._direction == 0
        assert weak_tank._speed == 1
        assert weak_tank._attack_speed == 2.5
        assert weak_tank._health_point == 50  # Уменьшено здоровье
        assert weak_tank._armor == 0
        assert isinstance(weak_tank._strategy, PatrolStrategy)

    def test_inheritance(self, weak_tank):
        """Проверка наследования."""
        assert isinstance(weak_tank, DefaultTank)


class TestRapidFireTank:
    @pytest.fixture
    def rapid_fire_tank(self, mock_bullet, mock_strategy):
        """Создает экземпляр RapidFireTank."""
        return RapidFireTank(x=50, y=50, bullet=mock_bullet, direction=0, strategy=mock_strategy)

    def test_initialization(self, rapid_fire_tank, mock_bullet, mock_strategy):
        """Проверка инициализации."""
        assert rapid_fire_tank._x == 50
        assert rapid_fire_tank._y == 50
        assert rapid_fire_tank._direction == 0
        assert rapid_fire_tank._speed == 1
        assert rapid_fire_tank._attack_speed == 2  # Уменьшенная задержка атаки
        assert rapid_fire_tank._health_point == 80
        assert rapid_fire_tank._armor == 0
        assert isinstance(rapid_fire_tank._strategy, PatrolStrategy)

    def test_inheritance(self, rapid_fire_tank):
        """Проверка наследования."""
        assert isinstance(rapid_fire_tank, DefaultTank)
