from unittest.mock import MagicMock, patch

import pytest

# Импорты из вашего проекта
from game.bullets import ConcretePunchingBullet, DefaultBullet, IncendiaryBullet, PlayerBullet, WeakBullet


@pytest.fixture
def mock_screen():
    """Создает мок объекта экрана pygame."""
    return MagicMock()


@pytest.fixture
def default_bullet():
    """Создает экземпляр DefaultBullet."""
    return DefaultBullet(100, 200, 0)


class TestDefaultBullet:
    @patch("pygame.image.load")
    @patch("pygame.transform.scale")
    def test_initialization(self, mock_scale, mock_load):
        """Проверка инициализации DefaultBullet."""
        mock_image = MagicMock()
        mock_load.return_value = mock_image
        mock_scale.return_value = mock_image

        bullet = DefaultBullet(100, 200, 0)

        # Проверка атрибутов
        assert bullet._x == 100
        assert bullet._y == 200
        assert bullet._direction == 0
        assert bullet._bullet_speed == 7.5
        assert not bullet._can_break_wall
        assert not bullet._fire
        assert bullet._damage == 20

        # Проверка загрузки и масштабирования изображения
        mock_load.assert_called_once_with("../game_images/bullet.png")
        mock_scale.assert_called_once_with(mock_image, (30, 15))

    def test_update_movement(self, default_bullet, mock_screen):
        """Проверка обновления координат пули."""
        # Обновляем положение пули
        bullet_rect = default_bullet.update(mock_screen)

        # Проверяем новые координаты
        assert default_bullet._x == 100  # _x не меняется при _direction=0
        assert default_bullet._y == 200 - default_bullet._bullet_speed

        # Проверяем возвращаемое значение (bullet_rect)
        assert bullet_rect is not None
        assert bullet_rect.center == (int(default_bullet._x), int(default_bullet._y))

    def test_directions(self, mock_screen):
        """Проверка движения в разных направлениях."""
        directions = {
            0: (100, 200 - 7.5),  # Вверх
            180: (100, 200 + 7.5),  # Вниз
            90: (100 - 7.5, 200),  # Влево
            -90: (100 + 7.5, 200),  # Вправо
        }

        for direction, expected_coords in directions.items():
            bullet = DefaultBullet(100, 200, direction)
            bullet.update(mock_screen)
            assert (bullet._x, bullet._y) == expected_coords


@pytest.mark.parametrize(
    "cls, expected_can_break_wall, expected_fire, expected_damage",
    [
        (PlayerBullet, True, False, 35),
        (ConcretePunchingBullet, True, False, 20),
        (IncendiaryBullet, False, True, 20),
        (WeakBullet, False, False, 15),
    ],
)
class TestDerivedBullets:
    def test_initialization(self, cls, expected_can_break_wall, expected_fire, expected_damage):
        """Проверка инициализации производных классов."""
        bullet = cls(100, 200, 0)

        # Проверка атрибутов
        assert bullet._can_break_wall == expected_can_break_wall
        assert bullet._fire == expected_fire
        assert bullet._damage == expected_damage

    def test_inheritance(self, cls, expected_can_break_wall, expected_fire, expected_damage):
        """Проверка наследования."""
        bullet = cls(100, 200, 0)
        assert isinstance(bullet, DefaultBullet)


class TestSpecificBehavior:
    def test_player_bullet(self):
        """Проверка специфического поведения PlayerBullet."""
        bullet = PlayerBullet(100, 200, 0)
        assert bullet._can_break_wall
        assert not bullet._fire
        assert bullet._damage == 35

    def test_concrete_punching_bullet(self):
        """Проверка специфического поведения ConcretePunchingBullet."""
        bullet = ConcretePunchingBullet(100, 200, 0)
        assert bullet._can_break_wall
        assert not bullet._fire
        assert bullet._damage == 20

    def test_incendiary_bullet(self):
        """Проверка специфического поведения IncendiaryBullet."""
        bullet = IncendiaryBullet(100, 200, 0)
        assert not bullet._can_break_wall
        assert bullet._fire
        assert bullet._damage == 20

    def test_weak_bullet(self):
        """Проверка специфического поведения WeakBullet."""
        bullet = WeakBullet(100, 200, 0)
        assert not bullet._can_break_wall
        assert not bullet._fire
        assert bullet._damage == 15
