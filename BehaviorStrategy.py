import pygame
class PatrolStrategy:
    def __init__(self, x, y, fin_x, fin_y):
        self.x = x
        self.y = y
        self.fin_x = fin_x
        self.fin_y = fin_y
        self.angle = 0
        self.image = pygame.image.load('game_images/opponent_tank.png')
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.current_axis = 'x'  # Текущая ось движения ('x' или 'y')

    def update(self, screen, speed, hp, armor):
        if self.current_axis == 'x':  # Сначала движемся по горизонтали
            if self.x < self.fin_x:
                self.x += speed
                self.angle = -90  # Направление вправо
            elif self.x > self.fin_x:
                self.x -= speed
                self.angle = 90  # Направление влево
            else:
                self.current_axis = 'y'  # Переключаемся на вертикальное движение

        if self.current_axis == 'y':  # Затем движемся по вертикали
            if self.y < self.fin_y:
                self.y += speed
                self.angle = 180  # Направление вниз
            elif self.y > self.fin_y:
                self.y -= speed
                self.angle = 0  # Направление вверх
            else:
                self.current_axis = 'x'  # Переключаемся обратно на горизонтальное движение

        # Отображаем танк на экране
        rotated_tank = pygame.transform.rotate(self.image, self.angle)
        rect = rotated_tank.get_rect(center=(int(self.x), int(self.y)))
        pygame.draw.rect(screen, 'red', (self.x - 35, self.y - 55, hp, 10))
        pygame.draw.rect(screen, 'white', (self.x - 35, self.y - 70, armor, 10))
        screen.blit(rotated_tank, rect)

        # Проверяем, достиг ли танк конечной точки
        if abs(self.x - self.fin_x) < 1 and abs(self.y - self.fin_y) < 1:
            return -1

    def set_new_point(self, x, y):
        self.fin_x = x
        self.fin_y = y
        self.current_axis = 'x'  # Всегда начинаем с горизонтального движения



class AttackerStrategy:
    def __init__(self, x, y, fin_x, fin_y):
        self.x = x
        self.y = y
        self.fin_x = fin_x
        self.fin_y = fin_y
        self.angle = 0
        self.image = pygame.image.load('game_images/opponent_tank.png')
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.current_axis = 'x'  # Текущая ось движения ('x' или 'y')
        self.old_x = x
        self.old_y = y





    def update(self, screen, speed, hp, armor):
        self.old_x = self.x
        self.old_y = self.y
        if self.x < self.fin_x:
            self.x += speed
            self.angle = -90  # Направление вправо
        elif self.x >+ self.fin_x:
            self.x -= speed
            self.angle = 90  # Направление влево


        if self.y < self.fin_y:
            self.y += speed
            self.angle = 180  # Направление вниз
        elif self.y >= self.fin_y:
            self.y -= speed
            self.angle = 0  # Направление вверх



        # Отображаем танк на экране
        rotated_tank = pygame.transform.rotate(self.image, self.angle)
        rect = rotated_tank.get_rect(center=(int(self.x), int(self.y)))
        pygame.draw.rect(screen, 'red', (self.x - 35, self.y - 55, hp, 10))
        pygame.draw.rect(screen, 'white', (self.x - 35, self.y - 70, armor, 10))
        screen.blit(rotated_tank, rect)




