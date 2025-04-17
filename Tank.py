class DefaultTank:
    def __init__(self, x, y, bullet, direction,strategy):
        self.direction = direction
        self.x = x
        self.y = y
        self.bullet = bullet
        self.speed = 1
        self.attack_speed = 2.5
        self.health_point = 80
        self.armor = 0
        self.strategy = strategy
        self.last_shot = 0
    def update_last_shot(self, time):
        self.last_shot = time


class FastTank(DefaultTank):
    def __init__(self, x, y, bullet,direction, strategy):
        super().__init__(x, y,bullet, direction,strategy)
        self.speed = 1.5


class ArmorTank(DefaultTank):
    def __init__(self, x, y,bullet, direction, strategy):
        super().__init__(x, y,bullet, direction, strategy)
        self.armor = 50


class WeakTank(DefaultTank):
    def __init__(self, x, y,bullet, direction, strategy):
        super().__init__(x, y,bullet, direction, strategy)
        self.bullet = bullet

class RapidFireTank(DefaultTank):
    def __init__(self, x, y,bullet, direction,strategy):
        super().__init__(x, y,bullet, direction, strategy)
        self.attack_speed = 2