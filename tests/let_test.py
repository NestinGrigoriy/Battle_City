from unittest.mock import MagicMock, patch

import pytest

from game.let import Brick, Ice, Let, Plant, Rock, Water


class TestLet:
    def test_initialization(self):
        """Проверка инициализации базового класса."""
        let = Let(5, 100, 200)
        assert let._strength == 5
        assert let._size == 40
        assert let._x == 100
        assert let._y == 200
        assert let._image is None  # Изображение не загружается в базовом классе

    def test_getters_and_setters(self):
        """Проверка геттеров и сеттеров."""
        let = Let(5, 100, 200)

        # Проверка strength
        assert let.get_strength() == 5
        let.set_strength(10)
        assert let.get_strength() == 10

        # Проверка x
        assert let.get_x() == 100
        let.set_x(150)
        assert let.get_x() == 150

        # Проверка y
        assert let.get_y() == 200
        let.set_y(250)
        assert let.get_y() == 250


@pytest.mark.parametrize(
    "cls, image_path, strength",
    [
        (Brick, "../game_images/brick.png", 3),
        (Ice, "../game_images/ice.png", 2),
        (Water, "../game_images/water.png", 999),
        (Plant, "../game_images/plant.png", 1),
        (Rock, "../game_images/rock.jpg", 5),
    ],
)
class TestDerivedClasses:
    @patch("pygame.image.load")
    @patch("pygame.transform.scale")
    def test_initialization(self, mock_scale, mock_load, cls, image_path, strength):
        """Проверка инициализации производных классов."""
        mock_image = MagicMock()
        mock_load.return_value = mock_image
        mock_scale.return_value = mock_image

        instance = cls(strength, 100, 200)

        # Проверка атрибутов
        assert instance._strength == strength
        assert instance._size == 40
        assert instance._x == 100
        assert instance._y == 200

        # Проверка загрузки и масштабирования изображения
        mock_load.assert_called_once_with(image_path)
        mock_scale.assert_called_once_with(mock_image, (40, 40))
        assert instance.get_transform_image() == mock_image

    def test_inheritance(self, cls, image_path, strength):
        """Проверка наследования."""
        instance = cls(3, 100, 200)
        assert isinstance(instance, Let)


class TestSpecificBehavior:
    @patch("pygame.image.load")
    @patch("pygame.transform.scale")
    def test_brick(self, mock_scale, mock_load):
        """Проверка специфического поведения Brick."""
        mock_image = MagicMock()
        mock_load.return_value = mock_image
        mock_scale.return_value = mock_image

        brick = Brick(3, 100, 200)

        # Проверка прочности
        assert brick.get_strength() == 3

        # Проверка изображения
        mock_load.assert_called_once_with("../game_images/brick.png")
        mock_scale.assert_called_once_with(mock_image, (40, 40))
        assert brick.get_transform_image() == mock_image

    @patch("pygame.image.load")
    @patch("pygame.transform.scale")
    def test_water(self, mock_scale, mock_load):
        """Проверка специфического поведения Water."""
        mock_image = MagicMock()
        mock_load.return_value = mock_image
        mock_scale.return_value = mock_image

        water = Water(999, 100, 200)

        # Проверка прочности
        assert water.get_strength() == 999

        # Проверка изображения
        mock_load.assert_called_once_with("../game_images/water.png")
        mock_scale.assert_called_once_with(mock_image, (40, 40))
        assert water.get_transform_image() == mock_image
