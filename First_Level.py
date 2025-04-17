from collections.abc import Iterator

import pygame
import ctypes
import time
import queue

from BehaviorStrategy import PatrolStrategy, AttackerStrategy
from CyclicIterator import CyclicIterator
from DefaultBullet import *
from Tank import *
from Let import *


def first_level():
    map = [
        'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
        'b                r                  r          b',
        'b    !    !  3   rbbbbbbbbbbbbbbbbbbr   2   3  b',
        'b                                              b',
        'b                @        @#        #          b',
        'b    ! 2  !                            $       b',
        'b                rbbbbbbbbbbbbbbbbbbr       2  b',
        'b    wwwwww      r                  r          b',
        'b 3  wwwwww      r                  r          b',
        'b    wwwwww      r                  r          b',
        'b  rrrrrrrr      r                  r          b',
        'b  r             r                  r          b',
        'b  r             r                  r  $       b',
        'b  r             r                  rrrr   rrrrb',
        'b  r             rp                    r       b',
        'b  r             rp                    r       b',
        'b  r             rp                    r       b',
        'brrr   rrrrrrrrrrrpiiiiiiiiiiiiiiiiiiiirrrrr   b',
        'b             ppppp                            b',
        'b                                              b',
        'b                        u                     b',
        'b                                ppppppppppppppb',
        'bpppppppppp           bbbbbbb    pwwwwwwwwwwwwwb',
        'bwwwwwwwwwp           b     b    pwwwwwwwwwwwwwb',
        'bwwwwwwwwwp           b  d  b    pwwwwwwwwwwwwwb',
        'bwwwwwwwwwp           b     b    pwwwwwwwwwwwwwb',
        'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'
    ]
    SPAWN_X = None
    SPAWN_Y = None
    let_size = 40
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    pygame.init()
    info = pygame.display.Info()
    width = info.current_w
    height = info.current_h
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    pygame.display.set_caption("Battle City")
    running = True

    base_image = pygame.image.load("game_images/base.jfif")
    base_image = pygame.transform.scale(base_image, (100, 100))
    base_pos = None

    player_tank_image = pygame.image.load("game_images/player_tank.png")
    player_tank_image = pygame.transform.scale(player_tank_image, (75, 75))

    back_image = pygame.image.load("game_images/back.png")
    back_image = pygame.transform.scale(back_image, (100, 100))
    back_pos = back_image.get_rect(topleft=(0, -25))

    player_tank = DefaultTank(width // 2, height // 2, ConcretePunchingBullet(width // 2, height // 2, 0), 0, None)

    # Создание списка кирпичей
    lets = []
    opponents = []
    # Верхняя и нижняя границы
    patrol1 = []
    patrol2 = []
    patrol3 = []
    patrol4 = []

    attackers_pos = []

    for y in range(height // let_size):
        for x in range(width // let_size):
            if map[y][x] == 'b' and (x == 0 or y == 0 or x == width // let_size - 1 or y == height // let_size - 1):
                lets.append(Brick(999, x * let_size, y * let_size))
            elif map[y][x] == 'b':
                lets.append(Brick(3, x * let_size, y * let_size))
            elif map[y][x] == 'i':
                lets.append(Ice(x * let_size, y * let_size))
            elif map[y][x] == 'r':
                lets.append(Rock(x * let_size, y * let_size))
            elif map[y][x] == 'p':
                lets.append(Plant(x * let_size, y * let_size))
            elif map[y][x] == 'w':
                lets.append(Water(x * let_size, y * let_size))
            elif map[y][x] == 'd':
                base_pos = base_image.get_rect(center=(x * let_size + let_size // 2, y * let_size + let_size // 2))
            elif map[y][x] == 'u':
                player_tank.x = SPAWN_X = x * let_size + let_size // 2
                player_tank.y = SPAWN_Y = y * let_size + let_size // 2
            elif map[y][x] == '!':
                patrol1.append((x * let_size, y * let_size))
            elif map[y][x] == '@':
                patrol2.append((x * let_size, y * let_size))
            elif map[y][x] == '#':
                patrol3.append((x * let_size, y * let_size))
            elif map[y][x] == '$':
                patrol4.append((x * let_size, y * let_size))
            elif map[y][x] == '2':
                attackers_pos.append((x * let_size, y * let_size))

    bullets = []
    start_time = 0

    patrol_tanks = []

    patrol_tank1 = FastTank(patrol1[0][0], patrol1[0][1], DefaultBullet(patrol1[0][0], patrol1[0][1], 0), 0,
                            PatrolStrategy(patrol1[0][0], patrol1[0][1], patrol1[1][0], patrol1[1][1]))
    iterator1 = CyclicIterator(patrol1)
    patrol_tanks.append((patrol_tank1, iterator1))

    patrol_tank2 = ArmorTank(patrol2[0][0], patrol2[0][1], DefaultBullet(patrol2[0][0], patrol2[0][1], 0), 0,
                             PatrolStrategy(patrol2[0][0], patrol2[0][1], patrol2[1][0], patrol2[1][1]))
    iterator2 = CyclicIterator(patrol2)
    patrol_tanks.append((patrol_tank2, iterator2))

    patrol_tank3 = WeakTank(patrol3[0][0], patrol3[0][1], DefaultBullet(patrol3[0][0], patrol3[0][1], 0), 0,
                            PatrolStrategy(patrol3[0][0], patrol3[0][1], patrol3[1][0], patrol3[1][1]))
    iterator3 = CyclicIterator(patrol3)
    patrol_tanks.append((patrol_tank3, iterator3))

    patrol_tank4 = RapidFireTank(patrol4[0][0], patrol4[0][1], DefaultBullet(patrol4[0][0], patrol4[0][1], 0), 0,
                                 PatrolStrategy(patrol4[0][0], patrol4[0][1], patrol4[1][0], patrol4[1][1]))
    iterator4 = CyclicIterator(patrol4)
    patrol_tanks.append((patrol_tank4, iterator4))

    attackers = []
    for pos in attackers_pos:
        attackers.append(ArmorTank(pos[0], pos[1], ConcretePunchingBullet(pos[0], pos[1], 0), 0,
                                   AttackerStrategy(pos[0], pos[1], base_pos.x, base_pos.y)))

    while running:
        screen.fill("black")
        cooldown = time.time() - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        mouse_pos = pygame.mouse.get_pos()

        if back_pos.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:  # Если нажата левая кнопка мыши
                running = False
        keys = pygame.key.get_pressed()

        original_player_tank_pos = (player_tank.x, player_tank.y)
        if keys[pygame.K_w]:  # Вперёд
            player_tank.y -= player_tank.speed
            player_tank.direction = 0
        elif keys[pygame.K_s]:  # Назад
            player_tank.y += player_tank.speed
            player_tank.direction = 180
        elif keys[pygame.K_a]:  # Влево
            player_tank.x -= player_tank.speed
            player_tank.direction = 90
        elif keys[pygame.K_d]:  # Вправо
            player_tank.x += player_tank.speed
            player_tank.direction = -90
        if keys[pygame.K_SPACE] and cooldown - player_tank.attack_speed >= 0:
            start_time = time.time()
            bullet = player_tank.bullet
            bullet.__init__(original_player_tank_pos[0], original_player_tank_pos[1], player_tank.direction)
            bullets.append((bullet, 1))

        rotated_tank = pygame.transform.rotate(player_tank_image, player_tank.direction)
        new_rect = rotated_tank.get_rect(center=(int(player_tank.x), int(player_tank.y)))

        for tank in attackers:
            for let in lets:
                let_rect = let.image.get_rect(topleft=(let.x, let.y))
                if let.strength <= 0:
                    lets.remove(let)
                    continue
                screen.blit(let.image, let_rect)
                if new_rect.colliderect(let_rect):
                    player_tank.x = original_player_tank_pos[0]
                    player_tank.y = original_player_tank_pos[1]
                if tank.strategy.image.get_rect(center=(int(tank.strategy.x), int(tank.strategy.y))).colliderect(
                    let_rect):
                    tank.strategy.x = tank.strategy.old_x
                    tank.strategy.y = tank.strategy.old_y

        for tank in patrol_tanks:
            res = tank[0].strategy.update(screen, tank[0].speed, tank[0].health_point, tank[0].armor)
            if time.time() - tank[0].last_shot >= tank[0].attack_speed:
                bullets.append((DefaultBullet(tank[0].strategy.x, tank[0].strategy.y,
                                              tank[0].strategy.angle), 2))
                tank[0].update_last_shot(time.time())

            if res == -1:
                new_pos = next(tank[1])
                tank[0].strategy.set_new_point(new_pos[0], new_pos[1])

        for tank in attackers:
            tank.strategy.update(screen, tank.speed, tank.health_point, tank.armor)
            if time.time() - tank.last_shot >= tank.attack_speed:
                bullets.append((ConcretePunchingBullet(tank.strategy.x, tank.strategy.y,
                                                       tank.strategy.angle), 2))
                tank.update_last_shot(time.time())

        new_rect = rotated_tank.get_rect(center=(int(player_tank.x), int(player_tank.y)))
        screen.blit(rotated_tank, new_rect)
        pygame.draw.rect(screen, 'red', (player_tank.x - 35, player_tank.y - 55, player_tank.health_point, 10))
        pygame.draw.rect(screen, 'white', (player_tank.x - 35, player_tank.y - 70, player_tank.armor, 10))

        for bullet in bullets:
            bullet_rect = bullet[0].update(screen)
            if bullet[1] == 2:
                if bullet_rect.colliderect(new_rect):
                    player_tank.health_point -= bullet[0].damage
                    bullets.remove(bullet)
                    if player_tank.health_point <= 0:
                        player_tank.health_point = 80
                        player_tank.x = SPAWN_X
                        player_tank.y = SPAWN_Y

            if bullet[1] == 1:
                for tank in patrol_tanks:
                    if bullet_rect.colliderect(tank[0].strategy.image.get_rect(
                            center=(tank[0].strategy.x, tank[0].strategy.y))):
                        if tank[0].armor > 0:
                            tank[0].armor -= bullet[0].damage
                            bullets.remove(bullet)
                        else:
                            tank[0].health_point -= bullet[0].damage
                            bullets.remove(bullet)
                        if tank[0].armor <= 0 and tank[0].health_point <= 0:
                            patrol_tanks.remove(tank)
            for let in lets:
                let_rect = let.image.get_rect(topleft=(let.x, let.y))
                if bullet_rect.colliderect(let_rect):
                    if bullet[0].can_break_wall and let.strength != 999:
                        let.strength -= 1
                    bullets.remove(bullet)
                    break
        screen.blit(base_image, base_pos)
        screen.blit(back_image, back_pos)
        pygame.display.flip()
