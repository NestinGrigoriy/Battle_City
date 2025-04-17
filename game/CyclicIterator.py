class CyclicIterator:
    """
    Цикличный итератор
    """

    def __init__(self, collection):
        """
        Инициализирует объект циклического итератора.
        :param collection: Коллекция, по которой будет выполняться циклическая итерация (list, tuple и т.д.).
        Атрибуты:
            - self.collection: Коллекция, по которой происходит итерация.
            - self.index: Текущий индекс в коллекции.
        """
        self.collection = collection
        self.index = 0

    def __iter__(self):
        """
        Возвращает сам объект итератора.
        :return: Сам объект циклического итератора.
        """
        return self

    def __next__(self):
        """
        Возвращает следующий элемент коллекции в циклическом порядке.
        Если коллекция пустая, вызывает исключение StopIteration.
        :return: Следующий элемент коллекции.
        """
        if not self.collection:
            raise StopIteration
        result = self.collection[self.index]
        self.index = (self.index + 1) % len(self.collection)
        return result
