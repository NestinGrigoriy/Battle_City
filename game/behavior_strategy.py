import heapq
import math
from collections import deque

import pygame

"""
Класс со стратегией патрулирования местности
"""


class PatrolStrategy:
    def __init__(self, x: int, y: int, fin_x: int, fin_y):
        """
        Инициализирует объект стратегии патрулирования.
        :param x: Начальная координата X танка (int).
        :param y: Начальная координата Y танка (int).
        :param fin_x: Конечная координата X для патрулирования (int).
        :param fin_y: Конечная координата Y для патрулирования (int).
        Атрибуты:
            - self._x, self._y: Текущие координаты танка.
            - self._fin_x, self._fin_y: Целевые координаты для патрулирования.
            - self._angle: Угол поворота танка.
            - self._transform_image: Изображение танка.
            - self._current_axis: Текущая ось движения ("_x" или "_y").
        """
        self._x = x
        self._y = y
        self._fin_x = fin_x
        self._fin_y = fin_y
        self._angle = 0
        self._image = pygame.image.load("../game_images/opponent_tank.png")
        self._transform_image = pygame.transform.scale(self._image, (75, 75))
        self._current_axis = "_x"  # Текущая ось движения ('_x' или '_y')

    def get_x(self) -> int:
        """Геттер"""
        return self._x

    def set_x(self, x: int):
        """Сеттер"""
        self._x = x

    def get_y(self) -> int:
        """Геттер"""
        return self._y

    def set_y(self, y: int):
        """Сеттер"""
        self._y = y

    def get_angle(self) -> int:
        """Геттер"""
        return self._angle

    def get_transform_image(self) -> pygame.transform:
        """Геттер"""
        return self._transform_image

    def update(self, screen: pygame.Surface, speed: float, hp: int, armor: int) -> int or None:
        """
        Обновляет положение танка на экране и его состояние.
        :param screen: Экран, на котором отображается танк (pygame.Surface).
        :param speed: Скорость движения танка (float).
        :param hp: Здоровье танка (int).
        :param armor: Броня танка (int).
        Действия:
            - Перемещает танк по горизонтали или вертикали в зависимости от текущей оси движения.
            - Отображает танк на экране с учетом угла поворота.
            - Проверяет, достиг ли танк конечной точки.
        Возвращаемое значение:
            - -1, если танк достиг конечной точки.
        """
        if self._current_axis == "_x":
            if self._x < self._fin_x:
                self._x += speed
                self._angle = -90
            elif self._x > self._fin_x:
                self._x -= speed
                self._angle = 90
            else:
                self._current_axis = "_y"

        if self._current_axis == "_y":
            if self._y < self._fin_y:
                self._y += speed
                self._angle = 180
            elif self._y > self._fin_y:
                self._y -= speed
                self._angle = 0
            else:
                self._current_axis = "_x"

        rotated_tank = pygame.transform.rotate(self._transform_image, self._angle)
        rect = rotated_tank.get_rect(center=(int(self._x), int(self._y)))
        pygame.draw.rect(screen, "red", (self._x - 35, self._y - 55, hp, 10))
        pygame.draw.rect(screen, "white", (self._x - 35, self._y - 70, armor, 10))
        screen.blit(rotated_tank, rect)

        if abs(self._x - self._fin_x) < 1 and abs(self._y - self._fin_y) < 1:
            return -1

    def set_new_point(self, x: int, y: int):
        """
        Устанавливает новую конечную точку для патрулирования.
        :param x: Новая целевая координата X (int).
        :param y: Новая целевая координата Y (int).
        Действия:
            - Обновляет атрибуты self._fin_x и self._fin_y.
             - Сбрасывает текущую ось движения на "_x".
        """
        self._fin_x = x
        self._fin_y = y
        self._current_axis = "_x"


