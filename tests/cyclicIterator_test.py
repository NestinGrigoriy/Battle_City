import pytest

from game.cyclicIterator import CyclicIterator


@pytest.fixture
def cyclic_iterator_empty():
    """Создает CyclicIterator с пустой коллекцией."""
    return CyclicIterator([])


@pytest.fixture
def cyclic_iterator_single():
    """Создает CyclicIterator с коллекцией из одного элемента."""
    return CyclicIterator([42])


@pytest.fixture
def cyclic_iterator_multiple():
    """Создает CyclicIterator с коллекцией из нескольких элементов."""
    return CyclicIterator([1, 2, 3])


class TestCyclicIterator:
    def test_empty_collection(self, cyclic_iterator_empty):
        """Проверка поведения итератора с пустой коллекцией."""
        with pytest.raises(StopIteration):
            next(cyclic_iterator_empty)

    def test_single_element(self, cyclic_iterator_single):
        """Проверка итерации по коллекции с одним элементом."""
        assert next(cyclic_iterator_single) == 42
        assert next(cyclic_iterator_single) == 42  # Зацикливание работает

    def test_multiple_elements(self, cyclic_iterator_multiple):
        """Проверка итерации по коллекции с несколькими элементами."""
        iterator = cyclic_iterator_multiple

        # Первый проход
        assert next(iterator) == 1
        assert next(iterator) == 2
        assert next(iterator) == 3

        # Второй проход (зацикливание)
        assert next(iterator) == 1
        assert next(iterator) == 2
        assert next(iterator) == 3

    def test_iter_method(self, cyclic_iterator_multiple):
        """Проверка метода __iter__."""
        iterator = cyclic_iterator_multiple

        # Убедимся, что метод __iter__ возвращает сам объект
        assert iter(iterator) is iterator

    def test_modification_during_iteration(self):
        """Проверка поведения при изменении коллекции во время итерации."""
        collection = [1, 2, 3]
        iterator = CyclicIterator(collection)

        # Изменяем коллекцию
        collection.append(4)

        # Итерация продолжается с измененной коллекцией
        assert next(iterator) == 1
        assert next(iterator) == 2
        assert next(iterator) == 3
        assert next(iterator) == 4

    def test_negative_indexing(self):
        """Проверка, что индекс не становится отрицательным."""
        collection = [10, 20, 30]
        iterator = CyclicIterator(collection)

        # Исчерпываем коллекцию
        for _ in range(10):
            next(iterator)

        # Убедимся, что индекс остается в пределах длины коллекции
        assert iterator._index == 1  # Примерное значение после 10 итераций
