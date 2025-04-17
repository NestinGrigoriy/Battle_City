import unittest

from game.CyclicIterator import CyclicIterator


class TestCyclicIterator(unittest.TestCase):
    def test_empty_collection(self):
        """Проверка поведения итератора с пустой коллекцией."""
        iterator = CyclicIterator([])
        with self.assertRaises(StopIteration):
            next(iterator)

    def test_single_element(self):
        """Проверка итерации по коллекции с одним элементом."""
        iterator = CyclicIterator([42])
        self.assertEqual(next(iterator), 42)
        self.assertEqual(next(iterator), 42)  # Зацикливание работает

    def test_multiple_elements(self):
        """Проверка итерации по коллекции с несколькими элементами."""
        collection = [1, 2, 3]
        iterator = CyclicIterator(collection)

        # Первый проход
        self.assertEqual(next(iterator), 1)
        self.assertEqual(next(iterator), 2)
        self.assertEqual(next(iterator), 3)

        # Второй проход (зацикливание)
        self.assertEqual(next(iterator), 1)
        self.assertEqual(next(iterator), 2)
        self.assertEqual(next(iterator), 3)

    def test_iter_method(self):
        """Проверка метода __iter__."""
        collection = [10, 20, 30]
        iterator = CyclicIterator(collection)

        # Убедимся, что метод __iter__ возвращает сам объект
        self.assertIs(iter(iterator), iterator)

    def test_modification_during_iteration(self):
        """Проверка поведения при изменении коллекции во время итерации."""
        collection = [1, 2, 3]
        iterator = CyclicIterator(collection)

        # Изменяем коллекцию
        collection.append(4)

        # Итерация продолжается с измененной коллекцией
        self.assertEqual(next(iterator), 1)
        self.assertEqual(next(iterator), 2)
        self.assertEqual(next(iterator), 3)
        self.assertEqual(next(iterator), 4)

    def test_negative_indexing(self):
        """Проверка, что индекс не становится отрицательным."""
        collection = [10, 20, 30]
        iterator = CyclicIterator(collection)

        # Исчерпываем коллекцию
        for _ in range(10):
            next(iterator)

        # Убедимся, что индекс остается в пределах длины коллекции
        self.assertEqual(
            iterator.index, 1
        )  # Примерное значение после 10 итераций