class AttackerStrategy:
    """
    Класс со стратегией пробивания к базе игрока
    """

    def __init__(self, x: int, y: int, fin_x: int, fin_y: int):
        """
        Инициализирует объект стратегии атакующего танка.
        :param x: Начальная координата X танка (int).
        :param y: Начальная координата Y танка (int).
        :param fin_x: Конечная координата X (int).
        :param fin_y: Конечная координата Y (int).
        Атрибуты:
            - self._x, self._y: Текущие координаты танка.
            - self._fin_x, self._fin_y: Целевые координаты.
            - self._angle: Угол поворота танка.
            - self._transform_image: Изображение танка.
            - self._old_x, self._old_y: Предыдущие координаты танка.
            - self._path: Путь, который должен пройти танк.
        """
        self._x = x
        self._y = y
        self._fin_x = fin_x
        self._fin_y = fin_y
        self._angle = 0
        self._image = pygame.image.load("../game_images/opponent_tank.png")
        self._transform_image = pygame.transform.scale(self._image, (75, 75))
        self._old_x = x
        self._old_y = y
        self._path = None

    def get_x(self) -> int:
        """Геттер"""
        return self._x

    def set_x(self, x: int):
        """Сеттер"""
        self._x = x

    def get_y(self) -> int:
        """Геттер"""
        return self._y

    def set_y(self, y: int):
        """Сеттер"""
        self._y = y

    def get_angle(self) -> int:
        """Геттер"""
        return self._angle

    def get_transform_image(self) -> pygame.transform:
        """Геттер"""
        return self._transform_image

    def get_old_x(self) -> int:
        """Геттер"""
        return self._old_x

    def get_old_y(self) -> int:
        """Геттер"""
        return self._old_y

    def find_path(self, map_data: list, start: int, end: int, tank_size=75, cell_size=40) -> list or None:
        """
        Находит путь для танка размером tank_size _x tank_size в
        лабиринте map_data,
        учитывая, что танк центрируется по середине.

        :param map_data: Список строк, представляющий лабиринт.
        :param start: Кортеж (_x, _y) — начальная точка (центр танка).
        :param end: Кортеж (_x', _y') — конечная точка (центр танка).
        :param tank_size: Размер танка (в пикселях).
        :param cell_size: Размер одной клетки лабиринта (в пикселях).
        :return: Список кортежей, представляющих путь, или None,
         если путь не существует.
        """
        obstacles = set("bripw")

        queue = deque([(start[0], start[1])])
        visited = set([(start[0], start[1])])
        parent = {}

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            x, y = queue.popleft()

            if (x, y) == end:
                path = []
                while (x, y) in parent:
                    path.append((x * cell_size, y * cell_size))
                    x, y = parent[(x, y)]
                path.append((start[0] * cell_size, start[1] * cell_size))
                self._path = path[::-1]
                self._fin_x = self._path[0][0]
                self._fin_y = self._path[0][1]
                del self._path[0]

            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if 0 <= nx < len(map_data[0]) and 0 <= ny < len(map_data):

                    is_clear = True

                    tank_left = nx * cell_size - tank_size // 2
                    tank_right = tank_left + tank_size
                    tank_top = ny * cell_size - tank_size // 2
                    tank_bottom = tank_top + tank_size

                    min_cell_x = max(0, tank_left // cell_size)
                    max_cell_x = min(len(map_data[0]) - 1, tank_right // cell_size)
                    min_cell_y = max(0, tank_top // cell_size)
                    max_cell_y = min(len(map_data) - 1, tank_bottom // cell_size)

                    for i in range(min_cell_x, max_cell_x + 1):
                        for j in range(min_cell_y, max_cell_y + 1):
                            if map_data[j][i] in obstacles:
                                is_clear = False
                                break
                        if not is_clear:
                            break

                    if is_clear and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        parent[(nx, ny)] = (x, y)
                        queue.append((nx, ny))

    def update(self, screen: pygame.Surface, speed: float, hp: int, armor: int):
        """
        Обновляет положение танка на экране и его состояние.
        :param screen: Экран, на котором отображается танк (pygame.Surface).
        :param speed: Скорость движения танка (float).
        :param hp: Здоровье танка (int).
        :param armor: Броня танка (int).
        Действия:
            - Перемещает танк вдоль текущего пути.
            - Отображает танк на экране с учетом угла поворота.
            - Обновляет координаты танка в зависимости от текущей цели.
        """
        if len(self._path) != 0 and (self._fin_x == self._x) and (self._fin_y == self._y):
            self._fin_x = self._path[0][0]
            self._fin_y = self._path[0][1]
            del self._path[0]
        self._old_x = self._x
        self._old_y = self._y
        if self._x < self._fin_x:
            self._x += speed
            self._angle = -90
        elif self._x > self._fin_x:
            self._x -= speed
            self._angle = 90

        elif self._y < self._fin_y:
            self._y += speed
            self._angle = 180
        elif self._y >= self._fin_y:
            self._y -= speed
            self._angle = 0

        rotated_tank = pygame.transform.rotate(self._transform_image, self._angle)
        rect = rotated_tank.get_rect(center=(int(self._x), int(self._y)))
        pygame.draw.rect(screen, "red", (self._x - 35, self._y - 55, hp, 10))
        pygame.draw.rect(screen, "white", (self._x - 35, self._y - 70, armor, 10))
        screen.blit(rotated_tank, rect)


class ChaserStrategy:
    """
    Класс со стратегией преследования игрока
    """

    def __init__(self, x: int, y: int, map_data: list):
        """
        Инициализирует объект стратегии преследования игрока.
        :param x: Начальная координата X танка (int).
        :param y: Начальная координата Y танка (int).
        :param map_data: Карта лабиринта, представленная списком строк.
        Атрибуты:
            - self._x, self._y: Текущие координаты танка.
            - self._angle: Угол поворота танка.
            - self._transform_image: Изображение танка.
            - self._grid: Сетка карты, где 1 — непроходимая клетка, 0 — проходимая.
            - self._path: Путь к игроку.
            - self._target_x, self._target_y: Текущая цель танка.
            - self._updatable: Флаг, указывающий, нужно ли обновить путь.
        """
        self._x = x
        self._y = y
        self._angle = 0
        self._image = pygame.image.load("../game_images/opponent_tank.png")
        self._transform_image = pygame.transform.scale(self._image, (75, 75))
        self._grid = None
        self._path = None
        self._target_x = x
        self._target_y = y
        self._updatable = False

        self.create_grid(map_data)

    def get_x(self) -> int:
        """Геттер"""
        return self._x

    def set_x(self, x: int):
        """Сеттер"""
        self._x = x

    def get_y(self) -> int:
        """Геттер"""
        return self._y

    def set_y(self, y: int):
        """Сеттер"""
        self._y = y

    def get_angle(self) -> int:
        """Геттер"""
        return self._angle

    def get_transform_image(self) -> pygame.transform:
        """Геттер"""
        return self._transform_image

    def set_updatable(self, updatable: bool):
        """Сеттер"""
        self._updatable = updatable

    def create_grid(self, map_data: list):
        """
        Создает сетку карты на основе данных лабиринта.
        :param map_data: Карта лабиринта, представленная списком строк.
        Действия:
            - Преобразует символы карты в числовые значения (1 — препятствие, 0 — свободная клетка).
            - Сохраняет сетку в атрибут self._grid.
        """
        grid = []
        for row in map_data:
            grid_row = []
            for cell in row:
                if cell in ["b", "r", "i", "p", "w", "s"]:
                    grid_row.append(1)
                else:
                    grid_row.append(0)
            grid.append(grid_row)
        self._grid = grid

    def heuristic(self, a: tuple, b: tuple) -> int:
        """
        Вычисляет эвристическое расстояние между двумя точками.
        :param a: Координаты первой точки (x1, y1).
        :param b: Координаты второй точки (x2, y2).
        :return: Расстояние Манхэттена между точками.
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star_search(self, start: tuple, goal: tuple) -> list or None:
        """
        Находит путь к цели с использованием алгоритма A*.
        :param start: Начальные координаты (_x, _y).
        :param goal: Целевые координаты (_x', _y').
        :return: Список координат пути или None, если путь не найден.
        """
        neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        closest_point = None
        closest_distance = float("inf")

        while open_set:
            current = heapq.heappop(open_set)[1]

            distance_to_goal = self.heuristic(current, goal)
            if distance_to_goal < closest_distance:
                closest_distance = distance_to_goal
                closest_point = current

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for dx, dy in neighbors:
                neighbor = (current[0] + dx, current[1] + dy)
                tentative_g_score = g_score[current] + 1

                if 0 <= neighbor[0] < len(self._grid) and 0 <= neighbor[1] < len(self._grid[0]):
                    if not self.can_stand_at(neighbor[0], neighbor[1]):
                        continue

                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        if closest_point:
            path = []
            current = closest_point
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        return None

    def is_valid_move(self, new_x: int, new_y: int) -> bool:
        """
        Проверяет, можно ли переместиться в заданную точку.
        :param new_x: Новая координата X (int).
        :param new_y: Новая координата Y (int).
        :return: True, если движение возможно; иначе False.
        """
        tank_size = 75
        half_size = tank_size // 2
        points_to_check = [
            (new_x - half_size, new_y - half_size),
            (new_x + half_size, new_y - half_size),
            (new_x - half_size, new_y + half_size),
            (new_x + half_size, new_y + half_size),
        ]

        for px, py in points_to_check:
            grid_y = py // 40
            grid_x = px // 40
            if not (0 <= grid_y < len(self._grid) and 0 <= grid_x < len(self._grid[0])):
                return False
            if self._grid[grid_y][grid_x] == 1:
                return False
        return True

    def can_stand_at(self, i: int, j: int) -> bool:
        """
        Проверяет, может ли танк находиться в заданной клетке.
        :param i: Индекс строки клетки (int).
        :param j: Индекс столбца клетки (int).
        :return: True, если клетка доступна; иначе False.
        """
        tank_size = 75
        half = tank_size // 2
        center_x = j * 40 + 20
        center_y = i * 40 + 20

        corners = [
            (center_x - half, center_y - half),
            (center_x + half, center_y - half),
            (center_x - half, center_y + half),
            (center_x + half, center_y + half),
        ]

        for px, py in corners:
            grid_i = py // 40
            grid_j = px // 40
            if not (0 <= grid_i < len(self._grid) and 0 <= grid_j < len(self._grid[0])):
                return False
            if self._grid[grid_i][grid_j] == 1:
                return False
        return True

    def update(self, screen: pygame.Surface, speed: float, hp: int, armor: int, player_x: int, player_y: int):
        """
        Обновляет положение танка на экране и его состояние.
        :param screen: Экран, на котором отображается танк (pygame.Surface).
        :param speed: Скорость движения танка (float).
        :param hp: Здоровье танка (int).
        :param armor: Броня танка (int).
        :param player_x: х - координата игрока(int).
        :param player_y: _y - координата игрока(int).
        Действия:
            - Перемещает танк вдоль текущего пути или находит новый путь.
            - Отображает танк на экране с учетом угла поворота.
            - Обновляет координаты танка в зависимости от текущей цели.
        """
        start = (self._y // 40, self._x // 40)
        goal = (player_y // 40, player_x // 40)

        if not self._path or (self._target_x, self._target_y) == (self._x, self._y) or self._updatable:
            self._path = self.a_star_search(start, goal)

            if self._path:
                next_step = self._path[0]
                self._target_x = next_step[1] * 40
                self._target_y = next_step[0] * 40

        if self._path:
            dx = self._target_x - self._x
            dy = self._target_y - self._y

            move_x, move_y = 0, 0
            if abs(dx) > 0:
                move_x = speed if dx > 0 else -speed
            else:
                move_y = speed if dy > 0 else -speed

            if self.is_valid_move(self._x + move_x, self._y + move_y):
                self._x += move_x
                self._y += move_y

            if move_x != 0 or move_y != 0:

                self._angle = math.degrees(math.atan2(-dy, dx))

                if move_x > 0:
                    self._angle = -90
                elif move_x < 0:
                    self._angle = 90
                elif move_y > 0:
                    self._angle = 180
                elif move_y < 0:
                    self._angle = 0
        self._updatable = False

        rotated_tank = pygame.transform.rotate(self._transform_image, self._angle)
        rect = rotated_tank.get_rect(center=(int(self._x), int(self._y)))
        pygame.draw.rect(screen, "red", (self._x - 35, self._y - 55, hp, 10))
        pygame.draw.rect(screen, "white", (self._x - 35, self._y - 70, armor, 10))
        screen.blit(rotated_tank, rect)
