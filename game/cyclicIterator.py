from typing import Collection


class CyclicIterator:
    """
    Цикличный итератор
    """

    def __init__(self, collection: Collection):
        """
        Инициализирует объект циклического итератора.
        :param collection: Коллекция, по которой будет выполняться циклическая итерация (list, tuple и т.д.).
        Атрибуты:
            - self._collection: Коллекция, по которой происходит итерация.
            - self._index: Текущий индекс в коллекции.
        """
        self._collection = collection
        self._index = 0

    def __iter__(self) -> iter:
        """
        Возвращает сам объект итератора.
        :return: Сам объект циклического итератора.
        """
        return self

    def __next__(self) -> any:
        """
        Возвращает следующий элемент коллекции в циклическом порядке.
        Если коллекция пустая, вызывает исключение StopIteration.
        :return: Следующий элемент коллекции.
        """
        if not self._collection:
            raise StopIteration
        result = self._collection[self._index]
        self._index = (self._index + 1) % len(self._collection)
        return result
