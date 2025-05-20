from typing import Any, Sequence, Iterator


class CyclicIterator:
    """
    Цикличный итератор
    """

    def __init__(self, collection: Sequence[Any]):
        """
        Инициализирует объект циклического итератора.
        :param collection: Последовательность, по которой будет выполняться циклическая итерация(например, list, tuple).
        Атрибуты:
            - self._collection: Последовательность, по которой происходит итерация.
            - self._index: Текущий индекс в последовательности.
        """
        self._collection = collection
        self._index = 0

    def __iter__(self) -> Iterator[Any]:
        """
        Возвращает сам объект итератора.
        :return: Сам объект циклического итератора.
        """
        return self

    def __next__(self) -> Any:
        """
        Возвращает следующий элемент последовательности в циклическом порядке.
        Если последовательность пустая, вызывает исключение StopIteration.
        :return: Следующий элемент последовательности.
        """
        if not self._collection:
            raise StopIteration
        result = self._collection[self._index]
        self._index = (self._index + 1) % len(self._collection)
        return result
