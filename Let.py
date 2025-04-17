import pygame


class Let:
    def __init__(self, strength, x, y):
        self.strength = strength
        self.size = 40
        self.image = None
        self.x = x
        self.y = y


class Brick(Let):
    def __init__(self, strength, x, y):
        super().__init__(strength , x, y)
        self.strength = strength
        brick_image = pygame.image.load("game_images/brick.png")
        self.image = pygame.transform.scale(brick_image, (self.size, self.size))

class Ice(Let):
    def __init__(self,x, y):
        super().__init__(2, x, y)
        brick_image = pygame.image.load("game_images/ice.png")
        self.image = pygame.transform.scale(brick_image, (self.size, self.size))

class Water(Let):
    def __init__(self,x, y):
        super().__init__(999, x, y)
        brick_image = pygame.image.load("game_images/water.png")
        self.image = pygame.transform.scale(brick_image, (self.size, self.size))

class Plant(Let):
    def __init__(self,x, y):
        super().__init__(1, x, y)
        brick_image = pygame.image.load("game_images/plant.png")
        self.image = pygame.transform.scale(brick_image, (self.size, self.size))

class Rock(Let):
    def __init__(self,x, y):
        super().__init__(5, x, y)
        brick_image = pygame.image.load("game_images/rock.jpg")
        self.image = pygame.transform.scale(brick_image, (self.size, self.size))