class CyclicIterator:
    def __init__(self, collection):
        self.collection = collection
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if not self.collection:
            raise StopIteration  # Если коллекция пустая
        result = self.collection[self.index]
        self.index = (self.index + 1) % len(self.collection)  # Зацикливаем индекс
        return result