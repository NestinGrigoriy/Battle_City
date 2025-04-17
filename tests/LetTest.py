import unittest
from unittest.mock import MagicMock, patch

from game.Let import Brick, Ice, Let, Plant, Rock, Water


class TestLet(unittest.TestCase):
    def test_initialization(self):
        """Проверка инициализации базового класса."""
        let = Let(strength=5, x=100, y=200)
        self.assertEqual(let.strength, 5)
        self.assertEqual(let.size, 40)
        self.assertEqual(let.x, 100)
        self.assertEqual(let.y, 200)
        self.assertIsNone(let.image)  # image не загружается в базовом классе

    def test_image_not_loaded(self):
        """Проверка, что изображение не загружается в базовом классе."""
        let = Let(strength=5, x=100, y=200)
        self.assertIsNone(let.image)


class TestBrick(unittest.TestCase):
    @patch("pygame.image.load")
    @patch("pygame.transform.scale")
    def test_initialization(self, mock_scale, mock_load):
        """Проверка инициализации Brick."""
        mock_image = MagicMock()
        mock_load.return_value = mock_image
        mock_scale.return_value = mock_image

        brick = Brick(strength=3, x=100, y=200)

        # Проверка атрибутов
        self.assertEqual(brick.strength, 3)
        self.assertEqual(brick.size, 40)
        self.assertEqual(brick.x, 100)
        self.assertEqual(brick.y, 200)

        # Проверка загрузки и масштабирования изображения
        mock_load.assert_called_once_with("../game_images/brick.png")
        mock_scale.assert_called_once_with(mock_image, (40, 40))
        self.assertEqual(brick.image, mock_image)

    def test_inheritance(self):
        """Проверка наследования."""
        brick = Brick(strength=3, x=100, y=200)
        self.assertIsInstance(brick, Let)


class TestIce(unittest.TestCase):
    @patch("pygame.image.load")
    @patch("pygame.transform.scale")
    def test_initialization(self, mock_scale, mock_load):
        """Проверка инициализации Ice."""
        mock_image = MagicMock()
        mock_load.return_value = mock_image
        mock_scale.return_value = mock_image

        ice = Ice(x=100, y=200)

        # Проверка атрибутов
        self.assertEqual(ice.strength, 2)
        self.assertEqual(ice.size, 40)
        self.assertEqual(ice.x, 100)
        self.assertEqual(ice.y, 200)

        # Проверка загрузки и масштабирования изображения
        mock_load.assert_called_once_with("../game_images/ice.png")
        mock_scale.assert_called_once_with(mock_image, (40, 40))
        self.assertEqual(ice.image, mock_image)

    def test_inheritance(self):
        """Проверка наследования."""
        ice = Ice(x=100, y=200)
        self.assertIsInstance(ice, Let)


class TestWater(unittest.TestCase):
    @patch("pygame.image.load")
    @patch("pygame.transform.scale")
    def test_initialization(self, mock_scale, mock_load):
        """Проверка инициализации Water."""
        mock_image = MagicMock()
        mock_load.return_value = mock_image
        mock_scale.return_value = mock_image

        water = Water(x=100, y=200)

        # Проверка атрибутов
        self.assertEqual(water.strength, 999)
        self.assertEqual(water.size, 40)
        self.assertEqual(water.x, 100)
        self.assertEqual(water.y, 200)

        # Проверка загрузки и масштабирования изображения
        mock_load.assert_called_once_with("../game_images/water.png")
        mock_scale.assert_called_once_with(mock_image, (40, 40))
        self.assertEqual(water.image, mock_image)

    def test_inheritance(self):
        """Проверка наследования."""
        water = Water(x=100, y=200)
        self.assertIsInstance(water, Let)


class TestPlant(unittest.TestCase):
    @patch("pygame.image.load")
    @patch("pygame.transform.scale")
    def test_initialization(self, mock_scale, mock_load):
        """Проверка инициализации Plant."""
        mock_image = MagicMock()
        mock_load.return_value = mock_image
        mock_scale.return_value = mock_image

        plant = Plant(x=100, y=200)

        # Проверка атрибутов
        self.assertEqual(plant.strength, 1)
        self.assertEqual(plant.size, 40)
        self.assertEqual(plant.x, 100)
        self.assertEqual(plant.y, 200)

        # Проверка загрузки и масштабирования изображения
        mock_load.assert_called_once_with("../game_images/plant.png")
        mock_scale.assert_called_once_with(mock_image, (40, 40))
        self.assertEqual(plant.image, mock_image)

    def test_inheritance(self):
        """Проверка наследования."""
        plant = Plant(x=100, y=200)
        self.assertIsInstance(plant, Let)


class TestRock(unittest.TestCase):
    @patch("pygame.image.load")
    @patch("pygame.transform.scale")
    def test_initialization(self, mock_scale, mock_load):
        """Проверка инициализации Rock."""
        mock_image = MagicMock()
        mock_load.return_value = mock_image
        mock_scale.return_value = mock_image

        rock = Rock(x=100, y=200)

        # Проверка атрибутов
        self.assertEqual(rock.strength, 5)
        self.assertEqual(rock.size, 40)
        self.assertEqual(rock.x, 100)
        self.assertEqual(rock.y, 200)

        # Проверка загрузки и масштабирования изображения
        mock_load.assert_called_once_with("../game_images/rock.jpg")
        mock_scale.assert_called_once_with(mock_image, (40, 40))
        self.assertEqual(rock.image, mock_image)

    def test_inheritance(self):
        """Проверка наследования."""
        rock = Rock(x=100, y=200)
        self.assertIsInstance(rock, Let)
