import pygame
class DefaultBullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.bullet_speed = 7.5
        self.bullet_image = pygame.image.load("game_images/bullet.png")
        self.bullet_image = pygame.transform.scale(self.bullet_image, (30, 15))
        self.can_break_wall = False
        self.fire = False
        self.damage = 20

    def update(self,screen):
        if self.direction == 0:
            self.y -= self.bullet_speed
        if self.direction == 180:
            self.y += self.bullet_speed
        if self.direction == 90:
            self.x -= self.bullet_speed
        if self.direction == -90:
            self.x += self.bullet_speed
        rotated_bullet = pygame.transform.rotate(self.bullet_image, self.direction+90)
        bullet_rect = rotated_bullet.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated_bullet,bullet_rect)
        return bullet_rect

class ConcretePunchingBullet(DefaultBullet):
    def __init__(self,x,y, direction):
        super().__init__(x,y,direction)
        self.can_break_wall = True

class IncendiaryBullet(DefaultBullet):
    def __init__(self,x,y, direction):
        super().__init__(x,y,direction)
        self.fire = True
class WeakBullet(DefaultBullet):
    def __init__(self,x,y, direction):
        super().__init__(x,y,direction)
        self.damage = 15
